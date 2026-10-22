#!/usr/bin/env python3
"""Contrat d'assistance administrative et mandat de facturation → PDF signable (DocuSeal).

Source unique : supports/service-devis-factures/mandat-de-facturation.md (partie entre les deux « --- »).
Les champs à remplir ([●], [Prénom NOM]…) deviennent des balises DocuSeal {{Nom;role=…;type=…}} :
DocuSeal les transforme en champs à remplir et à signer. Aucune donnée personnelle dans ce fichier.

Usage : python3 outils/contrat_mandat_pdf.py  → supports/service-devis-factures/DIG16-contrat-mandat-facturation.pdf
"""
import os
import re
import sys

import markdown

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "marque"))
from charte_documents import BASE, COUVERTURE, POLICES, attendre_polices, bandeau  # noqa: E402

DOSSIER = os.path.normpath(os.path.join(ICI, "..", "supports", "service-devis-factures"))
SOURCE = os.path.join(DOSSIER, "mandat-de-facturation.md")
HTML = os.path.join(DOSSIER, "..", "DIG16-contrat-mandat-facturation.html")  # dans supports/ : images ../site-dig/
PDF = os.path.join(DOSSIER, "DIG16-contrat-mandat-facturation.pdf")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


def tag(nom, role, type_="text"):
    return f"{{{{{nom};role={role};type={type_}}}}}"


# Remplacements dans l'ordre d'apparition (chaque motif n'est remplacé qu'une fois).
REMPLACEMENTS = [
    ("[Prénom NOM], entrepreneur individuel", tag("Nom DIG16", "DIG16") + ", entrepreneur individuel"),
    ("SIREN [●], [adresse], ci-après « DIG16 »", f"SIREN {tag('SIREN DIG16', 'DIG16')}, {tag('Adresse DIG16', 'DIG16')}, ci-après « DIG16 »"),
    ("[Dénomination ou Prénom NOM], [forme : entrepreneur individuel / société], SIREN [●], [adresse du siège],\nreprésentée par [Prénom NOM, qualité]",
     f"{tag('Nom du client', 'Client')}, {tag('Forme juridique', 'Client')}, SIREN {tag('SIREN du client', 'Client')}, {tag('Adresse du client', 'Client')},\nreprésentée par {tag('Représentant et qualité', 'Client')}"),
    ("délai de [2] jours ouvrés", "délai de 2 jours ouvrés"),
    ("[messagerie convenue : SMS, WhatsApp, email]", tag("Messagerie convenue", "Client")),
    ("J+[3]", "J+3"), ("J+[15]", "J+15"), ("J+[30]", "J+30"),
    ("[du lundi au vendredi, 9 h à 18 h]", "du lundi au vendredi, 9 h à 18 h"),
    ("urgences : [●]", "urgences : " + tag("Contact urgences", "DIG16")),
    ("devis n° [●] du [date] : [montant] € par mois, [TVA non applicable, article 293 B du CGI /\nTVA au taux de ●]",
     f"devis n° {tag('Numéro du devis', 'DIG16')} du {tag('Date du devis', 'DIG16', 'date')} : {tag('Montant mensuel', 'DIG16')} € par mois, TVA non applicable, article 293 B du CGI"),
    ("pénalités au taux de [●]", "pénalités au taux prévu par les conditions générales de vente de DIG16"),
    ("à compter du [date], résiliable", f"à compter du {tag('Date de début', 'DIG16', 'date')}, résiliable"),
    ("préavis de [30] jours", "préavis de 30 jours"), ("dans les [30] jours", "dans les 30 jours"),
    ("[assureur, n° de contrat]", tag("Assureur et numéro de contrat", "DIG16")),
    ("des [12] derniers mois", "des 12 derniers mois"),
    ("Fait à [●], le [●], en deux exemplaires.", f"Fait à {tag('Lieu', 'DIG16')}, le {tag('Date de signature', 'DIG16', 'date')}, en deux exemplaires."),
    ("Le Client : [signature, « lu et approuvé, bon pour mandat »] — DIG16 : [signature]",
     f"Le Client (lu et approuvé, bon pour mandat) : {tag('Signature du client', 'Client', 'signature')}\n\nDIG16 : {tag('Signature DIG16', 'DIG16', 'signature')}"),
]

ANNEXE = [
    "Modèle de devis et de facture", "Grille de prix", "TVA et régime", "Numérotation en cours", "Conditions de paiement",
    "Assurance professionnelle", "Mode d'acceptation", "Calendrier des relances", "Expert-comptable", "Canal d'envoi",
    "Plateforme de facturation électronique",
]

