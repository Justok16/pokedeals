#!/usr/bin/env python3
"""Reprise du contenu d'un ancien site d'artisan (09/10/2026), pour refaire SA page d'accueil plus vite.

Idée tirée du reel « Reverse Engineer Anything » (46-apprentissage-continu.md), ramenée à ce qui est légal : on ne
copie ni le code ni le design d'un tiers ; on récupère les **faits et les textes du client lui-même** (nom, métier,
services, zone, horaires, téléphone, années, photos et logo) pour qu'il retrouve son contenu dans la démo de son
nouveau site. À n'utiliser que sur le site du prospect concerné, et ses photos ou son logo seulement avec son accord
(décision du 05/10). Lecture polie : quelques pages du même site, une pause entre chaque, robots.txt respecté.

Usage : python3 outils/prospects/reprise_site.py <adresse du site> <dossier privé> [nb_pages, défaut 6]
Écrit <dossier>/<domaine>.json (fiche structurée) et <domaine>.md (résumé lisible). Le dossier doit être PRIVÉ
(scratchpad ou Drive « Dig ») : jamais dans ce dépôt public.
"""

import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser

AGENT = "Mozilla/5.0 (compatible; DIG16-reprise/1.0; +https://dig16.fr)"
TEL = re.compile(r"(?:\+33\s?|0)[1-9](?:[\s.-]?\d{2}){4}")
JOURS = re.compile(r"\b(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)\b[^<\n]{0,80}", re.I)
ANNEE = re.compile(r"\b(?:depuis|créée? en|fondée? en|en activité depuis)\s+(19\d\d|20[0-2]\d)\b", re.I)
CP = re.compile(r"\b(16\d{3}|17\d{3}|79\d{3}|86\d{3}|87\d{3}|24\d{3})\s+([A-ZÉÈ][\w' -]{2,40})")
MOTS_PAGES = ("service", "prestation", "activit", "savoir", "realisation", "réalisation", "contact", "propos", "qui-sommes",
              "entreprise", "horaire", "tarif", "carte", "menu")


def lire(url):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept-Language": "fr"})
    with urllib.request.urlopen(req, timeout=20) as r:
        if "html" not in (r.headers.get("Content-Type") or "html"):
            return ""
        return r.read(2_000_000).decode(r.headers.get_content_charset() or "utf-8", "replace")


def texte(fragment):
    fragment = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", fragment)
    fragment = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr)>", "\n", fragment)
    t = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return "\n".join(" ".join(ligne.split()) for ligne in t.splitlines() if ligne.strip())


def attr(tag, nom):
    m = re.search(r'%s\s*=\s*["\']([^"\']+)' % nom, tag, re.I)
    return html.unescape(m.group(1)) if m else ""


def analyser(url, page):
    titres = [texte(h) for h in re.findall(r"(?is)<h[1-3][^>]*>(.*?)</h[1-3]>", page)]
    imgs = []
    for tag in re.findall(r"(?i)<img\b[^>]*>", page):
        src = attr(tag, "src") or attr(tag, "data-src")
        if src and not src.startswith("data:"):
            imgs.append({"src": urllib.parse.urljoin(url, src), "alt": attr(tag, "alt"),
                         "logo_probable": bool(re.search(r"logo", tag, re.I))})
    meta = re.search(r'(?is)<meta[^>]+name=["\']description["\'][^>]*>', page)
    corps = texte(page)
    return {
        "adresse": url,
        "titre": texte(m.group(1)) if (m := re.search(r"(?is)<title[^>]*>(.*?)</title>", page)) else "",
        "description": attr(meta.group(0), "content") if meta else "",
        "titres": [t for t in titres if 2 < len(t) < 120][:25],
        "telephones": sorted({re.sub(r"[\s.-]", " ", t).strip() for t in TEL.findall(corps)}),
        "horaires": sorted({m.group(0).strip() for m in JOURS.finditer(corps)})[:14],
        "annees": sorted(set(ANNEE.findall(corps))),
        "villes": sorted({f"{c} {v.strip()}" for c, v in CP.findall(corps)})[:10],
        "images": imgs[:40],
        "texte": corps[:6000],
    }


