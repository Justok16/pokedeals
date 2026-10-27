#!/usr/bin/env python3
"""Cherche un article sur DIG16 dans Charente Libre (27/10/2026, demande de l'utilisateur après le rendez-vous du 27/10).

Sources lues, uniquement celles prévues pour la lecture automatique (aucun contournement de protection : les
rubriques du site renvoient « 403 » aux robots, on ne les lit pas) :
- le plan du site des articles du mois en cours et du mois précédent (sitemap officiel, fait pour les moteurs) ;
- Google Actualités (flux RSS public) pour « DIG16 » et « dig16.fr ».
Une adresse d'article est retenue si son titre parle de sites internet, d'artisans, de numérique ou de DIG16 ;
chaque article retenu est ensuite ouvert, et il est signalé s'il contient « DIG16 » (en clair, même derrière
l'abonnement, le titre et le début restent lisibles).

Usage : python3 outils/veille_presse.py   (code de sortie 0 : rien ; 2 : article trouvé, adresse affichée)
"""

import datetime
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://www.charentelibre.fr"
UA = {"User-Agent": "Mozilla/5.0 (compatible; veille DIG16)"}
INDICES = re.compile(r"dig-?16|site-?s?-internet|sites-web|site-web|numerique|artisan|createur|creation-d-entreprise", re.IGNORECASE)
MARQUE = re.compile(r"dig\s?16", re.IGNORECASE)


def lire(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def candidats():
    urls = set()
    aujourd_hui = datetime.datetime.now(datetime.UTC).date()
    mois = {aujourd_hui.strftime("%Y-%m"), (aujourd_hui.replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m")}
    for m in sorted(mois):
        try:
            xml = lire(f"{BASE}/sitemap/articles-{m}.xml")
        except Exception as e:  # noqa: BLE001 - une source en panne ne doit pas arrêter la veille
            print("plan du site illisible", m, e)
            continue
        urls.update(u for u in re.findall(r"<loc>([^<]+)</loc>", xml) if "/charente/" in u)
        time.sleep(3)
    return sorted(u for u in urls if INDICES.search(u.rsplit("/", 1)[-1]))


def google_actualites():
    q = urllib.parse.quote('"DIG16" OR "dig16.fr"')
    try:
        xml = lire(f"https://news.google.com/rss/search?q={q}&hl=fr&gl=FR&ceid=FR:fr")
    except Exception as e:  # noqa: BLE001
        print("Google Actualités illisible", e)
        return []
    items = re.findall(r"<item><title>([^<]*)</title><link>([^<]*)</link>", xml)
    return [(t, u) for t, u in items if MARQUE.search(t) or "charente" in t.lower()]


def main():
    trouves = []
    liste = candidats()
    for url in liste:
        time.sleep(3)
        try:
            html = lire(url)
        except Exception:  # noqa: BLE001, S112
            continue
        if MARQUE.search(html):
            titre = re.search(r"<title>([^<]*)", html)
            trouves.append((url, titre.group(1).strip() if titre else ""))
    for titre, url in google_actualites():
        trouves.append((url, "Google Actualités : " + titre))
    print(f"{len(liste)} articles candidats lus dans le plan du site")
    for url, titre in trouves:
        print("TROUVÉ", titre, url)
    return 2 if trouves else 0


if __name__ == "__main__":
    sys.exit(main())
