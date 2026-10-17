# La FIN de Claude Code : son code a été entièrement leaks (tout le monde peut copier leur feature)

Vidéo : https://youtu.be/OWdMpgGLkio · durée 22:29 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur analyse la fuite accidentelle de l'intégralité du code source de **Claude Code** (l'outil CLI d'Anthropic) survenue via la publication d'un fichier source map (`.map`) sur npm. Il décortique les fonctionnalités avancées et cachées découvertes dans la base de code (mode proactif 24/7, consolidation de mémoire « Dream Mode », compagnon virtuel Tamagotchi « Buddy », classifieur de permissions, etc.), évalue la qualité du code à l'aide de modèles d'IA et explique comment la communauté adapte déjà ces concepts pour d'autres modèles.

---

### 2) Outils, sites et dépôts cités

* **Claude Code (`@anthropic-ai/claude-code`)** :
  * *Statut :* Payant (accès via API / abonnement Anthropic).
  * *Utilité :* CLI officiel d'Anthropic pour le développement assisté par agent IA (vibe coding, exécution de commandes, refactorisation).
* **OpenClaude (par GitLawb)** :
  * *Statut :* Gratuit (Open source sur GitHub / GitLab).
  * *Utilité :* Fork / réécriture de Claude Code permettant d'utiliser son architecture et ses outils avec n'importe quel LLM (GPT, Gemini, DeepSeek, Ollama, MiniMax, etc.).
* **Cursor** :
  * *Statut :* Freemium (version gratuite disponible, formules payantes).
  * *Utilité :* Éditeur de code assisté par IA utilisé par l'auteur pour parcourir, auditer et exécuter des requêtes sur les fichiers leakés.
* **Excalidraw (`app.excalidraw.com`)** :
  * *Statut :* Gratuit (avec options payantes / freemium).
  * *Utilité :* Tableau blanc virtuel utilisé pour organiser visuellement les tweets et les schémas de la présentation.
* **X (Twitter)** :
  * *Statut :* Gratuit (avec options payantes).
  * *Utilité :* Plateforme source où les ingénieurs d'Anthropic (comme Boris Cherny) et la communauté tech ont publié les analyses et confirmations de la fuite.
* **Plateforme de configuration / Formation de l'auteur (`mlv.sh/fc` / `codelynx.dev`)** :
  * *Statut :* Gratuit (selon l'auteur).
  * *Utilité :* Propose un script d'installation (`AIBlueprint`), une configuration clé en main pour Claude Code (agents, skills, permissions, statusline) et des tutoriels d'installation pour Windows (WSL) et macOS/Linux.
* **Axios** :
  * *Statut :* Gratuit (Open source).
  * *Utilité :* Bibliothèque HTTP JavaScript identifiée dans les dépendances internes du code source de Claude Code.
* **npm** :
  * *Statut :* Gratuit.
  * *Utilité :* Gestionnaire de paquets Node.js sur lequel le fichier source map a été publié par erreur.

---

### 3) Astuces concrètes et réutilisables

* **Implémenter un mode proactif (boucle événementielle / Heartbeat) :** Structurer ses propres agents autonomes avec un système de « tick loop » pour qu'ils tournent en tâche de fond, détectent les erreurs, préparent des tests ou rédigent des pull requests sans intervention humaine constante.
* **Adopter la consolidation de mémoire (« Dream Mode ») :** Mettre en place un sous-agent qui s'exécute périodiquement pour relire les logs/transcriptions des sessions, synthétiser les apprentissages et purger les contextes obsolètes dans des fichiers de mémoire dédiés.
* **Mettre en place un classifieur de permissions (« Auto-mode ») :** Gagner du temps d'exécution en utilisant un modèle rapide pour classifier les commandes : autoriser automatiquement les lectures de fichiers/actions sans risque et restreindre/demander confirmation pour les actions destructives.
* **Gamifier l'expérience utilisateur (compagnons / feedback) :** Utiliser des concepts de gamification (comme le système « Buddy » avec statistiques, raretés et art ASCII généré selon l'identifiant utilisateur) pour créer des produits SaaS ou CLI plus engageants.
* **Sécuriser ses déploiements :** Pour préserver sa propriété intellectuelle et éviter le piratage d'un projet propriétaire, configurer impérativement `.npmignore` et les bundlers pour ne jamais inclure les fichiers source maps (`.js.map`) en production.
* **Respecter la légalité et le copyright :** L'auteur rappelle qu'Anthropic applique des DMCA takedowns sur les dépôts GitHub reprenant le code source leaké ; pour monétiser légalement des solutions dérivées, il convient de recoder la logique sous une autre forme (ex. réécriture en Python / « clean-room implementation ») sans copier le code protégé.

---

### 4) Chiffres de revenus annoncés

* Aucun chiffre de revenus n'est mentionné dans la vidéo (*non précisé*).
