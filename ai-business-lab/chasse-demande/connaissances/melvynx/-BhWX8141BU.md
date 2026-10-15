# Le nouveau "use cache" de NextJS 15 expliqué

Vidéo : https://youtu.be/-BhWX8141BU · durée 10:58 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Présentation du nouveau système de mise en cache natif de Next.js 15, le « Use Cache », qui permet de mettre en cache de manière dynamique et précise des composants ou des données sans recharger toute l'application.

2) **Outils, sites ou dépôts GitHub cités** :
- **Next.js 15 (Canary)** : framework React (version 15.0.2-canary ou supérieure). Gratuit (open source).
- **Prisma** : ORM pour la gestion de base de données (utilisé pour les exemples de code). Gratuit (open source).

3) **Astuces concrètes et réutilisables** :
- Activer la gestion dynamique du cache en configurant `experimental: { dynamicIO: true }` dans le fichier `next.config.ts`.
- Utiliser la directive `'use cache';` au début d'un fichier ou d'une fonction pour mettre en cache le résultat d'un composant ou d'une requête de données.
- Utiliser `cacheTag()` et `revalidateTag()` pour purger sélectivement le cache d'un composant spécifique lors d'une mutation (ex. : suppression ou ajout d'une citation), évitant ainsi de tout revalider.
- Gérer la durée de vie du cache avec `cacheLife()` en définissant des profils personnalisés (minutes, heures, jours).

4) **Chiffres de revenus annoncés ("affirmé par l'auteur")** :
- Non précisé.
