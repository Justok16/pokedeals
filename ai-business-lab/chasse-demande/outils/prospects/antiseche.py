import html
e=html.escape
S=[
("Qui êtes-vous ?",[
("Vous êtes qui exactement ?","Dig, une entreprise locale de création de sites pour les artisans et commerçants du coin. Vous avez un seul interlocuteur : moi."),
("Vous travaillez seul ?","Oui, avec des outils modernes qui me permettent d'être rapide et pas cher. Vous m'avez directement au téléphone, pas un standard."),
("Vous utilisez l'intelligence artificielle ?","Oui, pour aller plus vite sur la technique, c'est ce qui me permet ces prix. Mais chaque site est relu et vérifié par moi avant d'être en ligne."),
("Vous avez des références ?","Je démarre dans le secteur : c'est pour ça que je montre d'abord votre démo, gratuitement. Vous jugez sur pièce, sans rien signer."),
("Pourquoi vous m'appelez moi ?","J'ai vu que [votre site date un peu / on ne vous trouve pas sur Google]. J'ai préparé votre page d'accueil pour vous montrer la différence."),
]),
("Prix et engagement",[
("Combien ça coûte ?","À partir de 29 € par mois, 0 € de création. La formule la plus choisie est à 49 €, et 79 € si vous voulez plus de demandes via Google."),
("Pourquoi un abonnement ?","Parce qu'un site doit vivre : hébergement, sécurité, modifications, suivi Google. Tout est compris, vous n'avez rien à gérer."),
("Je préfère payer une fois.","C'est possible : 690 € une fois, le site est à vous. Le suivi à 15 € par mois est facultatif."),
("Je suis engagé combien de temps ?","6 mois minimum, puis vous êtes libre, sans engagement. Si vous restez, c'est parce que vous êtes content."),
("Comment j'arrête ?","Par un simple email. Le site et le nom de domaine sont à votre nom : vous partez avec."),
("Il y a des frais cachés ?","Non. Seul le nom de domaine, environ 10 € par an, est payé par vous directement : comme ça il vous appartient."),
("La TVA ?","Mes prix sont nets, [pas de TVA facturée tant que je suis en franchise de TVA — vérifier au démarrage]."),
("C'est plus cher / moins cher que X ?","Je ne compare pas les autres. Chez moi : pas de frais de création, 6 mois puis libre, site à votre nom. Regardez la démo et jugez."),
("Vous faites une remise ?","Mon prix est déjà serré. Par contre, si vous me recommandez un collègue qui signe, vous gagnez un mois offert."),
("Comment je paie ?","Chaque mois, avec une facture. [Mode de paiement exact à fixer : virement ou prélèvement]."),
]),
("Propriété et sécurité",[
("Le site est à qui ?","À vous. Le nom de domaine est à votre nom dès le premier jour. Si on arrête, je vous remets les fichiers."),
("Et si vous arrêtez votre activité ?","Votre domaine vous appartient et le site peut être déplacé en une heure chez n'importe quel hébergeur. Vous n'êtes jamais bloqué."),
("C'est hébergé où ?","Chez Cloudflare, un des plus gros hébergeurs au monde : rapide, sécurisé, disponible en permanence."),
("C'est sécurisé ?","Oui : cadenas https, pas de logiciel à mettre à jour ni de faille WordPress. C'est un site léger, très difficile à pirater."),
("Et mes données clients ?","Les demandes du formulaire arrivent directement dans votre boîte mail. Les mentions légales et la page de confidentialité sont faites."),
("J'aurai une adresse email pro ?","Oui, du type contact@votre-nom.fr, qui arrive dans votre boîte actuelle. Rien à changer à vos habitudes."),
]),
("Google et visibilité",[
("Je serai premier sur Google ?","Personne d'honnête ne peut le garantir. Ce que je garantis : un site construit dans les règles de Google, avec une page par service et par secteur, et une fiche Google soignée."),
("Combien de temps pour être visible ?","La fiche Google agit vite. Le site progresse sur quelques semaines à quelques mois, selon votre métier et votre concurrence."),
("C'est quoi la fiche Google ?","C'est la fiche qui apparaît sur Google Maps avec vos horaires, vos avis, vos photos. C'est souvent le premier contact avec un client."),
("Vous faites de la pub Google ?","Ce n'est pas inclus : je travaille le référencement naturel, qui ne coûte rien par clic. La pub peut s'ajouter plus tard si besoin."),
("Et les avis Google ?","Je vous aide à en demander à vos clients contents, avec un lien direct. Jamais de faux avis : c'est interdit et Google les supprime."),
("J'ai un mauvais avis, vous pouvez le supprimer ?","Non, mais on peut y répondre calmement et professionnellement : c'est ce qui rassure le plus les futurs clients."),
("On me trouve déjà sur Google.","Tant mieux ! Sur quelles recherches ? Le site sert à apparaître aussi sur « [métier] + [commune] » et à transformer la visite en appel."),
("Les réseaux sociaux, vous gérez ?","Ce n'est pas inclus. Je relie le site à votre Facebook ou Instagram. Pour publier régulièrement, on peut en parler."),
]),
("Contenu et fonctionnement",[
("Qui écrit les textes ?","Moi, à partir d'un entretien de 45 minutes avec vous. Vous relisez et validez tout avant la mise en ligne."),
("Et les photos ?","Les vôtres de préférence : vos chantiers, votre équipe. Si besoin, des photos d'illustration libres de droits en attendant."),
("En combien de temps c'est prêt ?","Une fois vos photos et informations reçues, comptez environ deux semaines. [Délai à confirmer selon la charge]."),
("Je peux modifier moi-même ?","Vous n'avez pas besoin : vous m'envoyez un message ou une photo et je m'en occupe (selon la formule, 1 à 3 modifications par mois)."),
("Ça marche sur téléphone ?","Il est d'abord pensé pour le téléphone, avec un bouton pour vous appeler directement. C'est là que vos clients vous cherchent."),
("Je peux recevoir des demandes de devis avec photos ?","Oui, le formulaire peut accepter des photos du chantier : vous arrivez chez le client en sachant déjà quoi faire."),
("Prise de rendez-vous en ligne ?","Oui, en option à 10 € par mois."),
("En anglais ?","Oui, version anglaise en option à 10 € par mois : utile pour la clientèle étrangère."),
("Vous faites de la boutique en ligne ?","Ce n'est pas dans les formules de base : sur devis si besoin."),
("Je saurai combien de personnes visitent ?","Oui, un rapport mensuel simple : visites, appels, demandes reçues."),
]),
("Changer de prestataire",[
("J'ai déjà un site chez [SoLocal / autre].","Je vous aide à trouver la date de fin et le préavis. On prépare le nouveau site avant, pour ne jamais être invisible."),
("Je vais perdre mon référencement ?","Non si c'est bien fait : on redirige vos anciennes pages vers les nouvelles et on garde le même nom de domaine si vous l'avez."),
("Mon ancien prestataire a mon nom de domaine.","On lui demande le transfert à votre nom, c'est votre droit. Je vous prépare le message à envoyer."),
("Mon site actuel me convient.","Parfait. Est-ce qu'il vous apporte des appels ? Si la démo ne fait pas mieux, je ne vous dérange plus."),
]),
("Objections",[
("J'ai assez de travail.","Tant mieux ! Le site sert alors à choisir vos chantiers : plus de demandes, vous gardez les meilleures, près de chez vous."),
("C'est trop cher.","Un seul chantier ou quelques clients de plus par an paient l'année. Et vous pouvez arrêter après 6 mois."),
("Le bouche-à-oreille me suffit.","Et vos clients vérifient sur Google avant d'appeler. Le site confirme ce qu'on leur a dit de vous."),
("Je n'ai pas le temps.","Il me faut 45 minutes avec vous, une fois. Tout le reste, je le fais."),
("Je vais réfléchir.","Bien sûr. Qu'est-ce qui vous fait hésiter ? … Je vous rappelle [jour] pour en parler ?"),
("Envoyez-moi une documentation.","Je vous envoie mieux : votre démo. Je vous rappelle [jour] pour avoir votre avis ?"),
("Je dois en parler à mon associé / ma femme.","Très bien, montrez-lui la démo. On se rappelle [jour] tous les deux, ou tous les trois ?"),
("J'ai un neveu qui fait des sites.","Super. La différence : je m'occupe aussi de Google, des avis et du suivi chaque mois, avec un engagement écrit."),
("Internet, ça ne marche pas dans mon métier.","Faisons le test : tapez « [métier] [commune] » sur votre téléphone. Ceux qui sortent en premier prennent les appels."),
]),
("Porte de sortie de pro",[
("Question que je ne sais pas","« Très bonne question. Je vérifie le point exact et je vous l'envoie par écrit aujourd'hui. » Puis me demander (souffleur)."),
("Question juridique ou fiscale pointue","« Je ne veux pas vous dire de bêtise : je vous confirme ça par écrit. »"),
("Le client veut une garantie de résultat","« Je ne promets pas ce que personne ne peut garantir. Je garantis le travail, la réactivité et la liberté de partir après 6 mois. »"),
]),
]
n=0;b=''
for t,qs in S:
    b+=f'<h2>{e(t)}</h2>'
    for q,r in qs:
        n+=1;b+=f'<div class="q"><b>{n}. {e(q)}</b><p>{e(r)}</p></div>'
