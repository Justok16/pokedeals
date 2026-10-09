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
  3. retire <meta name="robots" content="noindex"> des pages publiques (pas des démos) ;
  4. remplit le téléphone de l'accueil ([Téléphone], tel:[TELEPHONE]) ;
  5. autorise FormSubmit dans la politique de sécurité du site (_headers, connect-src) ;
  6. active le formulaire de contact : envoi par FormSubmit (formsubmit.co, gratuit, sans compte ni clé ;
     page officielle lue le 08/10/2026), en AJAX vers contact@dig16.fr, sans reCAPTCHA (pas de cookie Google)
     mais avec un champ piège _honey ; la première soumission envoie un lien d'activation à contact@dig16.fr
     que l'utilisateur doit cliquer ; le prestataire est ajouté aux mentions légales (section 4).
Après --ecrire : envoyer un vrai message de test depuis le site en ligne et vérifier sa réception.
"""

import datetime
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "marque"))
import identite  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(ICI, "..", "site-dig"))
PAGES = ["index.html", "prestige.html", "mentions-legales.html", "test-du-pouce/index.html"]
TVA = "non applicable, art. 293 B du CGI (franchise en base)"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
        "novembre", "décembre"]


def mentions(html, ident):
    # champ de la page -> clé du fichier privé (publication voulue : obligation de la LCEN, art. 1-1)
    champs = {"Prénom NOM": "nom", "adresse professionnelle": "adresse", "numéro SIREN": "siren",
              "téléphone": "telephone"}
    valeurs = dict(ident, tva=TVA)
    champs["régime de TVA"] = "tva"
    for champ, cle in champs.items():
        html = re.sub(r'<span class="a-completer" data-champ="%s">[^<]*</span>' % re.escape(champ),
                      lambda _m, c=cle: valeurs[c], html)
    j = datetime.date.today()
    html = re.sub(r"<p>Dernière mise à jour : [^<]*</p>",
                  "<p>Dernière mise à jour : %d %s %d</p>" % (j.day, MOIS[j.month - 1], j.year), html)
    return html


ENVOI = "https://formsubmit.co/ajax/contact@dig16.fr"
JS_FORM = ("document.getElementById('form').onsubmit=async e=>{e.preventDefault();const f=e.target,m=document.getElementById('msg'),"
           "b=f.querySelector('button');if(f._honey&&f._honey.value)return;b.disabled=true;m.textContent='Envoi en cours…';"
           "const d=Object.fromEntries(new FormData(f));d._subject='Demande de démo DIG16 : '+(d.entreprise||'');d._captcha='false';"
           "d._template='table';try{const r=await fetch('" + ENVOI + "',{method:'POST',headers:{'Content-Type':'application/json',"
           "Accept:'application/json'},body:JSON.stringify(d)});const j=await r.json();if(!r.ok||String(j.success)!=='true')throw 0;"
           "f.reset();m.textContent='Merci, votre demande est bien envoyée. Je vous recontacte très vite.'}catch(_){"
           "m.textContent='L’envoi n’a pas fonctionné. Appelez-moi ou écrivez à contact@dig16.fr.'}b.disabled=false}")
ANCIEN_JS = ("document.getElementById('form').onsubmit=e=>{e.preventDefault();document.getElementById('msg').textContent="
             "'Le formulaire sera ouvert à l’immatriculation de DIG16. Merci de votre patience.'};")
PRESTATAIRES = "Elles transitent par nos prestataires techniques (hébergement, messagerie), tenus à la confidentialité."
PRESTATAIRES_NOUV = ("Elles transitent par nos prestataires techniques (hébergement, messagerie et, pour le formulaire de "
                     "contact, le service d’envoi FormSubmit de Devro LABS, aux États-Unis), tenus à la confidentialité.")


def formulaire(html, ident):
    tel = "".join(ch for ch in ident["telephone"] if ch.isdigit())
    valeurs = {"[TELEPHONE]": "+33" + tel[1:] if tel.startswith("0") else tel, "[Téléphone]": ident["telephone"]}
    for champ in ("[TELEPHONE]", "[Téléphone]"):
        html = html.replace(champ, valeurs[champ])
    html = html.replace('<fieldset disabled style=', '<fieldset style=')
    html = html.replace('<button class="btn principal" type="submit" disabled aria-disabled="true">Formulaire ouvert à l’immatriculation</button>',
                        '<input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">'
                        '<button class="btn principal" type="submit">Recevoir ma démo gratuite</button>')
    return html.replace(ANCIEN_JS, JS_FORM)


def entetes(texte):
    """Autorise l'envoi du formulaire vers FormSubmit dans la politique de sécurité (CSP) du site : sans cela le
    navigateur bloque l'envoi (défaut trouvé le 09/10/2026, invisible dans un essai local sans _headers)."""
    if "https://formsubmit.co" in texte:
        return texte
    return texte.replace("connect-src 'self'", "connect-src 'self' https://formsubmit.co", 1)


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
        if page == "index.html":
            apres = formulaire(apres, ident)
            for reste in ("[TELEPHONE]", "[Téléphone]", "disabled aria-disabled", ANCIEN_JS):
                if reste in apres:
                    print("ALERTE accueil : reste", reste[:40])
        if page == "mentions-legales.html":
            apres = mentions(apres, ident).replace(PRESTATAIRES, PRESTATAIRES_NOUV)
            if PRESTATAIRES_NOUV not in apres:
                print("ALERTE mentions : prestataire du formulaire non ajouté")
            if 'class="a-completer"' in apres.split("<h2>2.")[0]:
                print("ALERTE champ éditeur non rempli dans", page)
        print(page, ":", "modifiée" if apres != avant else "inchangée",
              "| bandeau" if "avis-ouverture\" role" in apres else "", "| noindex" if "noindex" in apres else "")
        if ecrire and apres != avant:
            open(chemin, "w", encoding="utf-8").write(apres)
    chemin = os.path.join(site, "_headers")
    avant = open(chemin, encoding="utf-8").read()
    apres = entetes(avant)
    if "connect-src 'self' https://formsubmit.co" not in apres:
        print("ALERTE _headers : FormSubmit non autorisé dans connect-src (le formulaire serait bloqué)")
    print("_headers :", "modifiée" if apres != avant else "inchangée")
    if ecrire and apres != avant:
        open(chemin, "w", encoding="utf-8").write(apres)
    print("Écrit." if ecrire else "Aperçu seulement (ajouter --ecrire, avec l'accord de l'utilisateur).")


if __name__ == "__main__":
    main()
