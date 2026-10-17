# useRef en React | Ce Que J'aurais Voulu Savoir Plus Tôt !

Vidéo : https://youtu.be/zPG6YGhC7s4 · durée 12:12 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé demandé :

1. **Idée principale** :
Cette vidéo explique le fonctionnement et l'utilité du hook `useRef` en React. Elle montre comment récupérer la référence d'un élément du DOM, l'utiliser pour lier une valeur à un composant (sans provoquer de rerender contrairement à `useState`), et détaille plusieurs cas d'usage pratiques (comme le focus d'un input, un debounce ou un canvas).

2. **Outils, sites ou dépôts GitHub cités** :
- **React** (Bibliothèque JavaScript) : Gratuit, sert à créer des interfaces utilisateurs.
- **Vite** (Outil de build / bundler) : Gratuit, sert à démarrer et builder une application React.
- **VS Code** (Éditeur de code) : Gratuit, sert à écrire du code.
- **GitHub** (Hébergeur de code) : Gratuit (pour les fonctionnalités de base), mentionné via des liens dans le tutoriel.
- **CodeSandbox** (Environnement de code en ligne) : Gratuit (fonctionnalités de base), utilisé dans les exemples de code (liens vers des playgrounds interactifs).

3. **Astuces concrètes et réutilisables** :
- Utiliser `useRef` pour accéder directement à un élément du DOM (par exemple pour appliquer un `.focus()` ou modifier le style).
- Utiliser la valeur `.current` d'un `useRef` pour stocker des données sans déclencher de nouveau rendu (rerender) du composant.
- Utiliser un `useRef` pour gérer des timers (comme un debounce) ou des positions de souris (dans un canvas).

4. **Chiffres de revenus annoncés** :
- Non précisé.
