#!/usr/bin/env python3
"""Kit client complet (26/10/2026) : TOUT ce qui accompagne un site client, en une commande.

Demande de l'utilisateur du 26/10 : « quand je te demande de créer un site pour un client, je veux aussi que tu crées
tout ce qui va avec : l'administratif, les supports… tout ce que propose chaque formule. Le client et moi n'avons plus
qu'à signer ». Le kit reprend les 5 documents de documents_client.py et ajoute, selon la formule :
  0. fiche de contrôle du client avant signature (interne : annuaire officiel, BODACC — 45-impayes-se-proteger.md § 1) ;
  1-5. devis + rétractation, CGV, facture, questionnaire de lancement, accord gracieux si le site est offert ;
  6. procès-verbal de réception du site (le client valide la mise en ligne, réserves éventuelles) ;
  7. mode d'emploi du site, propre à la formule (ce qui est compris, modifications, paiement, arrêt, problèmes) ;
  8. « vos comptes » : nom de domaine, hébergement, formulaire, fiche Google, Search Console, tous au nom du client ;
  9. remise des fichiers (formule Achat, ou départ d'un client) ;
  10. textes d'annonce de la mise en ligne (page Facebook, fiche Google, SMS ou email aux clients), en texte brut ;
  11. kit avis Google (Visibilité et Prestige) si le dossier donne le place_id de la fiche ;
  LISEZMOI.md : la liste « qui signe quoi, qui fait quoi », pour ne rien oublier.
Les modèles publics sont dans supports/kit-client/ ; toutes les données (prestataire, client) viennent de fichiers JSON
privés hors du dépôt, et les PDF sont écrits hors du dépôt (refusé sinon). Rien n'est inventé : chaque phrase reprend
le devis, les CGV, l'accord gracieux ou le site dig16.fr.
Usage :
  python3 outils/kit_client.py --prestataire <prive/dig16.json> --client <prive/client.json> --sortie <dossier privé>
Champs facultatifs du JSON client (clé « dossier ») : adresse_site, paiement ("mensuel" ou "unique", Prestige),
option_suivi (true si l'option hébergement et suivi est prise, Achat), place_id (fiche Google, pour le kit avis),
controles (liste de {"point","resultat","source"} pour la fiche de contrôle), pages (liste de {"page","contenu"}).
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

KIT = os.path.join(dc.SUPPORTS, "kit-client")
TEL_7J = "Joignable 7 jours sur 7"


def modele(nom):
    return dc.lire(os.path.join(KIT, nom + ".html"))


def li(items):
    return "".join(f"<li>{dc.e(x)}</li>" for x in items)


def formule_info(D):
    """Ce que comprend chaque formule, mot pour mot d'après dig16.fr, le devis et les CGV (26/10/2026)."""
    f = D["formule"]
    offert = bool(D.get("offert"))
    base = ["Hébergement, sécurité et sauvegardes", "Mentions légales et page sur les données personnelles",
            "Site testé sur téléphone, tablette et ordinateur avant la mise en ligne"]
    if f == "Essentiel":
        compris = ["Site 5 pages sur mesure", "Galerie de réalisations", "Formulaire de demande de devis",
                   "1 modification par mois", "Rapport mensuel"] + base
        quota = "Votre formule comprend 1 modification par mois (les modifications non utilisées ne se reportent pas)."
        mois = ["Un rapport simple : nombre de visites (mesure sans cookie de l’hébergeur, sur votre compte), demandes de devis reçues, points d’amélioration. Sans jargon.",
                "Les contrôles techniques et de sécurité du site."]
        paiement = ("49 € par mois, par prélèvement SEPA (mandat signé en ligne) ou par virement, au choix ; une facture chaque mois ; en cas de "
                    "prélèvement, vous êtes prévenu du montant et de la date au moins 2 jours avant. Le premier mois est réglé avant la mise en ligne, "
                    "au plus tôt le 8e jour suivant la signature.")
        engagement = ("Engagement minimal de 6 mois (il couvre la création offerte), puis sans engagement : vous pouvez arrêter à "
                      "tout moment, par email, avec effet à la fin du mois en cours.")
        cession = "et au plus tard à la fin de l’engagement minimal"
    elif f == "Visibilité":
        compris = ["Tout l’Essentiel : site 5 pages sur mesure, galerie de réalisations, formulaire de demande de devis, rapport mensuel",
                   "Fiche Google suivie chaque mois", "Demandes d’avis clients (carte avec QR code et messages prêts à envoyer)",
                   "3 modifications par mois"] + base
        quota = "Votre formule comprend 3 modifications par mois (les modifications non utilisées ne se reportent pas)."
        mois = ["Votre fiche Google : une publication, les réponses aux avis, de nouvelles photos si vous en envoyez.",
                "Un rapport simple : visites, demandes reçues, ce qui a été fait sur la fiche Google, le prochain pas.",
                "Les contrôles techniques et de sécurité du site."]
        paiement = ("79 € par mois, par prélèvement SEPA (mandat signé en ligne) ou par virement, au choix ; une facture chaque mois ; en cas de "
                    "prélèvement, vous êtes prévenu du montant et de la date au moins 2 jours avant. Le premier mois est réglé avant la mise en ligne, "
                    "au plus tôt le 8e jour suivant la signature.")
        engagement = ("Engagement minimal de 6 mois (il couvre la création offerte), puis sans engagement : vous pouvez arrêter à "
                      "tout moment, par email, avec effet à la fin du mois en cours.")
        cession = "et au plus tard à la fin de l’engagement minimal"
    elif f == "Achat":
        option = bool(D.get("option_suivi"))
        compris = ["Site 5 pages livré, à vous pour toujours", "Galerie de réalisations", "Formulaire de demande de devis",
                   "Fichiers du site remis sur demande"] + base[1:]
        if option:
            compris.insert(1, "Option hébergement et suivi (15 € par mois) : hébergement, sécurité, surveillance du site et 1 petite modification par mois")
            quota = "Avec l’option hébergement et suivi, 1 petite modification par mois est comprise ; les autres modifications sont sur devis."
            mois = ["La surveillance et les contrôles techniques et de sécurité du site."]
            paiement = ("690 € en une fois, à réception de la facture et au plus tard dans les 30 jours (acompte convenu au devis, solde "
                        "avant la mise en ligne définitive). Option hébergement et suivi : 15 € par mois, par prélèvement SEPA ou par virement, "
                        "une facture chaque mois.")
            engagement = "L’option hébergement et suivi s’arrête à tout moment, par email, avec effet à la fin du mois en cours ; vous recevez alors les fichiers du site."
        else:
            quota = "Sans option de suivi, les modifications sont sur devis ; vous pouvez aussi confier le site à qui vous voulez."
            mois = ["Rien n’est dû chaque mois : le site vous est livré avec ses fichiers."]
            paiement = ("690 € en une fois, à réception de la facture et au plus tard dans les 30 jours (acompte convenu au devis, solde "
                        "avant la mise en ligne définitive).")
            engagement = "Aucun engagement de durée."
        cession = "(cédés à la livraison pour la formule Achat)"
    elif f == "Prestige":
        unique = D.get("paiement", "mensuel" if D.get("prix") == 199 else "unique") == "unique"
        compris = ["Site entièrement sur mesure, photos plein écran", "Version anglaise", "Réservation en ligne",
                   "Modifications incluses chaque mois (textes, photos, menus, tarifs, saisons)",
                   "Fiche Google suivie et demandes d’avis", "Rapport mensuel : visites, réservations, demandes"] + base
        if unique:
            compris[3] = "Hébergement, sécurité et modifications : 29 € par mois, facultatif"
            quota = "Avec l’option hébergement, sécurité et modifications (29 € par mois), vos modifications sont comprises ; sans elle, elles sont sur devis."
            mois = ["Avec l’option : les contrôles techniques et de sécurité, vos modifications, la fiche Google et le rapport."]
            paiement = ("1 990 € en une fois, à réception de la facture et au plus tard dans les 30 jours (acompte convenu au devis, "
                        "solde avant la mise en ligne définitive). Option à 29 € par mois : par prélèvement SEPA ou par virement, une facture chaque mois.")
            engagement = "Aucun engagement de durée ; l’option s’arrête à tout moment, par email, avec effet à la fin du mois en cours."
            cession = "(cédés à la livraison pour le paiement en une fois)"
        else:
            quota = "Vos modifications sont comprises chaque mois."
            mois = ["Votre fiche Google : une publication, les réponses aux avis, de nouvelles photos si vous en envoyez.",
                    "Un rapport simple : visites, réservations, demandes, le prochain pas.",
                    "Les contrôles techniques et de sécurité du site."]
            paiement = ("199 € par mois, par prélèvement SEPA (mandat signé en ligne) ou par virement, au choix ; une facture chaque mois ; en cas de "
                        "prélèvement, vous êtes prévenu du montant et de la date au moins 2 jours avant. 0 € de création ; le premier mois est réglé avant la "
                        "mise en ligne, au plus tôt le 8e jour suivant la signature.")
            engagement = ("Engagement minimal de 12 mois (il couvre la création offerte), puis sans engagement : vous pouvez arrêter à "
                          "tout moment, par email, avec effet à la fin du mois en cours.")
            cession = "et au plus tard à la fin de l’engagement minimal"
    else:
        sys.exit(f"Formule inconnue : {f}")
    if offert:  # site offert : l'accord de réalisation gracieuse prévaut (accord_gracieux.py)
        # ce qui est compris = le site lui-même ; aucun suivi mensuel, aucune option payante
        exclure = ("modification", "Rapport", "Fiche Google", "€", "Hébergement, sécurité")
        compris = [c for c in compris if not any(x in c for x in exclure)]
        compris.append("Hébergement sur un compte ouvert à votre nom, sur une offre gratuite autorisant l’usage commercial")
        quota = ("Site offert : DIG16 corrige gratuitement toute erreur de sa part signalée dans les 12 mois suivant la mise en "
                 "ligne définitive ; les autres modifications demandées plus tard sont convenues séparément.")
        paiement = "Site offert : aucun prix, aucun abonnement, aucune facture à payer et aucun prélèvement (accord de réalisation gracieuse)."
        engagement = "Aucun engagement de durée. Si vous souhaitez plus tard un suivi mensuel (modifications, fiche Google, rapport), les formules de dig16.fr s’appliquent."
        cession = "(site offert : mise en page et code cédés à titre non exclusif, voir l’accord de réalisation gracieuse)"
        mois = [m for m in mois if "Rapport" not in m and "rapport" not in m] or ["Les contrôles techniques et de sécurité du site, tant que DIG16 l’héberge."]
    return {"compris": compris, "quota": quota, "mois": mois, "paiement": paiement, "engagement": engagement, "cession": cession}


