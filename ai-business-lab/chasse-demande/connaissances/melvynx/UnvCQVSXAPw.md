# Apprendre le JSX en React en juste 5 MINUTES

Vidéo : https://youtu.be/UnvCQVSXAPw · durée 5:43 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Expliquer en 5 minutes et en français ce qu'est le JSX (qui n'est ni du HTML ni du JavaScript mélangé à du HTML, mais *juste du JavaScript* transformé en appels `React.createElement` par Babel), comment il fonctionne sous le capot (Virtual DOM, syntaxe, objets JS, props, children, ternaires et boucles `.map`), et proposer une formation interactive.

2) **Outils, sites et dépôts GitHub cités** :
* **Babel** : Transpilateur JavaScript (gratuit / open-source).
* **React / React DOM** : Bibliothèque JavaScript pour interfaces utilisateur (gratuit / open-source).
* **Chrome** : Navigateur web (gratuit).
* **Masterclass React de l'auteur** (`mlv.sh/react` / `iblueprint.dev`) : Plateforme de formation interactive de l'auteur (payant).

3) **Astuces concrètes et réutilisables** :
* Comprendre que le JSX est simplement du sucre syntactique : `<div title="Hey !">P !</div>` se traduit directement en `React.createElement("div", { title: "Hey !" }, React.createElement("p", null, "P !"))`.
* Utiliser les accolades `{}` dans le JSX comme une « porte d'entrée » pour injecter du code JavaScript classique (variables, ternaires, fonctions).
* Pour afficher des listes dynamiques, utiliser la méthode `.map()` sur un tableau en retournant des éléments JSX dotés d'une prop `key` unique.

4) **Chiffres de revenus annoncés** :
* Aucun chiffre de revenus n'est annoncé dans cette vidéo.
