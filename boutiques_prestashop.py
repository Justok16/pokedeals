# Boutiques PrestaShop confirmees couvertes par la strategie SITEMAP
# (cf. connecteur_prestashop_sitemap.py). Inspection manuelle aout 2026 sur
# les 20 boutiques PrestaShop identifiees dans l'audit technique
# (audit_resultats_0_15.md / audit_resultats_15_122.md) : 16/20 exposent un
# sitemap XML exploitable (natif /sitemap.xml, declare dans robots.txt, ou
# via le module tiers /1_index_sitemap.xml). 15/16 reellement actives ici
# (bcd-jeux.fr retiree, voir plus bas).

BOUTIQUES_PRESTASHOP_SITEMAP = [
    "blazingtail.fr",
    "nin-nin-game.com",
    "nordikards.com",
    "ludocortex.fr",
    "ludifolie.com",
    "lerepairedudragon.fr",
    "fungamesnet.fr",
    "ludum.fr",
    "lesgentlemendujeu.com",
    "setdebase.com",
    "ludivers.net",
    "skydreamer.fr",
    "figurines-goodies.com",
    "nippontcg.fr",
    "kyseii.fr",
]

# Sans sitemap exploitable, couvertes via le repli "recherche HTML"
# (ConnecteurPrestaShopSitemap.rechercher_via_recherche_html, cf.
# scan_boutique_prestashop.py) -- ajoutees le 10/08/2026 apres correction de
# 2 bugs reels qui les rendaient inexploitables a tort :
#   1. Header partage "Accept: application/json" (herite du connecteur
#      Shopify) renvoyait un corps de reponse VIDE sur les pages produit de
#      certains sites -- confondu avec un vrai blocage anti-bot (403) sur
#      investcollect.com, qui n'en etait pas un. Fix : HEADERS_HTML dedie
#      aux pages HTML (cf. connecteur_shopify.py), utilise par les 2
#      connecteurs sans sitemap.
#   2. Extraction du TITRE microdata prenait la 1ere occurrence
#      itemprop="name" du document (le nom de la MARQUE, "The Pokemon
#      Company", dans un <meta> vide) au lieu de la 1ere occurrence NON
#      VIDE (le vrai nom produit, dans le <h1>).
# Teste sur la watchlist complete (194 criteres) apres fix :
#   investcollect.com : 55 resultats a confiance forte, 3 vraies bonnes
#     affaires detectees (garde-fous prix/decote/devise verifies, ex:
#     Mega-Dracolosse ex 290/217 a 400e vs cote 583e, -31.4%).
#   lepantheon-tcg.com : 2 resultats a confiance forte (1 produit unique,
#     matche via nom+alias), 0 deal ce cycle -- integree quand meme, meme
#     principe que les boutiques actives qui ont 0 match certains cycles.
BOUTIQUES_PRESTASHOP_REPLI_HTML = [
    "investcollect.com",
    "lepantheon-tcg.com",
]

# Techniquement accessibles et corrigees (memes 2 bugs que ci-dessus), mais
# NON integrees faute de valeur reelle -- verifie sur la watchlist complete
# (194 criteres) le 10/08/2026 :
#   gamespirit.fr : boutique retro-gaming/goodies generaliste (jeux video,
#     figurines, maquettes), aucune categorie "cartes a l'unite", 0 carte
#     TCG trouvee (uniquement des accessoires : boites de protection,
#     portfolios) -- pas un probleme technique, un vrai desalignement de
#     catalogue avec la watchlist.
#   pokemoncarte.com : recherche fonctionnelle (bug de parametre corrige,
#     voir _decouvrir_candidats_recherche dans connecteur_prestashop_sitemap.py),
#     mais 22 resultats tous a confiance FAIBLE (matching nom seul, jamais
#     nom+numero) -- 0 alerte automatique possible en l'etat. A reevaluer si
#     son catalogue s'etoffe ou si le matching nom+numero est ameliore.
BOUTIQUES_PRESTASHOP_SANS_SITEMAP = [
    "gamespirit.fr",
    "pokemoncarte.com",
]

# RETIREE le 10/08/2026 : bcd-jeux.fr a un sitemap CASSE cote site. Son
# index (/1_index_sitemap.xml) declare 3 sous-fichiers
# (1_fr_0/1/2_sitemap.xml) qui renvoient TOUS 404, avec ou sans "www" --
# verifie manuellement, ce n'est pas un probleme de notre connecteur.
# Resultat observe en prod : "0 URLs sitemap" a chaque scan (silencieux,
# pas une erreur au sens Python, juste une liste vide).
# A REINTEGRER dans BOUTIQUES_PRESTASHOP_SITEMAP si son sitemap est un jour
# repare -- retester avec :
#   python -c "from connecteur_prestashop_sitemap import ConnecteurPrestaShopSitemap as C; print(len(C('bcd-jeux.fr').recuperer_toutes_les_urls_produits()))"
BOUTIQUES_PRESTASHOP_SITEMAP_CASSE = [
    "bcd-jeux.fr",
]
