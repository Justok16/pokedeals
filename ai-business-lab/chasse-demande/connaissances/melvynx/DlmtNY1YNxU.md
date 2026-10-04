# Codex : contrôle ton ordinateur et ton VPS avec ton iPhone

Vidéo : https://youtu.be/DlmtNY1YNxU · durée 12:40 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
La vidéo présente l'intégration mobile et le contrôle à distance de **Codex** (l'application d'OpenAI) via l'application smartphone ChatGPT. Cette configuration permet de piloter à distance son ordinateur ou des serveurs distants (VPS via SSH) afin de lancer, superviser et débugger des agents IA de code, exécuter des commandes Docker ou automatiser le navigateur depuis un smartphone, assurant un workflow de développement en multitâche permanent.

---

### 2) Outils, sites et dépôts cités

* **Codex (Desktop & Mobile - OpenAI)**  
  * **Statut :** Non précisé (associé à l'écosystème ChatGPT / OpenAI).  
  * **Rôle :** Environnement d'agent de développement IA permettant d'exécuter des tâches de code, de gérer des projets et de synchroniser des sessions avec l'application mobile.
* **ChatGPT (application mobile iOS / Android)**  
  * **Statut :** Gratuit / Freemium (non précisé en détail).  
  * **Rôle :** Sert d'interface mobile pour contrôler les sessions Codex et les connexions SSH à distance.
* **iPhone Mirroring**  
  * **Statut :** Gratuit (fonctionnalité native macOS / iOS).  
  * **Rôle :** Utilisé dans la vidéo pour afficher et manipuler l'écran de l'iPhone directement sur l'écran du Mac.
* **Coolify**  
  * **Statut :** Gratuit / Open source (auto-hébergé sur VPS).  
  * **Rôle :** Plateforme PaaS / gestionnaire de conteneurs Docker tournant sur un VPS distant (Ubuntu), administrable via des invites textuelles Codex.
* **OpenClaw / Hermes (steve-openclaw)**  
  * **Statut :** Non précisé.  
  * **Rôle :** Agent / assistant IA autonome déployé sur un VPS distant.
* **NordVPN**  
  * **Statut :** Payant (l'auteur précise l'avoir obtenu via son abonnement Revolut).  
  * **Rôle :** Permet de localiser la connexion aux États-Unis pour débloquer des fonctionnalités indisponibles en Europe.
* **Revolut**  
  * **Statut :** Payant (formule d'abonnement mentionnée).  
  * **Rôle :** Service bancaire mentionné pour l'inclusion d'un compte VPN.
* **Extension Chrome Codex (OpenAI Developers / Chrome Web Store)**  
  * **Statut :** Gratuit.  
  * **Rôle :** Extension permettant à l'agent Codex de piloter le navigateur Google Chrome.
* **Plugin "Computer Use" (Codex)**  
  * **Statut :** Non précisé (intégré à Codex).  
  * **Rôle :** Permet à l'IA d'interagir visuellement avec le système d'exploitation et de contrôler des applications locales.
* **YouTube Music**  
  * **Statut :** Non précisé.  
  * **Rôle :** Utilisé en guise de test d'interaction d'interface via le plugin *Computer Use*.
* **mlv.sh / codelynx.dev**  
  * **Statut :** Payant (formation payante / page d'inscription).  
  * **Rôle :** Site de l'auteur pour sa formation dédiée au codage avec l'IA.

---

### 3) Astuces concrètes et réutilisables

* **Superviser et coder sur un VPS distant depuis son smartphone :**  
  Dans les réglages de Codex Desktop (`Settings` > `Connections` > onglet `SSH`), ajoutez l'adresse IP et les accès de vos serveurs (VPS, instances Docker, etc.) et activez l'option *« Available from signed-in devices »*. Cela permet d'exécuter des tâches de développement ou d'administration système directement depuis l'application mobile ChatGPT.
* **Débogage de secours en déplacement :**  
  Si un agent autonome ou un bot (par exemple Telegram) plante à cause d'une coupure du serveur d'entrée (*gateway*), vous pouvez utiliser l'accès SSH via Codex Mobile pour analyser l'état des conteneurs Docker et réparer le problème sans avoir besoin d'ouvrir votre ordinateur.
* **Contourner le blocage géographique des plugins Codex :**  
  Certains plugins (*Computer Use*, extension Chrome Codex) ne sont pas listés pour les utilisateurs situés en Europe. L'utilisation d'un VPN connecté aux États-Unis (ex. New York) permet de les afficher et de les installer.
* **Accorder les permissions adaptées pour l'autonomie :**  
  Pour laisser un agent travailler en continu sur un serveur ou une branche Git sans interruption manuelle à chaque action, ajustez la politique d'approbation sur *« Full access »* ou modifiez l'*Approval policy* dans les réglages de configuration.
* **Standardiser le contexte avec un fichier `AGENTS.md` :**  
  Créer un fichier `AGENTS.md` à la racine d'un projet permet de définir formellement le rôle de la machine ou de l'agent (ex. architecture, rôle d'assistant domestique, chemins d'accès), ce qui évite d'avoir à recontextualiser chaque nouvelle session de chat.

---

### 4) Chiffres de revenus annoncés
* **Revenus financiers :** Non précisé (aucun chiffre de gain monétaire n'est mentionné).  
* **Autres chiffres annoncés (*affirmé par l'auteur*) :**  
  * Plus de 13 000 inscrits sur sa page de formation.  
  * Promesse d'« économiser 500h de R&D » et de « coder 3x plus vite » (puis 10x plus vite).
