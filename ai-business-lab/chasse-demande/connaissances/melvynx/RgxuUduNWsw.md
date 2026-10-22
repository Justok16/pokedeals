# TYPES ou INTERFACE en TypeScript?

Vidéo : https://youtu.be/RgxuUduNWsw · durée 8:26 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Comparaison détaillée entre **Type** et **Interface** en TypeScript. L'auteur analyse les performances, la syntaxe, la fusion de déclarations (*declaration merging*), l'héritage et la flexibilité pour déterminer quel outil utiliser au quotidien.
2) **Outils, sites ou dépôts GitHub cités :**
   - **TypeScript :** Superset de JavaScript.
   - **VS Code :** Éditeur de code.
3) **Astuces concrètes et réutilisables :**
   - Être **consistant** dans son code : utiliser une règle ESLint (`@typescript-eslint/consistent-type-definitions`) pour imposer soit `type`, soit `interface` dans tout le projet.
   - Utiliser les **interfaces** si vous avez besoin du *declaration merging* (fusion automatique de plusieurs interfaces portant le même nom).
   - Utiliser les **types** pour plus de flexibilité (unions, tuples, types primitifs, intersections complexes).
   - Privilégier l'utilisation des ` types` par défaut, sauf besoin spécifique (comme la fusion d'interfaces ou la programmation orientée objet avec `extends`).
4) **Chiffres de revenus annoncés :** Non précisé.
