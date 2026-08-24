"""Script de diagnostic JETABLE (v2) -- inspecte la sous-categorie
Precommandes > Jeux de cartes a collectionner de philibertnet.com."""
import re

import requests

from connecteur_shopify import HEADERS_HTML, TIMEOUT

URL = "https://www.philibertnet.com/fr/578-precommandes/s-3/categorie-jeux_de_cartes_a_collectionner_et_jeux_de_cartes_evolutifs"

r = requests.get(URL, headers=HEADERS_HTML, timeout=TIMEOUT)
print("status:", r.status_code, "len:", len(r.text))
html = r.text

print("\n--- liens contenant 'pokemon' (insensible casse) ---")
for m in list(set(re.findall(r'href="([^"]*pokemon[^"]*)"', html, re.I)))[:10]:
    print(m)

print("\n--- pagination (classe/attribut courants PrestaShop) ---")
for m in list(set(re.findall(r'href="([^"]*[?&]page=\d+[^"]*)"', html)))[:10]:
    print(m)
m2 = re.search(r'class="pagination[^"]*"[^>]*>.{0,600}', html, re.S)
print(m2.group(0)[:600] if m2 else "aucun bloc pagination trouve")

print("\n--- exemple de bloc produit (autour du premier 'product-title' ou similaire) ---")
m3 = re.search(r'(product[-_]?(?:title|name|link|thumb))', html, re.I)
print("indice trouve:", m3.group(0) if m3 else None)
if m3:
    i = m3.start()
    print(html[max(0, i-300):i+500])

print("\n--- tous les hrefs vers des fiches produit (motif /fr/<chiffres>-...) ---")
liens = list(set(re.findall(r'href="(https://www\.philibertnet\.com/fr/[0-9]+-[^"]+)"', html)))
print(f"{len(liens)} liens trouves, 10 premiers:")
for l in liens[:10]:
    print(l)

print("\n--- nombre total de resultats annonce ---")
m4 = re.search(r'([\d\s]{1,6})\s*résultats?', html, re.I)
print(m4.group(0) if m4 else None)
