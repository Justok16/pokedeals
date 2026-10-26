#!/usr/bin/env python3
"""Modèles de signature électronique DocuSeal (26/10/2026), décision de l'utilisateur du 26/10 :
« Signature : électronique par email (DocuSeal, gratuit) ».

Produit les 4 PDF génériques à charger UNE fois dans DocuSeal (fiche 72 § 6), avec les mêmes textes que le kit client
(outils/kit_client.py) ; seules les données qui changent d'un client à l'autre sont remplacées par des cadres vides
où l'on place les champs DocuSeal (rôles « DIG16 » et « Client ») :
  1. Devis et bon de commande + conditions générales de vente (un seul envoi : signer le devis vaut acceptation des CGV) ;
  2. Accord de réalisation gracieuse (sites offerts) ;
  3. Procès-verbal de réception du site ;
  4. Remise des fichiers.
Pour chaque modèle : le PDF, une image annotée (où placer chaque champ, avec son nom exact) et la liste des champs
(LISEZMOI-champs.md). Les noms de champs sont ceux qu'utilisera send_documents pour pré-remplir.

L'identité du prestataire vient d'un fichier JSON privé ; les PDF sont écrits hors du dépôt (refusé sinon), car ils
contiennent l'identité de l'entrepreneur. Aucun PDF ni aucune image produits ici ne doivent être ajoutés au dépôt.
Usage : python3 outils/modeles_docuseal.py --prestataire <prive/dig16-prestataire.json> --sortie <dossier privé>
"""
import argparse
import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import documents_client as dc
import kit_client as kc
from accord_gracieux import accord_html

# Chaque cadre a une couleur de fond unique (bleu de 120 à 200) : on retrouve sa position exacte dans le PDF rendu,
# sans dépendre de la mise en page, pour dessiner l'image annotée.
STYLE = ("<style>.zone{display:inline-block;vertical-align:middle;border:.25mm dashed #b39a6b;border-radius:1.2mm;"
         "box-sizing:border-box}.zone-bloc{display:block;margin:1.2mm 0}</style>")


class Zones:
    def __init__(self):
        self.liste = []  # (nom, type, rôle, remarque, couleur)

    def __call__(self, nom, typ, role, larg="45mm", haut="5.5mm", bloc=False, remarque=""):
        i = len(self.liste)
        couleur = (255, 251, 120 + 2 * i)
        self.liste.append((nom, typ, role, remarque, couleur))
        cls = "zone zone-bloc" if bloc else "zone"
        return (f'<span class="{cls}" style="width:{larg};height:{haut};'
                f'background:rgb{couleur}"></span>')


def sans_sentinelle(html):
    reste = re.findall(r"☐ (?:accepte|refuse)|⟦[^⟧]+⟧|\[[A-Z_]{3,}\]|\[Prénom Nom\]|\[Adresse\]|\[téléphone\]", html)
    if reste:
        sys.exit(f"cadres non remplacés : {sorted(set(reste))}")
    return html.replace("</head>", STYLE + "</head>", 1)


def signatures(z, html, gauche, droite, role_g, role_d):
    """Remplace le bloc .sign (2 cadres) par 2 cadres avec signature et date."""
    nouveau = (f'<div class="sign"><div>{gauche}<br>{z("Signature " + role_g, "signature", role_g, "70mm", "13mm", True)}'
               f'Date : {z("Date " + role_g, "date", role_g, "32mm", "5mm")}</div>'
               f'<div>{droite}<br>{z("Signature " + role_d, "signature", role_d, "70mm", "13mm", True)}'
               f'Date : {z("Date " + role_d, "date", role_d, "32mm", "5mm")}</div></div>')
    html, n = re.subn(r'<div class="sign">.*?</div></div>', nouveau, html, count=1, flags=re.DOTALL)
    assert n == 1, "bloc de signature introuvable"
    return html.replace(".sign div{border:.25mm solid var(--trait);border-radius:2.5mm;height:26mm;",
                        ".sign div{border:.25mm solid var(--trait);border-radius:2.5mm;min-height:26mm;", 1)


