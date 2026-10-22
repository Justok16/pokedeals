# Le guide complet useContext en React (pour vraiment tout comprendre)

Vidéo : https://youtu.be/V13h-VKpB7Y · durée 17:52 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Guide complet sur l'utilisation du hook `useContext` en React pour éviter le *props drilling* (passage de props à travers de multiples niveaux de composants) et gérer l'état global de manière centralisée.
2) **Outils, sites ou dépôts GitHub cités :**
   - **React :** Librairie JavaScript.
   - **Zustand :** Librairie de gestion d'état (alternative à Context).
   - **Jotai :** Librairie de gestion d'état (alternative à Context).
3) **Astuces concrètes et réutilisables :**
   - Utiliser `createContext` et `useContext` pour partager des données (comme un utilisateur connecté) sans passer par les props à chaque niveau.
   - Créer un composant Provider personnalisé pour encapsuler la logique et les fonctions de modification d'état.
   - Créer un hook personnalisé (ex: `useUser`) pour consommer le contexte plus facilement et proprement.
   - **Attention à l'optimisation :** Un changement de valeur dans le Provider provoque le *re-render* de tous les composants enfants consommateurs. Pour éviter des re-rendus inutiles sur de grosses applications, privilégier des librairies comme **Zustand** ou **Jotai**.
4) **Chiffres de revenus annoncés :** Non précisé.
