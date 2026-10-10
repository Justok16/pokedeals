# Formation Convex : Plateforme de database et Backend pour tes applications

Vidéo : https://youtu.be/t5herCGqveo · durée 36:53 · résumé Gemini (gemini-3.5-flash-lite, lot de 5) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : L'auteur présente Convex, une base de données et un backend temps réel populaire en 2025, et montre comment créer et déployer un clone de r/place en connectant Convex avec une application Next.js.

2) **Outils, sites et dépôts GitHub cités** :
   - **Convex** (`convex.dev`) : Solution de backend et base de données temps réel. Outil freemium / payant selon l'utilisation (non précisé en détail, mais service cloud).
   - **Next.js** : Framework React pour le web (gratuit / open source).
   - **GitHub** : Plateforme d'hébergement de code source, utilisée pour l'authentification Convex (gratuit/payant selon les offres).
   - **Vercel** : Plateforme de déploiement pour applications web (gratuit / payant selon les offres).
   - **Cursor** : IDE / éditeur de code utilisé dans la vidéo (non précisé si gratuit ou payant).
   - **Node.js / npm / pnpm** : Gestionnaires de paquets et environnement d'exécution (open source / gratuits).
   - **Tailwind CSS** : Framework CSS utilisé pour le style (open source / gratuit).
   - **Excalidraw** : Outil de schématisation utilisé pour les diagrammes d'architecture (non précisé si gratuit ou payant).
   - **UI Colors / Shadcn UI** (ou sources similaires de palettes/composants) : Utilisé pour les couleurs et composants UI (gratuits / open source).

3) **Astuces concrètes et réutilisables** :
   - Utiliser `pnpm create next-app@latest ... --yes` combiné avec l'installation du SDK Convex (`npx convex dev` ou `npm install convex`) pour initialiser rapidement un projet full-stack synchronisé.
   - Séparer la logique de base de données dans un fichier dédié (ex: `canvas.ts`) en définissant des fonctions `query` et `mutation` pour que Convex gère automatiquement la réactivité et la synchronisation des données côté client sans code WebSocket manuel.
   - Utiliser le `useQuery` de Convex dans les composants React pour récupérer les données en temps réel et les `useMutation` pour effectuer des mises à jour synchronisées.
   - Configurer les variables d'environnement (`.env.local`) et la clé de déploiement de production (`CONVEX_DEPLOY_KEY`) lors du déploiement sur Vercel pour relier l'application au backend Convex en production.

4) **Chiffres de revenus annoncés** :
   - Non précisé.
