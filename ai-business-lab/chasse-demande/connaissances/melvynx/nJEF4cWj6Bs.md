# Les 10 Erreurs useState que TOUS les Débutants Font en React

Vidéo : https://youtu.be/nJEF4cWj6Bs · durée 21:55 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Cette vidéo présente 10 erreurs courantes commises par les développeurs (y compris seniors) lors de l'utilisation de React et de son hook `useState`, et explique comment les corriger pour optimiser les performances, éviter les bugs et garder un code propre.

2) **Outils, sites ou dépôts GitHub cités :**
* `useState` (de React) : Gratuit (intégré à React), utilisé pour gérer l'état local dans un composant.
* `useEffect` (de React) : Gratuit (intégré à React), utilisé pour gérer les effets secondaires.
* React (bibliothèque JS) : Gratuit (open-source), framework frontend.
* Vite (outil de build) : Gratuit (open-source), utilisé pour le développement web.
* `use-state` (ou packages npm de state management similaires, mentionnés via `npm package` / `withState`) : Gratuits, utilisés pour encapsuler et structurer l'état.

3) **Astuces concrètes et réutilisables :**
* **Erreur 1 (Exécution de fonctions coûteuses) :** Ne pas passer l'appel direct d'une fonction lourde en argument initial de `useState` (car elle s'exécuterait à chaque render), mais passer une fonction fléchée ou la référence de la fonction pour qu'elle ne s'exécute qu'au premier render.
* **Erreur 2 (Objets imbriqués complexes) :** Ne pas muter directement un objet imbriqué dans l'état (ex. `appState.user... = ...`), mais utiliser la déstructuration (spread operator `...`) pour créer de nouvelles références d'objets afin que React détecte le changement et re-rende le composant.
* **Erreur 3 (Dériver un état avec `useEffect`) :** Ne pas utiliser `useEffect` pour synchroniser un état dérivé (ce qui provoque des renders en cascade), mais dériver la valeur directement pendant le rendu ou utiliser un pattern adapté.
* **Erreur 4 (useState dans des conditions) :** Ne jamais placer un hook `useState` à l'intérieur d'une condition (`if`), car cela brise l'ordre des hooks React. Isoler le composant conditionnel dans un sous-composant si nécessaire.
* **Erreur 5 (Trop d'appels `useState` séparés) :** Pour des états liés qui sont toujours mis à jour en même temps, regrouper les données dans un seul objet d'état pour éviter les re-renders multiples et garder un code plus propre.
* **Erreur 6 (Valeurs calculées stockées dans `useState`) :** Ne pas créer un état séparé pour une valeur calculée à partir d'un autre état, mais calculer cette valeur directement à la volée (ou utiliser des méthodes dérivées) pour éviter les incohérences lors des resets.
* **Erreur 7 (Appels `setState` consécutifs multiples) :** Ne pas enchaîner plusieurs `setCount(count + 1)` en pensant incrémenter de plusieurs unités dans le même rendu (car l'état est asynchrone), mais utiliser une fonction de callback (`prev => prev + 1`) ou une fonction fléchée (`curr => curr + 1`).
* **Erreur 8 (Mutation directe d'un tableau) :** Ne pas utiliser des méthodes mutables comme `push` sur un tableau dans l'état, mais utiliser des méthodes immuables (spread, filter, etc.) pour garantir que React détecte le changement et déclenche le re-rendu.
* **Erreur 9 (Asynchronisme de `setState`) :** Ne pas s'attendre à ce que la valeur d'un état soit immédiatement mise à jour juste après un appel `setState` dans la même fonction synchrone ; utiliser un `useEffect` ou un événement synchronisé (`fire event`) si l'on souhaite réagir aux modifications.
* **Erreur 10 (Utilisation inutile de `useState` dans des formulaires) :** Pour des formulaires simples, éviter de créer un `useState` par champ (ce qui provoque un re-render à chaque frappe de touche), et préférer récupérer les données via `FormData` lors de la soumission.

4) **Chiffres de revenus annoncés :**
* Non précisé

---
