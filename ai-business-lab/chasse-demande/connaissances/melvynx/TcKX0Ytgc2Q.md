# LA PIRE ERREUR REACT QUE TU FAIS #shorts #developpeur

Vidéo : https://youtu.be/TcKX0Ytgc2Q · durée 0:44 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Éviter l'utilisation excessive de `useEffect` pour synchroniser des états (`states`) dérivés en React, car cela provoque des rendus inutiles et un mauvais design de code, au profit d'un calcul direct lors du rendu.
2) **Outils, sites ou dépôts GitHub cités** : Aucun outil, site ou dépôt GitHub n'a été cité.
3) **Astuces concrètes et réutilisables** :
   - Éviter d'utiliser `useEffect` pour mettre à jour un state basé sur d'autres states (anti-pattern « derived state »).
   - Calculer directement la valeur combinée dans le corps du composant (ex. : `const fullName = `${firstName} - ${lastName}``).
   - Supprimer le state redondant et le `useEffect` associé pour garder un code plus simple et performant.
4) **Chiffres de revenus annoncés** : Non précisé.
