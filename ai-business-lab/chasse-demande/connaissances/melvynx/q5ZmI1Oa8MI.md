# Next.js 15.5: TOUTES les nouveautés à connaître!

Vidéo : https://youtu.be/q5ZmI1Oa8MI · durée 11:21 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. L'idée principale : La présentation des 5 nouveautés majeures de Next.js 15.5, incluant le nouveau bundler Turboopack en version bêta, le support stable du middleware Next.js, les améliorations de TypeScript (Typed Routes), l'optimisation pour l'IA et le nettoyage des outils de linting (remplacement par Biome).

2. Outils et sites cités :
- Next.js 15.5 : gratuit, framework React.
- Turboopack : gratuit (intégré à Next.js), bundler remplaçant Webpack.
- Vercel (vercel.com) : gratuit/payant, plateforme de déploiement.
- Aiblueprint.dev (aiblueprint.dev/ai) : payant, site proposant un blueprint et une formation sur l'utilisation de l'IA et des middlewares.

3. Astuces concrètes :
- Activer Turboopack lors du développement ou du build en ajoutant le flag `--turbopack` (ex: `next dev --turbopack` ou `next build --turbopack`) pour accélérer la compilation.
- Utiliser le middleware basé sur le runtime Edge (`runtime = 'edge'`) pour exécuter du code proche des utilisateurs.
- Activer les routes typées dans `next.config.ts` avec `typedRoutes: true` pour bénéficier d'une sécurité de type complète sur la navigation.
- Configurer des scripts de post-installation (`postinstall`) dans `package.json` pour générer automatiquement les types Prisma et types de routes.
- Remplacer le linter classique par Biome ou ESLint optimisé pour éviter les erreurs de type lors du build en production.

4. Chiffres de revenus : Non précisé.
