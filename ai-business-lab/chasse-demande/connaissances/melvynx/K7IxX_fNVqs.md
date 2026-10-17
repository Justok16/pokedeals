# Deviens un EXPERT de Codex : la formation avancée

Vidéo : https://youtu.be/K7IxX_fNVqs · durée 1:20:08 · résumé Gemini (gemini-3.5-flash-lite) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

### 1) Idée principale de la vidéo
La vidéo est un tutoriel avancé sur l'utilisation de **Codex / Claude Code** (assistant IA de codage), présenté par un créateur qui partage son expérience et ses astuces pour maximiser l'efficacité des agents IA dans le développement logiciel, la gestion de projets, l'optimisation des contextes et l'automatisation des tâches complexes (comme la migration de code ou le refactoring).

---

### 2) Outils, sites et dépôts GitHub cités
* **Codex (ou Claude Code / Codex-Spark)**
  * **Prix :** Payant (forfait Pro à 200 $ / mois mentionné, avec des recharges de crédits possibles ; modèle Freemium/Payant basé sur des abonnements et des tokens).
  * **Utilité :** Assistant IA avancé pour le développement de logiciels, la gestion de projets à distance (via SSH), l'exécution de commandes, la création de PR (Pull Requests), etc.
* **Tella (tella.tv / tella-to-mella)**
  * **Prix :** Non précisé (probablement payant/freemium).
  * **Utilité :** Outil d'hébergement, de lecture et de gestion de vidéos (utilisé pour l'hébergement et le player des vidéos de formation).
* **GitHub (github.com)**
  * **Prix :** Gratuit (avec des plans payants).
  * **Utilité :** Plateforme de gestion de code source et de versioning (utilisée pour créer des dépôts, gérer des branches, des pull requests et du code distant).
* **Mux (mux.com)**
  * **Prix :** Payant (service d'infrastructure vidéo basé sur la consommation).
  * **Utilité :** API et service cloud pour l'encodage, le stockage et le streaming de vidéos.
* **X (anciennement Twitter - x.com)**
  * **Prix :** Gratuit.
  * **Utilité :** Réseau social utilisé pour suivre des actualités sur l'IA et le développement (notamment le compte du gourou « Tibo »).

---

### 3) Astuces concrètes et réutilisables
* **Contrôle à distance (Remote Control) :** Il est possible de lier son téléphone ou un autre appareil (via QR code ou code de pairage) pour contrôler Codex sur son ordinateur principal à distance, ou de connecter des serveurs via **SSH** pour exécuter du code sur des machines distantes (VPS) et économiser les ressources de sa propre machine.
* **Gestion stricte du contexte (« Traite ton contexte comme ton temps ») :**
  * Éviter de gonfler inutilement le contexte avec des prompts, des compétences (skills) ou des fichiers système inutiles pour contrer le phénomène de « Lost in the middle » (baisse d'attention du modèle au milieu de grands contextes).
  * Ne pas augmenter le contexte à 1 million de tokens inutilement : cela coûte jusqu'à 5 fois plus cher et dégrade la qualité des réponses. Préférer un contexte court et ciblé (ex: autour de 250k tokens).
* **Utilisation des Worktrees Git :** Créer des branches de travail isolées (worktrees) pour permettre à l'IA de travailler en arrière-plan sur des fonctionnalités complexes (comme des refactorings massifs) sans bloquer la branche principale (`main`) ni saturer un seul fil de discussion.
* **Utilisation des Hooks (fichiers `hooks.json` ou scripts personnalisés) :**
  * Mettre en place des gardes-fous (ex: un hook `PreToolUse` avec un script Python) pour interdire à l'IA d'exécuter des commandes destructrices (comme `rm -rf`, `git reset --hard`, ou la suppression de bases de données).
* **Technique du « Goal » (`/goal`) :** Donner des objectifs clairs et mesurables à l'IA (résultat attendu, vérification par la preuve/évidence, et contraintes) pour l'empêcher d'arrêter prématurément sa tâche et l'obliger à prouver que son code fonctionne (par exemple en lançant un navigateur de test via `dev-browser`).
* **Utilisation des chats parallèles (`/side`) :** Lancer des sous-conversations temporaires pour tester des idées ou poser des questions sans polluer le fil de discussion principal du projet.

---

### 4) Chiffres de revenus annoncés (affirmés par l'auteur)
* **Revenus du créateur :** **10 000 $ de MRR** (Revenu Mensuel Récurrent) générés grâce à ses projets et tunnels de vente IA (« *scaling / l'humain à 10k MRR* »).
* **Dépenses en IA/API :** Le créateur affirme dépenser l'équivalent de **plus de 40 000 $ par mois** en Codex/API s'il devait payer l'utilisation brute de ses tokens à l'échelle de son activité (« *j'ai dépensé pour plus de 40 000 dollars en Codex si je prenais l'équivalent API* »).
