"""Tests de non-regression pour precommandes_watchlist.py.

V55 (18/08/2026, signale par Justok) : UPC Mentali (Espeon) et UPC Noctali
(Umbreon) sont deux produits DISTINCTS -- ils avaient ete modelises comme
UN SEUL ProduitSurveille avec les mots-cles type des deux personnages.
Bug reel identifie avant qu'il ne se manifeste : radar_precommandes._candidat()
utilise `produit.nom` comme cle de memoire (`domaine|nom_produit`, cf.
alerte_precommande._cle_memoire) -- deux fiches produit d'une meme
boutique (une pour chaque personnage) auraient partage la MEME cle, et la
seconde scannee aurait ecrase silencieusement la premiere en memoire,
perdant le suivi d'une des deux precommandes. Scinde en 2 entrees
distinctes -- ces tests verifient que chaque titre ne matche QUE son
propre produit, jamais l'autre, et que les deux ont des noms distincts
(donc des cles memoire distinctes)."""

from precommandes_watchlist import PRODUITS_SURVEILLES, titre_correspond_produit


def _produit(fragment_nom: str):
    candidats = [p for p in PRODUITS_SURVEILLES if fragment_nom in p.nom]
    assert len(candidats) == 1, f"attendu 1 produit contenant {fragment_nom!r}, trouve {len(candidats)}"
    return candidats[0]


def test_mentali_et_noctali_sont_deux_produits_avec_des_noms_distincts():
    mentali = _produit("Espeon (Mentali)")
    noctali = _produit("Umbreon (Noctali)")
    assert mentali.nom != noctali.nom
    assert mentali.date_sortie == noctali.date_sortie


def test_titre_upc_mentali_ne_matche_que_le_produit_mentali():
    mentali = _produit("Espeon (Mentali)")
    noctali = _produit("Umbreon (Noctali)")
    titre = "UPC Mentali (Collection Ultra-Premium) — 30ème Anniversaire - Français"
    assert titre_correspond_produit(titre, mentali) is True
    assert titre_correspond_produit(titre, noctali) is False


def test_titre_upc_noctali_ne_matche_que_le_produit_noctali():
    mentali = _produit("Espeon (Mentali)")
    noctali = _produit("Umbreon (Noctali)")
    titre = "UPC Pokémon Noctali ex 30e Anniversaire FR"
    assert titre_correspond_produit(titre, mentali) is False
    assert titre_correspond_produit(titre, noctali) is True


def test_titre_upc_espeon_ne_matche_que_le_produit_mentali():
    # "Espeon" (nom EN, parfois utilise par les boutiques a la place du
    # nom FR "Mentali") doit matcher le meme produit, pas l'autre.
    mentali = _produit("Espeon (Mentali)")
    noctali = _produit("Umbreon (Noctali)")
    titre = "Collection Ultra-Premium Espeon — 30th Celebration"
    assert titre_correspond_produit(titre, mentali) is True
    assert titre_correspond_produit(titre, noctali) is False


# ------------------- V56 : marqueur prioritaire (⭐ Noctali) -------------------

def test_noctali_est_marque_prioritaire():
    # Demande explicite de Justok (18/08/2026) : purement cosmetique, cf.
    # alerte_precommande._texte_precommande.
    noctali = _produit("Umbreon (Noctali)")
    assert noctali.prioritaire is True


def test_mentali_nest_pas_marque_prioritaire_par_defaut():
    mentali = _produit("Espeon (Mentali)")
    assert mentali.prioritaire is False
