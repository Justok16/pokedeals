# 10 BONNES PRATIQUES Pour Avoir un CODE PROPRE EN JavaScript

Vidéo : https://youtu.be/XmC7v6Njio0 · durée 6:45 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Présentation de 7 règles de *Clean Code* applicables en JavaScript pour écrire un code plus propre, lisible et maintenable.

2) **Outils, sites ou dépôts GitHub cités** :
- Dépôt GitHub : `clean-code-javascript` (gratuit, référentiel de bonnes pratiques).

3) **Astuces concrètes et réutilisables** :
- **Règle 1** : Éviter les « magic values » (nombres ou chaînes bruts non explicites) et utiliser des constantes nommées (ex: `MILLISECONDS_IN_A_DAY`).
- **Règle 2** : Éviter le « magic index » (récupérer des éléments par leur indice dans un tableau comme `result[2]`), préférer la déstructuration (ex: `const [, domain] = ...`).
- **Règle 3** : Gérer les valeurs par défaut proprement (préférer l'opérateur de coalescence des nuls `??` plutôt que des vérifications complexes).
- **Règle 4** : Ne pas passer trop de paramètres dans une fonction (maximum 3 ou regrouper dans un objet).
- **Règle 5** : S'assurer qu'une fonction ne fait qu'une seule chose (séparer la logique de récupération de données de la logique de suppression).
- **Règle 6** : Ne pas ajouter de drapeaux (*flags*) booléens en paramètres pour modifier le comportement d'une fonction, créer deux fonctions distinctes.
- **Règle 7** : Écrire des fonctions pures et éviter de modifier des variables situées en dehors de leur scope (*side effects*).

4) **Chiffres de revenus annoncés** : Non précisé.

---
