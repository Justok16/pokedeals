# Maîtriser Claude Code en 1 heure | Formation complète en 2025

Vidéo : https://youtu.be/hkbVuhRSkGY · durée 52:05 · résumé Gemini (gemini-flash-lite-latest, lot de 3) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale** : Guide complet (masterclass) sur le fonctionnement, la configuration, la tarification et l'utilisation avancée de **Claude Code** comparé à d'autres agents, en mettant l'accent sur le contexte, les commandes personnalisées, les modes de fonctionnement et l'intégration MCP.
2. **Outils, sites ou dépôts GitHub cités** : 
   - **Claude Code** (payant, outil CLI d'Anthropic).
   - **Cursor** / **Windsurf** / **Codex** (outils de code alternatifs mentionnés).
   - **Excalidraw** (outil de schéma).
   - **Anthropic.com / Claude.ai** (site officiel pour l'abonnement et la doc).
   - **GitHub / `ibluetooth.dev`** (ressource/plateforme mentionnée pour des templates ou formations, ex: `iblueprint.dev`).
3. **Astuces concrètes et réutilisables** : 
   - Comprendre le rôle d'intermédiaire de Claude Code entre l'utilisateur et l'API (lecture/écriture de fichiers via des outils précis comme `ReadFile` et `EditFile`).
   - Gérer le contexte avec soin : utiliser la commande `/init` pour scanner le code et générer un résumé initial, et créer des fichiers `claude.md` (aux niveaux Projet, Personnel ou Machine) pour structurer les règles et instructions persistantes.
   - Utiliser les commandes en mode slash (`/clear`, `/compact`, `/init`, `/resume`) pour gérer l'historique et la taille du contexte.
   - Créer des prompts et des commandes personnalisées dans les dossiers `claud/commands` (au niveau projet ou global).
   - Intégrer des serveurs MCP (Model Context Protocol) comme `sequential-thinking` via `claude mcp add` pour améliorer les capacités de raisonnement de l'IA.
   - Configurer les "Hooks" (`PreToolUse`, `PostToolUse`, `Stop`, `Notification`) dans les paramètres (`settings.json`) pour automatiser des vérifications (ex: linter, tests, sons de fin).
   - Utiliser les raccourcis clavier dans le terminal : `ESC + ESC` pour retourner dans un ancien message, `#` pour ajouter de la mémoire, ou passer en mode Bash direct (`!`).
4. **Chiffres de revenus annoncés** : 
   - Non précisé (les montants mentionnés correspondent à des coûts d'abonnement ou de consommation d'API, par exemple l'abonnement Pro à 17 $/mois, Max 5x à 100 $/mois, Max 20x à 200 $/mois, et des coûts d'utilisation en tokens atteignant parfois 60 $ à 261 $ par période d'utilisation intensive, **affirmé par l'auteur**).
