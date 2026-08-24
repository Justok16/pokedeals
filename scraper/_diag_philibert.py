"""Script de diagnostic JETABLE -- inspecte la structure reelle de la
categorie Pokemon sur philibertnet.com (pagination, disponibilite/mention
precommande visible sur le listing ou seulement sur la fiche produit,
JSON-LD). Sera supprime une fois le vrai connecteur cible ecrit."""
import re

import requests

from connecteur_shopify import HEADERS_HTML, TIMEOUT

URL = "https://www.philibertnet.com/fr/212-pokemon"

r = requests.get(URL, headers=HEADERS_HTML, timeout=TIMEOUT)
print("status:", r.status_code, "len:", len(r.text))

html = r.text

# Pagination
print("\n--- pagination ---")
for m in re.finditer(r'href="([^"]*page[^"]*)"', html, re.I):
    print(m.group(1))

# Nombre de produits annonce
m = re.search(r'([\d\s]+)\s*(?:produits?|résultats?|articles?)', html, re.I)
print("\nnb produits annonce approx:", m.group(0) if m else None)

# Precommande mention sur le listing
print("\n--- mentions precommande sur le listing ---")
for m in list(re.finditer(r'.{40}pr[ée]commande.{40}', html, re.I))[:5]:
    print(repr(m.group(0)))

# JSON-LD sur la page listing
print("\n--- json-ld present ---", "application/ld+json" in html)

# Un lien produit exemple
m = re.search(r'href="(https://www\.philibertnet\.com/fr/pokemon/[^"]+)"', html)
print("\nlien produit exemple:", m.group(1) if m else None)

# Categorie/sous-filtre precommande ?
print("\n--- sous-liens categorie contenant 'precommande' ---")
for m in list(re.finditer(r'href="([^"]*precommande[^"]*)"', html, re.I))[:10]:
    print(m.group(1))
