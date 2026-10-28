"""Rend un PDF remplissable au clavier (demande de l'utilisateur du 28/10 : « taper au clavier dessus pendant l'appel »).

Ajoute un champ texte sur chaque blanc « ____ », une case à cocher sur chaque « ☐ », et une grande zone de saisie
sous chaque étiquette de cadre de notes donnée en option (jusqu'au bas de la page). Avec --lignes : un champ texte
au-dessus de chaque ligne d'écriture tracée (trait horizontal fin de plus de 120 points, ex. questionnaire de lancement).
Usage : python3 outils/pdf_remplissable.py entree.pdf sortie.pdf [--notes "Étiquette 1" …] [--lignes]
Les fiches et leurs données restent privées : entrée et sortie hors du dépôt.
"""
import argparse
import pymupdf


def rendre_remplissable(entree, sortie, notes=(), lignes=False):
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
        if lignes:
            vus = set()
            for dessin in page.get_drawings():
                r = dessin["rect"]
                zone = pymupdf.Rect(r.x0, r.y0 - 15, r.x1, r.y0 - .5)
                if r.width > 120 and r.height < 1.5 and (round(r.x0), round(r.y0)) not in vus:
                    vus.add((round(r.x0), round(r.y0)))
                    if page.get_text("text", clip=zone).strip():
                        continue  # ligne déjà remplie ou étiquette au-dessus : on n'y touche pas
                    w = pymupdf.Widget()
                    w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
                    w.field_name = f"ligne_{num}_{n}"
                    w.rect = zone
                    w.text_fontsize = 0
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
    a.add_argument("--lignes", action="store_true")
    o = a.parse_args()
    print("champs ajoutés :", rendre_remplissable(o.entree, o.sortie, o.notes, o.lignes))
