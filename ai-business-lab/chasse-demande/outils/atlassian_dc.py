"""Apps Atlassian Data Center (fin de vie le 28/03/2029, source :
atlassian.com/licensing/data-center-end-of-life) : liste toutes les apps DC
(API publique /rest/2/addons?hosting=datacenter), puis vérifie pour chacune
s'il existe une version cloud (/versions/latest?hosting=cloud ; 404 = aucune).
Sortie : dc.csv."""
import csv, json, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

B = "https://marketplace.atlassian.com"

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

apps, off = [], 0
while True:
    d = lire(f"/rest/2/addons?hosting=datacenter&limit=50&offset={off}")
    lot = (d or {}).get("_embedded", {}).get("addons", [])
    if not lot:
        break
    apps += lot
    off += 50
print(len(apps), "apps DC")

def traiter(a):
    cle = a["key"]
    e = a.get("_embedded", {})
    cloud = lire(f"/rest/2/addons/{cle}/versions/latest?hosting=cloud")
    dc = lire(f"/rest/2/addons/{cle}/versions/latest?hosting=datacenter") or {}
    return [cle, a.get("name"), (e.get("vendor") or {}).get("name", ""),
            ";".join(c["name"] for c in e.get("categories", [])),
            (e.get("distribution") or {}).get("totalInstalls", 0),
            (e.get("reviews") or {}).get("count", 0),
            round((e.get("reviews") or {}).get("averageStars") or 0, 2),
            "oui" if cloud else "non", dc.get("paymentModel", ""),
            (dc.get("release") or {}).get("date", "")]

w = csv.writer(open("dc.csv", "w", newline="", encoding="utf-8"))
w.writerow(["key", "nom", "editeur", "categories", "installs", "avis", "note", "cloud", "modele_dc", "derniere_version_dc"])
with ThreadPoolExecutor(6) as ex:
    for x in ex.map(traiter, apps):
        w.writerow(x)