def liens_internes(base, page):
    hote = urllib.parse.urlparse(base).netloc
    vus = []
    for href in re.findall(r'(?i)<a\b[^>]*href=["\']([^"\'#]+)', page):
        u = urllib.parse.urljoin(base, html.unescape(href)).split("#")[0]
        p = urllib.parse.urlparse(u)
        if p.netloc == hote and p.scheme in ("http", "https") and u not in vus and not re.search(r"\.(pdf|jpe?g|png|zip|docx?)$", p.path, re.I):
            vus.append(u)
    return sorted(vus, key=lambda u: not any(m in u.lower() for m in MOTS_PAGES))


def main(url, dossier, nb=6):
    if not re.match(r"https?://", url):
        url = "https://" + url
    robots = urllib.robotparser.RobotFileParser(urllib.parse.urljoin(url, "/robots.txt"))
    try:
        robots.read()
    except Exception:
        robots = None
    accueil = lire(url)
    pages = [analyser(url, accueil)]
    for u in liens_internes(url, accueil):
        if len(pages) >= nb:
            break
        if u.rstrip("/") == url.rstrip("/") or (robots and not robots.can_fetch(AGENT, u)):
            continue
        time.sleep(1.5)
        try:
            pages.append(analyser(u, lire(u)))
        except Exception as e:
            pages.append({"adresse": u, "erreur": str(e)[:120]})
    ok = [p for p in pages if "erreur" not in p]
    fiche = {
        "site": url, "lu_le": time.strftime("%Y-%m-%d"), "pages": pages,
        "synthese": {
            "nom_probable": ok[0]["titre"].split("|")[0].split(" - ")[0].strip() if ok else "",
            "description": ok[0]["description"] if ok else "",
            "telephones": sorted({t for p in ok for t in p["telephones"]}),
            "horaires": sorted({h for p in ok for h in p["horaires"]})[:14],
            "annees": sorted({a for p in ok for a in p["annees"]}),
            "villes": sorted({v for p in ok for v in p["villes"]})[:10],
            "services_probables": list(dict.fromkeys(t for p in ok for t in p["titres"]))[:30],
            "logos_probables": list(dict.fromkeys(i["src"] for p in ok for i in p["images"] if i["logo_probable"]))[:5],
            "photos": list(dict.fromkeys(i["src"] for p in ok for i in p["images"] if not i["logo_probable"]))[:40],
        },
        "rappel": "Contenu du client seulement ; photos et logo dans une démo uniquement avec son accord ; ne rien publier.",
    }
    os.makedirs(dossier, exist_ok=True)
    nom = urllib.parse.urlparse(url).netloc.replace("www.", "")
    with open(os.path.join(dossier, nom + ".json"), "w", encoding="utf-8") as f:
        json.dump(fiche, f, ensure_ascii=False, indent=1)
    s = fiche["synthese"]
    lignes = [f"# Reprise du site {url} (lu le {fiche['lu_le']}, {len(ok)} page(s))", "",
              f"- Nom probable : {s['nom_probable']}", f"- Description : {s['description']}",
              f"- Téléphones : {', '.join(s['telephones']) or '—'}", f"- Années citées : {', '.join(s['annees']) or '—'}",
              f"- Villes : {', '.join(s['villes']) or '—'}", f"- Logos probables : {len(s['logos_probables'])} ; photos : {len(s['photos'])}",
              "", "## Horaires repérés", *([f"- {h}" for h in s["horaires"]] or ["- —"]),
              "", "## Titres de sections (services probables)", *([f"- {t}" for t in s["services_probables"]] or ["- —"]),
              "", "> " + fiche["rappel"]]
    with open(os.path.join(dossier, nom + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"{nom} : {len(ok)} page(s) lue(s), {len(s['telephones'])} téléphone(s), {len(s['services_probables'])} titre(s), "
          f"{len(s['photos'])} photo(s), {len(s['logos_probables'])} logo(s) probable(s) -> {dossier}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 6)
