# Prisma : La mise à jour qui CASSE tes nouveaux projets !

Vidéo : https://youtu.be/gKw_yJzV9-Y · durée 11:18 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Résolution d'un problème technique courant suite à la mise à jour de **Prisma ORM (v6.6.0)**, qui modifie la génération du client Prisma, et guide pour configurer correctement les chemins de sortie (`output`), **ESLint** et **Git** pour éviter les erreurs de compilation.
2) **Outils, sites ou dépôts GitHub cités :**
   - **Prisma ORM** : Gratuit (open-source), outil de gestion de base de données (version 6.6.0 présentée).
   - **Prisma Client** : Gratuit, bibliothèque générée pour interagir avec la base de données.
   - **Node.js / Node Modules** : Gratuit, environnement d'exécution JavaScript.
   - **ESLint** : Gratuit, outil d'analyse de code statique.
   - **Git** : Gratuit, système de contrôle de version.
   - **TypeScript** : Gratuit, sur-ensemble de JavaScript.
   - **npm / pnpm** : Gratuit, gestionnaires de paquets.
3) **Astuces concrètes et réutilisables :**
   - Depuis Prisma v6.6.0, ne plus laisser le client Prisma se générer par défaut dans `node_modules` (ce qui pose des problèmes de portabilité et de CI), mais définir un chemin d'export explicite dans le fichier `schema.prisma` (ex: `output = "./src/generated/prisma"`).
   - Configurer le fichier `prisma.config.ts` pour indiquer l'emplacement exact du schéma Prisma (`earlyAccess: true`, `schema: path.join(__dirname, "prisma/schema")`).
   - Exclure le dossier généré (`src/generated/prisma`) des fichiers analysés par **ESLint** (dans `eslint.config.mjs`) et des fichiers suivis par **Git** (dans `.gitignore`) pour garder un dépôt propre.
   - Mettre à jour globalement les imports dans le code de `@prisma/client` vers le nouveau chemin local d'export (`@/generated/prisma` ou chemin relatif équivalent) et relancer `pnpm prisma generate`.
4) **Chiffres de revenus annoncés :** Non précisé.
