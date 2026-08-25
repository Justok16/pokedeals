"""Tests de non-regression pour detecter_nouvelles_precommandes()
(alerte_precommande.py) -- logique de suppression/declenchement d'alerte a
3 etats (premiere fois / deja vu a ce niveau / deja confirme mieux),
jusqu'ici sans aucune couverture de test (audit du 18/08/2026).

Cas V53 (18/08/2026, signale par Justok) : une premiere detection deja a
confiance "forte" (date de sortie confirmee sur la page) doit alerter
IMMEDIATEMENT, contrairement a une premiere detection "moyenne" (mots-cles
seuls) qui reste silencieuse comme avant (etablit juste la memoire).

Cas V54 (18/08/2026, signale par Justok : "les dates de precommande ne
sont pas egales aux dates de sortie -- je veux precommander des que
possible") : un produit DEJA connu qui devient commandable (en_stock
False/indetermine -> True) doit TOUJOURS alerter, meme si la confiance
n'a pas change et meme si "forte" a deja ete confirmee -- le moment qui
compte pour Justok est celui ou il peut reellement passer commande, pas
la premiere apparition de la page. Les tests de suppression "classiques"
ci-dessous fixent `en_stock: True` cote memoire pour isoler ce qu'ils
testent reellement (la logique de confiance) de cette nouvelle regle."""

from unittest.mock import Mock, patch

import requests

from alerte_precommande import _texte_precommande, detecter_nouvelles_precommandes, envoyer_telegram_precommandes


def _candidat(nom_produit="ETB 30e Anniversaire", confiance="moyenne", **kw):
    base = dict(
        nom_produit=nom_produit,
        confiance=confiance,
        raison="mots-cles presents, aucune date detectee sur la page",
        titre="ETB Pokemon 30e Anniversaire",
        url_produit="https://exemple.fr/produit",
        prix=59.99,
        en_stock=True,
    )
    base.update(kw)
    return base


def test_premiere_fois_confiance_moyenne_ne_declenche_pas_dalerte():
    memoire = {}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="moyenne")], memoire)
    assert evenements == []
    assert memoire["exemple.fr|ETB 30e Anniversaire"]["confiance"] == "moyenne"


def test_premiere_fois_confiance_forte_declenche_une_alerte_immediate():
    # V53 : signale par Justok -- playshop.fr/gamesavenue.fr avaient la
    # date de sortie confirmee des la premiere verification et n'ont
    # jamais alerte avant ce correctif.
    # V57 : l'ecriture memoire pour un evenement ALERTE est desormais
    # DIFFEREE (cf. section V57 plus bas) -- on verifie ici l'etat EN
    # ATTENTE attache a l'evenement, pas memoire[cle] directement (qui
    # n'est ecrit qu'apres confirmation d'envoi Telegram).
    memoire = {}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", raison="date de sortie attendue (2026-09-16) confirmee sur la page")], memoire)
    assert len(evenements) == 1
    assert evenements[0]["confiance"] == "forte"
    assert "exemple.fr|ETB 30e Anniversaire" not in memoire
    assert evenements[0]["_nouvel_etat"]["confiance"] == "forte"


def test_deja_vu_a_moyenne_nouveau_match_moyenne_ne_re_alerte_pas():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "moyenne", "en_stock": True}}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="moyenne")], memoire)
    assert evenements == []


def test_deja_vu_a_moyenne_nouveau_match_forte_alerte_la_confirmation():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "moyenne", "en_stock": True}}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="forte")], memoire)
    assert len(evenements) == 1
    assert evenements[0]["confiance"] == "forte"


def test_deja_vu_a_forte_nouveau_match_moyenne_ne_re_alerte_pas():
    # Une fois confirmee, un match moyenne ulterieur sur la meme page ne
    # doit jamais redeclencher (deja_confirme_mieux).
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": True}}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="moyenne")], memoire)
    assert evenements == []


def test_confiance_forte_ne_redescend_jamais_en_memoire():
    # Audit du 18/08/2026 : un cycle qui ne retrouve plus la date sur la
    # page (boutique qui retire/modifie le texte) ne doit PAS ecraser la
    # confiance "forte" deja confirmee en memoire par "moyenne" -- sinon un
    # cycle ULTERIEUR qui retrouve "forte" redeclencherait a tort une 2e
    # alerte de "confirmation" pour une date deja confirmee une 1ere fois.
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": True}}
    detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="moyenne")], memoire)
    assert memoire["exemple.fr|ETB 30e Anniversaire"]["confiance"] == "forte"


def test_flapping_forte_moyenne_forte_ne_re_alerte_pas_a_la_3e_detection():
    # Verification bout-en-bout du scenario complet : forte (memorisee) ->
    # moyenne (silencieux, ne doit pas degrader la memoire) -> forte a
    # nouveau -> toujours pas d'alerte (deja confirme la 1ere fois).
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": True}}
    evenements_cycle2 = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="moyenne")], memoire)
    assert evenements_cycle2 == []
    evenements_cycle3 = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="forte")], memoire)
    assert evenements_cycle3 == []


