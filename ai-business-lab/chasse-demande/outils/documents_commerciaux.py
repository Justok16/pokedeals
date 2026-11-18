# Documents commerciaux de DIG16 (05/10/2026) : CGV, modèle de devis-bon de commande, modèle de facture.
# Sources lues le 05/10/2026 :
#  - mentions obligatoires d'une facture : Service Public Entreprendre F31808 (« Vérifié le 11 août 2026 ») ;
#  - pénalités de retard et indemnité de 40 € : F23211 (vérifié le 07/08/2026, voir 45-impayes-se-proteger.md) ;
#  - franchise en base : mention « TVA non applicable, art. 293 B du code général des impôts » (F31808) ;
#  - compte bancaire dédié et mention « EI » : F35991 (« Vérifié le 28 mai 2026 »).
#  - rétractation : informations-type (annexe à l'article R221-3 du code de la consommation, version du 19/06/2026)
#    et modèle de formulaire (annexe à l'article R221-1, version du 28/05/2022), lus sur Légifrance le 05/10/2026 ;
#  - clause de tribunal retirée (CPC art. 48 : réservée aux parties toutes commerçantes) ; prénotification SEPA
#    abaissée à 2 jours par accord (14 jours par défaut, ACPR) ; délais rendus compatibles avec L221-10 ;
#  - cession des droits (article 9) : CPI L131-3 (« mention distincte » de chaque droit, étendue, destination, lieu,
#    durée), lu le 05/10/2026 ;
#    rétractation applicable aux contrats hors établissement avec un client de 5 salariés au plus (L221-3), cf. 40-cadre-legal-sites.md.
# Les promesses (engagement, rétractation, propriété du site, délais) reprennent mot pour mot le site de DIG16.
# Les champs entre crochets se remplissent à l'immatriculation : aucune donnée personnelle dans ce dépôt.
# Usage : python3 outils/documents_commerciaux.py   (écrit supports/*.html et supports/Dig-*.pdf)
# Version remplie (privée) : DIG16_IDENTITE=<json privé> DIG16_SORTIE=<dossier privé> python3 outils/documents_commerciaux.py
#   (voir outils/marque/identite.py ; les fichiers remplis ne vont jamais dans supports/)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "marque"))
from charte_documents import BASE, COUVERTURE, POLICES, attendre_polices, bandeau  # noqa: E402
import identite  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
SUP = os.path.normpath(os.path.join(ICI, "..", "supports"))
CHROME = "/opt/pw-browsers/chromium"

EMETTEUR = "[Prénom Nom] EI — « DIG16 »<br>[Adresse]<br>SIREN [numéro à l’immatriculation]<br>contact@dig16.fr"
CSS = BASE + COUVERTURE + """@page{size:A4;margin:13mm 14mm 14mm}*{box-sizing:border-box}
body{font-size:9.2pt;line-height:1.48;margin:0}
h2{font-size:13pt;line-height:1.1;margin:4.2mm 0 1mm;break-after:avoid}
p,li{margin:.8mm 0}ul{padding-left:5mm;margin:1mm 0}
table{width:100%;border-collapse:collapse;margin:2.4mm 0;font-size:8.9pt}
th,td{border-bottom:.25mm solid var(--trait);padding:1.8mm 2mm;text-align:left;vertical-align:top}
th{font-family:'Geist Mono',monospace;font-weight:400;font-size:6.8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--bronze);border-bottom:.35mm solid var(--or);background:none}
td.n{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:.35mm solid var(--texte)}
.deux{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin:2mm 0}
.cadre{background:var(--fond-doux);border:.25mm solid var(--trait);border-radius:2.5mm;padding:3mm 4mm}
.cadre>b:first-child{font-family:'Geist Mono',monospace;font-weight:400;font-size:6.8pt;letter-spacing:.16em;text-transform:uppercase;color:var(--bronze)}
.champ{border-bottom:.25mm solid #b9b0a2;height:6mm;margin:1mm 0}.petit{color:var(--gris);font-size:8pt}
.sign{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:4mm}.sign div{border:.25mm solid var(--trait);border-radius:2.5mm;height:26mm;padding:2mm 3mm;font-size:8.2pt;color:var(--gris)}
.cgv{columns:2;column-gap:7mm;column-rule:.25mm solid var(--trait);font-size:8.15pt;line-height:1.37}.cgv h2{font-size:11pt;margin:2.2mm 0 .4mm}.cgv p{margin:.5mm 0;text-align:justify;hyphens:auto}"""
TETE = (
    '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{t}</title>'
    + POLICES
    + "<style>" + CSS + "</style></head><body>"
)

