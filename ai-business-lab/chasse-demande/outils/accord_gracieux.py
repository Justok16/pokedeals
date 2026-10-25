"""Accord de réalisation gracieuse d'un site (site offert par DIG16). Utilisé par documents_client.py.
Aucune donnée personnelle ici : tout vient des fichiers JSON privés passés en paramètre."""
import html
import re

NB = " "


def _t(x):
    """Typographie française : espace insécable avant : ; ? ! et dans les guillemets."""
    for a in (" :", " ;", " ?", " !"):
        x = x.replace(a, NB + a[1])
    return x.replace("« ", "«" + NB).replace(" »", NB + "»")


def articles(C, D):
    pages = D.get("pages_site", "")
    adresse = D.get("adresse_provisoire", "")
    logo = D.get("logo_origine", "")
    return [
        ("Objet", [f"DIG16 réalise le site internet de {C['nom_commercial']} et l’offre au bénéficiaire. {pages}"
                   + (f" Il est visible à l’adresse provisoire {adresse}." if adresse else "")]),
        ("Gratuité", [("La réalisation est offerte. Elle ne donne lieu à aucun prix, aucun abonnement ni aucune facture à payer, "
                      "et n’engage le bénéficiaire pour aucune durée. Les clauses de prix, d’engagement et de paiement des "
                      "conditions générales de vente de DIG16 ne s’appliquent pas ; en cas de différence, le présent accord prévaut.")]),
        ("Contenu et validation", [
            ("DIG16 a rédigé les textes à partir des informations données par le bénéficiaire. Le bénéficiaire les relit et "
            "valide le site par écrit (e-mail ou SMS) avant la mise en ligne définitive. Il reste responsable de l’exactitude "
            "des informations qu’il a données, notamment ses prestations, sa zone d’intervention et ses mentions légales, dont "
            "son régime de TVA."),
            ("Les photos d’illustration proviennent d’Unsplash et sont utilisées selon la licence Unsplash ; elles ne montrent ni "
            "l’entreprise ni ses interventions. Le bénéficiaire peut les remplacer à tout moment par ses propres photos.")]),
        ("Droits sur le site", [
            "DIG16 cède gratuitement au bénéficiaire les droits de reproduction, de représentation et d’adaptation sur les "
            "textes, le logo" + (f" redessiné d’après {logo}" if logo else "") + ", la mise en page et le code du site "
            "(fichiers HTML, CSS et scripts), pour son site internet et tous ses supports de communication, numériques ou "
            "imprimés (réseaux sociaux, cartes de visite, véhicule, devis, factures…), dans le monde entier et pour toute la "
            "durée des droits d’auteur.",
            ("Les textes et le logo sont cédés à titre exclusif. La mise en page et le code sont cédés à titre non exclusif : "
            "DIG16 garde le droit de réutiliser ses modèles, sa structure de site et son savoir-faire pour d’autres "
            "réalisations, sans les textes, le logo ni les photos propres au bénéficiaire."),
            ("Le bénéficiaire déclare disposer des droits sur le logo figurant sur " + logo + " et autorise DIG16 à l’adapter. "
             if logo else "")
            + "Les photos Unsplash et les polices de caractères (licence SIL Open Font License) restent soumises à leur propre "
            "licence. Sur simple demande, DIG16 remet au bénéficiaire l’ensemble des fichiers du site ; le bénéficiaire en "
            "conserve une copie."]),
        ("Hébergement et nom de domaine", [
            ("L’adresse actuelle est provisoire et sert uniquement à faire relire le site au bénéficiaire. Elle sera supprimée "
            "dès la mise en ligne définitive. Pour celle-ci, DIG16 installe gratuitement le site sur un compte d’hébergement "
            "ouvert au nom du bénéficiaire, sur une offre gratuite qui autorise l’usage commercial, et met à jour l’hébergeur "
            "indiqué dans les mentions légales et la politique de confidentialité. Le nom de domaine est enregistré au nom du "
            "bénéficiaire et à sa charge.")]),
        ("Formulaire de demande et données personnelles", [
            ("Les messages envoyés depuis le formulaire du site arrivent directement dans la boîte e-mail du bénéficiaire, par le "
            "service FormSubmit ; DIG16 n’y a pas accès. Le bénéficiaire est responsable du traitement des données reçues par "
            "le formulaire ; il les conserve et les supprime comme l’indique la politique de confidentialité du site."),
            ("Lors du premier envoi depuis le formulaire, FormSubmit adresse au bénéficiaire un e-mail de confirmation ; il clique "
            "une fois sur le lien qu’il contient pour activer la réception des messages. DIG16 fait ce premier envoi de test "
            "avec le bénéficiaire, avant la mise en ligne définitive.")]),
        ("Modifications et corrections", [
            ("DIG16 corrige gratuitement toute erreur qu’il aurait commise dans la réalisation et qui lui est signalée dans les "
            "douze mois suivant la mise en ligne définitive. Les autres modifications demandées plus tard sont convenues "
            "séparément. Le bénéficiaire reste libre de faire modifier son site par la personne de son choix.")]),
        ("Mention « Site conçu par DIG16 »", [
            ("Le pied de page du site porte la mention « Site conçu par DIG16 », avec un lien vers dig16.fr. DIG16 accepte par "
            "avance de retirer cette mention à la demande du bénéficiaire.")]),
        ("Exemple de réalisation", [
            ("Le bénéficiaire ☐ accepte ☐ refuse (cocher une case) que DIG16 présente ce site comme exemple de réalisation "
            "(captures d’écran et lien), en ne citant que le nom commercial et la commune. Il peut retirer son accord à tout "
            "moment par simple e-mail à contact@dig16.fr.")]),
        ("Engagement de DIG16", [
            ("Le site est fourni tel qu’il a été validé. DIG16 ne promet aucun résultat de fréquentation, de position dans les "
            "moteurs de recherche ou de nombre de demandes."),
            ("Le site repose sur des services gratuits de tiers (hébergement, formulaire) que DIG16 ne contrôle pas ; DIG16 n’est "
            "pas responsable de leurs interruptions ni de leurs changements de conditions. DIG16 n’est pas responsable des "
            "modifications faites par une autre personne.")]),
        ("Droit applicable", [("Le présent accord est soumis au droit français. En cas de désaccord, les parties cherchent "
                              "d’abord une solution amiable.")]),
    ]


