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

## Blocages et solutions de rechange (tenir à jour à chaque blocage)
| Blocage | Solution gratuite qui marche |
|---|---|
| Sous-titres YouTube bloqués (conteneur, Vercel, Invidious, Piped) | Gemini lit la vidéo ; secours vidIQ (transcription) |
| Recherche Unsplash bloquée (défi anti-robots) | Firecrawl `firecrawl_scrape` (1 crédit la page) |
| Similarweb sans crédit | OpenRush `inspect_domain` |
| Annuaire officiel bloqué depuis le conteneur | Relais Vercel `/api/entreprise` |
| Crédit Vercel AI Gateway épuisé | 9 modèles de la clé Gemini gratuite |
