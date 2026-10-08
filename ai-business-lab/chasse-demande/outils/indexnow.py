#!/usr/bin/env python3
"""Signale les pages de dig16.fr aux moteurs qui utilisent IndexNow (Bing, Yandex, Seznam, Naver…), sans compte
(protocole public : https://www.indexnow.org/documentation, préparé le 08/10/2026).

Usage : python3 outils/indexnow.py            (toutes les adresses du sitemap)
        python3 outils/indexnow.py URL [URL…]  (seulement ces pages, après une modification)
À lancer UNIQUEMENT quand le site est ouvert (bandeau et « noindex » retirés par outils/ouverture_site.py),
puis après chaque modification publiée. La « clé » n'est pas un secret : c'est un jeton public de preuve de
propriété, servi à la racine du site (site-dig/<clé>.txt), comme le prévoit le protocole.
Réponses : 200 ou 202 = accepté ; 403 = clé introuvable sur le site ; 422 = adresse hors du domaine.
"""

import json
import re
import sys
import urllib.request

CLE = "dig16-indexnow-2026-cle-publique"
HOTE = "dig16.fr"


def adresses_du_sitemap():
    with urllib.request.urlopen(f"https://{HOTE}/sitemap.xml", timeout=20) as r:
        return re.findall(r"<loc>([^<]+)</loc>", r.read().decode())


def main():
    with urllib.request.urlopen(f"https://{HOTE}/", timeout=20) as r:
        if 'name="robots" content="noindex"' in r.read().decode():
            raise SystemExit("ALERTE : le site est encore en « noindex » (ouverture prochaine) : rien n'est envoyé")
    urls = sys.argv[1:] or adresses_du_sitemap()
    corps = json.dumps({"host": HOTE, "key": CLE, "keyLocation": f"https://{HOTE}/{CLE}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=corps, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow :", r.status, "-", len(urls), "adresse(s) signalée(s)")
    except urllib.error.HTTPError as e:
        print("ALERTE IndexNow :", e.code, e.reason)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