def test_deja_vu_a_forte_nouveau_match_forte_ne_re_alerte_pas():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": True}}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="forte")], memoire)
    assert evenements == []


# ------------------- V54 : transition hors-stock -> en-stock -------------------

def test_produit_deja_connu_devient_commandable_alerte_meme_a_confiance_identique():
    # Deja vu "forte" et HORS STOCK -- devient commandable : doit alerter,
    # meme si la confiance n'a pas change (le scenario exact signale par
    # Justok : la page etait deja la avec la date confirmee, mais pas
    # encore ouverte a la commande).
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": False}}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", en_stock=True)], memoire)
    assert len(evenements) == 1
    # V57 : ecriture differee -- memoire garde l'ANCIEN etat tant que
    # Telegram n'a pas confirme l'envoi (cf. section V57 plus bas).
    assert memoire["exemple.fr|ETB 30e Anniversaire"]["en_stock"] is False
    assert evenements[0]["_nouvel_etat"]["en_stock"] is True


def test_produit_deja_connu_stock_indetermine_devient_commandable_alerte():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": None}}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", en_stock=True)], memoire)
    assert len(evenements) == 1


def test_produit_deja_connu_reste_hors_stock_ne_re_alerte_pas():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": False}}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", en_stock=False)], memoire)
    assert evenements == []


def test_produit_deja_connu_reste_en_stock_ne_re_alerte_pas_deux_fois():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": True}}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", en_stock=True)], memoire)
    assert evenements == []


def test_premiere_fois_moyenne_en_stock_reste_silencieuse():
    # La transition de stock ne s'applique QU'a un produit deja connu --
    # une toute premiere detection "moyenne" (meme en_stock=True) reste
    # soumise a la regle habituelle (silencieuse).
    memoire = {}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="moyenne", en_stock=True)], memoire)
    assert evenements == []


# ------------------- 25/08/2026 : jamais d'alerte sans stock reel -------------------
# Demande explicite de Justok apres 3 alertes recues sans stock reel malgre
# le fix du 25/08 sur la lecture du stock (golden-poke.fr/guizettefamily.com/
# fuji-store.fr, toutes des PREMIERES detections a confiance "forte") --
# abandonne la regle V53 (alerte immediate des la 1ere date confirmee, quel
# que soit le stock) au profit de : jamais d'alerte si en_stock n'est pas True.

def test_premiere_fois_confiance_forte_mais_hors_stock_ne_declenche_pas_dalerte():
    memoire = {}
    evenements = detecter_nouvelles_precommandes(
        "golden-poke.fr", [_candidat(confiance="forte", en_stock=False)], memoire)
    assert evenements == []
    # La memoire est quand meme etablie normalement (silencieuse), pour que
    # la transition ulterieure hors-stock -> en-stock puisse etre detectee.
    assert memoire["golden-poke.fr|ETB 30e Anniversaire"]["confiance"] == "forte"
    assert memoire["golden-poke.fr|ETB 30e Anniversaire"]["en_stock"] is False


def test_premiere_fois_confiance_forte_stock_indetermine_ne_declenche_pas_dalerte():
    memoire = {}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", en_stock=None)], memoire)
    assert evenements == []


def test_produit_deja_connu_hors_stock_reste_hors_stock_ne_re_alerte_toujours_pas():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": False}}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", en_stock=False)], memoire)
    assert evenements == []


def test_produit_deja_connu_hors_stock_passe_en_stock_alerte_bien():
    # La transition hors-stock -> en-stock (V54) continue de fonctionner
    # normalement pour un produit dont la premiere detection avait ete
    # rendue silencieuse par cette nouvelle regle.
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte", "en_stock": False}}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", en_stock=True)], memoire)
    assert len(evenements) == 1


def test_plusieurs_candidats_independants_meme_boutique():
    memoire = {}
    candidats = [
        _candidat(nom_produit="ETB 30e Anniversaire", confiance="forte"),
        _candidat(nom_produit="ETB ME06 Regne Delta", confiance="moyenne"),
    ]
    evenements = detecter_nouvelles_precommandes("exemple.fr", candidats, memoire)
    assert len(evenements) == 1
    assert evenements[0]["nom_produit"] == "ETB 30e Anniversaire"
    # V57 : seul le candidat NON alertant ("moyenne", silencieux) est ecrit
    # immediatement -- celui qui alerte ("forte") reste en attente sur
    # l'evenement tant que Telegram n'a pas confirme.
    assert len(memoire) == 1
    assert "exemple.fr|ETB ME06 Regne Delta" in memoire


