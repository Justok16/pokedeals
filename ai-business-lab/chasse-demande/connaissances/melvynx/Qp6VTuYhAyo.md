# Ils ont résolu les plus GROS problèmes NextJS (v15)

Vidéo : https://youtu.be/Qp6VTuYhAyo · durée 12:37 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur présente les principales nouveautés et problématiques résolues par la version 15 Release Candidate (RC) de Next.js, en se focalisant particulièrement sur le système de cache et la gestion des exécutions asynchrones.

2) **Outils, sites ou dépôts GitHub cités :**
- **Next.js (version 15 RC) :** Framework React (open source/gratuit) permettant de créer des applications web, mis à jour pour modifier le comportement par défaut du cache et introduire de nouvelles méthodes.
- **Escalidraw :** Outil de dessin et de schématisation (gratuit) utilisé pour illustrer le fonctionnement du cache et du routage.
- **Prisma :** ORM (gratuit) utilisé pour la gestion de la base de données dans l'exemple de l'application de Todos.

3) **Astuces concrètes et réutilisables :**
- **Gérer le cache des requêtes Fetch :** Dans Next.js 15, les requêtes `fetch`, les `GET Route Handlers` et le cache du routeur client ne sont plus mis en cache par défaut, ce qui évite les comportements inattendus lors des redirections ou des mises à jour de données.
- **Utiliser l'option `after` (expérimentale) :** Permet d'exécuter du code JavaScript *après* l'envoi de la réponse au client (par exemple pour des tâches de journalisation, d'analytique ou d'autres appels externes) sans bloquer la réponse principale.
- **Structurer les applications avec des routes et des actions serveur claires :** Utiliser les bonnes méthodes de mutation et de revalidation (comme `router.refresh()` ou les nouvelles configurations de cache) pour maintenir les données à jour sans recharger inutilement toute la page.

4) **Chiffres de revenus annoncés :** Aucun chiffre de revenus n'est mentionné dans la vidéo.

---
