# Tu dois (encore) tout changer dans ton code NextJS 15

Vidéo : https://youtu.be/LYYRKZ8omEs · durée 13:12 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Analyse des nouveautés de la Release Candidate 2 (RC2) de Next.js 15, incluant l'amélioration des codemods, l'état de TurboPack en production, les modifications sur les Server Actions (sécurité/leak) et les indicateurs de routes statiques.

2) **Outils, sites ou dépôts GitHub cités** :
- **Next.js 15 (RC2)** : framework React. Gratuit (open source).
- **Codemod CLI** (`npx @next/codemod@canary upgrade`) : outil en ligne de commande pour automatiser la mise à jour du code et des dépendances. Gratuit.
- **TurboPack** : bundler pour le développement Next.js. Gratuit (open source).
- **ESLint 9** : outil de linting du code (avec support de la version 9 et de la nouvelle configuration plate). Gratuit (open source).
- **OpenTelemetry** : bibliothèque d'observabilité intégrée dans Next.js via `instrumentation.js`. Gratuit (open source).

3) **Astuces concrètes et réutilisables** :
- Utiliser la commande `npx @next/codemod@canary upgrade` pour automatiser la migration du code lors du passage à Next.js 15 et adapter les types automatiquement.
- Sécuriser les Server Actions en ajoutant explicitement la directive `'use server';` et en faisant attention à ne pas exposer par inadvertance des fonctions sensibles côté client (problème de leak résolu dans cette version).
- Exploiter le fichier `instrumentation.js` (stable en 15) pour capturer les erreurs serveur, les contextes de requêtes et intégrer des outils de monitoring comme Sentry.
- Configurer l'indicateur de route statique pour identifier facilement les pages statiques par rapport aux pages dynamiques pendant le développement.

4) **Chiffres de revenus annoncés ("affirmé par l'auteur")** :
- Non précisé.
