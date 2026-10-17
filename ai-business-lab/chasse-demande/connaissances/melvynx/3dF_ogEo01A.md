# LIGHT.TS : La nouvelle boilerplate minimaliste pour ton SaaS

Vidéo : https://youtu.be/3dF_ogEo01A · durée 15:48 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. L'idée principale : La présentation d'une mise à jour majeure de la boilerplate « Now.ts » pour la création de SaaS, axée sur l'optimisation pour l'IA (notamment l'amélioration des fichiers de consignes comme `claude.md`), l'ajout de l'outil `autofix`, un panneau d'administration complet (Back-office B2C/B2B), une version allégée (`LIGHT.ts`) et un système d'adaptateurs simplifiés pour l'upload d'images et l'envoi d'emails.

2. Outils et sites cités :
- Now.ts : payant (boilerplate SaaS), base de code initiale pour lancer des projets.
- Prisma : gratuit, ORM de base de données.
- Stripe : payant (commission sur paiements), solution de paiement.
- Better-Auth : gratuit, bibliothèque d'authentification.
- SendGrid / Resend / AWS R2 / Cloudflare R2 : payants (services tiers), solutions d'envoi d'e-mails et de stockage d'images.
- Aiblueprint.dev (aiblueprint.dev/ai) : payant, plateforme proposant le blueprint et une formation masterclass sur Claude Code.

3. Astuces concrètes :
- Utiliser un fichier `claude.md` (ou `agents.md`) très structuré et complet à la racine du projet pour guider l'IA (avec des consignes d'autofix et de correction d'erreurs ESLint/TypeScript).
- Lancer la commande `autofix` avec Claude Code pour corriger automatiquement les erreurs de typage et de lintage sur plusieurs fichiers en parallèle.
- Configurer le fichier `package.json` avec un script `postinstall` pour automatiser la génération des types Prisma et des routes lors du déploiement.
- Utiliser le système d'adaptateurs modulaires de Now.ts pour basculer facilement entre différents services tiers (ex: passer d'un service d'e-mail à un autre sans réécrire la logique métier).
- Basculer vers la version `LIGHT.ts` de la boilerplate si l'on souhaite développer une application orientée B2C sans la complexité de la gestion des organisations multi-utilisateurs.

4. Chiffres de revenus : Non précisé.
