"""Pack visibilité d'un site client publié : Google et assistants IA (ChatGPT, Claude, Perplexity).

Idées tirées de la grille GEO Optimizer (Auriti-Labs/geo-optimizer-skill, licence MIT, grille lue le 29/09/2026)
et de l'offre de Durable (fiche d'entreprise, annuaires, llms.txt). Rien n'est inventé : tout vient de la fiche client.

Usage : python3 pack_visibilite.py <dossier_du_site> <fiche_client.json>
La fiche (PRIVÉE, jamais dans le dépôt) contient :
  {"nom": "...", "type": "HomeAndConstructionBusiness", "numero_public": "05 45 ...", "rue": "...",
   "code_postal": "16...", "commune": "...", "url": "https://...", "description": "...",
   "zone": ["Cognac", "Jarnac"], "services": ["...", "..."], "horaires": ["Mo-Fr 08:00-18:00"],
   "profils": ["https://www.facebook.com/..."]}
Types schema.org utiles : HomeAndConstructionBusiness, Electrician, Plumber, RoofingContractor, HousePainter,
AutoRepair, HairSalon, Bakery, HardwareStore, Restaurant.
Effets : dans index.html, retire « noindex », ajoute canonical, balises de partage (Open Graph) et données
structurées JSON-LD ; écrit robots.txt (moteurs et assistants IA autorisés), sitemap.xml et llms.txt.
"""

import datetime
import html
import json
import os
import re
import sys

dossier, fiche = sys.argv[1], sys.argv[2]
F = json.load(open(fiche, encoding="utf-8"))
for cle in ("nom", "type", "numero_public", "commune", "url", "description"):
    if not F.get(cle):
        sys.exit(f"fiche incomplète : « {cle} » manquant")
url = F["url"].rstrip("/") + "/"
if not re.match(r"^https://[a-z0-9.-]+\.[a-z]{2,}/$", url):
    sys.exit("adresse du site invalide (https://nom-de-domaine/ attendu)")
standard = re.sub(
    r"\D", "", F["numero_public"]
)  # standard public de l'entreprise, publié exprès
standard_intl = (
    "+33" + standard[1:]
    if len(standard) == 10 and standard.startswith("0")
    else F["numero_public"]
)

ld = {
    "@context": "https://schema.org",
    "@type": F["type"],
    "name": F["nom"],
    "url": url,
    "telephone": standard_intl,
    "description": F["description"],
    "address": {
        "@type": "PostalAddress",
        "addressLocality": F["commune"],
        "addressCountry": "FR",
    },
}
if F.get("rue"):
    ld["address"]["streetAddress"] = F["rue"]
if F.get("code_postal"):
    ld["address"]["postalCode"] = F["code_postal"]
if F.get("zone"):
    ld["areaServed"] = [{"@type": "City", "name": z} for z in F["zone"]]
if F.get("horaires"):
    ld["openingHours"] = F["horaires"]
if F.get("profils"):
    ld["sameAs"] = F["profils"]
if F.get("services"):
    ld["makesOffer"] = [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}}
        for s in F["services"]
    ]
site = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": F["nom"],
    "url": url,
    "inLanguage": "fr-FR",
}
bloc_ld = json.dumps([ld, site], ensure_ascii=False).replace(
    "</", "<\\/"
)  # pas de fermeture de balise possible

a = lambda t: html.escape(t, quote=True)
tete = (
    f'<link rel="canonical" href="{a(url)}">'
    f'<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR">'
    f'<meta property="og:title" content="{a(F["nom"])}"><meta property="og:description" content="{a(F["description"])}">'
    f'<meta property="og:url" content="{a(url)}">'
    f'<script type="application/ld+json">{bloc_ld}</script>'
)
p = os.path.join(dossier, "index.html")
s = open(p, encoding="utf-8").read()
s = re.sub(r'<meta name="robots" content="noindex[^"]*">', "", s)
s = re.sub(
    r'<link rel="canonical"[^>]*>|<meta property="og:[^>]*>|<script type="application/ld\+json">.*?</script>',
    "",
    s,
    flags=re.S,
)
if '<meta name="description"' not in s:
    tete = f'<meta name="description" content="{a(F["description"])}">' + tete
s = s.replace("</head>", tete + "</head>", 1)
open(p, "w", encoding="utf-8").write(s)

open(os.path.join(dossier, "robots.txt"), "w").write(
    "# Moteurs de recherche et assistants IA autorisés (ils citent les sites qu’ils peuvent lire)\n"
    "User-agent: *\nAllow: /\n\n"
    + "".join(
        f"User-agent: {b}\nAllow: /\n\n"
        for b in (
            "OAI-SearchBot",
            "ChatGPT-User",
            "ClaudeBot",
            "Claude-SearchBot",
            "PerplexityBot",
            "Google-Extended",
        )
    )
    + f"Sitemap: {url}sitemap.xml\n"
)
jour = datetime.date.today().isoformat()
open(os.path.join(dossier, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    f"<url><loc>{html.escape(url)}</loc><lastmod>{jour}</lastmod></url></urlset>\n"
)
L = [
    f"# {F['nom']}",
    "",
    f"> {F['description']}",
    "",
    "## Coordonnées",
    f"- Téléphone : {F['numero_public']}",
    f"- Adresse : {', '.join(x for x in (F.get('rue'), F.get('code_postal'), F['commune']) if x)}",
    f"- Site : {url}",
]
if F.get("zone"):
    L += ["", "## Zone d’intervention", ", ".join(F["zone"])]
if F.get("services"):
    L += ["", "## Services"] + [f"- {x}" for x in F["services"]]
if F.get("horaires"):
    L += ["", "## Horaires"] + [f"- {x}" for x in F["horaires"]]
open(os.path.join(dossier, "llms.txt"), "w", encoding="utf-8").write(
    "\n".join(L) + "\n"
)
print("pack visibilité ajouté :", p, "+ robots.txt, sitemap.xml, llms.txt")
