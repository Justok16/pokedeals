# WaQClgUYSXQ — « Claude Desktop 2.0 : tout a changé pour Claude Code »

- Auteur : Melvynx ; lien : https://youtu.be/WaQClgUYSXQ
- Envoyée par l'utilisateur le 13/11/2026 ; résumée le 13/11 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les fonctions décrites sont celles montrées par l'auteur ; non revérifiées dans la documentation officielle (aucune n'est appliquée).

## Tri pour DIG16 (13/11)

Tour de l'application Claude sur ordinateur (onglet Code) : tri des conversations par état, travail sur un serveur distant, sous-agents en parallèle, tableau blanc, pilotage depuis le téléphone. Comparé à DIG16 :

- **Tri des conversations par état et archivage** : notre règle du 11/11 règle déjà le problème à la source (une seule conversation pour l'utilisateur, conversations de service archivées dès la fin). Rien à changer.
- **Sous-agents en parallèle** : déjà utilisé (relecteurs en lecture seule, conversations de service).
- **Pilotage depuis le téléphone** : déjà notre fonctionnement (sessions dans le nuage, sans ordinateur allumé).
- **Serveur distant payant (VPS)** : écarté (budget 0 € ; nos sessions tournent déjà dans le nuage).
- **Tableau blanc et pages partagées** : déjà disponibles ici (pages publiées) ; à ressortir si un client veut valider une maquette en la commentant.
- **Cours « Brain » de l'auteur** : publicité pour sa formation ; notre mémoire (CLAUDE.md, leçons, journal) remplit ce rôle.
- **Fonction en aperçu, sur invitation, citée en fin de vidéo** : non disponible ; la veille des outils du lundi la signalera si elle s'ouvre.

Conclusion : rien à installer, rien à changer.

## Résumé (Gemini)

Voici le résumé complet de la vidéo :

---

### 1) Idée principale
La vidéo présente 5 fonctionnalités clés de la nouvelle interface de l'application **Claude Desktop (Claude Code / version 2.0)** permettant de démultiplier sa productivité. Grâce à l'organisation des sessions par statut, l'exécution distante via SSH/VPS, l'orchestration de sous-agents en parallèle, les tableaux blancs interactifs (*Whiteboard*) et le contrôle à distance depuis son smartphone, l'utilisateur peut automatiser et exécuter plusieurs projets simultanément sans surcharger son ordinateur.

---

### 2) Outils, sites et projets cités

1. **Claude Desktop / Claude Code** (par Anthropic)
   * **Gratuit / Payant :** Gratuit à télécharger, mais nécessite un compte et des crédits pour consommer les modèles de langage (ex. Claude 3.5 Sonnet, Opus, Fable).
   * **À quoi il sert :** Application de bureau offrant une interface de travail avec gestion de projets, onglet Code, configuration d'environnements et suivi de tâches d'agents IA.

2. **Serveur VPS / SSH / Remote Control**
   * **Gratuit / Payant :** Payant (hébergement VPS externe).
   * **À quoi il sert :** Permet de déporter l'exécution de tâches lourdes (comme le montage vidéo automatisé) sur un serveur distant connecté par SSH pour éviter de faire crasher son ordinateur local.

3. **Application mobile Claude (iOS / iPhone)**
   * **Gratuit / Payant :** Gratuit à télécharger (lié au compte Claude).
   * **À quoi il sert :** Permet de dicter des consignes à la voix et de contrôler à distance la session active sur son ordinateur via l'option *Remote Control*.

4. **Whiteboard / Artifacts (intégré à Claude)**
   * **Gratuit / Payant :** Inclus dans l'application Claude.
   * **À quoi il sert :** Génération de tableaux blancs virtuels (post-it, schémas, feedback bidirectionnel), documents, présentation de slides et feuilles de calcul.

5. **OpenBot / OpenClaw** (cité dans les exemples)
   * **Gratuit / Payant :** Non précisé.
   * **À quoi il sert :** Projet de bot/agent IA cité à titre d'exemple pratique de recherche et d'écriture de scripts.

6. **Cours Brain (lien `mlv.sh/fx`)**
   * **Gratuit / Payant :** Gratuit.
   * **À quoi il sert :** Formation/méthode pour structurer son propre système "Brain" (gestion de connaissances, mémoire et scripts de "rêve" automatique pour organiser Claude).

7. **Claude Duet (Claude Duct)**
   * **Gratuit / Payant :** Aperçu / Beta (sur invitation / preview).
   * **À quoi il sert :** Fonctionnalité proactive fonctionnant 24/7 en arrière-plan pour accomplir des tâches autonomes (mentionnée brièvement à la fin).

---

### 3) Astuces concrètes et réutilisables

* **Travailler sur l'onglet Code :** Passer sur l'onglet *Code* plutôt que *Chat* pour débloquer la gestion des projets, des environnements et de l'orchestration.
* **Trier les chats par statut (`Group by -> Status`) :** Organiser visuellement les conversations en trois catégories clés :
  * `Working` : l'agent est en train de travailler.
  * `Needs Input` : l'agent est bloqué et attend une validation/consigne de votre part.
  * `Idle` : l'agent a terminé sa tâche.
* **Activer l'affichage des métadonnées (`Show -> Metadata`) :** Affiche sous le titre de chaque chat le dossier de travail associé ainsi qu'un résumé de la dernière tâche pour retrouver le contexte instantanément.
* **Archiver régulièrement les chats inutiles :** Utiliser le raccourci ou le menu `... -> Archive` pour nettoyer la barre latérale et garder uniquement les sessions de travail actives.
* **Orchestrer des sous-chats / sous-agents :** Donner un prompt global à un agent principal ("Orchestrateur") lui demandant de lancer et piloter plusieurs "sous-chats" en parallèle (ex. lancer 9 sous-agents pour traiter 9 vidéos différentes).
* **Utiliser le contrôle à distance depuis le mobile :** Utiliser le mode vocal de l'application Claude sur smartphone pour envoyer une consigne qui s'exécutera et s'affichera directement sur l'écran de votre ordinateur.

---

### 4) Chiffres de revenus annoncés
* **Aucun chiffre de revenus n'est mentionné dans la vidéo** (*non précisé*).
