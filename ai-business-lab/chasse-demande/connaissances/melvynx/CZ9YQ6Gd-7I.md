# Je teste Better-Auth pour la première fois (je suis choqué)

Vidéo : https://youtu.be/CZ9YQ6Gd-7I · durée 22:18 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale** : Présentation et démonstration de Better Auth, une alternative open-source à NextAuth, axée sur l'authentification complète pour TypeScript avec un système de plugins modulaires.

2. **Outils, sites ou dépôts GitHub cités** :
   - **Better Auth** : Framework d'authentification pour TypeScript, gratuit (open-source). Sert à gérer l'authentification (email/mot de passe, OAuth, 2FA, etc.).
   - **Next.js** / **Next.js JS** : Framework web, gratuit.
   - **Prisma** : ORM, gratuit. Utilisé comme adaptateur de base de données.
   - **PostgreSQL** : Base de données relationnelle.
   - **Resend** : Service d'envoi d'e-mails (utilisé pour les plugins Magic Link et Email OTP).
   - **GitHub** : Fournisseur d'authentification OAuth.

3. **Astuces concrètes et réutilisables** :
   - Installer Better Auth via npm (`npm i better-auth`) et configurer les variables d'environnement (`BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`).
   - Utiliser la CLI de Better Auth (`npx better-auth migrate`) pour générer et appliquer automatiquement les tables d'authentification nécessaires dans la base de données.
   - Activer des plugins modulaires (Two Factor, Magic Link, Username, Passkey, Two-Factor Authentication, etc.) selon les besoins de l'application.
   - Utiliser `authClient` côté client pour simplifier les appels d'authentification (sign-in, sign-up, sign-out).

4. **Chiffres de revenus annoncés** :
   - Non précisé.

---