def entete_commun(s, P, C, D, titre_ref):
    s = dc.prestataire_html(s, P)
    s = s.replace("[CLIENT]", "<br>".join([dc.e(C["denomination"]), dc.e(C["adresse"]), "SIREN " + dc.e(C["siren"])]))
    s = s.replace("[REFERENCE]", dc.e(titre_ref)).replace("[FORMULE]", dc.e(D["formule"]) + (" (offerte)" if D.get("offert") else ""))
    s = s.replace("[ADRESSE_SITE]", dc.e(D.get("adresse_site", "l’adresse provisoire communiquée par DIG16")))
    return s.replace("[NUMERO_DEVIS]", dc.e(D["numero_devis"])).replace("[DATE]", dc.e(D["date"]))


def controle(P, C, D):
    s = entete_commun(modele("controle-avant-signature"), P, C, D, f"Dossier {C['nom_commercial']} · {D['date']}")
    lignes = D.get("controles") or [
        {"point": "Entreprise active dans l’annuaire officiel (annuaire-entreprises.data.gouv.fr)", "resultat": "à vérifier", "source": "outils/verif_entreprises.py"},
        {"point": "Aucune procédure collective ni radiation au BODACC", "resultat": "à vérifier", "source": "outils/verif_entreprises.py"},
        {"point": "Secteur autorisé (hors secteurs exclus de la liste DIG16)", "resultat": "à vérifier", "source": ".claude/CLAUDE.md"},
        {"point": "Signataire habilité (dirigeant ou mandataire)", "resultat": "à vérifier", "source": "annuaire officiel, pièce d’identité au rendez-vous"},
    ]
    s = s.replace("[CONTROLES]", "".join(f"<tr><td>{dc.e(l['point'])}</td><td>{dc.e(l['resultat'])}</td><td>{dc.e(l.get('source', ''))}</td></tr>" for l in lignes))
    return s.replace("[DECISION]", dc.e(D.get("decision", "Signature possible si toutes les lignes sont vérifiées ; sinon, en parler à l’utilisateur avant de signer.")))


