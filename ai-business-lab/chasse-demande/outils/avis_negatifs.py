"""Collecte d'avis négatifs (1-2 étoiles) sur des applications payantes.

But : trouver les problèmes que des clients QUI PAIENT citent le plus souvent
sans bonne solution (grille anti-DigCost, points 5 et 6).

Sources :
- App Store : recherche iTunes (https://itunes.apple.com/search) puis flux
  public d'avis (https://itunes.apple.com/<pays>/rss/customerreviews/...).
- Google Play : bibliothèque google-play-scraper.

Usage :
    python3 avis_negatifs.py "facturation" "planning" --pays fr us gb --max-apps 15
Sortie : avis.csv (tous les avis 1-2 étoiles) et resume.md (applications
classées par nombre d'avis négatifs, mots les plus fréquents).

Nécessite l'accès réseau à itunes.apple.com et play.google.com.
"""
import argparse
import collections
import csv
import json
import re
import time
import urllib.parse
import urllib.request

MOTS_VIDES = set("""
the a an and or to of in on for is it this that with app i my me you your
be are was were not but have has had they them at as so if just can do
le la les un une des et ou de du en au aux pour est ce cette avec je mon ma
mes vous votre pas mais il elle ils on sur que qui ne plus tres très
""".split())


def lire_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def apps_ios(terme, pays, n):
    q = urllib.parse.urlencode({"term": terme, "entity": "software",
                                "country": pays, "limit": n})
    res = lire_json(f"https://itunes.apple.com/search?{q}")["results"]
    return [(str(a["trackId"]), a["trackName"], a.get("price", 0),
             a.get("userRatingCount", 0)) for a in res]


def avis_ios(app_id, pays, pages=3):
    for p in range(1, pages + 1):
        url = (f"https://itunes.apple.com/{pays}/rss/customerreviews/"
               f"page={p}/id={app_id}/sortby=mostrecent/json")
        try:
            entrees = lire_json(url)["feed"].get("entry", [])
        except Exception:
            return
        for e in entrees:
            if "im:rating" not in e:
                continue
            yield int(e["im:rating"]["label"]), e["content"]["label"]
        time.sleep(0.5)


def apps_android(terme, pays, n):
    from google_play_scraper import search
    res = search(terme, lang=pays if pays != "us" else "en", country=pays,
                 n_hits=n)
    return [(a["appId"], a["title"], a.get("price", 0),
             a.get("score") or 0) for a in res]


def avis_android(app_id, pays, n=300):
    from google_play_scraper import reviews, Sort
    try:
        res, _ = reviews(app_id, lang=pays if pays != "us" else "en",
                         country=pays, sort=Sort.NEWEST, count=n)
    except Exception:
        return
    for r in res:
        yield r["score"], r["content"] or ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("termes", nargs="+")
    ap.add_argument("--pays", nargs="+", default=["fr", "us"])
    ap.add_argument("--max-apps", type=int, default=15)
    a = ap.parse_args()

    lignes, par_app = [], collections.Counter()
    for terme in a.termes:
        for pays in a.pays:
            for source, lister, lire in (("ios", apps_ios, avis_ios),
                                         ("android", apps_android, avis_android)):
                try:
                    apps = lister(terme, pays, a.max_apps)
                except Exception as err:
                    print(f"[{source}/{pays}] recherche impossible : {err}")
                    continue
                for app_id, nom, prix, _ in apps:
                    for note, texte in lire(app_id, pays):
                        if note <= 2 and texte.strip():
                            lignes.append([terme, source, pays, nom, prix,
                                           note, texte.replace("\n", " ")])
                            par_app[(source, nom)] += 1

    with open("avis.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["terme", "source", "pays", "app", "prix", "note", "avis"])
        w.writerows(lignes)

    mots = collections.Counter(
        m for l in lignes for m in re.findall(r"[a-zà-ÿ]{4,}", l[6].lower())
        if m not in MOTS_VIDES)
    with open("resume.md", "w", encoding="utf-8") as f:
        f.write(f"# Avis 1-2 étoiles : {len(lignes)}\n\n## Par application\n\n")
        for (src, nom), n in par_app.most_common(40):
            f.write(f"- {n} — {nom} ({src})\n")
        f.write("\n## Mots les plus fréquents\n\n")
        f.write(", ".join(f"{m} ({n})" for m, n in mots.most_common(60)))
    print(f"{len(lignes)} avis négatifs -> avis.csv, resume.md")


if __name__ == "__main__":
    main()
