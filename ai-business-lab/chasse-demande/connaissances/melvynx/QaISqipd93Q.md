# 3 Erreur à ABSOLUMENT Éviter en React useState !

Vidéo : https://youtu.be/QaISqipd93Q · durée 9:49 · résumé Gemini (gemini-3.1-flash-lite-preview, lot de 2) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo traite de la gestion optimisée des états (`state`) dans une application React, en expliquant pourquoi il faut éviter de centraliser tous les états dans les composants parents (ce qui provoque des rendus inutiles) et comment "refactoriser" pour placer le `state` au plus proche de son utilisation.

2) **Outils, sites ou dépôts GitHub cités** :
*   **React** (gratuit) : Bibliothèque JavaScript utilisée pour la construction de l'interface.
*   **BeginReact.dev** (payant) : Plateforme de formation proposée par l'auteur (masterclass sur React).

3) **Astuces concrètes et réutilisables** :
*   Éviter les "Global States" inutiles : si un état n'est utilisé que par un composant enfant, il doit être défini dans cet enfant plutôt que dans le parent pour éviter les rendus superflus de toute l'application.
*   "Lifting state down" : déplacer le `state` au niveau du composant qui l'utilise réellement.
*   Utiliser des fonctions de rappel (`callbacks`) pour faire remonter des informations du composant enfant vers le parent si nécessaire.
*   Utiliser `useEffect` de manière pertinente et non pour gérer des side-effects qui peuvent être encapsulés dans des fonctions de gestionnaires d'événements (ex: `onSubmit`).

4) **Chiffres de revenus** : Aucun revenu n'est mentionné (non précisé).
