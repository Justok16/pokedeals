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

# Sans sitemap exploitable (a traiter plus tard via un repli "recherche
# HTML" si on decide d'investir dedans -- cf. discussion) :
#   gamespirit.fr, pokemoncarte.com, lepantheon-tcg.com, investcollect.com
# (investcollect.com bloque aussi en 403, anti-bot probable)
BOUTIQUES_PRESTASHOP_SANS_SITEMAP = [
    "gamespirit.fr",
    "pokemoncarte.com",
    "lepantheon-tcg.com",
    "investcollect.com",
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
