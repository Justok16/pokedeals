# Le CSS en 2024 a changé : il ne sera plus jamais pareil

Vidéo : https://youtu.be/-XXRlMn04Dk · durée 11:24 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Présentation des dernières évolutions majeures de CSS et de l'UI web présentées lors de Google I/O 2024, qui remplacent de nombreuses bibliothèques JavaScript complexes par du CSS natif et puissant (animations au scroll, view transitions, popovers, anchor positioning, field-sizing: content, et align-content).

2) **Outils, sites et dépôts GitHub cités :**
- **Google Chrome / Google I/O 2024** (navigateur et événement gratuits) : Source des nouveautés CSS présentées.
- **CodePen** (plateforme gratuite/payante) : Utilisée pour tester et montrer les exemples de code (liens vers des démos de développeurs comme `codepen.io/melwynx`).
- **Framer Motion** (bibliothèque JavaScript payante/gratuite) : Bibliothèque d'animation pour React, comparée aux nouvelles animations CSS natives.
- **SWR** (bibliothèque open-source gratuite de Vercel) : Mentionnée dans la conclusion pour le data fetching.
- **TanStack Query** (bibliothèque open-source gratuite) : Mentionnée dans la conclusion comme alternative.

3) **Astuces concrètes et réutilisables :**
- **Animations au scroll :** Utiliser `animation-timeline: scroll()` et `animation-range` pour animer des éléments lors du défilement sans JavaScript.
- **View Transitions :** Utiliser `view-transition-name` et `document.startViewTransition()` pour animer la transition d'un élément d'une position à une autre de manière fluide entre deux états ou pages.
- **Popovers :** Utiliser l'attribut `popover` combiné avec `anchor-name` et `position-anchor` (Anchor Positioning) pour positionner facilement des infobulles (tooltips) par rapport à un élément déclencheur sans calculs complexes.
- **Field-sizing: content :** Utiliser cette propriété CSS sur les `textarea` ou `input` pour qu'ils s'agrandissent ou se réduisent automatiquement en fonction du contenu saisi.
- **Align-content en block layout :** Utiliser `align-content: center` pour centrer verticalement des éléments dans un bloc sans avoir à utiliser obligatoirement `display: flex`.

4) **Chiffres de revenus annoncés :**
- Non précisé.
