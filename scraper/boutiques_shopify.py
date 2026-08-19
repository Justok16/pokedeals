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
    # AJOUTEES le 12/08/2026 -- issues des captures d'ecran fournies par
    # Justok, verifiees une a une (Shopify confirme via /products.json +
    # ratio reel de cartes a l'unite avec numero de collection, pas juste
    # presence du mot "pokemon") avant integration :
    "playshop.fr",      # 214/214 produits tagges "pokemon-tcg", excellent signal
    "kairyu.fr",         # boutique multi-JCC, 74 cartes Pokemon a l'unite confirmees sur 190 singles
    "kwilytcg.com",       # 39 cartes Pokemon a l'unite confirmees (FR/JP/CN), + grade
    "upcfrance.shop",     # singles + scelle (Coffrets 30e Anniversaire deja en catalogue)
    "wwcg.fr",            # AJOUTEE le 12/08/2026 -- cartes Pokemon a l'unite confirmees (type "carte pokemon" explicite)
]

# AJOUTEES le 12/08/2026 : boutiques verifiees Shopify, actives, mais dont
# le catalogue est 100% SCELLE (coffrets/boosters/ETB), 0 carte a l'unite
# trouvee sur un echantillon de leur collection Pokemon dediee. Inutiles
# pour bonne_affaire_shopify.py/alerte_stock.py (scan cartes), MAIS utiles
# pour le radar de precommandes (precommandes_watchlist.py) qui cherche
# justement des produits scellés precis. Volontairement PAS dans
# BOUTIQUES_SHOPIFY ci-dessus pour ne pas polluer le scan cartes de
# candidats voues a 0 resultat a chaque cycle -- cf. scan_precommandes.py
# (_boutiques_et_replis) qui les ajoute specifiquement au radar precommandes.
BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT = [
    "lepotoryko.fr",   # multi-JCC (Pokemon/YuGiOh/Lorcana/One Piece), catalogue Pokemon = 100% scelle
    "bgeek.be",        # BELGE (.be, pas .fr) -- multi-JCC, catalogue Pokemon = 100% scelle
    "cardsarena.fr",   # AJOUTEE le 12/08/2026 -- multi-jeux (TCG/figurines/jeux societe), 48 produits Pokemon, 100% scelle
    # AJOUTEE le 18/08/2026 -- signalee par Justok : precommande Coffret ETB
    # 30e Anniversaire vue le 18/08/2026 sur /fr-fr/collections/chiques/PRECO,
    # jamais alertee car la boutique n'etait enregistree NULLE PART (ni ici,
    # ni dans la decouverte auto -- domaine .com, hors perimetre de
    # decouverte_boutiques.py qui ne couvre que les nouveaux .fr AFNIC).
    # Plateforme deduite du motif d'URL (/collections/<handle>, prefixe
    # /fr-fr/ typique de Shopify Markets) -- PAS verifiee via /products.json
    # depuis cette session (reseau sortant bloque vers ce domaine dans cet
    # environnement). Si Shopify est un mauvais diagnostic, le connecteur
    # echoue silencieusement (catalogue vide, cf. recuperer_tout_le_catalogue)
    # sans casser le scan -- a reverifier au premier vrai cycle en prod.
    "gmcardsandtoys.com",
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

# Candidats issus des captures d'ecran de Justok (12/08/2026), verifies et
# REJETES -- raison precise pour chacun, pour eviter de re-tester en vain :
#   lorenzone.fr : VRAI Shopify, mais boutique Disney LORCANA, pas Pokemon
#     (243 "singles" trouves, tous des cartes Lorcana -- faux positif du
#     nom de domaine).
#   europetcg.com : Shopify confirme, mais catalogue generaliste multi-JCC
#     tres reduit (52 produits, principalement Naruto/Lorcana/One Piece),
#     0 carte Pokemon avec numero de collection detectee.
#   poketropik.fr, pokemon-laboutique.fr : certificat SSL/TLS invalide
#     cote serveur (meme categorie que loot-factory.com ci-dessus, verifie
#     via `requests` -- pas juste curl) -- pas de contournement raisonnable
#     sans desactiver la verification TLS (hors de question).
#   ton-pokemon.fr : ce n'est PAS une boutique, c'est un blog WordPress
#     ("Le blog de ton-pokemon.fr"), aucun signal WooCommerce/e-commerce.
#   cartepokemon.shop, redom.store : domaine introuvable, la resolution
#     DNS echoue completement -- a reverifier avec Justok si coquille dans
#     la capture d'ecran d'origine.
#   icekeeper.fr : ne vend AUCUNE carte -- boutique specialisee dans les
#     boitiers de protection acrylique pour displays/ETB uniquement.
#   pokemagique.fr : VRAI WooCommerce (pas Shopify), 100% scelle (peluches
#     + boosters/coffrets/accessoires, 0 carte a l'unite sur 51 produits)
#     -- cf. boutiques_woocommerce.BOUTIQUES_WOOCOMMERCE_PRECOMMANDE_SEULEMENT.

# Suite du 12/08/2026 : liens exacts fournis par Justok pour les candidats
# ci-dessus initialement non resolus.
#   "Wonderful World Cards and Games" = wwcg.fr -> AJOUTEE a BOUTIQUES_SHOPIFY
#     (voir plus haut), cartes Pokemon a l'unite confirmees.
#   "Card Arena Shop" = cardsarena.fr (PAS cardarenausa.com, boutique
#     francaise distincte) -> AJOUTEE a BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT
#     (voir plus haut), 100% scelle.
#   "PokeVault" = pokeshop.cards -> VRAI WooCommerce (pas Shopify), 100%
#     scelle -- cf. boutiques_woocommerce.BOUTIQUES_WOOCOMMERCE_PRECOMMANDE_SEULEMENT.
#   "CMay Collections" = cmay-collections.com -> plateforme confirmee
#     Shopify, mais vitrine "headless" (frontend Next.js personnalise,
#     pas le theme Shopify standard) : n'expose PAS l'endpoint public
#     /products.json que connecteur_shopify.py sait lire (verifie :
#     404 sur products.json, page renvoie du HTML genere par Next.js/
#     "__next_error__", pas du Liquid Shopify classique). Integration
#     necessiterait un connecteur different (API GraphQL Storefront avec
#     token public) -- NON FAIT, hors perimetre d'un ajout de liste simple.
#     A envisager comme un vrai chantier a part si Justok le souhaite.
#   "Osakard" = osakard.com -> Shopify confirme, mais boutique en pleine
#     refonte (protegee par mot de passe), retour annonce par Justok pour
#     septembre 2026 -- A RETESTER a partir de cette date, pas avant.
