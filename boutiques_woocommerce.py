# Boutiques WooCommerce confirmees couvertes par la strategie SITEMAP
# (cf. connecteur_woocommerce.py). Inspection aout 2026 sur les 28 boutiques
# WooCommerce identifiees dans l'audit technique (audit_resultats_0_15.md /
# audit_resultats_15_122.md) : 26/28 exposent un sitemap XML exploitable.

BOUTIQUES_WOOCOMMERCE_SITEMAP = [
    "guizettefamily.com",
    "lecoindesbarons.com",
    "hobby-one.net",
    "lepion.com",
    "jmcards.fr",
    "topdecktcg.fr",       # catalogue tres petit/fige depuis 2024, mais sitemap valide
    "mgs-shop.fr",
    "pokestock.fr",
    "cardshunter.fr",
    "placeofgeek.fr",
    "pokegourou.com",
    "vinticards.fr",
    "magicalstore.fr",
    "lecrocodeal.com",
    "comptoirdesecoliers.com",
    "pokelite.fr",
    "fuji-store.fr",
    "pokeloutre.fr",
    "hamacards.com",
    "pokemoms.fr",
    "importpokecoree.com",
    "pakushop.com",
    "pokuji.fr",
    "ecardstore.fr",
    "k-tcg.com",
    "figuyatta.com",
]

# Scinde en 2 lots pour le workflow scan_woocommerce.yml (19 min mesurees
# sur les 26 d'un coup -- marge insuffisante face au surcout habituel de
# GitHub Actions). Repartition EQUILIBREE PAR VOLUME D'URLs sitemap (pas par
# nombre de boutiques) via un bin-packing glouton sur les tailles mesurees
# le 10/08/2026, pour que les 2 lots prennent un temps comparable
# (~115 200 URLs chacun sur ~230 400 au total) :
LOT_A = [
    "cardshunter.fr", "hamacards.com", "comptoirdesecoliers.com",
    "lecoindesbarons.com", "figuyatta.com", "magicalstore.fr",
    "pokestock.fr", "jmcards.fr", "ecardstore.fr", "pokelite.fr",
    "pokegourou.com", "pokeloutre.fr",
]
LOT_B = [
    "k-tcg.com", "placeofgeek.fr", "lepion.com", "vinticards.fr",
    "lecrocodeal.com", "mgs-shop.fr", "hobby-one.net", "fuji-store.fr",
    "pakushop.com", "guizettefamily.com", "pokuji.fr",
    "importpokecoree.com", "pokemoms.fr", "topdecktcg.fr",
]

# Sans sitemap exploitable :
BOUTIQUES_WOOCOMMERCE_SANS_SITEMAP = [
    "kiokutcg.fr",  # aucun sitemap declare (robots.txt vide de toute ligne "Sitemap:", aucun chemin standard ne repond)
]

# RETIREE le 10/08/2026 : mymesis.fr a un robots.txt qui declare le sitemap
# d'un domaine TIERS generique/demo ("https://enhancedwordpress.fr/sitemap_index.xml")
# vendant des articles sans rapport (sacs, casquettes, parapluies) -- pas
# une panne technique mais une configuration jamais finalisee cote site.
# A reintegrer seulement si son propre robots.txt est corrige un jour --
# retester avec :
#   python -c "from connecteur_woocommerce import ConnecteurWooCommerce as C; print(C('mymesis.fr')._decouvrir_sitemaps_racine())"
BOUTIQUES_WOOCOMMERCE_SITEMAP_INCORRECT = [
    "mymesis.fr",
]
