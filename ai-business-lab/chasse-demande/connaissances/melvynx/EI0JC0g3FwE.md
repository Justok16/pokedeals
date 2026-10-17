# Je SETUP OpenClaw en 1 heure à un total débutant

Vidéo : https://youtu.be/EI0JC0g3FwE · durée 43:41 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Bien sûr ! Voici le résumé structuré et complet de la vidéo, répondant précisément à tes critères pour quelqu'un qui souhaite gagner de l'argent légalement grâce à l'IA et **Claude Code**.

---

### 1) Idée principale
La vidéo montre en direct comment configurer, installer et exploiter **OpenClaw** (un assistant IA connecté à des outils et à des plateformes comme Telegram) hébergé sur un serveur virtuel privé (VPS), piloté à l'aide de **Claude Code** et de skills (compétences) développées sur mesure. L'objectif est de se créer un agent IA personnel ultra-puissant, autonome et capable de gérer des tâches complexes (comme automatiser l'envoi de rappels, gérer un calendrier, répondre à des messages, piloter des API, interagir avec GitHub et automatiser des flux de travail professionnels) pour booster sa productivité et potentiellement monétiser ces services ou compétences en tant qu'agence/développeur.

---

### 2) Liste des outils, sites et dépôts GitHub cités

* **Ghostty** (Terminal pour macOS)
  * *Prix :* Gratuit (Open Source)
  * *Rôle :* Un émulateur de terminal rapide et esthétique.
* **Raycast** (Application macOS)
  * *Prix :* Gratuit (avec options payantes pour l'IA avancée)
  * *Rôle :* Un launcher de productivité ultime pour macOS (remplace Spotlight, gère le presse-papier, les extensions, etc.).
* **Blackbox**
  * *Prix :* Non précisé
  * *Rôle :* Un outil de recherche / application mentionné brièvement.
* **Arc**
  * *Prix :* Gratuit
  * *Rôle :* Un navigateur web moderne et puissant.
* **Hostinger / Hetzner** (Fournisseurs de VPS)
  * *Prix :* Payant (selon l'abonnement VPS choisi)
  * *Rôle :* Hébergement de serveurs virtuels privés (VPS) pour faire tourner OpenClaw 24/7.
* **Claude Code** (par Anthropic)
  * *Prix :* Nécessite une clé API Anthropic (payante à l'usage / modèle économique des abonnements Anthropic).
  * *Rôle :* Outil en ligne de commande officiel permettant à Claude d'interagir directement avec le terminal, de coder, configurer et résoudre des bugs de manière autonome.
* **Telegram**
  * *Prix :* Gratuit
  * *Rôle :* Interface de chat principale utilisée pour dialoguer et piloter le bot OpenClaw à distance via un bot créé via BotFather.
* **GitHub**
  * *Prix :* Gratuit / Payant
  * *Rôle :* Plateforme de gestion de code pour stocker, versionner et synchroniser les configurations (`claude-workspace`).
* **Google Cloud Console (Google Calendar & Gmail API)**
  * *Prix :* Gratuit (soumis aux quotas Google)
  * *Rôle :* Permet de générer des identifiants OAuth et des clés API pour connecter l'agent IA aux services Google (Gmail et Calendar).
* **Parler** (par Melvyn Malherbe)
  * *Prix :* Gratuit (Open Source)
  * *Rôle :* Application de transcription vocale locale basée sur Whisper (permet de convertir la voix en texte).
* **Whisper / Whisper Turbo / Parler V3** (Modèles OpenAI Whisper)
  * *Prix :* Gratuit (exécuté en local ou via API)
  * *Rôle :* Modèles de reconnaissance vocale et de speech-to-text ultra-rapides.
* **Dub**
  * *Prix :* Gratuit / Payant
  * *Rôle :* Service de gestion et de création de liens courts (`dub.sh`).
* **NPM / Node.js**
  * *Prix :* Gratuit
  * *Rôle :* Environnement d'exécution JavaScript et gestionnaire de paquets pour installer les dépendances.

---

### 3) Astuces concrètes et réutilisables

* **Remplacer Spotlight par Raycast :** Sur macOS, configurer Raycast avec le raccourci `Command + Space` permet de lancer des applications et d'accéder à l'historique du presse-papier de manière instantanée et beaucoup plus fluide.
* **Utiliser Ghostty et configurer les alias :** Installez Ghostty pour un terminal plus rapide et utilisez des alias de commandes (`alias`) pour lancer rapidement des scripts ou des outils complexes sans retaper de longs chemins.
* **Sécuriser son VPS (SSH Hardening) :** Lors du setup d'un VPS, activez les options de sécurité de base (`Fail2ban`, pare-feu UFW, désactivation de l'authentification par mot de passe au profit de clés SSH publiques/privées) pour éviter les accès non autorisés.
* **Le contournement des permissions strictes de Claude Code (`is_sandbox=1`) :** Si Claude Code refuse d'exécuter des actions par sécurité sur le VPS, modifiez le fichier `.bash` ou l'environnement pour définir la variable `CLAUDE_IS_SANDBOX=1` (ou configurer un `bypassPermissions` dans les paramètres de Claude) afin de lui donner les pleins pouvoirs d'exécution sans bloquer l'automatisation.
* **Créer un dépôt Git pour sauvegarder sa configuration (`claude-workspace`) :** Initialiser un dépôt Git sur GitHub pour chaque agent ou VPS configuré permet de sauvegarder l'état de l'agent, ses instructions (`SOUL.md`, `IDENTITY.md`) et de cloner facilement sa configuration sur un autre serveur.
* **Utiliser Telegram comme interface universelle de commande :** Connecter son agent IA à Telegram via un bot personnel permet d'interagir avec son serveur et ses applications à tout moment, directement depuis son téléphone, pour planifier des tâches ou récupérer des infos.
* **Lier des outils de transcription vocale locale (comme Parler/Whisper) :** Intégrer un outil de dictée vocale locale permet de transformer la voix en texte brut instantanément, idéal pour dicter de longs prompts ou des e-mails à son agent IA sans effort.

---

### 4) Chiffres de revenus annoncés
* *Affirmé par l'auteur :* **Non précisé** (la vidéo se concentre uniquement sur l'aspect technique, le setup, l'installation d'OpenClaw, de Claude Code et l'automatisation, sans mentionner de chiffres de gains financiers précis).
