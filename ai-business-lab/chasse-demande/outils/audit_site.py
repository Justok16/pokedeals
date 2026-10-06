# Audit du site public https://dig16.fr (06/10/2026) : liens, ressources, erreurs console, mobile, balises, accessibilité de base.
import requests
from playwright.sync_api import sync_playwright

BASE = "https://dig16.fr"
pages = ["/", "/prestige", "/mentions-legales", "/demos/menuisier/", "/demos/prestige/"]
res = {}
liens = set()
with sync_playwright() as p:
    b = p.chromium.launch(
        executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    )
    for chemin in pages:
        for nom, vp in (
            ("mobile", {"width": 390, "height": 844}),
            ("pc", {"width": 1366, "height": 800}),
        ):
            ctx = b.new_context(viewport=vp, is_mobile=(nom == "mobile"))
            pg = ctx.new_page()
            erreurs = []
            ko = []
            pg.on(
                "console",
                lambda m: (
                    erreurs.append(m.text[:140])
                    if m.type in ("error", "warning")
                    else None
                ),
            )
            pg.on(
                "response",
                lambda r: (
                    ko.append((r.status, r.url[:90])) if r.status >= 400 else None
                ),
            )
            try:
                pg.goto(BASE + chemin, wait_until="networkidle", timeout=40000)
            except Exception as e:
                erreurs.append("goto " + str(e)[:80])
            info = pg.evaluate("""()=>({
              titre:document.title, tl:document.title.length,
              desc:(document.querySelector('meta[name=description]')||{}).content||'', 
              h1:document.querySelectorAll('h1').length,
              lang:document.documentElement.lang,
              viewport:!!document.querySelector('meta[name=viewport]'),
              sansalt:[...document.images].filter(i=>!i.hasAttribute('alt')).length,
              nimg:document.images.length,
              defil:document.documentElement.scrollWidth>window.innerWidth+1,
              boutonsvides:[...document.querySelectorAll('button,a')].filter(e=>!(e.textContent.trim()||e.getAttribute('aria-label')||e.querySelector('img[alt]'))).length,
              champsansnom:[...document.querySelectorAll('input,select,textarea')].filter(e=>e.type!='hidden'&&!e.labels?.length&&!e.getAttribute('aria-label')).length,
              petitcible:[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.height<24||r.width<24)&&e.textContent.trim().length>0&&getComputedStyle(e).display!='inline'}).length,
              liens:[...document.querySelectorAll('a[href]')].map(a=>a.href)
            })""")
            for lien in info.pop("liens"):
                liens.add(lien)
            res[f"{chemin}|{nom}"] = dict(info, console=erreurs[:4], http=ko[:4])
            ctx.close()
    b.close()
for k, v in res.items():
    print(
        k,
        "| titre",
        v["tl"],
        "| desc",
        len(v["desc"]),
        "| h1",
        v["h1"],
        "| lang",
        v["lang"],
        "| img sans alt",
        v["sansalt"],
        "/",
        v["nimg"],
        "| défilement horizontal" if v["defil"] else "",
        "| liens/boutons vides",
        v["boutonsvides"],
        "| champs sans nom",
        v["champsansnom"],
        "| cibles <24px",
        v["petitcible"],
        "|",
        v["console"],
        v["http"],
    )
ext = sorted(
    lien for lien in liens if not lien.startswith(BASE) and lien.startswith("http")
)
inte = sorted(lien.split("#")[0] for lien in liens if lien.startswith(BASE))
print("\nliens internes testés :")
for lien in sorted(set(inte)):
    try:
        r = requests.head(lien, timeout=20, allow_redirects=True)
    except Exception as e:
        print("ERREUR", lien, e)
        continue
    if r.status_code >= 400:
        print(r.status_code, lien)
print("liens externes :")
for lien in ext:
    try:
        r = requests.head(
            lien,
            timeout=20,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        print(r.status_code, lien[:100])
    except Exception as e:
        print("ERREUR", lien[:80], str(e)[:50])
