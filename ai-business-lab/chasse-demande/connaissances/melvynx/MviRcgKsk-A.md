# TUTO / COURS : Comment utiliser Claude Code en tant que développeur

Vidéo : https://youtu.be/MviRcgKsk-A · durée 24:40 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Ce tutoriel présente **Claude Code**, un outil de développement d'Anthropic en mode terminal. L'auteur explique comment l'installer, le configurer (gestion des abonnements, de l'API pricing et des MCP serveurs), le comparer à Cursor, et l'utiliser avec des commandes et un fichier de configuration (`CLAUDE.md`) pour automatiser des tâches de programmation, gérer la mémoire du projet et déléguer du travail à des sous-agents.

2) **Outils, sites et dépôts GitHub cités** :
- **Claude Code** (développé par Anthropic) : Outil de ligne de commande (CLI) agissant comme un agent collaborateur pour la base de code. (Payant : abonnement mensuel ou tarification à l'API).
- **Cursor** : Éditeur de code concurrent basé sur l'IA (mentionné pour comparaison). (Modèle tarifaire non précisé).
- **ui.nowts.app** : Dépôt ou site de composants full-stack (utilisé comme projet de démonstration). (Gratuit ou non précisé).
- **Extension VS Code "Claude Code"** : Extension pour utiliser Claude Code directement dans l'interface de VS Code. (Gratuit).
- **CCSeva** : Petite application/outil (disponible sur GitHub) pour suivre et surveiller en temps réel l'utilisation de l'API Claude (dashboard de consommation de tokens et de coûts). (Gratuit/Open source).
- **mlv.sh/ai** : Site ou formation de l'auteur sur l'IA, Cursor et Claude. (Payant / Formation).

3) **Astuces concrètes et réutilisables** :
- Lancer la commande `npm install -g @anthropic-ai/claude-code` pour installer Claude Code globalement, puis utiliser `claude -v` pour vérifier l'accès.
- Utiliser la commande `*init` dans le terminal Claude Code pour analyser la base de code et générer automatiquement le fichier de documentation `CLAUDE.md`.
- Ajouter des balises de mémorisation dans `CLAUDE.md` avec `#` (par exemple, `# To memory: Always use descriptive variable names` ou des directives comme l'utilisation d'exports nommés) pour contraindre l'agent à respecter des conventions de code spécifiques.
- Configurer les permissions et les modes de fonctionnement (comme `acceptEdits`) dans le fichier `settings.json` ou `settings.local.json` pour automatiser l'application des modifications sans avoir à valider chaque action manuellement.
- Utiliser des serveurs MCP (`Context7`, etc.) pour permettre à Claude d'accéder à de la documentation externe et d'interagir avec des registres de composants.

4) **Chiffres de revenus annoncés** :
- **Affirmé par l'auteur** : Aucun chiffre de revenus n'est annoncé dans cette vidéo (seuls des coûts d'utilisation de l'API et des abonnements sont mentionnés, par exemple un abonnement à 20 $/mois ou un coût estimé de l'API pricing).

---
