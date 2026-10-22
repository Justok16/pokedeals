# TUTO / COURS React useMemo et useCallback en 1 heure (5/5)

Vidéo : https://youtu.be/WDtVP52qukg · durée 46:10 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette masterclass avance sur React aborde l'utilisation de `useRef`, le mécanisme des rendus (`render`), l'optimisation avec `useMemo` et `useCallback`, ainsi que l'optimisation avancée des composants.

2) **Outils, sites ou dépôts GitHub cités** :
   - **Vite (ViteJS)** : Gratuit, outil de bundling et de développement frontend.
   - **Tailwind CSS** : Gratuit, framework CSS pour le styling.
   - **DaisyUI** : Gratuit, bibliothèque de composants pour Tailwind CSS permettant de simplifier le design des boutons et classes.
   - **mlv.sh/react** (ou `mlv.sh/ytr5`) : Gratuit (lien mentionné par l'auteur), plateforme de formation et d'exercices pratiques sur React.

3) **Astuces concrètes et réutilisables** :
   - Utiliser **`useRef`** pour cibler un élément DOM (par exemple un input) et appeler des méthodes comme `.focus()` sans provoquer de re-rendu du composant (contournant le cycle de rendu React).
   - Mémoriser des composants avec **`useMemo`** (ou `memo`) pour éviter les rendus inutiles lorsqu'aucun `prop` n'a changé.
   - Utiliser **`useCallback`** pour stabiliser les références de fonctions passées en `props` à des composants enfants mémorisés.
   - Comprendre les déclencheurs de rendu : un composant se re-render si son parent render, si son propre `state` change, ou si un contexte (`useContext`) auquel il est abonné est modifié.
   - Utiliser l'outil de profilage pour mesurer les durées de rendu et identifier les composants lents.

4) **Chiffres de revenus annoncés** : Non précisé.

---
