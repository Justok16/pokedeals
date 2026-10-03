"""Relevé de toutes les apps de la boutique Shopify : note, nombre d'avis, prix affiché.

Source : sitemap public https://apps.shopify.com/sitemap_apps_en.xml puis la
page de chaque app (données structurées schema.org). Sortie : shopify_apps.csv.
Usage : python3 shopify_apps.py handles.txt
"""
import csv, json, os, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

def lire(handle):
    for essai in range(5):
        try:
            req = urllib.request.Request(f"https://apps.shopify.com/{handle}",
                                         headers={"User-Agent": "Mozilla/5.0"})
            s = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
            time.sleep(0.8)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(60 * (essai + 1))  # limite de débit : attendre
                continue
            return None
        except Exception:
            time.sleep(5)
    else:
        return None
    d = {}
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            j = json.loads(m)
        except Exception:
            continue
        if j.get("@type") == "SoftwareApplication":
            d = j
    ag = d.get("aggregateRating") or {}
    prix = re.search(r'(Free plan available|Free to install|Free|From \$[\d,.]+/month|\$[\d,.]+/month)', s)
    return [handle, d.get("name", ""), ag.get("ratingValue", ""), ag.get("ratingCount", 0),
            prix.group(1) if prix else "", (d.get("description") or "").replace("\n", " ")[:200]]

handles = [h.strip() for h in open(sys.argv[1]) if h.strip()]
deja = set()
if os.path.exists("shopify_apps.csv"):  # reprise : ne pas refaire les apps déjà relevées
    deja = {r[0] for r in csv.reader(open("shopify_apps.csv", encoding="utf-8"))}
handles = [h for h in handles if h not in deja]
nouveau = not deja
with open("shopify_apps.csv", "a", newline="", encoding="utf-8") as f, ThreadPoolExecutor(3) as ex:
    w = csv.writer(f)
    if nouveau:
        w.writerow(["handle", "nom", "note", "avis", "prix", "description"])
    for i, r in enumerate(ex.map(lire, handles)):
        if r:
            w.writerow(r)
        if i % 500 == 0:
            f.flush(); print(i, flush=True)
