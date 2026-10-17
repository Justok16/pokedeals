# Antigravity 2.0 : la PIRE copie que j'aie jamais vue ?

Vidéo : https://youtu.be/k8-Dnt1vsOg · durée 18:59 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé complet et fidèle de la vidéo :

---

### 1) Idée principale
L'auteur teste et donne son avis critique sur **Antigravity 2.0** (présenté sous l'égide de Google). Il compare cette interface d'agents IA autonomes à **Codex** et **Cursor**, critiquant son manque de fluidité (application Electron mal optimisée), ses blocages récurrents dus aux demandes de permissions incessantes à chaque commande de terminal, et ses quotas de requêtes stricts (notamment sur les modèles avancés comme Claude Opus), recommandant plutôt des outils natifs plus réactifs et mieux pensés pour les développeurs.

---

### 2) Outils, sites et dépôts cités

* **Google Antigravity 2.0**
  * *Statut :* Gratuit avec quotas / Payant selon abonnement Google (non précisé en détail).
  * *Utilité :* Environnement de développement et plateforme d'orchestration d'agents IA autonomes capables d'exécuter des tâches en parallèle sur des projets de code.
* **Codex**
  * *Statut :* Payant (avec quotas/accès selon plans).
  * *Utilité :* Application de développement assisté par agents IA (mise en avant par le créateur Tibo), servant de référence de comparaison pour l'expérience utilisateur et l'autonomie.
* **Cursor**
  * *Statut :* Gratuit avec formule payante (non détaillé dans la vidéo).
  * *Utilité :* Éditeur de code assisté par IA (fork de VS Code).
* **VS Code (Visual Studio Code)**
  * *Statut :* Gratuit.
  * *Utilité :* Éditeur de code standard open source de Microsoft.
* **Zed**
  * *Statut :* Gratuit / Open source.
  * *Utilité :* Éditeur de code natif très rapide, recommandé par l'auteur comme alternative fluide.
* **Artificial Analysis (`artificialanalysis.ai`)**
  * *Statut :* Gratuit.
  * *Utilité :* Site de benchmark indépendant comparant les performances, vitesses et indices de programmation des différents modèles d'IA (Gemini, Claude, GPT).
* **Google One (Google AI Plus / Pro / Ultra)**
  * *Statut :* Payant (Google AI Plus à 7 CHF/mois, Pro à 17 CHF/mois, Ultra à partir de 100 CHF/mois affichés à l'écran).
  * *Utilité :* Abonnements cloud/IA de Google donnant accès à des fonctionnalités et quotas accrus pour Gemini.
* **Modèles d'IA mentionnés :**
  * *Gemini (3.5 Flash, 3.1 Pro)*, *Claude Sonnet 4.6 / Claude Opus 4.6 (Thinking)*, *GPT-OSS 120B*.
  * *Utilité :* Modèles de langage utilisés pour générer et inspecter le code.
* **mlv.sh/fc (Configuration CLI de Melvynx)**
  * *Statut :* Gratuit (avec inscription email).
  * *Utilité :* Script et configuration en ligne de commande pour paramétrer des agents IA (agents, commandes personnalisées, statusline, safe scripts) compatibles Claude Code, Codex et Cursor.
* **Projets / applications persos montrés :**
  * `tchao.app` (widget web de conversation/vente) et `thumbfa.st` / `codelynx` (générateur de miniatures).

---

### 3) Astuces concrètes et réutilisables

* **Détecter si une application desktop est une web app Electron :** Utilisez le raccourci clavier `Cmd + Option + I` (sur Mac). Si l'inspecteur d'éléments web (DevTools) s'ouvre, l'application est packagée sous Electron, ce qui explique souvent une plus grande lourdeur et une consommation accrue de RAM par rapport à une application native.
* **Supprimer les blocages de permissions dans les agents :** Pour éviter que l'agent ne s'arrête à chaque script ou commande de terminal, modifiez les paramètres de sécurité de l'environnement (dans les réglages de l'agent / projet) en passant les règles de terminal sur **« Unrestricted »** ou en cochant l'option d'autorisation permanente des commandes récurrentes (ex. `pnpm build`, scripts TypeScript).
* **Paralléliser l'analyse de codebase avec des sous-agents :** Pour auditer une application, demandez explicitement au modèle de lancer des sous-agents dédiés (ex. un sous-agent pour analyser la sécurité backend, un autre pour les endpoints API, un autre pour les droits d'accès).
* **Gérer ses quotas de requêtes :** Utilisez des modèles plus légers et rapides (comme *Flash*) pour les tâches d'exploration, de routine ou de recherche, et réservez les modèles plus lourds (*Pro* ou *Opus*) uniquement pour le raisonnement complexe afin d'éviter d'épuiser prématurément le quota d'appels.

---

### 4) Chiffres de revenus annoncés

* **Revenus annoncés :** Non précisé (la vidéo ne mentionne aucun chiffre d'affaires, gain financier ou revenu généré).
