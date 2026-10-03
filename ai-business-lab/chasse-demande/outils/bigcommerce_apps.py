"""Relevé des apps BigCommerce (sitemap officiel) : nom, note, nombre d'avis, résumé.
Sortie : bigcommerce_apps.csv. Usage : python3 bigcommerce_apps.py bc_urls.txt
"""
import csv, html, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

def lire(url):
    for essai in range(4):
        try:
            s = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                       timeout=25).read().decode("utf-8", "ignore")
            time.sleep(0.5)
            break
        except Exception:
            time.sleep(10 * (essai + 1))
    else:
        return None
    nom = re.search(r'<meta property="og:title" content="([^"]*)"', s)
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    note = re.search(r'"ratingValue":"?([\d.]+)', s)
    nb = re.search(r'"reviewCount":(\d+)', s)
    prix = re.search(r'(Free|\$[\d,.]+ ?/ ?(?:mo|month))', s)
    return [url.rstrip("/").split("/")[-1], html.unescape(nom.group(1)) if nom else "",
            note.group(1) if note else "", nb.group(1) if nb else "0",
            prix.group(1) if prix else "", html.unescape(desc.group(1))[:200] if desc else ""]

urls = [u.strip() for u in open(sys.argv[1]) if u.strip().count("/") >= 5]
with open("bigcommerce_apps.csv", "w", newline="", encoding="utf-8") as f, ThreadPoolExecutor(4) as ex:
    w = csv.writer(f)
    w.writerow(["handle", "nom", "note", "avis", "prix", "description"])
    for r in ex.map(lire, urls):
        if r:
            w.writerow(r)
