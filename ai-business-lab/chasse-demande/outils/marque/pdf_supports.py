#!/usr/bin/env python3
"""Refait les PDF (et le visuel PNG) des supports écrits à la main, après restyler_supports.py.

Usage : python3 outils/marque/pdf_supports.py
Supports à pages fixes (section.page) : contrôle de débordement de outils/pdf_pages.py.
Autres : PDF A4 après chargement des polices. Affiche le nombre de pages de chaque PDF.
"""

import os
import sys

import pymupdf
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, ".."))
from charte_documents import attendre_polices  # noqa: E402
from pdf_pages import MESURE  # noqa: E402

SUP = os.path.normpath(os.path.join(ICI, "..", "..", "supports"))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

PDF = {
    "antiseche-reponses.html": "Dig-Antiseche-reponses.pdf",
    "guide-prospection.html": "Dig-Guide-prospection.pdf",
    "questionnaire-decouverte.html": "Dig-Questionnaire-decouverte.pdf",
    "questionnaire-lancement-site.html": "Dig-Questionnaire-lancement-site.pdf",
    "audit-interne-claude.html": "Dig-Audit-interne-Claude.pdf",
    "guide-jarvis.html": "Dig-Guide-Jarvis.pdf",
    "guide-minimax-h3.html": "Dig-Guide-MiniMax-H3.pdf",
}
PNG = {"visuel-lancement.html": ("visuel-lancement-v2.png", 1080, 1350)}


def main():
    erreurs = 0
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        for html, pdf in PDF.items():
            pg = nav.new_page()
            pg.goto("file://" + os.path.join(SUP, html))
            pg.emulate_media(media="print")
            attendre_polices(pg)
            fautes = [r for r in pg.evaluate(MESURE) if r["depasse_px"] > 0 or r["scroll"] > 1]
            for r in fautes:
                print(f"ALERTE {html} page {r['page']} déborde de {r['depasse_px']} px : {r['quoi']!r}")
            erreurs += len(fautes)
            pg.pdf(path=os.path.join(SUP, pdf), format="A4", print_background=True, prefer_css_page_size=True)
            pg.close()
            print(f"{pdf} : {len(pymupdf.open(os.path.join(SUP, pdf)))} pages")
        for html, (png, l, h) in PNG.items():
            pg = nav.new_page(viewport={"width": l, "height": h})
            pg.goto("file://" + os.path.join(SUP, html))
            attendre_polices(pg)
            pg.screenshot(path=os.path.join(SUP, png))
            pg.close()
            print(f"{png} : {l} × {h}")
        nav.close()
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
