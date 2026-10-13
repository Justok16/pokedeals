# Cherche les adresses email publiques d'un organisme : page d'accueil + pages contact, économie, presse,
# rédaction (navigateur réel, rendu JavaScript). Usage : python3 outils/trouver_contact.py URL [URL...]
# Les résultats s'affichent seulement : ne jamais les recopier dans le dépôt public (citer la page source).
import re, sys
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
KEY=re.compile(r"(contact|econom|entrepr|entreprise|nous-joindre|developpement|presse|redaction|commerce)",re.I)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    ctx=b.new_context(locale="fr-FR",user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36")
    for start in sys.argv[1:]:
        pg=ctx.new_page(); found={}; seen=set()
        try:
            pg.goto(start,timeout=30000,wait_until="domcontentloaded"); pg.wait_for_timeout(2500)
            host=urlparse(pg.url).netloc
            links=[urljoin(pg.url,h) for h in re.findall(r'href="([^"#]+)"',pg.content())]
            cand=[l for l in dict.fromkeys(links) if urlparse(l).netloc==host and KEY.search(l)][:8]
            for u in [pg.url]+cand:
                if u in seen: continue
                seen.add(u)
                try:
                    pg.goto(u,timeout=25000,wait_until="domcontentloaded"); pg.wait_for_timeout(1500)
                    h=pg.content()
                    for m in set(re.findall(r"[\w.+-]+@[\w-]+\.[a-z]{2,}(?:\.[a-z]{2,})?",h)):
                        if not re.search(r"\.(png|jpg|webp|svg|gif)$",m): found.setdefault(m,u)
                except Exception: pass
            print("==",start,"->",host); [print("  ",m,"<-",u) for m,u in found.items()]
        except Exception as e: print("==",start,"ERR",str(e)[:100])
        pg.close()
    b.close()
