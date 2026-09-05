"""Tests de non-regression pour watchlist_saas.py -- extension de la
watchlist scraper avec les cartes ajoutees par les utilisateurs du SaaS."""

from unittest.mock import patch

from watchlist_shopify import CarteWatchlist
from watchlist_saas import (
    MAX_CARTES_SAAS_EBAY,
    _grouper_par_carte,
    _selectionner_avec_rotation,
    cartes_watchlist_saas,
    dict_watchlist_saas,
)


def _item(nom_carte="Dracaufeu ex 199/165", langue="fr", prix_seuil=50.0, item_id="i1", actif=None):
    item = {"id": item_id, "user_id": "u1", "nom_carte": nom_carte, "langue": langue, "prix_seuil": prix_seuil}
    if actif is not None:
        item["actif"] = actif
    return item


# ------------------- _grouper_par_carte -------------------

def test_grouper_carte_unique():
    groupes = _grouper_par_carte([_item()])
    assert len(groupes) == 1
    assert groupes[0]["nom"] == "Dracaufeu ex 199/165"
    assert groupes[0]["langue"] == "fr"
    assert groupes[0]["prix_max_fixe"] == 50.0
    assert groupes[0]["nb_utilisateurs"] == 1


def test_grouper_meme_carte_deux_utilisateurs_garde_le_seuil_le_plus_haut():
    items = [_item(prix_seuil=50.0, item_id="i1"), _item(prix_seuil=80.0, item_id="i2")]
    groupes = _grouper_par_carte(items)
    assert len(groupes) == 1
    assert groupes[0]["prix_max_fixe"] == 80.0
    assert groupes[0]["nb_utilisateurs"] == 2


def test_grouper_insensible_a_la_casse_et_accents():
    items = [_item(nom_carte="DRACAUFEU EX 199/165"), _item(nom_carte="dracaufeu ex 199/165")]
    groupes = _grouper_par_carte(items)
    assert len(groupes) == 1
    assert groupes[0]["nb_utilisateurs"] == 2


def test_grouper_langues_differentes_restent_separees():
    items = [_item(langue="fr"), _item(langue="jp")]
    groupes = _grouper_par_carte(items)
    assert len(groupes) == 2


def test_grouper_seuil_invalide_est_ignore():
    groupes = _grouper_par_carte([_item(prix_seuil="pas-un-nombre")])
    assert groupes == []


def test_grouper_seuil_nul_ou_negatif_est_ignore():
    assert _grouper_par_carte([_item(prix_seuil=0)]) == []
    assert _grouper_par_carte([_item(prix_seuil=-5)]) == []


def test_grouper_nom_carte_vide_est_ignore():
    assert _grouper_par_carte([_item(nom_carte="")]) == []


def test_grouper_carte_en_pause_est_exclue():
    # Correctif du 04/09/2026 : le bouton "Mettre en pause" du dashboard SaaS
    # (watchlist_items.actif = false) ne faisait rien cote scraper avant ce
    # correctif -- la carte continuait d'etre scannee malgre la pause.
    assert _grouper_par_carte([_item(actif=False)]) == []


def test_grouper_carte_active_explicitement_est_incluse():
    groupes = _grouper_par_carte([_item(actif=True)])
    assert len(groupes) == 1


def test_grouper_carte_sans_colonne_actif_est_traitee_comme_active():
    # Retro-compatibilite : une ligne qui n'aurait pas la colonne `actif`
    # (ancien schema) ne doit jamais etre silencieusement exclue par defaut.
    groupes = _grouper_par_carte([_item()])
    assert len(groupes) == 1


def test_grouper_melange_cartes_actives_et_en_pause():
    items = [
        _item(item_id="i1", nom_carte="Dracaufeu ex 199/165", actif=True),
        _item(item_id="i2", nom_carte="Pikachu vmax 44/185", actif=False),
    ]
    groupes = _grouper_par_carte(items)
    assert len(groupes) == 1
    assert groupes[0]["nom"] == "Dracaufeu ex 199/165"


def test_grouper_trie_par_nombre_dutilisateurs_decroissant():
    items = (
        [_item(nom_carte="Pikachu 173/165", item_id="p1")]
        + [_item(nom_carte="Dracaufeu ex 199/165", item_id=f"d{i}") for i in range(3)]
    )
    groupes = _grouper_par_carte(items)
    assert groupes[0]["nom"] == "Dracaufeu ex 199/165"
    assert groupes[0]["nb_utilisateurs"] == 3
    assert groupes[1]["nom"] == "Pikachu 173/165"


