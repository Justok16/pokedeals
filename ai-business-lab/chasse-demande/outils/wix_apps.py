"""Relevé de la boutique d'apps Wix (pages rendues par un vrai navigateur).

Parcourt chaque sous-catégorie de https://www.wix.com/app-market, fait défiler
la page jusqu'à charger toutes les apps, puis lit : nom, accroche, prix,
note, nombre d'avis. Sortie : wix_apps.csv. Nécessite Playwright + Chromium
(le magasin de certificats NSS doit contenir l'autorité du proxy).
"""
import csv, re
from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PRIX = re.compile(r"^(Free to install|Free plan available|Free|\d+ day free trial|From .*|\$.*)$")

def lire_apps(texte, cat):
    lignes = [l.strip() for l in texte.split("\n") if l.strip()]
    apps = []
    for i, l in enumerate(lignes):
        if re.fullmatch(r"\(\d[\d,]*\)", l) and i >= 4:
            note = lignes[i - 1]
            prix = lignes[i - 2]
            if not re.fullmatch(r"\d(\.\d)?", note) or not PRIX.match(prix):
                continue
            nom, accroche = lignes[i - 4], lignes[i - 3]
            apps.append([cat, nom, accroche, prix, note, int(l.strip("()").replace(",", ""))])
    return apps

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--headless=new"])
        pg = b.new_page()
        pg.goto("https://www.wix.com/app-market", timeout=90000)
        pg.wait_for_timeout(5000)
        cats = sorted({re.sub(r"\?.*", "", h) for h in pg.eval_on_selector_all("a", "e=>e.map(x=>x.href)")
                       if re.search(r"/app-market/category/[^/]+/[^/?]+", h)})
        print(len(cats), "sous-catégories", flush=True)
        w = csv.writer(open("wix_apps.csv", "w", newline="", encoding="utf-8"))
        w.writerow(["categorie", "nom", "accroche", "prix", "note", "avis"])
        for c in cats:
            try:
                pg.goto(c, timeout=90000)
                pg.wait_for_timeout(4000)
                avant = 0
                for _ in range(40):
                    pg.mouse.wheel(0, 6000)
                    pg.wait_for_timeout(900)
                    h = pg.evaluate("document.body.scrollHeight")
                    if h == avant:
                        break
                    avant = h
                apps = lire_apps(pg.inner_text("body"), c.split("/category/")[1])
                w.writerows(apps)
                print(c.split("/category/")[1], len(apps), flush=True)
            except Exception as e:
                print("échec", c, e, flush=True)
        b.close()

if __name__ == "__main__":
    main()