def pv(P, C, D):
    s = entete_commun(modele("pv-reception"), P, C, D, f"Site {C['nom_commercial']} · devis n° {D['numero_devis']}")
    pages = D.get("pages") or [{"page": "Ensemble du site", "contenu": D.get("pages_site", "")}]
    s = s.replace("[PAGES]", "".join(f"<tr><td>{dc.e(p['page'])}</td><td>{dc.e(p['contenu'])}</td></tr>" for p in pages))
    s = s.replace("[CONTROLES]", li([
        "Affichage vérifié sur téléphone (360 et 390 px), tablette et ordinateur : rien ne déborde, tout se lit sans zoomer",
        "Orthographe et typographie françaises relues ; textes validés par le client",
        "Formulaire de contact testé de bout en bout (message reçu par le client)",
        "Mentions légales et page sur les données personnelles en place ; aucun traceur publicitaire",
        "Vitesse mesurée sur téléphone (Lighthouse), accessibilité (cibles 44 px, textes alternatifs, contrastes)",
        "Référencement de base : titres et descriptions uniques, plan du site, données structurées « entreprise locale », une seule adresse en ligne",
        "Nom de domaine au nom du client, certificat HTTPS actif",
    ]))
    if D.get("offert"):
        pai = "Site offert : aucun paiement."
    elif D["formule"] in ("Essentiel", "Visibilité") or (D["formule"] == "Prestige" and D.get("prix") == 199):
        pai = "Le premier mois est réglé avant la mise en ligne définitive, au plus tôt le 8e jour suivant la signature du devis."
    else:
        pai = "Le solde est réglé avant la mise en ligne définitive, à réception de la facture."
    return s.replace("[PAIEMENT]", pai)