PENALITES = (
    "En cas de retard de paiement, des pénalités sont dues de plein droit, sans rappel préalable, au taux "
    "appliqué par la Banque centrale européenne à son opération de refinancement la plus récente, majoré de "
    "10 points, ainsi qu’une indemnité forfaitaire pour frais de recouvrement de 40 € par facture."
)

CGV = f"""{bandeau("Création et suivi de sites internet", "Conditions générales de vente", "Applicables à toute commande passée par un professionnel. Version 3 du 18 novembre 2026.")}
<div class="cgv">
<h2>1. Prestataire</h2><p>{EMETTEUR.replace("<br>", ", ")}. TVA non applicable, art. 293 B du code général des impôts.</p>
<h2>2. Objet</h2><p>DIG16 crée, héberge et suit des sites internet pour les professionnels (entreprises, artisans, commerçants). Les présentes conditions s’appliquent à toute commande ; elles prévalent sur tout autre document, sauf accord écrit contraire.</p>
<h2>3. Formules et prix</h2><p>Les formules et leurs prix sont ceux du devis signé : Essentiel 49 € par mois, Visibilité 79 € par mois, Prestige 1 990 € une fois ou 199 € par mois, Achat 690 € une fois (hébergement et suivi en option à 15 € par mois : hébergement, sécurité, surveillance et 1 petite modification par mois, autres modifications sur devis). Douze mois payés d’avance : un mois offert (Essentiel 539 €, Visibilité 869 €). Les prix sont nets : TVA non applicable. Le nom de domaine est enregistré au nom du client, qui le règle lui-même directement au bureau d’enregistrement (environ 10 € par an) ; DIG16 l’accompagne dans cette démarche, n’avance pas cette somme et ne la refacture pas.</p>
<h2>4. Commande et délais</h2><p>La commande est formée par la signature du devis-bon de commande. Pour les formules mensuelles, la création du site est offerte. La date de mise en ligne est convenue avec le client et écrite sur le devis-bon de commande (article L111-1, 3°, du code de la consommation) ; elle suppose la réception de tous les contenus et leur validation par le client, et n’intervient jamais avant le 8e jour suivant la signature. La réalisation ne commence qu’après le délai de 14 jours de l’article 5, sauf si le client a demandé par écrit, sur le devis-bon de commande, qu’elle commence pendant ce délai (article L221-25 du code de la consommation). Le premier mois est réglé avant la mise en ligne, au plus tôt le 8e jour suivant la signature.</p>
<h2>4 bis. Validation avant mise en ligne</h2><p>Avant la mise en ligne, DIG16 envoie au client une adresse de prévisualisation du site. Le client vérifie le site et donne son accord par écrit (email ou message). Il peut signaler des réserves dans les 8 jours suivant la mise en ligne ; DIG16 corrige sans frais les écarts avec ce qui a été convenu. Passé ce délai sans réserve, le site est réputé conforme à la commande.</p>
<h2>5. Droit de changer d’avis</h2><p>Le client dispose de 14 jours à compter de la signature pour se rétracter, sans motif ni frais, par simple email ou courrier. Aucun paiement n’est demandé avant 8 jours. Ce droit, prévu par la loi pour les contrats signés hors des locaux de DIG16, est appliqué à tous les clients.</p><p>L’information prévue par la loi et le formulaire de rétractation sont joints au devis-bon de commande. Si le client a demandé que la prestation commence pendant ce délai puis se rétracte, il règle seulement la part déjà fournie, en proportion du prix convenu.</p>
<h2>6. Durée et résiliation</h2><p>Les formules mensuelles comportent un engagement minimal de 6 mois (12 mois pour Prestige en paiement mensuel et pour les 12 mois payés d’avance), qui couvre la création offerte. Ensuite, le contrat se poursuit sans engagement : le client peut y mettre fin à tout moment, par email, avec effet à la fin du mois en cours. Le client peut passer à tout moment à une formule supérieure, et à une formule inférieure à la fin de son engagement minimal.</p><p>La création du site est offerte en contrepartie de l’engagement minimal : si le client met fin au contrat avant son terme, les mensualités restant à courir jusqu’à ce terme restent dues.</p>
<h2>7. Paiement</h2><p>Formules mensuelles : une facture chaque mois, réglée au choix du client par prélèvement SEPA mensuel sur mandat signé par lui (il est prévenu du montant et de la date au moins 2 jours avant chaque prélèvement) ou par virement à réception de la facture, au plus tard dans les 10 jours. Formules payées en une fois : à réception de la facture, au plus tard dans les 30 jours. Escompte pour paiement anticipé : néant. {PENALITES}</p><p>Si une somme reste impayée 15 jours après une mise en demeure par écrit restée sans effet, DIG16 peut suspendre l’hébergement et le suivi du site jusqu’au paiement, après en avoir prévenu le client par écrit.</p>
<h2>8. Réalisation, modifications et contenus</h2><p>DIG16 rédige les textes à partir de l’échange avec le client, qui relit et valide tout avant la mise en ligne. Le client fournit des informations exactes et des photos dont il détient les droits. Une modification est un changement de contenu sur une page existante (texte, photo, horaires, prix, actualité) ; une nouvelle page ou une nouvelle fonction fait l’objet d’un devis. Les demandes, envoyées par email, sont traitées sous 3 jours ouvrés, dans la limite prévue par la formule (Essentiel : 1 par mois ; Visibilité : 3 par mois ; Prestige : selon le devis) ; les modifications non utilisées ne se reportent pas. La correction d’une erreur de DIG16 ne compte pas comme une modification.</p><p>Le client garantit qu’il détient les droits nécessaires sur les textes, photos, logos et vidéos qu’il fournit, et garantit DIG16 contre toute réclamation d’un tiers à leur sujet. Les images d’illustration ajoutées par DIG16 proviennent de banques d’images dont la licence autorise l’usage commercial ; leur origine est conservée. Sur simple réclamation d’un tiers, DIG16 retire le contenu concerné sans délai et en informe le client.</p>
<h2>9. Propriété</h2><p>Le nom de domaine est enregistré au nom du client. DIG16 cède au client, dès le complet paiement des sommes dues au titre de l’engagement minimal (dès le paiement du prix pour les formules payées en une fois), ses droits d’auteur sur le site réalisé pour lui (textes, mise en page, graphisme et code créés par DIG16) : le droit de <b>reproduction</b>, le droit de <b>représentation</b> et le droit d’<b>adaptation</b>, pour tout usage lié à la présentation et à la promotion de l’activité du client, sur internet et tout support numérique, pour le monde entier et pour toute la durée légale de protection. Les photos et contenus fournis par le client restent les siens. À la fin du contrat, une fois ces sommes réglées, le client reçoit l’ensemble des fichiers de son site et DIG16 l’aide à le transférer chez l’hébergeur de son choix.</p>
<h2>10. Hébergement et disponibilité</h2><p>DIG16 est tenu d’une obligation de moyens. Il fait ses meilleurs efforts pour que le site reste accessible et sécurisé ; une interruption ponctuelle pour maintenance ou du fait de l’hébergeur peut survenir. En cas d’interruption, DIG16 s’efforce de rétablir le site dans la journée ouvrée qui suit le signalement. DIG16 ne promet pas de position dans les résultats de Google.</p>
<h2>11. Données personnelles</h2><p>DIG16 traite les données du client et de ses visiteurs uniquement pour réaliser et suivre le site, conformément au RGPD. Chaque site comprend ses mentions légales et ses informations sur les données ; aucun traceur publicitaire n’est installé.</p><p>Pour les messages envoyés par les visiteurs au moyen du formulaire du site, le client est responsable du traitement et DIG16 agit comme sous-traitant au sens de l’article 28 du RGPD, selon l’annexe ci-dessous. DIG16 informe le client sans délai de toute violation de données dont il a connaissance.</p>
<h2>12. Responsabilité</h2><p>Le client reste responsable du contenu qu’il fournit ou valide. DIG16 ne répond pas des préjudices indirects, notamment la perte de clientèle, de chiffre d’affaires ou d’image. La responsabilité de DIG16 est limitée aux sommes payées au titre des 12 derniers mois. Ces limites ne s’appliquent pas en cas de faute lourde ou intentionnelle.</p>
<h2>12 bis. Preuve</h2><p>Les parties conviennent que les échanges par email ou messagerie, les validations écrites du client et les documents signés électroniquement font preuve entre elles.</p>
<h2>13. Litiges</h2><p>Les parties cherchent d’abord une solution amiable, par écrit, pendant au moins 30 jours, en recourant si besoin au conciliateur de justice (gratuit). À défaut, le litige est porté devant la juridiction compétente selon les règles de droit commun. Droit français applicable.</p>
<h2>Annexe. Sous-traitance des données personnelles (formulaire du site)</h2><p>D’après le modèle de clauses de la CNIL. 1. Objet : DIG16 met en place le formulaire du site, qui transmet au client, par email, les messages des visiteurs. 2. Durée : celle du contrat. 3. Données : nom, coordonnées (téléphone ou email) et message laissés par le visiteur ; aucune donnée de santé ni bancaire n’est demandée. 4. Finalité : permettre au client de répondre aux demandes. 5. Instructions : DIG16 ne traite ces données que pour cette finalité et sur instruction écrite du client. 6. Conservation : DIG16 ne conserve pas les messages ; ils sont acheminés vers l’adresse email du client. 7. Confidentialité et sécurité : accès réservé, liaison chiffrée (HTTPS), comptes protégés par une validation en deux étapes. 8. Sous-traitant ultérieur : Cloudflare (hébergement du site et acheminement des messages), dans le compte du client ; tout autre sous-traitant est soumis à l’accord écrit du client. 9. Violation de données : DIG16 prévient le client sans délai après en avoir eu connaissance et l’aide à notifier la CNIL, si nécessaire, dans les 72 heures. 10. Droits des personnes : DIG16 aide le client à répondre aux demandes des visiteurs. 11. Fin du contrat : DIG16 supprime tout accès aux données et remet au client les fichiers de son site.</p>
</div>"""

