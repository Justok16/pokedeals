# Formation Codex CLI : La SEUL formation dont tu as besoin (TUTO COMPLET)

Vidéo : https://youtu.be/Qi8BAp7xGvE · durée 26:45 · résumé Gemini (gemini-3.5-flash, lot de 4) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) Idée principale**
Formation complète à l'installation, la configuration et l'utilisation de Codex CLI (l'agent IA d'OpenAI en ligne de commande) pour générer du code, analyser des données et automatiser des tâches terminal.

**2) Outils, sites ou dépôts GitHub cités**
*   **OpenAI Codex CLI (`@openai/codex`)** : Gratuit (l'outil CLI en lui-même) / Nécessite un abonnement ou clé API — Agent IA de codage en ligne de commande.
*   **ChatGPT Plus / Pro** : Payant (20 $/mois) — Abonnement OpenAI permettant d'utiliser Codex CLI sans payer de supplément d'API.
*   **Terminal (zsh, WSL, macOS Terminal)** : Gratuit — Interface en ligne de commande de l'ordinateur.
*   **iTerm2 / Ghostty** : Gratuit — Applications de terminal alternatives recommandées sur Mac.
*   **Node.js / npm / nvm** : Gratuit — Environnement d'exécution JavaScript et gestionnaire de paquets nécessaires à l'installation.
*   **Visual Studio Code (VS Code)** : Gratuit — Éditeur de code source.
*   **Vite / Tailwind CSS / shadcn/ui** : Gratuit — Technologies web utilisées dans la démonstration de création de projet.
*   **Context7 (MCP)** : Gratuit / Payant (via clé API) — Serveur MCP fournissant la documentation à jour des bibliothèques aux modèles IA.
*   **Excalidraw** : Gratuit — Outil de schéma web utilisé dans la vidéo.
*   **`AI CLI` / `AI Blueprint` (`mlv.sh`)** : Gratuit — Ressource/newsletter de l'auteur pour configurer son environnement IA.

**3) Astuces concrètes et réutilisables**
*   **Installation globale** : Installer Codex via la commande `npm install -g @openai/codex`.
*   **Mode d'exécution automatique** : Lancer Codex avec `codex --yolo` pour exécuter les commandes sans demande de confirmation manuelle systématique.
*   **Fichier de mémoire projet (`AGENTS.md`)** : Générer ou créer un fichier `AGENTS.md` à la racine de vos projets (via la commande `/init`) pour y inscrire la stack technique, les préférences UI et les règles que l'IA doit toujours respecter.
*   **Intégration MCP (Context7)** : Ajouter le serveur Context7 dans `.codex/config.toml` pour permettre à Codex d'aller chercher la documentation la plus récente des librairies.
*   **Prompts personnalisés réutilisables** : Créer des fichiers `.md` dans le dossier `.codex/prompts/` (ex: `commit.md`, `search-docs.md`) utilisables comme des commandes slash (ex: `/promptcommit`).
*   **Raccourcis clavier Codex** : `Ctrl+J` pour sauter une ligne, `Ctrl+V` pour coller une image/capture d'écran, `Ctrl+T` pour afficher le transcript complet des échanges, `Échap + Échap` pour éditer les anciens messages.

**4) Chiffres de revenus annoncés**
*   non précisé (affirmé par l'auteur : aucun chiffre de revenu n'est cité).

---
