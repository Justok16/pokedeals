# Les règles ESSENTIEL pour les HOOKS React !

Vidéo : https://youtu.be/rLYtXmIjHdA · durée 9:35 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Explication des **Rules of Hooks** (règles des hooks) en React, notamment l'interdiction d'appeler des hooks dans des boucles, des conditions ou des fonctions imbriquées, et l'importance de respecter la convention de nommage commençant par `use`.
2) **Outils, sites ou dépôts GitHub cités :**
   - **React :** Librairie JavaScript.
   - **TypeScript :** Langage de programmation.
3) **Astuces concrètes et réutilisables :**
   - Toujours appeler les hooks au niveau supérieur (top level) d'un composant fonctionnel, jamais dans un `if`, une boucle ou une fonction classique.
   - Nommer ses hooks personnalisés en commençant obligatoirement par le préfixe `use` (convention de nommage indispensable pour que React et les linters identifient les hooks).
   - Comprendre le fonctionnement interne des hooks (gestion par index dans une liste chaînée / structure liée au composant lors du rendu).
4) **Chiffres de revenus annoncés :** Non précisé.
