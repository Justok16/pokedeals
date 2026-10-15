# Faire des JOBS en NextJS en utilisant Inngest

Vidéo : https://youtu.be/mcfUbKjqads · durée 22:02 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Présentation des performances spectaculaires de la mise à jour « Turbo Pack » de Next.js 15, qui réduit drastiquement les temps de chargement des applications web et transforme l'expérience de développement.

2) **Outils, sites ou dépôts GitHub cités** :
- **Next.js 15 (avec Turbo Pack)** : framework React mis à jour avec le nouveau bundler Turbo Pack. Gratuit (open source).
- **Codelynx** : plateforme de formation utilisée pour tester et illustrer les temps de chargement. (Gratuit/Payant selon les cours).
- **Webpack** : ancien bundler JavaScript/TypeScript. Gratuit (open source).
- **Babel** : outil de transpilation JavaScript pour la compatibilité (ES5). Gratuit (open source).
- **Vite (ViteJS)** : bundler/outil de build frontend rapide. Gratuit (open source).
- **SWC (Speedy Web Compiler)** : compilateur web rapide en Rust. Gratuit (open source).

3) **Astuces concrètes et réutilisables** :
- Activer Turbo Pack dans un projet Next.js en lançant la commande de développement avec le flag `--turbopack` (`next dev --turbopack`).
- Comprendre les différences entre bundlers (Webpack vs Vite/TurboPack/SWC) pour optimiser les performances de build et de rechargement à chaud (HMR) en développement.
- Utiliser le code-splitting et la modularisation pour éviter de charger des dépendances inutiles et améliorer les temps de First Load JS.

4) **Chiffres de revenus annoncés ("affirmé par l'auteur")** :
- Non précisé (la vidéo se concentre sur les performances techniques et les temps de chargement en millisecondes/secondes).
