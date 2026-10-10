# Pourquoi j'ai arrêté d'utiliser NPM pour PNPM et POURQUOI tu devrais AUSSI !

Vidéo : https://youtu.be/mpxotS_9Dzc · durée 15:28 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo demandée :

### 1) Idée principale
La vidéo critique l'utilisation de **NPM** comme gestionnaire de paquets en raison de sa lenteur, de sa propension à consommer beaucoup d'espace disque et de sa mauvaise gestion des dépendances redondantes, tout en présentant **PNPM** comme une alternative nettement plus rapide et optimisée grâce à l'utilisation de liens symboliques (*symlinks*) et de disques partagés (*storage*).

---

### 2) Outils, sites et dépôts GitHub cités
* **NPM** : Gestionnaire de paquets officiel de Node.js (gratuit). Sert à installer et gérer les dépendances.
* **Yarn** : Gestionnaire de paquets alternatif développé par Facebook (gratuit). Plus rapide que NPM, inclus dans Corepack.
* **PNPM** : Gestionnaire de paquets alternatif, open source, soutenu par la société *BIT* (gratuit). Plus rapide, utilise des liens symboliques pour stocker les fichiers de manière unique sur le disque.
* **Corepack** : Outil natif de Node.js (gratuit) pour gérer automatiquement les gestionnaires de paquets (Yarn, PNPM).
* **dépôt GitHub "nodes/corepack"** : Dépôt officiel de Corepack.
* **site officiel de Yarn** (*yarnpkg.com*) : Documentation pour installer et configurer Corepack et Yarn.

---

### 3) Astuces concrètes et réutilisables
* **Activer Corepack** : Utiliser la commande `corepack enable` pour installer et gérer automatiquement les gestionnaires de paquets (comme PNPM et Yarn) sans avoir à les installer manuellement.
* **Éviter la duplication des fichiers de dépendances** : Utiliser PNPM pour stocker chaque version de bibliothèque une seule fois sur l'ordinateur, en créant des liens symboliques dans le dossier `node_modules` au lieu de copier physiquement les fichiers pour chaque projet.
* **Accélérer l'installation des dépendances** : Grâce à l'architecture de PNPM basée sur un stockage centralisé (*pnpm-store*) et des liens matériels/symboliques, les installations de projets (comme Next.js ou React) se font de manière quasi instantanée (*x3* plus rapide par rapport à NPM).

---

### 4) Chiffres de revenus annoncés
* **Revenus :** Non précisé (la vidéo ne traite pas de monétisation ou de gains financiers avec l'IA ou d'autres outils, mais de performance technique des gestionnaires de paquets).
