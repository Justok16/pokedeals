#!/usr/bin/env python3
"""Contrôle SEO d'un site client DIG16 (12/10/2026), à lancer avant chaque livraison puis chaque mois.

Usage :
  python3 outils/seo_client.py https://site-du-client.fr/            # audit (ALERTE = bloque la livraison)
  python3 outils/seo_client.py https://site-du-client.fr/ --local    # tolère l'absence de HTTPS (préproduction)
  python3 outils/seo_client.py --schema fiche.json                   # écrit le JSON-LD « entreprise locale »

Le contrôle lit le plan du site (sitemap.xml) ou, à défaut, les liens internes de l'accueil, rend chaque page
dans Chromium (comme Google) et vérifie, page par page : code 200, titre 30-60 caractères et unique, description
70-160 caractères et unique, un seul H1, niveaux de titres sans saut, canonique vers elle-même, langue fr,
viewport, image de partage, texte alternatif des images, liens internes sans redirection, absence de « noindex »
involontaire et d'adresse email masquée par Cloudflare (lien /cdn-cgi/ en 404). Pour le site : HTTPS, robots.txt
qui cite le plan du site, et données structurées « entreprise locale » complètes sur l'accueil (nom, adresse ou
zone desservie, téléphone, horaires, URL). Sortie : OK / ATTENTION / ALERTE, code de retour 1 s'il reste une ALERTE.

Le fichier fiche.json (privé, jamais dans le dépôt) contient : nom, metier (clé de METIERS), url, telephone,
email, adresse {rue, cp, ville}, masquer_adresse (vrai si l'artisan se déplace chez ses clients), zone (liste de
communes), horaires [{jours: ["Monday", …], ouvre: "08:00", ferme: "18:00"}], reseaux (liste d'URL),
logo, image, prix ("€€"), siren, latitude, longitude.
"""

import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

import requests
from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
UA = "Mozilla/5.0 (compatible; DIG16-controle-SEO/1.0)"

# Type schema.org le plus précis pour chaque métier courant (liste officielle : schema.org/LocalBusiness)
METIERS = {
    "plombier": "Plumber", "electricien": "Electrician", "chauffagiste": "HVACBusiness", "couvreur": "RoofingContractor",
    "peintre": "HousePainter", "serrurier": "Locksmith", "menuisier": "GeneralContractor", "macon": "GeneralContractor",
    "paysagiste": "HomeAndConstructionBusiness", "carreleur": "GeneralContractor",
    "garage": "AutoRepair", "carrossier": "AutoBodyShop", "coiffeur": "HairSalon", "estheticienne": "BeautySalon",
    "boulanger": "Bakery", "restaurant": "Restaurant", "hotel": "Hotel", "fleuriste": "Florist",
    "boutique": "Store", "toiletteur": "LocalBusiness", "photographe": "LocalBusiness", "nettoyage": "HomeAndConstructionBusiness",
}


def schema(fiche):
    """JSON-LD « entreprise locale » à partir d'une fiche client (aucune donnée inventée : champ absent = omis)."""
    t = METIERS.get(fiche.get("metier", ""), "LocalBusiness")
    d = {"@context": "https://schema.org", "@type": t, "@id": fiche["url"].rstrip("/") + "/#entreprise",
         "name": fiche["nom"], "url": fiche["url"]}
    for cle, champ in (("telephone", "telephone"), ("email", "email"), ("logo", "logo"), ("image", "image"),
                       ("priceRange", "prix")):
        if fiche.get(champ):
            d[cle] = fiche[champ]
    a = fiche.get("adresse")
    if a and not fiche.get("masquer_adresse"):
        d["address"] = {"@type": "PostalAddress", "streetAddress": a.get("rue", ""), "postalCode": a.get("cp", ""),
                        "addressLocality": a.get("ville", ""), "addressRegion": "Charente", "addressCountry": "FR"}
        if fiche.get("latitude") and fiche.get("longitude"):
            d["geo"] = {"@type": "GeoCoordinates", "latitude": fiche["latitude"], "longitude": fiche["longitude"]}
    elif a:
        d["address"] = {"@type": "PostalAddress", "addressLocality": a.get("ville", ""), "postalCode": a.get("cp", ""),
                        "addressRegion": "Charente", "addressCountry": "FR"}
    if fiche.get("zone"):
        d["areaServed"] = [{"@type": "City", "name": v} for v in fiche["zone"]]
    if fiche.get("horaires"):
        d["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["jours"],
                                           "opens": h["ouvre"], "closes": h["ferme"]} for h in fiche["horaires"]]
    if fiche.get("reseaux"):
        d["sameAs"] = fiche["reseaux"]
    if fiche.get("siren"):
        d["identifier"] = {"@type": "PropertyValue", "propertyID": "SIREN", "value": str(fiche["siren"]).replace(" ", "")}
    return d


