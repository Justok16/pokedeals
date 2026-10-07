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
import os

ICI = os.path.dirname(os.path.abspath(__file__))
SUP = os.path.normpath(os.path.join(ICI, "..", "supports"))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

EMETTEUR = "[Prénom Nom] EI — « DIG16 »<br>[Adresse]<br>SIREN [numéro à l’immatriculation]<br>contact@dig16.fr"
CSS = """@page{size:A4;margin:13mm 14mm 14mm}*{box-sizing:border-box}
body{font-family:Inter,sans-serif;font-size:9.4pt;color:#1d1a17;line-height:1.45;margin:0}
.couv{background:#0d1330;color:#f4f1ea;border-radius:12px;padding:6mm 8mm;margin-bottom:4mm;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.couv h1{font-family:Fraunces,serif;font-size:20pt;margin:1mm 0}.couv p{color:#c6cbe4;margin:.5mm 0}
.k{color:#ff8a3d;font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:7.8pt}
h2{font-family:Fraunces,serif;font-size:11.5pt;margin:4mm 0 1mm;break-after:avoid}
p,li{margin:.8mm 0}ul{padding-left:5mm;margin:1mm 0}
table{width:100%;border-collapse:collapse;margin:2mm 0;font-size:9pt}th,td{border:1px solid #d8d0c3;padding:1.6mm 2mm;text-align:left;vertical-align:top}
th{background:#f4efe6;-webkit-print-color-adjust:exact;print-color-adjust:exact}td.n{text-align:right;white-space:nowrap}
.deux{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin:2mm 0}.cadre{border:1px solid #d8d0c3;border-radius:8px;padding:3mm 4mm}
.champ{border-bottom:1px solid #999;height:6mm;margin:1mm 0}.petit{color:#5d5a66;font-size:8.2pt}
.sign{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:4mm}.sign div{border:1px solid #d8d0c3;border-radius:8px;height:26mm;padding:2mm 3mm;font-size:8.4pt;color:#5d5a66}
.cgv{columns:2;column-gap:7mm;font-size:8.5pt;line-height:1.37}.cgv h2{font-size:10pt;margin:2.4mm 0 .6mm}.cgv p{margin:.5mm 0;text-align:justify}"""
TETE = (
    '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{t}</title>'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Inter:wght@400;600&display=swap" rel="stylesheet">'
    "<style>" + CSS + "</style></head><body>"
)

PENALITES = (
    "En cas de retard de paiement, des pénalités sont dues de plein droit, sans rappel préalable, au taux "
    "appliqué par la Banque centrale européenne à son opération de refinancement la plus récente, majoré de "
    "10 points, ainsi qu’une indemnité forfaitaire pour frais de recouvrement de 40 € par facture."
)

