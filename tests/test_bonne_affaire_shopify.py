"""Tests de non-regression pour les garde-fous de evaluer_deal
(bonne_affaire_shopify.py) : stock -> langue -> qualificatif -> prix. Chaque
garde-fou correspond a un bug reel deja rencontre en prod, cf.
SESSION_NOTES.md."""

from unittest.mock import patch

from connecteur_shopify import ResultatRecherche
from bonne_affaire_shopify import (
    _etat_refuse, _texte_bonne_affaire, envoyer_telegram_bonnes_affaires, evaluer_deal,
)
from watchlist_shopify import CarteWatchlist


def _resultat(**kwargs) -> ResultatRecherche:
    base = dict(
        boutique="exemple.fr",
        titre="Dracaufeu 199/165",
        prix=50.0,
        en_stock=True,
        url_produit="https://exemple.fr/produit",
        variante_titre="",
        image_url=None,
        langue_detectee=None,
        confiance="forte",
        etat_detecte=None,
    )
    base.update(kwargs)
    return ResultatRecherche(**base)


def _carte(**kwargs) -> CarteWatchlist:
    base = dict(
        nom_recherche="Dracaufeu",
        numero="199/165",
        langue="fr",
        nom_config="Dracaufeu ex 199/165",
        prix_max_fixe=None,
        qualificatif=None,
    )
    base.update(kwargs)
    return CarteWatchlist(**base)


REGLES = {"cote_min": 5.0, "marge_achat": 0.10, "prix_plancher_ratio": 0.15,
          "marge_revente": 0.10, "frais_revente_estimes": 0.13, "profit_min": 0}
COTES = {"Dracaufeu ex 199/165|fr": [{"cote": 100.0, "ts": 0}]}


def test_carte_gradee_psa_rejetee():
    # Cas reel signale par Justok le 13/08/2026 : Evoli ex 167/131 sur
    # relictcg.com, annonce "PSA 8" alertee comme "bonne affaire" a -53.9%
    # -- une carte gradee n'est pas comparable a la cote d'une carte brute.
    titre = "Acheter - Evoli ex SAR - PRE167/131 - EV8.5 - PSA 8 - FR"
    deal, raison = evaluer_deal(_resultat(titre=titre), _carte(), COTES, REGLES)
    assert deal is None
    assert "gradee" in raison


def test_carte_gradee_ccc_rejetee():
    # Meme soiree, 2e annonce sur la meme carte : notation de gradation
    # differente ("CCC 9.5") -- pas dans la liste initiale, ajoutee suite
    # a ce cas reel.
    titre = "Evoli ex - Evolutions Prismatiques 167/131 - CCC 9.5 - FR"
    deal, raison = evaluer_deal(_resultat(titre=titre), _carte(), COTES, REGLES)
    assert deal is None
    assert "gradee" in raison


def test_carte_non_gradee_nest_pas_rejetee_a_tort():
    # "non gradee" contient "gradee" en sous-chaine -- ne doit PAS etre
    # exclue (c'est justement une carte BRUTE), meme negation que main.py.
    # (titre volontairement SANS "ex" pour ne pas declencher le garde-fou
    # qualificatif symetrique, deja teste ailleurs dans ce fichier.)
    titre = "Dracaufeu 199/165 non gradee excellent etat"
    deal, raison = evaluer_deal(_resultat(titre=titre), _carte(), COTES, REGLES)
    assert deal is not None, raison


def test_etat_excellent_rejete():
    # Cas reel (14/08/2026) : kairyu.fr, Eevee ex 223 sv8a, "Etat : Exc"
    # alertee a tort comme bonne affaire -- Justok ne veut que du Neuf/NM.
    deal, raison = evaluer_deal(_resultat(etat_detecte="exc"), _carte(), COTES, REGLES)
    assert deal is None
    assert "etat refuse" in raison


def test_etat_near_mint_nest_pas_rejete():
    deal, raison = evaluer_deal(_resultat(etat_detecte="near mint"), _carte(), COTES, REGLES)
    assert deal is not None, raison


