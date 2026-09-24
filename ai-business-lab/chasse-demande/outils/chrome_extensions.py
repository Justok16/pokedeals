"""Relevé complet du Chrome Web Store : nom, catégorie, utilisateurs, note,
nombre de notes, achats intégrés, description.

Sources : sitemap public https://chromewebstore.google.com/sitemap (43 lots),
puis la page de chaque extension (en-tête HTML). Reprend là où il s'est
arrêté (fichier chrome.csv). Usage : python3 chrome_extensions.py
"""
import csv, gzip, html, os, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}

def lire(url, essais=5):
    for e in range(essais):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120)
            b = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                b = gzip.decompress(b)
            return b.decode("utf-8", "ignore")
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return None
            time.sleep(30 * (e + 1) if err.code == 429 else 5)
        except Exception:
            time.sleep(5)
    return None

def urls():
    if os.path.exists("urls.txt"):
        return [u.strip() for u in open("urls.txt") if u.strip()]
    tout = []
    for i in range(60):
        s = lire(f"https://chromewebstore.google.com/sitemap?shard={i}")
        if not s or "<loc>" not in s:
            break
        tout += re.findall(r"<loc>([^<]*/detail/[^<]*)</loc>", s)
    if tout:
        open("urls.txt", "w").write("\n".join(tout))
    return tout

def extraire(url):
    s = lire(url)
    if not s:
        return None
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    if not m:
        return None
    bloc = html.unescape(re.sub(r"<[^>]+>", "|", s[m.start():m.start() + 12000]))
    bloc = re.sub(r"\|+", "|", bloc)
    note = re.search(r"\|(\d\.\d)\|\(\|([\d.,]+K?) ratings?\|", bloc)
    users = re.search(r"\|([\d,]+\+?) users?\|", bloc)
    cat = re.search(r"\|(Extension|Theme|App)\|([^|]+)\|", bloc)
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    nb = note.group(2) if note else "0"
    nb = int(float(nb[:-1]) * 1000) if nb.endswith("K") else int(nb.replace(",", "") or 0)
    return [url.rstrip("/").split("/")[-1], html.unescape(m.group(1)).strip()[:120],
            cat.group(2).strip() if cat else "",
            int(users.group(1).replace(",", "").rstrip("+")) if users else 0,
            note.group(1) if note else "", nb,
            1 if re.search(r"in-app purchases", s, re.I) else 0,
            html.unescape(desc.group(1))[:200] if desc else ""]

def main():
    liste = urls()
    faits = set()
    if os.path.exists("chrome.csv"):
        faits = {r[0] for r in csv.reader(open("chrome.csv", encoding="utf-8")) if r}
    reste = [u for u in liste if u.rstrip("/").split("/")[-1] not in faits]
    print(len(liste), "extensions,", len(reste), "à relever", flush=True)
    neuf = not faits
    with open("chrome.csv", "a", newline="", encoding="utf-8") as f, ThreadPoolExecutor(8) as ex:
        w = csv.writer(f)
        if neuf:
            w.writerow(["id", "nom", "categorie", "utilisateurs", "note", "nb_notes", "achats_integres", "description"])
        for i, r in enumerate(ex.map(extraire, reste)):
            if r:
                w.writerow(r)
            if i % 2000 == 0:
                f.flush(); print(i, flush=True)

if __name__ == "__main__":
    main()
