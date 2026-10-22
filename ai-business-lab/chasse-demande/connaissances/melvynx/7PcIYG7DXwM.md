# Le PIÈGE du rendu Conditionnel en React (tu fais peut-être cette erreur)

Vidéo : https://youtu.be/7PcIYG7DXwM · durée 5:38 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Éviter l'erreur courante en React/JSX consistant à afficher directement un nombre égal à `0` (ou d'autres falsy values) avec l'opérateur logique `&&`, ce qui affiche "0" à l'écran au lieu de ne rien afficher.
2) **Outils, sites ou dépôts GitHub cités :**
   - **React :** Bibliothèque JavaScript (gratuite).
   - **CodeSandbox :** Éditeur de code en ligne utilisé pour les exemples (gratuit).
3) **Astuces concrètes et réutilisables :**
   - Ne pas utiliser la syntaxe `{ condition && <composant /> }` lorsque la condition est un nombre qui peut valoir `0`, car `0 && ...` évalue à `0` et affiche `0` dans le DOM.
   - **Solution 1 :** Transformer la condition en booléen explicite en utilisant l'opérateur de double négation ou `Boolean()` (ex. `{ !!age && <p>...</p> }` ou `{ age !== null && <p>...</p> }`).
   - **Solution 2 :** Utiliser une condition stricte comparant à `null` ou vérifiant explicitement la présence d'une valeur valide (ex. `{ age != null && <p>...</p> }`).
4) **Chiffres de revenus annoncés :** Non précisé.
