# Comment deployer une App sur Vercel (NextJS + PostgresQL)

Vidéo : https://youtu.be/2yXb5lhGaC4 · durée 8:44 · résumé Gemini (gemini-flash-lite-latest, lot de 9) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur montre étape par étape comment déployer une application web Next.js connectée à une base de données PostgreSQL sur la plateforme Vercel, en gérant les pièges fréquents liés aux variables d'environnement, aux migrations de base de données Prisma et aux secrets GitHub/OAuth.
2) **Outils, sites ou dépôts GitHub cités :**
- **Next.js** (non précisé) : Framework React pour l'application web.
- **Vercel** (non précisé) : Plateforme d'hébergement et de déploiement cloud.
- **GitHub** (non précisé) : Hébergement du code source et authentification OAuth.
- **Prisma** (non précisé) : ORM pour gérer la base de données et les migrations.
- **Neon / neon.tech** (non précisé) : Service de base de données PostgreSQL serverless.
- **YouCode** (non précisé) : Plateforme de cours en ligne créée par l'auteur (lien en description).
3) **Astuces concrètes et réutilisables :**
- Pour déployer une application Next.js avec base de données sur Vercel, lier d'abord le dépôt GitHub, configurer les commandes de build (`prisma generate && prisma migrate deploy && next build`) et définir toutes les variables d'environnement nécessaires (`DATABASE_URL`, `NEXTAUTH_SECRET`, identifiants GitHub/Google).
- En cas d'erreur de migration Prisma lors du premier déploiement, reproduire l'environnement de production en local (`prisma migrate dev`) pour tester et valider les scripts de migration avant de les pousser en production.
- Utiliser **Neon** pour obtenir rapidement une URL de connexion PostgreSQL sécurisée et l'injecter dans les variables d'environnement de Vercel.
- Générer de nouveaux secrets sécurisés (par exemple pour `NEXTAUTH_SECRET` en utilisant `openssl rand -base64 32`) et mettre à jour les URLs de callback OAuth sur GitHub (en remplaçant `localhost` par l'URL de production fournie par Vercel).
- Activer l'option « *Use existing build cache* » sur Vercel pour accélérer les redéploiements successifs sans tout reconstruire à zéro.
4) **Chiffres de revenus annoncés :** Non précisé.
