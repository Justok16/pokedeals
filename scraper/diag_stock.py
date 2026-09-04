"""Script de diagnostic JETABLE (pas destine a rester dans le depot) --
inspecte pourquoi verifier_une_alerte() dit "disponible" pour une URL
precise alors que la page affiche "rupture de stock"."""
import re

import requests

from connecteur_prestashop_sitemap import (
    _analyser_offre as _analyser_offre_prestashop,
    _extraire_jsonld_produit as _extraire_jsonld_prestashop,
    _extraire_microdata_produit,
    _stock_indisponible_selon_dom,
    MOTS_RUPTURE_DOM,
)
from connecteur_shopify import HEADERS_HTML
from verification_alertes import verifier_une_alerte

URL = "https://plazatcg.com/cartes-a-l-unite/1214-plumeline-ex-024-promo-mep-black-star-promos.html"

r = requests.get(URL, headers=HEADERS_HTML, timeout=15)
print("STATUS:", r.status_code)
html = r.text
print("LEN HTML:", len(html))

print("\n--- MOTS_RUPTURE_DOM ---")
print(MOTS_RUPTURE_DOM)

m = re.search(r'<span[^>]*id="product-availability"[^>]*>(.*?)</span>', html, re.S)
print("\n--- span#product-availability trouve ? ---", bool(m))
if m:
    print("CONTENU BRUT:", repr(m.group(0))[:1000])

print("\n--- recherche large de 'availability' dans le HTML ---")
for mm in re.finditer(r'[^>]{0,60}availability[^<]{0,200}', html, re.I):
    print(repr(mm.group(0))[:300])

print("\n--- recherche large de 'rupture' dans le HTML ---")
for mm in re.finditer(r'.{0,80}rupture.{0,120}', html, re.I):
    print(repr(mm.group(0))[:300])

produit = _extraire_jsonld_prestashop(html)
print("\n--- JSON-LD Product trouve ? ---", bool(produit))
if produit:
    print("JSON-LD:", produit)
    offre = _analyser_offre_prestashop(produit)
    print("Offre analysee depuis JSON-LD:", offre)
else:
    offre = _extraire_microdata_produit(html)
    print("Offre analysee depuis microdata:", offre)

print("\n--- _stock_indisponible_selon_dom(html) ---", _stock_indisponible_selon_dom(html))

print("\n--- Resultat verifier_une_alerte() (fonction reellement utilisee en prod) ---")
print(verifier_une_alerte(URL))
