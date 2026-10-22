# Tutoriel NextJS 13 en 1 HEURE | Apprendre l'ESSENTIEL

Vidéo : https://youtu.be/c6yk8apme_c · durée 54:46 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. L'idée principale de cette vidéo est de proposer un tutoriel complet d'une heure sur Next.js 13 en créant pas à pas une application de type "board list" (tableau de propositions avec votes) pour expliquer en pratique le routage du dossier `app`, l'utilisation des *Server Components*, la gestion des erreurs, et l'intégration de Prisma.

2. Outils, sites ou dépôts GitHub cités :
- Next.js 13 (framework, gratuit) : framework principal du tutoriel.
- Prisma (ORM, gratuit) : utilisé pour la base de données et l'interaction avec les modèles.
- TypeScript (langage, gratuit) : utilisé pour le typage.
- Tailwind CSS (framework CSS, gratuit) : utilisé pour le design et les classes utilitaires.
- Zod (librairie de validation, gratuite) : utilisée pour valider les schémas de données.
- VS Code (éditeur de code, gratuit) : environnement de développement.
- Dépôt GitHub (mentionné dans la description : `Melyvn/board-application-ranking`) : contient le code de départ (setup de base) du projet.
- Site de formation / Dépôt personnel (CodeLynx, avec un cours gratuit sur Next.js, Server Components, TypeScript, Zod et React-Query) : mentionné pour aller plus loin.

3. Astuces concrètes et réutilisables :
- Structurer le dossier `app` de Next.js 13 avec la hiérarchie des fichiers spéciaux (`layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`) pour gérer automatiquement les structures de pages, les états de chargement et les frontières d'erreur de manière emboîtée (comme des poupées russes).
- Utiliser `use client` uniquement sur les composants nécessitant de l'interactivité (formulaires, clics, hooks), tandis que les composants par défaut restent des *Server Components* légers sans JavaScript envoyé inutilement au client.
- Valider les données entrantes des requêtes API POST avec Zod (`Zod.object({...})`) pour s'assurer de la conformité des données avant de les insérer en base de données via Prisma (`prisma.board.create(...)`).

4. Chiffres de revenus annoncés :
- Non précisé.
