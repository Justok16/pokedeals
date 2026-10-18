# Tuto NextJS : Création d’une application de Scrapping de A à Z

Vidéo : https://youtu.be/pvg60ivrj-A · durée 52:44 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Créer une application Next.js de A à Z pour scraper des offres d'emploi (Remote Jobs) sur des sites de référence, en utilisant Prisma et Bright Data pour contourner les blocages.

2) **Outils, sites ou dépôts GitHub cités** :
- **Remote.co** / **We Work Remotely** (sites web de recherche d'emploi, source de scraping)
- **Prisma** (gratuit / open-source, ORM pour la base de données)
- **SQLite** (gratuit, base de données locale)
- **Bright Data** (payant / freemium avec essai, sponsor de la vidéo, infrastructure de proxies et scraping browser pour éviter les captchas et blocages IP)
- **Shadcn UI** (gratuit, bibliothèque de composants UI)
- **Playwright** (gratuit, outil d'automatisation de navigateur utilisé avec Bright Data)

3) **Astuces concrètes et réutilisables** :
- Lancer un projet Next.js avec `npx create-next-app@latest`.
- Initialiser Prisma avec `npx prisma init --datasource-provider sqlite` et configurer le schéma de données dans `schema.prisma`.
- Utiliser `npx prisma migrate dev --name initial_migration` pour synchroniser la base de données.
- Utiliser `@prisma/client` pour interroger la base de données depuis les routes API ou composants Next.js.
- Configurer un proxy distant (via Bright Data et Playwright) pour se connecter à un navigateur distant et éviter les bannissements d'IP lors du scraping.
- Stocker les données récupérées dans la base SQLite via Prisma et les afficher dynamiquement dans l'interface utilisateur.
- Configurer une tâche automatique (cron job sur Vercel) pour exécuter le scraping quotidiennement.

4) **Chiffres de revenus** : Non précisé.

---
