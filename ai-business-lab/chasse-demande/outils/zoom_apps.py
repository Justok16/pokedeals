"""Relevé de Zoom App Marketplace via l'interface publique de la boutique
(/api/v1/marketplaceV2/homepage/search, pagination par jeton), catégorie par
catégorie. Sortie : zoom.csv (nom, éditeur, catégories, note, nombre d'avis)."""
import csv, json, time, urllib.parse, urllib.request

def lire(u):
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60))
        except Exception:
            time.sleep(5)
    return None

base = "https://marketplace.zoom.us/api/v1/marketplaceV2"
filtres = lire(base + "/search/filter?")
cats = [c["id"] for f in filtres["filterList"] if f["id"] == "category" for c in f["children"]]
vus = {}
for cat in cats:
    jeton = ""
    while True:
        d = lire(f"{base}/homepage/search?pageSize=100&category={cat}" + (f"&nextPageToken={urllib.parse.quote(jeton)}" if jeton else ""))
        if not d:
            break
        for a in d.get("apps", []):
            st = a.get("ratingStatistics") or {}
            vus[a["id"]] = [a["id"], a["displayName"], a.get("companyName", ""), "|".join(a.get("categories") or []),
                            st.get("averageRating", st.get("rating", "")), st.get("totalRatings", st.get("count", st.get("ratingCount", 0))),
                            (a.get("description") or "")[:150]]
        jeton = d.get("nextPageToken") or ""
        if not jeton or not d.get("apps"):
            break
        time.sleep(0.5)
    print(cat, len(vus), flush=True)
w = csv.writer(open("zoom.csv", "w", newline="", encoding="utf-8"))
w.writerow(["id", "nom", "editeur", "categories", "note", "avis", "description"])
w.writerows(vus.values())
