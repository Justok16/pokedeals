# Next.js : N'utilise plus les API Routes, voici ton nouvel outil favori

Vidéo : https://youtu.be/e4eWX8er2sQ · durée 19:36 · résumé Gemini (gemini-flash-lite-latest, lot de 9) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Le vidéaste présente **ZSA**, une bibliothèque TypeScript pour Next.js qui permet de créer des Server Actions typées de manière simple, efficace et sécurisée, tout en intégrant facilement des validateurs comme Zod et des outils comme React Query.

3) **Outils, sites ou dépôts GitHub cités** :
- **ZSA** : Bibliothèque TypeScript open-source pour les Server Actions dans Next.js (gratuite).
- **Zod** : Bibliothèque de validation de schémas (gratuite).
- **React Query (@tanstack/react-query)** : Bibliothèque de gestion d'état et de requêtes asynchrones pour React (gratuite).
- **Next.js** : Framework web (gratuit).
- **Prisma** : ORM (mentionné dans le code du projet, gratuit).

3) **Astuces concrètes et réutilisables** :
- Installer ZSA avec la commande `pnpm install zsa zsa-react zod`.
- Créer un fichier d'actions (ex: `zsa.ts` ou `actions.ts`) avec `"use server"` et `createserverAction()` pour centraliser les Server Actions.
- Utiliser les schémas Zod pour valider automatiquement les entrées (`input`) et les sorties (`output`) des Server Actions.
- Intégrer ZSA avec React Query (`@tanstack/react-query`) via les hooks fournis (`useServerActionQuery`, `useServerActionMutation`) pour bénéficier du typage et du cache.
- Gérer l'authentification et les autorisations via des procédures chaînées (`createserverActionProcedure()`) pour vérifier les cookies ou les tokens avant d'exécuter l'action.

4) **Chiffres de revenus annoncés** : Non précisé.