# ------------------- _selectionner_avec_rotation -------------------
# Bug reel corrige le 05/09/2026 (audit externe multi-IA) : l'ancien tri
# (nb_utilisateurs decroissant, plafonne) etait un ordre STATIQUE -- une
# carte moins populaire que les max_cartes autres restait hors rotation
# pour toujours, sans jamais etre recherchee sur eBay/Vinted, sans aucun
# signal visible pour l'utilisateur.

def _carte(nom="Dracaufeu ex 199/165", langue="fr", nb_utilisateurs=1):
    return {"nom": nom, "langue": langue, "prix_max_fixe": 50.0, "nb_utilisateurs": nb_utilisateurs}


def test_rotation_memoire_vide_conserve_lordre_de_grouper_par_carte():
    # Memoire vide -- toutes les cartes sont "jamais scannees", donc l'ordre
    # de popularite decroissante deja etabli par _grouper_par_carte() (avant
    # cette fonction) est simplement conserve, comme avant ce correctif.
    cartes = [_carte(nom="Tres populaire", nb_utilisateurs=5), _carte(nom="Peu populaire", nb_utilisateurs=1)]
    with patch("watchlist_saas.charger_memoire_supabase", return_value={}), \
         patch("watchlist_saas.sauvegarder_memoire_supabase", return_value=True):
        selection = _selectionner_avec_rotation(cartes, 1, "https://x.supabase.co", "cle")
    assert [c["nom"] for c in selection] == ["Tres populaire"]


def test_rotation_carte_jamais_scannee_passe_avant_une_carte_deja_scannee_meme_moins_populaire():
    populaire_deja_scannee = _carte(nom="Populaire", nb_utilisateurs=10)
    nouvelle_carte = _carte(nom="Nouvelle carte", nb_utilisateurs=1)
    memoire = {_cle_test(populaire_deja_scannee): "2026-09-01T00:00:00+00:00"}
    with patch("watchlist_saas.charger_memoire_supabase", return_value=memoire), \
         patch("watchlist_saas.sauvegarder_memoire_supabase", return_value=True):
        selection = _selectionner_avec_rotation(
            [populaire_deja_scannee, nouvelle_carte], 1, "https://x.supabase.co", "cle")
    assert selection == [nouvelle_carte]


def test_rotation_carte_jamais_exclue_definitivement():
    # Le coeur du bug corrige : sur 2 cycles avec un plafond de 1, une carte
    # jamais scannee au cycle precedent doit finir par passer.
    carte_populaire = _carte(nom="Toujours populaire", nb_utilisateurs=100)
    carte_ecrasee = _carte(nom="Jamais populaire", nb_utilisateurs=1)
    memoire_persistee = {}

    def _charger(cle, url, key):
        return dict(memoire_persistee)

    def _sauvegarder(memoire, cle, url, key):
        memoire_persistee.clear()
        memoire_persistee.update(memoire)
        return True

    with patch("watchlist_saas.charger_memoire_supabase", side_effect=_charger), \
         patch("watchlist_saas.sauvegarder_memoire_supabase", side_effect=_sauvegarder):
        cycle_1 = _selectionner_avec_rotation(
            [carte_populaire, carte_ecrasee], 1, "https://x.supabase.co", "cle")
        cycle_2 = _selectionner_avec_rotation(
            [carte_populaire, carte_ecrasee], 1, "https://x.supabase.co", "cle")
    assert cycle_1 == [carte_populaire]  # jamais scannee, en tete par popularite parmi les jamais-scannees
    assert cycle_2 == [carte_ecrasee]  # seule carte encore jamais scannee au cycle 2


def test_rotation_purge_les_cartes_qui_nexistent_plus():
    carte_actuelle = _carte(nom="Existe toujours")
    memoire = {_cle_test(carte_actuelle): "2026-09-01T00:00:00+00:00",
               "carte-disparue|fr": "2026-08-01T00:00:00+00:00"}
    sauvegardes = []
    with patch("watchlist_saas.charger_memoire_supabase", return_value=memoire), \
         patch("watchlist_saas.sauvegarder_memoire_supabase",
               side_effect=lambda m, *a: sauvegardes.append(m) or True):
        _selectionner_avec_rotation([carte_actuelle], 5, "https://x.supabase.co", "cle")
    assert "carte-disparue|fr" not in sauvegardes[0]


