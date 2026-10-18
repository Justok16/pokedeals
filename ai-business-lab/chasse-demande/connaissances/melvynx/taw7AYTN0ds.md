# Je Regrette de ne PAS avoir connu ces 3 Tricks React AVANT

Vidéo : https://youtu.be/taw7AYTN0ds · durée 9:13 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Trois astuces essentielles en TypeScript avec React pour améliorer la robustesse, la maintenabilité et la typage des composants et des pages.
2) **Outils, sites ou dépôts GitHub cités :**
   - **TypeScript** (gratuit, surcouche typée de JavaScript)
   - **React** (gratuit, bibliothèque front-end)
   - **VS Code** (gratuit, éditeur de code source)
   - **Console Ninja** (gratuit/freemium, extension VS Code pour afficher les logs dans l'éditeur)
3) **Astuces concrètes et réutilisables :**
   - **Astuce n°1 :** Éviter d'utiliser `React.DetailedHTMLProps` ou de deviner les types natifs des éléments HTML pour les props de composants. Utiliser plutôt `ComponentPropsWithoutRef<'button'>` (ou l'élément HTML concerné) combiné à `forwardRef` et `useImperativeHandle` / `useRef` pour typer correctement les props d'un composant tout en gérant la `ref` sans erreur TypeScript.
   - **Astuce n°2 :** Remplacer l'utilisation de `React.ReactNode` ou `React.ReactElement` pour les enfants d'un composant par l'utilisation de `PropsWithChildren<T>`, ou mieux encore, exploiter la prop `children` native et la destructuration des props (`{ title, children }`) en typant les props avec `PropsWithChildren<T>` pour simplifier la syntaxe du composant (pattern `child run` / `props with children`).
   - **Astuce n°3 :** Utiliser les types génériques (`<T>`) pour typer les `params` et `searchParams` des pages (par exemple dans Next.js) en étendant `Record<string, string | string[] | undefined>`, ce qui permet d'éviter le type `any`, de garantir la sécurité du code et de bénéficier d'une autocomplétion précise.
4) **Chiffres de revenus annoncés :**
   - Non précisé.
