# La plus GROSSE Incompréhension de REACT expliquée !

Vidéo : https://youtu.be/Mtl7agDQD60 · durée 9:02 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Explication détaillée de l'immutabilité des états dans React (`useState`), pourquoi modifier un state avec la même valeur ne déclenche pas de nouveau rendu, et comment fonctionne la comparaison par référence des objets et des tableaux.
2) **Outils, sites ou dépôts GitHub cités :**
   - **CodeSandbox :** gratuit (éditeur de code en ligne utilisé pour les démos).
3) **Astuces concrètes et réutilisables :**
   - Pour forcer React à ré-afficher un composant lors de la modification d'un objet ou d'un tableau dans un `state`, il faut créer une nouvelle référence (par exemple en utilisant l'opérateur de décomposition `{ ...currentValue, key: newValue }` ou `[...currentArray, newItem]`) plutôt que de modifier l'objet existant en place.
   - Comprendre que les types primitifs (string, number, boolean) comparent leurs valeurs, tandis que les objets et tableaux comparent leurs références en mémoire.
4) **Chiffres de revenus annoncés :**
   - Non précisé.