DEVIS = f"""{bandeau("Création et suivi de sites internet", "Devis et bon de commande", "N° [AAAA-NNN] · Date : [jj/mm/aaaa] · Valable 30 jours")}
<div class="deux"><div class="cadre"><b>Prestataire</b><br>{EMETTEUR}<br>TVA non applicable, art. 293 B du CGI</div>
<div class="cadre"><b>Client</b><div class="champ"></div><div class="champ"></div><span class="petit">Nom de l’entreprise, adresse, SIREN</span></div></div>
<table><tr><th>Formule (cocher)</th><th>Contenu</th><th>Prix</th></tr>
<tr><td>☐ Essentiel</td><td>Site 5 pages sur mesure, hébergement, sécurité, mentions légales, 1 modification par mois, rapport mensuel</td><td class="n">49 €/mois</td></tr>
<tr><td>☐ Visibilité</td><td>Essentiel + fiche Google suivie, demandes d’avis, 3 modifications par mois</td><td class="n">79 €/mois</td></tr>
<tr><td>☐ Prestige</td><td>Site haut de gamme, voir le détail joint</td><td class="n">1 990 € ou 199 €/mois</td></tr>
<tr><td>☐ Achat</td><td>Site 5 pages livré, à vous pour toujours ; ☐ hébergement et suivi en option (hébergement, sécurité, surveillance et 1 petite modification par mois)</td><td class="n">690 € · option 15 €/mois</td></tr>
<tr><td>☐ 12 mois d’avance</td><td>Un mois offert : ☐ Essentiel 539 € · ☐ Visibilité 869 €</td><td class="n">une fois</td></tr></table>
<p><b>Création offerte</b> sur les formules mensuelles. Mise en ligne prévue au plus tard le <b>[date convenue ensemble]</b>, sous réserve de la réception et de la validation de vos contenus, jamais avant le 8e jour suivant la signature ; le premier mois est réglé avant la mise en ligne, au plus tôt ce 8e jour. Nom de domaine enregistré au nom du client et réglé par lui directement au bureau d’enregistrement (environ 10 € par an), avec l’aide de DIG16 pendant le rendez-vous.</p>
<p><b>Engagement</b> : 6 mois minimum (12 mois pour Prestige en mensuel et pour 12 mois d’avance), puis sans engagement. <b>14 jours pour changer d’avis</b> après la signature ; aucun paiement avant 8 jours.</p>
<p><b>Paiement</b> : prélèvement automatique mensuel ou virement mensuel, au choix ; à réception de facture pour un paiement en une fois. Escompte pour paiement anticipé : néant. {PENALITES}</p>
<p class="petit">Signer ce devis vaut commande et acceptation des conditions générales de vente jointes.</p>
<div class="sign"><div>Date, signature et cachet du client<br>précédés de « Bon pour accord »</div><div>Pour DIG16<br>(date et signature)</div></div>
<div style="break-before:page"></div>
<h2>Informations concernant l’exercice du droit de rétractation</h2>
<p><b>Droit de rétractation.</b> Vous avez le droit de vous rétracter du présent contrat sans donner de motif dans un délai de quatorze jours. Le délai de rétractation expire quatorze jours après le jour de la conclusion du contrat.</p>
<p>Pour exercer le droit de rétractation, vous devez nous notifier ([Prénom Nom] EI — « DIG16 », [Adresse], [téléphone], contact@dig16.fr) votre décision de rétractation du présent contrat au moyen d’une déclaration dénuée d’ambiguïté (par exemple, lettre envoyée par la poste ou courrier électronique). Vous pouvez utiliser le modèle de formulaire de rétractation ci-dessous mais ce n’est pas obligatoire.</p>
<p>Pour que le délai de rétractation soit respecté, il suffit que vous transmettiez votre communication relative à l’exercice du droit de rétractation avant l’expiration du délai de rétractation.</p>
<p><b>Effets de rétractation.</b> En cas de rétractation de votre part du présent contrat, nous vous rembourserons tous les paiements reçus de vous sans retard excessif et, en tout état de cause, au plus tard quatorze jours à compter du jour où nous sommes informés de votre décision de rétractation du présent contrat. Nous procéderons au remboursement en utilisant le même moyen de paiement que celui que vous aurez utilisé pour la transaction initiale, sauf si vous convenez expressément d’un moyen différent ; en tout état de cause, ce remboursement n’occasionnera pas de frais pour vous.</p>
<p>Si vous avez demandé de commencer la prestation de services pendant le délai de rétractation, vous devrez nous payer un montant proportionnel à ce qui vous a été fourni jusqu’au moment où vous nous avez informé de votre rétractation du présent contrat, par rapport à l’ensemble des prestations prévues par le contrat.</p>
<p>☐ Je demande que la prestation commence avant la fin du délai de rétractation (aucun paiement n’est demandé avant 8 jours). Je reconnais qu’après l’exécution entière du contrat, je ne disposerai plus du droit de rétractation.</p>
<p class="petit">Texte repris de l’annexe à l’article R221-3 du code de la consommation. Ce droit s’applique aux contrats signés hors des locaux de DIG16 avec une entreprise de cinq salariés au plus (article L221-3) ; DIG16 l’applique à tous ses clients.</p>
<div class="cadre" style="margin-top:5mm;border-style:dashed">
<h2 style="margin-top:1mm">Modèle de formulaire de rétractation</h2>
<p>(Veuillez compléter et renvoyer le présent formulaire uniquement si vous souhaitez vous rétracter du contrat.)</p>
<p>À l’attention de [Prénom Nom] EI — « DIG16 », [Adresse], contact@dig16.fr :</p>
<p>Je/nous (*) vous notifie/notifions (*) par la présente ma/notre (*) rétractation du contrat portant sur la prestation de services ci-dessous :</p>
<div class="champ"></div>
<p>Commandé le :</p><div class="champ"></div>
<p>Nom du (des) client(s) :</p><div class="champ"></div>
<p>Adresse du (des) client(s) :</p><div class="champ"></div>
<p>Signature du (des) client(s) (uniquement en cas de notification du présent formulaire sur papier) :</p><div class="champ" style="height:12mm"></div>
<p>Date :</p><div class="champ"></div>
<p class="petit">(*) Rayez la mention inutile.</p></div>"""