# ------------------- V56 : marqueur ⭐ prioritaire dans le texte Telegram -------------------

def test_texte_precommande_ajoute_une_etoile_si_prioritaire():
    texte = _texte_precommande(_candidat(domaine="exemple.fr", prioritaire=True))
    assert "⭐" in texte


def test_texte_precommande_najoute_pas_detoile_par_defaut():
    texte = _texte_precommande(_candidat(domaine="exemple.fr"))
    assert "⭐" not in texte


# ------------------- V57 : ecriture memoire differee jusqu'a confirmation Telegram -------------------
# Audit externe du 18/08/2026 (verifie contre le code reel) : avant ce
# correctif, la memoire etait ecrite par detecter_nouvelles_precommandes()
# puis sauvegardee sur disque AVANT la tentative d'envoi Telegram (cf.
# scan_precommandes.py) -- un echec Telegram survenant apres cette
# ecriture perdait l'evenement DEFINITIVEMENT (plus jamais redetecte).
# Desormais, l'etat n'est commite dans `memoire` qu'apres un envoi reussi.

def _reponse(status_code=200):
    r = Mock()
    r.status_code = status_code
    r.text = ""
    return r


def test_envoi_reussi_commite_letat_en_memoire():
    memoire = {}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", domaine="exemple.fr")], memoire)
    assert "exemple.fr|ETB 30e Anniversaire" not in memoire  # pas encore, avant l'envoi

    with patch("alerte_precommande.requests.post", return_value=_reponse(200)):
        ok = envoyer_telegram_precommandes(evenements, "123", "token", memoire)

    assert ok is True
    assert memoire["exemple.fr|ETB 30e Anniversaire"]["confiance"] == "forte"


def test_echec_telegram_ne_commite_pas_letat_en_memoire():
    # Le coeur du fix : un evenement dont l'envoi Telegram echoue ne doit
    # PAS etre memorise comme "deja alerte" -- sinon il ne serait plus
    # jamais redetecte au cycle suivant, alors qu'aucune alerte n'est
    # jamais partie.
    memoire = {}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", domaine="exemple.fr")], memoire)

    with patch("alerte_precommande.requests.post", return_value=_reponse(500)):
        ok = envoyer_telegram_precommandes(evenements, "123", "token", memoire)

    assert ok is False
    assert "exemple.fr|ETB 30e Anniversaire" not in memoire


def test_exception_reseau_ne_commite_pas_letat_en_memoire():
    memoire = {}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", domaine="exemple.fr")], memoire)

    with patch("alerte_precommande.requests.post", side_effect=requests.exceptions.Timeout("trop long")):
        ok = envoyer_telegram_precommandes(evenements, "123", "token", memoire)

    assert ok is False
    assert "exemple.fr|ETB 30e Anniversaire" not in memoire


def test_evenement_non_envoye_reste_redetectable_au_cycle_suivant():
    # Verification bout-en-bout de la garantie "au moins une fois" :
    # apres un echec Telegram, un second appel a
    # detecter_nouvelles_precommandes() avec le MEME candidat doit encore
    # produire un evenement (memoire inchangee = toujours "jamais vu").
    memoire = {}
    evenements_1 = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte")], memoire)
    with patch("alerte_precommande.requests.post", return_value=_reponse(500)):
        envoyer_telegram_precommandes(evenements_1, "123", "token", memoire)

    evenements_2 = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte")], memoire)
    assert len(evenements_2) == 1  # toujours redetecte, pas perdu


def test_plusieurs_evenements_succes_partiel_ne_commite_que_les_reussis():
    memoire = {}
    candidats = [
        _candidat(nom_produit="ETB 30e Anniversaire", confiance="forte", domaine="exemple.fr"),
        _candidat(nom_produit="ETB ME06 Regne Delta", confiance="forte", domaine="exemple.fr"),
    ]
    evenements = detecter_nouvelles_precommandes("exemple.fr", candidats, memoire)
    assert len(evenements) == 2

    with patch("alerte_precommande.requests.post", side_effect=[_reponse(200), _reponse(500)]):
        ok = envoyer_telegram_precommandes(evenements, "123", "token", memoire)

    assert ok is False  # au moins un echec -> ok global a False
    assert "exemple.fr|ETB 30e Anniversaire" in memoire      # succes -> commite
    assert "exemple.fr|ETB ME06 Regne Delta" not in memoire  # echec -> pas commite


def test_sans_memoire_fournie_fonctionne_toujours_comme_avant():
    # memoire=None (retro-compatibilite, ex. appel manuel sans dedup) --
    # ne doit ni planter ni exiger le parametre.
    evenement = _candidat(confiance="forte", domaine="exemple.fr")
    with patch("alerte_precommande.requests.post", return_value=_reponse(200)):
        ok = envoyer_telegram_precommandes([evenement], "123", "token")
    assert ok is True
