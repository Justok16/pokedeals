# Claude Opus 5 m'a créé un site à 10.000€ en un prompt !

Vidéo : https://youtu.be/gwKurw7tk7g · durée 9:29 · résumé Gemini (gemini-3.5-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé détaillé de la vidéo, structuré pour répondre aux besoins d'une personne souhaitant utiliser l'IA de manière professionnelle et légale pour créer des sites web de qualité supérieure.

---

### 1) Idée principale
L'objectif de la vidéo est de montrer comment dépasser le design générique, répétitif et souvent considéré comme « moche » des sites web créés par défaut par l'IA. Pour ce faire, l'auteur explique comment injecter des compétences de design (skills), des bibliothèques de composants animés et des outils de déploiement directement dans **Claude Code** (via le protocole MCP). Cela permet de générer un site web unique, haut de gamme, entièrement animé et de le publier en ligne en une seule commande.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude (Application desktop d'Anthropic) & Claude Code**
    *   *Statut :* Gratuit pour l'application de base / Utilisation de l'API (tokens) payante pour Claude Code (*précision exacte des tarifs non mentionnée*).
    *   *Rôle :* L'assistant de codage IA principal utilisé pour générer l'intégralité du code du site.
*   **UI UX Pro Max Design Intelligence (uipm.co)**
    *   *Dépôt GitHub :* `nextlevelbuilder/ui-ux-pro-max-skill`
    *   *Statut :* Gratuit (dépôt GitHub) avec des options Premium sur le site.
    *   *Rôle :* Fournit à Claude des bases de données de styles UI, de palettes de couleurs, d'associations de polices et de templates pour améliorer ses compétences en web design.
*   **Impeccable (impeccable.style)**
    *   *Dépôt GitHub :* `pbakaus/impeccable`
    *   *Statut :* Gratuit.
    *   *Rôle :* Un outil qui nettoie le "AI slop" (les tics de design répétitifs de l'IA comme le fond beige systématique, les polices serif en italique et les petites bordures) pour forcer l'IA à créer un design plus moderne et unique.
*   **Magic UI (magicui.design)**
    *   *Statut :* Gratuit et open-source (avec des templates/composants Pro payants).
    *   *Rôle :* Une bibliothèque de composants UI animés (React, TypeScript, Tailwind CSS, Motion). Elle est connectée à Claude via MCP pour lui permettre d'insérer des animations complexes.
*   **Hostinger (hostinger.fr / hostinger.com)**
    *   *Statut :* Payant (le plan « Business » est présenté à 3,79 €/mois).
    *   *Rôle :* L'hébergeur web utilisé pour stocker le site et réserver le nom de domaine.
*   **Hostinger Connector**
    *   *Statut :* Gratuit (inclus avec l'hébergement).
    *   *Rôle :* Un outil MCP qui connecte Hostinger directement à Claude Code, permettant de publier le site sur un serveur en ligne sans passer par GitHub ou des configurations manuelles complexes.
*   **GSAP & Three.js**
    *   *Statut :* Gratuit (bibliothèques JavaScript open-source).
    *   *Rôle :* Utilisés dans le prompt pour ajouter des animations fluides au défilement (scroll) et des rendus d'images haut de gamme.

---

### 3) Astuces concrètes et réutilisables

*   **Activer le mode automatique dans Claude Code :** Passer l'outil en mode `Auto` pour lui permettre d'exécuter des commandes et d'écrire des fichiers sans demander une autorisation manuelle à chaque étape.
*   **Alimenter l'IA en compétences (Skills) avant de rédiger le prompt :** Au lieu de lui demander directement de créer un site, fournissez d'abord à Claude Code les URL GitHub de bibliothèques de design (comme *UI UX Pro Max* et *Impeccable*) pour définir des règles de qualité visuelle.
*   **Exploiter le Model Context Protocol (MCP) :** Utilisez ce protocole pour connecter des serveurs d'outils tiers (comme *Magic UI* pour le design ou *Hostinger* pour le déploiement) directement dans l'environnement de Claude.
*   **Rédiger un prompt de structure stricte :** Pour obtenir un effet haut de gamme, demandez explicitement des animations au scroll (via GSAP), des effets de flou au chargement (blur load), et demandez à l'IA de s'inspirer de la charte graphique d'une marque de luxe reconnue (dans l'exemple : Apple).
*   **Réduction Hostinger :** L'auteur partage le code promo `EASYWORDPRESS` permettant d'obtenir 10 % de réduction supplémentaire sur l'hébergement Hostinger.

---

### 4) Chiffres de revenus annoncés

*   *Affirmé par l'auteur :* **Aucun chiffre de revenus** précis n'est annoncé ou promis dans cette vidéo (*non précisé*). L'auteur mentionne simplement qu'il s'agit d'une méthode pour professionnaliser la création de sites web et potentiellement "en faire son métier".
