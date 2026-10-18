# Les 15 Erreurs useState & useEffect que TOUS les Débutants Font en React

Vidéo : https://youtu.be/z3A_tuWn0wA · durée 30:58 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Corriger 15 erreurs courantes commises par les développeurs débutants ou intermédiaires avec React et ses hooks, notamment `useState` et `useEffect`.
2) **Outils, sites ou dépôts GitHub cités :**
   - **React** : Gratuit, bibliothèque JavaScript.
   - **Sonner** : Gratuit, bibliothèque de notifications (toast).
   - **React DevTools** : Gratuit, extension de navigateur pour déboguer React.
   - **useSWR** : Gratuit, bibliothèque de data fetching pour React.
3) **Astuces concrètes et réutilisables :**
   - Ne pas supposer que le changement de state dans React est synchrone ; utiliser une variable dérivée ou attendre le rendu suivant.
   - Éviter d'appeler les hooks (`useState`) de manière conditionnelle ou à l'intérieur de boucles/conditions pour ne pas corrompre l'ordre des hooks.
   - Ne pas modifier un state en mutant directement sa référence ou en modifiant un objet passé en dépendance, toujours créer un nouvel objet (`new Object`) pour forcer le re-rendu.
   - Éviter d'utiliser `useEffect` avec un `fetch` pour synchroniser des données si une autre approche plus propre (comme SWR) ou un calcul direct dans le composant est possible.
   - Utiliser des contrôleurs d'annulation (`AbortController`) ou des bibliothèques dédiées (`useSWR`) pour éviter les requêtes dupliquées et gérer proprement les états de chargement (`isLoading`).
4) **Chiffres de revenus annoncés :** Non précisé.
