#!/usr/bin/env python3
"""Comparateur pour les rendez-vous (demande de l'utilisateur du 03/11/2026, « TOUT ») : une page qui met côte à côte le
site actuel d'un prospect (ou d'un concurrent) et le niveau exigé par DIG16, avec les notes mesurées par Unlighthouse
(Lighthouse de Google, sur téléphone) et une capture téléphone du site.

Usage : python3 outils/prospects/comparer_site.py https://site-du-prospect.fr <dossier de sortie PRIVÉ> [nom affiché]
Produit <dossier>/comparatif.pdf (une page A4, remplissable : notes de l'appel) et comparatif.png.
Données de prospect : sortie dans le scratchpad ou le Drive « Dig », JAMAIS dans ce dépôt.
Ton : factuel, jamais dénigrant (on montre des mesures, on ne critique pas le prestataire du prospect)."""

import base64
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(ICI))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
EXIGENCE = {"performance": 0.95, "accessibility": 1.0, "best-practices": 1.0, "seo": 1.0}
NOMS = {
    "performance": "Vitesse sur téléphone",
    "accessibility": "Lisibilité et accessibilité",
    "best-practices": "Sécurité et bonnes pratiques",
    "seo": "Bases du référencement Google",
}


def mesurer(site, sortie):
    rapport = os.path.join(sortie, "unlighthouse")
    subprocess.run(
        ["sh", os.path.join(ICI, "..", "unlighthouse", "audit.sh"), site, rapport],
        check=True,
        capture_output=True,
        text=True,
    )
    with open(os.path.join(rapport, "ci-result.json")) as f:
        pages = json.load(f)
    accueil = next((p for p in pages if p["path"] in ("/", "")), pages[0])
    return accueil, len(pages)


def capture(site, fichier):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        page = nav.new_page(viewport={"width": 390, "height": 760}, device_scale_factor=2, is_mobile=True)
        page.goto(site, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        page.screenshot(path=fichier)
        nav.close()


def page_html(site, nom, accueil, nb, image):
    lignes = ""
    for cle, libelle in NOMS.items():
        note = round(accueil[cle] * 100)
        cible = round(EXIGENCE[cle] * 100)
        ok = accueil[cle] >= EXIGENCE[cle]
        couleur = "#2e6b3f" if ok else "#a3462b"
        lignes += (
            f"<tr><td>{libelle}</td><td style='color:{couleur};font-weight:600'>{note}/100</td>"
            f"<td>{cible}/100 minimum</td></tr>"
        )
    return f"""<!doctype html><html lang="fr"><meta charset="utf-8"><style>
@page{{size:A4;margin:14mm}}body{{font-family:'DejaVu Sans',Arial,sans-serif;color:#1d1a16;font-size:11pt}}
h1{{font-size:17pt;margin:0 0 2mm}}.sous{{color:#6b6257;margin:0 0 6mm}}.grille{{display:flex;gap:8mm}}
img{{width:62mm;border:1px solid #d8d0c4;border-radius:4mm}}table{{border-collapse:collapse;width:100%}}
td,th{{border-bottom:1px solid #e4ddd2;padding:2.2mm 1.5mm;text-align:left;vertical-align:top}}
th{{font-size:9.5pt;color:#6b6257;font-weight:600}}.note{{font-size:9pt;color:#6b6257;margin-top:5mm}}
.cadre{{border:1px solid #d8d0c4;border-radius:2mm;height:42mm;margin-top:5mm;padding:2mm;color:#8a8175;font-size:9pt}}
</style><h1>Votre site aujourd'hui, mesuré</h1>
<p class="sous">{nom} · {site} · page d'accueil, sur téléphone ({nb} page(s) du site analysée(s))</p>
<div class="grille"><img src="data:image/png;base64,{image}" alt="Capture du site sur téléphone">
<div style="flex:1"><table><tr><th>Critère (outil Lighthouse de Google)</th><th>Votre site</th><th>Exigence DIG16</th></tr>
{lignes}</table>
<p class="note">Mesures faites par l'outil gratuit Lighthouse de Google (via Unlighthouse), sur téléphone, le jour de la
préparation de cet échange. Elles peuvent varier un peu d'un essai à l'autre. dig16.fr obtient 96 à 100/100 sur
chaque critère (mesure du 03/11/2026).</p></div></div>
<div class="cadre">Notes de l'échange :</div></html>"""


def main(site, sortie, nom=None):
    os.makedirs(sortie, exist_ok=True)
    nom = nom or site.split("//")[-1].strip("/")
    accueil, nb = mesurer(site, sortie)
    png = os.path.join(sortie, "comparatif.png")
    capture(site, png)
    with open(png, "rb") as f:
        image = base64.b64encode(f.read()).decode()
    from playwright.sync_api import sync_playwright

    brut = os.path.join(sortie, "comparatif-brut.pdf")
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        page = nav.new_page()
        page.set_content(page_html(site, nom, accueil, nb, image), wait_until="load")
        page.pdf(path=brut, format="A4", print_background=True)
        nav.close()
    final = os.path.join(sortie, "comparatif.pdf")
    subprocess.run(
        [sys.executable, os.path.join(RACINE, "outils", "pdf_remplissable.py"), brut, final, "--notes", "Notes de l'échange"],
        check=True,
    )
    print(json.dumps({k: accueil[k] for k in NOMS}, ensure_ascii=False), final)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:4])
