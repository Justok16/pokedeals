#!/usr/bin/env python3
"""Audit HTTP redirects for a website migration (Python standard library only)."""
from __future__ import annotations

import argparse
import csv
import http.client
import ipaddress
import math
import socket
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

VERSION = "0.4.5"
PERMANENT_REDIRECTS = {301, 308}
REDIRECTS = {301, 302, 303, 307, 308}
USER_AGENT = f"DIG16-Migration-Audit/{VERSION} (+https://dig16.fr)"


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Return 3xx responses to the caller instead of following them implicitly."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: N802
        return None


def normalized_url(value: str) -> str:
    """Normalize only URL components that are safely equivalent for comparison."""
    parsed = urllib.parse.urlsplit(value.strip())
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("seul http:// ou https:// est accepté")
    if not parsed.hostname:
        raise ValueError("nom d'hôte manquant")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("les identifiants intégrés dans l'URL sont interdits")
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("port invalide") from exc
    host = parsed.hostname.lower()
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    if port is not None and not ((parsed.scheme.lower() == "http" and port == 80) or (parsed.scheme.lower() == "https" and port == 443)):
        netloc = f"{host}:{port}"
    else:
        netloc = host
    path = parsed.path or "/"
    # Fragments are not sent in HTTP requests and therefore do not affect redirects.
    return urllib.parse.urlunsplit((parsed.scheme.lower(), netloc, path, parsed.query, ""))



def resolve_destination_ip(url: str, *, allow_private_hosts: bool = False) -> str:
    """Resolve a URL once, validate the IP, and return the exact address to pin."""
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname
    if not host:
        raise ValueError("nom d'hôte manquant")
    port = parsed.port if parsed.port is not None else (443 if parsed.scheme.lower() == "https" else 80)
    try:
        try:
            addresses = [ipaddress.ip_address(host)]
        except ValueError:
            answers = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
            addresses = list(dict.fromkeys(
                ipaddress.ip_address(answer[4][0].split("%", 1)[0]) for answer in answers
            ))
    except (OSError, ValueError) as exc:
        raise ValueError(f"résolution DNS impossible: {exc}") from exc
    if not addresses:
        raise ValueError("aucune adresse IP résolue")
    blocked = sorted(str(address) for address in addresses if not address.is_global)
    if blocked and not allow_private_hosts:
        raise ValueError("destination non publique bloquée: " + ", ".join(blocked))
    # Pin the socket to an IP from the validated DNS answer. This avoids a
    # second DNS lookup during connect and closes the common rebinding window.
    return str(addresses[0])


def assert_public_destination(url: str, *, allow_private_hosts: bool = False) -> None:
    """Validate that a URL resolves only to globally routable addresses."""
    resolve_destination_ip(url, allow_private_hosts=allow_private_hosts)


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host, pinned_ip, **kwargs):
        self._pinned_ip = pinned_ip
        super().__init__(host, **kwargs)

    def connect(self):
        self.sock = socket.create_connection((self._pinned_ip, self.port), self.timeout, self.source_address)
        try:
            self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except OSError:
            pass
        if self._tunnel_host:
            self._tunnel()


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, pinned_ip, **kwargs):
        self._pinned_ip = pinned_ip
        super().__init__(host, **kwargs)

    def connect(self):
        sock = socket.create_connection((self._pinned_ip, self.port), self.timeout, self.source_address)
        try:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except OSError:
            pass
        if self._tunnel_host:
            self._tunnel()
        self.sock = self._context.wrap_socket(sock, server_hostname=self._tunnel_host or self.host)


class _PinnedHTTPHandler(urllib.request.HTTPHandler):
    def __init__(self, pinned_ip):
        super().__init__()
        self._pinned_ip = pinned_ip

    def http_open(self, req):
        return self.do_open(
            lambda host, **kwargs: _PinnedHTTPConnection(host, self._pinned_ip, **kwargs), req
        )


