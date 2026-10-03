"""Relevé de Google Workspace Marketplace par catégorie (sitemap officiel) :
nom, éditeur, description, note, installations. Sortie : workspace.csv."""
import csv, html, re, urllib.request

def lire(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}),
                                  timeout=90).read().decode("utf-8", "ignore")

sm = lire("https://workspace.google.com/marketplace/sitemap.xml")
cats = [u for u in re.findall(r"<loc>([^<]*/category/[^<]*)</loc>", sm) if u.count("/") >= 6]
motif = re.compile(r"\|([^|]{2,80})\|([^|]{2,60})\|([^|]{15,300})\|(\d\.\d)\|([\d.]+[KM]?\+?) \|Install\|")
w = csv.writer(open("workspace.csv", "w", newline="", encoding="utf-8"))
w.writerow(["categorie", "nom", "editeur", "description", "note", "installations"])
vus = set()
for c in cats:
    s = lire(c)
    t = html.unescape(re.sub(r"<[^>]+>", "|", re.sub(r"<(script|style)\b.*?</\1\s*>", "", s, flags=re.S | re.I)))
    t = re.sub(r"\|+", "|", t)
    n = 0
    for nom, ed, desc, note, inst in motif.findall(t):
        v = inst.rstrip("+")
        v = float(v[:-1]) * (1000 if v.endswith("K") else 1e6) if v[-1] in "KM" else float(v)
        w.writerow([c.split("/category/")[1], nom.strip(), ed.strip(), desc.strip(), note, int(v)])
        n += 1
    print(c.split("/category/")[1], n, flush=True)