def test_rotation_panne_lecture_memoire_degrade_vers_ordre_de_popularite():
    # Etat non critique (contrairement a la memoire de dedup) -- une panne
    # ne doit jamais faire echouer le scan, juste revenir au comportement
    # d'avant ce correctif.
    carte_populaire = _carte(nom="Populaire", nb_utilisateurs=10)
    carte_moins_populaire = _carte(nom="Moins populaire", nb_utilisateurs=1)
    with patch("watchlist_saas.charger_memoire_supabase", return_value=None), \
         patch("watchlist_saas.sauvegarder_memoire_supabase", return_value=True):
        selection = _selectionner_avec_rotation(
            [carte_populaire, carte_moins_populaire], 1, "https://x.supabase.co", "cle")
    assert selection == [carte_populaire]


def _cle_test(carte):
    from filtre_annonces import normaliser
    return f"{normaliser(carte['nom'])}|{carte['langue']}"


# ------------------- dict_watchlist_saas -------------------

def test_dict_watchlist_saas_format_compatible_config_yaml():
    with patch("watchlist_saas.lister_watchlist_items", return_value=[_item()]):
        cartes = dict_watchlist_saas("https://x.supabase.co", "cle-secrete")
    assert cartes == [{"nom": "Dracaufeu ex 199/165", "langue": "fr", "prix_max_fixe": 50.0}]


def test_dict_watchlist_saas_liste_vide_si_pas_de_watchlists():
    with patch("watchlist_saas.lister_watchlist_items", return_value=[]):
        cartes = dict_watchlist_saas("https://x.supabase.co", "cle-secrete")
    assert cartes == []


def test_dict_watchlist_saas_respecte_le_plafond():
    items = [_item(nom_carte=f"Carte {i} 001/165", item_id=str(i)) for i in range(5)]
    with patch("watchlist_saas.lister_watchlist_items", return_value=items), \
         patch("watchlist_saas.charger_memoire_supabase", return_value={}), \
         patch("watchlist_saas.sauvegarder_memoire_supabase", return_value=True):
        cartes = dict_watchlist_saas("https://x.supabase.co", "cle-secrete", max_cartes=2)
    assert len(cartes) == 2


def test_dict_watchlist_saas_sans_plafond_par_defaut():
    items = [_item(nom_carte=f"Carte {i} 001/165", item_id=str(i)) for i in range(MAX_CARTES_SAAS_EBAY + 5)]
    with patch("watchlist_saas.lister_watchlist_items", return_value=items):
        cartes = dict_watchlist_saas("https://x.supabase.co", "cle-secrete")
    assert len(cartes) == MAX_CARTES_SAAS_EBAY + 5


# ------------------- cartes_watchlist_saas -------------------

def test_cartes_watchlist_saas_convertit_en_cartewatchlist():
    with patch("watchlist_saas.lister_watchlist_items", return_value=[_item()]):
        cartes = cartes_watchlist_saas("https://x.supabase.co", "cle-secrete")
    assert len(cartes) == 1
    carte = cartes[0]
    assert isinstance(carte, CarteWatchlist)
    assert carte.nom_recherche == "Dracaufeu"
    assert carte.numero == "199/165"
    assert carte.qualificatif == "ex"
    assert carte.langue == "fr"
    assert carte.nom_config == "Dracaufeu ex 199/165"
    assert carte.prix_max_fixe == 50.0


def test_cartes_watchlist_saas_sans_qualificatif():
    with patch("watchlist_saas.lister_watchlist_items", return_value=[_item(nom_carte="Pikachu 173/165")]):
        cartes = cartes_watchlist_saas("https://x.supabase.co", "cle-secrete")
    assert cartes[0].qualificatif is None
    assert cartes[0].nom_recherche == "Pikachu"


def test_cartes_watchlist_saas_liste_vide_si_pas_de_watchlists():
    with patch("watchlist_saas.lister_watchlist_items", return_value=[]):
        cartes = cartes_watchlist_saas("https://x.supabase.co", "cle-secrete")
    assert cartes == []
