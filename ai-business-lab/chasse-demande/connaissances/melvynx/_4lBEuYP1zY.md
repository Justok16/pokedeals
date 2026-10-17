# Teste de SvelteKit pour la première fois ! (par un dev NextJS)

Vidéo : https://youtu.be/_4lBEuYP1zY · durée 36:31 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** :
   Présentation de la création d'un projet avec **SvelteKit** combiné à **Prisma** et l'utilisation de **Claude Code** (ou de l'approche agentique avec des assistants IA) pour développer une application de type *to-do list*, avec les avantages et les difficultés rencontrées en cours de route.

2) **Outils, sites et dépôts GitHub cités** :
   - **Svelte / SvelteKit** : Gratuit — Framework de développement web (alternative à React/Next.js/Nuxt).
   - **npm trends** (npmtrends.com) : Gratuit — Site pour comparer la popularité de paquets npm (SvelteKit vs Next.js).
   - **Prisma** (prisma.io) : Gratuit (ou offre payante) — ORM / outil de gestion de base de données.
   - **SQLite** : Gratuit — Moteur de base de données relationnelle léger.
   - **TypeScript** : Gratuit — Superset typé de JavaScript.
   - **Tailwind CSS** : Gratuit — Framework CSS utilitaire.
   - **Prettier** / **ESLint** / **Playwright** : Gratuit — Outils de formatage, lintage et test.
   - **Lucia** : Gratuit — Bibliothèque pour l'authentification.
   - **Zod** : Gratuit — Bibliothèque de validation de schémas.
   - **Zepto** (api.ipify.org / placeholder.typicode.com / zep.io mentionnés) : Gratuit/API — Services et exemples d'API.
   - **Cursor** : Gratuit/Payant — Éditeur de code/IDE dopé à l'IA.

3) **Astuces concrètes et réutilisables** :
   - Initialiser un projet SvelteKit avec la CLI : `npx sv create <nom-du-projet>` (en choisissant la bibliothèque minimale, TypeScript, etc.).
   - Installer l'extension VS Code dédiée pour Svelte (`Svelte language support for VS Code`) pour l'analyse du code.
   - Structurer les routes dans le dossier `src/routes/` avec `+page.svelte`, `+page.ts`/`+page.server.ts` pour gérer le rendu côté serveur et les actions (*Form actions*).
   - Gérer le routage dynamique et la récupération de données via les fonctions `load` et les actions de formulaire (`actions` dans `+page.server.ts`).
   - Configurer Prisma avec SQLite, générer le client Prisma (`npx prisma generate`) et initialiser les migrations (`npx prisma migrate dev`).

4) **Chiffres de revenus** :
   - Non précisé.

---
