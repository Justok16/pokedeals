# Le nouveau manuel et guide de prompting pour ChatGPT

Vidéo : https://youtu.be/MDy_b9F7oUc · durée 38:58 · résumé Gemini (gemini-3.6-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo, rédigé en français :

---

### 1) Idée principale
La vidéo présente un guide complet de la nouvelle application **ChatGPT** et des modèles **GPT-5.6** (Work, Codex, Sites, Browser). L'auteur montre comment utiliser cette plateforme unifiée et ses capacités avancées (agents autonomes, contrôle d'écran/CUA, génération de code, création de sites/jeux hébergés en un clic, automatisation de tâches) pour décupler sa productivité, créer des outils sur mesure ou lancer des services/projets web rentables sans compétences techniques approfondies.

---

### 2) Outils, sites et dépôts GitHub cités

*   **ChatGPT App / ChatGPT Work / ChatGPT Codex (OpenAI)** : *Gratuit / Payant (Abonnement ChatGPT / Accès API)* — Application unifiée combinant l'assistance bureautique (Work) et le développement/génération de code avancé (Codex).
*   **ChatGPT Sites** : *Inclus dans ChatGPT* — Fonctionnalité permettant de publier et d'héberger instantanément sur le web des sites, applications ou jeux générés par l'IA.
*   **Computer Use Agent (CUA / Computer Use)** : *Inclus dans l'application* — Agent IA capable d'interagir directement avec l'interface graphique de votre ordinateur et de vos logiciels (ex. contrôler Blender).
*   **ChatGPT Browser (Navigateur intégré)** : *Inclus dans l'application* — Navigateur web interne permettant à l'IA de naviguer, d'annoter des éléments visuels à l'écran et d'importer les cookies/mots de passe de Chrome.
*   **Future Tools (`futuretools.io`)** : *Gratuit* — Annuaire d'outils IA développé par l'auteur, avec classement communautaire et algorithme de recommandation.
*   **Teachable** : *Payant* — Plateforme de cours en ligne utilisée pour illustrer la création automatique de présentations de webinaire.
*   **Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets** : *Gratuit / Payant* — Plugins intégrés dans ChatGPT pour lire vos données et rédiger des brouillons d'e-mails ou organiser votre agenda.
*   **Slack, Todoist, Granola, Canva, Figma, Supabase, Vercel** : *Gratuit / Payant* — Diverses intégrations/plugins connectés à l'assistant personnel pour centraliser l'information et exécuter des tâches.
*   **Cornerpost** (`cornerpost-market.mreflow.chatgpt.site`) : *Démo gratuite* — Prototype de plateforme de petites annonces locales (réinvention de Craigslist) généré et hébergé en quelques minutes sur ChatGPT Sites.
*   **Compressor** (`compressor.sonnylab.com`) : *Site présenté (par Sunny Lazquardi)* — Page d'atterrissage pour une application de compression d'images créée avec Codex / GPT-5.6 Sol.
*   **Solbonk & Echo Garden** (`echo-garden-twelve.mreflow.chatgpt.site`) : *Démos gratuites* — Jeux vidéo 3D (un clone et un jeu de réflexion original) créés entièrement par prompt et publiés sur ChatGPT Sites.
*   **TopView MCP / Seedance 2.0 / HyperFrame / HeyGen** : *Payant / APIs* — Outils de création vidéo utilisés par des créateurs pour automatiser la génération de scripts, d'avatars vidéo et le montage complet à partir d'un prompt.
*   **Blender** : *Gratuit (Open Source)* — Logiciel de modélisation 3D contrôlé en temps réel par l'agent CUA de GPT-5.6 pour créer des objets 3D (ex. un canon).
*   **NYC Sim** (`nycsim.com`) : *Site présenté (par David Lietjauw)* — Simulateur 3D de New York style GameBoy intégrant des données de transport en temps réel.
*   **MapLibre GL JS / OpenFreeMap** : *Gratuit (Open Source)* — Bibliothèques de cartographie 3D utilisées par un utilisateur Reddit pour générer une carte interactive de Londres en 5 minutes.
*   **BuseyBench** : *Gratuit (projet de l'auteur)* — Outil de benchmark mesurant la capacité des modèles LLM à générer du code SVG.
*   **Wolfe Control Tower** : *Projet personnel de l'auteur (non disponible)* — Tableau de bord sur mesure compilant la veille IA, les statistiques d'audience et les mentions de marque.
*   **Dock Toggle** : *Gratuit (projet de l'auteur)* — Script/application macOS généré par Codex pour masquer/afficher le Dock Mac via un bouton Stream Deck.

---

### 3) Astuces concrètes et réutilisables

1.  **Configurer un profil "Assistant Personnel" avec compétences globales** : Créez un projet dédié et donnez-lui un prompt ("Skill") l'autorisant à consulter en *lecture seule* l'ensemble de vos applications (Gmail, Slack, Drive, réunions Granola). L'IA aura tout le contexte de votre activité sans que vous ayez à lui réexpliquer votre vie à chaque prompt.
2.  **Cloner son style rédactionnel** : Demandez à l'IA d'analyser l'historique de vos e-mails et messages Slack envoyés sur les 12 derniers mois pour créer un "profil de voix" (ton, structure de phrase, vocabulaire). Elle pourra ensuite rédiger des brouillons d'e-mails ou de messages qui vous ressemblent parfaitement.
3.  **Référencer des conversations passées via leur ID** : Dans Codex/Work, vous pouvez copier le `Session ID` d'anciennes discussions et les fournir à l'IA pour qu'elle réutilise des idées ou des blocs de texte déjà abordés auparavant (ex: synthétiser 3 réunions en un document de présentation).
4.  **Prospection commerciale et création automatique de brouillons Gmail** :
    *   *Prompt type* : Demandez à l'IA de chercher des prospects ciblés (ex. 20 PME dans une ville donnée), d'identifier un besoin en IA, et de rédiger une offre personnalisée.
    *   Grâce à l'intégration Gmail, demandez-lui d'injecter directement les e-mails rédigés dans votre dossier **Brouillons Gmail**. Vous n'avez plus qu'à relire et cliquer sur "Envoyer".
5.  **Renommage et tri automatique de fichiers locaux (Vision + Fichiers)** :
    *   Fournissez le chemin d'accès d'un dossier local (ex. un dossier rempli de miniatures ou de captures d'écran nommées "image1.jpg").
    *   Demandez à l'IA de regarder le contenu visuel de chaque image, de lire le texte présent dessus et de renommer chaque fichier de manière explicite (ex. `Gemini-3-First-Look.jpg`).
6.  **Développement d'applications/outils internes sur mesure** : Ne payez plus d'abonnements SaaS coûteux pour des petits besoins. Utilisez Codex pour créer des scripts ou applications web spécifiques à votre entreprise, puis hébergez-les gratuitement via la fonction "Sites".

---

### 4) Chiffres de revenus annoncés

*   **Non précisé** *(L'auteur montre l'utilisation intensive de l'outil — jusqu'à 2 milliards de tokens consommés en une journée — et explique comment générer des opportunités d'affaires ou vendre des services d'automatisation/conseil, mais n'annonce aucun chiffre de revenus personnels directs dans la vidéo).*
