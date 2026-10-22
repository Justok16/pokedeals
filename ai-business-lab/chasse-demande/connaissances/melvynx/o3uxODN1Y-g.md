# TUTO / COURS React useContext et Zustand en 1 heure (4/5)

Vidéo : https://youtu.be/o3uxODN1Y-g · durée 40:46 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo présente le hook `useContext` pour la gestion d'état en React, ses limites face aux états globaux, et introduit **Zustand** comme solution idéale et performante pour gérer l'état global de manière simple et composable.

2) **Outils, sites ou dépôts GitHub cités** :
   - **Vite (ViteJS)** : Gratuit, outil de build frontend.
   - **Tailwind CSS** : Gratuit, framework CSS.
   - **DaisyUI** : Gratuit, bibliothèque de composants UI.
   - **Lucide (Lucide React)** : Gratuit, bibliothèque d'icônes.
   - **Zustand** : Gratuit, bibliothèque légère de gestion d'état global (`npm install zustand`).
   - **Radix UI** : Gratuit, bibliothèque de composants primitifs (mentionnée pour ses patterns de dialogue).
   - **mlv.sh/react** : Gratuit (lien de la formation de l'auteur), pour accéder aux cours et exercices pratiques.

3) **Astuces concrètes et réutilisables** :
   - Utiliser **`useContext`** pour injecter des données (comme des props ou des états) à travers l'arbre des composants sans faire de "prop drilling" (passage de props de parent en enfant sur plusieurs niveaux).
   - Attention : `useContext` n'est pas un gestionnaire d'état global complet ; dès qu'une valeur du Context change, **tous** les composants consommateurs se re-rendent (ce qui peut poser des problèmes de performance sur de grands arbres).
   - Utiliser **Zustand** pour créer un `store` externe à React, permettant de contourner les re-rendus inutiles et de gérer des états globaux complexes de façon propre et modulaire.
   - Créer des composants composites réutilisables (pattern Compound Components) en combinant `useContext` et des méthodes de validation pour lever des erreurs explicites si un composant enfant est utilisé hors de son Provider.
   - Utiliser `createPortal` pour rendre des modales (`Dialog`) directement dans le `<body>` du DOM afin d'éviter les problèmes de positionnement CSS (`z-index` ou `overflow`).

4) **Chiffres de revenus annoncés** : Non précisé.

---
