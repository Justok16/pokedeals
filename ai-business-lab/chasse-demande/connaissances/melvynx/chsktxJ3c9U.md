# 5 nouveautés Claude Code que peu de personnes connaissent…

Vidéo : https://youtu.be/chsktxJ3c9U · durée 17:26 · résumé Gemini (gemini-3-flash-preview, lot de 3) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Présentation des nouvelles fonctionnalités de **Claude Code CLI** pour les développeurs, notamment la gestion d'agents en arrière-plan, l'organisation de règles modulaires et le suivi précis de la consommation de jetons (tokens).

4) **Outils, sites ou dépôts GitHub cités** :
* **Claude Code CLI** : Outil en ligne de commande pour coder avec l'IA (payant via crédits API).
* **Codex** : Outil concurrent cité comme moins performant par l'auteur.
* **Vercel CLI** : Utilisé dans l'exemple pour surveiller les builds (payant/gratuit selon l'usage).
* **Proxyman** : Outil de débogage réseau utilisé pour analyser les requêtes de Claude (payant).
* **Dépôt GitHub "statuline"** : Projet de démonstration utilisé pour tester l'exploration de code.
* **mlv.sh/ai** : Site web proposant une masterclass gratuite et des fichiers de configuration pour Claude Code.

3) **Astuces concrètes et réutilisables** :
* **Utiliser des "Sub-agents"** : Lancer une tâche longue (ex: vérifier un build Vercel) en arrière-plan avec la commande `launch background agent` pour continuer à coder sur la session principale.
* **Gérer les règles par projet** : Créer un dossier `.claude/rules` avec des fichiers Markdown spécifiques (ex: `react.md`) pour donner des instructions de style ou de sécurité précises que l'IA lira automatiquement.
* **Optimiser le contexte** : Utiliser la commande `/compact` pour réduire la taille du contexte et économiser des tokens, bien que l'auteur note que cela reste parfois lent.
* **Renommer les sessions** : Utiliser le raccourci clavier `R` dans le menu `/resume` pour nommer ses conversations et les retrouver plus facilement.
* **Suivre les coûts** : Utiliser `/stats` pour visualiser la consommation de tokens des 30 derniers jours et comparer le coût par rapport à la taille d'un livre (ex: "22x plus de tokens que le Seigneur des Anneaux").

4) **Chiffres de revenus annoncés** : Non précisé. (L'auteur mentionne avoir dépensé environ **200 $** en API le mois dernier, mais aucun revenu n'est cité).