CSS = BASE + COUVERTURE + """@page{size:A4;margin:13mm 14mm 14mm}*{box-sizing:border-box}
body{font-size:9.1pt;line-height:1.46;margin:0}
h2{font-size:14pt;margin:3mm 0 1.5mm}h3{font-size:10.6pt;margin:3.6mm 0 .8mm;break-after:avoid}
p,li{margin:.9mm 0;text-align:justify;hyphens:auto}ol,ul{padding-left:5mm;margin:1mm 0}
table{width:100%;border-collapse:collapse;margin:2mm 0;font-size:8.8pt}
th,td{border-bottom:.25mm solid var(--trait);padding:1.6mm 2mm;text-align:left;vertical-align:top}
th{font-family:'Geist Mono',monospace;font-weight:400;font-size:6.8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--bronze);border-bottom:.35mm solid var(--or)}
.sig{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin:3mm 0}.sig div{border:.25mm solid var(--trait);border-radius:2.5mm;min-height:30mm;padding:2mm 3mm}
.tag{font-family:'Geist Mono',monospace;font-size:7.6pt;color:#9a8f7e}
.bal{color:#9a8f7e;font-family:Arial,Helvetica,sans-serif;font-size:7.4pt;white-space:nowrap;font-feature-settings:normal;letter-spacing:0}
.signe{border:.25mm solid var(--trait);border-radius:2.5mm;padding:9mm 3mm;margin:1.5mm 0 3mm}.sig2{font-size:11pt}"""


def corps_contrat():
    md = open(SOURCE, encoding="utf-8").read()
    parts = md.split("\n---\n")
    if len(parts) < 3:
        raise SystemExit("ALERTE : séparateurs --- introuvables dans le contrat")
    contrat, annexe = parts[1], parts[2]
    for ancien, nouveau in REMPLACEMENTS:
        if contrat.count(ancien) != 1:
            raise SystemExit(f"ALERTE : motif absent ou multiple dans le contrat : {ancien[:60]!r}")
        contrat = contrat.replace(ancien, nouveau, 1)
    reste = re.findall(r"\[[^\]]*●[^\]]*\]|\[Prénom NOM[^\]]*\]", contrat)
    if reste:
        raise SystemExit(f"ALERTE : champs non convertis : {reste}")
    # Annexe : une balise par ligne du tableau (colonne « Réponse du Client »).
    lignes = annexe.split("\n")
    i = 0
    for n, l in enumerate(lignes):
        if l.startswith("| ") and l.endswith("| |") and not l.startswith("| Rubrique"):
            if i >= len(ANNEXE):
                raise SystemExit("ALERTE : plus de lignes d'annexe que de noms de champs")
            lignes[n] = l[:-2] + tag(ANNEXE[i], "Client") + " |"
            i += 1
    if i != len(ANNEXE):
        raise SystemExit(f"ALERTE : annexe : {i} lignes converties, {len(ANNEXE)} attendues")
    annexe = "\n".join(lignes).replace("## Annexe", "### Annexe", 1)
    tout = contrat + "\n" + annexe
    reste = re.findall(r"\[[^\]]{0,40}\]", tout)
    if reste:
        raise SystemExit(f"ALERTE : crochets restants : {reste}")
    return tout


def html_page():
    corps = markdown.markdown(corps_contrat(), extensions=["tables"])
    corps = corps.replace("<h2>Contrat d'assistance administrative et mandat de facturation</h2>", "", 1)
    corps = re.sub(r"(\{\{[^}]*type=signature\}\})", r'<div class="signe"><span class="bal sig2">\1</span></div>', corps)
    corps = re.sub(r"(\{\{[^}]+\}\})(?![^<]*</span>)", r'<span class="bal">\1</span>', corps)
    tete = bandeau("Contrat", "Assistance administrative <em>et mandat de facturation</em>",
                   "Devis, factures et relances préparés par DIG16, validés et signés par vous")
    return (f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>DIG16 — Contrat et mandat de facturation</title>"
            f"{POLICES}<style>{CSS}</style></head><body>{tete}{corps}</body></html>")


def main():
    open(HTML, "w", encoding="utf-8").write(html_page())
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        pg.goto("file://" + HTML)
        pg.emulate_media(media="print")
        attendre_polices(pg)
        pg.pdf(path=PDF, format="A4", print_background=True, prefer_css_page_size=True)
        b.close()
    os.remove(HTML)
    print("OK", PDF, os.path.getsize(PDF), "octets")


if __name__ == "__main__":
    main()
