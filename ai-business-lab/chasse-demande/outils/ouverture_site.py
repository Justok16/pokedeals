#!/usr/bin/env python3
"""Ouverture de dig16.fr le jour où la formalité de création est validée (préparé le 08/10/2026).

Usage : DIG16_IDENTITE=<json privé> python3 outils/ouverture_site.py [dossier_du_site] [--ecrire]
  sans --ecrire : montre seulement ce qui changerait (aucun fichier touché) ;
  avec --ecrire : modifie les pages. À lancer UNIQUEMENT avec l'accord de l'utilisateur pour publier
  ses coordonnées (le dépôt est public), puis outils/test_pages.py avant toute mise en ligne.
Ce que fait le script :
  1. remplit l'éditeur dans mentions-legales.html (nom, adresse, SIREN, TVA, téléphone, directeur de la
     publication) avec le fichier privé de outils/marque/identite.py, et met la date à jour ;
  2. retire le bandeau « Ouverture prochaine » (index.html, prestige.html) ;
  3. retire <meta name="robots" content="noindex"> des pages publiques (pas des démos).
Le formulaire de contact reste désactivé : il ne s'active qu'avec une vraie transmission testée.
"""

import datetime
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "marque"))
import identite  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ICI, "..", "site-dig"))
PAGES = ["index.html", "prestige.html", "mentions-legales.html"]
TVA = "non applicable, art. 293 B du CGI (franchise en base)"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
        "novembre", "décembre"]


def mentions(html, ident):
    champs = {
        "Prénom NOM": ident["nom"],
        "adresse professionnelle": ident["adresse"],
        "numéro SIREN": ident["siren"],
        "régime de TVA": TVA,
        "téléphone": ident["telephone"],
    }
    for cle, valeur in champs.items():
        html = re.sub(r'<span class="a-completer" data-champ="%s">[^<]*</span>' % re.escape(cle), valeur, html)
    j = datetime.date.today()
    html = re.sub(r"<p>Dernière mise à jour : [^<]*</p>",
                  "<p>Dernière mise à jour : %d %s %d</p>" % (j.day, MOIS[j.month - 1], j.year), html)
    return html


def ouvrir(html):
    html = re.sub(r'<div class="avis-ouverture" role="status">.*?</div>', "", html, flags=re.S)
    return html.replace('<meta name="robots" content="noindex">\n', "").replace('<meta name="robots" content="noindex">', "")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    site = args[0] if args else SITE
    ecrire = "--ecrire" in sys.argv
    ident = identite.charger_identite_seule()
    if not ident:
        raise SystemExit("ALERTE : DIG16_IDENTITE manquant (fichier privé des coordonnées)")
    for page in PAGES:
        chemin = os.path.join(site, page)
        avant = open(chemin, encoding="utf-8").read()
        apres = ouvrir(avant)
        if page == "mentions-legales.html":
            apres = mentions(apres, ident)
            if 'class="a-completer"' in apres.split("<h2>2.")[0]:
                print("ALERTE champ éditeur non rempli dans", page)
        print(page, ":", "modifiée" if apres != avant else "inchangée",
              "| bandeau" if "avis-ouverture\" role" in apres else "", "| noindex" if "noindex" in apres else "")
        if ecrire and apres != avant:
            open(chemin, "w", encoding="utf-8").write(apres)
    print("Écrit." if ecrire else "Aperçu seulement (ajouter --ecrire, avec l'accord de l'utilisateur).")


if __name__ == "__main__":
    main()