class _PinnedHTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, pinned_ip):
        super().__init__(context=ssl.create_default_context())
        self._pinned_ip = pinned_ip

    def https_open(self, req):
        return self.do_open(
            lambda host, **kwargs: _PinnedHTTPSConnection(host, self._pinned_ip, **kwargs),
            req,
            context=self._context,
        )


def validate_url(value: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError("URL vide")
    normalized_url(value)
    return value


@dataclass
class AuditResult:
    old_url: str
    expected_url: str
    outcome: str
    flags: str
    redirect_count: int
    redirect_statuses: str
    final_status: str
    final_url: str
    chain: str
    detail: str


def _request_once(opener: urllib.request.OpenerDirector, url: str, timeout: float):
    """Make a HEAD request; retry as GET when the server refuses HEAD."""
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(
            url,
            method=method,
            headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
        )
        try:
            with opener.open(request, timeout=timeout) as response:
                return response.status, response.headers, response.geturl(), method
        except urllib.error.HTTPError as exc:
            status, headers = exc.code, exc.headers
            exc.close()
            if method == "HEAD" and status in {405, 501}:
                continue
            return status, headers, url, method
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            raise RuntimeError(f"{type(reason).__name__}: {reason}") from exc
    raise RuntimeError("échec de la requête")


def audit_one(old_url: str, expected_url: str, timeout: float = 12.0, max_redirects: int = 10, *, allow_private_hosts: bool = False) -> AuditResult:
    flags: list[str] = []
    redirects: list[int] = []
    chain: list[str] = []
    current = old_url
    seen: set[str] = set()
    final_status: int | str = ""
    final_url = current
    detail = ""
    try:
        old_norm = normalized_url(old_url)
        expected_norm = normalized_url(expected_url)
    except ValueError as exc:
        return AuditResult(old_url, expected_url, "ERROR", "INVALID_URL", 0, "", "", "", "", str(exc))

    for hop in range(max_redirects + 1):
        try:
            current_norm = normalized_url(current)
        except ValueError as exc:
            flags.append("INVALID_REDIRECT_TARGET")
            detail = str(exc)
            break
        if current_norm in seen:
            flags.append("REDIRECT_LOOP")
            detail = "une URL déjà visitée a été rencontrée"
            break
        seen.add(current_norm)
        chain.append(current)

        try:
            pinned_ip = resolve_destination_ip(current, allow_private_hosts=allow_private_hosts)
        except ValueError as exc:
            flags.append("BLOCKED_PRIVATE_OR_UNRESOLVABLE_HOST")
            detail = str(exc)
            break

        # Disable environment proxies and connect to the exact IP already
        # validated above; TLS still verifies the original hostname.
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            NoRedirectHandler(),
            _PinnedHTTPHandler(pinned_ip),
            _PinnedHTTPSHandler(pinned_ip),
        )
        try:
            status, headers, response_url, method = _request_once(opener, current, timeout)
        except RuntimeError as exc:
            flags.append("REQUEST_ERROR")
            detail = str(exc)
            break

        final_status = status
        final_url = response_url or current
        if status in REDIRECTS:
            location = headers.get("Location") if headers else None
            if not location:
                flags.append("REDIRECT_WITHOUT_LOCATION")
                detail = f"réponse HTTP {status} sans en-tête Location"
                break
            redirects.append(status)
            target = urllib.parse.urljoin(current, location)
            try:
                normalized_url(target)
            except ValueError as exc:
                flags.append("INVALID_REDIRECT_TARGET")
                detail = str(exc)
                final_url = target
                break
            if hop >= max_redirects:
                flags.append("TOO_MANY_REDIRECTS")
                detail = f"limite de {max_redirects} redirections atteinte"
                final_url = target
                break
            if normalized_url(target) in seen:
                flags.append("REDIRECT_LOOP")
                detail = "la redirection revient vers une URL déjà visitée"
                final_url = target
                break
            if urllib.parse.urlsplit(current).scheme.lower() == "https" and urllib.parse.urlsplit(target).scheme.lower() == "http":
                flags.append("HTTPS_DOWNGRADE")
            current = target
            continue

        if status < 200 or status >= 300:
            flags.append("FINAL_HTTP_ERROR")
            detail = f"destination finale en HTTP {status} (requête {method})"
        break

    if redirects and any(code not in PERMANENT_REDIRECTS for code in redirects):
        flags.append("NON_PERMANENT_REDIRECT")
    if len(redirects) > 1:
        flags.append("REDIRECT_CHAIN")
    if len(redirects) >= 5:
        flags.append("LONG_REDIRECT_CHAIN")
    try:
        final_norm = normalized_url(final_url)
    except ValueError:
        final_norm = ""
    if not redirects and old_norm != expected_norm and final_status != "":
        flags.append("MISSING_REDIRECT")
    elif final_norm and final_norm != expected_norm and not any(
        flag in flags for flag in {
            "REDIRECT_LOOP", "REQUEST_ERROR", "BLOCKED_PRIVATE_OR_UNRESOLVABLE_HOST",
            "REDIRECT_WITHOUT_LOCATION", "INVALID_REDIRECT_TARGET", "TOO_MANY_REDIRECTS",
        }
    ):
        flags.append("WRONG_DESTINATION")

    # Avoid duplicate flags while preserving diagnostic order.
    flags = list(dict.fromkeys(flags))
    failures = {
        "INVALID_URL", "INVALID_REDIRECT_TARGET", "REDIRECT_LOOP", "TOO_MANY_REDIRECTS",
        "REDIRECT_WITHOUT_LOCATION", "REQUEST_ERROR", "FINAL_HTTP_ERROR", "MISSING_REDIRECT",
        "WRONG_DESTINATION", "NON_PERMANENT_REDIRECT", "BLOCKED_PRIVATE_OR_UNRESOLVABLE_HOST",
        "HTTPS_DOWNGRADE", "LONG_REDIRECT_CHAIN",
    }
    blocking = [flag for flag in flags if flag in failures]
    outcome = "ERROR" if any(flag in flags for flag in {"INVALID_URL", "REQUEST_ERROR", "BLOCKED_PRIVATE_OR_UNRESOLVABLE_HOST"}) else ("FAIL" if blocking else ("WARNING" if flags else "PASS"))
    return AuditResult(
        old_url=old_url,
        expected_url=expected_url,
        outcome=outcome,
        flags=";".join(flags),
        redirect_count=len(redirects),
        redirect_statuses=";".join(map(str, redirects)),
        final_status=str(final_status),
        final_url=final_url,
        chain=" -> ".join(chain + ([final_url] if final_url and (not chain or chain[-1] != final_url) else [])),
        detail=detail,
    )


