# Boutiques PrestaShop confirmees couvertes par la strategie SITEMAP
# (cf. connecteur_prestashop_sitemap.py). Inspection manuelle aout 2026 sur
# les 20 boutiques PrestaShop identifiees dans l'audit technique initial :
# 16/20 exposent un sitemap XML exploitable (natif /sitemap.xml, declare
# dans robots.txt, ou via le module tiers /1_index_sitemap.xml). 15/16
# reellement actives ici (bcd-jeux.fr retiree, voir plus bas).

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
    # AJOUTEE le 24/08/2026 -- trouvee par recherche web (limite assumee du
    # radar decouverte_boutiques.py : ne couvre que les .fr fraichement
    # crees via AFNIC, jamais une boutique existante ni un .com), verifiee
    # via verifier_candidats_manuels.py : sitemap PrestaShop valide, 313
    # slugs Pokemon sur 4195 produits au total.
    "plazatcg.com",
    # AJOUTEES le 25/08/2026 -- issues de l'annuaire V2 (candidats fournis
    # par Justok, extraits de MapTCG/PkmCards : ~123 boutiques physiques
    # nommees/adressees, cf. data/annuaire_boutiques_candidates.csv),
    # verifiees une a une via verifier_candidats_manuels.py (sitemap
    # PrestaShop valide + slugs Pokemon reels dans l'URL -- signal plus
    # grossier que Shopify, pas de distinction singles/scelle possible sans
    # visiter chaque page produit, meme limite que shop-tcg.fr/golden-poke.fr
    # cote WooCommerce) :
    "atmos-arena.com",     # 1478 produits/610 slugs pokemon -- tres bon signal
    "curiouspop.com",      # 36 produits/13 slugs pokemon -- petit catalogue mais bon ratio
    "majestikgames.com",   # 18442 produits/28 slugs pokemon
    "starplayer.fr",       # 16624 produits/132 slugs pokemon
    "uchroniesgames.fr",   # 237 produits/6 slugs pokemon -- signal faible mais reel
    "thevaults.fr",        # 1992 produits/224 slugs pokemon
    "konobacards.fr",      # 1043 produits/228 slugs pokemon
    "fantasysphere.net",   # 84014 produits/10214 slugs pokemon -- tres gros volume
    "gamecash.fr",         # 97448 produits/731 slugs pokemon -- chaine nationale, tres gros volume
    "bulleenstock.com",    # 197636 produits/453 slugs pokemon -- record absolu de volume
    "goupiya.com",         # 10127 produits/182 slugs pokemon
    "tzp.fr",               # 724 produits/18 slugs pokemon
    "octopusgame.fr",      # 1382 produits/307 slugs pokemon
    "playmogames.com",     # 43128 produits/845 slugs pokemon -- tres gros volume
    "ludiworld.com",       # 39593 produits/728 slugs pokemon -- tres gros volume
    "crique-aux-jeux.fr",  # 19276 produits/175 slugs pokemon
    "backingame.fr",       # 1886 produits/36 slugs pokemon
    "kraknplay.com",       # 188 produits/9 slugs pokemon
    "jeux-comte.fr",       # 1306 produits/48 slugs pokemon
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
# lepantheon-tcg.com a ete retiree le 16/08/2026, voir
# BOUTIQUES_PRESTASHOP_REPLI_HTML_TROP_LENTE plus bas.
BOUTIQUES_PRESTASHOP_REPLI_HTML = [
    "investcollect.com",
]

# RETIREE le 16/08/2026 : lepantheon-tcg.com a fait echouer/timeout
# scan_prestashop.yml a repetition dans la soiree du 15/08/2026 (job entier
# a 30 min de budget). Diagnostic confirme grace au fix PYTHONUNBUFFERED
# (cf. SESSION_NOTES.md) : sur un run reel, les 16 AUTRES boutiques (dont
# investcollect.com, meme methode "repli HTML" sans sitemap) ont pris entre
# quelques secondes et ~2 min chacune -- lepantheon-tcg.com, SEULE, a pris
# 14min34s a elle seule (874s sur un total de 1525.9s pour les 17
# boutiques), et a de nouveau bloque l'etape suivante (radar precommandes)
# jusqu'au timeout du job. Le meme scan complet termine en 2min33s dans un
# environnement de dev different (IP differente) : tout pointe vers un
# rate-limit/anti-bot cote lepantheon-tcg.com qui cible specifiquement les
# plages d'IP des runners GitHub Actions (Azure), pas un probleme de notre
# code (`rechercher_via_recherche_html` fait le meme nombre de requetes,
# avec le meme delai de politesse, pour investcollect.com qui reste rapide).
# Valeur deja documentee comme marginale avant meme cet incident (1 seul
# produit unique jamais trouve, 0 deal). A REINTEGRER dans
# BOUTIQUES_PRESTASHOP_REPLI_HTML seulement si un futur test manuel montre
# un temps de reponse redevenu raisonnable.
BOUTIQUES_PRESTASHOP_REPLI_HTML_TROP_LENTE = [
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