FACTURE = f"""{bandeau("Création et suivi de sites internet", "Facture", "N° [AAAA-NNN] (numérotation continue) · Date d’émission : [jj/mm/aaaa] · Date de la prestation : [période ou jj/mm/aaaa]")}
<div class="deux"><div class="cadre"><b>Prestataire</b><br>{EMETTEUR}</div>
<div class="cadre"><b>Client</b><br>[Nom de l’entreprise]<br>[Adresse du client]<br>SIREN [numéro du client]<br><span class="petit">N° de bon de commande : [si le client en a établi un]</span></div></div>
<p><b>Nature de l’opération</b> : prestation de services.</p>
<table><tr><th>Désignation</th><th>Quantité</th><th>Prix unitaire HT</th><th>Total HT</th></tr>
<tr><td>[Formule Essentiel — abonnement du mois de …]</td><td class="n">1</td><td class="n">[49,00 €]</td><td class="n">[49,00 €]</td></tr>
<tr><td>[Autre ligne si besoin]</td><td class="n"></td><td class="n"></td><td class="n"></td></tr>
<tr><td colspan="3"><b>Total HT</b> · réduction de prix : [néant ou montant]</td><td class="n"><b>[49,00 €]</b></td></tr>
<tr><td colspan="3"><b>Total à payer (TVA non applicable)</b></td><td class="n"><b>[49,00 €]</b></td></tr></table>
<p><b>TVA non applicable, art. 293 B du code général des impôts.</b></p>
<p><b>Date de règlement</b> : [jj/mm/aaaa] · Mode : [prélèvement / virement]. Escompte pour paiement anticipé : néant.</p>
<p>{PENALITES}</p>
<p class="petit">Mentions vérifiées sur Service Public Entreprendre (fiche F31808, vérifiée le 11 août 2026). Facture électronique obligatoire pour les micro-entreprises à partir du 1er septembre 2027 : il faudra alors aussi le SIREN du client, la nature de l’opération (déjà indiquée ici) et, le cas échéant, l’adresse de livraison.</p>"""


