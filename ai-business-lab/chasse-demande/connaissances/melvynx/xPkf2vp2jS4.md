# Je n'ai PLUS BESOIN d’Express pour mon Backend

Vidéo : https://youtu.be/xPkf2vp2jS4 · durée 28:12 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** L'auteur explique que Next.js est un véritable framework full-stack (backend et frontend) et qu'il n'est pas nécessaire de configurer un serveur Node.js séparé (comme Express ou Fastify) pour des projets personnels ou de taille moyenne. Il démontre comment gérer l'authentification, les bases de données et les requêtes directement dans Next.js via Server Actions.

2. **Outils, sites ou dépôts cités :**
- **Next.js** : Framework React open source, gratuit.
- **Docker** : Outil de conteneurisation, gratuit.
- **Node.js** : Environnement d'exécution JavaScript, gratuit.
- **Express**, **Fastify**, **NestJS** : Frameworks backend (présentés comme superflus pour certains projets avec Next.js), gratuits.
- **Excalidraw** (*app.excalidraw.com*) : Outil de dessin et de schématisation, gratuit.
- **Prisma** : ORM pour base de données, gratuit.
- **PostgreSQL** : Système de gestion de base de données, gratuit.
- **NextAuth** / **Clerk** / **Supabase** : Outils d'authentification, gratuits/freemium.
- **Trigger.dev** : Service de gestion de tâches de fond (CRON jobs), gratuit/freemium.
- **Ably** (*ably.com*) : Service de web-sockets, gratuit/freemium.
- **next-safe-action** (*next-safe-action.dev*) : Bibliothèque pour sécuriser les Server Actions avec validation de type, gratuite.

3. **Astuces concrètes et réutilisables :**
- Utiliser la directive `"use server"` au sommet des fonctions pour exécuter du code côté serveur directement depuis les composants React.
- Gérer l'authentification avec `auth()` de NextAuth pour bloquer l'accès aux pages non autorisées et retourner des composants d'alerte (`<Alert>`).
- Utiliser `revalidatePath('/todos')` et `redirect('/todos')` dans les Server Actions pour rafraîchir les données et rediriger l'utilisateur après une modification en base de données.
- Valider les données de formulaires avec une bibliothèque de schéma (comme Zod) dans les Server Actions pour garantir la sécurité et le typage.

4. **Chiffres de revenus annoncés :**
- Non précisé.
