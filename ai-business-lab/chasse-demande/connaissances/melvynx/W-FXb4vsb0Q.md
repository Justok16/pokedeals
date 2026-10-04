# Le GROS problème de l'IA : j'ai une nouvelle addiction

Vidéo : https://youtu.be/W-FXb4vsb0Q · durée 10:19 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur explique comment l'automatisation quasi totale de son activité de développement par des agents IA (comme Codex ou Claude) modifie profondément son travail. Au lieu de coder et de rester dans un état de concentration intense (*flow*), il passe désormais l'essentiel de ses journées à attendre la fin des générations de code. Ces temps morts répétés entraînent un ennui et une perte d'attention qu'il comble par des distractions compulsives (scrolling sur X et parties d'échecs sur Chess.com). Pour rentabiliser son temps, il est contraint d'orchestrer plusieurs agents et projets en simultané (*multitasking*), tout en constatant une perte de la satisfaction intellectuelle liée à la réflexion technique.

---

### 2) Outils, sites ou dépôts cités

* **Codex Desktop / Codex CLI** :
  * *Utilité :* Agent de développement autonome qui modifie les fichiers, exécute des commandes et prépare les commits/pushs.
  * *Modèle économique :* Non précisé pour le logiciel lui-même ; consomme des crédits API payants.
* **Claude (Anthropic) / Claude Code** :
  * *Utilité :* Modèles de langage utilisés pour piloter les agents et générer le code source.
  * *Modèle économique :* Payant (consommation de tokens API).
* **agent-burn (`npx agent-burn`)** :
  * *Utilité :* Outil CLI dans le terminal permettant d'auditer et d'afficher le résumé des dépenses financières et du volume de tokens consommés par les différents agents de code.
  * *Modèle économique :* Non précisé (utilitaire en ligne de commande / open source).
* **Chess.com** :
  * *Utilité :* Application et plateforme d'échecs utilisée par l'auteur pour s'occuper pendant les temps de chargement des agents IA.
  * *Modèle économique :* Gratuit (l'auteur utilise l'application mobile standard ; existence d'options payantes non précisée dans la vidéo).
* **X (ex-Twitter / x.com)** :
  * *Utilité :* Réseau social parcouru pendant les temps d'attente de génération.
  * *Modèle économique :* Gratuit (accès au flux standard).
* **App Store Connect** :
  * *Utilité :* Console Apple pour publier des versions d'applications mobiles, importer les captures d'écran générées et suivre les déploiements TestFlight.
  * *Modèle économique :* Payant (implique un compte Apple Developer payant, tarif non précisé dans la vidéo).
* **Tella (tella.tv)** :
  * *Utilité :* Outil d'enregistrement et de montage vidéo d'écran visible parmi les onglets de l'auteur.
  * *Modèle économique :* Non précisé.
* **NowStack Mobile (sur codelynx.dev)** :
  * *Utilité :* Stack technique clé en main et vidéos de formation créées par l'auteur pour assembler une application mobile (Expo, Convex, Better Auth, Stripe, In-App purchases, agents IA).
  * *Modèle économique :* Gratuit (la page indique « formation 100% vidéo gratuit »).
* **melvynx.com / codelynx.dev** :
  * *Utilité :* Site personnel et catalogue de formations de l'auteur (*Agent Config Pro*, *AssistantPro*, *NextFullStack*, *AIBp*).
  * *Modèle économique :* Non précisé selon les programmes.

---

### 3) Astuces concrètes et réutilisables

1. **Déléguer la routine de publication d'applications :** Confier aux agents IA la création et l'ajustement automatique des captures d'écran pour tous les formats d'écrans (Apple Watch, iPhone), la mise à jour des versions, les scripts de build et l'envoi vers TestFlight.
2. **Piloter plusieurs agents en parallèle (multithreading d'agents) :** Pour compenser l'inactivité liée au temps de calcul, attribuer une tâche distincte à chaque agent (Agent 1 sur une branche, Agent 2 sur une autre feature, Agent 3 sur une mise à jour d'UI) puis procéder à la revue de code à tour de rôle.
3. **Optimiser la création de tutoriels vidéo :** Découper les sessions d'enregistrement : mettre en pause pendant le temps de calcul de l'IA pour enregistrer un extrait d'une autre vidéo en parallèle, évitant ainsi 40 minutes de temps mort pour une vidéo finale de 20 minutes.
4. **Verrouiller activement les sources de distraction :** Bloquer ou limiter l'accès aux applications réflexes (jeux mobiles, réseaux sociaux) qui profitent des micro-pauses imposées par les requêtes d'IA et détruisent la capacité de concentration.

---

### 4) Chiffres de revenus annoncés

* **Chiffre d'affaires / Bénéfices :** Aucun chiffre de gain ou de revenu n'est annoncé (les métriques de l'App Store montrées à l'écran indiquent *« Not enough data »* pour les ventes et achats intégrés).
* **Dépenses d'API annoncées (affirmé par l'auteur) :**
  * **847,84 $** dépensés sur une seule journée (représentant **921,3 millions de tokens**).
  * **4 324,48 $** dépensés sur une semaine (représentant **4,48 milliards de tokens**).
