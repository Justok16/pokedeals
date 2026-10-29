# MMOs in the Instagram Era: Highrise (S18) - YC Gaming Tech Talks 2020

Vidéo : https://youtu.be/ztoZF65LUgk · durée 5:38 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici la fiche de connaissances résumant la vidéo :

### 1) Sujet et thèse principale
* **Sujet** : La conception et le développement de jeux MMO (jeux massivement multijoueurs) pour mobiles à l'ère des réseaux sociaux, avec l'exemple de l'application Highrise.
* **Thèse principale** : Pour réussir un MMO mobile aujourd'hui, il ne faut pas concevoir d'abord le jeu puis ajouter le social, mais adopter une approche « **social-first** » : commencer par les fonctionnalités sociales (messagerie, flux, guildes, avatar, monde, économie) et intégrer le jeu ensuite pour fidéliser les utilisateurs et résoudre le problème de l'attention à long terme.

---

### 2) Notions expliquées
* **MMO (Massively Multiplayer Online game)** : Jeu vidéo en ligne réunissant un grand nombre de joueurs simultanément dans un univers virtuel.
* **Social-first** : Approche de conception de produits (ici de jeux) qui met la dimension sociale et la communauté au cœur du projet, avant même les mécaniques de jeu.
* **Architecture 50/50 app/jeu** : Conception logicielle où l'application est partagée entre une interface utilisateur fluide de type réseau social et un moteur de jeu performant.

---

### 3) Chiffres, taux, plafonds et règles fiscales cités
* **Plus de 5 millions de téléchargements** (à vérifier à la source officielle).
* **Plus d'un million de dollars de revenus mensuels** (à vérifier à la source officielle).
* **Architecture technique** : 50 % Swift (iOS) et 50 % C++ (moteur de jeu et logique métier partagée).
* **Entreprise** : Fondée sur un modèle entièrement à distance depuis **4 ans**, ayant levé une série A (à vérifier à la source officielle).

---

### 4) Conseils concrets et leurs limites ou risques
* **Conseil** : Privilégier une architecture hybride (composants natifs UI pour la fluidité et moteur puissant pour le monde virtuel) plutôt que de s'appuyer uniquement sur des moteurs de jeux tiers qui ne maîtrisent pas aussi bien l'ergonomie des applications mobiles.
* **Limites / Risques** : Nécessite une maîtrise poussée du développement natif (Swift, C++, JNI/Objective-C) et une structure logicielle complexe (microservices par fonctionnalité et système de ponts) qui peut être difficile à mettre en place pour de petites équipes.

---

### 5) Produits, applications ou entreprises cités
* **Highrise** (application iOS et Android) – **Produit de l'intervenant / Publicité** pour son application.
* **Pocket Worlds** (entreprise) – **Entreprise de l'intervenant**.
* **Snapchat** / **Instagram** – Cités comme exemples de références pour l'expérience utilisateur mobile.
* **Unity** – Cité comme moteur de jeu concurrent (jugé moins adapté pour l'ergonomie purement mobile par rapport au natif).
