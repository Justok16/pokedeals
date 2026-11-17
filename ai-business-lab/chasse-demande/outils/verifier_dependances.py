#!/usr/bin/env python3
"""Vérifie que chaque module importé par les outils DIG16 (outils/, videos/) est installé (17/11/2026).

Né d'une panne silencieuse : la transcription de secours manquait après un redémarrage du conteneur.
Sortie 0 si tout est présent, 1 sinon (liste des modules manquants et des fichiers qui les importent).
Correction : ajouter le module à outils/requirements.txt (installé au démarrage), puis pip install.
"""
import ast
import importlib.util
import os
import sys
import warnings

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)


def locaux():
    noms = set()
    for d, _, fs in os.walk(RACINE):
        if "__pycache__" in d or "/." in d:
            continue
        noms.update(f[:-3] for f in fs if f.endswith(".py"))
        noms.update(os.path.basename(x) for x in [d])
    return noms


def main():
    loc, manque = locaux(), {}
    for racine in ("outils", "videos"):
        for d, _, fs in os.walk(os.path.join(RACINE, racine)):
            if "__pycache__" in d:
                continue
            for f in fs:
                if not f.endswith(".py"):
                    continue
                p = os.path.join(d, f)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    try:
                        arbre = ast.parse(open(p, encoding="utf-8").read())
                    except SyntaxError:
                        manque.setdefault("(erreur de syntaxe)", set()).add(os.path.relpath(p, RACINE))
                        continue
                for n in ast.walk(arbre):
                    if isinstance(n, ast.Import):
                        mods = [a.name.split(".")[0] for a in n.names]
                    elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                        mods = [n.module.split(".")[0]]
                    else:
                        continue
                    for m in mods:
                        if m in sys.stdlib_module_names or m in loc:
                            continue
                        if importlib.util.find_spec(m) is None:
                            manque.setdefault(m, set()).add(os.path.relpath(p, RACINE))
    for m, fichiers in sorted(manque.items()):
        print(f"{m} : {', '.join(sorted(fichiers)[:3])}")
    print("toutes les dépendances sont installées" if not manque else f"{len(manque)} module(s) manquant(s)")
    return 1 if manque else 0


if __name__ == "__main__":
    sys.exit(main())
