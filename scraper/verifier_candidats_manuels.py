"""
Verification technique d'une liste de domaines candidats fournie a la main
(annuaires/forums/communautes TCG trouves par recherche web) -- complement
au radar automatique decouverte_boutiques.py, qui ne couvre QUE les
domaines .fr fraichement enregistres (source AFNIC). Une boutique existante
depuis plusieurs annees, ou en .com/.shop, n'apparait JAMAIS dans le flux
AFNIC -- ce script permet de verifier ce genre de candidat des qu'on en
trouve, avec les MEMES criteres objectifs que la verification manuelle
habituelle (motif de numero de collection NNN/MMM + mention Pokemon
explicite, ou volume de produits scelles Pokemon).

Teste les 3 plateformes supportees par le projet, dans l'ordre :
Shopify (/products.json) -> WooCommerce (product-sitemap.xml) -> PrestaShop
(sitemap XML, via ConnecteurPrestaShopSitemap).

NE MODIFIE JAMAIS aucune liste de boutiques (ni les listes annotees a la
main, ni boutiques_decouvertes.py) -- rapporte seulement un verdict par
domaine. Un ajout reste une decision humaine (Justok), comme pour tout
candidat "insuffisant"/ambigu du radar automatique -- meme philosophie de
prudence (mieux vaut manquer une boutique limite qu'ajouter un faux
positif dans un systeme qui declenche de vraies alertes Telegram).

Usage :
  python verifier_candidats_manuels.py domaine1.fr domaine2.com ...
"""
import sys

from decouverte_boutiques import SEUIL_MIN_PRODUITS_SCELLE_POKEMON, verifier_candidat


def verifier_prestashop(domaine: str) -> dict:
    """Repli PrestaShop pour un domaine que verifier_candidat() a classe
    "non_boutique" (ni Shopify ni WooCommerce). Meme heuristique grossiere
    que le repli WooCommerce de verifier_candidat() : mots-cles dans les
    slugs d'URL du sitemap, pas de titre exploitable sans visiter chaque
    page produit individuellement (trop couteux pour une verification
    rapide de plusieurs candidats)."""
    from connecteur_prestashop_sitemap import ConnecteurPrestaShopSitemap

    try:
        connecteur = ConnecteurPrestaShopSitemap(domaine)
        sitemaps = connecteur._decouvrir_sitemaps_racine()
        if not sitemaps:
            return {"domaine": domaine, "plateforme": None, "verdict": "non_boutique"}
        urls = []
        for sm in sitemaps:
            urls.extend(connecteur._lister_urls_recursif(sm))
        if not urls:
            return {"domaine": domaine, "plateforme": None, "verdict": "non_boutique"}
        slugs_pokemon = [
            u for u in urls if "pokemon" in u.lower() or "pok%c3%a9mon" in u.lower()
        ]
        verdict = "scelle" if len(slugs_pokemon) >= SEUIL_MIN_PRODUITS_SCELLE_POKEMON else "insuffisant"
        return {
            "domaine": domaine, "plateforme": "prestashop", "verdict": verdict,
            "nb_produits": len(urls), "nb_slugs_pokemon": len(slugs_pokemon),
        }
    except Exception as e:  # noqa: BLE001 -- un candidat en echec ne doit jamais arreter le batch
        return {"domaine": domaine, "plateforme": None, "verdict": "erreur", "raison": str(e)}


def verifier(domaine: str) -> dict:
    rapport = verifier_candidat(domaine)
    if rapport["verdict"] == "non_boutique":
        rapport = verifier_prestashop(domaine)
    return rapport


if __name__ == "__main__":
    domaines = sys.argv[1:]
    if not domaines:
        print("Usage : python verifier_candidats_manuels.py domaine1.fr domaine2.com ...")
        sys.exit(1)

    for d in domaines:
        r = verifier(d)
        print(f"{d} -> {r}")
