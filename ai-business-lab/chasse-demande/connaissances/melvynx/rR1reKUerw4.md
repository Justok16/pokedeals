# On a HACKÉ mon clone de R/PLACE

Vidéo : https://youtu.be/rR1reKUerw4 · durée 14:13 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

- **Idée principale :** Récit du projet de clonage du site collaboratif *r/place* en JavaScript pur avec WebSockets, victime d'un piratage/attaque de bots, et explications techniques sur le fonctionnement des WebSockets.
- **Outils, sites ou dépôts GitHub cités :**
  - **JavaScript :** Langage de programmation gratuit.
  - **GitHub :** Plateforme gratuite de gestion de code source.
  - **Railway :** Service d'hébergement cloud (freemium/payant).
  - **Vercel :** Plateforme de déploiement cloud (freemium/payant).
  - **Render :** Service d'hébergement (mentionné ou utilisé pour le déploiement).
  - **ChatGPT / OpenAI :** Outil d'assistance payant/freemium.
- **Astuces concrètes et réutilisables :**
  - Utiliser les **WebSockets** pour créer une connexion bidirectionnelle en temps réel (tunnel persistant) entre le client et le serveur, contrairement aux requêtes HTTP unidirectionnelles classiques (API REST).
  - Stocker la correspondance des connexions (`Map`) associant l'IP et le `user-agent` au `socket.id` pour identifier les clients.
  - Mettre en place un mécanisme de limitation de taux (*rate limiting* / *debounce* basé sur le timestamp du dernier clic, ex: minimum 500 millisecondes entre chaque action) pour contrer le spam et les bots sur un canvas partagé.
  - Maintenir un compteur d'utilisateurs connectés en temps réel en émettant des événements via les sockets.
- **Chiffres de revenus annoncés :** Non précisé.
