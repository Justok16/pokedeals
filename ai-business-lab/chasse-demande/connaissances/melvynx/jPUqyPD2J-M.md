# Si tu utilises pas ça, arrête d'utiliser TypeScript !

Vidéo : https://youtu.be/jPUqyPD2J-M · durée 8:09 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Explication des limites et des risques du typage `any` (ou de l'assertion forcée `as Promise<User>`) lors de requêtes `fetch` en TypeScript, et présentation de la bibliothèque **Zod** pour valider et parser les données reçues d'une API de manière sûre et type-safe.

2) **Outils, sites ou dépôts GitHub cités** :
   - **TypeScript** : Gratuit, langage de programmation.
   - **Zod** : Gratuit (open source), bibliothèque de déclaration et de validation de schémas pour TypeScript/JavaScript.
   - **JSONPlaceholder** : Gratuit, API de test en ligne (utilisée dans l'exemple de code : `https://jsonplaceholder.typicode.com/users`).

3) **Astuces concrètes et réutilisables** :
   - Éviter d'utiliser `as User` ou `any` aveuglément après un `res.json()`, car TypeScript croira le type sans vérifier la réalité des données renvoyées par le serveur (ce qui provoque des plantages en cas de non-correspondance).
   - Importer Zod (`import { z } from 'zod'`) pour définir un schéma de validation rigoureux (ex: `z.object({ id: z.number(), name: z.string(), email: z.string().email() })`).
   - Utiliser la méthode `.parse()` ou `.safeParse()` sur les données brutes du JSON pour valider leur structure à l'exécution avant de les injecter dans l'état de l'application.
   - Gérer proprement les erreurs de validation levées par Zod (`ZodError`) dans un bloc `catch` pour identifier immédiatement les écarts entre le type attendu et les données reçues de l'API.

4) **Chiffres de revenus annoncés** :
   - Non précisé.

---
