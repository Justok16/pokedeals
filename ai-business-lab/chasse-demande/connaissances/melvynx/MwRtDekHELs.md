# Comment Sécuriser les Server Actions en NextJS : la solution

Vidéo : https://youtu.be/MwRtDekHELs · durée 14:59 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur met en garde les développeurs utilisant Next.js et Prisma contre une faille de sécurité critique liée aux Server Actions, où les requêtes HTTP (comme les suppressions) ne valident pas correctement l'identité ou les permissions de l'utilisateur. Il présente la bibliothèque open-source `next-safe-action` pour sécuriser ces actions à l'aide de Zod.

2) **Outils, sites ou dépôts GitHub cités :**
- **JustCode (Application de démo) :** Non précisé (gratuit dans le cadre du tutoriel), application utilisée pour illustrer la faille de suppression de cours.
- **HTTPie (ou autre client HTTP) :** Non précisé (gratuit), outil pour simuler des requêtes POST et exploiter l'API de suppression.
- **GitHub / Documentation `next-safe-action` :** Gratuit, bibliothèque TypeScript open-source pour sécuriser les Server Actions avec Zod.
- **Zod :** Gratuit, bibliothèque de validation de schémas.

3) **Astuces concrètes et réutilisables :**
- Toujours valider et authentifier l'utilisateur (`getSession`) à l'intérieur des Server Actions, plutôt de faire confiance aveuglément aux données envoyées par le client.
- Utiliser `next-safe-action` pour définir des schémas Zod sur les Server Actions, garantissant un typage strict et rejetant automatiquement les requêtes non valides ou non authentifiées.
- Créer un client d'action sécurisé (`createSafeActionClient`) intégrant un middleware d'authentification pour factoriser la vérification des sessions.

4) **Chiffres de revenus annoncés :**
- Non précisé.

---
