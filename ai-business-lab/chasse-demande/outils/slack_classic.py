"""Apps de la Slack Marketplace encore « classic » (fin de fonctionnement le
16/11/2026 : docs.slack.dev/changelog/2024-09-legacy-custom-bots-classic-apps-deprecation).
Source : sitemap public slack.com/sitemaps/sitemap_marketplace_en-us.xml
(robots.txt ne l'interdit pas). Une app est marquée « classic » si sa fiche
demande la permission générique `bot` (ou les anciennes `client`, `read`,
`post`), inexistantes chez les apps à permissions granulaires.
Usage : python3 slack_classic.py urls.txt -> slack.csv"""
import csv, html, json, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ANCIENNES = {"bot", "client", "read", "post", "identify"}

def lire(u):
    for _ in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40)
            return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(5)
    return ""

def traiter(u):
    s = html.unescape(lire(u))
    if not s:
        return [u, "", "", "", "", "erreur"]
    nom = re.search(r"<title>([^<]*)</title>", s)
    prix = re.search(r'"pricing":"([^"]*)"', s)
    scopes = set(re.findall(r'"scopes":\[([^\]]*)\]', s))
    tous = set()
    for g in scopes:
        tous |= set(x.strip('"') for x in g.split(",") if x)
    anciens = sorted(tous & ANCIENNES)
    time.sleep(0.5)
    return [u, nom.group(1).strip() if nom else "", prix.group(1) if prix else "",
            " ".join(sorted(tous)), " ".join(anciens), "classic" if "bot" in anciens or {"client", "read", "post"} & set(anciens) else ""]

urls = [l.strip() for l in open(sys.argv[1]) if l.strip()]
w = csv.writer(open("slack.csv", "w", newline="", encoding="utf-8"))
w.writerow(["url", "nom", "prix", "scopes", "scopes_anciens", "statut"])
with ThreadPoolExecutor(4) as ex:
    for x in ex.map(traiter, urls):
        w.writerow(x)
