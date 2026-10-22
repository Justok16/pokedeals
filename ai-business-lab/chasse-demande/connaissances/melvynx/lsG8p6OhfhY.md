# TUTO / COURS React useState en 1 heure (2/5)

Vidéo : https://youtu.be/lsG8p6OhfhY · durée 47:53 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Ce cours magistral détaille l'utilisation du hook `useState` en React à travers la construction et le débogage d'une application de type « todo list ».

2) **Outils, sites ou dépôts GitHub cités** :
- **Vite (vitejs.dev)** : Gratuit, outil de build et de création d'applications web frontend (ViteJS).
- **Tailwind CSS** : Gratuit, bibliothèque CSS.
- **DaisyUI** : Gratuit, bibliothèque de composants pour Tailwind CSS.
- **React (GitHub / react-github)** : Gratuit, bibliothèque JavaScript.
- **Escalidraw (app.excalidraw.com)** : Gratuit, outil de dessin et de schémas.

3) **Astuces concrètes et réutilisables** :
- Utiliser des fonctions anonymes (`onClick={() => handleEvent()}`) pour passer des callbacks aux gestionnaires d'événements React.
- Effectuer du *destructuring* sur le tableau retourné par `useState` (`const [count, setCount] = useState(10);`) pour récupérer proprement la valeur (*getter*) et la fonction de mise à jour (*setter*).
- Ne pas modifier directement le state, mais utiliser des copies ou des fonctions de mise à jour immutables pour que React détecte les changements et déclenche un re-rendu (*diffing* / *commit*).
- Utiliser l'approche fonctionnelle avec `setCount(current => current + 1)` pour s'assurer d'utiliser la valeur la plus récente du state.

4) **Chiffres de revenus annoncés** : Non précisé.

---