CGV = f"""<div class="couv"><div class="k">DIG16 — création et suivi de sites internet</div><h1>Conditions générales de vente</h1>
<p>Applicables à toute commande passée par un professionnel. Version du [date de l’immatriculation].</p></div>
<div class="cgv">
<h2>1. Prestataire</h2><p>{EMETTEUR.replace("<br>", ", ")}. TVA non applicable, art. 293 B du code général des impôts.</p>
<h2>2. Objet</h2><p>DIG16 crée, héberge et suit des sites internet pour les professionnels (entreprises, artisans, commerçants). Les présentes conditions s’appliquent à toute commande ; elles prévalent sur tout autre document, sauf accord écrit contraire.</p>
<h2>3. Formules et prix</h2><p>Les formules et leurs prix sont ceux du devis signé : Essentiel 49 € par mois, Visibilité 79 € par mois, Prestige 1 990 € une fois ou 199 € par mois, Achat 690 € une fois (hébergement et suivi en option à 15 € par mois). Douze mois payés d’avance : un mois offert (Essentiel 539 €, Visibilité 869 €). Les prix sont nets : TVA non applicable. Le nom de domaine est enregistré au nom du client et à sa charge (environ 10 € par an).</p>
<h2>4. Commande et délais</h2><p>La commande est formée par la signature du devis-bon de commande. Pour les formules mensuelles, la création du site est offerte. Le site est mis en ligne 7 jours après la réception de tous les contenus et leur validation par le client (3 semaines pour Prestige), et jamais avant le 8e jour suivant la signature. Le premier mois est réglé avant la mise en ligne, au plus tôt le 8e jour suivant la signature.</p>
<h2>5. Droit de changer d’avis</h2><p>Le client dispose de 14 jours à compter de la signature pour se rétracter, sans motif ni frais, par simple email ou courrier. Aucun paiement n’est demandé avant 8 jours. Ce droit, prévu par la loi pour les contrats signés hors des locaux de DIG16, est appliqué à tous les clients.</p>
<h2>6. Durée et résiliation</h2><p>Les formules mensuelles comportent un engagement minimal de 6 mois (12 mois pour Prestige en paiement mensuel et pour les 12 mois payés d’avance), qui couvre la création offerte. Ensuite, le contrat se poursuit sans engagement : le client peut y mettre fin à tout moment, par email, avec effet à la fin du mois en cours. Le client peut passer à tout moment à une formule supérieure, et à une formule inférieure à la fin de son engagement minimal.</p>
<h2>7. Paiement</h2><p>Formules mensuelles : prélèvement SEPA mensuel sur mandat signé par le client, une facture chaque mois ; le client est prévenu du montant et de la date au moins 2 jours avant chaque prélèvement. Formules payées en une fois : à réception de la facture, au plus tard dans les 30 jours. Escompte pour paiement anticipé : néant. {PENALITES}</p>
<h2>8. Réalisation et modifications</h2><p>DIG16 rédige les textes à partir de l’échange avec le client, qui relit et valide tout avant la mise en ligne. Le client fournit des informations exactes et des photos dont il détient les droits. Une modification est un changement de contenu sur une page existante (texte, photo, horaires, prix, actualité) ; une nouvelle page ou une nouvelle fonction fait l’objet d’un devis. Les demandes, envoyées par email, sont traitées sous 3 jours ouvrés, dans la limite prévue par la formule (Essentiel : 1 par mois ; Visibilité : 3 par mois ; Prestige : selon le devis) ; les modifications non utilisées ne se reportent pas. La correction d’une erreur de DIG16 ne compte pas comme une modification.</p>
<h2>9. Propriété</h2><p>Le nom de domaine est enregistré au nom du client. DIG16 cède au client, au fur et à mesure des paiements et au plus tard à la fin de l’engagement minimal (à la livraison pour la formule Achat), ses droits d’auteur sur le site réalisé pour lui (textes, mise en page, graphisme et code créés par DIG16) : le droit de <b>reproduction</b>, le droit de <b>représentation</b> et le droit d’<b>adaptation</b>, pour tout usage lié à la présentation et à la promotion de l’activité du client, sur internet et tout support numérique, pour le monde entier et pour toute la durée légale de protection. Les photos et contenus fournis par le client restent les siens. En partant, le client reçoit l’ensemble des fichiers de son site et DIG16 l’aide à le transférer chez l’hébergeur de son choix.</p>
<h2>10. Hébergement et disponibilité</h2><p>DIG16 fait ses meilleurs efforts pour que le site reste accessible et sécurisé ; une interruption ponctuelle pour maintenance ou du fait de l’hébergeur peut survenir. DIG16 ne promet pas de position dans les résultats de Google.</p>
<h2>11. Données personnelles</h2><p>DIG16 traite les données du client et de ses visiteurs uniquement pour réaliser et suivre le site, conformément au RGPD. Chaque site comprend ses mentions légales et ses informations sur les données ; aucun traceur publicitaire n’est installé.</p>
<h2>12. Responsabilité</h2><p>Le client reste responsable du contenu qu’il fournit ou valide. La responsabilité de DIG16 est limitée aux sommes payées au titre des 12 derniers mois.</p>
<h2>13. Litiges</h2><p>Les parties cherchent d’abord une solution amiable. À défaut, le litige est porté devant la juridiction compétente selon les règles de droit commun. Droit français applicable.</p>
</div>"""

