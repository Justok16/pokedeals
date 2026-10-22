# Pourquoi les Développeurs sont Essentiels

Vidéo : https://youtu.be/XrobPI4gKw0 · durée 2:33 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Explication des limites de l'architecture serverless (Next.js, AWS SNS, Database, Cloudflare R2) face à un volume massif d'événements et de la nécessité de mettre en place une file d'attente (queue) d'événements pour éviter les plantages.
2) **Outils, sites ou dépôts GitHub :**
- **Lumail.io :** application SaaS de l'auteur (payante/abonnement, gérant l'envoi d'e-mails et de newsletters).
- **Next.js Serverless :** framework (gratuit/open source, utilisé pour le serveur principal).
- **AWS SNS :** service d'événements Amazon (utilisé pour créer des événements lors de l'envoi d'e-mails).
- **R2 Cloudflare :** service de stockage de données (utilisé pour stocker temporairement le contenu des e-mails).
3) **Astuces concrètes et réutilisables :**
- Stocker temporairement les contenus lourds (comme les e-mails) dans un service de stockage (ex. Cloudflare R2) pendant 30 jours avant suppression automatique pour éviter de saturer la base de données.
- Utiliser un système combinant des événements et une file d'attente (`events` et `queue`) pour regrouper les écritures (par exemple, attendre 1000 événements avant d'effectuer une seule écriture en base de données) afin de préserver la connexion de la base de données.
4) **Chiffres de revenus annoncés :** Non précisé.
