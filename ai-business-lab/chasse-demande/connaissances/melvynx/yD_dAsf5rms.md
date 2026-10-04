# Le CLI le plus cheaté : ASC pour déployer ton application sur l'App Store

Vidéo : https://youtu.be/yD_dAsf5rms · durée 9:08 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’auteur montre comment automatiser de bout en bout la création, la configuration et la publication d’applications iOS (et web) sur l’App Store grâce à **Claude Code** couplé à l'outil CLI **`asc`** (App Store Connect CLI) et sa propre boilerplate **`NowStack Mobile`**. L'intelligence artificielle gère directement via le terminal l'authentification API, la génération/upload des captures d'écran, les métadonnées, les achats intégrés (IAP), les builds et le déploiement sur TestFlight et la mise en production.

---

### 2) Outils, sites et dépôts cités

* **`asc` (App Store Connect CLI)** *(Site : `ascli.sh` / Dépôt GitHub)*
  * **Statut :** Gratuit / Open source.
  * **Rôle :** Interface en ligne de commande (CLI) en un seul binaire Go permettant de piloter l'ensemble des API d'App Store Connect (gestion des builds, métadonnées, TestFlight, certificats, captures d'écran, validation).
* **`Claude Code`** *(Anthropic)*
  * **Statut :** Payant (accès via abonnement Claude / crédits API Anthropic).
  * **Rôle :** Agent d'IA en terminal qui exécute les commandes, génère le code, audite le projet et appelle les commandes CLI pour automatiser les déploiements.
* **`NowStack Mobile`** *(Boilerplate de l'auteur / Site : `codelynx.dev/nowstack-mobile/get` ou `mlv.sh/fm`)*
  * **Statut :** Présenté avec une mini-formation gratuite (accès sur liste d'attente / tarif complet non précisé).
  * **Rôle :** Modèle de projet fullstack (mobile + web + admin) intégrant des compétences d'agents IA prédéfinies (`ns-*`) pour automatiser le développement et le déploiement.
* **`App Store Connect`** *(Apple)*
  * **Statut :** Nécessite le compte Apple Developer (99 $/an habituellement, *non précisé dans la vidéo*).
  * **Rôle :** Plateforme de gestion et de publication des applications iOS.
* **`Expo` / `EAS`**
  * **Statut :** Gratuit / Modèle freemium (*non précisé*).
  * **Rôle :** Framework et infrastructure de build pour applications React Native.
* **`Convex`**
  * **Statut :** Gratuit / Freemium (*non précisé*).
  * **Rôle :** Backend réactif en temps réel et base de données pour l'application.
* **`Better Auth`**
  * **Statut :** Gratuit / Open source.
  * **Rôle :** Gestion de l'authentification (e-mail avec code OTP, Apple, Google).
* **`NativeWind`**
  * **Statut :** Gratuit / Open source.
  * **Rôle :** Intégration de Tailwind CSS pour le style sur React Native.
* **`Stripe` & `Apple In-App Purchases (IAP)`**
  * **Statut :** Gratuit à intégrer (commission sur les ventes).
  * **Rôle :** Gestion des paiements web (Stripe) et des achats intégrés mobiles (Apple).

---

### 3) Astuces concrètes et réutilisables

1. **Bannir l'interface web d'App Store Connect :** Créez une clé API dans *Users and Access > Integrations > App Store Connect API* (rôle Admin) et configurez-la dans votre terminal avec `asc auth login` pour tout piloter en scripts.
2. **Créer des commandes d'agent (*Agent Skills*) :** Encapsulez les flux répétitifs dans des commandes personnalisées exécutables par Claude Code, comme :
   * `/find-asc-credentials` : Récupère et configure les clés d'accès.
   * `/ns-ios-audit` : Vérifie la conformité de l'application avec les règles de soumission Apple.
   * `/ns-images` : Génère les maquettes/captures d'écran multi-formats (iPhone, Apple Watch) via des modèles HTML/CSS et les téléverse automatiquement.
   * `/ns-ios-testflight` / `/ns-ios-distribute` : Compile, publie sur TestFlight et pré-remplit les métadonnées (description, mots-clés, URLs, IAP) sur la fiche produit.
3. **Centralisation des logs :** Redirigez l'ensemble des logs (backend Convex, web et mobile) vers un dossier commun du projet afin que l'agent IA puisse les lire et auto-corriger les bugs lors des tests.
4. **Panneau d'administration intégré :** Prévoir une interface admin web connectée à la même base de données pour passer un utilisateur en `admin` via le terminal et tester les comptes immédiatement.

---

### 4) Chiffres de revenus annoncés

* **Revenus globaux réalisés :** **Non précisé** (l'auteur ne dévoile pas son chiffre d'affaires total).
* **Tarifs / Monétisation montrés dans les exemples :**
  * Accès à vie (*Lifetime Access*) sur le modèle NowStack : **19,99 $** (*affirmé par l'auteur*).
  * Abonnement récurrent pour son application *Panda Couple Trackers* : **5 € / mois** (*affirmé par l'auteur*).
