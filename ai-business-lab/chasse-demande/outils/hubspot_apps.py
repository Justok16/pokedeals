"""Relevé de la place de marché HubSpot (sitemap officiel, pages rendues).

Lit pour chaque app : nom, éditeur, installations, note, nombre d'avis,
catégorie, thèmes d'avis résumés par HubSpot. Sortie : hubspot.csv (reprise
possible). Usage : python3 hubspot_apps.py hs_urls.txt
"""
import asyncio, csv, os, re, sys
from playwright.async_api import async_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

def conv(x):
    x = x.rstrip("+")
    return int(float(x[:-1]) * (1000 if x[-1] == "K" else 1e6)) if x[-1] in "KM" else int(x.replace(",", ""))

def lire(url, t):
    t = re.sub(r"\n+", " | ", t)
    nom = re.search(r"Marketplace \| Apps \| ([^|]+) \|", t)
    ed = re.search(r"Built by \| ([^|]+) \|", t)
    inst = re.search(r"Installs \| ([\d.,]+[KM]?\+?) installs", t)
    note = re.search(r"Rating \| (\d(?:\.\d)?) \| \((\d[\d,]*)\)", t)
    cat = re.search(r"Categories \| ([^|]+) \|", t)
    themes = re.findall(r"\| ([a-z&' -]{4,40}) \((\d+)\)", t)
    return [url.rsplit("/", 1)[-1], nom.group(1).strip() if nom else "", ed.group(1).strip() if ed else "",
            conv(inst.group(1)) if inst else 0, note.group(1) if note else "",
            int(note.group(2).replace(",", "")) if note else 0, cat.group(1).strip() if cat else "",
            "; ".join(f"{a} ({b})" for a, b in themes[:8])]

async def main():
    urls = [u.strip() for u in open(sys.argv[1]) if "/marketplace/listing/" in u]
    faits = set()
    if os.path.exists("hubspot.csv"):
        faits = {r[0] for r in csv.reader(open("hubspot.csv", encoding="utf-8")) if r}
    urls = [u for u in urls if u.rsplit("/", 1)[-1] not in faits]
    f = open("hubspot.csv", "a", newline="", encoding="utf-8")
    w = csv.writer(f)
    if not faits:
        w.writerow(["id", "nom", "editeur", "installations", "note", "avis", "categorie", "themes"])
    file = asyncio.Queue()
    for u in urls:
        file.put_nowait(u)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=["--headless=new"])
        async def ouvrier():
            pg = await b.new_page()
            while not file.empty():
                u = await file.get()
                try:
                    await pg.goto(u, timeout=60000)
                    await pg.wait_for_timeout(3500)
                    w.writerow(lire(u, await pg.inner_text("body")))
                    f.flush()
                except Exception as e:
                    print("échec", u, e, flush=True)
        await asyncio.gather(*[ouvrier() for _ in range(4)])
        await b.close()

asyncio.run(main())
