# Tu n’as PAS besoin de useCallback en React

Vidéo : https://youtu.be/5aFioB5N4gM · durée 10:34 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Démonstration expliquant pourquoi la majorité des utilisations du hook `useCallback` en React sont inutiles, inefficaces, voire contre-productives, et comment React gère le rendu des composants.
2) **Outils, sites ou dépôts GitHub cités** :
- **React** (bibliothèque JavaScript, framework front-end).
- **CodeSandbox** (sandbox de code en ligne pour les démos).
- **Shiki / Shikiki** (outil de coloration syntaxique de code).
3) **Astuces concrètes et réutilisables** :
- Ne pas utiliser `useCallback` par anticipation ou par prévention : la mémorisation de composants ou de fonctions ne sert à rien, sauf en cas de réels problèmes de performances (lenteurs mesurées, calculs très lourds, ou mémorisation stricte passée à un composant lourd enveloppé dans `React.memo`).
- Comprendre que si un composant parent se re-rend, les fonctions déclarées à l'intérieur sont recréées, ce qui est un comportement natif et extrêmement rapide en JavaScript moderne, sauf si le composant enfant est explicitement mémoïsé (`React.memo`).
- Utiliser `useEvent` (ou les patterns alternatifs) lorsqu'on a besoin de stabiliser une référence sans alourdir le code avec des tableaux de dépendances complexes.
4) **Chiffres de revenus annoncés** : Non précisé.