def devis(P):
    z = Zones()
    s = dc.prestataire_html(dc.lire(os.path.join(dc.SUPPORTS, "modele-devis.html")), P)
    s = s.replace("N° [AAAA-NNN] · Date : [jj/mm/aaaa]",
                  f'N° {z("Numéro du devis", "texte", "DIG16", "30mm", "5mm")} · Date : '
                  f'{z("Date du devis", "texte", "DIG16", "28mm", "5mm")}', 1)
    s = s.replace('<div class="champ"></div><div class="champ"></div><span class="petit">Nom de l’entreprise, adresse, SIREN</span>',
                  z("Client", "texte (plusieurs lignes)", "DIG16", "100%", "17mm", True,
                    "nom de l’entreprise, représentant, adresse, SIREN"), 1)
    s = s.replace("<th>Formule (cocher)</th>", "<th>Formule</th>", 1).replace("☐ hébergement et suivi en option", "hébergement et suivi en option", 1)
    s = s.replace("Un mois offert : ☐ Essentiel 539 € · ☐ Visibilité 869 €", "Un mois offert : Essentiel 539 € · Visibilité 869 €", 1)
    s = re.sub(r"<td>☐ ", "<td>", s)
    s = s.replace("</table>\n<p><b>Création offerte</b>",
                  f'</table>\n<p><b>Formule retenue</b> : {z("Formule retenue", "texte", "DIG16", "125mm", "5.5mm", remarque="formule, prix et option éventuelle")}</p>\n<p><b>Création offerte</b>', 1)
    s = s.replace("<b>[date convenue ensemble]</b>", z("Mise en ligne prévue", "texte", "DIG16", "34mm", "5mm"), 1)
    s = s.replace('<p class="petit">Signer ce devis vaut commande et acceptation des conditions générales de vente jointes.</p>',
                  f'<p><b>Conditions particulières</b> : {z("Conditions particulières", "texte (plusieurs lignes)", "DIG16", "100%", "11mm", True, "« Aucune » ou le texte du site offert")}</p>'
                  '<p class="petit">Signer ce devis vaut commande et acceptation des conditions générales de vente jointes '
                  '(pages suivantes).</p>', 1)
    s = signatures(z, s, "Bon pour accord : signature du client", "Pour DIG16", "Client", "DIG16")
    s = s.replace("<p>☐ Je demande que la prestation commence",
                  f'<p>{z("Exécution immédiate", "case à cocher", "Client", "3.6mm", "3.6mm", remarque="facultative, cochée par le client")} Je demande que la prestation commence', 1)
    return sans_sentinelle(s), z


def accord(P):
    z = Zones()
    C = {k: f"⟦C.{k}⟧" for k in ("nom_commercial", "dirigeant", "forme", "siren", "adresse", "denomination")}
    D = {k: f"⟦D.{k}⟧" for k in ("adresse_provisoire", "annee", "date", "date_longue", "formule", "logo_origine",
                                  "mise_en_ligne", "numero_devis", "pages_site")}
    D["offert"] = True
    s = accord_html(P, C, D, dc.lire(os.path.join(dc.SUPPORTS, "modele-devis.html")))
    s = s.replace("Site de ⟦C.nom_commercial⟧ · Version du ⟦D.date_longue⟧",
                  f'Site du bénéficiaire · Version du {z("Date de version", "texte", "DIG16", "34mm", "5mm")}', 1)
    s, n = re.subn(r"⟦C\.dirigeant⟧, ⟦C\.forme⟧, nom commercial ⟦C\.nom_commercial⟧<br>SIREN <span class=\"nowrap\">⟦C\.siren⟧</span><br>⟦C\.adresse⟧",
                   z("Bénéficiaire", "texte (plusieurs lignes)", "DIG16", "100%", "15mm", True,
                     "dirigeant, forme, nom commercial, SIREN, adresse"), s, count=1)
    assert n == 1, "bloc bénéficiaire introuvable"
    s = s.replace("DIG16 réalise le site internet de ⟦C.nom_commercial⟧ et l’offre au bénéficiaire. ⟦D.pages_site⟧",
                  "DIG16 réalise le site internet du bénéficiaire et le lui offre. "
                  + z("Pages du site", "texte (plusieurs lignes)", "DIG16", "100%", "11mm", True, "pages et contenu du site"), 1)
    s = re.sub(r'<span class="nowrap">⟦D\.adresse_provisoire⟧</span>|⟦D\.adresse_provisoire⟧',
               z("Adresse provisoire", "texte", "DIG16", "70mm", "5mm"), s, count=1)
    s = s.replace("le logo redessiné d’après ⟦D.logo_origine⟧",
                  "le logo redessiné d’après " + z("Origine du logo", "texte", "DIG16", "60mm", "5mm",
                                                   remarque="ex. : le fichier fourni par le bénéficiaire"), 1)
    s = s.replace("des droits sur le logo figurant sur ⟦D.logo_origine⟧", "des droits sur ce logo", 1)
    s, n = re.subn(r"☐(\s|&nbsp;|\u00a0)accepte ☐(\s|&nbsp;|\u00a0)refuse",
                   z("Exemple accepté", "case à cocher", "Client", "3.6mm", "3.6mm", remarque="article 9 : une seule des deux cases")
                   + "\u00a0accepte " + z("Exemple refusé", "case à cocher", "Client", "3.6mm", "3.6mm") + "\u00a0refuse", s, count=1)
    assert n == 1, "cases de l'article 9 introuvables"
    s = re.sub(r'<p class="fait">.*?</p>', '<p class="fait">Fait par signature électronique, à la date indiquée sous chaque signature ; '
               'chaque partie en reçoit un exemplaire.</p>', s, count=1, flags=re.DOTALL)
    nouveau = (f'<div class="sign"><div>Pour DIG16<br>{dc.e(P["nom"])}<br>'
               f'{z("Signature DIG16", "signature", "DIG16", "70mm", "13mm", True)}Date : {z("Date DIG16", "date", "DIG16", "32mm", "5mm")}</div>'
               f'<div>Pour le bénéficiaire<br>{z("Signataire", "texte", "DIG16", "60mm", "5mm", remarque="nom du dirigeant")}<br>'
               f'{z("Signature Client", "signature", "Client", "70mm", "13mm", True)}Date : {z("Date Client", "date", "Client", "32mm", "5mm")}</div></div>')
    s, n = re.subn(r'<div class="sign">.*?</div></div>', nouveau, s, count=1, flags=re.DOTALL)
    assert n == 1, "bloc de signature de l'accord introuvable"
    return sans_sentinelle(s), z


