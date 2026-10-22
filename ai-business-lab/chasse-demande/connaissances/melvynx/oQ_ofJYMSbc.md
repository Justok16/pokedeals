# Utiliser Axios est il pertinent ?

Vidéo : https://youtu.be/oQ_ofJYMSbc · durée 2:34 · résumé Gemini (gemini-3.1-flash-lite, lot de 6) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur recommande de délaisser la bibliothèque Axios au profit d'UpFetch, car cette dernière est beaucoup plus légère, moderne et intègre des fonctionnalités avancées comme la validation de schémas.
2) **Outils :** 
- **Axios :** Gratuit (open source). Sert à effectuer des requêtes HTTP.
- **UpFetch :** Gratuit (open source). Sert à effectuer des requêtes HTTP avec une approche plus légère.
- **Zod :** Gratuit. Sert à la validation de schémas de données.
3) **Astuces :** Utiliser UpFetch pour réduire le bundle size, mettre en place une validation de schéma avec Zod pour garantir la sécurité des données reçues et utiliser les méthodes intégrées (`isResponseError`, `isValidationError`) pour une meilleure gestion des erreurs.
4) **Chiffres :** Non précisé.
