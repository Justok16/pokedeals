"""Veille express des produits des 30 ans (08/10/2026) : une seule alerte
par passage en stock, que ce soit la veille ou le radar qui le voie."""

from unittest.mock import MagicMock

import veille_express_30e as v

ETB = "Coffret Dresseur d'Élite — 30e Anniversaire FR (suivi restock)"
CLE = f"b.fr|{ETB}"


def obs(stock, horodatage="2026-10-08T08:00:00+00:00", prix=60.0, url="https://b.fr/p/etb"):
    return {"domaine": "b.fr", "nom_produit": ETB, "confiance": "moyenne", "raison": "", "titre": "ETB 30e",
            "url_produit": url, "prix": prix, "en_stock": stock, "alerte_disponibilite": True,
            "horodatage": horodatage}


def test_reference_silencieuse_puis_alerte_sur_passage_en_stock():
    memoire = {}
    assert v.evenements_express([obs(False)], memoire, {}) == []
    assert memoire[CLE]["en_stock"] is False
    ev = v.evenements_express([obs(True, "2026-10-08T08:05:00+00:00")], memoire, {})
    assert [e["_cle_memoire"] for e in ev] == [CLE] and ev[0]["_nouvel_etat"]["alerte"]
    assert memoire[CLE]["en_stock"] is False          # ecriture differee jusqu'a l'envoi reussi


def test_pas_de_doublon_si_le_radar_a_vu_le_stock_plus_recemment():
    memoire = {CLE: {"en_stock": False, "verifie": "2026-10-08T08:00:00+00:00"}}
    radar = {CLE: {"en_stock": True, "derniere_verification": "2026-10-08T08:03:00+00:00"}}
    assert v.evenements_express([obs(True, "2026-10-08T08:05:00+00:00")], memoire, radar) == []
    assert memoire[CLE]["en_stock"] is True


def test_alerte_si_le_radar_est_reste_sur_un_vieux_en_stock():
    """Le radar a vu le stock il y a longtemps, la veille a vu la rupture
    depuis : un retour en stock doit alerter."""
    memoire = {CLE: {"en_stock": False, "verifie": "2026-10-08T08:00:00+00:00"}}
    radar = {CLE: {"en_stock": True, "derniere_verification": "2026-10-08T06:00:00+00:00"}}
    assert len(v.evenements_express([obs(True, "2026-10-08T08:05:00+00:00")], memoire, radar)) == 1


def test_le_radar_ne_realerte_pas_ce_que_la_veille_a_deja_signale():
    express = {CLE: {"en_stock": True, "verifie": "2026-10-08T08:05:00+00:00", "alerte": "2026-10-08T08:05:00+00:00"}}
    evenement = {"_cle_memoire": CLE}
    assert v.deja_alerte_par_la_veille_express(evenement, express, {"derniere_verification": "2026-10-08T08:00:00+00:00"})
    # Signalement de la veille ANTERIEUR a la derniere observation du radar : nouvel episode.
    assert not v.deja_alerte_par_la_veille_express(evenement, express, {"derniere_verification": "2026-10-08T09:00:00+00:00"})
    assert not v.deja_alerte_par_la_veille_express(evenement, {}, None)


def test_fiches_a_surveiller_lit_les_memoires_du_radar():
    memoires = {"precommandes_anniversaire_shopify": {
        "__balayage__|b.fr|x": {"depuis": ""},
        CLE: {"url_produit": "https://b.fr/products/etb", "titre_produit": "ETB"},
        "b.fr|Autre produit": {"url_produit": "https://b.fr/products/autre"}},
        "precommandes_anniversaire_leclerc_complement": {"e.leclerc|" + ETB: {"url_produit": "https://e.leclerc/fp/x"}}}
    plateformes = {"precommandes_anniversaire_shopify": "shopify", "precommandes_anniversaire_leclerc_complement": "leclerc"}
    assert v.fiches_a_surveiller(memoires, plateformes, {ETB}) == [
        {"plateforme": "shopify", "domaine": "b.fr", "nom_produit": ETB, "url": "https://b.fr/products/etb", "titre": "ETB"}]


def test_fiche_shopify_lit_la_variante_exacte_et_le_prix_en_centimes():
    reponse = MagicMock(status_code=200)
    reponse.json.return_value = {"title": "UPC 30e", "variants": [
        {"id": 1, "available": True, "price": 42990}, {"id": 2, "available": False, "price": 42990}]}
    session = MagicMock()
    session.get.return_value = reponse
    produit = MagicMock(prioritaire=False)
    fiche = {"domaine": "b.fr", "nom_produit": ETB, "url": "https://b.fr/products/upc?variant=2", "titre": ""}
    o = v.observer_fiche_shopify(session, fiche, produit)
    assert session.get.call_args[0][0] == "https://b.fr/products/upc.js"
    assert (o["en_stock"], o["prix"]) == (False, 429.9)
    fiche["url"] = "https://b.fr/products/upc"
    assert v.observer_fiche_shopify(session, fiche, produit)["en_stock"] is True
