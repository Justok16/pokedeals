import html
e=html.escape
# (titre, intro, [ (question, type, aide) ])  type: l=ligne, L=plusieurs lignes, c=cases (options séparées par |), o=oui/non
S=[
("Identité de l'entreprise","Ces informations servent aux mentions légales et doivent être identiques partout sur internet (site, fiche Google, annuaires) : c'est un point clé du référencement local.",[
("Nom commercial exact (tel qu'il doit apparaître)","l",""),
("Raison sociale et forme juridique","l","Ex. SARL, SAS, entreprise individuelle"),
("SIRET","l",""),
("Adresse du siège","L",""),
("Afficher l'adresse sur le site et sur Google ?","c","Oui, adresse complète|Non, seulement la zone d'intervention"),
("Nom et fonction du dirigeant (responsable de la publication)","l",""),
("Téléphone(s) à afficher (fixe / portable)","l","Un seul numéro principal, le même partout"),
("Email de contact à afficher","l",""),
("Année de création / de reprise","l",""),
("Numéro de TVA intracommunautaire (si assujetti)","l",""),
("Assureur décennale / RC pro : nom, n° de contrat, zone couverte","L","À demander pour les métiers du bâtiment"),
]),
("Métier, services et offre","Chaque service important aura sa propre page : c'est ce qui permet d'apparaître sur Google pour chaque type de recherche.",[
("Votre métier en une phrase, comme vous le diriez à un client","L",""),
("Tous vos services (même les petits)","L","Lister tout, on triera ensuite"),
("Les 3 services qui rapportent le plus / que vous voulez développer","L","Ce seront les pages mises en avant"),
("Services que vous NE voulez PAS faire (ou plus)","L","Pour éviter les demandes inutiles"),
("Vos clients","c","Particuliers|Professionnels|Collectivités|Syndics / agences|Architectes"),
("Prix : afficher des tarifs ou des fourchettes ?","c","Oui, prix indicatifs|« À partir de »|Non, sur devis uniquement"),
("Devis gratuit ? Déplacement gratuit ? Sous quel délai ?","l",""),
("Urgences / dépannage : oui ? horaires ? zone ?","l",""),
("Délais habituels d'intervention ou de réalisation","l",""),
("Horaires d'ouverture (et jours de fermeture, congés annuels)","L",""),
("Moyens de paiement acceptés, facilités de paiement","l",""),
("Saisonnalité : périodes fortes / creuses","l","On adaptera les contenus et les posts Google"),
]),
("Zone d'intervention","Google classe les artisans selon la commune recherchée : plus la liste est précise, plus le site peut se positionner.",[
("Commune principale","l",""),
("Rayon d'intervention (en km) ou départements couverts","l",""),
("Liste des communes où vous voulez le plus de chantiers (10 à 20)","L","Des pages ou sections dédiées seront créées pour les plus importantes"),
("Communes / secteurs où vous ne voulez PAS aller","l",""),
]),
("Ce qui vous rend différent (les preuves)","Les visiteurs choisissent sur la confiance : chaque preuve concrète augmente le nombre d'appels.",[
("Votre histoire : comment l'entreprise est née, transmission familiale…","L",""),
("L'équipe : nombre de personnes, prénoms, rôles, ancienneté","L","Avec leur accord pour les afficher"),
("Qualifications et labels (RGE, Qualibat, QualiPac, Qualibois, Qualisol, Handibat, Artisan d'art…) : n° et dates de validité","L","Joindre les certificats ; vérifiés avant publication"),
("Adhésions (CAPEB, FFB, réseau, chambre de métiers, association de commerçants…)","l",""),
("Marques et fournisseurs avec lesquels vous travaillez","l","Les marques sont souvent recherchées sur Google"),
("Garanties offertes","l",""),
("Chiffres dont vous êtes fier (chantiers par an, clients, années…)","L","Uniquement des chiffres réels et vérifiables"),
("Vos 3 arguments principaux face à la concurrence","L",""),
("Avis clients : où en avez-vous ? (Google, PagesJaunes, Facebook…) combien ?","l",""),
("Clients prêts à laisser un témoignage (avec leur accord)","L",""),
]),
("Réalisations, photos et vidéos","Les photos réelles sont le contenu le plus efficace : elles rassurent et sont aussi référencées par Google Images.",[
("Photos de chantiers disponibles (avant / après si possible) : combien ? où sont-elles ?","L",""),
("Accord des clients pour montrer leurs chantiers (sans adresse)","o",""),
("Photos de l'équipe, de l'atelier, des véhicules, du magasin","o",""),
("Vidéos existantes","o",""),
("Besoin d'une séance photo ?","o",""),
("Pour chaque réalisation phare : type de travaux, commune, durée, difficulté, résultat","L","Chaque réalisation peut devenir un article référencé"),
]),
("Objectifs du site","Le site est construit autour de l'action que vous attendez du visiteur.",[
("Ce que le visiteur doit faire en priorité","c","Appeler|Demander un devis|Prendre rendez-vous|Réserver|Venir au magasin|Envoyer des photos de son projet"),
("Combien de nouvelles demandes par mois souhaitez-vous ? Combien pouvez-vous en traiter ?","l",""),
("Qui répond aux demandes ? Sous quel délai ?","l",""),
("Où recevoir les demandes du formulaire (email, SMS…) ?","l",""),
("Autres objectifs","c","Recruter|Trouver des sous-traitants|Présenter un magasin / showroom|Vendre des produits|Informer sur les aides"),
]),
("Référencement Google (SEO)","Section la plus importante pour être trouvé. On pense comme un client qui cherche sur son téléphone.",[
("Comment un client vous cherche-t-il sur Google ? (ses mots exacts)","L","Ex. « plombier Cognac », « changer chaudière prix », « couvreur urgence fuite »"),
("Questions que les clients vous posent le plus souvent (au moins 10)","L","Elles deviendront la FAQ et des articles : très efficace pour Google"),
("Vos principaux concurrents (noms, sites) et ce qu'ils font mieux ou moins bien","L",""),
("Fiche Google (Google Business Profile) : existe-t-elle ? qui a l'accès ? catégorie ? nombre d'avis ?","L","Réclamer l'accès avant le lancement"),
("Présence dans les annuaires (PagesJaunes, Mappy, annuaires métiers, chambre de métiers…) avec quelles coordonnées ?","L","Nom, adresse et téléphone doivent être identiques partout"),
("Ancien site : adresse ? qui a les accès (hébergeur, nom de domaine) ? pages qui marchaient bien ?","L","Pour rediriger les anciennes pages et garder le référencement acquis"),
("Réseaux sociaux (Facebook, Instagram, LinkedIn, YouTube…) : adresses et accès","L",""),
("Partenaires qui pourraient faire un lien vers votre site (fournisseurs, clubs sponsorisés, mairie, associations…)","L","Les liens depuis des sites locaux renforcent le classement"),
("Sujets de conseils que vous pourriez expliquer (entretien, aides, choix de matériaux…)","L","Pour les articles de blog"),
("Langues : clientèle étrangère (anglais, néerlandais…) ?","o","Important pour gîtes, restaurants, résidents étrangers"),
("Aides et financements que vos clients utilisent (MaPrimeRénov', CEE, éco-PTZ…)","l","Contenu très recherché ; informations vérifiées sur les sites officiels avant publication"),
]),
("Identité visuelle et style","",[
("Logo : fichiers disponibles (qualité, formats) ?","c","Oui, fichiers de qualité|Oui, mauvaise qualité|Non, à créer"),
("Couleurs de l'entreprise (véhicules, tenues, cartes de visite)","l",""),
("3 sites que vous aimez (même d'autres métiers) et pourquoi","L",""),
("Ce que vous ne voulez surtout pas","L",""),
("Ton du site","c","Vouvoiement, sérieux|Chaleureux, proche|Haut de gamme|Technique, expert"),
("Supports existants à reprendre (plaquettes, cartes, textes)","l",""),
]),
("Technique et accès","",[
("Nom de domaine souhaité (ex. nom-entreprise.fr) / existant et qui le possède","l","Le domaine est au nom du client"),
("Adresse email professionnelle souhaitée","l",""),
("Compte Google de l'entreprise (pour la fiche Google et les statistiques)","l","Ne jamais communiquer de mot de passe par écrit : accès donné par invitation"),
("Outils déjà utilisés (prise de rendez-vous, devis, réservation, caisse…)","l",""),
("Boutons souhaités","c","Appeler|SMS|WhatsApp|Itinéraire|Formulaire avec photos"),
]),
("Données personnelles et mentions légales","",[
("Qui reçoit et conserve les demandes des visiteurs ? Combien de temps ?","l","Pour la politique de confidentialité"),
("Mesure d'audience souhaitée ?","c","Statistiques sans cookies (recommandé)|Google Analytics (bandeau cookies obligatoire)"),
("Médiateur de la consommation (si clients particuliers)","l","Nom et coordonnées ; à vérifier au lancement"),
("Conditions générales / conditions de devis existantes","o",""),
]),
("Lancement et suivi","",[
("Date de mise en ligne souhaitée / événement à ne pas rater","l",""),
("Qui valide les textes et le site ?","l",""),
("Fréquence souhaitée des mises à jour (réalisations, actualités, posts Google)","c","Chaque semaine|Chaque mois|Quand il y a du nouveau"),
("Personne à contacter pour les photos et informations","l",""),
("Formule choisie et prix convenu","l",""),
]),
]
DOCS=["Logo (meilleure qualité disponible)","Photos de chantiers / réalisations","Photos de l'équipe et de l'atelier ou du magasin","Certificats RGE / Qualibat / labels","Attestation d'assurance décennale","Extrait Kbis ou avis de situation (SIRET)","Plaquettes, cartes de visite, anciens textes","Accès fiche Google (invitation)","Accès ancien site et nom de domaine (le cas échéant)","Liste des communes prioritaires","Liste des questions fréquentes des clients","Coordonnées de 3 clients témoins (avec accord)"]
def champ(t,a):
    if t=='l': return '<div class="ln"></div>'
    if t=='L': return '<div class="ln"></div><div class="ln"></div><div class="ln"></div>'
    if t=='o': return '<span class="ck">☐ Oui</span><span class="ck">☐ Non</span><div class="ln"></div>'
    if t=='c': return ''.join(f'<span class="ck">☐ {e(x)}</span>' for x in a.split('|'))+'<span class="ck">☐ Autre : ________</span>'
