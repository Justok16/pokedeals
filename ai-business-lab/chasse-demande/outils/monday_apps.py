"""Relevé de la place de marché monday.com : catalogue public
(https://cdn.monday.com/public_marketplace_apps) puis page de chaque app
(installations, note, nombre d'avis, prix). Sortie : monday.csv."""
import asyncio, csv, json, os, re, sys, urllib.request
from playwright.async_api import async_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
def catalogue():
    """Catalogue local (argument) ou téléchargé, avec nouvelles tentatives."""
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        return json.load(open(sys.argv[1]))["marketplace_apps"]
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(
                "https://cdn.monday.com/public_marketplace_apps",
                headers={"User-Agent": "Mozilla/5.0"}), timeout=120))["marketplace_apps"]
        except Exception:
            pass
    raise SystemExit("catalogue monday.com inaccessible")

apps = catalogue()

async def main():
    w = csv.writer(open("monday.csv", "w", newline="", encoding="utf-8"))
    w.writerow(["id", "nom", "prix", "installations", "note", "avis", "resume"])
    file = asyncio.Queue()
    for a in apps:
        file.put_nowait(a)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=["--headless=new"])
        async def ouvrier():
            pg = await b.new_page()
            while not file.empty():
                a = await file.get()
                try:
                    await pg.goto(f"https://monday.com/marketplace/listing/{a['id']}", timeout=60000)
                    await pg.wait_for_timeout(3500)
                    t = re.sub(r"\n+", " | ", await pg.inner_text("body"))
                except Exception:
                    continue
                inst = re.search(r"Installs \| ([\d,]+)", t)
                note = re.search(r"Rating \| (\d(?:\.\d)?) \| \((\d[\d,]*)\)", t)
                w.writerow([a["id"], a["name"], a.get("pricing_data") or "",
                            int(inst.group(1).replace(",", "")) if inst else 0,
                            note.group(1) if note else "", int(note.group(2).replace(",", "")) if note else 0,
                            (a.get("short_description") or "")[:150]])
        await asyncio.gather(*[ouvrier() for _ in range(4)])
        await b.close()

asyncio.run(main())
