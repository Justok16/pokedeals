# REMIX vs NEXTJS : Mon avis Tranché 🗡️

Vidéo : https://youtu.be/nuT6JOyVZho · durée 16:54 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Comparer **Next.js** et **Remix** en 2023 à travers un cas d'étude détaillé (gestion des layouts, du data fetching, des Server Actions, etc.).
2) **Outils, sites ou dépôts GitHub cités :**
   - **Next.js** : Framework React gratuit.
   - **Remix** : Framework React concurrent, gratuit.
   - **GitHub** : Plateforme gratuite (référencée pour le code source du clone Twitter).
3) **Astuces concrètes et réutilisables :**
   - En Next.js (App Router), la gestion des layouts se fait via des fichiers imbriqués (`layout.tsx`), tandis qu'en Remix, on utilise des fichiers de base avec des suffixes (`_base`).
   - Pour le data fetching, Remix utilise des `loader` (fonctions exécutées uniquement sur le serveur), tandis que Next.js utilise des Server Components avec `await` direct.
   - Pour les mutations de données, Remix utilise des `action` avec des formulaires HTML natifs et des hooks comme `useActionData`, tandis que Next.js utilise les Server Actions (`"use server"`).
   - Next.js gère le streaming natif via `<Suspense>`, ce qui permet d'afficher des parties de page progressivement, alors que Remix utilise la fonction `defer`.
4) **Chiffres de revenus annoncés :** Non précisé.
