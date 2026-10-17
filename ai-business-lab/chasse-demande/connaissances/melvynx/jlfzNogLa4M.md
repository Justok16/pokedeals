# MON MAC N'EST PLUS MON SEUL OUTIL POUR CODER : je fais tout sur Linux via VPS, voici pourquoi

Vidéo : https://youtu.be/jlfzNogLa4M · durée 15:23 · résumé Gemini (gemini-3.5-flash-lite) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

### 1) Idée principale
L'auteur explique qu'il ne code plus sur son Mac personnel pour éviter de saturer sa RAM et son processeur. Il délègue toutes ses tâches de développement IA à un serveur distant (VPS) en utilisant un système qu'il a créé, nommé « Code OS ». Cela lui permet de coder en multi-projets, de lancer ses agents IA et de faire tourner ses applications à distance tout en économisant les ressources de son propre ordinateur.

### 2) Outils, sites et dépôts GitHub cités
* **Cursor** : Éditeur de code (et agent IA), payant (utilisation courante), sert à coder et manager les agents IA.
* **Cursor Codec / Claude Code / Claude Fable 5.1 High** : Modèles d'IA intégrés, payants (abonnements), utilisés pour le codage et les agents.
* **Code OS** : Projet personnel de l'auteur, gratuit (ressource partagée sous la vidéo), permet de configurer et gérer son VPS et ses applications à distance.
* **Lumal.io** : Le SaaS de l'auteur (outil d'e-mail marketing), modèle de tarification payant (Pro à 60 $/mois, Business à 200 $/mois), sert à envoyer des e-mails et tester le code IA.
* **Portly** : Outil headless supervisor (CLI Linux), gratuit, sert à lancer et superviser les serveurs et applications sur le VPS.
* **Cloudflare Tunnel** : Service de tunnel réseau, modèle non précisé (souvent gratuit de base), protège et sécurise l'accès aux sites et images.
* **GitHub** : Plateforme de gestion de code, gratuit/payant, sert à stocker les dépôts de code (ex. : `agents-config`).
* **Next.js** : Framework web (abandonné par l'auteur au profit de TanStack Start), open-source/gratuit, utilisé pour le front-end.
* **TanStack Start** : Framework web, open-source/gratuit, remplace Next.js pour de meilleures performances.
* **Excalidraw** : Outil de schématisation, gratuit/payant, sert à créer des diagrammes (ex. : le schéma de l'architecture VPS).
* **Tella / Tella-cli** : Outil de montage vidéo, payant, sert à réaliser des vidéos et du montage.
* **Neon** : Base de données, payant/gratuit (freemium), sert de base de données PostgreSQL pour les projets.
* **Postgres** : Système de gestion de base de données, open-source/gratuit.
* **NordVPN** : Service VPN, payant, sert à whitelister les IPs pour sécuriser l'accès aux ports du VPS.
* **CleanMyMac** : Application de nettoyage Mac, payant, sert à libérer de l'espace de stockage.

### 3) Astuces concrètes et réutilisables
* **Déléguer sur un VPS :** Ne pas faire tourner les agents IA de codage (Cursor, Claude) sur sa machine locale pour éviter de saturer le processeur et la mémoire, mais utiliser un serveur distant (VPS).
* **Centraliser avec un Command Center (Code OS) :** Regrouper tous ses projets, applications, statuts de ports, modifications Git et captures d'écran d'agents sur une seule interface web accessible en local ou à distance.
* **Whitelister les IPs :** Protéger les ports de développement sur le VPS en restreignant l'accès aux IPs autorisées (ou via un VPN) pour éviter les accès non désirés.
* **Automatiser les captures d'écran par l'IA :** Demander aux agents IA de faire des screenshots des pages sur lesquelles ils codent pour pouvoir les inspecter directement dans le chat et leur faire des retours visuels.
* **Synchroniser les compétences (Skills sync) :** Stocker et versionner les dossiers de compétences des agents (`.agents` ou `agents-config`) sur un dépôt GitHub privé pour les conserver et les réutiliser facilement.
* **Utiliser des worktrees Git :** Travailler sur plusieurs branches simultanément en isolant les environnements de travail pour chaque tâche.

### 4) Chiffres de revenus annoncés
* **Non précisé** (aucun chiffre de chiffre d'affaires ou de bénéfice n'est mentionné dans la vidéo).
