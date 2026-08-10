# Boutiques TCG confirmees Shopify avec API JSON publique /products.json
# Issues de l'audit technique (aout 2026) sur les 122 boutiques de la liste de Justok.
# A utiliser avec connecteur_shopify.py -- un seul connecteur pour toutes ces boutiques.

# RETIREE le 11/08/2026 (demande explicite) : card-binder.com est une
# boutique anglophone vendant des produits anglophones -- hors interet
# pour Justok (watchlist FR/JP).
#   "card-binder.com",

BOUTIQUES_SHOPIFY = [
    "dracaugames.com",
    "cardlabtcg.com",
    "ash-tcg.com",
    "tcgspeed.com",
    "boostrclub.com",
    "pika-boutique.fr",
    "thecollectiblesshop.fr",
    "sakuro.fr",
    "lerepaireducollectionneur.fr",
    "poke-geek.fr",
    "kyoriyu.fr",          # favorite de Justok
    "gamesavenue.fr",
    "lemantcg.fr",
    "hikarudistribution.com",
    "relictcg.com",
    "tradingcardsxxx.fr",
    "mrjoshop.com",
    "pokemagic.fr",
    "hobbyhouse.fr",
    "masterset.store",
    "latavernededream.com",
    "questcorner.fr",      # favorite de Justok
    "lesprofesseurschinent.fr",
    "pramstcg.fr",
    "sneyzencorp.com",
    "japantradingcardstore.com",
    "pokeninjapan.store",
    "neyzertcg.com",
    "sugoitcg.com",
    "leviacards.com",
    "pikadi-collect.fr",
    "fandom.tokyo",
    "cartespokemon.com",
    "kimstcgstore.com",
    "japan2uk.com",
    "riotcg.shop",
    "japanresell.fr",
    "lectorshop.com",
    "cardotaku.com",
]

# Detectees Shopify en priorite 2 (plateforme identifiee mais API non confirmee
# lors de l'audit initial -- a re-tester avec connecteur_shopify.py directement,
# il gere le cas ou products.json ne renvoie rien).
# Retestees le 10/08/2026, toujours NON exploitables (pas un bug cote
# connecteur) :
#   loot-factory.com : certificat SSL/TLS invalide cote serveur
#     ("unable to get local issuer certificate", chaine de certificats
#     incomplete) -- bloque toute requete HTTPS avant meme d'atteindre
#     products.json. Pas de contournement raisonnable sans desactiver la
#     verification TLS (hors de question).
#   uturitrading.com : VRAI Shopify confirme (signaux cdn.shopify.com
#     presents, page d'accueil accessible en 200), mais /products.json
#     renvoie 404 -- l'endpoint JSON public semble desactive
#     volontairement cote marchand. Alternative sitemap.xml non
#     investiguee (faible priorite, boutique non prioritaire).
BOUTIQUES_SHOPIFY_A_CONFIRMER = [
    "loot-factory.com",
    "uturitrading.com",
]

# nexthobby.fr : identifiee WooCommerce (pas Shopify) -- cf.
# boutiques_woocommerce.py / BOUTIQUES_WOOCOMMERCE_SANS_SITEMAP pour le
# diagnostic complet (rate-limit trop agressif, non integree).
