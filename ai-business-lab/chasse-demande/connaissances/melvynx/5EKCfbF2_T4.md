# Nuxt est-il meilleur que NextJS ? (test par un dev NextJS)

Vidéo : https://youtu.be/5EKCfbF2_T4 · durée 35:56 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Découverte et test en direct de **Nuxt 3** (framework web) et de ses modules associés, notamment la configuration, le routing, la gestion des assets et l'intégration avec **Prisma** et **Tailwind CSS**.
2) **Outils, sites ou dépôts GitHub cités :**
   - **Nuxt 3** : Gratuit (open-source), framework web full-stack basé sur Vue.js, Vite et Nitro.
   - **Vite** : Gratuit, bundler et serveur de développement.
   - **Nitro** : Gratuit, serveur pour déployer l'application partout.
   - **Visual Studio Code** : Gratuit, éditeur de code recommandé.
   - **Vue / Vue Official / Volar** : Gratuit, extension pour le support de Vue.
   - **Tailwind CSS** : Gratuit (via Nuxt UI), bibliothèque de classes CSS.
   - **Prisma** : Gratuit (ORM open-source), gestion de base de données.
   - **Prisma Studio** : Gratuit, interface graphique pour gérer la base de données SQLite/Prisma.
3) **Astuces concrètes et réutilisables :**
   - Initialiser un projet Nuxt via la commande `npx nuxi@latest init <nom-du-projet>` en choisissant son gestionnaire de paquets (npm, pnpm, yarn, bun).
   - Utiliser les dossiers par défaut (`pages/`, `components/`, `server/`, `layouts/`, `assets/`) pour un auto-import automatique des composants et des routes sans configuration manuelle lourde.
   - Activer le mode dev (`npm run dev` / `pnpm dev`) pour lancer le serveur local et profiter du "Dev Tools" intégré (via `Shift + Option + D`).
   - Gérer la base de données avec Prisma en configurant le fichier `schema.prisma`, en lançant `npx prisma generate`, puis `npx prisma db push` pour synchroniser le schéma avec SQLite.
4) **Chiffres de revenus annoncés :** Non précisé.
