# TUTO / Cours Prisma en 40 minutes : TOUT savoir sur Prisma avec NextJS

Vidéo : https://youtu.be/7L0U-j-SZjM · durée 44:07 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale** : Formation complète sur l'utilisation de Prisma ORM avec JavaScript et Next.js, expliquant son fonctionnement, ses avantages par rapport au SQL brut et aux autres ORM, ainsi que la gestion des migrations de base de données.

2. **Outils, sites ou dépôts GitHub cités** :
   - **Prisma** : ORM (Object-Relational Mapping), gratuit (open-source avec services payants optionnels). Sert à transformer le code JavaScript/TypeScript en requêtes SQL de manière intuitive.
   - **Next.js** : Framework web, gratuit. Utilisé comme exemple d'application dans la formation.
   - **Prisma Studio** : Éditeur visuel de base de données fourni avec Prisma, gratuit.
   - **SQLite**, **MongoDB**, **PostgreSQL** : Systèmes de gestion de base de données compatibles avec Prisma.
   - **BetterAuth** : Outil d'authentification mentionné dans le plan de formation complet (`mlv.sh/fullstack`).
   - **Zustand** : Gestionnaire d'état mentionné dans la formation complète.
   - **Tanstack Query** : Bibliothèque de gestion de requêtes asynchrones mentionnée dans la formation.

3. **Astuces concrètes et réutilisables** :
   - Utiliser le fichier de schéma Prisma (`schema.prisma`) pour définir les modèles de données indépendamment de la base de données utilisée.
   - Lancer les migrations avec `prisma migrate dev` pour synchroniser le schéma avec la base de données sans perdre de données existantes.
   - Utiliser `prisma.post.findMany()` avec des filtres, des tris (`orderBy`) et des limites (`take`) pour interroger la base de données de manière sécurisée (type-safe).
   - Utiliser `prisma.post.upsert()` pour créer ou mettre à jour un enregistrement en une seule opération.
   - Utiliser `satisfies` en TypeScript avec les types de retour Prisma pour conserver l'autocomplétion tout en typant les données.

4. **Chiffres de revenus annoncés** :
   - Non précisé.

---
