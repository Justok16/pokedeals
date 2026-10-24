# Je ne touche plus jamais à mes DNS (Claude le fait sur Cloudflare)

Vidéo : https://youtu.be/01sWd0EoQWQ · durée 4:53 · résumé Gemini (gemini-3-flash-preview, lot de 3) du 2026-10-24
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **L'idée principale** : Utiliser la plateforme Cloudflare pour déployer, gérer et sécuriser des sites web de manière automatisée (notamment via un agent IA), en profitant d'outils souvent gratuits ou à prix coûtant.

2) **Outils, sites ou dépôts cités** :
*   **Cloudflare** (cloudflare.com) : Plateforme globale pour l'hébergement, la gestion de domaines et la sécurité. (Gratuit pour commencer).
*   **Workers** : Service de déploiement d'applications sans serveur. (Gratuit jusqu'à 100 000 requêtes par jour ; à partir de 5 $/mois au-delà).
*   **DNS** : Gestionnaire de noms de domaine. (Proposé à prix coûtant, sans marge bénéficiaire de la part de Cloudflare).
*   **Proxy (Nuage orange)** : Filtre de trafic pour protéger le site des bots et attaques. (Inclus dans Cloudflare).
*   **R2** : Stockage de fichiers (images, vidéos, PDF). (10 Go gratuits, puis paliers à partir de 5 $/mois).
*   **CLI CF** : Interface de ligne de commande officielle de Cloudflare. (Outil gratuit).
*   **Claude** (mentionné comme agent IA) : Utilisé pour piloter Cloudflare via le CLI.

3) **Astuces concrètes et réutilisables** :
*   Connecter un agent IA (comme Claude) au CLI de Cloudflare pour automatiser la configuration des DNS (MX, TXT records) et éviter de le faire manuellement.
*   Activer le "Proxy" (l'icône du nuage orange) pour que tout le trafic passe par Cloudflare, permettant de filtrer les bots pirates et les robots d'IA indésirables.
*   Utiliser Cloudflare pour gérer la redirection d'emails professionnels vers une adresse Gmail personnelle afin de centraliser sa gestion.

4) **Chiffres de revenus** : Aucun chiffre de revenu (affirmé par l'auteur).
