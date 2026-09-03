"""Tests de non-regression pour verification_alertes.py (ajoute le
03/09/2026 -- verification periodique de disponibilite/prix des alertes
watchlist_alerts pour le dashboard SaaS). Couvre : le dispatch par
plateforme, les 3 connecteurs (Shopify/PrestaShop/WooCommerce) sur un cas
"disponible" et un cas ou le garde-fou DOM doit forcer disponible=False
malgre un JSON-LD optimiste, et le cas eBay (volontairement non couvert,
doit toujours renvoyer None -- jamais une conclusion par exces de
confiance)."""

from unittest.mock import Mock, patch

import requests

import verification_alertes as va


def test_plateforme_boutique_reconnait_les_3_types():
    assert va._plateforme_boutique("kairyu.fr") == "shopify"
    assert va._plateforme_boutique("plazatcg.com") == "prestashop"
    assert va._plateforme_boutique("mymesis.fr") == "woocommerce"


def test_plateforme_boutique_ebay_non_couvert():
    assert va._plateforme_boutique("ebay.fr") is None


def test_domaine_depuis_url_retire_www():
    assert va._domaine_depuis_url("https://www.blazingtail.fr/59033-x.html") == "blazingtail.fr"


def test_verifier_shopify_disponible():
    with patch.object(va, "requests") as mrequests:
        reponse = Mock(status_code=200, ok=True)
        reponse.json.return_value = {"product": {"variants": [{"available": True, "price": "12.50"}]}}
        mrequests.get.return_value = reponse
        assert va._verifier_shopify("https://kairyu.fr/products/x") == {"disponible": True, "prix": 12.50}


def test_verifier_shopify_404_signifie_vendu_ou_supprime():
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=404)
        assert va._verifier_shopify("https://kairyu.fr/products/x") == {"disponible": False, "prix": None}


def _html_jsonld(prix: str, disponibilite: str = "https://schema.org/InStock") -> str:
    return (
        '<html><script type="application/ld+json">'
        f'{{"@type":"Product","offers":{{"price":"{prix}","priceCurrency":"EUR",'
        f'"availability":"{disponibilite}"}}}}'
        "</script></html>"
    )


def test_verifier_prestashop_disponible():
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=200, ok=True, text=_html_jsonld("29.90"))
        assert va._verifier_prestashop("https://plazatcg.com/x.html") == {"disponible": True, "prix": 29.90}


def test_verifier_prestashop_garde_fou_dom_force_indisponible():
    # JSON-LD annonce InStock, mais le span de rupture PrestaShop dit le
    # contraire -- le signal RENDU (DOM) doit toujours l'emporter (meme
    # garde-fou que connecteur_prestashop_sitemap.py).
    html = _html_jsonld("29.90").replace(
        "</html>", '<span id="product-availability">Rupture de stock</span></html>'
    )
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=200, ok=True, text=html)
        assert va._verifier_prestashop("https://plazatcg.com/x.html") == {"disponible": False, "prix": 29.90}


def test_verifier_woocommerce_disponible():
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=200, ok=True, text=_html_jsonld("18.90"))
        assert va._verifier_woocommerce("https://mymesis.fr/x/") == {"disponible": True, "prix": 18.90}


def test_verifier_woocommerce_garde_fou_dom_classe_outofstock():
    html = _html_jsonld("18.90").replace("<html>", '<html><div class="product outofstock">')
    with patch.object(va, "requests") as mrequests:
        mrequests.get.return_value = Mock(status_code=200, ok=True, text=html)
        assert va._verifier_woocommerce("https://mymesis.fr/x/") == {"disponible": False, "prix": 18.90}


def test_verifier_une_alerte_ebay_jamais_de_conclusion_par_defaut():
    # Plateforme non couverte -- doit toujours renvoyer None, jamais
    # interpreter l'absence de verification comme "indisponible".
    assert va.verifier_une_alerte("https://www.ebay.fr/itm/123456") is None


def test_verifier_shopify_erreur_reseau_renvoie_none():
    import requests as requests_reel

    with patch.object(va, "requests") as mrequests:
        mrequests.RequestException = requests_reel.RequestException
        mrequests.get.side_effect = requests_reel.RequestException("boom")
        assert va._verifier_shopify("https://kairyu.fr/products/x") is None


# ------------------- lister_alertes_recentes (03/09/2026, champs etendus) -------------------

def test_lister_alertes_recentes_selectionne_les_champs_necessaires_a_la_transition():
    reponse = Mock()
    reponse.raise_for_status = Mock()
    reponse.json.return_value = []
    with patch.object(va.requests, "get", return_value=reponse) as get_mock:
        va.lister_alertes_recentes("https://x.supabase.co", "cle")
    _, kwargs = get_mock.call_args
    champs = set(kwargs["params"]["select"].split(","))
    # id/url : verification elle-meme. user_id/titre/prix/plateforme :
    # necessaires a la notification. disponible/prix_verifie : etat
    # PRECEDENT, indispensable a detecter_transition().
    assert champs == {"id", "url", "user_id", "titre", "prix", "plateforme", "disponible", "prix_verifie"}


