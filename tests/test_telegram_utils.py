"""Tests de non-regression pour telegram_utils.py (echapper_html /
echapper_url_html) -- premiere couverture dediee (audit du 18/08/2026),
partagees par bonne_affaire_shopify.py, alerte_stock.py, alerte_precommande.py
et radar_prix_bas.py."""

from telegram_utils import echapper_html, echapper_url_html


def test_echapper_html_echappe_les_3_caracteres_speciaux():
    assert echapper_html('A & B <script> "test"') == 'A &amp; B &lt;script&gt; "test"'


def test_echapper_html_convertit_en_chaine():
    assert echapper_html(123) == "123"


def test_echapper_url_html_echappe_lesperluette():
    assert echapper_url_html("https://ex.fr/p?a=1&b=2") == "https://ex.fr/p?a=1&amp;b=2"


def test_echapper_url_html_echappe_les_chevrons():
    assert echapper_url_html('https://ex.fr/p?x=<script>') == "https://ex.fr/p?x=&lt;script&gt;"


def test_echapper_url_html_echappe_le_guillemet_double():
    # V59 : cette fonction n'est utilisee QUE dans un attribut href="..." --
    # un guillemet non echappe fermerait prematurement l'attribut et
    # casserait le HTML du message envoye a Telegram (rejet 400).
    url = 'https://ex.fr/p?x="onmouseover=alert(1)'
    resultat = echapper_url_html(url)
    assert '"' not in resultat
    assert "&quot;" in resultat


def test_echapper_url_html_produit_un_attribut_href_valide():
    url = 'https://ex.fr/p?x="><b>'
    html = f'<a href="{echapper_url_html(url)}">Voir</a>'
    # Le guillemet ne doit jamais apparaitre en dehors des 2 guillemets
    # delimitant l'attribut href.
    assert html.count('"') == 2
