"""
Echappement HTML minimal pour les messages Telegram (parse_mode="HTML").

Partage par les 3 modules d'alerte (bonne_affaire_shopify.py, alerte_stock.py,
alerte_precommande.py) -- fonctions identiques dupliquees dans les 3 avant
factorisation ici le 11/08/2026 (audit de sante du projet).
"""


def echapper_html(texte) -> str:
    return str(texte).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def echapper_url_html(url: str) -> str:
    # V51 (audit externe du 17/08/2026) : aligne sur echapper_html --
    # echapper aussi < et > (invalides dans une URL, mais mieux vaut les
    # neutraliser explicitement que de laisser une URL malformee casser
    # l'attribut href="..." ou le parsing HTML de Telegram).
    return str(url).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
