# FABLE 5 : LA SUPER INTELLIGENCE EST DÉJÀ LÀ ? (modèle Claude)

Vidéo : https://youtu.be/nPnVq0nOxQc · durée 20:57 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
Dans cette vidéo d’anticipation / parodie futuriste (située en 2026), l’auteur présente un retour d’expérience sur les capacités des modèles IA fictifs **Claude Fable 5** et **Claude Mythos 5** (comparés à Claude Opus 4.8 et GPT-5.5). Il démontre concrètement comment il utilise ces modèles et des agents autonomes (comme Claude Code) pour exécuter des chantiers de programmation massifs en quasi-autonomie (refactorisation complète d'un backend, création et refonte d'applications mobiles Expo/React Native, génération d'UI), tout en mettant en garde contre le coût exponentiel des tokens et les restrictions de sécurité (« safeguards »).

---

### 2) Outils, sites et dépôts cités

* **Claude / Modèles Claude Fable 5, Mythos 5, Opus 4.8, Sonnet, Haiku (Anthropic)** :
  * *Statut :* Payant (facturation à l'usage par token / abonnement mentionné à 200 $/mois pour les plans élevés).
  * *Utilité :* Modèles de langage et de raisonnement servant à orchestrer le développement, générer du code complexe et piloter des agents de bout en bout.
* **Claude Code** :
  * *Statut :* Outil officiel en ligne de commande (CLI). Coût lié à la consommation de tokens API Claude.
  * *Utilité :* Agent de terminal capable de lire, modifier des fichiers, exécuter des commandes, tester et corriger le code de manière autonome.
* **Codex (interface / outil agentique)** :
  * *Statut :* Payant (abonnement mentionné).
  * *Utilité :* Environnement de développement assisté par agent pour coder, tester sur simulateur et générer des assets.
* **saveit.now (dépôt / application)** :
  * *Statut :* Projet de l'auteur (statut gratuit/payant du code source : *non précisé*).
  * *Utilité :* Application de sauvegarde et scraping de bookmarks, utilisée ici comme cas d’étude de migration backend complète.
* **Convex** :
  * *Statut :* Gratuit avec paliers payants (*détail exact non précisé dans la vidéo*).
  * *Utilité :* Plateforme backend réactive et serverless vers laquelle l'auteur a fait migrer toute son application.
* **Prisma, Inngest, Redis** :
  * *Statut :* Outils open-source / services cloud freemium (*non précisé*).
  * *Utilité :* Ancienne pile technique de `saveit.now` supprimée au profit de Convex.
* **PandaCouple / panda-couple (dépôt / application)** :
  * *Statut :* Projet personnel de l'auteur (*statut payant/gratuit non précisé*).
  * *Utilité :* Application mobile pour couples créée sous Expo/React Native pour tester le développement d'écrans, d'onboarding et de composants UI par IA.
* **FrontierCode (`cognition.ai/blog/frontier-code`)** :
  * *Statut :* Gratuit d'accès (benchmark public).
  * *Utilité :* Benchmark créé par Cognition (créateurs de Devin) mesurant la conformité du code généré par IA aux critères d'acceptation de production (mergabilité réelle).
* **SWE-bench Pro** :
  * *Statut :* Benchmark public d'évaluation logicielle.
  * *Utilité :* Mesure la capacité des modèles à résoudre des problèmes d'ingénierie logicielle concrets.
* **CursorBench 3.1 (`cursor.com/cursorbench`)** :
  * *Statut :* Gratuit d'accès (données publiques).
  * *Utilité :* Benchmark publié par l'équipe de l'éditeur Cursor évaluant l'efficacité et le coût par tâche des différents modèles de code.
* **DeepSWE (`deepswe.datacurve.ai`)** :
  * *Statut :* Gratuit d'accès.
  * *Utilité :* Benchmark mesurant les agents de code sur des tâches d'ingénierie logicielle longues.
* **UI Skills (`ui-skills.com`)** :
  * *Statut :* Gratuit d'accès.
  * *Utilité :* Répertoire de patterns, règles et compétences de design/front-end pour orienter les développeurs et agents IA.
* **NowStack (`codelynx.dev/nowstack`)** :
  * *Statut :* Payant (*fermé au public au moment de la vidéo*).
  * *Utilité :* Boilerplate et stack technique conçue par l'auteur pour créer des applications mobiles exploitables directement par des agents IA.
* **Formation Claude Code (`mlv.sh/fa` / `codelynx.app`)** :
  * *Statut :* Gratuite (sur inscription).
  * *Utilité :* Formation vidéo et ressources pour configurer Claude Code, les agents et la barre d'état.
* **X / SuperGrok (Twitter)** :
  * *Statut :* Gratuit avec formules payantes (Grok / SuperGrok).
  * *Utilité :* Veille technologique et recherche de publications sur les performances des modèles IA.
* **Excalidraw (`app.excalidraw.com`)** :
  * *Statut :* Gratuit (version web).
  * *Utilité :* Tableau blanc virtuel pour schématiser la hiérarchie des familles de modèles.

---

### 3) Astuces concrètes et réutilisables

1. **Stratégie hybride de modèles pour réduire les coûts :** Utiliser le modèle le plus puissant (ex. Fable) pour le découpage stratégique, l'architecture et la supervision, mais déléguer les appels d'outils et l'implémentation répétitive à des modèles plus légers/moins chers (ex. Opus 4.8) afin d'éviter l'explosion des coûts d'API.
2. **Utilisation de « Skills » dédiés :** Configurer des commandes et instructions contextuelles réutilisables (ex. commande `/impeccable`, règles de design mobile, scripts de publication automatique vers les stores) pour forcer l'agent à respecter les standards de qualité sans réécrire les consignes.
3. **S'appuyer sur des boilerplates standardisées :** Pour rentabiliser l'IA, démarrer avec une base de code unifiée (ex. Expo + Convex), ce qui permet à l'agent d'implémenter des fonctionnalités complètes en « one-shot » (gestion d'état, base de données, authentification) sans blocage d'architecture.
4. **Surveillance des « safeguards » (sécurité) :** Dès qu'un prompt aborde explicitement l'audit de sécurité ou la détection de vulnérabilités, certains modèles basculent automatiquement vers un modèle inférieur bridé. Pour les tâches complexes, il faut formuler ses consignes d'ingénierie sans déclencher inutilement les filtres.
5. **Boucle de rétroaction automatisée :** Faire valider le résultat par l'agent lui-même à l'aide de tests automatisés, de captures d'écran sur simulateur et de lectures de logs avant de soumettre une pull request.

---

### 4) Chiffres de revenus annoncés

* **Revenus / Gains :** **Aucun chiffre de revenus n'est annoncé** dans la vidéo.
* **Dépenses annoncées (« affirmé par l'auteur ») :** L'auteur indique avoir dépensé environ **414 $ de tokens Claude** et **200 $ de tokens GPT** sur une seule journée (soit plus de **600 $ en une journée** pour faire tourner ses agents de code intensifs).
