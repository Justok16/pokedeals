# Setup d'un SaaS avec NextJS 15 / Prisma / NextAuth en 20 minutes

Vidéo : https://youtu.be/5l7ZRXOecbA · durée 27:27 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** 
Ce tutoriel montre pas à pas comment set-up un projet Next.js avec Tailwind, Shadcn/UI, Next-Auth (authentification par e-mail et GitHub), et Prisma (avec PostgreSQL), en créant une structure propre et modulaire, ainsi que des pages d'authentification personnalisées (protégées par des règles d'accès).

2. **Outils, sites et dépôts GitHub cités :**
- **Shadcn/UI** (Site : `ui.shadcn.com` / Gratuit) : Bibliothèque de composants prêts à l'emploi.
- **Next.js** (Site/Framework / Gratuit) : Framework React utilisé pour l'application.
- **PNPM** (Outil de gestion de paquets / Gratuit) : Utilisé pour installer les packages.
- **VS Code** (IDE / Gratuit) : Éditeur de code.
- **Lucide React** (Bibliothèque d'icônes / Gratuit) : Utilisée pour les icônes (fournie avec Shadcn).
- **Prisma** (Site : `prisma.io` / Gratuit) : ORM pour interagir avec la base de données.
- **PostgreSQL** (Base de données / Gratuit) : Utilisée comme SGBD local.
- **Auth.js / Next-Auth** (Site : `auth.js.dev` / Gratuit) : Solution d'authentification pour Next.js.
- **Resend** (Site : `resend.com` / Modèle freemium) : Service d'e-mailing utilisé pour l'authentification par e-mail magique.
- **NOW.TS** (Site : `mlv.sh/nextjs` / Payant - Cours de l'auteur) : Boilerplate et formation payante proposée par l'auteur pour les développeurs.
- **GitHub** (Site : `github.com` / Gratuit) : Utilisé comme fournisseur d'authentification OAuth.

3. **Astuces concrètes et réutilisables :**
- Organiser le code en plaçant le dossier `components` dans un dossier `src` et en modifiant la configuration `tsconfig.json` (`paths` avec `src/*`) pour éviter d'encombrer la racine du projet.
- Utiliser `next-themes` avec Shadcn pour gérer un mode sombre (dark mode) propre et réactif avec un composant de bascule (toggle).
- Structurer l'authentification avec Next-Auth en utilisant un adaptateur Prisma (`@auth/prisma-adapter`) pour stocker les sessions et utilisateurs directement en base de données.
- Sécuriser les routes et pages (ex: page `/private`) en utilisant les fonctions de vérification de session (`auth()` ou `requiredAuth()`) pour rediriger automatiquement les utilisateurs non connectés vers la page de connexion.
- Ajouter des composants UI comme le `Toaster` (Sonner) globalement dans le layout pour gérer les notifications visuelles.

4. **Chiffres de revenus annoncés :**
- Non précisé.

---