H=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Dig — Antisèche des réponses</title><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Inter:wght@400;600&display=swap" rel="stylesheet"><style>
@page{{size:A4;margin:11mm 12mm}}body{{font-family:Inter,sans-serif;font-size:8.9pt;color:#1d1a17;line-height:1.38;margin:0}}
.couv{{background:#0d1330;color:#f4f1ea;border-radius:12px;padding:6mm 8mm;margin-bottom:3mm}}.couv h1{{font-family:Fraunces,serif;font-size:19pt;margin:1mm 0}}.couv p{{color:#c6cbe4;margin:0}}
.k{{color:#ff8a3d;font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:7.6pt}}
.col{{columns:2;column-gap:7mm}}h2{{font-family:Fraunces,serif;font-size:11.5pt;color:#c2410c;margin:3mm 0 1mm;break-after:avoid}}
.q{{break-inside:avoid;margin:0 0 1.8mm}}.q b{{display:block}}.q p{{margin:.3mm 0 0;color:#3d3833}}
.regles{{border:1px solid #e8e1d6;border-radius:8px;padding:2mm 3mm;margin-bottom:2mm;font-size:8.6pt}}
</style></head><body><div class="couv"><div class="k">Dig — à garder sous les yeux pendant l'appel</div><h1>Antisèche : {n} réponses prêtes</h1><p>Réponses courtes à dire telles quelles. Entre crochets : à adapter. Rien n'est promis qu'on ne puisse tenir.</p></div>
<div class="regles"><b>3 règles d'or :</b> 1) parler moins que le client ; 2) ramener toujours à la démo gratuite ; 3) finir chaque appel par une date de rappel précise.</div>
<div class="col">{b}</div></body></html>'''
open('antiseche.html','w').write(H);print(n)
