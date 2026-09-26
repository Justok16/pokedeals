"""Pour les apps DC payantes sans version cloud (dc.csv), cherche sur la
boutique cloud (API publique, recherche texte) : 1) une app cloud du même
éditeur au nom proche ; 2) le nombre d'alternatives cloud bien notées
(>= 4 étoiles, >= 10 avis). Sortie : dc_alternatives.csv."""
import csv, json, re, time, urllib.parse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

B = "https://marketplace.atlassian.com"
VIDES = set("for jira confluence bitbucket data center dc server app plugin the and & - | with by of to in pro".split())

def lire(u):
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(B + u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(5)
        except Exception:
            time.sleep(5)
    return None

def mots(nom):
    nom = re.split(r"[|:(\-–]", nom)[0]
    return [m for m in re.findall(r"[a-z0-9]+", nom.lower()) if m not in VIDES]

def traiter(r):
    m = mots(r["nom"])
    q = urllib.parse.quote(" ".join(m[:3]))
    d = lire(f"/rest/2/addons?hosting=cloud&text={q}&limit=20") or {}
    res = d.get("_embedded", {}).get("addons", [])
    meme, alt = "", []
    for a in res:
        e = a.get("_embedded", {})
        ven = (e.get("vendor") or {}).get("name", "")
        rv = e.get("reviews") or {}
        if ven == r["editeur"] and set(m[:2]) <= set(mots(a["name"])):
            meme = a["name"]
        elif (rv.get("averageStars") or 0) >= 4 and (rv.get("count") or 0) >= 10:
            alt.append(f'{a["name"][:40]} ({rv["count"]})')
    return [r["key"], r["nom"], r["editeur"], r["installs"], r["avis"], r["note"],
            r["derniere_version_dc"], meme, len(alt), "; ".join(alt[:4])]

rows = [r for r in csv.DictReader(open("dc.csv", encoding="utf-8"))
        if r["cloud"] == "non" and r["modele_dc"] == "atlassian"]
w = csv.writer(open("dc_alternatives.csv", "w", newline="", encoding="utf-8"))
w.writerow(["key", "nom", "editeur", "installs", "avis", "note", "derniere_version_dc",
            "cloud_meme_editeur", "nb_alternatives", "exemples"])
with ThreadPoolExecutor(6) as ex:
    for x in ex.map(traiter, rows):
        w.writerow(x)
print(len(rows), "apps traitées")