n=0;body=''
for i,(t,intro,qs) in enumerate(S):
    body+=f'<h2><span>{i+1}</span>{e(t)}</h2>'+(f'<p class="intro">{e(intro)}</p>' if intro else '')
    for q,ty,aide in qs:
        n+=1
        a=aide if ty!='c' else ''
        body+=f'<div class="q"><div class="t"><b>{n}.</b> {e(q)}</div>'+(f'<div class="aide">{e(a)}</div>' if a else '')+champ(ty,aide)+'</div>'
docs=''.join(f'<li>☐ {e(d)}</li>' for d in DOCS)
H=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Dig — Questionnaire de lancement du site</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Inter:wght@400;600&display=swap" rel="stylesheet"><style>
@page{{size:A4;margin:13mm 14mm 14mm}}*{{box-sizing:border-box}}body{{font-family:Inter,sans-serif;font-size:9.6pt;color:#1d1a17;line-height:1.45;margin:0}}
.couv{{background:#0d1330;color:#f4f1ea;border-radius:14px;padding:9mm}}.couv h1{{font-family:Fraunces,serif;font-size:24pt;margin:2mm 0}}.couv p{{color:#c6cbe4;margin:1mm 0}}
.k{{color:#ff8a3d;font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:8pt}}
.mode{{border:1px solid #e8e1d6;border-radius:10px;padding:3mm 4mm;margin:4mm 0}}.mode li{{margin:.6mm 0}}
.entete{{display:grid;grid-template-columns:1fr 1fr;gap:3mm 6mm;margin:3mm 0}}.entete div{{border-bottom:1px solid #999;padding-top:5mm;font-size:8.5pt;color:#5d5a66}}
h2{{font-family:Fraunces,serif;font-size:14pt;margin:6mm 0 1.5mm;break-after:avoid;display:flex;align-items:center;gap:3mm}}h2 span{{background:#ff8a3d;color:#fff;border-radius:50%;width:8mm;height:8mm;display:inline-grid;place-items:center;font-size:10pt}}
.intro{{color:#5d5a66;margin:0 0 2mm;font-size:9pt}}.q{{break-inside:avoid;margin:2.2mm 0}}.t{{font-weight:600}}.aide{{color:#7a7480;font-size:8.3pt;font-style:italic}}
.ln{{border-bottom:1px solid #c9c2b6;height:6.5mm}}.ck{{display:inline-block;margin:1mm 4mm 0 0;font-size:9pt}}
.docs{{columns:2;list-style:none;padding:0}}.docs li{{margin:1mm 0}}.page{{break-before:page}}.pied{{color:#7a7480;font-size:8pt;margin-top:5mm}}
</style></head><body>
<div class="couv"><div class="k">Dig — dossier client</div><h1>Questionnaire de lancement du site</h1><p>{n} questions pour un site qui convertit et un référencement Google au maximum de ses possibilités. À remplir ensemble pendant l'entretien (45 à 60 minutes).</p></div>
<div class="entete"><div>Entreprise</div><div>Date de l'entretien</div><div>Interlocuteur</div><div>Formule envisagée</div></div>
<div class="mode"><b>Mode d'emploi pour l'entretien</b><ul>
<li>Commencer par les sections 2, 3 et 7 : ce sont elles qui font le chiffre d'affaires du client (services, zone, recherches Google).</li>
<li>Faire parler le client avec ses propres mots : ses expressions deviennent les mots-clés du site.</li>
<li>Ce qui manque est noté dans la liste des documents (dernière page) et envoyé par le client après le rendez-vous.</li>
<li>Rien n'est publié sans vérification : qualifications, chiffres et avis sont contrôlés avant la mise en ligne.</li></ul></div>
{body}
<h2 class="page"><span>✓</span>Documents à récupérer après le rendez-vous</h2><ul class="docs">{docs}</ul>
<h2><span>✎</span>Notes libres</h2>{'<div class="ln"></div>'*14}
<p class="pied">Dig — création et suivi de sites internet. Les informations recueillies servent uniquement à la réalisation du site du client.</p>
</body></html>'''
open('questionnaire.html','w').write(H);print(n)
