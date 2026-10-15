# Comment j’organise mon code avec NextJS ?

Vidéo : https://youtu.be/O8vlNp2aD20 · durée 7:53 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de détailler l'organisation et la structure des dossiers d'un projet Next.js multi-tenant (SaaS) basé sur l'App Directory, en séparant clairement le routage, les composants réutilisables et les fonctionnalités métiers.
2)
- nowts.app : application/boilerplate SaaS de l'auteur (payant via accès au cours, prix non précisé dans l'extrait) comptant plus de 515 utilisateurs.
- Excalidraw : outil de schéma (gratuit/freemium) utilisé pour visualiser l'architecture des dossiers.
- Vercel : plateforme d'hébergement et de déploiement (freemium).
3) Astuces :
- Utiliser le dossier `app/` (routing) strictement pour les fichiers de structure Next.js (`page.tsx`, `layout.tsx`, `error.tsx`, `loading.tsx`, `template.tsx`) et y placer les composants UI spécifiques à la page voisine si nécessaire.
- Isoler les composants transversaux et UI purs (boutons, icônes SVG, utilitaires) dans un dossier `components/` à la racine de `src/`.
- Regrouper la logique métier, les actions de serveur, les schémas Zod et les formulaires par domaine fonctionnel dans un dossier `features/` (ex: `auth`, `contact`), et stocker les configurations globales (Prisma, environnement, actions sécurisées) dans `libs/`.
4) Chiffres :
- Plus de 515 personnes codent avec nowts.app (affirmé par l'auteur).
