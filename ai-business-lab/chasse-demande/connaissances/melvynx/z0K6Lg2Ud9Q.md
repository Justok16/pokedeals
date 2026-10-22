# J'ai fait le setup VPS le plus cheaté : je migre toutes mes apps à Netcup

Vidéo : https://youtu.be/z0K6Lg2Ud9Q · durée 16:30 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

### 1) Idée principale
L'auteur explique comment il a considérablement réduit ses coûts d'infrastructure (en passant de Vercel à Netcup pour ses VPS) afin de rendre l'hébergement de ses applications et services (comme son outil d'e-mailing Lumail.io) plus rentable, tout en maintenant une haute disponibilité et en automatisant la gestion des erreurs grâce à l'IA (Claude / Codex CLI).

---

### 2) Outils, sites et dépôts GitHub cités
* **Lumail.io** *(Payant / Inscription avec abonnement)* : Application d'e-mailing (l'auteur l'utilise pour ses campagnes et services d'e-mailing).
* **Vercel** *(Modèle freemium / payant)* : Plateforme cloud d'hébergement et de déploiement (juge jugée trop coûteuse à grande échelle pour l'e-mailing).
* **AWS SES (Simple Email Service)** *(Payant à l'usage)* : Service d'e-mailing cloud d'Amazon, utilisé avec Lumail.
* **Hetzner** *(Payant)* : Hébergeur VPS (jugé de plus en plus cher par l'auteur).
* **Netcup** *(Payant)* : Hébergeur VPS/webhosting allemand (choisi en remplacement de Hetzner pour ses tarifs très compétitifs).
* **Docker / Docker Desktop** *(Gratuit / Open-source)* : Outil de conteneurisation.
* **Beszel** *(Gratuit / Open-source)* : Outil de monitoring pour surveiller les ressources et performances des VPS (CPU, RAM, disque, etc.).
* **Dokploy** *(Gratuit / Open-source)* : Outil open-source de gestion de VPS et de déploiement d'applications.
* **Raycast** *(Gratuit avec options payantes)* : Lanceur d'applications pour macOS (utilisé pour des calculs rapides et commandes).
* **Cloudflare R2** *(Payant à l'usage)* : Stockage cloud objet, utilisé pour sauvegarder les VPS.
* **Uptime Kuma** *(Gratuit / Open-source)* : Outil de surveillance de disponibilité (uptime) des applications et des services.
* **Codex CLI / Codex (Agent IA)** *(Non précisé, probablement payant/API)* : Agent IA et script d'audit automatisé pour surveiller, diagnostiquer et corriger les erreurs sur les VPS.

---

### 3) Astuces concrètes et réutilisables
* **Migration vers des VPS économiques :** Remplacer des services cloud managés coûteux (comme Vercel pour certains workloads lourds) par des VPS dédiés (Netcup) gérés via **Dokploy** pour diviser les coûts d'infrastructure par deux tout en améliorant les performances matérielles.
* **Automatisation du monitoring et de l'audit par IA :** Mettre en place un script d'audit régulier (avec Codex) qui tourne à intervalles réguliers (toutes les 5 minutes ou via des vérifications quotidiennes) pour détecter et corriger automatiquement les pannes (erreurs 503, indisponibilité de sites) sans intervention humaine constante.
* **Séparation des environnements :** Conserver des environnements de prévisualisation (preview) sur des plateformes managées (comme Vercel à faible coût) pour le développement et les *Pull Requests*, tout en migrant la production lourde sur des VPS autohébergés (Netcup) pour éliminer les frais variables excessifs.
* **Centralisation des alertes :** Relier les notifications de build, les rapports de sauvegarde et les alertes de pannes à un canal Telegram dédié pour garder un œil sur la santé de l'infrastructure en temps réel.

---

### 4) Chiffres de revenus et coûts (affirmés par l'auteur)
* **Coût initial de l'application Lumail.io sur Vercel :** Près de **100 $ par mois** (*affirmé par l'auteur*).
* **Taille des campagnes d'e-mailing :** Jusqu'à **20 000 e-mails** par campagne (*affirmé par l'auteur*).
* **Ancien coût d'un serveur Hetzner pour la production :** **40 $ par mois** (*affirmé par l'auteur*).
* **Économie réalisée en changeant d'hébergeur :** Environ **60 $ à 70 $ d'économie par mois** par rapport à l'ancien hébergeur (*affirmé par l'auteur*).
* **Coût du serveur Netcup ciblé (RS 2000) :** Environ **24 $ par mois (24 €)** (*affirmé par l'auteur*).
* **Limite de trafic (bande passante) chez Netcup :** Jusqu'à **3 To en 24h** (puis *fair-use* illimité) (*affirmé par l'auteur*).
* **Abonnement de l'auteur sur Vercel (pour les environnements de preview) :** **20 $ par mois** (*affirmé par l'auteur*).