def test_etat_absent_nest_pas_rejete():
    # Aucun label d'etat trouve sur la fiche produit -> on alerte quand meme
    # (beaucoup de boutiques n'indiquent pas l'etat sur toutes leurs fiches).
    deal, raison = evaluer_deal(_resultat(etat_detecte=None), _carte(), COTES, REGLES)
    assert deal is not None, raison


def test_etat_refuse_fonction_directe():
    assert _etat_refuse("exc") is True
    assert _etat_refuse("excellent") is True
    assert _etat_refuse("light played") is True
    assert _etat_refuse("near mint") is False
    assert _etat_refuse("neuf") is False
    assert _etat_refuse(None) is False


def test_rupture_de_stock_rejetee():
    deal, raison = evaluer_deal(_resultat(en_stock=False), _carte(), COTES, REGLES)
    assert deal is None
    assert "rupture" in raison


def test_langue_incoherente_rejetee():
    # Une carte configuree FR ne doit jamais matcher un titre explicitement JP/KR.
    deal, raison = evaluer_deal(_resultat(langue_detectee="jp"), _carte(langue="fr"), COTES, REGLES)
    assert deal is None
    assert "langue" in raison


def test_jp_ou_kr_compatible_avec_carte_jp():
    cotes = {"Eevee 078|jp": [{"cote": 100.0, "ts": 0}]}
    carte = _carte(nom_config="Eevee 078", numero="078", langue="jp")
    deal, raison = evaluer_deal(_resultat(langue_detectee="jp_ou_kr", prix=50.0), carte, cotes, REGLES)
    assert deal is not None, raison


def test_qualificatif_manquant_dans_le_titre_rejete():
    # "Plumeline ex 024" (config) ne doit pas matcher un titre sans "ex".
    carte = _carte(nom_config="Plumeline ex 024", numero="024", qualificatif="ex")
    deal, raison = evaluer_deal(_resultat(titre="Plumeline 24 Sun & Moon REVERSE"), carte, COTES, REGLES)
    assert deal is None
    assert "qualificatif" in raison


def test_qualificatif_inattendu_dans_le_titre_rejete_symetrique():
    # Carte configuree SANS qualificatif ne doit pas matcher un titre "ex" homonyme.
    carte = _carte(qualificatif=None)
    deal, raison = evaluer_deal(_resultat(titre="Dracaufeu ex 199/165 - Edition Speciale"), carte, COTES, REGLES)
    assert deal is None
    assert "qualificatif" in raison


def test_prix_sous_la_cote_avec_marge_est_un_deal():
    deal, raison = evaluer_deal(_resultat(prix=50.0), _carte(), COTES, REGLES)
    assert deal is not None, raison
    assert deal["decote_pct"] == 50.0


def test_prix_trop_proche_de_la_cote_rejete():
    deal, raison = evaluer_deal(_resultat(prix=95.0), _carte(), COTES, REGLES)
    assert deal is None
    assert "pas assez sous la cote" in raison


def test_prix_suspect_trop_bas_rejete():
    # Garde-fou "trop beau pour etre vrai" : sous 15% de la cote.
    deal, raison = evaluer_deal(_resultat(prix=5.0), _carte(), COTES, REGLES)
    assert deal is None
    assert "suspect" in raison


def test_seuil_fixe_prioritaire_sur_la_cote():
    carte = _carte(prix_max_fixe=60.0)
    deal, raison = evaluer_deal(_resultat(prix=55.0), carte, COTES, REGLES)
    assert deal is not None, raison
    assert raison == "DEAL (seuil fixe)"

    deal, raison = evaluer_deal(_resultat(prix=65.0), carte, COTES, REGLES)
    assert deal is None
    assert "seuil fixe" in raison


def test_deal_transporte_image_url_et_langue_pour_la_verification_photo():
    # image_url/langue doivent survivre jusqu'au deal pour que
    # envoyer_telegram_bonnes_affaires puisse appeler verifier_photo_annonce.
    deal, raison = evaluer_deal(
        _resultat(image_url="https://exemple.fr/photo.jpg"), _carte(), COTES, REGLES)
    assert deal is not None, raison
    assert deal["image_url"] == "https://exemple.fr/photo.jpg"
    assert deal["langue"] == "fr"


