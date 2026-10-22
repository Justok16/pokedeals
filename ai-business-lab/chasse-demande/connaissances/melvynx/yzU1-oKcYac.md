# 7 Questions React À ABSOLUMENT SAVOIR pour ton Entretien

Vidéo : https://youtu.be/yzU1-oKcYac · durée 14:15 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur teste des dizaines d'entretiens techniques React et interroge des recruteurs pour identifier les 7 questions les plus complexes et pièges posées en entretien, afin d'aider les développeurs à réussir leurs entretiens techniques haut la main.

2) **Outils, sites ou dépôts GitHub cités :**
- **React / ReactDOM :** Bibliothèque JavaScript (open source/gratuit).
- **Visual Studio Code (VS Code) :** Éditeur de code (gratuit).
- **GitHub :** Plateforme de code (gratuite).
- **Codeline :** Plateforme de formation de l'auteur (payante) pour maîtriser React.
- **TanStack Query (React Query) / useSWR :** Bibliothèques de gestion d'état et de fetching (open source/gratuit).
- **Zustand :** Gestionnaire d'état global (open source/gratuit).
- **Storyset :** Bibliothèque d'illustrations (gratuite).

3) **Astuces concrètes et réutilisables :**
- **Maîtriser les Portails (`ReactDOM.createPortal`) :** Savoir rendre un composant en dehors du DOM parent direct (ex: modales).
- **Comprendre le JSX en profondeur :** Le JSX est transformé en appels `React.createElement` et ne doit pas être confondu avec du HTML brut.
- **Saisir le pattern HOC (Higher-Order Component) :** Utile pour envelopper un composant et réutiliser de la logique (comme l'authentification).
- **Éviter le Props Drilling et utiliser le Context ou Zustand :** Savoir gérer le flux de données (dataflow) proprement dans une application React de grande envergure.
- **Préférer l'opérateur ternaire (`? :`) à l'opérateur logique `&&` pour les conditions en JSX :** Évite l'affichage inattendu de `0` lorsque la condition est évaluée à un nombre.
- **Utiliser TanStack Query ou `use` (React 19) pour le fetching de données :** Évite les pièges liés au mauvais usage de `useEffect` (absence de nettoyage, requêtes en doublon, etc.).

4) **Chiffres de revenus annoncés :** Aucun chiffre de revenus n'est mentionné dans la vidéo.
