# Parcours vérifiés dans les applis (guidage pas à pas de l'utilisateur)

Créé le 11/10/2026 après la remarque de l'utilisateur : des indications de menus données de mémoire étaient
fausses (menus renommés, options disparues), ce qui lui a fait perdre du temps.

## Méthode obligatoire avant de guider l'utilisateur dans une appli ou un site

1. **Le faire soi-même d'abord** si un connecteur ou un outil le permet (Metricool, Gmail, Drive, Vercel, GitHub…).
   L'utilisateur n'agit que pour ce qui exige son compte ou son identité.
2. **Chercher ici** si le parcours a déjà été vérifié (tableau ci-dessous). Si oui, le donner tel quel.
3. Sinon, **lire la page d'aide officielle actuelle** de l'éditeur (recherche web, date de la page) avant d'écrire
   les étapes, et citer le lien. Ne jamais décrire un menu de mémoire.
4. **Un écran à la fois** quand le parcours n'est pas vérifié : demander une capture de l'écran de départ, donner
   seulement la ou les 2 prochaines touches, puis attendre la capture suivante. Dire clairement « je n'ai pas vu
   cet écran, envoie-moi une capture si ça ne correspond pas ».
5. **Prévoir l'alternative** dès le départ (ex. « si l'option n'existe pas, on passe par X »).
6. **Vérifier le résultat soi-même** quand c'est possible (API, page publique), sans conclure trop vite : une
   absence d'erreur n'est pas une preuve (leçon Threads/Metricool du 11/10).
7. **Consigner ici** chaque parcours confirmé par une capture de l'utilisateur, avec la date.

## Parcours confirmés (captures de l'utilisateur)

