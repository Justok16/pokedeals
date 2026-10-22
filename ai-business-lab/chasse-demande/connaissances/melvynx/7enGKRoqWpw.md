# La seule formation Claude Code dont tu as besoin en 2026 (tuto complet)

Vidéo : https://youtu.be/7enGKRoqWpw · durée 1:04:52 · résumé Gemini (gemini-3-flash-preview) du 2026-10-22
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo pour vous aider à exploiter **Claude Code** dans un cadre entrepreneurial et de développement :

### 1) L'idée principale
La vidéo explique comment devenir un "développeur 10x" en utilisant **Claude Code**, l'agent IA d'Anthropic. L'idée est de passer d'un simple chat avec l'IA à un système **agentique** où l'IA agit directement sur votre ordinateur (lit, écrit, exécute des commandes et déploie des sites). L'auteur démontre que l'on peut créer, gérer et mettre en ligne des applications (SaaS) complexes de manière automatisée pour générer des revenus.

### 2) Outils, sites et dépôts cités
*   **Claude (Anthropic)** : Modèle d'IA (Opus, Sonnet, Haiku). **Payant** (Abonnements Pro à 20$ ou Max à 100$/200$). Sert de "cerveau" pour générer du texte et du code.
*   **Claude Code (application Desktop)** : Interface d'agentique. **Gratuit** (nécessite un abonnement Claude). Permet à l'IA d'interagir avec vos fichiers locaux et votre terminal.
*   **Claude API** : Interface de programmation. **Payant au token**. Utilisée par l'auteur pour des volumes massifs.
*   **Lumail** : SaaS d'email marketing (créé par l'auteur). **Payant**. Cité comme exemple de projet réussi.
*   **SaveIt, Thumbfast, Codeline, PadelTally, Tchao** : Divers SaaS créés avec Claude. **Payants** (modèles économiques non précisés).
*   **Vercel** : Plateforme de déploiement web. **Gratuit/Payant**. Utilisé pour mettre les sites en ligne.
*   **Cloudflare (Workers, Pages, Drop)** : Service d'hébergement et de déploiement. **Gratuit/Payant**. Recommandé par l'auteur pour sa générosité et sa compatibilité avec les agents IA.
*   **Notion** : Outil de productivité. **Gratuit/Payant**. Connecté à Claude pour automatiser la gestion de tâches.
*   **GitHub** : Service de gestion de versions. **Gratuit/Payant**. Utilisé pour le stockage et le déploiement du code.
*   **skills.sh** : Répertoire open-source de "recettes" (skills) pour agents IA. **Gratuit**.
*   **mlv.sh/fc** : Page de ressources de l'auteur (configuration et commandes). **Payant** (pour l'accès complet aux réglages "Pro").
*   **AGENTS.md / CLAUDE.md** : Fichiers de configuration de projet. **Gratuit**. Sert de "mémoire" locale à l'agent.

### 3) Astuces concrètes et réutilisables
*   **Structure du Prompt (4 morceaux)** : Pour chaque projet, définissez clairement : **Quoi** (l'objectif), **Pour qui** (la cible), **Design** (l'apparence) et **Comment vérifier** (les tests à effectuer).
*   **Gestion du Contexte** : Gardez votre fichier `AGENTS.md` sous la barre des **200 lignes**. Si ce fichier est trop long, l'IA devient "plus bête" car le contexte est saturé.
*   **Utilisation des "Skills"** : Ne mettez pas les procédures complexes dans la mémoire globale. Créez des fichiers `.md` dans un dossier `/skills`. Claude ne les lira que lorsqu'il en aura besoin, économisant ainsi de l'argent et de l'intelligence.
*   **CLI plutôt que MCP** : Pour connecter des outils comme Notion ou GitHub, utilisez leurs interfaces en ligne de commande (**CLI**) via un skill. C'est beaucoup plus léger en jetons (tokens) que le protocole MCP.
*   **Bypass Permissions** : Dans les réglages, activez "Allow bypass permissions" (avec précaution) pour permettre à Claude d'enchaîner les tâches de codage sans vous demander votre accord à chaque fichier modifié.
*   **Une tâche = Une session** : Ne faites pas tout dans le même chat. Ouvrez une nouvelle session pour chaque nouvelle fonctionnalité afin de repartir avec une "barre de contexte" propre.

### 4) Chiffres de revenus et d'usage
*   **Dépenses API Claude** : Plus de **10 000 € / mois** (affirmé par l'auteur).
*   **Volume de jetons** : **28,48 milliards de tokens** générés en 30 jours (affirmé par l'auteur).
*   **Emails envoyés (via Lumail)** : **4 634 046** emails (affirmé par l'auteur).
*   **Coût abonnement "Max 20x"** : **200 $ / mois** (affirmé par l'auteur).
*   **Revenus des SaaS** : L'auteur affirme en avoir créé plusieurs, mais les revenus exacts générés par chaque application ne sont **pas précisés** dans cette vidéo.
