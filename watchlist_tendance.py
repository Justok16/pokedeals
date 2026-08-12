"""
Watchlist DEDIEE au suivi de tendance de prix long terme (historique_prix.py),
separee de la watchlist principale (config.yaml, 121+ cartes suivies pour les
alertes bonne-affaire/retour-stock/precommande).

Volontairement une liste EXPLICITE et REDUITE, pas la watchlist complete :
cette fonctionnalite vise a repondre a une question precise ("est-ce un bon
moment pour acheter CETTE carte precise ?"), pas a tout suivre en tendance.
Ajouter une carte ici est un choix delibere de Justok, pas automatique.

Chaque entree correspond a une carte deja presente dans config.yaml (meme
nom_config/langue, pour pouvoir recouper avec data/cotes.json quand une
cote y existe) + les parametres de recherche PokemonPriceTracker (nom
anglais du Pokemon, set japonais, numero) -- cf. historique_prix.py.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CarteTendance:
    nom_config: str       # identique a config.yaml, pour recouper avec cotes.json
    langue: str            # "jp" / "kr" / "cn"
    nom_affichage: str      # nom FR usuel, pour les messages Telegram
    nom_anglais: str        # nom du Pokemon en anglais, pour la recherche PokemonPriceTracker
    set_jp: str              # nom du set japonais (tel qu'utilise par PokemonPriceTracker)
    numero: str               # numero de collection SANS denominateur (ex: "111", "170", "199")


# Ajoutees le 12/08/2026 a la demande de Justok -- 3 cartes JP suivies en
# priorite (langues ciblees : japonais/coreen/chinois, memes numeros de
# collection partages entre ces 3 langues pour la numerotation JP/KR).
CARTES_TENDANCE = [
    CarteTendance(
        nom_config="Oricorio ex 111 m2",
        langue="jp",
        nom_affichage="Plumeline ex (Oricorio ex)",
        nom_anglais="Oricorio ex",
        set_jp="MEGA Dream ex",
        numero="111",
    ),
    CarteTendance(
        nom_config="Squirtle 170/165 sv2a",
        langue="jp",
        nom_affichage="Carapuce (Squirtle)",
        nom_anglais="Squirtle",
        set_jp="Pokemon Card 151",
        numero="170",
    ),
    CarteTendance(
        nom_config="Psyduck 199 m2a",
        langue="jp",
        nom_affichage="Psykokwak (Psyduck)",
        nom_anglais="Psyduck",
        set_jp="MEGA Dream ex",
        numero="199",
    ),
]
