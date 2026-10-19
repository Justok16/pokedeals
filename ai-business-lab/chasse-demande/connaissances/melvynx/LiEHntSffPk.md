# React Query en 40 minutes - Cours complet débutant

Vidéo : https://youtu.be/LiEHntSffPk · durée 40:04 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** Crash-course complet sur l'utilisation de React Query (TanStack Query) avec Next.js pour gérer le "server state" et le cache des données, en remplaçant efficacement les `useEffect` classiques.
2. **Outils et dépôts cités :**
   - **React Query (TanStack Query) :** Gratuit, bibliothèque de gestion d'état serveur.
   - **Next.js :** Gratuit, framework React.
   - **TypeScript :** Gratuit, sur-ensemble typé de JavaScript.
   - **Zod :** Gratuit, bibliothèque de validation de schémas.
   - **React Query Devtools :** Gratuit, outils de débogage pour React Query.
3. **Astuces concrètes :**
   - Utiliser `QueryClient` et `QueryClientProvider` pour envelopper l'application.
   - Remplacer les `useEffect` et états locaux par le hook `useQuery` pour un fetch automatique et sécurisé.
   - Définir une `queryKey` unique (ex. `['users']`) et une `queryFn` (la fonction fetch).
   - Utiliser `enabled` dans `useQuery` pour conditionner le fetch (ex. attendre qu'un ID soit défini).
   - Utiliser `useMutation` pour les requêtes d'écriture (POST, etc.) combiné avec `queryClient.invalidateQueries` pour rafraîchir le cache.
   - Activer `ReactQueryDevtools` pour visualiser et inspecter l'état du cache.
4. **Chiffres de revenus :** Non précisé.
