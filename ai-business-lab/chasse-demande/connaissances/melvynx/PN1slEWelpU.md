# Arrêtez d'Utiliser useState en 2025!

Vidéo : https://youtu.be/PN1slEWelpU · durée 1:41 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur analyse et critique un post LinkedIn proposant l'utilisation conjointe de `useState`, d'un `useReducer` avec un store contextuel et de `useQuery`, pour conclure qu'il vaut mieux privilégier des bibliothèques existantes comme TanStack Table et `useQuery` afin d'éviter la complexité inutile.
2) **Outils, sites ou dépôts cités :**
   - **TanStack Query :** Non précisé (bibliothèque recommandée pour la gestion des données et state de l'URL).
   - **TanStack Table :** Non précisé (bibliothèque recommandée pour la gestion des tables, filtres, etc.).
   - **useQuery / useQueryState / useTable :** Non précisé (fonctions/hooks mentionnés).
3) **Astuces concrètes et réutilisables :**
   - Éviter d'utiliser de multiples `useState` et des `useEffect` complexes pour fetcher des données ; préférer l'utilisation de `useQuery`.
   - Utiliser des bibliothèques de composants comme TanStack Table pour gérer les tables et les filtres plutôt que de réinventer la logique dans un store personnalisé.
   - Utiliser `useQueryState` pour gérer l'état de l'URL.
4) **Chiffres de revenus annoncés :** Aucun chiffre de revenus n'est annoncé.
