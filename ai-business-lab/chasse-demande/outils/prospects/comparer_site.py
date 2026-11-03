#!/usr/bin/env python3
"""Comparateur pour les rendez-vous (demande de l'utilisateur du 03/11/2026, « TOUT ») : une page qui met côte à côte le
site actuel d'un prospect (ou d'un concurrent) et le niveau exigé par DIG16, avec les notes mesurées par Unlighthouse
(Lighthouse de Google, sur téléphone) et une capture téléphone du site.

Usage : python3 outils/prospects/comparer_site.py https://site-du-prospect.fr <dossier de sortie PRIVÉ> [nom affiché]
Produit <dossier>/comparatif.pdf (une page A4, remplissable : notes de l'appel) et comparatif.png.
Données de prospect : sortie dans le scratchpad ou le Drive « Dig », JAMAIS dans ce dépôt.
Ton : factuel, jamais dénigrant (on montre des mesures, on ne critique pas le prestataire du prospect)."""

import base64
import glob
import json
import os
import re
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
    if pages:
        return next((p for p in pages if p["path"] in ("/", "")), pages[0]), len(pages)
    # Repli : certains hébergeurs (SoLocal/PagesJaunes, constaté le 03/11/2026) refusent le robot d'Unlighthouse (403)
    # mais acceptent un vrai navigateur : Lighthouse seul (installé avec Unlighthouse), page d'accueil sur téléphone.
    lh = glob.glob("/tmp/claude-*/*/*/scratchpad/unlighthouse/node_modules/.bin/lighthouse")
    if not lh:
        sys.exit("Lighthouse introuvable : lancer d'abord outils/unlighthouse/audit.sh une fois.")
    json_lh = os.path.join(sortie, "lighthouse.json")
    subprocess.run(
        [lh[0], site, "--quiet", "--chrome-flags=--headless=new --no-sandbox", "--output=json",
         f"--output-path={json_lh}", "--only-categories=performance,accessibility,best-practices,seo"],
        check=True,
        capture_output=True,
        env={**os.environ, "CHROME_PATH": "/opt/pw-browsers/chromium"},
    )
    with open(json_lh) as f:
        cats = json.load(f)["categories"]
    if any(cats[k]["score"] is None for k in NOMS):
        sys.exit(f"Lighthouse n'a pas pu mesurer {site} : vérifier le site à la main.")
    return {k: cats[k]["score"] for k in NOMS} | {"path": "/"}, 1


def capture(site, fichier):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        page = nav.new_page(viewport={"width": 390, "height": 760}, device_scale_factor=2, is_mobile=True,
                            locale="fr-FR", extra_http_headers={"Accept-Language": "fr-FR,fr;q=0.9"})
        page.goto(site, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        # Bandeau de cookies : on le refuse pour montrer le site lui-même (comme le ferait un visiteur).
        # Le bandeau peut être dans un cadre (iframe) : on cherche dans tous ; un échec ne bloque pas la capture.
        motif = re.compile(r"tout\s*refuser|refuser|continuer sans|refuse all", re.IGNORECASE)
        for cadre in page.frames:
            refus = cadre.get_by_role("button", name=motif)
            if not refus.count():
                refus = cadre.locator("button, a").filter(has_text=motif)
            if refus.count():
                try:
                    refus.first.click(timeout=5000)
                    page.wait_for_timeout(1500)
                    break
                except Exception as erreur:  # noqa: BLE001 (capture quand même, bandeau visible)
                    print("bandeau de cookies non fermé :", erreur.__class__.__name__)
        page.screenshot(path=fichier)
        nav.close()


def page_html(site, nom, accueil, nb, image):
    plus = f" ({nb} pages du site analysées)" if nb > 1 else ""
    dossier = os.path.join(RACINE, "site-dig", "moteur", "polices")
    def en_ligne(m):
        with open(os.path.join(dossier, m.group(1)), "rb") as f:
            return "url(data:font/woff2;base64," + base64.b64encode(f.read()).decode() + ")"

    with open(os.path.join(dossier, "instrumentserif-geist-geistmono.css"), encoding="utf-8") as f:
        polices = re.sub(r"url\(/moteur/polices/([^)]+)\)", en_ligne, f.read())
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
@page{{size:A4;margin:14mm}}{polices}body{{font-family:Geist,'DejaVu Sans',Arial,sans-serif;color:#1d1a16;font-size:11pt}}
h1{{font-family:'Instrument Serif',serif;font-weight:400;font-size:24pt;margin:0 0 2mm}}.sous{{color:#6b6257;margin:0 0 6mm}}.grille{{display:flex;gap:8mm}}
img{{width:62mm;border:1px solid #d8d0c4;border-radius:4mm}}table{{border-collapse:collapse;width:100%}}
td,th{{border-bottom:1px solid #e4ddd2;padding:2.2mm 1.5mm;text-align:left;vertical-align:top}}
th{{font-size:9.5pt;color:#6b6257;font-weight:600}}.note{{font-size:9pt;color:#6b6257;margin-top:5mm}}
.cadre{{border:1px solid #d8d0c4;border-radius:2mm;height:42mm;margin-top:5mm;padding:2mm;color:#8a8175;font-size:9pt}}
</style><h1>Votre site aujourd’hui, mesuré</h1>
<p class="sous">{nom} · {site} · page d’accueil, sur téléphone{plus}</p>
<div class="grille"><img src="data:image/png;base64,{image}" alt="Capture du site sur téléphone">
<div style="flex:1"><table><tr><th>Critère (outil Lighthouse de Google)</th><th>Votre site</th><th>Exigence DIG16</th></tr>
{lignes}</table>
<p class="note">Mesures faites par l'outil gratuit Lighthouse de Google, sur téléphone, le jour de la
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
