"""Régénère supports/Dig-Plan-complet.pdf à partir des fichiers à jour du dossier
(règle « PDF toujours à jour » : relancer après toute modification de 39, 40, 41, 42 ou 36).

Usage : python3 outils/plan_complet.py
Produit supports/plan-complet.html puis supports/Dig-Plan-complet.pdf (A4) avec Playwright.
"""

import datetime
import os
import re
import markdown
import sys
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
sys.path.insert(0, os.path.join(ICI, "marque"))
from charte_documents import BASE, MARQUE, POLICES, attendre_polices  # noqa: E402
PARTIES = [
    ("39-business-plan-sites.md", "Business plan"),
    ("40-cadre-legal-sites.md", "Cadre légal"),
    ("41-prospection-questionnaire-et-textes.md", "Questionnaire et textes d'appel"),
    ("42-flyer-et-prompt.md", "Flyer et prompts"),
    ("36-aides-creation.md", "Aides à la création"),
]
STYLE = BASE + """
@page{size:A4;margin:16mm 15mm 17mm}
body{font-size:9.4pt;line-height:1.5}
h1{font-size:24pt;line-height:1.05;margin:0 0 4mm;padding-bottom:3mm;border-bottom:.35mm solid var(--or)}
h2{font-size:16pt;line-height:1.1;margin:7mm 0 2mm;break-after:avoid} h3{font-size:12.5pt;margin:5mm 0 1.5mm;break-after:avoid}
table{border-collapse:collapse;width:100%;margin:2.5mm 0;font-size:8.2pt}
th{font-family:'Geist Mono',monospace;font-weight:400;font-size:6.6pt;letter-spacing:.12em;text-transform:uppercase;color:var(--bronze);text-align:left;padding:1.6mm 2mm;border-bottom:.35mm solid var(--or)}
td{border-bottom:.25mm solid var(--trait);padding:1.5mm 2mm;vertical-align:top}
tr,img{page-break-inside:avoid}
blockquote{border-left:.6mm solid var(--or);margin:2mm 0;padding:1mm 4mm;background:var(--fond-doux)}
code{font-family:'Geist Mono',monospace;font-size:.92em;background:var(--fond-doux);padding:0 1mm;border-radius:1mm;word-break:break-all}
a{word-break:break-all} del{color:#8c8478}
hr{border:0;border-top:.25mm solid var(--trait);margin:5mm 0}
section{page-break-before:always}
.cover{box-sizing:border-box;height:258mm;background:var(--nuit);color:var(--ivoire);border-radius:3mm;padding:16mm 15mm;display:flex;flex-direction:column;justify-content:space-between;
 background-image:radial-gradient(140mm 110mm at 100% 0,rgba(200,164,110,.17),rgba(200,164,110,0) 70%);box-shadow:inset 0 0 0 .3mm rgba(200,164,110,.35)}
.cover .signature{height:17mm;width:auto;align-self:flex-start}
.cover .k{color:var(--or);font-size:7.4pt;display:flex;align-items:center;gap:3mm}
.cover .k::before{content:"";width:9mm;height:.3mm;background:var(--or)}
.cover h1{color:var(--ivoire);font-size:44pt;line-height:.98;border:0;margin:4mm 0 5mm;padding:0}
.cover h1 em{color:var(--or-clair)}
.cover p{color:var(--doux);margin:1mm 0}
.cover ol{margin:6mm 0 0;padding:0;list-style:none;counter-reset:n;border-top:.25mm solid rgba(239,233,223,.14)}
.cover li{counter-increment:n;padding:2.2mm 0;border-bottom:.25mm solid rgba(239,233,223,.14);font-family:'Instrument Serif',serif;font-size:14pt;color:var(--ivoire)}
.cover li::before{content:counter(n,decimal-leading-zero);font-family:'Geist Mono',monospace;font-size:7pt;color:var(--or);margin-right:5mm;vertical-align:2pt}
.cover .note{font-size:7.6pt;color:#8c8478}
"""


def couverture(etiquette, titre, sous, parties, note):
    """Page de garde sombre commune (plan complet, campagne)."""
    return (
        f'<div class="cover"><img class="signature" src="{MARQUE}signature-ivoire@6x.png" alt="DIG16, sites internet">'
        f'<div><div class="k">{etiquette}</div><h1>{titre}</h1>'
        + "".join(f"<p>{x}</p>" for x in sous)
        + ("<ol>" + "".join(f"<li>{t}</li>" for t in parties) + "</ol>" if parties else "")
        + f'</div><p class="note">{note}</p></div>'
    )


def main():
    jour = datetime.date.today().strftime("%d/%m/%Y")
    corps = [
        couverture(
            "Sites internet pour artisans, commerçants et indépendants",
            "Plan <em>complet</em>",
            [f"Version du {jour}, régénérée depuis les fichiers du dossier."],
            [t for _, t in PARTIES],
            "Les listes de prospects et toute donnée personnelle sont dans des documents privés séparés.",
        )
    ]
    for fichier, _ in PARTIES:
        texte = open(os.path.join(RACINE, fichier), encoding="utf-8").read()
        texte = re.sub(r"~~(.+?)~~", r"<del>\1</del>", texte)
        html = markdown.markdown(texte, extensions=["tables", "sane_lists"])
        corps.append(f"<section>{html}</section>")
    page = (
        "<!doctype html><html lang=fr><head><meta charset=utf-8>" + POLICES + "<style>"
        + STYLE
        + "</style></head><body>"
        + "".join(corps)
        + "</body></html>"
    )
    sortie_html = os.path.join(RACINE, "supports", "plan-complet.html")
    open(sortie_html, "w", encoding="utf-8").write(page)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = b.new_page()
        pg.goto("file://" + sortie_html)
        pg.emulate_media(media="print")
        attendre_polices(pg)
        pg.pdf(
            path=os.path.join(RACINE, "supports", "Dig-Plan-complet.pdf"),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
        )
        b.close()
    print("Plan complet régénéré :", sortie_html)


if __name__ == "__main__":
    main()