def load_mappings(path: Path) -> list[tuple[str, str, str | None]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(8192)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(
            handle, dialect=dialect, restkey="__extra_fields__", restval=None, strict=True
        )
        if reader.fieldnames:
            normalized_headers = [name.strip().lower() for name in reader.fieldnames]
            if len(set(normalized_headers)) != len(normalized_headers):
                raise ValueError("le CSV contient des noms de colonnes en double")
            reader.fieldnames = normalized_headers
        required = {"old_url", "new_url"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("le CSV doit contenir les colonnes old_url et new_url")
        rows = []
        try:
            for row in reader:
                old_value = row.get("old_url")
                new_value = row.get("new_url")
                old = old_value.strip() if isinstance(old_value, str) else ""
                new = new_value.strip() if isinstance(new_value, str) else ""
                if not old and not new and not row.get("__extra_fields__"):
                    continue
                if row.get("__extra_fields__") is not None:
                    rows.append((old, new, f"Ligne {reader.line_num}: colonnes supplémentaires inattendues"))
                    continue
                try:
                    validate_url(old)
                    validate_url(new)
                    rows.append((old, new, None))
                except ValueError as exc:
                    rows.append((old, new, f"Ligne {reader.line_num}: {exc}"))
        except csv.Error as exc:
            raise ValueError(f"CSV mal formé à la ligne {reader.line_num}: {exc}") from exc
        if not rows:
            raise ValueError("le CSV ne contient aucune correspondance")

    # Conflicting destinations for the same source URL are never sent to the network.
    destinations: dict[str, set[str]] = {}
    for old, new, error in rows:
        if error is None:
            destinations.setdefault(normalized_url(old), set()).add(normalized_url(new))
    final_rows = []
    seen_pairs: set[tuple[str, str]] = set()
    for old, new, error in rows:
        if error is None and len(destinations[normalized_url(old)]) > 1:
            error = "Correspondances contradictoires: une même ancienne URL cible plusieurs nouvelles URL"
        if error is None:
            pair = (normalized_url(old), normalized_url(new))
            if pair in seen_pairs:
                error = "DUPLICATE_MAPPING: cette correspondance apparaît plusieurs fois dans le CSV"
            else:
                seen_pairs.add(pair)
        final_rows.append((old, new, error))
    return final_rows


def _excel_safe_cell(value: object) -> object:
    """Neutralize cells that spreadsheet software could interpret as formulas."""
    if not isinstance(value, str) or not value:
        return value
    significant = value.lstrip(" \t\r\n")
    if significant.startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n")):
        return "'" + value
    return value


def write_report(results: Iterable[AuditResult], output_path: Path) -> None:
    fields = list(AuditResult.__dataclass_fields__.keys())
    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter=";")
        writer.writeheader()
        for result in results:
            row = asdict(result)
            writer.writerow({key: _excel_safe_cell(value) for key, value in row.items()})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Contrôle les redirections HTTP d'une migration de site.")
    parser.add_argument("--version", action="version", version=f"DIG16 Migration Audit {VERSION}")
    parser.add_argument("csv_file", type=Path, help="CSV avec les colonnes old_url,new_url")
    parser.add_argument("-o", "--output", type=Path, default=Path("rapport_migration.csv"), help="rapport CSV de sortie")
    parser.add_argument("--timeout", type=float, default=12.0, help="délai maximal par requête en secondes (défaut: 12)")
    parser.add_argument("--max-redirects", type=int, default=10, help="nombre maximal de redirections suivies (défaut: 10)")
    parser.add_argument("--allow-private-hosts", action="store_true", help="autorise les IP privées pour un environnement de préproduction maîtrisé")
    args = parser.parse_args(argv)
    if sys.version_info < (3, 11):
        parser.error("Python 3.11 ou supérieur est requis")
    if not math.isfinite(args.timeout) or args.timeout <= 0 or args.max_redirects < 0:
        parser.error("--timeout doit être un nombre fini positif et --max-redirects positif ou nul")
    try:
        same_file = False
        if args.csv_file.exists() and args.output.exists():
            try:
                same_file = args.csv_file.samefile(args.output)
            except OSError:
                same_file = False
        if args.csv_file.resolve() == args.output.resolve() or same_file:
            raise ValueError("le rapport de sortie ne peut pas écraser le CSV source")
        mappings = load_mappings(args.csv_file)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Erreur d'entrée: {exc}", file=sys.stderr)
        return 2

    results: list[AuditResult] = []
    for old, new, validation_error in mappings:
        if validation_error:
            if validation_error.startswith("DUPLICATE_MAPPING:"):
                results.append(AuditResult(old, new, "WARNING", "DUPLICATE_MAPPING", 0, "", "", "", "", validation_error))
            else:
                results.append(AuditResult(old, new, "ERROR", "INVALID_MAPPING", 0, "", "", "", "", validation_error))
        else:
            results.append(audit_one(old, new, timeout=args.timeout, max_redirects=args.max_redirects, allow_private_hosts=args.allow_private_hosts))

    try:
        write_report(results, args.output)
    except OSError as exc:
        print(f"Impossible d'écrire le rapport: {exc}", file=sys.stderr)
        return 2

    counts = {name: sum(result.outcome == name for result in results) for name in ("PASS", "WARNING", "FAIL", "ERROR")}
    print(f"Audit terminé: {len(results)} correspondance(s)")
    print(" | ".join(f"{key}: {value}" for key, value in counts.items()))
    print(f"Rapport: {args.output.resolve()}")
    return 1 if counts["FAIL"] or counts["ERROR"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
