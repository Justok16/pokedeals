# J'ai créé ET publié une app iOS en seulement 2 heures (hack ultime)

Vidéo : https://youtu.be/9-AGC9p_R7g · durée 16:17 · résumé Gemini (gemini-3.8-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, orienté pour le développement de projets rémunérateurs et l'automatisation avec des agents de code IA.

---

### 1) Idée principale
L'auteur montre comment créer, tester et publier une application mobile iOS native complète (liée à un SaaS web existant) sur l'App Store Connect / TestFlight en quelques heures, sans coder manuellement. Il utilise des agents IA autonomes (pilotés par des modèles avancés comme Claude et GPT-5/Codex) combinés à une collection de **"skills"** (instructions et scripts d'automatisation) et un mécanisme de **validation visuelle par capture d'écran** sur simulateur. 

Cette méthode permet de monétiser très rapidement des compétences de développement : soit en lançant ses propres micro-SaaS mobiles, soit en vendant des applications à des clients/entreprises à des tarifs d'agence (50 000 € à 100 000 € selon lui), tout en réduisant le travail à une demi-journée de supervision.

---

### 2) Outils, sites et dépôts cités

* **Claude / Claude Code / API Anthropic** : 
  * *Statut :* Payant (facturation à la consommation de tokens API).
  * *Rôle :* Modèle de raisonnement et agent d'exécution pour coder, corriger les bugs complexes et structurer les fonctionnalités.
* **Codex / Apex (environnement agent)** : 
  * *Statut :* Payant (consommation de tokens/abonnements API).
  * *Rôle :* Interface de terminal/agent autonome exécutant les commandes, les tests et les modifications de fichiers en boucle fermée.
* **asc (asc-cli / `asc.sh`)** : 
  * *Statut :* Gratuit (outil open-source en Go).
  * *Rôle :* CLI scriptable pour automatiser App Store Connect (gestion TestFlight, certificats, téléversement de builds, captures d'écran et métadonnées sans passer par le navigateur).
* **NowStack Mobile / NowStack** : 
  * *Statut :* Accessible via mini-formation gratuite avec inscription email (`codelynx.dev/nowstack-mobile/get`) ; le pack complet de scripts/boilerplate peut être soumis à condition ou payant selon l'offre de l'auteur.
  * *Rôle :* Boilerplate React Native / Expo configuré avec authentification, backend temps réel et bibliothèque d'agents/skills pré-écrits.
* **Expo / EAS (Expo Application Services)** : 
  * *Statut :* Outil CLI gratuit ; services cloud de build (EAS Build) freemium/payants (l'auteur privilégie l'option `--local` pour que ce soit gratuit).
  * *Rôle :* Framework pour compiler et packager l'application iOS.
* **Convex** : 
  * *Statut :* Freemium (gratuit avec quotas, puis payant).
  * *Rôle :* Backend en temps réel et gestion de la base de données.
* **iPhone Mirroring (macOS)** : 
  * *Statut :* Gratuit (fonctionnalité native macOS).
  * *Rôle :* Permet de manipuler et tester l'application directement sur un iPhone physique depuis l'ordinateur.
* **Tchao.app** : 
  * *Statut :* Commercial / Payant (SaaS de l'auteur).
  * *Rôle :* SaaS de widget de chat commercial pour sites web dont l'application mobile a été créée dans la vidéo.
* **Daily AI Citation** : 
  * *Statut :* Application freemium (3 citations gratuites puis payante).
  * *Rôle :* Micro-application d'exemple créée et validée sur l'App Store pour tester la stack de publication.

---

### 3) Astuces concrètes et réutilisables

1. **Standardiser des "Skills" pour vos agents :** Au lieu de redonner de longs prompts à chaque tâche, regroupez les consignes dans des fichiers de compétences réutilisables (ex. : `ns-ios-testflight`, `ns-ios-distribute`, `ns-image`). L'agent sait exactement quels scripts lancer (`asc`, `eas`), quelles clés d'API utiliser et comment réagir en cas d'erreur.
2. **Imposer une boucle de vérification visuelle (`-axv`) :** Pour éviter que l'IA ne prétende avoir terminé alors que l'interface est cassée, imposez-lui de lancer le simulateur iOS, d'interagir avec l'UI, de capturer une capture d'écran (`visual proof`) et de comparer le résultat avec le ticket.
3. **Automatiser l'audit des règles Apple (`ns-ios-audit`) :** Faites auditer le code par l'IA avant toute soumission pour vérifier la conformité aux directives strictes de l'App Store (présence d'achats in-app conformes, bouton de suppression de compte, politique de confidentialité).
4. **Faire les builds en local :** Pour éviter d'exploser les coûts de cloud EAS, paramétrez l'IA pour compiler l'application localement sur votre machine (`--local`).
5. **Génération automatisée des assets :** Utilisez l'agent pour créer automatiquement les déclinaisons de captures d'écran aux résolutions exactes exigées par Apple (6.5", 5.5", iPad, etc.) et les injecter directement via `asc`.

---

### 4) Chiffres annoncés

* **Revenus personnels / CA généré par cette app :** *Non précisé*.
* **Valeur marchande d'une telle application :** **50 000 € à 100 000 €** si elle était commandée à une agence de développement web/mobile (*affirmé par l'auteur*).
* **Coûts de fonctionnement / API engagés :**
  * La veille du tournage : **1 127,93 $** dépensés en API (dont **761,50 $** uniquement pour Claude) (*affirmé par l'auteur*).
  * En cours de session sur la vidéo : environ **442 $** à **642 $** de tokens consommés (*affirmé par l'auteur*).
