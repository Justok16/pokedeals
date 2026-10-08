"""Noms FRANCAIS officiels des produits des 30 ans (08/10/2026, visuels envoyes
par Justok) : chaque titre doit etre reconnu par le BON produit suivi, et
seulement lui ; les lots de revendeur restent exclus."""

import pytest

import precommandes_watchlist as w

PRODUITS = {p.nom: p for p in w.PRODUITS_SURVEILLES if p.alerte_disponibilite}


def _produit(fragment):
    return next(p for nom, p in PRODUITS.items() if fragment in nom)


def _reconnu_par(titre, description="Précommande, version française"):
    return [nom for nom, p in PRODUITS.items() if w.evaluer_correspondance(titre, description, p)[0]]


@pytest.mark.parametrize("titre,fragment", [
    ("Pokémon 30e Anniversaire - Lot de boosters", "Booster Bundle"),
    ("Lot de boosters Pokémon 30ème Anniversaire FR", "Booster Bundle"),
    ("Pokémon - Bundle / Lot de 6 boosters ME05.5 : 30e Anniversaire", "Booster Bundle"),  # dracaugames
    ("ME5.5 - 30 ans - Bundle - FRANCAIS (02/10)", "Booster Bundle"),  # gmcardsandtoys (code d'extension)
    ("Pokémon ME05.5 : coffret Dresseur d'Elite - français", "Coffret Dresseur d'Élite — 30e Anniversaire FR (suivi"),
    ("Coffret Dresseur d'Élite 30e Anniversaire", "Coffret Dresseur d'Élite — 30e Anniversaire FR (suivi"),
    ("Pokémon 30e Anniversaire : Mini Tin", "Mini Tin"),
    ("Tin Pokémon Nymphali-ex 30e Anniversaire", "Nymphali"),
    ("Boîte métal Nymphali-ex 30e Anniversaire", "Nymphali"),
    ("Pokébox Nymphali ex 30 ans FR", "Nymphali"),
    ("Collection Ultra-Premium 30e Anniversaire Noctali-ex", "Noctali"),
    ("Coffret Ultra Premium Mentali ex 30e Anniversaire", "Mentali"),
])
def test_nom_francais_reconnu_par_le_seul_bon_produit(titre, fragment):
    attendu = _produit(fragment).nom
    assert _reconnu_par(titre) == [attendu]


@pytest.mark.parametrize("titre", [
    "Lot de 3 lots de boosters 30e Anniversaire",   # vrai lot de revendeur
    "Lot 2 Bundle 30e anniversaire",
    "Lot/bundle 30 ans - 30e anniversaire - Pokémon français officiel",  # lot revendeur (kwilytcg)
    "Tin Pokémon Martin 30e anniversaire",          # "tin" jamais seul
    "Carte ultra premium Noctali VMAX EVS 215/203",  # faux positif historique
    "30th Celebration Elite Trainer Box - EN",       # version anglaise
])
def test_titres_qui_ne_doivent_rien_declencher(titre):
    assert _reconnu_par(titre) == []


def test_mini_tin_jamais_pris_pour_la_pokebox_nymphali():
    assert _reconnu_par("Pokémon 30e Anniversaire : Mini Tin (Nymphali)") == [_produit("Mini Tin").nom]


def test_pokebox_amphinobi_seule_rejetee_mais_modele_au_choix_garde():
    """08/10/2026 : la Pokebox soeur Amphinobi-ex 30e (plazatcg.com,
    pokemagic.fr) passait pour la Nymphali via "nymphali" ailleurs sur la page."""
    p = next(p for p in w.PRODUITS_SURVEILLES if p.nom.startswith("Pokébox"))
    texte = "Version française. Voir aussi la Pokébox Nymphali-ex."
    assert w.evaluer_correspondance("Pokémon – Pokébox – 30e Anniversaire - Amphinobi-ex – Français", texte, p)[0] is None
    assert w.evaluer_correspondance("Pokébox Pokémon Nymphali Ex et Amphinobi Ex – 30e Anniversaire", texte, p)[0]
    assert w.evaluer_correspondance("Pokémon – Pokébox – 30e Anniversaire - Nymphali-ex – Français", texte, p)[0]


def test_plusieurs_fiches_du_meme_produit_dans_une_boutique_n_alertent_qu_une_fois():
    """08/10/2026 : 10 fiches Mini Tin chez ultrajeux.com ; une seule
    commandable ne doit pas re-alerter a chaque cycle (etat ecrase)."""
    import alerte_precommande as ap
    nom = "Mini Tin — 30e Anniversaire (30th Celebration) FR"

    def fiche(n, stock, prix=29.9):
        return {"nom_produit": nom, "confiance": "moyenne", "raison": "", "titre": f"Mini Tin {n}",
                "url_produit": f"https://u.fr/p{n}", "prix": prix, "en_stock": stock, "alerte_disponibilite": True}

    memoire = {}
    ap.detecter_nouvelles_precommandes("u.fr", [fiche(1, False), fiche(2, False)], memoire)   # reference
    ev = ap.detecter_nouvelles_precommandes("u.fr", [fiche(1, False), fiche(2, True), fiche(3, False)], memoire)
    assert [e["url_produit"] for e in ev] == ["https://u.fr/p2"]
    memoire[ev[0]["_cle_memoire"]] = ev[0]["_nouvel_etat"]                                    # envoi reussi
    assert ap.detecter_nouvelles_precommandes("u.fr", [fiche(1, False), fiche(2, True), fiche(3, False)], memoire) == []
    choix = ap._consolider_suivi_disponibilite([fiche(1, True, 40), fiche(2, True, 30)])
    assert [c["url_produit"] for c in choix] == ["https://u.fr/p2"]
