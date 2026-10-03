"""Applications Atlassian cloud encore sur Connect (fin de support le
31/01/2027) : pour chaque app installée, lit la dernière version cloud
(API publique /rest/2/addons/<clé>/versions/latest?hosting=cloud) et note si
elle est « connect » et sa date de sortie. Entrée : atlassian.csv (relevé du
24/09). Sortie : connect.csv."""
import csv, json, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

def lire(cle):
    u = f"https://marketplace.atlassian.com/rest/2/addons/{cle}/versions/latest?hosting=cloud"
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(5)
        except Exception:
            time.sleep(5)
    return None

rows = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")) if int(r["installs"] or 0) >= int(sys.argv[2] if len(sys.argv) > 2 else 200)]

def traiter(r):
    v = lire(r["key"])
    if not v:
        return None
    d = v.get("deployment") or {}
    return [r["key"], r["nom"], r["categories"], r["installs"], r["avis"], r["note"],
            d.get("connect"), (v.get("release") or {}).get("date", ""), v.get("paymentModel", "")]

w = csv.writer(open("connect.csv", "w", newline="", encoding="utf-8"))
w.writerow(["key", "nom", "categories", "installs", "avis", "note", "connect", "derniere_version", "modele"])
with ThreadPoolExecutor(6) as ex:
    for x in ex.map(traiter, rows):
        if x:
            w.writerow(x)
print(len(rows), "apps examinées")
