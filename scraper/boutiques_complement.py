"""
Boutiques COMPLEMENTAIRES du radar de precommandes/disponibilite (cf.
scan_precommandes.py, mode RADAR_PERIMETRE=complement), scannees par leur
propre workflow (scan_complement.yml) -- indépendant des 3 workflows de scan
existants, dont la marge de temps est deja serree (cf. commentaires de
scan_shopify.yml / boutiques_prestashop.py LOT_A/LOT_B).

FICHIER AUTO-GENERE par decouverte_annuaires.py (annuaire Pokescam des
boutiques verifiees a la main + controles de legitimite, cf. legitimite.py)
-- ne pas editer a la main : il est reecrit a chaque execution. Pour retirer
une boutique durablement, l'ajouter a DOMAINES_REFUSES dans
decouverte_annuaires.py.

Derniere mise a jour : 2026-10-04
"""

BOUTIQUES_COMPLEMENT_SHOPIFY = [
    'cardsgamecollect.fr',
    'hitndrop.com',
    'lebordelmagique.com',
    'outpostbrussels.be',
    'pikadisplay.com',
    'tokyocards.com',
]

BOUTIQUES_COMPLEMENT_PRESTASHOP_SITEMAP = [
    'pokesumo.com',
    'pokezenith.com',
    'variantes.com',
]

BOUTIQUES_COMPLEMENT_PRESTASHOP_REPLI_HTML = [
    'pikastore.fr',
]

BOUTIQUES_COMPLEMENT_WOOCOMMERCE_SITEMAP = [
    'ludotrotter.fr',
    'maxicartes.com',
]

# Boutiques verifiees mais SANS connecteur compatible (plateforme maison,
# rendu JavaScript ou anti-robot) -- informatif, pas scannees.
BOUTIQUES_COMPLEMENT_A_CONNECTEUR_DEDIE = [
    'amazon.fr',
    'cultura.com',
    'destocktcg.fr',
    'e.leclerc',
    'fnac.com',
    'joueclub.fr',
    'king-jouet.com',
    'lagranderecre.fr',
    'maisondelapresse.com',
    'micromania.fr',
    'play-in.com',
    'smythstoys.com',
    'ultrajeux.com',
]
