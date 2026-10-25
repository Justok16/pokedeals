"""Pré-remplit TOUS les documents d'un nouveau site client (règle du 25/10/2026 : « à chaque site créé, quel que soit le prix »).

Documents produits (PDF, rendus en mémoire, jamais de HTML rempli sur disque) :
  1. devis et bon de commande, avec l'information sur la rétractation et le formulaire de rétractation ;
  2. conditions générales de vente ;
  3. facture (prête à émettre ; à 0 € avec la remise si le site est offert) ;
  4. questionnaire de lancement du site, avec les réponses déjà connues ;
  5. si le site est offert : l'accord de réalisation gracieuse (droits, hébergement, modifications).

Les modèles publics sont dans supports/ ; les données (prestataire et client) sont PRIVÉES et lues dans des
fichiers JSON hors du dépôt. Usage :
  python3 outils/documents_client.py --prestataire <prive/dig16.json> --client <prive/client.json> --sortie <dossier privé>
Le dossier de sortie doit être hors du dépôt (refusé sinon).
"""
import argparse
import base64
import html
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
SUPPORTS = os.path.join(RACINE, "supports")
DEPOT = os.path.dirname(os.path.dirname(RACINE))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
NB = " "


def lire(chemin):
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def euros(x):
    s = f"{x:,.2f}".replace(",", NB).replace(".", ",")
    return s + NB + "€"


def e(x):
    return html.escape(str(x), quote=False)


def images_en_ligne(s):
    """Les modèles pointent vers ../site-dig/img/... : on les intègre en data URI (rendu en mémoire)."""
    def rempl(m):
        chemin = os.path.normpath(os.path.join(SUPPORTS, m.group(1)))
        with open(chemin, "rb") as f:
            return 'src="data:image/png;base64,' + base64.b64encode(f.read()).decode() + '"'
    return re.sub(r'src="(\.\./site-dig/img/[^"]+\.png)"', rempl, s)


def prestataire_html(s, P):
    s = s.replace("[Prénom Nom]", e(P["nom"])).replace("[Adresse]", e(P["adresse"]))
    s = s.replace("[numéro à l’immatriculation]", e(P["siren"])).replace("[téléphone]", e(P["telephone"]))
    s = s.replace("[date de l’immatriculation]", e(P["date_immatriculation"]))
    return s


def bloc_client(C):
    lignes = [e(C["denomination"]), e(C["adresse"]), "SIREN " + e(C["siren"])]
    if C.get("dirigeant"):
        lignes.insert(1, "Représentée par " + e(C["dirigeant"]))
    return '<div class="cadre"><b>Client</b><br>' + "<br>".join(lignes) + "</div>"


def devis(P, C, D):
    s = lire(os.path.join(SUPPORTS, "modele-devis.html"))
    s = prestataire_html(s, P)
    s = s.replace("N° [AAAA-NNN] · Date : [jj/mm/aaaa]", f"N° {e(D['numero_devis'])} · Date : {e(D['date'])}")
    s = re.sub(r'<div class="cadre"><b>Client</b>.*?</div></div>', bloc_client(C) + "</div>", s, count=1, flags=re.DOTALL)
    s = s.replace("☐ " + D["formule"], "☑ " + D["formule"], 1)
    s = s.replace("[date convenue ensemble]", e(D["mise_en_ligne"]))
    if D.get("offert"):
        texte = (f"<p><b>Site offert</b> : remise de 100 % sur la formule {e(D['formule'])} (valeur {euros(D['prix'])}). "
                 "Aucun paiement, aucun abonnement, aucun engagement de durée et aucun prélèvement. Les clauses de prix, "
                 "d’engagement et de paiement de ce devis et des conditions générales de vente ne s’appliquent pas ; "
                 "l’accord de réalisation gracieuse joint précise les droits sur le site, l’hébergement et les modifications, "
                 "et prévaut en cas de différence.</p>")
        s = re.sub(r"<p><b>Engagement</b>.*?</p>\s*<p><b>Paiement</b>.*?</p>", texte, s, count=1, flags=re.DOTALL)
        s = re.sub(r"<p><b>Création offerte</b>.*?</p>",
                   f"<p>Mise en ligne prévue {'au plus tard le ' if D['mise_en_ligne'][:1].isdigit() else ': '}<b>{e(D['mise_en_ligne'])}</b>, sous réserve de la validation "
                   "des contenus par le client. Nom de domaine au nom du client, à sa charge.</p>", s, count=1, flags=re.DOTALL)
    return s


