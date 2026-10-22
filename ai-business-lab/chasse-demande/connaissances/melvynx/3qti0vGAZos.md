# TUTO / COURS pour SÉCURISER ton application en NextJS !

Vidéo : https://youtu.be/3qti0vGAZos · durée 16:06 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Sécuriser une application Next.js en gérant l'authentification et les autorisations (accès aux pages et aux données selon l'état de connexion de l'utilisateur).

2) **Outils, sites ou dépôts cités** :
- **Next.js** : Framework web (gratuit).
- **Better Auth** : Bibliothèque d'authentification (gratuit).
- **GitHub** : Fournisseur d'authentification OAuth (gratuit).

3) **Astuces concrètes et réutilisables** :
- Utiliser la fonction `await getUser()` pour vérifier si un utilisateur est connecté avant d'afficher du contenu spécifique.
- Créer une méthode de protection de page (`getRequiredUser`) qui redirige ou lève une erreur ("Unauthorized") si l'utilisateur n'est pas authentifié.
- Filtrer les requêtes de base de données en incluant le `userId` pour garantir que chaque utilisateur ne récupère que ses propres données.
- Mettre en place un Middleware Next.js pour intercepter les requêtes sur des routes protégées (comme `/dashboard`) et rediriger vers la page de connexion si nécessaire.

4) **Chiffres de revenus annoncés** :
- Non précisé.

---
