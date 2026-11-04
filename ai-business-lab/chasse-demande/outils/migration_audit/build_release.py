#!/usr/bin/env python3
"""Build a deterministic ZIP release and verify its internal SHA-256 manifest."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", "build", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
MANIFEST_NAME = "MANIFEST.sha256"
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_included(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    if path.name == MANIFEST_NAME:
        return False
    if path.is_symlink() or not path.is_file():
        return False
    return True


def _source_files(root: Path) -> list[Path]:
    return sorted(
        (p for p in root.rglob("*") if _is_included(p, root)),
        key=lambda p: p.relative_to(root).as_posix(),
    )


def _manifest_text(root: Path, files: list[Path]) -> str:
    lines = [f"{sha256_bytes(path.read_bytes())}  {path.relative_to(root).as_posix()}" for path in files]
    return "\n".join(lines) + "\n"


def verify_archive(archive_path: Path) -> list[str]:
    """Verify ZIP integrity, a single package root, and every manifest digest."""
    with zipfile.ZipFile(archive_path, "r") as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"CRC invalide dans l'archive: {bad_member}")
        names = [info.filename for info in archive.infolist() if not info.is_dir()]
        if len(names) != len(set(names)):
            raise ValueError("membre de fichier dupliqué dans l'archive ZIP")
        if not names:
            raise ValueError("archive vide")
        roots = {name.split("/", 1)[0] for name in names if "/" in name}
        if len(roots) != 1 or any("/" not in name for name in names):
            raise ValueError("l'archive doit contenir un seul dossier racine")
        root_name = next(iter(roots))
        manifest_member = f"{root_name}/{MANIFEST_NAME}"
        if manifest_member not in names:
            raise ValueError("MANIFEST.sha256 absent")
        manifest = archive.read(manifest_member).decode("utf-8")
        listed: set[str] = set()
        for line_number, line in enumerate(manifest.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                digest, relative = line.split("  ", 1)
            except ValueError as exc:
                raise ValueError(f"ligne {line_number} invalide dans le manifeste") from exc
            relative_path = PurePosixPath(relative)
            if relative_path.is_absolute() or ".." in relative_path.parts or not relative:
                raise ValueError(f"chemin interdit dans le manifeste: {relative}")
            member = f"{root_name}/{relative_path.as_posix()}"
            if member not in names or member == manifest_member:
                raise ValueError(f"fichier absent ou invalide dans le manifeste: {relative}")
            if member in listed:
                raise ValueError(f"fichier dupliqué dans le manifeste: {relative}")
            listed.add(member)
            actual = sha256_bytes(archive.read(member))
            if actual != digest:
                raise ValueError(f"empreinte incorrecte: {relative}")
        packaged = set(names) - {manifest_member}
        if listed != packaged:
            missing = sorted(packaged - listed)
            extra = sorted(listed - packaged)
            raise ValueError(f"manifeste incomplet (non listés: {missing}; inattendus: {extra})")
        return sorted(names)


def verify_sidecar(archive_path: Path) -> str:
    sidecar = Path(str(archive_path) + ".sha256")
    try:
        content = sidecar.read_text(encoding="ascii").strip()
    except UnicodeError as exc:
        raise ValueError("le fichier SHA-256 externe n'est pas ASCII") from exc
    parts = content.split(maxsplit=1)
    if len(parts) != 2 or re.fullmatch(r"[0-9a-f]{64}", parts[0]) is None:
        raise ValueError("format du fichier SHA-256 externe invalide")
    expected, named_file = parts
    if named_file.strip() != archive_path.name:
        raise ValueError("le fichier SHA-256 externe ne désigne pas le bon ZIP")
    actual = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError("l'empreinte SHA-256 externe ne correspond pas à l'archive")
    return actual


def build_release(source_dir: Path, output_path: Path) -> str:
    root = source_dir.resolve()
    output = output_path.resolve()
    if not root.is_dir():
        raise ValueError(f"dossier source introuvable: {root}")
    if output == root or root in output.parents:
        raise ValueError("le ZIP et son fichier SHA-256 doivent être créés hors du dossier source")
    output.parent.mkdir(parents=True, exist_ok=True)

    files = _source_files(root)
    if not files:
        raise ValueError("aucun fichier source à empaqueter")
    (root / MANIFEST_NAME).write_text(_manifest_text(root, files), encoding="utf-8", newline="\n")
    package_files = sorted(
        (p for p in root.rglob("*") if p.is_file() and not p.is_symlink()
         and not any(part in EXCLUDED_DIRS for part in p.relative_to(root).parts)
         and p.suffix.lower() not in EXCLUDED_SUFFIXES),
        key=lambda p: p.relative_to(root).as_posix(),
    )

    fd, temp_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=".tmp", dir=output.parent)
    os.close(fd)
    temp_path = Path(temp_name)
    try:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in package_files:
                relative = path.relative_to(root).as_posix()
                info = zipfile.ZipInfo(f"{root.name}/{relative}", date_time=ZIP_EPOCH)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (0o100644) << 16
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        verify_archive(temp_path)
        os.replace(temp_path, output)
    finally:
        if temp_path.exists():
            temp_path.unlink()

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    sidecar = Path(str(output) + ".sha256")
    sidecar.write_text(f"{digest}  {output.name}\n", encoding="ascii", newline="\n")
    verify_sidecar(output)
    return digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Construit et vérifie une archive ZIP DIG16 reproductible.")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent, help="dossier du projet")
    parser.add_argument("--output", type=Path, required=True, help="ZIP de sortie (hors du dossier source)")
    args = parser.parse_args(argv)
    try:
        digest = build_release(args.source, args.output)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        parser.exit(2, f"Erreur de release: {exc}\n")
    print(f"Archive vérifiée: {args.output.resolve()}")
    print(f"SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
