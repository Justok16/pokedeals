# pvdL7q1EuG4 — « Fable 5.2 for Web Design, 3D, UI and UX is Amazing »

- Auteur : Codex Community ; lien : https://youtu.be/pvdL7q1EuG4
- Envoyée par l'utilisateur ; résumée le 14/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (14/11)

Essai en anglais du modèle Claude Fable 5.2 pour la création de sites : un site en 3D animé, la refonte d'une page existante et un tableau de bord branché sur Zapier.

- **Sites en 3D animés (Three.js, GSAP)** : déjà en place (skills `threejs-web`, `threejs-animation` et `gsap-*`), avec notre règle des animations qui marchent aussi sur PC. Nouvelles démos en pause jusqu'au premier client payant.
- **Vite (outil de fabrication de projets web)** : écarté, inutile pour nous ; nos sites sont des pages simples mises en ligne sur Cloudflare Pages.
- **Fable 5.2 pour organiser un gros chantier, Opus 5.5 pour le travail courant** : déjà dans nos consignes (`connaissances/consignes-detaillees.md`, « Modèle à utiliser », conseil du 24/10).
- **Zapier relié à Claude, avec des droits limités (lire et préparer un brouillon, mais pas supprimer)** : connecteur Zapier déjà branché chez nous ; le principe des droits limités est déjà notre règle (brouillon validé pour les mails sensibles, ne jamais supprimer un fil).
- **Tableau de bord « résumé du jour » fabriqué pour un client à partir de ses mails et de son agenda** : en réserve ; pour nous, le point automatique du matin fait déjà ce travail. À ressortir si un client demande un outil sur mesure en plus de son site, et seulement avec son accord écrit sur l'accès à ses comptes.
- **Mode rapide du modèle** : écarté, réglage de l'abonnement de l'utilisateur, aucun besoin constaté.
- **T3 Code (autre éditeur pour agents, statut non précisé)** : écarté, Claude Code suffit.
- **TypeUI (typeui.sh)** : simple site d'exemple utilisé pour l'essai, rien à en faire.
- **Toujours contrôler à l'œil ce que l'IA produit (une lettre oubliée dans un logo pendant l'essai)** : déjà notre règle (`outils/test_pages.py`, contrôle `44-controle-qualite.md`, validation par l'utilisateur avant tout envoi).
- **Durées citées (un site 3D en 30 à 70 minutes, mode jusqu'à 2,5 fois plus rapide)** : affirmées par l'auteur, non vérifiées. Aucun chiffre de revenu dans la vidéo.

Conclusion : rien à installer, rien à changer ; la vidéo confirme nos outils (3D, GSAP) et notre partage des modèles.

## Résumé (Gemini)

Voici le résumé structuré de la vidéo, axé sur l'utilisation de l'IA et de Claude Code pour des opportunités professionnelles et d'automatisation :

---

### 1) Idée principale
La vidéo évalue les performances du nouveau modèle **Claude Fable 5.2** d'Anthropic (ainsi que Mythos 5.2). L'auteur teste sa capacité à générer des sites web 3D complexes (Three.js, GSAP), à redéfinir des interfaces utilisateur (UI/UX) et à orchestrer des flux de travail autonomes via le protocole MCP (Zapier). La conclusion est que Fable 5.2 excelle dans l'**orchestration globale de projets ambitieux** et la compréhension des intentions sans sur-ingénierie, tandis que Claude Opus 5.5 reste recommandé pour le codage quotidien.

---

### 2) Outils, sites et bibliothèques cités

*   **Claude Fable 5.2 & Mythos 5.2** (Anthropic)
    *   *Statut :* Payant (via API / abonnement Claude).
    *   *Rôle :* Modèle d'IA conçu pour l'orchestration technique, le raisonnement avancé et les tâches ouvertes/ambitieuses.
*   **Claude Opus 5.5** (Anthropic)
    *   *Statut :* Payant.
    *   *Rôle :* Modèle d'IA recommandé comme outil quotidien pour le développement et la rédaction de code standard.
*   **T3 Code**
    *   *Statut :* Non précisé.
    *   *Rôle :* Environnement / Éditeur de code utilisé dans la vidéo pour exécuter des agents de codage IA avec réglage du niveau de raisonnement.
*   **Zapier / Zapier MCP**
    *   *Statut :* Gratuit (version de base) / Payant.
    *   *Rôle :* Serveur MCP (Model Context Protocol) permettant de connecter l'IA à des applications tierces (Gmail, Google Calendar, Notion, etc.) avec des autorisations de sécurité granualaires.
*   **Three.js**
    *   *Statut :* Gratuit (Open Source).
    *   *Rôle :* Bibliothèque JavaScript pour la création et le rendu de graphismes 3D interactifs dans un navigateur web.
*   **GSAP (GreenSock Animation Platform)**
    *   *Statut :* Gratuit pour usage standard / Freemium.
    *   *Rôle :* Bibliothèque JavaScript dédiée aux animations web complexes et aux micro-interactions liées au défilement.
*   **Vite**
    *   *Statut :* Gratuit (Open Source).
    *   *Rôle :* Outil de build et serveur de développement web local utilisé par l'IA pour générer et tester des projets web.
*   **TypeUI (`typeui.sh`)**
    *   *Statut :* Non précisé (site d'exemple).
    *   *Rôle :* Site d'inspiration/modèles UI utilisé comme cas d'étude pour tester la refonte automatisée d'un site par l'IA.

---

### 3) Astuces concrètes et réutilisables

1.  **Vendre des services de Redesign Web & 3D à haute valeur ajoutée :**
    *   En fournissant un prompt structuré demandant une expérience web interactive (utilisant Vite, Three.js et GSAP), Fable 5.2 produit en 30 à 70 minutes des sites web 3D scénarisés (comme le site spatial *Astraeus* dans la vidéo). Cela permet d'offrir des services de conception web avancés à des clients en une fraction du temps habituel.
2.  **Architecture d'Orchestration d'Agents (Réduction de coûts/temps) :**
    *   Utiliser un modèle très intelligent (Fable 5.2) comme **orchestrateur** pour découper un grand projet, puis déléguer l'exécution des tâches simples à des modèles plus rapides ou moins chers (Opus, Sonnet, Haiku).
3.  **Création de Tableaux de Bord / Outils Métier sur-mesure via MCP :**
    *   Utiliser **Zapier MCP** dans Claude Desktop pour connecter l'IA aux données de travail d'un client (ex: Gmail, Google Calendar).
    *   Demander à l'IA de générer un composant/dashboard interactif (ex: *Daily Brief*) affichant les données essentielles en temps réel sans coder l'intégration manuellement.
4.  **Sécurisation des accès IA (Man-in-the-Middle) :**
    *   Configurer des limites strictes sur le serveur MCP (ex: autoriser la lecture d'e-mails et la création de brouillons, mais restreindre la suppression) pour éviter que les agents autonomes ne fassent des actions destructrices chez les clients.
5.  **Utiliser le "Fast Mode" pour les itérations :**
    *   Activer le mode rapide (génération jusqu'à 2,5x plus rapide) lors des phases de prototypage code pour accélérer les tests et baisser les délais de livraison.
6.  **Contrôle qualité systématique :**
    *   L'IA peut commettre des erreurs mineures (ex: oubli d'une lettre dans le logo "TypeU" au lieu de "TypeUI"). Toujours inspecter visuellement et tester le code généré avant livraison client.

---

### 4) Chiffres de revenus annoncés

*   **Non précisé** (l'auteur ne mentionne aucun chiffre de revenus financiers spécifiques générés personnellement dans cette vidéo).
