# Zod V4 résout le plus gros problème de Zod (+ pleins de nouveauté)

Vidéo : https://youtu.be/o6jz9C0ztyg · durée 19:44 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Présentation des principales nouveautés de Zod V4 (mise à jour après 4 ans), comparaison des performances, de la taille des "bundles" avec d'autres bibliothèques (Valibot) et introduction de nouvelles fonctionnalités comme `@zod/mini`, `z.jsonSchema()` et `z.interface()`.
2) **Outils, sites ou dépôts GitHub cités :**
- **Zod** (bibliothèque de validation TypeScript) : Gratuit (Open Source), sert à valider et structurer des données.
- **Valibot** (bibliothèque de validation alternative) : Gratuit (Open Source), comparé pour sa taille de bundle plus légère et son support du tree-shaking.
- **TypeScript / VS Code** : Outils de développement mentionnés pour l'analyse des types.
3) **Astuces concrètes et réutilisables :**
- Utiliser `@zod/mini` pour bénéficier du tree-shaking et réduire la taille du bundle en n'important que les méthodes nécessaires.
- Utiliser `z.jsonSchema()` pour convertir automatiquement un schéma Zod en JSON Schema (utile pour des intégrations avec des SDK d'IA comme Vercel).
- Utiliser `z.interface()` pour définir des schémas d'objets avec typage récursif sans avoir à typer manuellement des types intermédiaires.
4) **Chiffres de revenus annoncés :**
- Non précisé.
