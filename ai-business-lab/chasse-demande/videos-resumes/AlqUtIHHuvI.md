# Vidéo https://youtu.be/AlqUtIHHuvI

> Résumé produit par Gemini (via le relais Vercel) le 25/09/2026. Les chiffres de revenus sont **affirmés par l’auteur de la vidéo, non vérifiés**.

Voici un résumé de la vidéo, en français, axé sur l'utilisation de l'IA (notamment Claude Code) pour gagner de l'argent et optimiser les entreprises, avec les outils mentionnés :

---

**Idée Principale :**
Le présentateur affirme qu'il utilisait mal Claude et que l'intégration de dépôts GitHub spécialisés peut transformer Claude en un outil "des ordres de grandeur plus puissant". L'objectif est d'utiliser ces "skills" (compétences) ou "MCPs" (Model Context Protocols) pour doper les capacités de Claude, le transformant en un assistant IA ou même une équipe d'agents IA complète, capable de gérer des aspects complexes d'une entreprise ou de tâches de recherche, souvent de manière autonome.

**Les Outils et Dépôts GitHub :**

1.  **Last30Days** (dépôt GitHub : mvanhorn/last30days-skill)
    *   **Gratuit/Payant :** Gratuit (dépôt GitHub).
    *   **Description :** Un moteur de recherche piloté par l'IA qui évalue le sentiment du public sur des sujets donnés. Il scanne des plateformes comme Reddit, X (anciennement Twitter), YouTube, Hacker News, Polymarket et le web pour identifier ce qui est populaire, surévalué, ou ce dont les gens se plaignent, fournissant des opinions réelles plutôt que des agrégations d'articles de presse.
    *   **Utilité :** Idéal pour la recherche marketing, l'étude de nouveaux produits, la compréhension des tendances sociales, l'analyse des opinions publiques sur des sujets spécifiques, et la recherche de contenu pour des vidéos ou des articles.

2.  **Playwright MCP** (dépôt GitHub : microsoft/playwright-mcp)
    *   **Gratuit/Payant :** Gratuit (dépôt GitHub, solution officielle de Microsoft).
    *   **Description :** Un serveur Model Context Protocol (MCP) qui permet aux LLMs comme Claude d'interagir directement avec des pages web via des "snapshots" d'accessibilité structurés, sans avoir besoin de captures d'écran.
    *   **Utilité :** Confère à Claude la capacité de naviguer sur internet, de cliquer, de taper, de lire des structures de pages, de remplir des formulaires et de collecter des données de manière beaucoup plus rapide et autonome qu'un simple navigateur ou un système basé sur des captures d'écran. Permet d'automatiser des tâches web complexes.

3.  **Archify** (dépôt GitHub : tt-ai/archify)
    *   **Gratuit/Payant :** Gratuit (dépôt GitHub).
    *   **Description :** Une compétence d'agent IA qui crée des diagrammes d'architecture, de workflow, de séquence, de flux de données et de cycle de vie. Il prend une description en langage naturel (anglais simple) et génère un diagramme HTML auto-contenu, exportable.
    *   **Utilité :** Permet de visualiser et de comprendre des processus complexes, de créer des Procédures Opératoires Standard (SOPs), de planifier des systèmes et de documenter des architectures. Très utile pour les consultants ou les entreprises souhaitant automatiser ou clarifier leurs workflows.

4.  **Claude Ads** (dépôt GitHub : AgrciDaniel/claude-ads)
    *   **Gratuit/Payant :** Gratuit (dépôt GitHub).
    *   **Description :** Un "système d'exploitation publicitaire payant" multi-plateformes et une compétence d'optimisation pour Claude Code. Il permet d'auditer, de planifier, de créer et d'optimiser des campagnes publicitaires sur Google Ads, Meta Ads, YouTube, LinkedIn, TikTok, Microsoft Ads, Apple Ads et Amazon Ads.
    *   **Utilité :** Automatise la gestion complète des publicités payantes. Il exécute des audits, propose des plans d'action basés sur un "score de santé" de l'annonce, aide à la création de créatifs (images, vidéos, texte), et surveille les performances. Il est présenté comme un moyen d'avoir une "agence publicitaire entière" au sein de Claude.

5.  **Gstack** (dépôt GitHub : garrytan/gstack)
    *   **Gratuit/Payant :** Gratuit (dépôt GitHub).
    *   **Description :** C'est la configuration exacte de Claude Code utilisée par Garry Tan, le PDG de Y Combinator. Elle comprend 23 outils spécialisés agissant comme des rôles d'entreprise (PDG, designer, ingénieur, QA, etc.) et suit un processus de "sprint" (Penser -> Planifier -> Construire -> Réviser -> Tester -> Expédier -> Réfléchir).
    *   **Utilité :** Permet à Claude de gérer des workflows complets de développement de produits et de services, en simulant les interactions d'une équipe d'entreprise. Il intègre des outils pour la révision du code (par OpenAI Codex ou Claude Code), des garde-fous de sécurité, la navigation web, la gestion des déploiements, et bien plus encore.

