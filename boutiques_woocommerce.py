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

# Sans sitemap exploitable, repli "recherche HTML" teste le 10/08/2026 --
# NON integrees faute de valeur reelle (pas un probleme technique) :
BOUTIQUES_WOOCOMMERCE_SANS_SITEMAP = [
    # kiokutcg.fr : aucun sitemap declare (robots.txt vide de toute ligne
    # "Sitemap:", aucun chemin standard ne repond). Repli recherche HTML
    # (ConnecteurWooCommerce.rechercher_via_recherche_html) fonctionnel,
    # mais 0 resultat sur la watchlist complete (194 criteres) -- boutique
    # de PRODUITS SCELLES (coffrets, displays, tripacks, mini-tins),
    # aucune carte a l'unite trouvee lors de plusieurs recherches
    # (Pikachu/Dracaufeu ex/Evoli), a confirmer si son catalogue evolue.
    "kiokutcg.fr",
    # nexthobby.fr : meme constat que kiokutcg.fr (pas de sitemap, repli
    # recherche HTML fonctionnel quand accessible -- confirme 27 candidats
    # reels pour "Dracaufeu", essentiellement des ACCESSOIRES/sleeves, pas
    # de carte a l'unite vue). Rate-limit (429) tres agressif : persiste
    # meme apres 5 minutes sans requete (au-dela du simple throttle par
    # minute, pas de header Retry-After fourni) -- incompatible avec un
    # cycle de scan automatique (~60-90 requetes necessaires sur la
    # watchlist complete). A reevaluer seulement si le site assouplit sa
    # politique de rate-limit.
    "nexthobby.fr",
]

# RETIREE le 10/08/2026 : mymesis.fr a un robots.txt qui declare le sitemap
# d'un domaine TIERS generique/demo ("https://enhancedwordpress.fr/sitemap_index.xml")
# vendant des articles sans rapport (sacs, casquettes, parapluies) -- pas
# une panne technique mais une configuration jamais finalisee cote site.
# A reintegrer seulement si son propre robots.txt est corrige un jour --
# retester avec :
#   python -c "from connecteur_woocommerce import ConnecteurWooCommerce as C; print(C('mymesis.fr')._decouvrir_sitemaps_racine())"
#
# Repli "recherche HTML" NON PLUS VIABLE (teste 10/08/2026) : son moteur de
# recherche est un widget Elementor "Jet Search" pilote par AJAX cote client
# -- une requete GET statique sur "?s=..." renvoie une page quasi identique
# quelle que soit la requete (verifie : "Dracaufeu" et une requete bidon
# donnent une longueur de reponse a moins de 600 octets d'ecart, aucun lien
# produit pertinent). Recuperer les vrais resultats necessiterait de
# retro-ingenierer l'appel AJAX de ce widget -- non fait (boutique deja
# jugee faible priorite : accessoires/sleeves, peu de cartes a l'unite).
BOUTIQUES_WOOCOMMERCE_SITEMAP_INCORRECT = [
    "mymesis.fr",
]
