# Tout savoir sur le useState en 2 minutes

Vidéo : https://youtu.be/Z3bN-I6W8QQ · durée 7:23 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur explique en détail le fonctionnement du hook `useState` de React, sa nature asynchrone, son immuabilité, et comment manipuler correctement les états (notamment avec les objets) pour éviter les problèmes de rendu.
2) **Outils, sites ou dépôts GitHub cités :**
- **Codesandbox** (utilisé pour les démonstrations de code en direct) ;
- **Cours gratuit sur le useState** (gratuit, accessible via la description de la vidéo, incluant 5 exercices et leurs solutions).
3) **Astuces concrètes et réutilisables :**
- Retenir la structure de base de `useState` : une valeur initiale, un getter pour afficher la valeur, et un setter pour la modifier.
- Garder en tête que `useState` est asynchrone : pour mettre à jour un état basé sur la valeur précédente, utiliser une fonction callback (ex: `setCount(curr => curr + 1)`) plutôt que de modifier directement la variable.
- Se souvenir que `useState` est immuable : un composant ne se re-render que si la nouvelle valeur est différente de l'ancienne.
- Pour les objets, utiliser l'opérateur de décomposition (*spread operator*, ex: `{ ...user, username: "Jean" }`) lors de la mise à jour via le setter afin de créer une nouvelle référence en mémoire et déclencher un re-render.
4) **Chiffres de revenus annoncés :**
- Non précisé.
