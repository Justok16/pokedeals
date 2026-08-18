"""Tests de non-regression pour detecter_nouvelles_precommandes()
(alerte_precommande.py) -- logique de suppression/declenchement d'alerte a
3 etats (premiere fois / deja vu a ce niveau / deja confirme mieux),
jusqu'ici sans aucune couverture de test (audit du 18/08/2026).

Cas V53 (18/08/2026, signale par Justok) : une premiere detection deja a
confiance "forte" (date de sortie confirmee sur la page) doit alerter
IMMEDIATEMENT, contrairement a une premiere detection "moyenne" (mots-cles
seuls) qui reste silencieuse comme avant (etablit juste la memoire)."""

from alerte_precommande import detecter_nouvelles_precommandes


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
    memoire = {}
    evenements = detecter_nouvelles_precommandes(
        "exemple.fr", [_candidat(confiance="forte", raison="date de sortie attendue (2026-09-16) confirmee sur la page")], memoire)
    assert len(evenements) == 1
    assert evenements[0]["confiance"] == "forte"
    assert memoire["exemple.fr|ETB 30e Anniversaire"]["confiance"] == "forte"


def test_deja_vu_a_moyenne_nouveau_match_moyenne_ne_re_alerte_pas():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "moyenne"}}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="moyenne")], memoire)
    assert evenements == []


def test_deja_vu_a_moyenne_nouveau_match_forte_alerte_la_confirmation():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "moyenne"}}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="forte")], memoire)
    assert len(evenements) == 1
    assert evenements[0]["confiance"] == "forte"


def test_deja_vu_a_forte_nouveau_match_moyenne_ne_re_alerte_pas():
    # Une fois confirmee, un match moyenne ulterieur sur la meme page ne
    # doit jamais redeclencher (deja_confirme_mieux).
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte"}}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="moyenne")], memoire)
    assert evenements == []


def test_deja_vu_a_forte_nouveau_match_forte_ne_re_alerte_pas():
    memoire = {"exemple.fr|ETB 30e Anniversaire": {"confiance": "forte"}}
    evenements = detecter_nouvelles_precommandes("exemple.fr", [_candidat(confiance="forte")], memoire)
    assert evenements == []


def test_plusieurs_candidats_independants_meme_boutique():
    memoire = {}
    candidats = [
        _candidat(nom_produit="ETB 30e Anniversaire", confiance="forte"),
        _candidat(nom_produit="ETB ME06 Regne Delta", confiance="moyenne"),
    ]
    evenements = detecter_nouvelles_precommandes("exemple.fr", candidats, memoire)
    assert len(evenements) == 1
    assert evenements[0]["nom_produit"] == "ETB 30e Anniversaire"
    assert len(memoire) == 2
