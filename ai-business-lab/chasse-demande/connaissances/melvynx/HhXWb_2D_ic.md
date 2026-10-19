# Créer Des Toasts Serveur Avec Now.ts

Vidéo : https://youtu.be/HhXWb_2D_ic · durée 1:24 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Implémentation d'une Server Action avec `server-toast` pour afficher des notifications (toasts) persistantes basées sur des cookies, permettant de conserver les messages même après des actions de formulaire.
2) **Outils, sites ou dépôts cités :**
- **BuildUI** : Plateforme ou ressource de formation (payante/mentionnée comme formation de l'auteur) expliquant comment créer ce type de fonctionnalités.
- **ServerAction** (Next.js) : Méthode serveur native (gratuite).
3) **Astuces concrètes et réutilisables :**
- Utiliser des Server Actions associées à un cookie (`toast-id`) pour stocker les messages de notification pendant 1 jour.
- Récupérer les cookies côté serveur/client dans un `toasti-toaster` pour parser les toasts et les supprimer (`cookieStore.delete`) lors du dismiss.
4) **Chiffres de revenus :** Non précisé.