| Appli | But | Parcours exact | Vu le |
|---|---|---|---|
| Metricool (appli Android) | Voir / changer la marque active | Rond du logo de la marque **en bas à droite** → liste « Marques » (⚙️ à droite de chaque marque) | 11/10/2026 |
| Metricool (appli Android) | Relier un réseau | Rond en bas à droite → ⚙️ de la marque → « Paramètres des marques » → **Connexions** → « Connecter » sur la ligne du réseau | 11/10/2026 |
| Metricool (appli Android) | Piège | L'appli peut être ouverte sur une **autre marque/compte** (« Marque vide ») : toujours vérifier le nom de la marque avant de connecter | 11/10/2026 |
| Metricool (API) | Piège | `getBrandSettings` n'affiche que Facebook/Instagram dans `networksData` ; une publication acceptée sur un réseau ne prouve pas qu'il est relié | 11/10/2026 |
| Instagram (Android) | Lien cliquable dans la bio | Modifier le profil → **Liens** → Ajouter un lien → Ajouter un lien externe (le texte de la bio n'est jamais cliquable) | 11/10/2026 |
| Instagram (Android) | Piège | « Nom » (affiché) ≠ « Nom d'utilisateur » (identifiant `dig16fr`, à ne jamais changer) ; ancien identifiant récupérable 14 jours | 11/10/2026 |
| Threads (Android) | Ajouter le profil DIG16 | S'ouvre sur le compte personnel ; profil DIG16 ajouté depuis le compte Instagram `dig16fr` ; Modifier le profil : Nom, Bio, Centres d'intérêt, Liens, Confidentialité | 11/10/2026 |
| TikTok (Android) | Changer le nom | Modifier le profil → Nom : **bloqué 7 jours** après la création du compte | 11/10/2026 |
| TikTok (Android) | Compte professionnel | **N'existe plus** dans Paramètres → Compte ; seul « Deviens un compte Entreprise vérifié » (documents exigés). Metricool accepte le **compte personnel** (1re ligne TikTok de Connexions) | 11/10/2026 |
| TikTok (Android) | Mot de passe | Paramètres et confidentialité → Compte → **Mot de passe** (code envoyé par e-mail) | 11/10/2026 |
| YouTube | Commentaire épinglé sur un Short | Ouvrir le Short → bulle 💬 à droite → écrire → ⋮ du commentaire → Épingler | 11/10/2026 |
| YouTube Studio | Avertissement règlement | Bandeau en haut : formulation « mise en garde » + formation de 7 questions (expire en 90 jours) | 11/10/2026 |
| Metricool (appli Android) | Relier la fiche Google | Connexions → ligne « Google Business Profile » → Connecter (fiche « Dig16 » reliée) | 12/10/2026 |
| Metricool (appli Android) | Relier YouTube | Connexions → ligne « YouTube, Connecter un canal » → chaîne « DIG16 » | 12/10/2026 |
| X (navigateur, inscription) | Piège | `dig16fr` déjà pris ; `dig16charente` disponible ; le **Nom refuse tout chiffre** à l'inscription (« Erreur lors de la validation du nom », trouvé par l'utilisateur) : s'inscrire avec un nom sans chiffre puis le changer dans Modifier le profil | 12/10/2026 |
| Google Search Console (navigateur) | Ajouter et valider le site | Accueil → « Ajouter un site Web » → « Préfixe d'URL » `https://dig16.fr/` → « Balise HTML » → Claude insère la balise dans `site-dig/index.html` et publie → « Valider » (propriété validée) | 12/10/2026 |
| Google Search Console | Menu de gauche | Vue d'ensemble, Insights, Performances, Inspection de l'URL ; Indexation : Pages, **Sitemaps**, Suppressions | 12/10/2026 |
| Google Search Console | Sitemap et indexation | Sitemaps → saisir `sitemap.xml` → ENVOYER (1er état « Impossible de récupérer » sur propriété neuve, normal) ; barre « Inspecter n'importe quelle URL » → TEST EN LIGNE (« Google a accès à cette URL ») → DEMANDER UNE INDEXATION (« Indexation demandée ») | 12/10/2026 |
| Bing Webmaster Tools (navigateur) | Ajouter le site | bing.com/webmasters → cadre gauche « Google Search Console » → **Importer** → compte Google → autoriser → arrive sur l'accueil `dig16.fr/` (« données en cours de traitement, jusqu'à 48 h ») ; menu gauche : Accueil, Performances, Inspection d'URL, **Plans de site**, IndexNow… | 12/10/2026 |
| Bing Webmaster Tools | Sitemap | Menu gauche « Plans de site » : `https://dig16.fr/sitemap.xml` déjà repris de Google par l'import, statut « Traitement » (rien à envoyer) | 12/10/2026 |
| Bing Places (navigateur Brave) | Piège | « Importer à partir de votre fiche d'établissement Google » **revient en boucle** sur « Configurez votre profil » : passer par « Créez votre profil Bing en trois étapes » | 12/10/2026 |
| Bing Places | Créer la fiche | Trouvez votre entreprise (recherche « Dig16 » → « Nous n'avons pas pu trouver ») → **Créer une liste** → nom + catégorie principale → … → fiche « Vérification en cours », **code par courrier** | 12/10/2026 |
| Bing Places | Piège | L'adresse saisie s'affiche en entier ; **Détails Essentiel non modifiables avant vérification** (« Vous pourrez … mettre à jour … une fois votre entreprise vérifiée ») ; masquer l'adresse ensuite (option + zones desservies obligatoires, aide officielle) | 12/10/2026 |
| PagesJaunes / Solocal Manager | Créer la fiche | pagesjaunes.fr/plusdeservices/gerer-ma-fiche-pagesjaunes → « C'est parti, je crée un compte » → « Continuer avec Google » → « Recherchez votre établissement » → fiche créée en « Accès limité » (mode public) | 12/10/2026 |
| Solocal Manager | Piège | Bouton « Valider mon établissement » sans effet (2 navigateurs) ; aide officielle : 3 voies (bandeau, notification « Je m'authentifie », « Mes fiches établissements ») ; le contact n'est **que par téléphone** : bas du menu « Mon compte, mes factures, contacter solocal » → Contacter solocal → « Afficher le numéro » | 12/10/2026 |
| Apple Business (ex-Business Connect, navigateur, sans iPhone) | Valider l'organisation | business.apple.com → bandeau « Valider › » → méthode 1 : document (Kbis) ; méthode 2 : « Validation d'un domaine » → dig16.fr → « Générer un enregistrement TXT » → Copier → « Envoyer pour validation » une fois le TXT en ligne (aide officielle support.apple.com/fr-fr/guide/business/axm402206497) | 12/10/2026 |
| Cloudflare (navigateur) | Ajouter un TXT | dash.cloudflare.com → dig16.fr → menu DNS → Records → « + Add record » → Type TXT, Name `@`, Content = code, TTL Auto → Save ; vérifié en ligne par Claude (dns.google) en moins d'une minute | 12/10/2026 |
| Apple Business | Piège | Validation de domaine : la liste ne proposait que `www.dig16.fr` (CNAME, aucun TXT possible) → « Envoyer pour validation » restait grisé ; solution : méthode 2 = document (attestation de contrat d'énergie au nom du titulaire, adresse du siège), puis envoi accepté | 12/10/2026 |
| Metricool (appli Android) | Piège | Connexions → « Web / Blog » → Connecter : « pas encore prise en charge depuis l'application mobile » → passer par le site metricool.com sur ordinateur. Le code de suivi a été installé par Claude sans attendre (format du code officiel tiré de l'extension WordPress Metricool, identifiant de marque lu dans getBrandSettings) | 12/10/2026 |
| Metricool (navigateur, app.metricool.com) | Relier le site web | Marque DIG16 → Analyses → menu « Gérer les connexions » → bloc **Web** : le domaine était resté « localhost » (cause des 0 visite) → icône crayon → « Nom du site web » : `https://dig16.fr` → Accepter (« Le nom du site a été mis à jour avec succès ») ; balise déjà en place (`site-dig/mesure.js`), visites de test du 13/10 acceptées (200) ; chiffres du jour visibles le lendemain, onglet « En temps réel » pour le direct | 13/10/2026 |
| Nouvel Outlook pour Windows | Ajouter contact@dig16.fr (OVH MX Plan) | « Ajouter un compte » → adresse → mot de passe → « Afficher plus » → IMAP ssl0.ovh.net 993 SSL/TLS, SMTP ssl0.ovh.net 465 SSL/TLS, utilisateur = adresse complète (guide OVH du 08/06/2026) ; compte ajouté par l'utilisateur | 13/10/2026 |
| Nouvel Outlook pour Windows | Signature HTML d'un compte | Roue dentée → « Signatures de comptes » → choisir le compte → + Ajoutez une signature → coller → cases nouveaux messages / réponses → Enregistrer. **Piège** : ouvrir le fichier .html dans le **navigateur** (clic droit → Ouvrir avec → Edge) et copier la signature affichée ; sinon Outlook reçoit le code | 13/10/2026 |
| Nouvel Outlook pour Windows | Remplacer une signature existante | Écran « Modifier la signature » (nom de la signature en haut, contenu dessous, cases « Définir les valeurs par défaut des nouveaux messages » et « … des réponses et des transferts ») ; **piège** : après un collage, « Enregistrer » peut rester grisé → taper un espace puis l'effacer pour l'activer ; source à copier : page Artifact privée (un .html envoyé par l'appli arrive en PNG) | 19/10/2026 |
| Outlook pour Android | Signature d'un compte | Menu (icône du compte en haut à gauche) → roue dentée en bas à gauche → Paramètres → « Paramètres rapides » → **Signatures** → interrupteur « Signature par compte » activé → toucher la ligne du compte → remplacer « Envoyé à partir de Outlook pour Android » par la signature en texte simple (captures de l'utilisateur) | 18/10/2026 |
| OpenSEO (navigateur) | Relier Search Console | Projet DIG16 créé par Claude (app.openseo.so/p/9d8e84cb-…) → l'utilisateur ouvre le projet et autorise Google → `get_search_console_performance` renvoie `siteUrl: https://dig16.fr/` (lecture seule, « uses no credits ») | 12/10/2026 |
| Instagram (appli, compte pro dig16fr) | Lien de la bio | Jusqu'à **5 liens** cliquables : « Modifier le profil » → **Liens** → ajouter une adresse ; réordonner par « Options » → « Réorganiser les liens » (aide officielle <https://help.instagram.com/362497417173378/>, lue le 19/10 : « You can add up to five websites… by going to Edit Profile and selecting Links »). **Piège** : une adresse écrite dans le texte de la bio n'est **pas** cliquable (capture du 19/10 : `https://dig16.fr/ig` dans le texte, seul `dig16.fr/guide` du champ Liens est cliquable) | 19/10/2026 |
| TikTok (appli, compte @dig16fr) | Qui peut m'écrire (messages directs) | **Profil** → **Menu ☰** → **Paramètres et confidentialité** → **Confidentialité** → **Messages directs** → **Paramètres d'autorisation** → « Contacts potentiels » et « Autres sur TikTok » sur **Demandes** (jamais « Ne pas recevoir »). Même écran « Messages directs » : **Mode sécurisé** (les messages jugés douteux vont dans « Demandes filtrées » **sans notification**), Statut de lecture, Mots-clés filtrés. Relever : **Boîte de réception** → **Demandes de message** (+ **Demandes filtrées**) → Accepter. Aide officielle <https://www.tiktok.com/support/faq_detail?id=7543897461052529158> ; **libellés confirmés par les captures de l'utilisateur du 19/10 à 1 h 16** (les deux lignes déjà sur « Demandes ») | 19/10/2026 |
| Google Maps (appli Android, compte qui gère la fiche) | Gérer la fiche Dig16 | Onglet du bas à droite **« Entreprise »** (l'aide Google dit « Établissement ») → écran « Votre établissement » : Dig16, badge bleu validé, efficacité 91 % ; boutons **Éditer la fiche**, Publicité, Ajouter photo, Horaires d'ouverture ; « Plus » déplie Éditer services, Questions, Ajouter une offre, Ajouter un événement, Votre actualité, Logo, Photo de couverture ; plus bas Performances (16 vues en octobre) et carte « Finalisez l'annonce » | 19/10/2026 |
| Google Maps (appli Android) | Publier une actualité sur la fiche | « Entreprise » → « Plus » → **« Votre actualité »** → écran « Votre actualité » : encadré règles Google, zone photo « Mettez votre post en valeur grâce à une photo », champ « Rédigez votre post », « Ajouter un bouton (facultatif) » (liste, « Aucun » par défaut), boutons **Aperçu** et **Publier** | 21/10/2026 (capture 0 h 49) |
| Google Maps (appli Android) | Date d'ouverture de la fiche | « Entreprise » → **Éditer la fiche** → écran « Informations sur l'établissement », onglets À propos / Contact / Emplacement / Horaires ; dans **À propos** : Nom, Catégorie, Description, puis **« Date de création »** (l'aide Google dit « Date d'ouverture ») avec un crayon ; valeur au 19/10 : « octobre 2026 » ; puis Coordonnées (téléphone, chat) | 19/10/2026 |
| Google Recherche (ordinateur, compte qui gère la fiche) | Modifier la fiche | Chercher « Dig16 » → encadré « Votre établissement » → **Éditer la fiche** → fenêtre « Informations sur l'établissement », onglets À propos / Contact / Emplacement / Horaires / Plus ; **Contact** : téléphone, chat, **Site Web**, **Profils sur les réseaux sociaux** (5 adresses acceptées le 19/10 : X, TikTok, YouTube, Instagram, Facebook ; **Threads n'est pas proposé** par Google, confirmé par l'utilisateur) | 19/10/2026 |

### Buffer : relier Facebook, Instagram et TikTok (confirmé par captures le 19/10/2026)

Source : aide Buffer « Connecting your channels », « Connecting your Instagram account », « Using TikTok with Buffer » (lues le 19/10).
1. Se connecter au réseau voulu dans un autre onglet (pour TikTok : le compte DIG16 ouvert, Buffer prend celui-là sans choix).
2. publish.buffer.com, à gauche « Connect more channels » → icône du réseau.
3. Facebook : tout autoriser, choisir la page DIG16. Instagram : « Connect Instagram through Facebook » en bas de la fenêtre.
4. Après chaque réseau, fenêtre « How many times a week would you like to post? » → 5 times/week → Next → « Got It » (heures indicatives seulement).
Résultat le 19/10 : « 3/3 channels connected » (DIG16 Facebook, dig16fr Instagram, dig16fr TikTok), offre gratuite.

## Google : supprimer une fiche d'établissement en double (confirmé sur captures le 21/10/2026, téléphone, navigateur)
- Lien direct : https://business.google.com/locations (connexion Google, puis liste « Établissements » avec « Tous (N) »).
- Chaque fiche montre un numéro, le nom, la zone et son état (« Validation requise » ou « Validé »). Garder la fiche « Validé » ; les doublons non validés sont invisibles du public.
- Cocher les fiches à supprimer → « Actions » → « Supprimer les établissements » → « Supprimer » (aide Google 4669092, lue le 21/10). Ne pas cocher « définitivement fermé ».
- Résultat vérifié : la liste passe à « Tous (1) » ; la fiche publique garde ses actualités.
- Variante (fiche ouverte depuis la recherche Google « mon entreprise », 21/10) : ⋮ en haut à droite → « Paramètres de la fiche d'établissement » → « Supprimer la fiche d'établissement » → « Supprimer les administrateurs et le contenu de la fiche » → « Continuer » → « Supprimer » → « OK » (aide 4669092 ; suppression faite par l'utilisateur, écrans non vus sur capture).

## Outils gratuits choisis le 21/10 (annuaire « There's An AI For That »)

**Postnify** (documentation officielle docs.postnify.com, lue le 21/10)
- Créer le compte sur https://platform.postnify.com/ (offre « Free Forever » : 2 réseaux, 15 publications par mois).
- Relier les réseaux : Settings → Channels → « Add Channel », puis X, puis Facebook. Chaque réseau demande la connexion de son titulaire.
- Clé pour Claude : Settings → Developers → Public API. La clé ne se colle **jamais** dans la conversation : elle va dans les réglages de l'environnement cloud (menu de l'environnement dans la barre de titre de la session → Edit → « Network secrets », ou variable d'environnement `POSTNIFY_API_KEY`). Elle sera lue par une nouvelle session.
- Limite de l'API : 30 appels par heure ; plusieurs publications peuvent partir dans un seul appel.
- **Constaté sur captures le 30/10/2026 (compte gratuit)** : Settings n'a que « Global Settings » et « Approved Apps » ; aucun onglet « Developers / Public API », rien non plus dans « Integrations » (HeyGen, Reel.Farm). La clé n'est donc pas accessible en offre gratuite malgré la page des prix : ne plus reproposer Postnify pour X automatique, sauf si l'onglet apparaît.

**WebAnatomy** (écrans vus par Claude le 21/10)
- https://www.webanatomy.ai/landing-page-analyzer → coller `https://dig16.fr/` → « Analyze for free ».
- L'écran suivant est « Create an account » : email, mot de passe (12 caractères ou plus, avec majuscule, minuscule, chiffre et symbole), une vérification anti-robot, une case « Receive CRO & growth insights by email » (facultative, à décocher), puis « Sign up ». « Continue with Google » existe aussi.
- La vérification anti-robot bloque Claude : seul l'utilisateur peut créer ce compte.

**TrustGrowth** (écrans vus par Claude le 21/10)
- https://trustgrowth.ai/ → champ « Your site URL » : `dig16.fr` → « Get my score → ». Le site annonce : « Read-only Google Search Console · about 60 seconds · no card, ever ».
- La suite (connexion Google, autorisation de lecture de la Search Console) n'est pas visible sans compte : procéder **un écran à la fois, sur capture**.
- **Confirmé sur captures le 30/10/2026** : connexion Google → « Select Properties » (dig16.fr coché, « Continue with 1 site → ») → « Record Baselines & Continue → » (≈ 30 s) → « You're All Set! » (étapes Connected… Published, puis Scored et Live) → « Open Dashboard ». En bas : offre Starter à 9 $/mois et liste d'attente Growth (adresse pré-remplie) : ne rien cocher.
- Search Console de dig16.fr validée depuis le 12/10.

**ProspectFlow** : le lien d'inscription mène à une **liste d'attente** (« ProspectFlow is launching soon. Join the waitlist », lu le 21/10). Il n'y a pas de compte possible pour l'instant, donc l'outil est écarté.

### YouTube : supprimer une de ses vidéos (page d'aide officielle support.google.com/youtube/answer/55770, lue le 22/10/2026)
- **Application YouTube sur Android** : « Connectez-vous à YouTube » → touchez votre photo de profil, puis « Vos vidéos » → à côté de la vidéo, « Plus » (⋮) puis « Supprimer » → « Supprimer » pour confirmer.
- **YouTube Studio (ordinateur)** : menu de gauche « Contenu » → survoler la vidéo → options → suppression définitive → cocher la case de confirmation → valider. La suppression est définitive.

### TikTok : supprimer une de ses vidéos (aide officielle support.tiktok.com « Editing, posting, and deleting », lue le 22/10/2026, page sans date)
1. Ouvrir la vidéo à supprimer. 2. Toucher le bouton « Plus d'options » (…) sur le côté de la vidéo. 3. Toucher « Supprimer ».
La vidéo reste 30 jours dans « supprimés récemment » avant d'être effacée pour de bon. 22/10 : l'utilisateur n'y arrive pas → capture de l'écran après « … » pour guider (ne pas improviser).
- **22/10 (capture de 18 h 39)** : la vidéo était ouverte depuis le **compte personnel** de l'utilisateur (« Te suit », « Écrire à DIG16 Sites in… ») : seul le compte dig16fr peut la supprimer. Changer de compte (aide officielle support.tiktok.com « Creating an account », lue le 22/10) : onglet **Profil** en bas → toucher son **nom** en haut → choisir le compte déjà ajouté (ou « Ajouter un compte »). Puis Profil dig16fr → la vidéo → « … » → « Supprimer ».
- **✅ Confirmé par capture le 22/10 (18 h 45, Android, compte dig16fr)** : sur sa propre vidéo, il n'y a pas de « … » visible ; c'est la **flèche « Partager »** (côté droit) qui ouvre le panneau du bas, dont la dernière ligne contient « **Supprimer** » (à côté de « Gérer plusieurs commentaires », « Copier », « Répondre en vidéo »). Toucher « Supprimer » puis confirmer.

### TikTok : épingler un commentaire sur une vidéo → n'existe plus (vérifié le 22/10/2026)
L'aide officielle TikTok « Comments » et « Manage comments » (lues le 22/10) ne parle plus d'épingler ; wikiHow « How to Pin a Comment on TikTok » (lu le 22/10) indique que l'épinglage n'existe plus que pendant un LIVE ; l'utilisateur ne trouve pas l'option (22/10). Ne plus le proposer : écrire un simple commentaire (marqué « Créateur ») et garder le lien dans la bio.

## Facebook : partager une publication de la page DIG16 sur le profil personnel (Android)
- Source : aide officielle Facebook « Switch between your profile and Page » (facebook.com/business/help/571062040244333, lue le 24/10/2026) ; **✅ confirmé par capture le 24/10 (17 h 23)**.
- Piège vu le 24/10 : si l'appli est restée sur la page, le partage part **au nom de la page** (auteur « DIG16 - Sites intern… », bouton « Créer une publicité »). Avant de partager : Menu ou photo de profil → petite flèche → choisir le profil personnel. Après le partage, l'auteur affiché doit être le nom du profil, avec l'icône « amis » à côté de l'heure.
- Le texte d'accompagnement se colle dans la zone au-dessus de la publication **avant** de publier (le 24/10 il a été oublié : partage sans texte, acceptable).

## Claude (application ordinateur) : mettre la session en mode « Auto »
- Source : documentation de l'environnement (`read_documentation` session.permissions, 24/10/2026) ; **✅ confirmé par capture le 24/10 (PC)**.
- En bas, sous la zone de saisie, à gauche : bouton du mode (affichait « Accepter les modifications »). Clic → menu « Mode » : **Auto** (Recommandé, « Claude gère les décisions d'autorisation »), Accepter les modifications, Plan. Choisir **Auto**. Jamais « Plan » (bloque les rappels).
- Sur téléphone (Android, 24/10) : pas trouvé ; « Default » dans l'en-tête n'ouvre rien.

## URSSAF auto-entrepreneur : question écrite sur la situation du compte (vérifié le 27/10/2026)

Source : page officielle « L'essentiel du statut » (autoentrepreneur.urssaf.fr), lue le 27/10/2026 : « autoentrepreneur.urssaf.fr > Rubrique « Ma messagerie » > Nouveau Message > Une question concernant la situation administrative de votre compte ». Utilisé le 27/10 pour demander la catégorie BIC ou BNC : aucun écran de l'espace ne l'affiche clairement ; la déclaration de chiffre d'affaires (lignes « BIC Prestations » ou « Activités libérales BNC », fiche « Déterminer mon chiffre d'affaires ») la montre à l'ouverture de la déclaration.

## PagesJaunes (Solocal Manager) : horaires d'ouverture (aide officielle lue le 27/10/2026, article 360016527599 mis à jour le 27/10/2026)

Solocal reprend la règle de Google : indiquer les horaires où l'on reçoit les clients ; les établissements qui reçoivent seulement sur rendez-vous « n'ont pas intérêt à mentionner des horaires ». Parcours : solocal manager → « Mes fiches établissements » → « Voir mon établissement » → section « Horaire d'ouverture » → crayon → fenêtre de modification (jours ouverts et créneaux). L'aide ne dit pas s'il existe une option « aucun horaire » : capture de la fenêtre avant d'enregistrer ; ne jamais enregistrer un réglage qui afficherait « Fermé ». Les horaires Solocal sont aussi envoyés vers Google si la fiche Google est reliée à Solocal Manager.

Constat sur capture du 27/10/2026 : la fenêtre « Horaires d'ouverture » de Solocal Manager propose seulement, pour chaque jour, « Ouvert » (désactivé = Fermé) et « Ouvert 24h/24 », puis Annuler/Enregistrer : pas d'option « aucun horaire ».

## YouTube : description de la chaîne (aide officielle support.google.com/youtube/answer/3027950, lue le 27/10/2026)

Ordinateur : se connecter à YouTube Studio (studio.youtube.com) → menu de gauche « Personnalisation » → onglet « Profil » (nom, identifiant, description, liens) → modifier → « Publier ». Sur téléphone : appli YouTube ou YouTube Studio, photo de profil → modifier (aide answer/2657964).

- **28/10, autoriser un outil de connecteur une fois pour toutes (ex. Vercel « Upload file »)** : https://claude.ai/customize/connectors → ouvrir le connecteur (Vercel) → réglages des outils → mettre l'outil sur « toujours autoriser ». Source : documentation de l'environnement lue le 28/10. La règle `mcp__Vercel__*` est déjà dans `.claude/settings.json` ; la fenêtre vient du réglage du connecteur côté claude.ai. Libellés exacts de l'écran : à confirmer sur capture.

## GoCardless : créer les modèles de paiement (confirmé sur captures le 29/10/2026)

- Accueil manage.gocardless.com → cadre « Démarrer avec les paiements » → **Poursuivre** → page « Créer des paiements » (cartes Plan d'abonnement, Frais de provision, Service ou produit unique…).
- Accès direct au formulaire : https://manage.gocardless.com/setup-payments/create → onglets « Client final uniquement », « Unique », « Abonnement », « Échéances ».
- **Abonnement** : Nom du produit, Montant, Fréquence (Mensuel), Référence (facultatif, visible sur le relevé du client), 3 interrupteurs (nombre fixe de paiements, date du prélèvement, redirection) laissés éteints. **Unique** : Nom, Montant, interrupteurs « Rediriger » et « Utiliser Pay by Bank » (paiement instantané par l'appli bancaire ; inclus dans l'offre Standard au même tarif, page tarifs lue le 29/10).
- « Créer » → page « Invitez des clients finaux » avec le lien pay.gocardless.com à partager (et code QR). Ne pas suivre le conseil « partagez le lien avec vous-même » (vrai prélèvement).
- Modèles créés le 29/10 : Essentiel 49 €/mois (réf. DIG16 ESSENTIEL), Visibilité 79 €/mois (DIG16 VISIBILITE), Prestige au mois 199 €/mois (DIG16 PRESTIGE), option Achat 15 €/mois (DIG16 SUIVI), Achat 690 € et Prestige 1 990 € en paiement unique avec Pay by Bank.
- Logo : bouton « + Ajoutez votre logo » (en haut à droite de l'aperçu) → « Télécharger un logo » (JPG ou PNG jusqu'à 5 Mo), taille S/M/L, couleurs « Arrière-plan du logo » et « Bouton », aperçu « Page de paiement » / « E-mail » → « Enregistrer les modifications ». Fait le 29/10 avec site-dig/img/marque/icone-512.png, taille L.
- Bandeau « jours restants sans frais » + « Prolonger » : ne pas cliquer avant d'avoir lu ce que propose « Prolonger » (conditions de l'offre de bienvenue : aucun frais de transaction pendant la période).

### Modifier la légende d'une publication déjà parue
- **Instagram** (aide officielle help.instagram.com/1490745927855762, lue le 29/10/2026) : « … » (Options) en haut à droite de la publication → **Modifier** → corriger la légende → **OK / Terminé**.
- **Facebook** (aide officielle facebook.com/help/462476073850410, lue le 29/10/2026) : sur la publication, « … » (Options) en haut à droite → **Modifier la publication** → corriger → **Enregistrer**.

### Instagram : archiver une publication (la masquer sans la supprimer)
- Aide officielle help.instagram.com/136706673552668 (« Archive a post you've shared on Instagram », lue le 29/10/2026) : fonction disponible dans l'appli (Android, iPhone), pas sur ordinateur ; réversible (« Show an archived post again in your Instagram profile », help.instagram.com). Dans l'appli : sur la publication, « … » en haut à droite → **Archiver**. Si le mot n'apparaît pas : capture de l'écran.

### YouTube : rendre une vidéo privée (sans la supprimer)
- Aide officielle support.google.com/youtube/answer/157177 (Android, lue le 29/10/2026) : **appli YouTube** → photo de profil → **Vos vidéos** → « ⋮ » (Plus) à côté de la vidéo → **Corriger** → **Visibilité** → **Privé** → Retour → **ENREGISTRER**. Appli YouTube Studio : **Contenu** → « ⋮ » → **Corriger** → **Visibilité** → **Privé**. Réversible.

## vidIQ : ajouter un compte Instagram (page d'aide officielle lue le 29/10/2026)

Source : support.vidiq.com, article « vidIQ for Instagram ». Inclus dans l'offre gratuite (150 crédits par mois, partagés avec YouTube ; une analyse Instagram coûte environ 10 crédits).
- Sur ordinateur : app.vidiq.com/ai-coach → clic sur la photo de profil ou l'adresse en **bas à gauche** → **Accounts** → **Add** → **Instagram** → taper le nom du compte (`@...`) → le sélectionner dans **Accounts**.
- Ce n'est pas une vraie connexion : vidIQ lit seulement les données publiques (aucun mot de passe Instagram ni autorisation Meta).
- Inutile pour Claude : l'outil vidIQ lit déjà un compte public à partir de son nom (`vidiq_ig_profile`, 5 crédits ; `vidiq_ig_profile_reels`).
- Statistiques privées et publication de Reels : une connexion Meta distincte, par l'outil « Clipping » de vidIQ. Non nécessaire, car Metricool publie déjà sur Instagram.

## PagesJaunes (Solocal Manager) : publier une actualité (aide officielle lue le 30/10/2026)

Source : help.solocal.com, article 360017586359 « Publier une actualité » (mis à jour le 26/10/2026) et article 13625331212188 « Les règles de paramétrages de votre publication » (26/10/2026), lus par l'API publique du centre d'aide.
- Menu **Communication** → **« Créer une publication »** (ou bouton « Créer une publication » en haut à droite dans « Mes publications »).
- Plateformes de diffusion : celles qui sont connectées sont **pré-cochées** ; ne garder que **pagesjaunes** (la fiche Google reçoit ses publications par Metricool).
- Type de publication : **Standard** ; texte obligatoire (1 500 caractères au plus pour pagesjaunes) ; jusqu'à 10 photos ; « Ajouter un bouton » → **En savoir plus** + adresse (lien de mesure `https://dig16.fr/pj`).
- « Début de la diffusion » : **maintenant** par défaut ; « Fin de diffusion » facultative (la publication disparaît alors du fil pagesjaunes) → **Publier**.
- Libellés exacts sur téléphone : à confirmer sur capture.

## X : profil (aide officielle lue le 30/10/2026)

Sources : help.x.com « How to customize your profile » et « About profile visibility settings » (lues le 30/10/2026, en anglais ; libellés français à confirmer sur capture).
- Profil → **Edit profile / Éditer le profil** : bio (160 caractères), site web, lieu, date de naissance.
- Date de naissance : section **Birth date** → réglages de visibilité séparés pour le jour et le mois, et pour l'année → **Only you / Uniquement vous** ; ces réglages ne peuvent être changés que « quelques fois ». Retrait possible aussi (« Remove birth date » sur l'appli), mais la date sert à X pour vérifier l'âge : préférer la visibilité.
- Épingler : sur le profil, la publication → icône « … » → **Pin to your profile / Épingler à votre profil**.
- **Contrôle par Claude sans connexion (30/10/2026)** : `curl -s https://api.fxtwitter.com/dig16charente` renvoie la bio, le site web et le lieu publics du profil (la date de naissance et la publication épinglée n'y figurent pas : capture si besoin).
