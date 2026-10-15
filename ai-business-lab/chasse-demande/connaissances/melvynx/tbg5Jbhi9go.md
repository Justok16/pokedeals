# Authentification : Le Guide Complet pour comprendre l'authentification Web

Vidéo : https://youtu.be/tbg5Jbhi9go · durée 17:52 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** Comprendre le fonctionnement de l’authentification et de la session (notamment l’utilisation de cookies et de tokens) dans le développement web, à travers différents types d’authentification (email/mot de passe, 2FA, magic-link, OAuth2, passkeys).
2. **Outils, sites ou dépôts GitHub cités :**
   - **Prisma Studio** (ou **Prisma**) : outil de gestion/visualisation de base de données (gratuit / open-source, utilisé pour la démo technique).
   - **Cursor** (ou **Cursor IDE**) : éditeur de code (gratuit / freemium).
3. **Astuces concrètes et réutilisables :**
   - Ne jamais stocker les mots de passe en clair dans la base de données, mais stocker un **hash** (généré avec un secret).
   - Utiliser des **tokens de session** stockés dans des **cookies** (avec des attributs sécurisés) pour éviter de redemander les identifiants à chaque requête.
   - Privilégier les méthodes d’authentification modernes (OAuth2, Magic Link, Passkeys) selon le niveau de sécurité et d’expérience utilisateur souhaité.
4. **Chiffres de revenus annoncés :** Non précisé.