def pages_du_site(base):
    try:
        r = requests.get(urllib.parse.urljoin(base, "/sitemap.xml"), headers={"User-Agent": UA}, timeout=20)
        if r.ok and "<urlset" in r.text:
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            return [e.text.strip() for e in ET.fromstring(r.content).findall("s:url/s:loc", ns)], True
    except (requests.RequestException, ET.ParseError):
        pass
    return [base], False


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--schema":
        print(json.dumps(schema(json.load(open(sys.argv[2], encoding="utf-8"))), ensure_ascii=False, indent=1))
        return 0
    base = sys.argv[1]
    local = "--local" in sys.argv
    hote = urllib.parse.urlparse(base).netloc
    alertes, attentions = [], []
    A = lambda m: alertes.append(m)  # noqa: E731
    W = lambda m: attentions.append(m)  # noqa: E731

    if not base.startswith("https://") and not local:
        A("le site n'est pas en HTTPS")
    urls, a_sitemap = pages_du_site(base)
    if not a_sitemap:
        A("pas de sitemap.xml lisible")
    try:
        rob = requests.get(urllib.parse.urljoin(base, "/robots.txt"), headers={"User-Agent": UA}, timeout=20)
        if not rob.ok or "sitemap" not in rob.text.lower():
            W("robots.txt absent ou ne cite pas le plan du site")
        if re.search(r"(?im)^disallow:\s*/\s*$", rob.text or ""):
            A("robots.txt interdit tout le site (Disallow: /)")
    except requests.RequestException:
        W("robots.txt illisible")

    titres, descs, liens_internes = {}, {}, set()
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        for i, u in enumerate(urls[:60]):
            pg = nav.new_page(user_agent=UA)
            r = pg.goto(u, wait_until="networkidle")
            code = r.status if r else 0
            if code != 200:
                A(f"{u} : code {code}")
                pg.close()
                continue
            d = pg.evaluate("""() => ({
              t: document.title.trim(), md: (document.querySelector('meta[name=description]')||{}).content||'',
              h: [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e => +e.tagName[1]),
              can: (document.querySelector('link[rel=canonical]')||{}).href||'',
              rob: ((document.querySelector('meta[name=robots]')||{}).content||'').toLowerCase(),
              lang: document.documentElement.lang, vp: !!document.querySelector('meta[name=viewport]'),
              og: !!document.querySelector('meta[property="og:image"]'),
              noalt: [...document.images].filter(i => !i.hasAttribute('alt')).map(i => i.src).slice(0, 3),
              ld: [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent),
              liens: [...document.querySelectorAll('a[href]')].map(a => a.href),
              cfmail: !!document.querySelector('a[href*="/cdn-cgi/l/email-protection"]')})""")
            nom = urllib.parse.urlparse(u).path or "/"
            n1 = d["h"].count(1)
            if not d["t"]:
                A(f"{nom} : pas de titre")
            elif not 30 <= len(d["t"]) <= 60:
                W(f"{nom} : titre de {len(d['t'])} caractères (viser 30 à 60)")
            if not d["md"]:
                A(f"{nom} : pas de description")
            elif not 70 <= len(d["md"]) <= 160:
                W(f"{nom} : description de {len(d['md'])} caractères (viser 70 à 160)")
            titres.setdefault(d["t"], []).append(nom)
            descs.setdefault(d["md"], []).append(nom)
            if n1 != 1:
                A(f"{nom} : {n1} titre(s) H1 (il en faut exactement 1)")
            if any(b - a > 1 for a, b in zip(d["h"], d["h"][1:])):
                W(f"{nom} : niveaux de titres qui sautent (ex. H2 puis H4)")
            if not d["can"]:
                W(f"{nom} : pas de lien canonique")
            elif d["can"].rstrip("/") != u.rstrip("/"):
                W(f"{nom} : canonique vers {d['can']} (différent de l'adresse du plan du site)")
            if "noindex" in d["rob"]:
                A(f"{nom} : « noindex » (la page ne sortira jamais sur Google)")
            if not d["lang"].startswith("fr"):
                W(f"{nom} : langue de la page « {d['lang']} » (attendu fr)")
            if not d["vp"]:
                A(f"{nom} : pas de viewport (site non adapté au téléphone)")
            if not d["og"]:
                W(f"{nom} : pas d'image de partage (og:image)")
            if d["noalt"]:
                W(f"{nom} : images sans texte alternatif ({', '.join(d['noalt'])})")
            if d["cfmail"]:
                A(f"{nom} : email masqué par Cloudflare (/cdn-cgi/, 404 pour Google) : entourer de <!--email_off-->")
            for lien in d["liens"]:
                pl = urllib.parse.urlparse(lien)
                if pl.netloc == hote and pl.scheme.startswith("http"):
                    liens_internes.add(lien.split("#")[0])
            if i == 0:
                locaux = []
                for brut in d["ld"]:
                    try:
                        j = json.loads(brut)
                    except json.JSONDecodeError:
                        A("/ : données structurées illisibles (JSON invalide)")
                        continue
                    for x in j.get("@graph", [j]) if isinstance(j, dict) else j:
                        types = x.get("@type", [])
                        types = types if isinstance(types, list) else [types]
                        if any(t in METIERS.values() or t in ("LocalBusiness", "ProfessionalService") for t in types):
                            locaux.append(x)
                if not locaux:
                    A("/ : pas de données structurées « entreprise locale » (LocalBusiness ou métier précis)")
                for x in locaux:
                    for champ in ("name", "telephone", "url"):
                        if not x.get(champ):
                            A(f"/ : données structurées sans « {champ} »")
                    if not x.get("address") and not x.get("areaServed"):
                        A("/ : données structurées sans adresse ni zone desservie")
                    if not x.get("openingHoursSpecification") and not x.get("openingHours"):
                        W("/ : données structurées sans horaires")
                    if not x.get("sameAs"):
                        W("/ : données structurées sans liens vers les réseaux et la fiche Google (sameAs)")
            pg.close()
        nav.close()

    for t, ou in titres.items():
        if t and len(ou) > 1:
            A(f"titre identique sur {len(ou)} pages : {', '.join(ou)}")
    for t, ou in descs.items():
        if t and len(ou) > 1:
            W(f"description identique sur {len(ou)} pages : {', '.join(ou)}")
    for lien in sorted(liens_internes)[:150]:
        try:
            r = requests.head(lien, headers={"User-Agent": UA}, timeout=15, allow_redirects=False)
            if r.status_code in (301, 302, 307, 308):
                W(f"lien interne qui redirige : {lien} → {r.headers.get('location')}")
            elif r.status_code >= 400:
                A(f"lien interne cassé ({r.status_code}) : {lien}")
        except requests.RequestException:
            W(f"lien interne injoignable : {lien}")

    print(f"Contrôle SEO de {base} : {len(urls[:60])} page(s)")
    for m in alertes:
        print("ALERTE   ", m)
    for m in attentions:
        print("ATTENTION", m)
    if not alertes and not attentions:
        print("OK        aucun défaut")
    return 1 if alertes else 0


if __name__ == "__main__":
    raise SystemExit(main())
