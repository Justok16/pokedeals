# 9 SECRETS Claude Code qui rendent les développeurs 10x plus rapides

Vidéo : https://youtu.be/Zd9eqVjcBw4 · durée 26:06 · résumé Gemini (gemini-flash-lite-latest, lot de 3) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale** : Présentation de 9 astuces et bonnes pratiques pour optimiser l'utilisation de **Claude Code** (raccourcis SSH, hooks audio, modes de sécurité, prompt de flux EPCT, utilisation de tests, évitement des MCP au profit de Bash CLI, changement de modèle, suivi d'utilisation, et utilisation partout).
2. **Outils, sites ou dépôts GitHub cités** : 
   - **Claude Code** (payant / abonnement, outil principal de génération de code en CLI).
   - **Excalidraw** / `app.excalidraw.com` (gratuit/freemium, outil de schématisation/whiteboard).
   - **Neon CLI** (gratuit open-source, CLI pour base de données Neon).
   - **Vercel CLI** (gratuit open-source, CLI pour le déploiement Vercel).
   - **GitHub CLI (`gh`)** (gratuit open-source, CLI pour GitHub).
3. **Astuces concrètes et réutilisables** : 
   - Utiliser des alias SSH (`cc` pour `--dangerously-skip-permissions` et `ccc` avec `-c` pour continuer la conversation).
   - Configurer des "hooks" de fin de tâche (`Stop`) avec `afplay` pour jouer un son MP3 (`finish.mp3` ou `need-human.mp3`) afin de ne pas perdre de temps.
   - Sécuriser le mode "YOLO" avec un script `validate-command.js` (PreToolUse hook) pour bloquer les commandes dangereuses (`rm -rf`).
   - Utiliser le prompt standardisé **EPCT** (Explore, Plan, Code, Test) dans les worktrees.
   - Lancer systématiquement des tests pour permettre à l'IA de s'auto-corriger.
   - Préférer l'utilisation des **Bash CLI** directs plutôt que des MCP (Model Context Protocols) qui alourdissent et ralentissent l'outil.
   - Basculer sur un modèle plus puissant (comme Opus) en cas de bug persistant avec un prompt de type "deep search".
   - Surveiller sa consommation de tokens en temps réel via la commande `ccusage` (`ccusage -live`).
   - Utiliser `claude.md` (à différents niveaux : projet, personnel, machine) pour donner du contexte permanent à l'IA.
4. **Chiffres de revenus annoncés** : 
   - Non précisé (seuls des coûts d'utilisation en tokens sont mentionnés, ex. ~$8 à ~$66 de consommation par session/jour).