def entete(z, s, P, ref=True):
    s = dc.prestataire_html(s, P)
    if ref:
        s = s.replace("[REFERENCE]", "Référence : " + z("Référence", "texte", "DIG16", "90mm", "5mm",
                                                         remarque="site, n° de devis"), 1)
    return s.replace("[CLIENT]", z("Client", "texte (plusieurs lignes)", "DIG16", "100%", "15mm", True,
                                   "nom de l’entreprise, adresse, SIREN"), 1)


def pv(P):
    z = Zones()
    s = entete(z, kc.modele("pv-reception"), P)
    s = s.replace("<b>[ADRESSE_SITE]</b>", z("Adresse du site", "texte", "DIG16", "70mm", "5mm"), 1)
    s = s.replace("<table><tr><th>Page</th><th>Contenu</th></tr>[PAGES]</table>",
                  z("Pages livrées", "texte (plusieurs lignes)", "DIG16", "100%", "20mm", True, "page par page, ce qui est livré"), 1)
    controles = kc.pv(P, {"nom_commercial": "x", "denomination": "x", "adresse": "x", "siren": "x"},
                      {"numero_devis": "x", "formule": "Essentiel", "date": "x", "pages_site": "x"})
    liste = re.search(r'<ul class="ok liste">(.*?)</ul>', controles, re.DOTALL).group(1)
    s = s.replace("[CONTROLES]", liste, 1)
    s = s.replace('<div class="champ"></div><div class="champ"></div><div class="champ"></div>',
                  z("Réserves du client", "texte (plusieurs lignes)", "Client", "100%", "18mm", True,
                    "facultatif : laissé vide s’il n’y a aucune réserve"), 1)
    s = s.replace("[PAIEMENT]", z("Paiement", "texte (plusieurs lignes)", "DIG16", "100%", "9mm", True,
                                  "phrase de paiement selon la formule ou « Site offert : aucun paiement. »"), 1)
    s = signatures(z, s, "« Site reçu et accepté » : signature du client", "Pour DIG16", "Client", "DIG16")
    return sans_sentinelle(s), z


def remise(P):
    z = Zones()
    s = entete(z, kc.modele("remise-fichiers"), P)
    s = s.replace("[ADRESSE_SITE]", z("Adresse du site", "texte", "DIG16", "60mm", "5mm"), 1)
    s = s.replace("[DATE_REMISE]", z("Date de remise", "texte", "DIG16", "34mm", "5mm"), 1)
    contenu = [("Pages du site", "toutes les pages du site, en HTML"),
               ("Images", "photos et logo fournis par le client, images d’illustration (WebP), avec la liste de leurs sources"),
               ("Polices d’écriture", "fichiers de polices inclus (aucun appel à un service extérieur)"),
               ("Fichiers techniques", "feuilles de style, scripts, plan du site, robots.txt, réglages de sécurité et de cache"),
               ("Archive", "un fichier ZIP de l’ensemble, remis par lien de téléchargement sécurisé")]
    s = s.replace("[CONTENU]", "".join(f"<tr><td>{dc.e(a)}</td><td>{dc.e(b)}</td></tr>" for a, b in contenu), 1)
    s = s.replace("[DROITS]", z("Droits", "texte (plusieurs lignes)", "DIG16", "100%", "16mm", True,
                                "droits cédés (site payé) ou non exclusifs (site offert)"), 1)
    s = signatures(z, s, "« Fichiers reçus » : signature du client", "Pour DIG16", "Client", "DIG16")
    return sans_sentinelle(s), z


