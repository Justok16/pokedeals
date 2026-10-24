"""Remplir un formulaire PDF (cerfa, dossier d'organisme, contrat) sans le réécrire à la main (24/10/2026).

Demande de l'utilisateur du 24/10 : « pouvoir remplir directement des fichiers PDF » lors des démarches et entretiens.

Deux cas :
1. PDF « remplissable » (cases à remplir intégrées, cas de la plupart des cerfa) : on remplit les champs par leur nom.
2. PDF « plat » (scan, imprimé) : on écrit le texte par-dessus, à des positions données (surimpression).

Usage (Python 3.13 : /usr/bin/python3.13, où pypdf et reportlab sont installés) :
  python3.13 remplir_pdf.py champs  formulaire.pdf                 → liste les cases (nom, type, choix, page, libellé)
  python3.13 remplir_pdf.py remplir formulaire.pdf valeurs.json sortie.pdf
        valeurs.json = {"nom de la case": "texte", "case à cocher": true, ...}
  python3.13 remplir_pdf.py ecrire  formulaire.pdf textes.json sortie.pdf
        textes.json = [{"page": 1, "x": 120, "y": 700, "texte": "…", "taille": 10}, ...]  (points, origine en bas à gauche)

Le PDF rempli reste modifiable (les cases ne sont pas figées) : l'utilisateur peut corriger avant de signer.
VIE PRIVÉE : les valeurs (identité, adresse, SIREN…) viennent des fichiers privés (scratchpad/prive) et le PDF rempli
va dans le scratchpad ou le Drive « Dig », JAMAIS dans le dépôt. Contrôle 44 avant tout envoi.
"""

import io
import json
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject


def champs(chemin):
    lecteur = PdfReader(chemin)
    trouves = 0
    for num, page in enumerate(lecteur.pages, 1):
        for annot in page.get("/Annots") or []:
            a = annot.get_object()
            if a.get("/Subtype") != "/Widget":
                continue
            parent = a.get("/Parent")
            nom = a.get("/T") or (parent.get_object().get("/T") if parent else None)
            if nom is None:
                continue
            source = a if a.get("/FT") else (parent.get_object() if parent else a)
            genre = {"/Tx": "texte", "/Btn": "case", "/Ch": "liste", "/Sig": "signature"}.get(source.get("/FT"), "?")
            libelle = a.get("/TU") or source.get("/TU") or ""
            choix = ""
            if genre == "case":
                etats = [str(k) for k in (a.get("/AP", {}).get("/N", {}) or {}).keys() if str(k) != "/Off"]
                choix = " valeur=" + ",".join(etats)
            elif genre == "liste":
                choix = " choix=" + ",".join(str(o) for o in source.get("/Opt", []))
            x0, y0 = (round(float(v)) for v in a.get("/Rect", [0, 0])[:2])
            print(f"p{num} ({x0},{y0}) [{genre}] {nom!s}{choix}  {libelle!s}")
            trouves += 1
    if not trouves:
        print("Aucune case à remplir : PDF « plat ». Utiliser la commande « ecrire » (surimpression).")
    return trouves


def remplir(chemin, valeurs_json, sortie):
    valeurs = json.load(open(valeurs_json, encoding="utf-8"))
    lecteur = PdfReader(chemin)
    redacteur = PdfWriter(clone_from=lecteur)
    connus = set((lecteur.get_fields() or {}).keys())  # noms complets…
    for page in lecteur.pages:  # … et noms courts des cases (/T), ceux qu'affiche « champs »
        for annot in page.get("/Annots") or []:
            a = annot.get_object()
            parent = a.get("/Parent")
            nom = a.get("/T") or (parent.get_object().get("/T") if parent else None)
            if nom is not None:
                connus.add(str(nom))
    inconnus = [k for k in valeurs if k not in connus]
    if inconnus:
        sys.exit(f"Cases inconnues (vérifier avec « champs ») : {inconnus}")
    for page in redacteur.pages:
        a_remplir = {}
        for annot in page.get("/Annots") or []:
            a = annot.get_object()
            parent = a.get("/Parent")
            nom = a.get("/T") or (parent.get_object().get("/T") if parent else None)
            if nom in valeurs:
                v = valeurs[nom]
                if isinstance(v, bool):
                    etats = [k for k in (a.get("/AP", {}).get("/N", {}) or {}).keys() if str(k) != "/Off"]
                    v = str(etats[0]) if (v and etats) else "/Off"
                a_remplir[nom] = v
        if a_remplir:
            redacteur.update_page_form_field_values(page, a_remplir, auto_regenerate=False)
    redacteur.set_need_appearances_writer(True)  # les lecteurs redessinent les cases : texte visible partout
    with open(sortie, "wb") as f:
        redacteur.write(f)
    print(f"{len(valeurs)} case(s) remplie(s) → {sortie}")


def ecrire(chemin, textes_json, sortie):
    from reportlab.pdfgen import canvas

    textes = json.load(open(textes_json, encoding="utf-8"))
    lecteur = PdfReader(chemin)
    redacteur = PdfWriter(clone_from=lecteur)
    for num, page in enumerate(redacteur.pages, 1):
        a_poser = [t for t in textes if t.get("page", 1) == num]
        if not a_poser:
            continue
        largeur, hauteur = float(page.mediabox.width), float(page.mediabox.height)
        tampon = io.BytesIO()
        c = canvas.Canvas(tampon, pagesize=(largeur, hauteur))
        for t in a_poser:
            c.setFont("Helvetica", t.get("taille", 10))
            c.drawString(t["x"], t["y"], str(t["texte"]))
        c.save()
        tampon.seek(0)
        page.merge_page(PdfReader(tampon).pages[0])
    with open(sortie, "wb") as f:
        redacteur.write(f)
    print(f"{len(textes)} texte(s) posé(s) → {sortie}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("champs", "remplir", "ecrire"):
        sys.exit(__doc__)
    if sys.argv[1] == "champs":
        champs(sys.argv[2])
    elif len(sys.argv) < 5:
        sys.exit(__doc__)
    elif sys.argv[1] == "remplir":
        remplir(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        ecrire(sys.argv[2], sys.argv[3], sys.argv[4])
