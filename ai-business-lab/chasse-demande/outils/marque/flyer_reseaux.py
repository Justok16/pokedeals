#!/usr/bin/env python3
"""Flyer DIG16 pour les réseaux sociaux (18/10/2026) : même flyer que l'A5 (`flyer.py`), adapté au fil.

- Format 1080 × 1350 px (4:5, le plus haut accepté par le fil Instagram et Facebook) : l'A5 (rapport 0,705) serait
  rogné ; il est donc posé entier sur un fond de la même teinte.
- Téléphone rempli (déjà public sur dig16.fr) ; **ni nom ni adresse** : en ligne, les mentions légales sont sur
  dig16.fr/mentions-legales (choix du 18/10 : pas d'adresse personnelle diffusée sur les réseaux) ;
  « Ne pas jeter sur la voie publique » retiré (papier seulement).
- Contrôles : ceux de `flyer.py` (zone, chevauchements, tailles, contrastes, polices) + QR décodé sur l'image finale.

Usage : DIG16_IDENTITE=<json privé> python3 outils/marque/flyer_reseaux.py <dossier de sortie>
"""

import os
import sys

import cv2
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flyer  # noqa: E402
import identite  # noqa: E402

LEGAL_PAPIER = ("DIG16 — [Prénom Nom], entrepreneur individuel (EI) — SIREN [à compléter] — [adresse]. ")
LEGAL_RESEAUX = "DIG16, entrepreneur individuel (EI). Mentions légales : dig16.fr. "


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sortie = sys.argv[1]
    os.makedirs(sortie, exist_ok=True)
    ident = identite.charger_identite_seule()
    if not ident:
        sys.exit("ALERTE : DIG16_IDENTITE manquant (téléphone)")
    html = flyer.HTML.replace("{QR}", flyer.qr_svg())
    assert LEGAL_PAPIER in html and " Ne pas jeter sur la voie publique." in html
    html = html.replace(LEGAL_PAPIER, LEGAL_RESEAUX).replace(" Ne pas jeter sur la voie publique.", "")
    # le HTML est écrit hors de supports/ : ses images relatives (logo, téléphone) doivent y être cherchées
    html = html.replace("<head>", '<head><base href="file://' + flyer.SUP + '/">', 1)
    chemin = os.path.join(sortie, "flyer-reseaux.html")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(html)
    largeur, hauteur = 148 * 96 / 25.4, 210 * 96 / 25.4
    a5 = os.path.join(sortie, "flyer-a5-reseaux.png")
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=flyer.CHROME)
        pg = nav.new_page(viewport={"width": round(largeur), "height": round(hauteur)}, device_scale_factor=1748 / largeur)
        pg.goto("file://" + chemin)
        # téléphone posé dans la page seulement : aucune donnée de l'identité n'est écrite sur disque (CodeQL)
        pg.evaluate("t => { const b = document.querySelector('.contact b'); b.textContent = b.textContent.replace('[Téléphone]', t); }",
                    ident["telephone"])
        if pg.evaluate("document.body.innerText.includes('[')"):
            sys.exit("ALERTE : champ entre crochets restant")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(800)
        res = pg.evaluate(flyer.CONTROLE)
        cassees = pg.evaluate("[...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.alt || i.src)")
        pg.locator(".page").screenshot(path=a5)
        nav.close()
    os.remove(chemin)
    fautes = list(res["fautes"]) + [f"image non chargée : {c}" for c in cassees]
    manque = {"Instrument Serif", "Geist"} - set(res["fonts"])
    if manque:
        fautes.append(f"polices non chargées : {manque}")
    im = Image.open(a5).convert("RGB")
    h = 1350 - 2 * 24
    w = round(im.width * h / im.height)
    petit = im.resize((w, h), Image.LANCZOS)
    fond = Image.new("RGB", (1080, 1350), (237, 230, 217))  # #ede6d9, bas du dégradé du flyer
    fond.paste(petit, ((1080 - w) // 2, 24))
    jpg = os.path.join(sortie, "DIG16-flyer-reseaux-1080x1350.jpg")
    fond.save(jpg, quality=92, optimize=True)
    os.remove(a5)
    lu = cv2.QRCodeDetector().detectAndDecode(cv2.imread(jpg))[0]
    if lu != flyer.LIEN:
        fautes.append(f"QR illisible sur l'image finale : {lu!r}")
    for f in fautes:
        print("ALERTE", f)
    print("QR ->", lu, "| plus petit texte :", res["mini"], "pt | pire contraste :", res["pire"])
    print("Flyer réseaux prêt :" if not fautes else "ALERTE flyer réseaux :", jpg)
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main())
