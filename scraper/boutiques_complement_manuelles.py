"""Sources ajoutees manuellement : ne pas ecraser lors des decouvertes.

Verifiees HTTP 200 le 08/10/2026 avec User-Agent honnete :
etw-tcg.com /collections/pokemon-30e-anniversaire/products.json?limit=250
lorenzone.fr /products/coffret-ultra-premium-upc-30eme-anniversaire.js
Notices legales : SIRET 99367661800016 et 93444064500018 respectivement.
"""
BOUTIQUES_SHOPIFY = ["etw-tcg.com", "lorenzone.fr"]

# Le mandat est vendeurs FRANCAIS, pas simplement cartes en francais.
# Exclusion appliquee aussi apres regeneration de l'annuaire automatique.
VENDEURS_HORS_FRANCE = frozenset({"outpostbrussels.be"})
