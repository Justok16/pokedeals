#!/usr/bin/env python3
"""Traces d'un autre client dans un site DIG16 (27/10/2026), avant toute livraison ou démo.

Un site client est souvent bâti à partir d'un modèle ou d'un autre site : ce contrôle cherche, dans les fichiers du
site, le nom, le domaine ou les couleurs d'un AUTRE client ou du modèle (y compris dans les noms de fichiers et les
identifiants) et sort en erreur (code 1) s'il en trouve. À lancer sur le dossier du site, avec la liste des noms à
exclure, par exemple :
    python3 outils/traces_autre_client.py <dossier du site> --avoid "FD Touchatou,Touchatou" --domains exemple.fr
Repris tel quel de `replica-brand/sweep.py` (dépôt Jakeschincariol/replica-skill, licence MIT, lu en entier le 27/10 :
bibliothèque standard seulement, aucun accès réseau). Licence d'origine en fin de fichier.
"""
# Docstring d'origine (anglais) : recherche du nom, du domaine et des couleurs de l'original ; code 1 si trouvé.


import argparse
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", ".next", ".nuxt", ".svelte-kit", "dist", "build",
             "out", ".vercel", ".turbo", ".cache", "coverage", "__pycache__", ".venv",
             "venv", "Pods", ".expo", "DerivedData", ".gradle"}
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
              "Podfile.lock", "Cargo.lock", "poetry.lock"}
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".icns", ".pdf", ".zip",
              ".gz", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".mov", ".mp3",
              ".wav", ".avif", ".heic", ".psd", ".sketch", ".fig", ".jar", ".so", ".dylib"}
HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z])")
BINARY_ASSET_HINT = re.compile(r"\.(png|jpe?g|svg|webp|gif|ico|woff2?|ttf|otf)$", re.IGNORECASE)


def norm_hex(h):
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h


def build_patterns(avoid, domains):
    pats = []
    for name in avoid:
        name = name.strip()
        if not name:
            continue
        # "Acuity Scheduling" also matches AcuityScheduling and acuity-scheduling
        parts = [re.escape(p) for p in re.split(r"[\s_-]+", name) if p]
        pats.append(("name", name, re.compile(r"[\s_-]?".join(parts), re.IGNORECASE)))
    for d in domains:
        d = d.strip().lower()
        if d:
            pats.append(("domain", d, re.compile(re.escape(d), re.IGNORECASE)))
    return pats


def is_binary(path):
    if os.path.splitext(path)[1].lower() in BINARY_EXT:
        return True
    try:
        with open(path, "rb") as fh:
            return b"\0" in fh.read(4096)
    except OSError:
        return True


def sweep(root, avoid=(), domains=(), colors=(), include_replica=False, max_size=2_000_000):
    pats = build_patterns(avoid, domains)
    cols = {norm_hex(c) for c in colors if HEX.fullmatch(c.strip())}
    hits = []
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        keep = []
        for d in dirnames:
            if d in SKIP_DIRS:
                continue
            if d == "replica" and rel_dir == "." and not include_replica:
                continue
            keep.append(d)
        dirnames[:] = sorted(keep)
        for d in dirnames:
            for kind, label, rx in pats:
                if kind == "name" and rx.search(d):
                    hits.append({"file": os.path.normpath(os.path.join(rel_dir, d)) + "/",
                                 "line": 0, "kind": "path", "match": label,
                                 "text": "folder name"})
        for fn in sorted(filenames):
            if fn in SKIP_FILES:
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.normpath(os.path.join(rel_dir, fn))
            for kind, label, rx in pats:
                if kind == "name" and rx.search(fn):
                    hits.append({"file": rel, "line": 0, "kind": "path", "match": label,
                                 "text": "file name"})
            try:
                if os.path.getsize(path) > max_size or is_binary(path):
                    continue
                with open(path, encoding="utf-8", errors="replace") as fh:
                    lines = fh.readlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                for kind, label, rx in pats:
                    if rx.search(line):
                        hits.append({"file": rel, "line": i, "kind": kind, "match": label,
                                     "text": line.strip()[:160]})
                if cols:
                    for m in HEX.finditer(line):
                        if norm_hex(m.group(0)) in cols:
                            hits.append({"file": rel, "line": i, "kind": "color",
                                         "match": norm_hex(m.group(0)),
                                         "text": line.strip()[:160]})
    return hits


def render(hits):
    if not hits:
        return "Clean. Nothing of the original's name, domain or colours found."
    out = []
    by_kind = {}
    for h in hits:
        by_kind.setdefault(h["kind"], 0)
        by_kind[h["kind"]] += 1
        loc = h["file"] if not h["line"] else f"{h['file']}:{h['line']}"
        out.append(f"{h['kind']:<7} {h['match'][:18]:<18} {loc}  {h['text']}")
    out.append("")
    out.append("{} hits ({}). Replace every one before you launch.".format(
        len(hits), ", ".join(f"{k} {v}" for k, v in sorted(by_kind.items()))))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Traces d'un autre client dans un site DIG16")
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--avoid", default="", help="comma-separated names")
    ap.add_argument("--domains", default="", help="comma-separated domains")
    ap.add_argument("--colors", default="", help="comma-separated hex colours")
    ap.add_argument("--config", help="JSON with avoid / domains / colors lists")
    ap.add_argument("--include-replica", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    avoid = [x for x in args.avoid.split(",") if x.strip()]
    domains = [x for x in args.domains.split(",") if x.strip()]
    colors = [x for x in args.colors.split(",") if x.strip()]
    if args.config:
        try:
            with open(args.config, encoding="utf-8") as fh:
                cfg = json.load(fh)
        except (OSError, ValueError) as exc:
            print(f"sweep: {exc}", file=sys.stderr)
            return 2
        avoid += cfg.get("avoid", [])
        domains += cfg.get("domains", [])
        colors += cfg.get("colors", [])
    if not (avoid or domains or colors):
        print("sweep: nothing to look for. Pass --avoid with the original app's name.",
              file=sys.stderr)
        return 2
    hits = sweep(args.root, avoid, domains, colors, args.include_replica)
    print(json.dumps(hits, indent=2) if args.json else render(hits))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())

# --- Licence d'origine (MIT) ---
# MIT License
#
# Copyright (c) 2026 Jake Schincariol
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
