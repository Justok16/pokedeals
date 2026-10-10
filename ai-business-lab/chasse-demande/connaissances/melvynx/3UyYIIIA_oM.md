# Voici la SEUL chose que j'ai repris de Bmad (les skills workflows = le futur).

Vidéo : https://youtu.be/3UyYIIIA_oM · durée 26:19 · résumé Gemini (gemini-3.5-flash-lite, lot de 6) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : L'auteur présente un nouveau workflow de commandes pour **Claude Code** (basé sur l'outil **Apex** et des prompts structurés en plusieurs étapes) qu'il a conçu pour automatiser la création d'un SaaS complet en seulement deux jours, en guidant l'IA pas à pas de l'analyse jusqu'à la validation et la correction de bugs.

2) **Outils, sites et dépôts GitHub cités** :
- **Claude Code** : Outil payant (via abonnement/API), assistant de code en ligne de commande.
- **Apex (Apex.md)** : Outil de workflow pour agents IA permettant de structurer des tâches complexes en plusieurs étapes séquentielles.
- **Escalidraw** : Outil de dessin/schématisation (utilisé pour illustrer le fonctionnement du workflow).
- **ElevenLabs** : Outil payant (génération de voix off / synthèse vocale).

3) **Astuces concrètes et réutilisables** :
- Structurer les prompts de développement en plusieurs étapes méthodologiques strictes : Initialisation, Analyse, Planification, Exécution, Validation/Tests, Examen (Code Review), et Résolution.
- Utiliser le mode économique (`--auto` ou configuration équivalente) pour limiter la consommation excessive de tokens tout en automatisant les boucles de correction.
- Lancer des sous-agents (subagents) spécialisés pour vérifier la sécurité, valider les types TypeScript, et lancer les tests unitaires avant de commiter le code.
- Configurer des "skills" et des scripts de test automatisés pour que l'IA puisse auto-corriger ses erreurs de code de manière autonome.

4) **Chiffres de revenus annoncés** :
- Non précisé.
