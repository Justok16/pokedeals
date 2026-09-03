"""Tests de non-regression pour connecteur_leboncoin.py (extrait de
main.py le 17/08/2026, module recolle a partir de deux blocs non
contigus -- cf. SESSION_NOTES.md). Couvre : le blocage 403/429 routine
(ne doit JAMAIS compter comme un echec de fiabilite), une vraie panne
(doit compter), et l'extraction d'annonces depuis un HTML d'email."""

from unittest.mock import patch

import connecteur_leboncoin as lbc


def setup_function():
    lbc._stats_fiabilite.update({"leboncoin_appels": 0, "leboncoin_echecs": 0})
    # 03/09/2026 (audit) : coupe-circuit Leboncoin -- chaque test repart
    # d'un etat propre, meme risque de pollution inter-tests que
    # _stats_fiabilite (cf. son commentaire dans stats_fiabilite.py).
    lbc._circuit_leboncoin.update({"echecs_consecutifs": 0, "abandonne": False})


def test_lbc_rechercher_403_est_ignore_sans_compter_comme_echec():
    # Blocage anti-bot ROUTINE (documente) -- ne doit jamais incrementer
    # leboncoin_echecs, sous peine de fausses alertes de fiabilite (V50).
    reponse = type("R", (), {"status_code": 403})()
    with patch.object(lbc, "requete_avec_retry", return_value=reponse):
        annonces = lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert annonces == []
    assert lbc._stats_fiabilite["leboncoin_appels"] == 1
    assert lbc._stats_fiabilite["leboncoin_echecs"] == 0


def test_lbc_rechercher_429_est_ignore_sans_compter_comme_echec():
    reponse = type("R", (), {"status_code": 429})()
    with patch.object(lbc, "requete_avec_retry", return_value=reponse):
        annonces = lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert annonces == []
    assert lbc._stats_fiabilite["leboncoin_echecs"] == 0


def test_lbc_rechercher_erreur_reseau_compte_comme_echec():
    with patch.object(lbc, "requete_avec_retry", side_effect=ConnectionError("panne")):
        annonces = lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert annonces == []
    assert lbc._stats_fiabilite["leboncoin_appels"] == 1
    assert lbc._stats_fiabilite["leboncoin_echecs"] == 1


def test_lbc_rechercher_succes_parse_les_annonces():
    reponse = type("R", (), {
        "status_code": 200,
        "raise_for_status": lambda self: None,
        "json": lambda self: {"ads": [
            {"list_id": 42, "subject": "Dracaufeu ex", "price": [45.0], "url": "https://x", "body": "TBE"},
            {"list_id": 43, "subject": "Sans prix", "price": [], "url": "https://y", "body": ""},
        ]},
    })()
    with patch.object(lbc, "requete_avec_retry", return_value=reponse):
        annonces = lbc.lbc_rechercher("Dracaufeu ex 199/165", "fr")
    assert len(annonces) == 1
    assert annonces[0]["id"] == "lbc-42"
    assert annonces[0]["prix"] == 45.0
    assert annonces[0]["plateforme"] == "Leboncoin"


def test_prix_depuis_texte_gere_les_espaces_insecables():
    # Un prix comme "1 234,56 €" utilise des espaces insecables entre
    # milliers -- piege documente dans la regex (RE_LBC_PRIX).
    assert lbc._prix_depuis_texte("1 234,56 €") == 1234.56
    assert lbc._prix_depuis_texte("45,00 €") == 45.0
    assert lbc._prix_depuis_texte("pas de prix ici") is None


def test_html_vers_texte_retire_scripts_et_balises():
    html = "<div>Bonjour<script>alert(1)</script> le <b>monde</b></div>"
    assert lbc._html_vers_texte(html) == " Bonjour le monde "


def test_lbc_extraire_annonces_email_cas_nominal():
    html = (
        '<a href="https://www.leboncoin.fr/ad/collection/1234567890">'
        'Dracaufeu ex 199/165 carte pokemon rare tres bon etat</a>'
        '<p>Prix : 45,00 €</p>'
    )
    annonces = lbc.lbc_extraire_annonces_email(html)
    assert len(annonces) == 1
    assert annonces[0]["id"] == "lbc-1234567890"
    assert annonces[0]["prix"] == 45.0
    assert "Dracaufeu" in annonces[0]["titre"]


def test_lbc_extraire_annonces_email_deduplique_le_meme_lien():
    html = (
        '<a href="https://www.leboncoin.fr/ad/collection/1234567890">Dracaufeu ex 199/165 carte pokemon rare</a>'
        '<p>45,00 €</p>'
        '<a href="https://www.leboncoin.fr/ad/collection/1234567890">Dracaufeu ex 199/165 carte pokemon rare</a>'
        '<p>45,00 €</p>'
    )
    annonces = lbc.lbc_extraire_annonces_email(html)
    assert len(annonces) == 1


def test_lbc_extraire_annonces_email_rejette_annonce_sans_prix_ni_titre():
    html = '<a href="https://www.leboncoin.fr/ad/collection/9999999999"></a>'
    assert lbc.lbc_extraire_annonces_email(html) == []


def test_lbc_relever_alertes_email_inactif_ne_fait_aucun_appel_imap():
    cfg = {"leboncoin_alertes_email": {"actif": False}}
    with patch.object(lbc.imaplib, "IMAP4_SSL") as mock_imap:
        annonces = lbc.lbc_relever_alertes_email(cfg, {})
    assert annonces == []
    mock_imap.assert_not_called()


def test_lbc_relever_alertes_email_sans_mdp_ni_appel_imap():
    cfg = {"leboncoin_alertes_email": {"actif": True}, "email": {"destinataire": "x@example.com"}}
    with patch.object(lbc.imaplib, "IMAP4_SSL") as mock_imap:
        annonces = lbc.lbc_relever_alertes_email(cfg, {})
    assert annonces == []
    mock_imap.assert_not_called()