def accord_html(P, C, D, gabarit):
    """gabarit : modèle HTML DIG16 (supports/modele-devis.html) dont on reprend la feuille de style et l'en-tête."""
    e = lambda x: html.escape(str(x), quote=False)
    cp = lambda x: re.sub(r"(\d{5}) ", r"\1" + NB, x)
    arts = ""
    for i, (titre, pars) in enumerate(articles(C, D), 1):
        corps = "".join(f"<p>{_t(e(x))}</p>" for x in pars if x)
        if D.get("adresse_provisoire"):
            corps = corps.replace(e(D["adresse_provisoire"]), f'<span class="nowrap">{e(D["adresse_provisoire"])}</span>')
        arts += f"<section><h2>Article {i}{NB}— {_t(e(titre))}</h2>{corps}</section>"
    tete = gabarit[:gabarit.index("<body>")].replace("DIG16 — Devis et bon de commande", "DIG16 — Accord de réalisation gracieuse")
    style = """<style>.accord p{text-align:justify;hyphens:auto;orphans:3;widows:3;margin:1mm 0}
.accord h2{margin:3.6mm 0 .8mm}.accord section h2+p{break-before:avoid}.nowrap{white-space:nowrap}
.fait{margin-top:5mm;break-inside:avoid}.sign{break-inside:avoid}</style>"""
    marque = gabarit[gabarit.index('<div class="ligne-haut">'):gabarit.index('<div class="k">')]
    couv = (f'<div class="couv">{marque}'
            '<div class="k">Création et suivi de sites internet</div><h1>Accord de réalisation gracieuse</h1>'
            f"<p>Site de {e(C['nom_commercial'])} · Version du {e(D['date_longue'])}</p></div>")
    pr = (f"{e(P['nom'])}, entrepreneur individuel, nom commercial DIG16<br>SIREN <span class=\"nowrap\">{e(P['siren'])}</span>"
          f"<br>{cp(e(P['adresse']))}<br>contact@dig16.fr<br>ci-après «{NB}DIG16{NB}»")
    cl = (f"{e(C['dirigeant'])}, {e(C['forme'])}, nom commercial {e(C['nom_commercial'])}<br>SIREN <span class=\"nowrap\">"
          f"{e(C['siren'])}</span><br>{cp(e(C['adresse']))}<br>ci-après «{NB}le bénéficiaire{NB}»")
    return (tete.replace("</head>", style + "</head>") + "<body>" + couv
            + f'<div class="deux"><div class="cadre"><b>DIG16</b><br>{pr}</div><div class="cadre"><b>Bénéficiaire</b><br>{cl}</div></div>'
            + f'<div class="accord">{arts}</div>'
            + f'<p class="fait">Fait à ........................................, le ........ / ........ / {e(D["annee"])}, en deux exemplaires.</p>'
            + f'<div class="sign"><div>Pour DIG16<br>{e(P["nom"])}<br>(signature)</div>'
            + f'<div>Pour {e(C["nom_commercial"])}<br>{e(C["dirigeant"])}<br>(signature)</div></div></body></html>')
