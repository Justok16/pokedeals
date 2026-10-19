# React useState : Tous les secrets du hooks React useState 🤫

Vidéo : https://youtu.be/FX7rSVnL1YA · durée 10:13 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Guide complet sur le hook `useState` en React : fonctionnement, syntaxe, valeur par défaut, déstructuration, déclenchement des re-renders, et bonnes pratiques pour optimiser les performances (notamment l'utilisation de `useCurr` / fonction de callback).
2) **Outils, sites ou dépôts GitHub cités :**
- **React :** Gratuit. Bibliothèque JavaScript.
- **Vite :** Gratuit. Outil de build et serveur de développement local.
- **JavaScript :** Langage de programmation.
3) **Astuces concrètes et réutilisables :**
- Utiliser la déstructuration du tableau renvoyé par `useState` : `const [state, setState] = useState(defaultValue)`.
- Fournir une valeur par défaut dans `useState(0)` pour éviter `undefined` au premier rendu.
- Pour mettre à jour un état basé sur la valeur précédente, utiliser une fonction de rappel dans le setter (ex: `setState(curr => curr + 1)`) pour s'assurer d'avoir toujours la valeur à jour et éviter les problèmes de synchronisation lors des re-renders multiples.
- Éviter d'appeler des calculs lourds ou des fonctions directement dans le corps du composant sans mémoïsation si cela déclenche des re-renders superflus.
4) **Chiffres de revenus annoncés :** Non précisé.
