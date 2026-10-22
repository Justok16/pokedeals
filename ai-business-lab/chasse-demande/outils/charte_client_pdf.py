#!/usr/bin/env python3
"""Charte « Comment nous travaillons ensemble » → PDF à remettre à chaque client du service devis-factures.

Source unique : supports/service-devis-factures/charte-client.md. Aucune donnée personnelle.
Usage : python3 outils/charte_client_pdf.py → supports/service-devis-factures/DIG16-charte-client.pdf
"""
import os
import re
import sys

import markdown

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "marque"))
from charte_documents import BASE, COUVERTURE, POLICES, attendre_polices, bandeau  # noqa: E402

DOSSIER = os.path.normpath(os.path.join(ICI, "..", "supports", "service-devis-factures"))
SOURCE = os.path.join(DOSSIER, "charte-client.md")
HTML = os.path.join(DOSSIER, "..", "DIG16-charte-client.html")  # dans supports/ : images ../site-dig/
PDF = os.path.join(DOSSIER, "DIG16-charte-client.pdf")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CSS = BASE + COUVERTURE + """@page{size:A4;margin:10mm 13mm 10mm}*{box-sizing:border-box}
body{font-size:9.1pt;line-height:1.4;margin:0}
h2{font-size:13pt;margin:2.6mm 0 .9mm;break-after:avoid}
p,li{margin:.7mm 0;text-align:justify;hyphens:auto}ol,ul{padding-left:5mm;margin:1mm 0}
ol li::marker{color:var(--bronze);font-weight:600}
.pied{margin-top:3mm;padding-top:1.6mm;border-top:.35mm solid var(--or);font-family:'Geist Mono',monospace;font-size:7.4pt;letter-spacing:.12em;text-transform:uppercase;color:var(--bronze)}"""


def html_page():
    md = open(SOURCE, encoding="utf-8").read()
    md = re.sub(r"^# .*\n", "", md, count=1)
    md = re.sub(r"^Une page à garder.*?\n\n", "", md, count=1, flags=re.S)
    md = md.replace("DIG16 — dig16.fr — contact@dig16.fr", "")
    if re.search(r"\[[^\]]{0,40}\]", md):
        raise SystemExit("ALERTE : crochets restants dans la charte")
    corps = markdown.markdown(md)
    tete = bandeau("Charte du service", "Comment nous <em>travaillons ensemble</em>",
                   "Devis, factures et relances : ce que DIG16 fait pour vous, ce qu'il ne fera jamais")
    pied = '<div class="pied">DIG16 · dig16.fr · contact@dig16.fr · remise à la signature du contrat</div>'
    return (f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>DIG16 — Charte du service</title>"
            f"{POLICES}<style>{CSS}</style></head><body>{tete}{corps}{pied}</body></html>")


def main():
    open(HTML, "w", encoding="utf-8").write(html_page())
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        pg.goto("file://" + HTML)
        pg.emulate_media(media="print")
        attendre_polices(pg)
        pg.pdf(path=PDF, format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    os.remove(HTML)
    print("OK", PDF, os.path.getsize(PDF), "octets")


if __name__ == "__main__":
    main()