6.  **Agency Agents** (dépôt GitHub : msitarzewski/agency-agents)
    *   **Gratuit/Payant :** Gratuit (dépôt GitHub).
    *   **Description :** Une collection complète d'agents IA spécialisés, organisés en divisions (académique, design, ingénierie, finance, marketing, ventes, etc.). Chaque agent est un expert formé avec une personnalité, des processus et des livrables spécifiques, conçu pour agir comme un employé réel dans un domaine donné. Il y a 279 agents disponibles.
    *   **Utilité :** Fournit une "agence IA" clé en main. Permet de choisir et d'intégrer des agents spécialisés pour diverses fonctions d'entreprise, pour ceux qui veulent étendre leur activité via des agents IA sans devoir tout coder.

7.  **Buzz** (dépôt GitHub : block/buzz)
    *   **Gratuit/Payant :** Gratuit (dépôt GitHub, créé par Jack Dorsey).
    *   **Description :** Une plateforme de communication "hive mind" auto-hébergeable où les humains et les agents IA partagent les mêmes espaces de travail, fonctionnant comme un "Slack pour agents".
    *   **Utilité :** Permet d'orchestrer et de superviser le travail d'une équipe hybride d'humains et d'agents IA. Les agents peuvent converser, accomplir des tâches, fournir des mises à jour et collaborer sur des projets au sein de canaux dédiés. Il est conçu pour que les agents et les humains "parlent tous le même protocole".

**Astuces Concrètes et Réutilisables :**

*   **Ne pas se contenter de Claude "stock" :** Toujours chercher à augmenter les capacités de Claude avec des outils et dépôts tiers adaptés à vos besoins.
*   **Recherche approfondie :** Utiliser des outils comme **Last30Days** pour obtenir des insights basés sur le sentiment social réel du web (Reddit, YouTube, X), pas seulement des articles de presse. Cela est crucial pour comprendre le marché, affiner les offres de produits ou générer des idées de contenu qui résonnent.
*   **Automatisation web avancée :** Exploiter **Playwright MCP** pour que Claude puisse interagir directement avec les navigateurs web de manière autonome (cliquer, remplir des formulaires, extraire des données), ce qui est bien plus efficace que des captures d'écran.
*   **Visualisation et optimisation des processus :** Utiliser **Archify** pour transformer des descriptions textuelles de workflows en diagrammes clairs et exploitables. Cela aide à mieux comprendre, documenter et automatiser les processus métier.
*   **Gestion IA des campagnes publicitaires :** Implémenter **Claude Ads** pour auditer, planifier et optimiser vos publicités payantes sur plusieurs plateformes, en identifiant les points faibles et en suggérant des améliorations.
*   **Construire une "entreprise IA" :** Adopter des frameworks comme **Gstack** ou **Agency Agents** pour simuler une équipe d'agents IA spécialisés qui collaborent pour accomplir des tâches complexes, du développement de produits à la gestion des opérations, en passant par le marketing et la finance.
*   **Orchestration humain-IA :** Intégrer **Buzz** pour créer un espace de travail collaboratif où les humains et les agents IA peuvent interagir et coordonner leurs efforts de manière transparente.
*   **Empiler les outils (Tool Stacking) :** La véritable puissance vient de la combinaison de ces outils. Par exemple, utiliser **Last30Days** pour identifier des tendances, puis **Claude Ads** pour créer des campagnes basées sur ces tendances, et **Playwright MCP** pour automatiser la collecte de données sur les concurrents.
*   **Documentation des SOPs :** Consigner toutes les procédures de votre entreprise dans une base de données (ex: Notion), puis les utiliser avec **Archify** pour créer des architectures visuelles, qui peuvent ensuite être utilisées pour entraîner ou orchestrer des agents.

**Chiffres de Revenus Annoncés (Affirmés par l'auteur) :**

*   "lancement d'une communauté payante pour les opérateurs IA à 49$/mois" (01:19) – affirmé par l'auteur, concernant son propre projet.
*   "500 membres fondateurs à 39$ à vie" (01:19) – affirmé par l'auteur, concernant son propre projet.
*   "Y Combinator gère un estimé de 12.2 milliards de dollars d'actifs et a levé environ 2 milliards de dollars" (01:45) – affirmé par l'auteur, comme contexte pour l'outil Gstack.

---