def facture(P, C, D):
    s = lire(os.path.join(SUPPORTS, "modele-facture.html"))
    s = prestataire_html(s, P)
    s = s.replace("N° [AAAA-NNN] (numérotation continue) · Date d’émission : [jj/mm/aaaa] · Date de la prestation : [période ou jj/mm/aaaa]",
                  f"N° {e(D['numero_facture'])} · Date d’émission : {e(D['date_facture'])} · Date de la prestation : {e(D['date_prestation'])}")
    s = s.replace("[Nom de l’entreprise]", e(C["denomination"])).replace("[Adresse du client]", e(C["adresse"]))
    s = s.replace("[numéro du client]", e(C["siren"]))
    s = s.replace("[si le client en a établi un]", "devis " + e(D["numero_devis"]) + " du " + e(D["date"]))
    remise = D["prix"] if D.get("offert") else D.get("remise", 0)
    total = D["prix"] - remise
    s = s.replace("[Formule Essentiel — abonnement du mois de …]", e(D["designation"]))
    s = s.replace("<td class=\"n\">[49,00 €]</td><td class=\"n\">[49,00 €]</td>", f'<td class="n">{euros(D["prix"])}</td><td class="n">{euros(D["prix"])}</td>', 1)
    s = re.sub(r"<tr><td>\[Autre ligne si besoin\]</td>.*?</tr>", "", s, count=1, flags=re.DOTALL)
    s = s.replace("[néant ou montant]", (euros(remise) + (" (site offert)" if D.get("offert") else "")) if remise else "néant")
    s = s.replace("<b>[49,00 €]</b></td></tr>\n<tr>", f"<b>{euros(total)}</b></td></tr>\n<tr>", 1)
    s = s.replace("<b>[49,00 €]</b>", f"<b>{euros(total)}</b>", 1)
    if total == 0:
        s = s.replace("<b>Date de règlement</b> : [jj/mm/aaaa] · Mode : [prélèvement / virement].", "<b>Règlement</b> : sans objet, rien n’est à payer.")
    else:
        s = s.replace("[jj/mm/aaaa]", e(D.get("date_reglement", "à réception"))).replace("[prélèvement / virement]", e(D.get("mode", "virement")))
    s = re.sub(r'<p class="petit">Mentions vérifiées.*?</p>', "", s, flags=re.DOTALL)
    return s


def cgv(P):
    return prestataire_html(lire(os.path.join(SUPPORTS, "cgv-dig.html")), P)


def questionnaire(C, D, reponses):
    s = lire(os.path.join(SUPPORTS, "questionnaire-lancement-site.html"))
    ent = (f'<div class="entete"><div>Entreprise : <b>{e(C["nom_commercial"])}</b></div><div>Date de l\'entretien : <b>{e(D["date"])}</b></div>'
           f'<div>Interlocuteur : <b>{e(C.get("dirigeant", ""))}</b></div><div>Formule envisagée : <b>{e(D["formule"])}'
           + (" (offerte)" if D.get("offert") else "") + "</b></div></div>")
    s = re.sub(r'<div class="entete">.*?</div></div>', ent, s, count=1, flags=re.DOTALL)
    for num, rep in reponses.items():
        debut = s.find(f'<div class="q"><div class="t"><b>{num}.</b>')
        if debut < 0:
            sys.exit(f"Question {num} introuvable dans le questionnaire.")
        fin, prof = debut, 0
        for m in re.finditer(r"<div\b|</div>", s[debut:]):  # fin du bloc de la question (divs imbriquées)
            prof += 1 if m.group() != "</div>" else -1
            if prof == 0:
                fin = debut + m.start()
                break
        corps = s[debut:fin]
        if isinstance(rep, dict) and "cocher" in rep:
            for c in rep["cocher"]:
                if "☐ " + c not in corps:
                    sys.exit(f"Question {num} : case « {c} » introuvable.")
                corps = corps.replace("☐ " + c, "☑ " + c, 1)
            if rep.get("texte"):
                corps += f'<div class="rep">{e(rep["texte"])}</div>'
        elif '<div class="ln"></div>' in corps:
            corps = re.sub(r'(<div class="ln"></div>)+', f'<div class="rep">{e(rep)}</div>', corps, count=1)
        else:
            corps += f'<div class="rep">{e(rep)}</div>'
        s = s[:debut] + corps + s[fin:]
    s = s.replace("</style>", ".rep{border-bottom:.25mm solid #b9b0a2;padding:1mm 0;font-family:Geist,Arial,sans-serif;color:#1a1814;min-height:6mm}</style>", 1)
    return s


def accord(P, C, D):
    sys.path.insert(0, ICI)
    from accord_gracieux import accord_html
    return accord_html(P, C, D, lire(os.path.join(SUPPORTS, "modele-devis.html")))


def rendre(pages, sortie):
    with sync_playwright() as pw:
        proxy = {"server": os.environ["HTTPS_PROXY"], "bypass": "127.0.0.1,localhost"} if os.environ.get("HTTPS_PROXY") else None
        b = pw.chromium.launch(executable_path=CHROME, proxy=proxy) if proxy else pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(ignore_https_errors=True)
        for nom, contenu in pages:
            pg = ctx.new_page()
            pg.set_content(images_en_ligne(contenu), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.pdf(path=os.path.join(sortie, nom), format="A4", print_background=True, prefer_css_page_size=True)
            pg.close()
            print("écrit :", nom)
        b.close()


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--prestataire", required=True)
    a.add_argument("--client", required=True)
    a.add_argument("--sortie", required=True)
    o = a.parse_args()
    sortie = os.path.abspath(o.sortie)
    if sortie.startswith(DEPOT):
        sys.exit("Refusé : le dossier de sortie doit être hors du dépôt public (données privées).")
    os.makedirs(sortie, exist_ok=True)
    P = json.loads(lire(o.prestataire))
    dossier = json.loads(lire(o.client))
    C, D = dossier["client"], dossier["dossier"]
    base = C["fichier"]
    pages = [(f"1-Devis-{base}.pdf", devis(P, C, D)), ("2-CGV-DIG16.pdf", cgv(P)),
             (f"3-Facture-{base}.pdf", facture(P, C, D)),
             (f"4-Questionnaire-lancement-{base}.pdf", questionnaire(C, D, dossier.get("questionnaire", {})))]
    if D.get("offert"):
        pages.append((f"5-Accord-gratuit-{base}.pdf", accord(P, C, D)))
    rendre(pages, sortie)


if __name__ == "__main__":
    main()
