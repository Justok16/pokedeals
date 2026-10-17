#!/usr/bin/env python3
"""Passe les supports écrits à la main (supports/*.html) à la charte premium du 08/10/2026.

Usage : python3 outils/marque/restyler_supports.py [fichier.html ...]   (sans argument : tous les SUPPORTS)
Remplace polices (Fraunces → Instrument Serif, Inter → Geist) et couleurs (bleu nuit, orange, violet,
vert → noir chaud, laiton, bronze), remplace l'ancien logo « D » par la signature DIG16 et ajoute un bloc
de style commun (<style id="charte-dig16">). Sans effet si on le relance (idempotent).
Les PDF se refont ensuite avec outils/marque/pdf_supports.py.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from charte_documents import MARQUE, POLICES  # noqa: E402

SUP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "supports"))

SUPPORTS = [
    "antiseche-reponses.html",
    "guide-prospection.html",
    "questionnaire-decouverte.html",
    "questionnaire-lancement-site.html",
    "visuel-lancement.html",
    "audit-interne-claude.html",
    "guide-jarvis.html",
    "guide-minimax-h3.html",
]

COULEURS = {
    # fonds sombres
    "#0d1330": "#0f0e0c", "#0f1b3d": "#0f0e0c", "#0b1020": "#0f0e0c", "#0f172a": "#1a1814",
    "#14254f": "#181613", "#0b1430": "#0c0b09", "#1f2937": "#181613", "#12100d": "#0f0e0c",
    "#1f3b2d": "#1a1814", "#1d1a17": "#1a1814", "#1f1b16": "#1a1814",
    # accents
    "#ff8a3d": "#c8a46e", "#ffb35c": "#d9bb8a", "#ffcf5c": "#d9bb8a", "#ff7d5a": "#d9bb8a",
    "#c98a4b": "#c8a46e", "#f59e6b": "#c8a46e", "#ff6f91": "#d9bb8a", "#c056e0": "#d9bb8a",
    "#7b5cff": "#7a5a2c", "#4fa3ff": "#c8a46e", "#16c79a": "#c8a46e", "#0ea5a4": "#7a5a2c",
    "#c2410c": "#7a5a2c", "#b44d0f": "#7a5a2c", "#9a3412": "#7a5a2c", "#0e7490": "#7a5a2c",
    # clairs et gris
    "#c6cbe4": "#a8a093", "#e7e4f2": "#e6dfd3", "#f4f1ea": "#efe9df", "#faf7f2": "#f6f2ea",
    "#e8e1d6": "#e0d8cb", "#fff4ec": "#f6f0e4", "#ffd2b5": "#e3d3b6", "#fff7ed": "#f6f0e4",
    "#fed7aa": "#e3d3b6", "#fff1e6": "#f6f0e4", "#eef0f6": "#f3eee5", "#5d5a66": "#655e54",
    "#9a93a6": "#8c8478", "#8c93b8": "#8c8478", "#7a7480": "#6f675c", "#e2e8f0": "#e0d8cb",
    "#f8fafc": "#f6f2ea", "#475569": "#655e54", "#dfe4f2": "#e6dfd3", "#7c86a3": "#a8a093",
    "#e3e6ef": "#e0d8cb", "#d6def5": "#cfc7b9", "#c9d3ee": "#cfc7b9", "#aab5d6": "#a8a093",
    "#4b5570": "#655e54", "#2c3a66": "#3a342b", "#0a0f1f": "#060605", "#f1e7da": "#f3eee5",
    "#e7e0d5": "#e0d8cb", "#6b645a": "#655e54", "#8a8176": "#8c8478",
    "#1f4fd1": "#181613", "#0b8a5f": "#7a5a2c",
}
RGBA = {
    "255,138,61": "200,164,110", "123,92,255": "200,164,110", "22,199,154": "200,164,110",
    "255,111,145": "200,164,110", "13,19,48": "15,14,12",
}

COMMUN = """
body{font-family:Geist,Arial,sans-serif}
h1,h2,h3{font-family:'Instrument Serif',Georgia,serif}
h1,h2,h3,.logo{font-weight:400!important}
h1,h2{letter-spacing:-.008em}
.k,h2 small,.qui,th,.etiquette{font-family:'Geist Mono',monospace!important;font-weight:400!important}
.degrade{color:#d9bb8a!important}
img.signature-dig16{display:block;height:13mm;width:auto;align-self:flex-start}
"""


def restyler(chemin):
    html = open(chemin, encoding="utf-8").read()
    html = re.sub(r'<style id="charte-dig16">.*?</style>', "", html, flags=re.S)
    html = re.sub(r'<link rel="preconnect" href="https://fonts.googleapis.com">', "", html)
    html = re.sub(r'<link href="https://fonts.googleapis.com/css2\?[^"]*" rel="stylesheet">', "", html)
    html = html.replace("</head>", POLICES + "</head>", 1) if POLICES not in html else html
    html = re.sub(r"\bFraunces\b", "'Instrument Serif'", html)
    html = html.replace("''Instrument Serif''", "'Instrument Serif'")
    html = re.sub(r"(?<![\w-])Inter(?=[,;\"'}\s])", "Geist", html)
    for a, b in COULEURS.items():
        html = re.sub(re.escape(a) + r"\b", b, html, flags=re.I)
    for a, b in RGBA.items():
        html = re.sub(r"rgba\(\s*" + a.replace(",", r"\s*,\s*") + r"\s*,", "rgba(" + b + ",", html)
    # ancien logo « D » en dégradé : remplacé par la signature
    html = re.sub(
        r'<div class="logo"><i>D</i>\s*DIG16</div>',
        f'<img class="signature-dig16" src="{MARQUE}signature-ivoire@6x.png" alt="DIG16, sites internet">',
        html,
    )
    html = html.replace("</head>", f'<style id="charte-dig16">{COMMUN}</style></head>', 1)
    open(chemin, "w", encoding="utf-8").write(html)
    return chemin


if __name__ == "__main__":
    for f in sys.argv[1:] or SUPPORTS:
        print("restylé :", restyler(os.path.join(SUP, os.path.basename(f))))
