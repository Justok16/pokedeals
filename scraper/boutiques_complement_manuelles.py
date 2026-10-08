"""Sources ajoutees manuellement : ne pas ecraser lors des decouvertes.

Verifiees HTTP 200 le 08/10/2026 avec User-Agent honnete :
etw-tcg.com /collections/pokemon-30e-anniversaire/products.json?limit=250
lorenzone.fr /products/coffret-ultra-premium-upc-30eme-anniversaire.js
Notices legales : SIRET 99367661800016 et 93444064500018 respectivement.
"""
BOUTIQUES_SHOPIFY = ["etw-tcg.com", "lorenzone.fr"]

# Regle de Justok (08/10/2026) : un vendeur etranger est garde s'il LIVRE EN
# FRANCE (le produit, lui, doit etre en version francaise -- cf.
# langue_non_francaise). Exclure ici, par domaine, ceux qui ne livrent pas
# en France ; exclusion appliquee aussi apres regeneration de l'annuaire.
# outpostbrussels.be (BE) remis le 08/10/2026 : livraison France 10 EUR,
# gratuite des 190 EUR, 2-3 jours ouvres (/pages/shipping).
VENDEURS_SANS_LIVRAISON_FRANCE = frozenset()

# WooCommerce lu par la Store API publique (/wp-json/wc/store/v1/products?search=),
# sans sitemap : boutique generaliste (jeux video), un sitemap complet serait
# disproportionne. Verifie le 08/10/2026 : UPC Noctali-ex et Mentali-ex
# "VERSION FRANCAISE" en precommande (is_in_stock + is_purchasable, classe
# available-on-backorder). Fiches doublees /fr/ et /en/ : /en/ ignoree.
BOUTIQUES_WOOCOMMERCE_API_REST = ["www.pixelheart.eu"]
