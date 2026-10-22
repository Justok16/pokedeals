# C'est la fin des développeurs backend - Server component 🤯

Vidéo : https://youtu.be/HSI2btKDmgY · durée 11:20 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Analyse de l'impact des Server Components et de Next.js sur le rôle des développeurs front-end et back-end, expliquant pourquoi le développement front-end intègre de plus en plus de logique serveur (sans pour autant tuer le métier de back-end).
2) **Outils, sites ou dépôts GitHub cités :**
- **Next.js :** Gratuit (open source). Framework React permettant d'intégrer des Server Components et d'exécuter du code côté serveur.
- **React :** Gratuit. Bibliothèque JavaScript.
- **Prisma :** Gratuit. ORM pour interagir avec la base de données.
- **Remix :** Gratuit (open source). Framework web pour React illustrant la gestion du chargement des données.
- **Roadmap.sh :** Gratuit. Site web proposant des feuilles de route pour les compétences de développeur front-end et back-end.
3) **Astuces concrètes et réutilisables :**
- Utiliser les Server Components dans Next.js pour effectuer des requêtes directement côté serveur dans les composants React (ex: `prisma.lesson.findUnique`).
- Gérer l'authentification, les bases de données et les endpoints API directement dans l'architecture front-end (via des fichiers API handlers ou des fonctions async dans les composants de page) pour simplifier les flux de données.
- Comprendre que le front-end récupère exactement les données nécessaires sans passer systématiquement par des allers-retours complexes avec un back-end séparé, tout en maintenant le typage (TypeScript).
4) **Chiffres de revenus annoncés :** Non précisé.