def mode_emploi(P, C, D):
    F = formule_info(D)
    s = entete_commun(modele("mode-d-emploi"), P, C, D, f"{C['nom_commercial']} · formule {D['formule']}")
    s = s.replace("[COMPRIS]", li(F["compris"])).replace("[QUOTA_MODIFS]", dc.e(F["quota"]))
    s = s.replace("[CHAQUE_MOIS]", li(F["mois"])).replace("[CESSION]", dc.e(F["cession"]))
    if D.get("offert"):
        s = s.replace(" Vous pouvez passer à tout moment à une formule supérieure, et à une formule inférieure à la fin de l’engagement minimal.", "")
        s = re.sub(r"suffit.{0,8}: nouveaux horaires, photo, tarif, promotion, congés, actualité\. C’est fait <b>sous 3.jours ouvrés</b>\. ", "suffit. ", s)
    pai = F["paiement"] + ("" if D.get("offert") else " Le nom de domaine, enregistré à votre nom par DIG16, est avancé puis refacturé au prix coûtant (environ 10 € par an).")
    return s.replace("[PAIEMENT]", dc.e(pai)).replace("[ENGAGEMENT]", dc.e(F["engagement"]))


def comptes(P, C, D):
    s = entete_commun(modele("vos-comptes"), P, C, D, f"{C['nom_commercial']} · {D['date']}")
    etapes = [
        ("DIG16", "Nom de domaine", "DIG16 l’enregistre à votre nom, en avance le coût (environ 10 € par an) et vous le refacture au prix coûtant, sans marge. Le domaine est à vous : il vous suit même si vous partez."),
        ("Client", "Hébergement", "Un compte d’hébergement est ouvert à votre nom (offre gratuite autorisant l’usage commercial) ; DIG16 y est invité comme gestionnaire pour installer et suivre le site. Vous pouvez retirer cet accès à tout moment."),
        ("Client", "Formulaire de contact", "Les messages arrivent sur votre adresse email. Au premier envoi, vous recevez un email de confirmation : un clic suffit pour activer le formulaire. DIG16 fait ensuite un test avec vous."),
        ("Client", "Fiche Google", "La fiche est à votre nom : vous la créez ou la validez (Google demande une vérification : en général un appel, une vidéo ou un courrier). DIG16 prépare les textes et les photos" + (", puis la suit chaque mois." if D["formule"] in ("Visibilité", "Prestige") else ".")),
        ("Client", "Google Search Console", "La propriété du site est à votre nom, DIG16 ajouté comme utilisateur : c’est ce qui permet de voir sur quelles recherches votre site apparaît. DIG16 y envoie le plan du site."),
        ("DIG16", "Bing et annuaires sérieux", "Mêmes informations partout (nom, zone, téléphone, horaires) ; DIG16 prépare chaque fiche, vous validez."),
    ]
    s = s.replace("[ETAPES]", "".join(
        f'<div class="etape"><div class="num">{i + 1}</div><div><b>{dc.e(t)}</b><span class="qui">{dc.e(qui)}</span><br>{dc.e(txt)}</div></div>'
        for i, (qui, t, txt) in enumerate(etapes)))
    return s


