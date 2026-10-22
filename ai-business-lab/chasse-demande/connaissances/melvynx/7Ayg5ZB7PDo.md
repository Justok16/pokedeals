# Formation Claude Code Avancées : devenir un PRO de Claude Code avec ces méthodes avancées

Vidéo : https://youtu.be/7Ayg5ZB7PDo · durée 1:13:42 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes consignes :

### 1) Idée principale
La vidéo propose un guide avancé d’utilisation de **Claude Code** pour optimiser, automatiser et structurer le développement de projets logiciels à l’aide de l’intelligence artificielle (via des sous-agents, des workflows, des skills et des méta-prompts), afin d’en faire un levier de productivité (et potentiellement de monétisation).

---

### 2) Outils, sites et dépôts GitHub cités
* **Claude Code** (outil principal) : Interface en ligne de commande/agent pour interagir avec les modèles Claude. (Modèle payant via l'API Anthropic / non précisé pour l'outil lui-même, mais lié aux coûts d'API).
* **Visual Studio Code (VS Code)** : Éditeur de code utilisé pour manipuler les dossiers et fichiers `.claude`. (Gratuit).
* **Exal.ai** (ou Exa) : API de recherche web optimisée pour les agents IA et les LLM. (Modèle économique non précisé dans la vidéo, mais présenté comme une API payante/freemium).
* **Proxyman** : Outil pour inspecter et capturer le trafic HTTP/HTTPS (utilisé pour analyser les requêtes faites par Claude Code). (Version gratuite/payante, non précisée en détail).
* **EscalIdraw** : Outil de schéma et de dessin (utilisé pour illustrer les concepts de méta-prompts et de workflows). (Gratuit).

---

### 3) Astuces concrètes et réutilisables
* **Gestion du dossier `.claude`** : Structurer ses projets avec des sous-dossiers spécifiques (`projects`, `sessions`, `rules`, `tasks`, `skills`, `agents`) pour permettre à Claude Code de retrouver l'historique des discussions, les plans et les règles globales.
* **Méta-prompts** : Créer des prompts qui génèrent des prompts (par exemple, un `skill` nommé `meta-prompt-creator`) pour automatiser la création de prompts complexes et performants adaptés aux LLM (Anthropic, OpenAI, Google).
* **Utilisation de sous-agents et Workflows** : Créer des sous-agents spécialisés (ex. `explore-codebase`, `explore-docs`, `fast-websearch`) et les enchaîner dans un workflow rigoureux en 4 étapes (Analyser $\rightarrow$ Planifier $\rightarrow$ Exécuter $\rightarrow$ Vérifier) pour guider l’IA de manière structurée et éviter les erreurs.
* **Gestion du contexte (Lost in the middle)** : Pour contrer le biais cognitif des LLM qui ont tendance à oublier les informations situées au milieu de grands contextes, structurer les prompts de manière stratégique (placer les instructions critiques au début et à la fin) et utiliser des agents spécialisés pour limiter la taille du contexte global.
* **Git Worktree pour le travail parallèle** : Utiliser `Git Worktree` pour lancer plusieurs instances de travail en parallèle sur des branches ou des dossiers séparés, permettant à plusieurs agents de travailler simultanément sur un même projet sans conflits.

---

### 4) Chiffres de revenus annoncés (affirmés par l'auteur)
* **Revenus financiers directs** : **Non précisé** (l'auteur mentionne avoir dépensé plus de **15 000 $** dans l'API de Claude, mais ne donne aucun chiffre précis sur ses revenus générés).
