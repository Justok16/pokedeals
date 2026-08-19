"""
Watchlist DEDIEE au radar de prix bas quotidien (radar_prix_bas.py),
INDEPENDANTE de watchlist_tendance.py (tendance de prix long terme, JP
seulement) et du reste de config.yaml (121+ cartes, alertes bonne-affaire/
retour-stock/precommande "des qu'un scan les croise").

4 cartes choisies par Justok (ajoutees le 13/08/2026), suivies dans les 4
langues qui l'interessent (FR/JP/KR/CN) -- liste EXPLICITE et REDUITE, ajout
manuel delibere, meme esprit que watchlist_tendance.py.

Chaque "famille" regroupe les variantes linguistiques d'une meme carte
physique. Chaque variante pointe vers un `nom_config` de config.yaml (les 16
entrees FR/JP/KR/CN y sont toutes presentes, y compris le chinois -- ajoute
dans la meme session avec cote manuelle approximee) : reutiliser
`charger_watchlist_config()` (watchlist_shopify.py) donne gratuitement le
nom_recherche/numero/qualificatif deja extraits, sans dupliquer cette
logique ici.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VariantePrixBas:
    langue: str        # fr / jp / kr / cn
    nom_config: str    # cle EXACTE dans config.yaml (watchlist[].nom)


@dataclass(frozen=True)
class FamillePrixBas:
    nom_affichage: str              # nom FR usuel, pour les messages Telegram
    variantes: list[VariantePrixBas]


FAMILLES_PRIX_BAS = [
    FamillePrixBas(
        nom_affichage="Plumeline ex (Oricorio ex)",
        variantes=[
            VariantePrixBas("fr", "Plumeline ex 024"),
            VariantePrixBas("jp", "Oricorio ex 111 m2"),
            VariantePrixBas("kr", "Oricorio ex 111 m2"),
            VariantePrixBas("cn", "Oricorio ex 111 m2"),
        ],
    ),
    FamillePrixBas(
        nom_affichage="Carapuce (Squirtle)",
        variantes=[
            VariantePrixBas("fr", "Carapuce 170/165"),
            VariantePrixBas("jp", "Squirtle 170/165 sv2a"),
            VariantePrixBas("kr", "Squirtle 170/165 sv2a"),
            VariantePrixBas("cn", "Squirtle 170/165 sv2a"),
        ],
    ),
    FamillePrixBas(
        nom_affichage="Psykokwak (Psyduck)",
        variantes=[
            VariantePrixBas("fr", "Psykokwak 226"),
            VariantePrixBas("jp", "Psyduck 199 m2a"),
            VariantePrixBas("kr", "Psyduck 199 m2a"),
            VariantePrixBas("cn", "Psyduck 199 m2a"),
        ],
    ),
    FamillePrixBas(
        nom_affichage="Tiplouf (Piplup)",
        variantes=[
            VariantePrixBas("fr", "Tiplouf 098/094"),
            VariantePrixBas("jp", "Piplup 085 m2"),
            VariantePrixBas("kr", "Piplup 085 m2"),
            VariantePrixBas("cn", "Piplup 085 m2"),
        ],
    ),
]
