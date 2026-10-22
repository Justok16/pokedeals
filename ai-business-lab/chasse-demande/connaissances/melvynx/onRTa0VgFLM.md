# NE FAIS PAS CETTE ERREUR REACT #shorts #developpeur

Vidéo : https://youtu.be/onRTa0VgFLM · durée 0:53 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Il est déconseillé d'effectuer des requêtes `fetch` à l'intérieur des `useEffect` en React, car ce n'est pas leur rôle ; il est préférable d'utiliser des librairies dédiées comme **SWR** pour gérer le cache, les erreurs et le chargement des données.
2) **Outils, sites ou dépôts cités** :
   - **SWR** : Librairie de React Hooks pour le data fetching (gratuite), créée par Vercel.
3) **Astuces concrètes et réutilisables** :
   - Remplacer le code lourd de `useEffect` (avec `AbortController` et `fetch` manuel) par un simple hook `useSWR` pour récupérer, mettre en cache et gérer les états de chargement (`isLoading`) et les erreurs en une seule ligne.
4) **Chiffres de revenus annoncés** :
   - Non précisé.
