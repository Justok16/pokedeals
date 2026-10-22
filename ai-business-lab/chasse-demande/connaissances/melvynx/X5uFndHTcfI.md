# Je peux pas croire que Claude Code est aussi bien (mon workflow complet)

Vidéo : https://youtu.be/X5uFndHTcfI · durée 20:58 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de comparer l'utilisation de deux assistants de code par IA (Cursor et Claude Code) pour montrer pourquoi Claude Code est jugé supérieur, notamment grâce à son fonctionnement natif dans le terminal, sa capacité à automatiser des tâches complexes via des scripts shell (worktrees) et son modèle de tarification à l'usage par jetons.

2) Outils, sites et dépôts cités :
- Cursor : IDE basé sur VS Code (gratuit ou plan Pro à 20 $/mois incluant 20 $ de requêtes d'agent). Sert d'éditeur de code assisté par IA.
- Claude Code : Outil CLI en terminal (gratuit d'utilisation de base, mais consommant des tokens facturés via l'API Anthropic ou l'abonnement Claude Pro à 20 $/mois). Sert d'agent de développement autonome en ligne de commande.
- GitHub CLI (gh) : Outil en ligne de commande (gratuit) pour interagir avec les issues et pull requests GitHub.
- Node.js / npm : Environnement d'exécution (gratuit) pour installer et lancer les outils.
- pnpm : Gestionnaire de paquets (gratuit).

3) Astuces concrètes et réutilisables :
- Utiliser un script bash de configuration de "git worktrees" (`setup-worktree.sh`) combiné avec Claude Code pour créer automatiquement une branche dédiée à une issue GitHub, copier l'environnement, lancer l'installation et exécuter les tests de manière isolée.
- Automatiser la résolution d'issues en passant l'URL d'une issue GitHub directement à Claude Code en mode "plan" puis "autopilot/run-task".
- Configurer des commandes de tâches récurrentes (`run-tasks.md`) pour guider l'IA étape par étape (création de code, tests, commit, pull request).
- Gérer les coûts des API en surveillant la consommation de tokens et en comparant les limites d'utilisation (rate limits) entre Cursor et les requêtes directes à l'API Claude.

4) Chiffres de revenus annoncés (affirmés par l'auteur) :
- Non précisé.
