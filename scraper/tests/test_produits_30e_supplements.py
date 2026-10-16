"""Produits des 30 ans ajoutes le 13/10/2026 (liste de Justok) : titres
reels releves sur les boutiques le jour de l'ajout."""

import pytest

from precommandes_watchlist import PRODUITS_SURVEILLES, evaluer_correspondance

P = {p.nom: p for p in PRODUITS_SURVEILLES}
DITTO = "Collection Premium Métamorph (Ditto) 30e Anniversaire FR"
MEW = "Collection avec figurine Mew 30e Anniversaire FR"
MEWTWO = "Collection avec figurine Mewtwo 30e Anniversaire FR"
BOX = "30th Celebration FUTURISTIC BOX (JP / chinois traditionnel / KR)"
FUTUR_CN = "Coffret commémoratif « Futur » 幻彩未来 (chinois simplifié)"
RARE_SET = "30th Celebration Futuristic Rare Set (thaï / indonésien)"
DECK = "Premium Deck Set Mentali & Noctali (JP / chinois traditionnel)"
EXPO_CN = "Coffret collection & exposition Mentali-ex & Noctali-ex (chinois simplifié)"


@pytest.mark.parametrize("nom, titre", [
    (DITTO, "Coffret Collection Premium Pokémon 30e Anniversaire Métamorph 🇫🇷"),
    (MEW, "[Précommande] Coffret Collection avec Figurine Mew Pokémon 30e Anniversaire"),
    (MEWTWO, "Pokémon · 30e Anniversaire - Coffret Figurine Mewtwo - FR"),
    (BOX, "Futuristic Box 30th Celebration - Coffret Ultra Premium 30 ans Japonais"),
    (BOX, "Pokemon TCG 30th Celebration Futuristic Box (Korean Ver.)"),
    (FUTUR_CN, "Coffret pokémon Celebration Futuristic Box 30 ème Anniversaire - version chinoise simplifiée"),
    (RARE_SET, "30th Celebration Futuristic Rare Set Thai"),
    (DECK, "Pokemon [Japonais] - Premium Deck Set Mentali & Noctali - 30th Celebration"),
    (DECK, "Premium Deck Set Mentali ex & Noctali ex - Pokémon 30th Celebration Chinois Traditionnel Scellé"),
    (DECK, "Pokémon 30th Celebration Premium Deck Set Espeon & Umbreon m6a - Japonais"),
])
def test_fiches_reelles_reconnues(nom, titre):
    assert evaluer_correspondance(titre, "", P[nom])[0] is not None


@pytest.mark.parametrize("nom, titre", [
    (DITTO, "Métamorph 132/180 30e Anniversaire carte Pokémon FR"),          # carte a l'unite
    (MEW, "Coffret Collection avec Figurine Mewtwo Pokémon 30e Anniversaire"),  # "mew" dans "mewtwo"
    (MEW, "30th Celebration Figure Collection Mew (EN)"),                      # version anglaise
    (BOX, "30th Celebration Futuristic Rare Set Thai"),                        # autre coffret
    (FUTUR_CN, "Vsinger Figurine Luo Tianyi Retro Future Storm Driver"),       # "futur" dans "future"
    (DECK, "Mentali ex 043/040 - 30th Celebration Premium Deck Set — + Cadre"),  # carte encadree
    (DECK, "Premium Deck Set Mentali ex & Noctali ex 30th + Double Gradation CollectAura"),
    # 16/10/2026, nippontcg.fr : "chinois" du titre + "cadre"/"aimant" ailleurs
    # dans la page faisaient passer le Premium Deck Set pour ce coffret.
    (EXPO_CN, "Premium Deck Set Mentali ex & Noctali ex - Pokémon 30th Celebration Chinois Traditionnel Scellé"),
])
def test_faux_positifs_rejetes(nom, titre):
    assert evaluer_correspondance(titre, "30 ans chinois", P[nom])[0] is None


def test_coffret_exposition_cn_maniatcg():
    """Fiche reelle maniatcg.com (16/10/2026) : le titre ne dit pas
    "aimant/exposition", seule la page le dit (slug "coffret-collection-aimants")."""
    titre = "Pokémon 30th Celebration Coffret Collection Premium Noctali & Mentali - Chinois Simplifié"
    assert evaluer_correspondance(titre, "coffret collection aimants", P[EXPO_CN])[0] is not None