def ecrire():
    docs = [
        ("cgv-dig.html", "DIG16 — Conditions générales de vente", CGV, "Dig-CGV.pdf"),
        (
            "modele-devis.html",
            "DIG16 — Devis et bon de commande",
            DEVIS,
            "Dig-Modele-devis.pdf",
        ),
        (
            "modele-facture.html",
            "DIG16 — Modèle de facture",
            FACTURE,
            "Dig-Modele-facture.pdf",
        ),
    ]
    ident = identite.charger()
    if ident:  # HTML provisoire à côté des images de la charte, effacé après le PDF
        docs = [(f.replace(".html", "-prive.html"), t, c, pdf) for f, t, c, pdf in docs]
    for f, t, corps, _ in docs:
        open(os.path.join(SUP, f), "w").write(
            identite.remplir(TETE.replace("{t}", t) + corps + "</body></html>", ident)
        )
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        for f, _, _, pdf in docs:
            pg.goto("file://" + os.path.join(SUP, f))
            pg.emulate_media(media="print")
            attendre_polices(pg)
            pg.pdf(
                path=os.path.join(identite.sortie(SUP), pdf),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
            )
        b.close()
    if ident:
        for f, *_ in docs:
            os.remove(os.path.join(SUP, f))
    return docs


if __name__ == "__main__":
    for d in ecrire():
        print(d[0], "->", d[3])
