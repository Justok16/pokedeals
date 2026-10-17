# NextJS : Server Actions, Ne les Utilises PAS comme ça (VS API Routes)

Vidéo : https://youtu.be/kIhdI9Fsp-w · durée 13:06 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : La vidéo explique les différences fondamentales, les cas d'usage et les pièges à éviter entre les **Server Actions** et les **API Routes** dans Next.js, tout en démontrant comment les utiliser efficacement avec l'aide de l'IA (Cursor).
2) **Outils, sites ou dépôts GitHub cités** :
   - **Next.js** : Framework React (gratuit).
   - **Prisma** : ORM pour base de données (gratuit).
   - **Cursor** : Éditeur de code assisté par IA (gratuit/payant).
   - **mlv.sh/ai** : Lien vers une formation sur l'utilisation de l'IA pour les développeurs (non précisé).
3) **Astuces concrètes et réutilisables** :
   - Réserver les **Server Actions** strictement aux mutations de données (écritures, mises à jour) initiées depuis le front-end de la même application, et non pour du *data fetching* (requêtes en lecture seule).
   - Utiliser les **API Routes** (endpoints HTTP classiques) lorsque l'application doit exposer des routes accessibles par des clients externes (applications mobiles, autres services tiers).
   - Toujours valider et sécuriser les données reçues en paramètre dans les Server Actions, car le front-end peut envoyer n'importe quel type de données.
4) **Chiffres de revenus annoncés** :
   - Non précisé.
