# Boutiques TCG confirmees Shopify avec API JSON publique /products.json
# Issues de l'audit technique (aout 2026) sur les 122 boutiques de la liste de Justok.
# A utiliser avec connecteur_shopify.py -- un seul connecteur pour toutes ces boutiques.

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
    "card-binder.com",
    "japanresell.fr",
    "lectorshop.com",
    "cardotaku.com",
]

# Detectees Shopify en priorite 2 (plateforme identifiee mais API non confirmee
# lors de l'audit initial -- a re-tester avec connecteur_shopify.py directement,
# il gere le cas ou products.json ne renvoie rien)
BOUTIQUES_SHOPIFY_A_CONFIRMER = [
    "loot-factory.com",
    "uturitrading.com",
]

# nexthobby.fr : en cours de re-test suite a un rate-limit (429) lors de l'audit.
# Voir retest_nexthobby.py -- sera ajoute a la bonne liste selon le resultat.