def test_texte_bonne_affaire_ajoute_la_ligne_incoherente():
    d = {"nom": "Test", "boutique": "x.fr", "prix": 10.0, "cote": 20.0,
         "decote_pct": 45.0, "prix_revente_conseille": 25.0,
         "profit_net_estime": 10.0, "confiance": 0, "url_produit": "https://x"}
    texte = _texte_bonne_affaire(d, ("incoherent", "carte coréenne visible"))
    assert "incohérente" in texte
    assert "peut se tromper" in texte
    assert "carte coréenne visible" in texte


def test_texte_bonne_affaire_verification_non_tentee_naffiche_rien():
    d = {"nom": "Test", "boutique": "x.fr", "prix": 10.0, "cote": 20.0,
         "decote_pct": 5.0, "prix_revente_conseille": 25.0,
         "profit_net_estime": 10.0, "confiance": 0, "url_produit": "https://x"}
    assert "Vérification IA" not in _texte_bonne_affaire(d, None)
    assert "Vérification IA" not in _texte_bonne_affaire(d)


def test_envoyer_telegram_bonnes_affaires_sans_cle_api_ninterroge_jamais_la_verification():
    deal = {"nom": "Test", "boutique": "x.fr", "prix": 10.0, "cote": 20.0,
            "decote_pct": 5.0, "prix_revente_conseille": 25.0,
            "profit_net_estime": 10.0, "confiance": 0, "url_produit": "https://x",
            "image_url": "https://x.fr/photo.jpg", "langue": "fr"}
    with patch("bonne_affaire_shopify.verifier_photo_annonce") as verif_mock, \
         patch("bonne_affaire_shopify.requests.post") as post_mock:
        post_mock.return_value.status_code = 200
        envoyer_telegram_bonnes_affaires([deal], "chat123", "token-telegram", anthropic_api_key="")
    verif_mock.assert_not_called()


def test_envoyer_telegram_bonnes_affaires_avec_cle_et_image_appelle_la_verification():
    deal = {"nom": "Dracaufeu ex 199/165", "boutique": "x.fr", "prix": 10.0, "cote": 20.0,
            "decote_pct": 5.0, "prix_revente_conseille": 25.0,
            "profit_net_estime": 10.0, "confiance": 0, "url_produit": "https://x",
            "image_url": "https://x.fr/photo.jpg", "langue": "jp"}
    with patch("bonne_affaire_shopify.verifier_photo_annonce", return_value=("incoherent", "carte coréenne")) as verif_mock, \
         patch("bonne_affaire_shopify.requests.post") as post_mock:
        post_mock.return_value.status_code = 200
        envoyer_telegram_bonnes_affaires([deal], "chat123", "token-telegram", anthropic_api_key="sk-ant-xxx")
    verif_mock.assert_called_once_with("https://x.fr/photo.jpg", "Dracaufeu ex 199/165", "jp", "sk-ant-xxx")
    texte_envoye = post_mock.call_args.kwargs["json"]["text"]
    assert "incohérente" in texte_envoye


def test_envoyer_telegram_bonnes_affaires_verdict_incoherent_nempeche_jamais_lenvoi():
    # Cas reel (17/08/2026, cf. SESSION_NOTES.md V51) : un faux positif de
    # verification photo NE DOIT JAMAIS empecher l'envoi d'un vrai deal --
    # le systeme est concu comme purement informatif, jamais bloquant.
    deal = {"nom": "Dracaufeu ex 199/165", "boutique": "x.fr", "prix": 10.0, "cote": 20.0,
            "decote_pct": 5.0, "prix_revente_conseille": 25.0,
            "profit_net_estime": 10.0, "confiance": 0, "url_produit": "https://x",
            "image_url": "https://x.fr/photo.jpg", "langue": "jp"}
    with patch("bonne_affaire_shopify.verifier_photo_annonce",
               return_value=("incoherent", "carte differente sur la photo")), \
         patch("bonne_affaire_shopify.requests.post") as post_mock:
        post_mock.return_value.status_code = 200
        resultat = envoyer_telegram_bonnes_affaires([deal], "chat123", "token-telegram", anthropic_api_key="sk-ant-xxx")
    post_mock.assert_called_once()
    assert resultat is True
