"""Pont entre la watchlist PokéDeals (config.yaml) et un futur système de
score de rareté/potentiel (recherche de cartes rares en nombre, dont le
prix n'a pas encore décollé -- objectif de Justok).

Ne fait AUCUN calcul de score : se contente de rassembler, pour chaque
carte suivie, les données déjà calculées ailleurs dans PokéDeals
(watchlist_shopify.py, moteur_cote.py) sous une forme facile à consommer.
Tout champ pour lequel PokéDeals n'a PAS déjà de source est mis à None
plutôt que d'inventer un calcul -- à compléter le jour où une vraie source
existera (ex: rareté/numéro de set officiel, compteur d'annonces
Cardtrader/eBay persistant).

Format d'une entrée retournée par charger_depuis_pokedeals() :
{
    "nom": str,                     # nom tel qu'écrit dans config.yaml
    "numero": str | None,           # ex: "199/165", ou None si absent
    "langue": str,                  # "fr" / "jp" / "kr"
    "cote_bas_marche": float | None,       # dernière cote lissée connue (data/cotes.json)
    "nb_annonces_cardtrader": None,        # pas de source : cardtrader_prix() ne renvoie qu'un prix, jamais un nombre d'annonces
    "nb_annonces_ebay": None,              # pas de source persistée : le nombre d'annonces utilisées par obtenir_cote() n'est calculé qu'en direct pendant un scan, jamais enregistré dans data/cotes.json
    "set": None,                            # pas de source : la watchlist ne stocke pas le set/l'édition séparément du nom
    "rarete": None,                         # pas de source : aucune notion de rareté n'existe dans PokéDeals aujourd'hui
}
"""
from __future__ import annotations

import moteur_cote
from watchlist_shopify import charger_watchlist_config


def charger_depuis_pokedeals() -> list[dict]:
    """Rassemble les cartes de la watchlist PokéDeals (config.yaml) avec
    leur dernière cote bas-marché connue (data/cotes.json, via
    moteur_cote.cote_lissee -- médiane des cotes des 7 derniers jours)."""
    cartes = []
    for carte in charger_watchlist_config():
        cartes.append({
            "nom": carte.nom_config,
            "numero": carte.numero,
            "langue": carte.langue,
            "cote_bas_marche": moteur_cote.cote_lissee(carte.nom_config, carte.langue),
            "nb_annonces_cardtrader": None,
            "nb_annonces_ebay": None,
            "set": None,
            "rarete": None,
        })
    return cartes
