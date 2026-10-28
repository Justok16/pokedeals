"""Rend un PDF remplissable au clavier (demande de l'utilisateur du 28/10 : « taper au clavier dessus pendant l'appel »).

Ajoute un champ texte sur chaque blanc « ____ », une case à cocher sur chaque « ☐ », et une grande zone de saisie
sous chaque étiquette de cadre de notes donnée en option (jusqu'au bas de la page).
Usage : python3 outils/pdf_remplissable.py entree.pdf sortie.pdf [--notes "Étiquette 1" "Étiquette 2" …]
Les fiches et leurs données restent privées : entrée et sortie hors du dépôt.
"""
import argparse
import pymupdf


def rendre_remplissable(entree, sortie, notes=()):
    d = pymupdf.open(entree)
    n = 0
    for num, page in enumerate(d):
        W, H = page.rect.width, page.rect.height
        for x0, y0, x1, y1, mot, *_ in page.get_text("words"):
            w = pymupdf.Widget()
            if "☐" in mot:
                w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
                w.rect = pymupdf.Rect(x0 - .5, y0 + .5, x0 + (y1 - y0) - .5, y1 + .5)
                w.field_value = False
            elif mot.strip(":.,;)").startswith("___"):
                w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
                w.rect = pymupdf.Rect(x0, y0 - 1.5, x1, y1 + 1)
                w.text_fontsize = 0  # taille automatique
                w.fill_color = (1, 1, 1)
            else:
                continue
            w.field_name = f"champ_{num}_{n}"
            page.add_widget(w)
            n += 1
        for etiquette in notes:
            for r in page.search_for(etiquette):
                w = pymupdf.Widget()
                w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
                w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
                w.field_name = f"notes_{num}_{n}"
                w.rect = pymupdf.Rect(r.x0 - 4, r.y1 + 3, W - 46, H - 40)
                w.text_fontsize = 10
                page.add_widget(w)
                n += 1
    d.save(sortie, garbage=3, deflate=True)
    return n


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("entree")
    a.add_argument("sortie")
    a.add_argument("--notes", nargs="*", default=[])
    o = a.parse_args()
    print("champs ajoutés :", rendre_remplissable(o.entree, o.sortie, o.notes))
