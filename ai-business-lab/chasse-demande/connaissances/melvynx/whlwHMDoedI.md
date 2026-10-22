# Sonnet 4.6 contre Opus 4.6 : es-il aussi puissant ?

Vidéo : https://youtu.be/whlwHMDoedI · durée 45:45 · résumé Gemini (gemini-3-flash-preview, lot de 7) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Test intensif des capacités de Claude Sonnet 4.6 sur des tâches de programmation de haut niveau, notamment l'intégration d'un système d'affiliation complexe dans une application existante.

2) **Outils, sites ou dépôts cités** :
*   **Claude Sonnet 4.6 (Anthropic)** : Payant (via API). Nouveau modèle testé, doté d'une fenêtre de contexte de 1 million de tokens.
*   **Codex 5.3 (OpenAI)** : Payant. Modèle concurrent utilisé pour comparer la logique de programmation.
*   **Thumbfa.st** : L'application de l'auteur servant de base aux tests.
*   **code.melvinx.dev** : Gratuit. Site de ressources et de prompts de l'auteur.
*   **Prisma** : Gratuit. ORM utilisé pour la gestion de la base de données dans le code.

3) **Astuces concrètes et réutilisables** :
*   Utiliser la commande `/model` dans l'interface CLI de Claude Code pour basculer rapidement entre les modèles (Opus, Sonnet, Haiku) selon la complexité de la tâche et le budget.
*   Pour des fonctionnalités logiques très imbriquées (comme la gestion des cookies d'affiliation), Sonnet 4.6 peut être moins performant que Codex ; il est conseillé de vérifier les liaisons de base de données générées, car l'IA peut oublier les relations complexes.

4) **Chiffres de revenus annoncés** : Aucun (« non précisé »).
