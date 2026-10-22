# Focus sur les permissions dans ma boilerplate.

Vidéo : https://youtu.be/6Cps63V-1Lc · durée 2:25 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur explique comment limiter les accès à certaines fonctionnalités en fonction d'un rôle dans une application en utilisant l'Access Control (statements) avec une bibliothèque, et montre la gestion conditionnelle des boutons d'action (comme delete) selon les permissions des utilisateurs (admin vs member).
2) **Outils, sites ou dépôts cités :**
   - **NOW.TS :** Non précisé (plateforme/formation de l'auteur proposant des cours sur la gestion des organisations, des accès, des tests automatiques et l'utilisation de Cursor).
3) **Astuces concrètes et réutilisables :**
   - Utiliser des déclarations d'accès (statements) basées sur des rôles (ex. `user`, `admin`) pour conditionner l'affichage des boutons d'action dans l'interface (comme afficher ou masquer le bouton de suppression).
   - Structurer les permissions dans le code (via une structure de type `AuthPermissionSchema`) pour sécuriser les actions CRUD.
4) **Chiffres de revenus annoncés :** Aucun chiffre de revenus n'est annoncé.