def annoter(pdf, zones, prefixe):
    """Rend chaque page en PNG, retrouve chaque cadre par sa couleur et écrit son nom dessus."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    subprocess.run(["pdftoppm", "-r", "110", "-png", pdf, prefixe], check=True)
    pages = sorted(f for f in os.listdir(os.path.dirname(prefixe)) if f.startswith(os.path.basename(prefixe) + "-") and f.endswith(".png"))
    trouves, sorties = set(), []
    try:
        police = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    except OSError:
        police = ImageFont.load_default()
    for nom_png in pages:
        chemin = os.path.join(os.path.dirname(prefixe), nom_png)
        im = Image.open(chemin).convert("RGB")
        a = np.asarray(im)
        d = ImageDraw.Draw(im)
        for nom, typ, role, _rem, c in zones.liste:
            m = (a[..., 0] == c[0]) & (a[..., 1] == c[1]) & (a[..., 2] == c[2])
            if m.sum() < 6:
                continue
            ys, xs = np.nonzero(m)
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
            trouves.add(nom)
            couleur = (200, 30, 30) if role == "Client" else (20, 90, 190)
            d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=couleur, width=3)
            etiquette = f"{nom} ({role})"
            tw = d.textlength(etiquette, font=police)
            ty = y0 - 20 if y0 > 24 else y1 + 4
            d.rectangle([x0 - 2, ty - 1, x0 + tw + 6, ty + 18], fill=couleur)
            d.text((x0 + 2, ty), etiquette, fill="white", font=police)
        im.save(chemin)
        sorties.append(chemin)
    manque = [n for n, *_ in zones.liste if n not in trouves]
    if manque:
        sys.exit(f"cadres non retrouvés dans {pdf} : {manque}")
    return sorties


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--prestataire", required=True)
    a.add_argument("--sortie", required=True)
    o = a.parse_args()
    sortie = os.path.abspath(o.sortie)
    if sortie.startswith(dc.DEPOT):
        sys.exit("refusé : les modèles contiennent l’identité de l’entrepreneur, écrire hors du dépôt")
    os.makedirs(sortie, exist_ok=True)
    P = json.loads(dc.lire(o.prestataire))
    modeles = [("1-DocuSeal-Devis-et-CGV", devis(P)), ("2-DocuSeal-Accord-site-offert", accord(P)),
               ("3-DocuSeal-PV-de-reception", pv(P)), ("4-DocuSeal-Remise-des-fichiers", remise(P))]
    dc.rendre([(f"{nom}-seul.pdf" if nom.startswith("1-") else f"{nom}.pdf", html) for nom, (html, _) in modeles]
              + [("CGV.pdf", dc.cgv(P))], sortie)
    subprocess.run(["pdfunite", os.path.join(sortie, "1-DocuSeal-Devis-et-CGV-seul.pdf"), os.path.join(sortie, "CGV.pdf"),
                    os.path.join(sortie, "1-DocuSeal-Devis-et-CGV.pdf")], check=True)
    for f in ("1-DocuSeal-Devis-et-CGV-seul.pdf", "CGV.pdf"):
        os.remove(os.path.join(sortie, f))
    apercus = os.path.join(sortie, "apercus")
    os.makedirs(apercus, exist_ok=True)
    lignes = ["# Champs à placer dans DocuSeal (une fois par modèle)", "",
              ("Rôles : **DIG16** (bleu sur les images : pré-rempli par Claude à chaque envoi) et **Client** (rouge : rempli "
               "ou signé par le client). Le nom de chaque champ doit être recopié **exactement** : c’est lui qui permet le "
               "pré-remplissage automatique."), ""]
    for nom, (_, z) in modeles:
        annoter(os.path.join(sortie, nom + ".pdf"), z, os.path.join(apercus, nom))
        lignes += [f"## {nom}", "", "| Champ (nom exact) | Type DocuSeal | Rôle | Remarque |", "|---|---|---|---|"]
        lignes += [f"| {n} | {t} | {r} | {rem} |" for n, t, r, rem, _ in z.liste] + [""]
    with open(os.path.join(sortie, "LISEZMOI-champs.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    print("écrit :", sortie)


if __name__ == "__main__":
    main()
