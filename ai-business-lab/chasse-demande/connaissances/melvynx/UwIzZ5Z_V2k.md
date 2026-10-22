# Pourquoi il ne faut PAS utiliser les enum TypeScript

Vidéo : https://youtu.be/UwIzZ5Z_V2k · durée 8:32 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

- **Idée principale :** Pourquoi l'utilisation des énumérations (`enum`) en TypeScript est une mauvaise pratique et quelles sont les meilleures alternatives basées sur les objets et les types littéraux.
- **Outils, sites ou dépôts GitHub cités :**
  - **TypeScript :** Langage de programmation open-source gratuit.
  - **Visual Studio Code (VS Code) :** Éditeur de code gratuit.
  - **Radix UI / Tailwind CSS :** Bibliothèques UI et CSS open-source gratuites (visibles à l'écran).
- **Astuces concrètes et réutilisables :**
  - Éviter d'utiliser les `enum` en TypeScript car ils génèrent du code JavaScript additionnel complexe et peuvent causer des incohérences de typage et de valeurs numériques implicites.
  - **Alternative 1 (Objet as const) :** Définir un objet de constantes figées avec `as const` et extraire son type avec `type MonType = (typeof MonObjet)[keyof typeof MonObjet]` pour obtenir un union type strict de chaînes de caractères.
  - **Alternative 2 (Union de types littéraux) :** Définir directement un type union de chaînes (ex: `type TaskStatus = 'Pending' | 'InProgress' | 'Completed'`) pour un typage plus propre, prévisible et sans artefacts JavaScript superflus.
  - Mapper un objet de type `as const` avec `.map()` pour générer dynamiquement des tableaux d'objets JSON propres (avec `name` et `status`) sans les problèmes inhérents aux enums.
- **Chiffres de revenus annoncés :** Non précisé.