def remise(P, C, D):
    s = entete_commun(modele("remise-fichiers"), P, C, D, f"{C['nom_commercial']} · devis n° {D['numero_devis']}")
    s = s.replace("[DATE_REMISE]", dc.e(D.get("date_remise", "jour de la mise en ligne définitive")))
    contenu = [("Pages du site", D.get("pages_site", "toutes les pages du site, en HTML")),
               ("Images", "photos et logo fournis par le client, images d’illustration (WebP), avec la liste de leurs sources"),
               ("Polices d’écriture", "fichiers de polices inclus (aucun appel à un service extérieur)"),
               ("Fichiers techniques", "feuilles de style, scripts, plan du site, robots.txt, réglages de sécurité et de cache"),
               ("Archive", "un fichier ZIP de l’ensemble, remis par lien de téléchargement sécurisé")]
    s = s.replace("[CONTENU]", "".join(f"<tr><td>{dc.e(a)}</td><td>{dc.e(b)}</td></tr>" for a, b in contenu))
    if D.get("offert"):
        droits = "Site offert : mise en page et code cédés à titre non exclusif, textes, logo et photos propres au client ; voir l’accord de réalisation gracieuse."
    else:
        droits = ("DIG16 cède au client ses droits d’auteur sur le site réalisé pour lui (textes, mise en page, graphisme et code) : "
                  "reproduction, représentation et adaptation, pour tout usage lié à la présentation et à la promotion de son activité "
                  "(article 9 des conditions générales de vente). Les photos et contenus fournis par le client restent les siens.")
    return s.replace("[DROITS]", dc.e(droits))


