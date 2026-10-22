# TUTO NextAuth avec NextJS 14 + Prisma - Guide De A à Z2024

Vidéo : https://youtu.be/LaMoteg626I · durée 48:56 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur propose un tutoriel complet pour configurer l'authentification dans une application Next.js (13/14/15/16) en combinant **NextAuth (Auth.js)**, **Prisma** (comme adaptateur de base de données) et plusieurs fournisseurs (GitHub, Google, liens magiques par email, SMTP).

2) **Outils, sites ou dépôts GitHub cités :**
- **NextAuth (Auth.js) :** Gratuit (open-source), bibliothèque d'authentification pour Next.js.
- **GitHub OAuth Provider :** Gratuit, fournisseur d'authentification via GitHub.
- **Google OAuth Provider :** Gratuit, fournisseur d'authentification via Google.
- **Email Provider / Magic Link :** Gratuit, méthode d'authentification par lien magique envoyé par email.
- **HTTP-based Email Provider (Resend, SendGrid, etc.) :** Modèle freemium/payant, service d'envoi d'emails transactionnels via HTTP/SMTP.
- **Prisma :** Gratuit (open-source), ORM pour la gestion de bases de données.
- **Prisma Adapter (pour NextAuth) :** Gratuit, adaptateur pour persister les sessions et utilisateurs NextAuth dans une base SQL via Prisma.
- **SQLite / PostgreSQL / MySQL :** Gratuit/Payant selon l'hébergement, systèmes de bases de données.
- **DaisyUI / Tailwind CSS :** Gratuit, bibliothèques de composants et styles CSS.
- **Prisma Studio :** Gratuit, interface visuelle pour explorer la base de données Prisma.
- **Resend (resend.com) :** Freemium/Payant, service d'envoi d'emails (utilisé pour les liens magiques).

3) **Astuces concrètes et réutilisables :**
- Structurer l'authentification NextAuth dans un fichier de configuration séparé (`auth.ts` ou `safe-actions.ts`) avec `NextAuthConfig`.
- Utiliser Prisma avec un adaptateur (`@auth/prisma-adapter`) pour stocker automatiquement les utilisateurs, comptes et sessions en base de données.
- Configurer les variables d'environnement (`.env`) pour stocker les secrets OAuth (GitHub, Google) et les clés API d'envoi d'emails.
- Étendre les types TypeScript de session (`next-auth.d.ts`) pour y intégrer l'ID utilisateur et éviter les erreurs de typage lors des requêtes serveur.

4) **Chiffres de revenus annoncés :**
- Non précisé.

---
