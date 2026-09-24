"""Relevé de toutes les apps de la boutique Shopify : note, nombre d'avis, prix affiché.

Source : sitemap public https://apps.shopify.com/sitemap_apps_en.xml puis la
page de chaque app (données structurées schema.org). Sortie : shopify_apps.csv.
Usage : python3 shopify_apps.py handles.txt
"""
import csv, json, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

def lire(handle):
    try:
        req = urllib.request.Request(f"https://apps.shopify.com/{handle}",
                                     headers={"User-Agent": "Mozilla/5.0"})
        s = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except Exception:
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
with open("shopify_apps.csv", "w", newline="", encoding="utf-8") as f, ThreadPoolExecutor(12) as ex:
    w = csv.writer(f)
    w.writerow(["handle", "nom", "note", "avis", "prix", "description"])
    for i, r in enumerate(ex.map(lire, handles)):
        if r:
            w.writerow(r)
        if i % 1000 == 0:
            f.flush(); print(i, flush=True)