def annonces(C, D):
    nom = C["nom_commercial"]
    site = D.get("adresse_site", "[adresse du site]")
    return f"""# Annonce de la mise en ligne — {nom}

Textes prêts à coller pour le client (à publier le jour de la mise en ligne définitive ; adresse du site : {site}).
Rien d'inventé : adapter les services cités à ce que fait vraiment l'entreprise.

## Page Facebook (ou Instagram)
Notre site internet est en ligne : {site}
Vous y trouverez nos services, nos réalisations en photos et un formulaire pour demander un devis en quelques secondes, depuis votre téléphone.
Merci de votre confiance, et n'hésitez pas à le partager autour de vous.

## Fiche Google (publication) — jamais de téléphone ni d'email dans le texte
Notre site internet est en ligne. Services, réalisations et demande de devis : tout est sur {site}.

## SMS ou email à vos clients
Bonjour, {nom} a maintenant son site internet : {site}. Vous y trouverez nos services, nos réalisations et la demande de devis. À bientôt.

## Signature d'email
{nom} · {site}
"""


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--prestataire", required=True)
    a.add_argument("--client", required=True)
    a.add_argument("--sortie", required=True)
    o = a.parse_args()
    sortie = os.path.abspath(o.sortie)
    if sortie.startswith(dc.DEPOT):
        sys.exit("Refusé : le dossier de sortie doit être hors du dépôt public (données privées).")
    os.makedirs(sortie, exist_ok=True)
    P = json.loads(dc.lire(o.prestataire))
    dossier = json.loads(dc.lire(o.client))
    C, D = dossier["client"], dossier["dossier"]
    base = C["fichier"]
    f = D["formule"]
    pages = [(f"0-Controle-avant-signature-{base}.pdf", controle(P, C, D)),
             (f"1-Devis-{base}.pdf", dc.devis(P, C, D)), ("2-CGV-DIG16.pdf", dc.cgv(P)),
             (f"3-Facture-{base}.pdf", dc.facture(P, C, D)),
             (f"4-Questionnaire-lancement-{base}.pdf", dc.questionnaire(C, D, dossier.get("questionnaire", {})))]
    if D.get("offert"):
        pages.append((f"5-Accord-gratuit-{base}.pdf", dc.accord(P, C, D)))
    pages += [(f"6-PV-de-reception-{base}.pdf", pv(P, C, D)),
              (f"7-Mode-d-emploi-{base}.pdf", mode_emploi(P, C, D)),
              (f"8-Vos-comptes-{base}.pdf", comptes(P, C, D))]
    if f == "Achat" or (f == "Prestige" and D.get("paiement") == "unique") or D.get("remise_fichiers"):
        pages.append((f"9-Remise-des-fichiers-{base}.pdf", remise(P, C, D)))
    dc.rendre(pages, sortie)
    with open(os.path.join(sortie, f"10-Annonce-mise-en-ligne-{base}.md"), "w", encoding="utf-8") as fh:
        fh.write(annonces(C, D))
    print("écrit :", f"10-Annonce-mise-en-ligne-{base}.md")
    avis = "non concerné (formule sans suivi de la fiche Google)"
    if f in ("Visibilité", "Prestige"):
        if D.get("place_id"):
            dossier_avis = os.path.join(sortie, "11-Kit-avis-Google")
            r = subprocess.run([sys.executable, os.path.join(ICI, "kit_avis.py"), C["nom_commercial"], D["place_id"], dossier_avis],
                               capture_output=True, text=True, check=False)
            avis = "produit dans 11-Kit-avis-Google/" if r.returncode == 0 else "ÉCHEC du kit avis : " + (r.stderr or r.stdout)[-300:]
            print("kit avis :", avis)
        else:
            avis = "à produire dès que la fiche Google du client est ouverte : python3 outils/kit_avis.py « nom » <place_id> <dossier privé>"
    mensuel = f in ("Essentiel", "Visibilité") or (f == "Prestige" and D.get("paiement", "mensuel") != "unique") or D.get("option_suivi")
    lisezmoi = f"""# Kit client {C['nom_commercial']} — formule {f}{' (offerte)' if D.get('offert') else ''}

Produit le {D['date']} par outils/kit_client.py. Dossier privé : ne jamais le copier dans le dépôt public.

## À signer (signature électronique par email avec DocuSeal, décision du 26/10 ; au rendez-vous sinon)
| Document | Client | DIG16 | Quand |
|---|---|---|---|
| 1 — Devis et bon de commande (+ formulaire de rétractation joint) | signe « Bon pour accord » | signe | à la commande |
| 2 — CGV | reçoit (jointes au devis) | — | à la commande |
{"| 5 — Accord de réalisation gracieuse | signe | signe | à la commande |" if D.get('offert') else "| Mandat de prélèvement SEPA (ou virement, au choix du client) | signe (lien GoCardless) | — | à la commande |" if mensuel else "| — | — | — | — |"}
| 6 — Procès-verbal de réception | signe « Site reçu et accepté » | signe | avant la mise en ligne définitive |
{"| 9 — Remise des fichiers | signe « Fichiers reçus » | signe | à la livraison |" if any(n.startswith('9-') for n, _ in pages) else ""}

## À remettre au client (sans signature)
- 4 — Questionnaire de lancement (déjà rempli avec ce qu'on sait ; compléter au rendez-vous de 20 minutes).
- 7 — Mode d'emploi du site ; 8 — Vos comptes ; 10 — Textes d'annonce de la mise en ligne.
- 11 — Kit avis Google : {avis}.

## Fait par DIG16 (Claude) avant la signature
- 0 — Contrôle du client (annuaire officiel, BODACC, secteur, signataire) : relire la fiche ; si une ligne dit « à vérifier », lancer outils/verif_entreprises.py.
- Contrôle qualité complet des documents (44-controle-qualite.md) et relecture par un agent en lecture seule.

## Fait par DIG16 avec le client (rendez-vous de lancement, 20 minutes)
- Nom de domaine à son nom, compte d'hébergement à son nom, activation du formulaire, fiche Google, Search Console (document 8).

## Au plus tard le jour de la mise en ligne définitive
- 3 — Facture : dater, régénérer, émettre (numérotation continue){" ; premier mois réglé avant la mise en ligne" if mensuel and not D.get('offert') else ""}.
- Contrôles : outils/seo_client.py (0 ALERTE), test des pages, IndexNow ; puis envoi des textes d'annonce (10).
- Copie de tout le dossier dans le Drive « Dig » (jamais dans le dépôt).
"""
    with open(os.path.join(sortie, "LISEZMOI.md"), "w", encoding="utf-8") as fh:
        fh.write(lisezmoi)
    print("écrit : LISEZMOI.md")


if __name__ == "__main__":
    main()
