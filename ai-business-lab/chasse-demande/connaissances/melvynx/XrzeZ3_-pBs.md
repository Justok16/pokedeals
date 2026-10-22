# Les requests HTTP : Le Guide Ultime avec Server State

Vidéo : https://youtu.be/XrzeZ3_-pBs · durée 9:30 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Présentation du « server-state » (état du serveur) et explication des avantages d'utiliser la bibliothèque TanStack/Query (React Query) pour le gérer efficacement dans une application web connectée à des API.

2) **Outils, sites ou dépôts GitHub cités** :
   - **TanStack/Query (React Query)** : Gratuit (open source), bibliothèque JavaScript/TypeScript pour gérer, mettre en cache et synchroniser le server-state.
   - **OpenAI API** : Service payant (mentionné comme exemple d'API externe).
   - **Redux / Redux Toolkit / React Query (autres variantes)** : Mentionnés comme alternatives ou comparaisons pour la gestion d'état.
   - **GitHub** : Dépôt de test utilisé dans l'exemple de code (URL : `https://api.github.com/repos/tannerlinsley/react-query`).

3) **Astuces concrètes et réutilisables** :
   - Différencier le *state* local (contrôlé par l'application, ex: mode sombre, champ de recherche) du *server-state* (données stockées sur un serveur distant, ex: liste des utilisateurs, modifiables par d'autres).
   - Utiliser `useQuery` avec une `queryKey` (clé unique) et une `queryFn` (fonction de fetch) pour déléguer à la bibliothèque le caching, les mises à jour en arrière-plan, la gestion des timeouts et la pagination.
   - Gérer automatiquement les états de chargement (`isLoading`), d'erreur (`error`) et les données reçues sans stocker manuellement ces valeurs dans un état local.

4) **Chiffres de revenus annoncés** :
   - Non précisé.

---
