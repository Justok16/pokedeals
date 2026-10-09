# Ce Plugin RALPH rend Claude Code 100x plus puissant

Vidéo : https://youtu.be/BJEihtJ4Efw · durée 23:57 · résumé Gemini (gemini-3.5-flash-lite, lot de 8) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Présentation et démonstration de l'outil « Ralph Wiggum » (ou Workflow Ralph), un agent IA autonome en boucle (basé sur des PRD - Product Required Documents, user stories et scripts bash) qui s'exécute de manière répétée pour implémenter des fonctionnalités de bout en bout, commiter le code, gérer les tests et mettre à jour sa progression sans intervention humaine.

2) **Outils, sites ou dépôts GitHub cités** :
- **Ralph Wiggum (ou Ralph)** : Workflow d'agent IA autonome (gratuit / open-source, basé sur des scripts).
- **Claude / Anthropic** : Modèle d'IA utilisé pour propulser l'agent (payant/abonnement).
- **Claude Code** : Outil CLI (inclus dans l'abonnement).
- **GitHub** : Plateforme de gestion de code (gratuit/payant).
- **Playwright** : Outil de test (gratuit).
- **MLV.sh/FC** : Lien de l'auteur pour accéder à sa configuration et ses scripts (non précisé).

3) **Astuces concrètes et réutilisables** :
- Rédiger un document PRD détaillé (`prd.json`) avec des user stories découpées en tâches précises, des priorités et des critères d'acceptation.
- Créer un fichier de suivi de progression (`progress.txt`) pour que l'agent IA sache où il en est d'une itération à l'autre.
- Utiliser un script bash de boucle (`ralph.sh`) combiné avec des commandes de test (ex: CI fixer, Playwright) pour forcer l'IA à coder, tester, corriger et commiter en boucle jusqu'à ce que toutes les stories soient validées (*promises complete*).

4) **Chiffres de revenus annoncés** :
- *Affirmé par l'auteur* : Non précisé.

---
