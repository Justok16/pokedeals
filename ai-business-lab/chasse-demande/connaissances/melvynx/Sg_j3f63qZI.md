# LA DIFFÉRENCE ENTRE TARGET ET CURRENT TARGET EN WEB

Vidéo : https://youtu.be/Sg_j3f63qZI · durée 9:48 · résumé Gemini (gemini-3.1-flash-lite-preview, lot de 2) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo explique la différence technique entre les propriétés `target` et `currentTarget` lors de la gestion des événements DOM en JavaScript/React, ainsi que le cycle de vie des événements (phases de capture et de bouillonnement).

2) **Outils, sites ou dépôts GitHub cités** :
*   **CodeSandbox** (gratuit) : Plateforme utilisée pour illustrer les exemples de code et démontrer les différences entre `target` et `currentTarget`.
*   **tldraw** (gratuit) : Outil utilisé pour visualiser le schéma du cycle de vie des événements (capture, target, bubble).

3) **Astuces concrètes et réutilisables** :
*   Utiliser `currentTarget` pour identifier l'élément sur lequel l'événement est attaché (l'élément qui "écoute"), alors que `target` identifie l'élément qui a été réellement cliqué (la source).
*   Comprendre le cycle de vie des événements en trois étapes : 1) La phase de **capture** (l'événement descend de `window` vers l'élément cible), 2) La phase de **target** (l'événement atteint l'élément cliqué), et 3) La phase de **bubble** (l'événement remonte vers `window`).
*   Le paramètre `useCapture` dans `addEventListener` : réglé sur `true`, il permet d'intercepter l'événement lors de la phase de capture.

4) **Chiffres de revenus** : Aucun revenu n'est mentionné (non précisé).

---
