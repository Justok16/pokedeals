# Actu IA : le nouveau navigateur de Claude, l'IA arrive sur Spotify et le nouveau matériel d'OpenAI

Vidéo : https://youtu.be/ss2LaCKUQmU · durée 23:10 · résumé Gemini (gemini-3.6-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé détaillé de la vidéo, structuré selon vos critères :

---

### 1) Idée principale
La vidéo est une revue hebdomadaire des actualités majeures de l'intelligence artificielle présentée par Matt Wolfe. Elle couvre les dernières mises à jour d'applications pour développeurs (navigateur intégré à Claude Code, open-source de Grok Build), le lancement de nouveaux modèles (Inkling, Bonsai 27B, Kimi K3), des intégrations concrètes d'agents IA (DoorDash CLI, 1Password avec Claude), des annonces matérielles et des initiatives d'infrastructure (calcul IA distribué chez les particuliers).

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Code (Anthropic)** : [Payant / Inclus dans l'abonnement Claude] — Application desktop pour développeurs. Elle intègre un navigateur web interne permettant d'inspecter le DOM, de sélectionner des éléments visuels pour modifier le code en direct et de naviguer/scraper le web sans passer par des API payantes.
*   **Google Search / Mode IA** : [Gratuit] — Mode de recherche IA de Google permettant désormais de connecter des applications externes (comme Instacart) directement depuis l'interface de recherche par simples prompts.
*   **Google Vids** : [Gratuit / Inclus dans Google Workspace] — Outil de création de présentations vidéo intégrant Gemini Omni, l'édition par chat et la génération d'avatars personnalisés dans des scènes vidéo.
*   **Spotify AI Voice ("Just Say the Word")** : [Payant (Spotify Premium)] — Assistant vocal interactif intégré à l'application mobile Spotify pour créer des playlists à partir de l'historique, explorer sa musique ou poser des questions sur des artistes.
*   **Seedream 5.0 Pro (ByteDance)** *(via **Artlist**)* : [Payant via abonnement Artlist] — Générateur d'images multimodal acceptant jusqu'à 5 images de référence pour contrôler le style, la composition, les personnages et générer du texte lisible ou des infographies.
*   **Artlist** : [Payant] — Plateforme de ressources créatives intégrant le module *AI Toolkit* avec le modèle Seedream 5.0 Pro.
*   **Inkling (Thinking Machines Lab)** : [Gratuit en essai / Payant via API] — Modèle de langage et multimodal open-weights de 952 milliards de paramètres (fichier de 1,9 To).
*   **Tinker** (`thinkingmachines.ai/tinker`) : [Gratuit en playground / Payant via API] — Plateforme permettant de tester et de fine-tuner le modèle Inkling.
*   **Hugging Face (`thinkingmachines/inkling`)** : [Gratuit] — Dépôt permettant de télécharger les poids du modèle Inkling.
*   **BuseyBench** : [Gratuit] — Benchmark mesurant la capacité des modèles IA à générer du code SVG.
*   **PrismML - Bonsai 27B** : [Gratuit] — Modèle ultra-compressé (1-bit, ~4 Go) de 27 milliards de paramètres conçu pour tourner localement sur smartphone. Démo disponible sur Hugging Face (`webml-community/bonsai-webgpu-kernels`).
*   **Moonshot AI - Kimi K3** : [Gratuit (poids ouverts prévus)] — Modèle open-weights puissant de 2,8 billions de paramètres spécialisé dans le codage, le raisonnement et les tâches d'agents.
*   **Grok Build (SpaceX AI / xAI)** : [Gratuit] — Agent de codage et interface terminal (TUI) open-sourcé par SpaceX AI. Dépôt GitHub : `xai-org/grok-build`.
*   **Automations in Grok (xAI)** : [Payant (Abonnement X/Grok)] — Système de tâches programmées et de déclencheurs (récurrents ou basés sur les emails reçus) au sein de Grok.
*   **ChatGPT Search (OpenAI)** : [Gratuit / Payant] — Fonctionnalité de recherche interne améliorée dans ChatGPT (filtres par projets, discussions, images et documents).
*   **Claude + 1Password (Anthropic)** : [Payant] — Intégration sécurisée (« zero-exposure ») permettant à l'agent Claude d'utiliser 1Password pour se connecter à des sites web sans avoir accès directement aux mots de passe.
*   **DoorDash CLI (`dd-cli`)** : [Gratuit sur liste d'attente (macOS US/Canada)] — Interface en ligne de commande permettant aux agents IA (OpenClaw, Hermes, Codex, etc.) d'effectuer des commandes de repas automatiquement.
*   **Meta Instagram AI Image Tagging** : [Désactivé] — Fonctionnalité retirée par Meta suite au mécontentement des créateurs concernant la création de deepfakes d'utilisateurs publics.
*   **Siri AI / Apple Intelligence** : [Gratuit avec matériel Apple compatible] — Nouvelle version de Siri déployée sur iOS et watchOS (Apple Watch).
*   **Claude for Teachers (Anthropic)** : [Gratuit pour les enseignants K-12 vérifiés aux USA] — Programme offrant l'accès gratuit aux capacités Premium de Claude pour l'éducation.
*   **Google Images (Mise à jour 25 ans)** : [Gratuit] — Interface repensée façon Pinterest avec suggestion d'images et génération d'images directe via le modèle Nano Banana.
*   **Gemini Notebook (ex-NotebookLM)** : [Gratuit] — Nouveau nom de NotebookLM par Google.
*   **Codex Creator Micro (OpenAI x Work Louder)** : [Payant (230 $)] — Clavier/pavé physique conçu pour interagir avec OpenAI Codex, disponible sur `openai.com/supply/`.
*   **Sunrun (Distributed AI Compute Program)** : [Programme pilote / Rémunéré] — Programme installant des micro-nœuds de calcul IA chez les particuliers (couplés à de l'énergie solaire/batterie) contre rémunération.
*   **Teachable (Atelier virtuel)** : [Gratuit] — Atelier en ligne animé par Matt Wolfe le 22 juillet axé sur l'automatisation personnelle et professionnelle avec l'IA.

---

### 3) Astuces concrètes et réutilisables

*   **Gain de temps et économie d'API avec Claude Code** :
    Dans l'application Claude Desktop (onglet *Code*), ouvrez un projet et utilisez le raccourci `Command + Shift + B` (ou l'icône navigateur). Vous pouvez pointer un composant d'une page web (ex. un bouton) et ordonner à Claude de modifier le code directement, ou lui faire scraper des sites sans payer d'API tierces coûteuses (comme l'API X/Twitter).
*   **Automatiser des actions web sécurisées via 1Password** :
    Liez l'agent Claude à 1Password pour lui permettre d'exécuter des parcours nécessitant une connexion web (ex. réservations, achats) sans avoir à saisir manuellement vos mots de passe et sans risquer de fuite d'identifiants.
*   **Connecter vos agents locaux au monde réel (DoorDash CLI)** :
    En utilisant des interfaces CLI comme `dd-cli`, vous pouvez configurer vos assistants ou agents locaux (OpenClaw, Hermes, Codex) pour exécuter des tâches concrètes de la vie quotidienne comme commander à manger à votre place.
*   **Optimiser l'accès aux outils Premium (Enseignants)** :
    Si vous êtes enseignant qualifié, profitez des offres comme *Claude for Teachers* pour accéder gratuitement aux versions payantes des modèles.

---

### 4) Chiffres de revenus annoncés

*   **Affirmé par l'auteur** : Aucun chiffre de revenus personnels ou de méthodes de gains financiers spécifiques n'est annoncé dans la vidéo (`non précisé`).
*   *Prix matériels/services mentionnés au passage dans la vidéo* :
    *   Clavier Codex Creator Micro : **230 $**
    *   Niveaux d'API X (Twitter) affichés à l'écran : **0 $ / 200 $ / 5 000 $ par mois**
    *   Indemnisation des clients du programme Sunrun : `non précisé`
