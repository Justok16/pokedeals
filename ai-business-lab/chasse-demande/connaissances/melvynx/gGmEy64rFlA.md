# Les mods de Claude Code

Vidéo : https://youtu.be/gGmEy64rFlA · durée 0:36 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale**
Présentation des **mods** (nouvelle fonctionnalité de **Claude Code** permettant de customiser l'application avec des scripts et des affichages spécifiques) et de l'utilisation avancée des **MCP (Model Context Protocols)** et des **agents**.

2) **Outils, sites ou dépôts GitHub cités**
* **Claude Code** : Éditeur/assistant IA en ligne de commande d'Anthropic.
* **Mod AI Blueprint** : Mod personnalisé pour afficher les tokens consommés, les limites de temps (5h, semaine) et le pourcentage d'utilisation.
* **Mod Crash** : Mod pour supprimer les erreurs de type RMRF et forcer une commande plus sécurisée (comme `trash`).
* **Mod Record** : Mod pour lancer des enregistrements vidéo (`/record`) en masquant les API keys et secrets.
* **GitHub CLI (`gh`)** : Outil en ligne de commande pour interagir avec GitHub.
* **Context7 (context7.com)** : Service MCP pour récupérer de la documentation technique sans passer par Internet.

3) **Astuces concrètes et réutilisables**
* Créer ou installer des **mods** pour Claude Code afin d'afficher des métriques de consommation de tokens en temps réel dans le terminal.
* Utiliser des commandes personnalisées comme `/record` pour cacher les données sensibles lors d'enregistrements d'écran.
* Configurer des **agents** spécialisés (via le dossier `.claude/agents`) pour automatiser des tâches complexes (comme l'exploration de code avec `explore-code`, l'analyse de bugs ou la rédaction de documentations).
* Remplacer les MCP lourds par des **CLIs** (comme GitHub CLI) pour éviter de saturer le contexte en tokens tout en gardant l'accès aux fonctionnalités nécessaires.
* Utiliser **Context7** comme serveur MCP pour injecter de la documentation de librairies directement dans le contexte de l'IA.
* Utiliser la commande `/clear` ou `/init` pour réinitialiser le contexte ou configurer un fichier `CLAUDE.md` qui sert de mémoire permanente à l'IA pour tout le projet.

4) **Chiffres de revenus annoncés (affirmés par l'auteur)**
* Non précisé
