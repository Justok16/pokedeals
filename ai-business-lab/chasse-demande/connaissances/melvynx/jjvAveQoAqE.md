# Claude Code : cette update change TOUT pour les devs

Vidéo : https://youtu.be/jjvAveQoAqE · durée 23:53 · résumé Gemini (gemini-3.5-flash-lite, lot de 6) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : La vidéo présente les dernières mises à jour majeures de **Claude Code**, notamment l'introduction des **Tasks** (système de gestion de tâches et de sous-agents autonomes), l'amélioration du **Tool Search** (recherche dynamique de MCP pour économiser les tokens), et la fusion des commandes Slash avec les Skills.

2) **Outils, sites et dépôts GitHub cités** :
- **Claude Code** : Outil payant (via abonnement/API Anthropic), assistant de développement en ligne de commande.
- **MCP (Model Context Protocol)** : Standard gratuit et open source pour connecter des outils et bases de données aux LLM.
- **Tool Search** : Fonctionnalité intégrée à Claude Code pour charger dynamiquement les MCP à la demande.
- **Tasks (Claude Code Tasks)** : Nouvelle primitive native de Claude Code pour traquer, planifier et exécuter des tâches complexes en parallèle.
- **Subagents** : Agents secondaires lancés par Claude Code pour exécuter des sous-tâches de manière isolée.
- **Exa (Exa Web Search)** : Moteur de recherche web optimisé pour les LLM (utilisé comme MCP de recherche).

3) **Astuces concrètes et réutilisables** :
- Activer le mode `tool search` (`enable_tool_search: true` dans les settings) pour éviter de charger en permanence tous les MCP dans le contexte, ce qui permet d'économiser considérablement la consommation de tokens.
- Utiliser le système de **Tasks** (`/tasks`) pour demander à Claude de décomposer un projet en plusieurs étapes, de créer une liste de tâches (`task list`), et de faire travailler plusieurs agents en parallèle sur des fichiers différents.
- Désactiver les MCP inutiles dans le fichier de configuration `settings.json` lorsque leur empreinte contextuelle dépasse 2 à 3 % du total des tokens.
- Combiner les Skills et les commandes Slash pour un meilleur routage des instructions contextuelles.

4) **Chiffres de revenus annoncés** :
- Non précisé.
