# Nouveau sur Codex : ChatGPT Voice te permet de discuter avec ton code

Vidéo : https://youtu.be/Du_weEGuzF0 · durée 17:09 · résumé Gemini (gemini-3.8-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo structuré selon vos critères :

---

### 1) Idée principale
La vidéo présente un test pratique du nouveau mode vocal interactif (**ChatGPT Voice**) intégré dans l'environnement desktop **Codex**. L'auteur démontre comment piloter des agents d'intelligence artificielle à la voix pour orchestrer plusieurs projets de développement web en parallèle (génération d'un site d'inventaire Minecraft, refonte d'un portfolio avec génération d'images, et création rapide d'un mini-jeu interactif façon Flappy Bird).

---

### 2) Outils, sites et dépôts cités

* **ChatGPT Voice / Codex (OpenAI)** :
  * *Nature & Utilité* : Application desktop et assistant vocal d'OpenAI permettant de piloter des agents de code et d'exécuter des tâches de programmation à la voix.
  * *Tarif* : Non précisé dans la vidéo (généralement lié aux forfaits ChatGPT Plus/Team/Enterprise).
* **OpenCodex** (interface locale `127.0.0.1:5100`) :
  * *Nature & Utilité* : Serveur proxy/gestionnaire de modèles permettant de router des requêtes vers différents fournisseurs. L'auteur signale qu'il doit être désactivé pour que le voice chat natif fonctionne correctement.
  * *Tarif* : Outil open-source / Gratuit (frais d'API éventuels selon les modèles : non précisé).
* **Claude / Claude Code (Anthropic)** :
  * *Nature & Utilité* : Outil de codage agentique d'Anthropic mentionné comme alternative disposant également d'un mode vocal et d'agents de terminal.
  * *Tarif* : Non précisé dans la vidéo.
* **Cursor** :
  * *Nature & Utilité* : Éditeur de code assisté par IA cité sur la page finale pour la configuration d'agents.
  * *Tarif* : Non précisé dans la vidéo.
* **Convex** :
  * *Nature & Utilité* : Plateforme backend / base de données visible dans l'historique de projet de l'auteur.
  * *Tarif* : Non précisé dans la vidéo.
* **mlv.sh/fc (codevalyx.dev)** :
  * *Nature & Utilité* : Page web de l'auteur proposant un script / kit de configuration en une seule commande pour configurer des agents IA (skills, règles, plugins) sur Claude Code, Codex CLI et Cursor.
  * *Tarif* : Payant / accès sur inscription (prix exact : non précisé).

---

### 3) Astuces concrètes et réutilisables

* **Résolution de bug au lancement vocal** : Si le mode vocal se ferme instantanément à l'ouverture, vérifier si un proxy local (tel qu'OpenCodex) intercepte le trafic de l'application ChatGPT / Codex et le désactiver.
* **Gestion du multitâche oral** : Demander explicitement à l'agent de créer des tâches ou des pages séparées pour éviter qu'il n'écrase le travail en cours sur un autre fichier.
* **Utilisation du bouton mute / micro** : Couper le micro dès que l'instruction est terminée ou lorsqu'on réfléchit à haute voix pour éviter que l'IA ne transcrive des bruits ou des paroles parasites.
* **Délégation multi-agents** : Lancer une tâche longue (comme la génération d'assets ou d'images) dans un fil d'exécution, puis basculer oralement sur une autre tâche (développement d'un mini-jeu) pour optimiser son temps de travail.
* **Prototypage de jeux légers à la volée** : Les modèles de code actuels sont capables de générer un jeu HTML5/Canvas fonctionnel en quelques secondes à partir d'une description simple (ex. : adapter la physique et les obstacles de Flappy Bird).

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de revenus n'est mentionné** dans la vidéo (l'auteur lance uniquement une boutade à 14:17 disant que l'application va « le rendre milliardaire », sans aucune donnée financière réelle). 
* **Chiffre concret** : **Non précisé** (affirmé par l'auteur).