DEVIS = f"""<div class="couv"><div class="k">DIG16 — création et suivi de sites internet</div><h1>Devis et bon de commande</h1>
<p>N° [AAAA-NNN] · Date : [jj/mm/aaaa] · Valable 30 jours</p></div>
<div class="deux"><div class="cadre"><b>Prestataire</b><br>{EMETTEUR}<br>TVA non applicable, art. 293 B du CGI</div>
<div class="cadre"><b>Client</b><div class="champ"></div><div class="champ"></div><span class="petit">Nom de l’entreprise, adresse, SIREN</span></div></div>
<table><tr><th>Formule (cocher)</th><th>Contenu</th><th>Prix</th></tr>
<tr><td>☐ Essentiel</td><td>Site 5 pages sur mesure, hébergement, sécurité, mentions légales, 1 modification par mois, rapport mensuel</td><td class="n">49 €/mois</td></tr>
<tr><td>☐ Visibilité</td><td>Essentiel + fiche Google suivie, demandes d’avis, 3 modifications par mois</td><td class="n">79 €/mois</td></tr>
<tr><td>☐ Prestige</td><td>Site haut de gamme, voir le détail joint</td><td class="n">1 990 € ou 199 €/mois</td></tr>
<tr><td>☐ Achat</td><td>Site 5 pages livré, à vous pour toujours ; ☐ hébergement et suivi en option</td><td class="n">690 € · option 15 €/mois</td></tr>
<tr><td>☐ 12 mois d’avance</td><td>Un mois offert : ☐ Essentiel 539 € · ☐ Visibilité 869 €</td><td class="n">une fois</td></tr></table>
<p><b>Création offerte</b> sur les formules mensuelles. Mise en ligne 7 jours après réception et validation de vos contenus (3 semaines pour Prestige), jamais avant le 8e jour suivant la signature ; le premier mois est réglé avant la mise en ligne, au plus tôt ce 8e jour. Nom de domaine au nom du client, à sa charge (environ 10 € par an).</p>
<p><b>Engagement</b> : 6 mois minimum (12 mois pour Prestige en mensuel et pour 12 mois d’avance), puis sans engagement. <b>14 jours pour changer d’avis</b> après la signature ; aucun paiement avant 8 jours.</p>
<p><b>Paiement</b> : prélèvement automatique mensuel, ou à réception de facture pour un paiement en une fois. Escompte pour paiement anticipé : néant. {PENALITES}</p>
<p class="petit">Signer ce devis vaut commande et acceptation des conditions générales de vente jointes.</p>
<div class="sign"><div>Date, signature et cachet du client<br>précédés de « Bon pour accord »</div><div>Pour DIG16<br>(date et signature)</div></div>
<div style="break-before:page"></div>
<h2>Informations concernant l’exercice du droit de rétractation</h2>
<p><b>Droit de rétractation.</b> Vous avez le droit de vous rétracter du présent contrat sans donner de motif dans un délai de quatorze jours. Le délai de rétractation expire quatorze jours après le jour de la conclusion du contrat.</p>
<p>Pour exercer le droit de rétractation, vous devez nous notifier ([Prénom Nom] EI — « DIG16 », [Adresse], [téléphone], contact@dig16.fr) votre décision de rétractation du présent contrat au moyen d’une déclaration dénuée d’ambiguïté (par exemple, lettre envoyée par la poste ou courrier électronique). Vous pouvez utiliser le modèle de formulaire de rétractation ci-dessous mais ce n’est pas obligatoire.</p>
<p>Pour que le délai de rétractation soit respecté, il suffit que vous transmettiez votre communication relative à l’exercice du droit de rétractation avant l’expiration du délai de rétractation.</p>
<p><b>Effets de rétractation.</b> En cas de rétractation de votre part du présent contrat, nous vous rembourserons tous les paiements reçus de vous sans retard excessif et, en tout état de cause, au plus tard quatorze jours à compter du jour où nous sommes informés de votre décision de rétractation du présent contrat. Nous procéderons au remboursement en utilisant le même moyen de paiement que celui que vous aurez utilisé pour la transaction initiale, sauf si vous convenez expressément d’un moyen différent ; en tout état de cause, ce remboursement n’occasionnera pas de frais pour vous.</p>
<p>Si vous avez demandé de commencer la prestation de services pendant le délai de rétractation, vous devrez nous payer un montant proportionnel à ce qui vous a été fourni jusqu’au moment où vous nous avez informé de votre rétractation du présent contrat, par rapport à l’ensemble des prestations prévues par le contrat.</p>
<p>☐ Je demande que la prestation commence avant la fin du délai de rétractation (aucun paiement n’est demandé avant 8 jours).</p>
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

FACTURE = f"""<div class="couv"><div class="k">DIG16 — création et suivi de sites internet</div><h1>Facture</h1>
<p>N° [AAAA-NNN] (numérotation continue) · Date d’émission : [jj/mm/aaaa] · Date de la prestation : [période ou jj/mm/aaaa]</p></div>
<div class="deux"><div class="cadre"><b>Prestataire</b><br>{EMETTEUR}</div>
<div class="cadre"><b>Client</b><br>[Nom de l’entreprise]<br>[Adresse]<br>SIREN [numéro du client]<br><span class="petit">N° de bon de commande : [si le client en a établi un]</span></div></div>
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
    for f, t, corps, _ in docs:
        open(os.path.join(SUP, f), "w").write(
            TETE.replace("{t}", t) + corps + "</body></html>"
        )
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        for f, _, _, pdf in docs:
            pg.goto("file://" + os.path.join(SUP, f))
            pg.wait_for_timeout(800)
            pg.pdf(
                path=os.path.join(SUP, pdf),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
            )
        b.close()
    return docs


if __name__ == "__main__":
    for d in ecrire():
        print(d[0], "->", d[3])
