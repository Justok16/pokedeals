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


# ------------- 04/10/2026 : suivi de disponibilite des produits des 30 ans -------------

from datetime import date

from precommandes_watchlist import evaluer_correspondance, produits_actifs


def test_etb_30e_suivi_restock_actif_apres_la_date_de_sortie():
    # L'entree d'origine (sortie 16/09) a expire ; l'entree "suivi restock"
    # reste active jusqu'a fin 2026.
    etb = _produit("suivi restock")
    assert etb in produits_actifs(date(2026, 10, 4))
    assert etb not in produits_actifs(date(2027, 1, 1))
    anciens = [p for p in PRODUITS_SURVEILLES
               if "30e Anniversaire" in p.nom and "Coffret Dresseur" in p.nom and p is not etb]
    assert anciens and all(p not in produits_actifs(date(2026, 10, 4)) for p in anciens)


def test_produit_sans_date_ni_fenetre_reste_actif_indefiniment():
    from precommandes_watchlist import ProduitSurveille
    p = ProduitSurveille("x", frozenset({"a"}), frozenset({"b"}), date_sortie=None)
    from unittest.mock import patch
    with patch("precommandes_watchlist.PRODUITS_SURVEILLES", [p]):
        assert produits_actifs(date(2030, 1, 1)) == [p]


def test_tous_les_produits_des_30_ans_sont_en_suivi_de_disponibilite():
    for fragment in ("suivi restock", "Booster Bundle", "Mini Tin", "Nymphali ex (Sylveon ex Tin)",
                     "Espeon (Mentali)", "Umbreon (Noctali)"):
        assert _produit(fragment).alerte_disponibilite is True


def test_bundle_et_mini_tin_ne_valident_pas_la_date():
    # Sortie reportee : une page affichant une date quelconque ne doit pas
    # etre rejetee pour incompatibilite de date.
    bundle = _produit("Booster Bundle")
    conf, _ = evaluer_correspondance("Booster Bundle 30th Celebration", "Sortie le 20/11/2026", bundle)
    assert conf == "moyenne"


def test_titres_bundle_et_mini_tin():
    bundle = _produit("Booster Bundle")
    mini = _produit("Mini Tin")
    assert titre_correspond_produit("Pokémon - Booster Bundle 30th Celebration - FR", bundle) is True
    assert titre_correspond_produit("Bundle 6 boosters 30e Anniversaire", bundle) is True
    assert titre_correspond_produit("Mini Tin 30e Anniversaire Pokémon (Mentali)", mini) is True
    assert titre_correspond_produit("Mini Tin 30e Anniversaire Pokémon", bundle) is False
    assert titre_correspond_produit("Booster Bundle Règne Delta ME06", bundle) is False


def test_titre_etb_30e_ne_matche_pas_un_etb_dun_autre_set():
    etb = _produit("suivi restock")
    assert titre_correspond_produit("Coffret Dresseur d'Élite 30e Anniversaire FR", etb) is True
    assert titre_correspond_produit("ETB ME06 Règne Delta, Pokémon fête ses 30 ans", etb) is False


def test_tin_nymphali_matche_le_coffret_mais_pas_la_carte_a_lunite():
    tin = _produit("Nymphali ex (Sylveon ex Tin)")
    assert titre_correspond_produit("Pokébox 30e Anniversaire Nymphali-ex", tin) is True
    assert titre_correspond_produit("30th Celebration ex Tin [Sylveon ex]", tin) is True
    assert titre_correspond_produit("Tin Nymphali ex - 30 ans Pokémon", tin) is True
    # carte isolee de la meme extension, avec "destinees" dans la description
    assert titre_correspond_produit(
        "Nymphali ex 018/030 - 30th Celebration", tin) is False
    assert titre_correspond_produit(
        "Nymphali ex - 30e Anniversaire - Rivalités Destinées carte rare", tin) is False
    # pokebox d'un autre personnage de la meme extension
    assert titre_correspond_produit("Pokébox 30e Anniversaire Amphinobi-ex", tin) is False
