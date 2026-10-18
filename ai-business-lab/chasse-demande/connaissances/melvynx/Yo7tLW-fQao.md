# forEach VS for VS for...of ? Lequel UTILISER (tu vas être surpris)

Vidéo : https://youtu.be/Yo7tLW-fQao · durée 7:50 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Comparer trois boucles en JavaScript (`for`, `for...of` et `forEach`) en termes de syntaxe, d'accès aux indices, de performance et de bonnes pratiques.

2) **Outils, sites ou dépôts GitHub cités** : Aucun outil payant ou site spécifique mentionné (utilisation de VS Code et d'un site de benchmarks de performance non nommé).

3) **Astuces concrètes et réutilisables** :
- Utiliser la boucle `for` classique ou `for...of` pour de meilleures performances par rapport à `forEach`.
- La boucle `for...of` ne donne pas directement accès à l'index (contrairement au `for` classique ou à `Object.entries()`), mais elle permet d'utiliser `break` ou `continue`.
- Éviter le chaînage excessif de méthodes de tableaux (`.filter().map().forEach()`) qui crée des boucles intermédiaires inutiles, au profit d'une boucle `for...of` unique avec des instructions `if/continue`.

4) **Chiffres de revenus annoncés** : Non précisé.

---
