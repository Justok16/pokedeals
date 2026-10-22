# OPTIMISER LES RENDERS SUR REACT

Vidéo : https://youtu.be/qJMf5k8MWks · durée 1:00 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Une technique d'optimisation des rendus React sans utiliser `useMemo` ou `useCallback`, consistant à isoler les états changeants dans un composant wrapper séparé pour éviter de re-render un composant lourd.
2) **Outils, sites ou dépôts GitHub cités :**
- React (framework, gratuit) avec ses hooks (`useState`).
3) **Astuces concrètes et réutilisables :**
- Créer un composant wrapper (ex: `UsernameWrapper`) pour y placer le `useState` et les sous-composants dépendants, afin de laisser le composant lourd en dehors.
- Utiliser la prop `children` (passée sous forme de composant parent) pour que le composant lourd ne subisse pas de re-render inutile lors du changement d'état du formulaire.
4) **Chiffres de revenus annoncés :**
- Non précisé.
