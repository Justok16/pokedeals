# TUTO / COURS React - Clone de TicTacToe de A à Z

Vidéo : https://youtu.be/WSrdYekvgX4 · durée 39:25 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Suivre le tutoriel officiel "Tic-Tac-Toe" de la documentation React pour apprendre les fondamentaux (composants, JSX, gestion du state, props, et l'utilisation de `useState` et des clés).
2) **Outils, sites ou dépôts GitHub cités :**
   - **Documentation React / Tutoriel Tic-Tac-Toe :** Site officiel de React (gratuit).
   - **CodeSandbox / Playgroud React :** Environnement de code en ligne utilisé pour coder le jeu (gratuit).
3) **Astuces concrètes et réutilisables :**
   - Utiliser la balise fragment `<>` ou `<React.Fragment>` pour retourner plusieurs éléments JSX adjacents sans conteneur superflu.
   - Comprendre la différence entre l'utilisation d'une référence d'objet (ex. `Square` avec une majuscule) et une chaîne de caractères (ex. `square` en minuscule) en JSX qui se traduit par `React.createElement`.
   - Passer des données aux composants enfants via les `props` (ex. `value` et `onSquareClick`).
   - Gérer l'immutabilité des tableaux (utiliser `.slice()`) avant de mettre à jour le state pour permettre le "time travel" (revenir en arrière dans l'historique des coups).
4) **Chiffres de revenus annoncés :** Non précisé.
