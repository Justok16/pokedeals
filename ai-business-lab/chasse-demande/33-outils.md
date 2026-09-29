# Outils pour renforcer Claude Code sur ce projet

Tenu à jour par la routine (point 3 : une recherche d'outils par jour).
Règle : gratuit et sans compte → installé par Claude ; compte ou clé
nécessaire → préparé puis proposé à l'utilisateur ; payant → seulement
quand un revenu le justifie (budget 0 €).

| Outil | Usage pour nous | Coût | État |
|---|---|---|---|
| Gmail (connecteur, boîte du pseudonyme) | Contacter et suivre les éditeurs | gratuit | **actif** |
| OpenRush (connecteur) | Mesurer la demande (volumes de recherche Google) | gratuit (déjà connecté) | **actif** |
| Jev — TypeSafe AI (skill `.claude/skills/typesafe-ai`, outil `outils/jev_trier_reponses.py`) | Aiguilleur des réponses : catégories fermées, repli Claude puis humain | 5 $/mois offerts via Vercel AI Gateway | skill installé ; **clé à ajouter** (inscription TypeSafe fermée → Vercel) |
| Similarweb, Crunchbase | Trafic des sites, fermetures de startups | payants (Similarweb 338 €/mois) | écartés tant que rien ne rapporte |
| Stripe | Encaisser un produit vendu en direct | commission | inutile pour Atlassian (Atlassian encaisse) |
| Plugin « Small Business » (Anthropic, 44 skills) | Contrats, propositions, factures, trésorerie, impôts | gratuit | **installé** dans le projet (.claude/settings.json) le 24/09 |
| Higgsfield | Vidéos IA de démonstration d'un produit | freemium | **à activer quand on aura un produit à promouvoir** |
| Outils de développement Shopify pour Claude Code (vidéo AI LABS, 24/09) | Créer apps/thèmes Shopify | gratuit (à vérifier) | en réserve : seulement si une piste Shopify se confirme (aucune à ce jour, voir 07 et 19) |

## Sources envoyées par l'utilisateur (24/09, nuit) et suite donnée

| Vidéo (auteur) | Suite |
|---|---|
| Claude pour les petites entreprises, 44 skills (Tony Lotis) | plugin officiel « Small Business » proposé à l'installation |
| Jev will 10x your Claude Code ; résumés NotebookLM sur Jev | skill installé + aiguilleur ; clé via Vercel à ajouter |
| 12 New Rules for Prompting Opus 5.5 (RoboNuggets) | `.claude/CLAUDE.md` créé (contexte permanent) |
| 7 Free GitHub Repos That Make Claude So Good… (AI Edge) | **noms des dépôts à obtenir** (description de la vidéo), puis vérifier/installer |
| Shopify Claude Code workflow (AI LABS) | en réserve |
| JARVIS avec Claude Code (Thomas Berton) | écarté : déjà couvert (session cloud + routine) |
| Trading bots Jev/MCP (Miles Deutscher, Saleh) | écartés : secteur à risque (point 19) |
| 1 Person Business (Nate Herk), 9-5 en 90 jours (Shane Hummus), Opus 5.5 (Alex Finn), gagner de l'argent (Amadou Fall) | pas d'outil ; confirme l'organisation actuelle |
| Formation Claude Code gratuite (Ben BK, playlist) ; vidéo wEEi2bCuZGQ (inaccessible) | rien à installer |

## Vidéos : ce qui a pu être lu (24/09, nuit)

YouTube bloque la lecture des sous-titres depuis les serveurs cloud
(« RequestBlocked ») ; protection anti-robots respectée, pas de
contournement. Contenu retrouvé par recherche web quand c'est possible.

- « 7 Free GitHub Repos… » (AI Edge / Miles Deutscher) : liste partielle
  retrouvée (skool.com, recherche) : Last30Days, Playwright MCP, gstack,
  Agency Agents, Buzz ; souvent cités à côté : Superpowers,
  awesome-claude-code, Repomix.
  - **Superpowers** (obra) : **installé** pour le projet (méthode : plan,
    tests, relecture) — servira au portage Forge.
  - Playwright : déjà utilisé via nos outils (Chromium dans l'environnement).
  - Autres : non installés (pas d'usage pour nous à ce jour).
- Pour les autres vidéos : obtenir leur contenu via NotebookLM
  (l'utilisateur) → export dans Google Drive → lecture par le connecteur
  Google Drive.

## Relais Vercel « relais-dig » (25/09, 22:30 UTC)

Petit programme déployé sur le compte Vercel de l'utilisateur
(`outils/relais-vercel/`) : `/api/video?id=…` (résumé d'une vidéo YouTube
par Gemini) et `/api/jev?q=…` (Jev). Aucune clé : authentification par le
jeton OIDC du déploiement. Accès uniquement par l'adresse protégée
`relais-dig-justok1.vercel.app` via le connecteur Vercel ; l'adresse
publique renvoie 403.

État : l'appel atteint bien l'AI Gateway, qui répond « a valid credit card
on file is required to unlock your free credits ». **Bloqué tant qu'aucune
carte n'est enregistrée** (décision de l'utilisateur ; ne jamais acheter de
crédits). YouTube bloque par ailleurs toute lecture directe depuis le cloud
(miroirs Invidious/Piped et youtubetranscript testés : bloqués).
Depuis le 26/09 au soir : **clé Gemini gratuite** créée par l'utilisateur et
enregistrée dans Vercel (`GEMINI_API_KEY`, jamais dans le dépôt). `/api/video`
l'utilise en priorité (offre gratuite : 8 h de vidéo YouTube par jour, et une
limite de débit : espacer les vidéos d'environ 75 s).
Correction du 27/09 : la vraie limite gratuite est d'environ **20 requêtes par jour
et par modèle** ; 7 modèles savent lire une vidéo (gemini-3.8/3.7/3.6/3.5-flash,
3-flash-preview, 3.5-flash-lite, 3.1-flash-lite) — `/api/video?modeles=…` choisit le
modèle, `/api/video?liste=1` liste les modèles de la clé, `/api/chaine?chaine=@nom`
liste toutes les vidéos d'une chaîne.
**Déploiement du relais depuis GitHub** (27/09) : `create_deployment` avec
`gitSource` (Justok16/pokedeals, branche de travail) et `rootDirectory`
`ai-business-lab/chasse-demande/outils/relais-vercel` — plus besoin de coller
les fichiers : committer, pousser, puis redéployer.

**Mise à jour 25/09, 22:40 UTC : fonctionne.** Carte enregistrée par
l'utilisateur ; Gemini résume les vidéos YouTube, Jev répond (coût facturé
0 $ au test). Accès : lien temporaire (23 h) créé à chaque passage avec
l'outil Vercel `get_access_to_vercel_url`, jamais écrit dans le dépôt.

## vidIQ (connecteur, ajouté le 28/09/2026)
- Compte gratuit de l'utilisateur : **150 crédits par mois** (renouvelés le 28 de chaque mois).
- `vidiq_video_transcript` (5 crédits) donne la transcription d'une vidéo YouTube, même quand
  YouTube bloque nos serveurs. Usage retenu : **secours** pour les vidéos que Gemini n'arrive pas
  à lire (≈ 30 par mois au maximum) ; la fiche est alors rédigée à partir de la transcription.
- Testé le 28/09 : les sous-titres YouTube sont bloqués depuis le conteneur, Vercel,
  youtubetranscript.com, Invidious et Piped ; seul vidIQ passe.

## Inventaire des connecteurs (28/09/2026, demande de l'utilisateur)
Branchés et utilisés : Gmail, Google Drive, Google Agenda, Vercel (relais), Canva, OpenRush,
vidIQ, Cloudflare, Supabase, Notion, Airtable, Make, Zapier, Resend, DocuSeal (signature),
PDF.net, Figma, Excalidraw, Webflow, TinyPages, B12, Slack.
Inutiles pour le projet (laissés tels quels) : AccuWeather, Trivago, Uber, Uber Eats,
Health Data Avatar, Zacks, Anthropic Economic Index, Perspective AI, AdWhispr (pas de publicité
avant l'immatriculation).

À connecter par l'utilisateur (claude.ai → Réglages → Connecteurs), avec son accord :
- **Firecrawl : branché le 28/09.** Testé : lit les pages qui bloquent nos serveurs (ex. recherche
  Unsplash, 1 crédit la page). À utiliser pour les photos, les annuaires et la vérification des prospects.
- **Similarweb : branché le 28/09 mais inutilisable gratuitement** (« plan has reached its credit
  limit » dès le premier appel). Ne pas prendre d'abonnement (budget 0 €).
  **Équivalents gratuits trouvés (28/09)** :
  - trafic estimé, mots-clés, pages et concurrents d'un site → **OpenRush** `inspect_domain`
    (testé sur pagesjaunes.fr : ~84,6 M visites Google/mois estimées, concurrents mappy.com, 118712.fr…) ;
  - fiche d'entreprise (SIREN, état, adresse) → annuaire officiel via le relais `/api/entreprise` + BODACC ;
  - téléphone, activité, présence en ligne → Firecrawl (pages des annuaires) et recherche web.
Seulement le jour où c'est utile :
- **Atlassian Rovo** (connexion inachevée) : si un éditeur accepte la reprise (portage Forge).
- **Stripe : branché le 28/09**, en **mode test** (« environnement de test Dig ») : sert à préparer
  et tester l'encaissement et le prélèvement SEPA sans argent réel ; mode réel seulement après la
  création de l'entreprise (accord de l'utilisateur). **Qonto** reste une option pour la banque.
- **Brevo** (emails B2B conformes CNIL) : pour une campagne, une fois la structure légale créée.
**Branchés aussi le 28/09** (testés en lecture seule, rien créé) : **PayPal** (factures, liens de
paiement ; 0 facture), **Wix** (0 site ; utile pour reprendre un client déjà sur Wix),
**Docusign** (signature électronique ; DocuSeal reste l'outil gratuit par défaut).
**HubSpot et Trello : connexion impossible (28/09)** → pas nécessaires. Équivalents déjà branchés et
gratuits : suivi des prospects et clients (CRM) → **Airtable** ou **Notion** (données privées :
jamais dans ce dépôt) ; tableau de tâches → **Notion** (vue tableau) ou la liste « À faire » du dépôt.
Les connecteurs « small-business » qui demandent encore une autorisation (HubSpot, Trello,
Zoho, Xero…) sont des doublons du module complémentaire : à ignorer.
Je ne peux pas connecter moi-même : chaque connexion demande l'identifiant de l'utilisateur.

## Skill « vibe-security » (installé le 28/09/2026, accord de l'utilisateur)

Source : github.com/raroque/vibe-security-skill (licence MIT), lu en entier avant installation :
uniquement du texte, aucun programme. Rangé dans `.claude/skills/vibe-security`.
Premier audit (28/09) :
- **Relais Vercel** : bon. L'adresse publique est refusée (403) et les adresses protégées
  demandent la connexion Vercel (302), même avec un en-tête d'hôte falsifié. Les paramètres
  sont filtrés, et le crédit de la passerelle IA est protégé par un garde-fou de solde.
- **Secrets** : aucune clé ni jeton dans tout l'historique Git (recherche des formats connus :
  Stripe, AWS, GitHub, Google, clés privées, liens de partage Vercel). Règle `.env` ajoutée au
  `.gitignore` pour tout le dépôt.
- **Site** : pas de dossier `.git` exposé ; `innerHTML` seulement avec des textes fixes ;
  formulaires sans envoi pour l'instant. Ajouté : `site-dig/_headers` (CSP, HSTS, anti-iframe,
  permissions), testé sur les 5 pages : 0 blocage.
- À faire au lancement : anti-spam et limite d'envois sur le vrai formulaire ; paiement
  uniquement par un prestataire (prix fixés côté serveur, jamais dans la page).

## Diagnostic « visibilité Google » d'un prospect (gratuit, trouvé le 28/09/2026)

Besoin : montrer à un artisan, preuve à l'appui, s'il apparaît ou non quand un client cherche
« son métier + sa commune ». Outil payant du marché : **Local Falcon** (100 crédits offerts une
fois, soit 4 scans de 25 points ; page tarifs lue le 28/09 : « +100 Free Credits on sign up »,
« No credit card needed »). **Équivalent gratuit déjà branché : OpenRush `inspect_serp`**
(requête « plombier <commune> », langue French, lieu « <Commune>,<Région>,France ») : renvoie
en direct le **trio Google Maps** (nom, note, nombre d'avis) et les **10 premiers résultats**.
Test du 28/09 sur « plombier Bordeaux » : le trio Maps est pris par 3 artisans (4,9★/180 avis,
5★/518 avis, 4,9★/31 avis) ; dans les 10 résultats, **8 sont des annuaires ou plateformes**
(travaux.com, bilik, allovoisins, depanneo, mappy, PagesJaunes…) et 1 seul artisan a son propre site.
Leçons pour Dig :
- l'artisan se bat surtout pour le **trio Maps** : fiche Google soignée + avis = cœur de la
  formule Visibilité ; son site sert à confirmer et à convertir ;
- avant une visite, lancer la recherche sur son métier et sa commune et noter sa position
  (dans la fiche privée du prospect, Drive « Dig », jamais ici) : argument concret et vérifiable.
Connecteurs vus et **non retenus** (28/09) : Local Falcon (doublon payant d'OpenRush),
Jotform (5 formulaires, 100 envois/mois gratuits, mais données stockées chez un tiers américain ;
le formulaire du site sera fait avec Cloudflare + Resend, déjà branchés), Vibe Prospecting
(200 crédits/mois gratuits, « 1 credit Find a business », « 5 credits » un téléphone ; couverture
des petits artisans français à vérifier ; l'annuaire officiel reste la source principale).

## Annuaires et sites envoyés par l'utilisateur le 28/09/2026 (soir)

Ce sont des **sites web**, pas des connecteurs : on s'en sert dans le navigateur, on ne peut pas
les « brancher ». Aucun n'a de connecteur dans le catalogue de Claude (recherche du 28/09).

- **nosignups.net** (ex-FckSignups) : 268 outils libres, sans compte, qui tournent dans le
  navigateur ; liste complète lue à la source (`tools.json` du dépôt GitHub BraveOPotato/FckSignups).
  Retenus pour Dig : Squoosh et Tiny Image (alléger les photos des sites), Screenshot Studio
  (présenter une démo dans un cadre de téléphone), BentoPDF et PaperKnife (PDF sans envoi à un
  tiers), ShadeStudio (palette de couleurs), Metadata Remover (idée reprise en local :
  `outils/verif_metadonnees.py`), free-for.dev (liste des offres gratuites des services en ligne :
  première source pour trouver un équivalent gratuit).
- **futuretools.io** : annuaire de plus de 4 500 outils d'IA, filtrable par prix (Free,
  Freemium, Paid, Open Source) ; lettre d'information gratuite qui donne accès à une « AI Income
  Database » (idées de revenus, à passer à la grille `00` comme toute piste).
- **mrfreetools.com** (vu dans un reel) : annuaire de logiciels gratuits par catégorie.
- **fingerprint.to** et **discoverprofile.com** : recherche de comptes publics à partir d'un
  pseudo, d'un email ou d'un téléphone (OSINT). **Usage limité** : vérifier si une *entreprise*
  a une page Facebook ou Instagram, ou ce qu'Internet montre du pseudonyme « Dig ». Jamais pour
  profiler un particulier (RGPD : pas de base légale, pas d'information de la personne).
- **topview.ai** (vidéos, avatars), **atoms.dev** (création d'applis par agents IA),
  **buzzy.now** (vidéo IA, connecteur MCP `https://mcp.buzzy.now/mcp`) : **non retenus**,
  fonctionnement à crédits payants (Topview dès 16 $/mois en annuel ; Atoms : « 15 per day / 25
  per month » gratuits ; Buzzy : 2 crédits puis 10 à l'inscription), pages lues le 28/09/2026.
  Équivalents gratuits déjà en place : Canva, Gemini, skill `motion-graphics` (à tester).
- **DeepL** : connecteur disponible dans le catalogue. Utile seulement si un éditeur répond dans
  une autre langue que l'anglais ; à brancher par l'utilisateur le moment venu.

## Second avis gratuit : `/api/avis` du relais (ajouté le 28/09/2026)
Idée des vidéos ucer2chlfM8 et _9ZGlLWr6UE (faire chercher les failles par une autre IA, sans
rien réécrire), refaite gratuitement avec la clé Gemini. Appel POST JSON `{texte, consigne?,
media_base64?, media_type?, modeles?}` avec le cookie de partage. Sert à : relire un document
avant envoi (en plus du contrôle `44`), et lire une courte vidéo ou un audio (reels Facebook :
télécharger la vidéo depuis m.facebook.com, puis l'envoyer en base64, 4,5 Mo maximum).
**Déploiement** : toujours préciser `projectSettings.rootDirectory` =
`ai-business-lab/chasse-demande/outils/relais-vercel`, sinon tout le relais répond 404
(erreur du 28/09, corrigée en 10 minutes). Chaque déploiement invalide le cookie : le renouveler.

## Blocages et solutions de rechange (tenir à jour à chaque blocage)
| Blocage | Solution gratuite qui marche |
|---|---|
| Sous-titres YouTube bloqués (conteneur, Vercel, Invidious, Piped) | Gemini lit la vidéo ; secours vidIQ (transcription) |
| Recherche Unsplash bloquée (défi anti-robots) | Firecrawl `firecrawl_scrape` (1 crédit la page) |
| Similarweb sans crédit | OpenRush `inspect_domain` |
| Annuaire officiel bloqué depuis le conteneur | Relais Vercel `/api/entreprise` |
| Crédit Vercel AI Gateway épuisé | 9 modèles de la clé Gemini gratuite |
| Firecrawl en erreur (« Invalid content from server », 28/09) | Outil WebFetch, ou curl direct sur la page |
| Reels Facebook (connexion demandée) | Version mobile m.facebook.com : fichier vidéo lisible, puis images (imageio-ffmpeg) ou Gemini `/api/avis` |
| Outil payant sans équivalent connu | Chercher dans free-for.dev, nosignups.net, futuretools.io (filtre Free / Open Source) |
| Site « hors ligne » d'après curl (code 000) alors que le DNS répond (28/09) | Faux négatif possible : le relais réseau du conteneur refuse certaines connexions. Confirmer avec Firecrawl `firecrawl_scrape` (ou WebFetch) avant de conclure ; seul un domaine NXDOMAIN (cloudflare-dns.com) ou une vraie page 404/500 prouve qu'un site est mort |
| Photos HD libres pour les démos (Openverse ne donne que 960 px, Unsplash demande une clé) | API Wikimedia Commons sans clé : recherche `filetype:bitmap <mot>`, ne garder que CC0 / domaine public, vignettes de taille standard (1920 px), une requête à la fois avec pauses (sinon erreur 429) ; sources notées dans `supports/sources-photos-wikimedia.md` |
| Wikimedia Commons répond 429 (trop de requêtes) depuis le conteneur (29/09) | Attendre au moins 1 h, puis une requête toutes les 10-20 s ; vignettes de taille standard seulement (1920 ou 3840 px) ; ne pas contourner la limite par d’autres serveurs. En attendant : rawpixel et StockSnap via Openverse (CC0, mais environ 1 000 px, donc seulement pour les petites vignettes) |
