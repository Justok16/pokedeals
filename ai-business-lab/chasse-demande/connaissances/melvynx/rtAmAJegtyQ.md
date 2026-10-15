# Je fais du TDD sans aucun Tests...

Vidéo : https://youtu.be/rtAmAJegtyQ · durée 10:48 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Démonsration des avantages du développement piloté par les types (TypeScript-driven development / TDD appliqué à TypeScript) pour garantir la robustesse du code, faciliter les refactorings massifs et éliminer les tests unitaires superflus.

2) **Outils, sites ou dépôts GitHub cités** :
- **TypeScript** : langage de programmation typé basé sur JavaScript. Gratuit (open source).
- **Zod** : bibliothèque de validation de schémas TypeScript. Gratuit (open source).
- **VS Code** : éditeur de code source. Gratuit.
- **Prisma** : ORM TypeScript. Gratuit (open source).

3) **Astuces concrètes et réutilisables** :
- Définir des types et des schémas stricts (avec TypeScript et Zod) pour s'assurer que toute modification de structure (comme renommer un paramètre ou un rôle dans une base de données) est immédiatement signalée par le compilateur dans l'ensemble du code.
- Utiliser le compilateur TypeScript (`tsc --noEmit`) pour vérifier l'absence d'erreurs de typage avant le déploiement, réduisant le besoin d'écrire de nombreux tests unitaires.
- S'appuyer sur l'inférence de types pour valider automatiquement les données entrantes (via les schémas Zod) et sécuriser les actions serveur.

4) **Chiffres de revenus annoncés ("affirmé par l'auteur")** :
- Non précisé.