def test_lister_alertes_recentes_sans_secrets_ne_declenche_aucun_appel():
    with patch.object(va.requests, "get") as get_mock:
        assert va.lister_alertes_recentes("", "") == []
    get_mock.assert_not_called()


def test_lister_alertes_recentes_erreur_reseau_retourne_liste_vide():
    with patch.object(va.requests, "get", side_effect=requests.RequestException("boom")):
        assert va.lister_alertes_recentes("https://x.supabase.co", "cle") == []


# ------------------- detecter_transition (03/09/2026, notification) -------------------
# Ne doit signaler QUE 2 transitions, jamais un etat deja connu (pour ne pas
# re-notifier a chaque cycle de 30 min tant que l'etat ne change pas) --
# cf. docstring du module pour le detail.

def _alerte(disponible=None, prix=100.0, prix_verifie=None, titre="Dracaufeu", plateforme="kairyu.fr"):
    return {"disponible": disponible, "prix": prix, "prix_verifie": prix_verifie,
            "titre": titre, "plateforme": plateforme}


def test_transition_aucune_si_resultat_none():
    assert va.detecter_transition(_alerte(), None) is None


def test_transition_vendu_depuis_jamais_verifie():
    # disponible=None (jamais verifie) -> False : premiere detection du "vendu".
    resultat = {"disponible": False, "prix": None}
    assert va.detecter_transition(_alerte(disponible=None), resultat) == "vendu"


def test_transition_vendu_depuis_disponible():
    resultat = {"disponible": False, "prix": None}
    assert va.detecter_transition(_alerte(disponible=True), resultat) == "vendu"


def test_transition_vendu_pas_re_signale_si_deja_indisponible():
    # Deja "disponible: False" au cycle precedent -- pas une NOUVELLE
    # transition, ne doit pas re-notifier a chaque cycle de 30 min.
    resultat = {"disponible": False, "prix": None}
    assert va.detecter_transition(_alerte(disponible=False), resultat) is None


def test_transition_aucune_si_toujours_disponible():
    resultat = {"disponible": True, "prix": 100.0}
    assert va.detecter_transition(_alerte(disponible=True), resultat) is None


def test_transition_baisse_prix_franchit_le_seuil():
    # Prix d'origine 100€, verifie a 90€ (baisse de 10% > 5%) -- premiere
    # fois que le seuil est franchi (prix_verifie precedent = None).
    resultat = {"disponible": True, "prix": 90.0}
    assert va.detecter_transition(_alerte(disponible=True, prix=100.0, prix_verifie=None), resultat) == "baisse_prix"


def test_transition_aucune_si_baisse_sous_le_seuil():
    # Baisse de seulement 2% (< 5%) -- pas assez significatif pour notifier.
    resultat = {"disponible": True, "prix": 98.0}
    assert va.detecter_transition(_alerte(disponible=True, prix=100.0, prix_verifie=None), resultat) is None


def test_transition_baisse_prix_pas_re_signalee_si_deja_signalee():
    # prix_verifie precedent (85€) deja sous le seuil (100 * 0.95 = 95€) --
    # meme si le nouveau prix (80€) est encore plus bas, ne re-notifie pas
    # (seule la PREMIERE fois franchie compte).
    resultat = {"disponible": True, "prix": 80.0}
    assert va.detecter_transition(_alerte(disponible=True, prix=100.0, prix_verifie=85.0), resultat) is None


def test_transition_baisse_prix_re_signalee_si_remontee_puis_rebaisse():
    # prix_verifie precedent (98€, pas encore sous le seuil) -> nouveau prix
    # (90€, sous le seuil) : nouvelle transition valable.
    resultat = {"disponible": True, "prix": 90.0}
    assert va.detecter_transition(_alerte(disponible=True, prix=100.0, prix_verifie=98.0), resultat) == "baisse_prix"


def test_transition_baisse_prix_sans_prix_verifie_ignoree():
    resultat = {"disponible": True, "prix": None}
    assert va.detecter_transition(_alerte(disponible=True, prix=100.0), resultat) is None


def test_transition_vendu_prioritaire_sur_baisse_prix():
    # Si les deux conditions sont techniquement vraies (rare, mais possible
    # si un connecteur renvoie encore un dernier prix connu avec
    # disponible=False), "vendu" prime -- pas la peine d'annoncer une baisse
    # de prix sur une annonce qui vient de disparaitre.
    resultat = {"disponible": False, "prix": 50.0}
    assert va.detecter_transition(_alerte(disponible=True, prix=100.0), resultat) == "vendu"


# ------------------- message_transition -------------------

def test_message_transition_vendu():
    titre, corps = va.message_transition(_alerte(titre="Dracaufeu ex 199/165", plateforme="kairyu.fr"),
                                          {"disponible": False, "prix": None}, "vendu")
    assert "Dracaufeu ex 199/165" in titre
    assert "kairyu.fr" in corps


def test_message_transition_baisse_prix():
    titre, corps = va.message_transition(
        _alerte(titre="Dracaufeu ex 199/165", prix=100.0, plateforme="kairyu.fr"),
        {"disponible": True, "prix": 85.0}, "baisse_prix",
    )
    assert "Dracaufeu ex 199/165" in titre
    assert "85.00" in corps
    assert "100.00" in corps
