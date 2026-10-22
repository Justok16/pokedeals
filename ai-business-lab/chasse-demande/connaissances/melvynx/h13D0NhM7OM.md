# CLAUDE REMOTE CONTROL : contrôle Claude Code depuis ton iPhone (c'est une folie)

Vidéo : https://youtu.be/h13D0NhM7OM · durée 11:43 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré comme demandé :

---

### 1) Idée principale
La vidéo présente deux nouveautés majeures de **Claude Code** (outil d'assistance au code par IA) :
1. **Remote Control** : Permet de contrôler une session Claude Code en cours sur son ordinateur à distance (par exemple depuis son iPhone via une application de messagerie ou Telegram), afin de continuer à coder ou valider des modifications même en déplacement.
2. **Worktrees** : Permet d'isoler chaque branche de travail dans un dossier séparé (via des scripts ou outils dédiés) pour éviter de perturber le projet principal et mieux s'organiser, notamment en parallèle de sessions multiples.

L'objectif global est d'optimiser le flux de travail des développeurs pour coder plus rapidement et efficacement à l'aide de l'IA, n'importe où et à tout moment.

---

### 2) Outils, sites et dépôts GitHub cités

* **Claude Code** (et **Claude.ai**)
  * **Type :** Non précisé (généralement payant/abonnement Pro, mentionné au début).
  * **Rôle :** Assistant de code par IA qui permet de générer, modifier et gérer du code source via des commandes textuelles.
* **Telegram**
  * **Type :** Gratuit.
  * **Rôle :** Application de messagerie utilisée pour interagir à distance avec Claude Code (via Remote Control) et envoyer des commandes/valider du code depuis son smartphone.
* **Escalidraw** (mentionné visuellement comme tableau blanc/schéma)
  * **Type :** Gratuit.
  * **Rôle :** Utilisé pour schématiser l'architecture des connexions entre l'ordinateur, le smartphone et les serveurs Claude.
* **GitHub / Dépôt communautaire (Configuration Claude Code)**
  * **Type :** Gratuit (accessible via le lien court fourni par l'auteur : `mlv.sh/fc`).
  * **Rôle :** Dépôt contenant la configuration personnelle de l'auteur, incluant agents, commandes et scripts (notamment pour renommer la session, gérer le statut, le validateur, et les raccourcis clavier).
* **Conductor**
  * **Type :** Non précisé (outil tiers/extension mentionné).
  * **Rôle :** Outil pour gérer et séparer les projets/dossiers de travail (Workspaces/sub-fast/Victoria) afin d'éviter les conflits de fichiers.
* **Git / LazyGit / Yazi**
  * **Type :** Gratuit / Open Source.
  * **Rôle :** Outils de gestion de versions et de navigation dans les fichiers, combinés dans des scripts pour automatiser la création de branches et de worktrees.

---

### 3) Astuces concrètes et réutilisables

* **Utiliser "Remote Control" :** Lancez la commande `/remote-control` dans votre terminal avec Claude Code. Copiez le lien généré et envoyez-le-vous (par exemple sur Telegram ou un autre support mobile). Cela vous permet de valider des modifications, d'accepter des "commits" ou d'envoyer des instructions à Claude depuis votre téléphone pendant que vous êtes en déplacement ou en train de faire autre chose.
* **Combiner Claude Code avec les "Worktrees" Git :** Utilisez des scripts ou des commandes automatisées (comme celles proposées dans le dépôt de l'auteur) pour créer chaque nouvelle branche de travail dans un sous-dossier séparé (`/worktrees/branch-name`). Cela évite d'ouvrir des copies dans le même projet principal et permet de travailler sur plusieurs fonctionnalités en parallèle sans mélanger les fichiers.
* **Synchroniser les interfaces :** Profitez de la fluidité des applications mobiles (comme Telegram combiné à l'interface de Claude) pour garder un œil sur l'état de votre code en temps réel et valider/refuser rapidement les modifications sans avoir à rester bloqué devant votre écran d'ordinateur.

---

### 4) Chiffres de revenus annoncés
* **Affirmé par l'auteur :** Non précisé (aucun chiffre de gain financier ou de revenu n'est mentionné dans la vidéo).
