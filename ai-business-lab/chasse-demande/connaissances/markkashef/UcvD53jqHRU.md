# These Mods Take Claude Code to Another Level (Mark Kashef)

Vidéo : https://youtu.be/UcvD53jqHRU · résumé Gemini (gemini-3-flash-preview) du 2026-10-07, envoyée par l'utilisateur
(connaissances générales, non vérifiées : tout chiffre ou prix est à contrôler à la source officielle)

### 1) Idée principale
L'auteur explique comment transformer **Claude Code** en un orchestrateur ultra-puissant en utilisant des "mods" (extensions personnalisées). L'idée est de permettre à Claude Code de dépasser ses limites natives pour :
*   Prendre le contrôle d'applications tierces sur votre ordinateur (via Codex).
*   Lancer des tâches complexes en parallèle en utilisant différents modèles d'IA (Sonnet, Opus, Haiku) simultanément pour gagner en productivité.

### 2) Outils, sites et dépôts cités
*   **Claude Code** : (Payant - via crédits API/abonnement) L'interface en ligne de commande d'Anthropic. Sert de "cerveau" pour orchestrer les tâches.
*   **Codex (app)** : (Payant - nécessite un abonnement existant) Utilisé ici spécifiquement pour sa fonction de "Computer Use" (contrôle de l'ordinateur).
*   **Dépôt GitHub de Mark Kashef** : (Gratuit) Contient le code source des mods présentés pour que l'utilisateur puisse les "brancher" directement (lien mentionné en description de la vidéo originale).
*   **MCP (Model Context Protocol)** : (Gratuit - Protocole) Utilisé comme pont technique pour connecter Claude à d'autres serveurs et outils.
*   **Skool.com/earlyaidopters** : (Payant) Communauté de l'auteur pour apprendre à bâtir et vendre des solutions basées sur l'IA.

### 3) Astuces concrètes et réutilisables
*   **Le Mod "Codex-CU"** : Permet à Claude d'utiliser la calculatrice ou l'éditeur de texte de votre Mac en arrière-plan sans bloquer votre souris. Utile pour automatiser des rapports ou des calculs complexes.
*   **L'orchestration multi-modèles (Mod "Threads")** : Vous pouvez demander à Claude de créer des sous-fils de discussion. Par exemple : un fil avec *Opus* pour la stratégie, un avec *Sonnet* pour le code, et un avec *Haiku* pour la relecture. Ils travaillent ensemble et centralisent la réponse.
*   **La commande `/goal`** : Une technique de "meta-prompt" pour forcer l'IA à tester son propre travail étape par étape et à s'auto-corriger jusqu'à atteindre l'objectif fixé.
*   **Gestion des permissions** : L'auteur a créé un "Helper" (assistant) qui valide automatiquement les demandes de permissions répétitives entre les outils, fluidifiant l'automatisation.
*   **Vérification par `claude --help`** : Utiliser cette commande pour que Claude analyse ses propres capacités et se "rappelle" comment manipuler ses outils avant d'exécuter une tâche complexe.

### 4) Chiffres et revenus
*   **1 788 $ par an** : (Affirmé par l'auteur). Ce chiffre apparaît dans la démo technique comme le résultat d'un calcul de coûts d'abonnement (149 $/mois) réalisé automatiquement par l'IA.
*   **Note sur les gains** : L'auteur ne cite pas de chiffre d'affaires précis généré par ces mods, mais insiste sur le fait que ces outils permettent de "bâtir, vendre ou utiliser l'IA au travail" pour générer de la valeur.
*   **Coûts d'infrastructure** : L'auteur précise que cette méthode permet d'utiliser votre abonnement Codex existant au lieu de payer des frais supplémentaires via l'API "Agents", ce qui optimise les marges bénéficiaires (montant exact de l'économie : **non précisé**).
