# Codex peut CONTROLLER ton ordianteur (même quand il est vérouillé)

Vidéo : https://youtu.be/QbZNV321GMs · durée 17:08 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
La vidéo présente les dernières mises à jour majeures apportées à **Codex** (l'environnement de travail pour agents IA développé autour des technologies OpenAI). L'auteur détaille comment ces nouveautés — notamment la capture de contexte instantanée par raccourci clavier (*Appshots*), la gestion d'objectifs itératifs en boucle (*Goal mode*), le navigateur interne avec annotations visuelles et la prise de contrôle d'un Mac verrouillé à distance (*Locked Computer Use*) — améliorent la productivité d'un développeur travaillant avec des agents IA, tout en comparant la fiabilité de Codex à celle de Claude.

---

### 2) Outils, sites et dépôts cités

* **Codex (OpenAI Developers)** : Environnement de travail / client pour agents de code propulsé par OpenAI.  
  * **Statut :** Nécessite des crédits API OpenAI / formule d'accès OpenAI (détail de la tarification exacte de l'app non précisé).  
  * **Utilité :** Exécution d'agents de code autonomes, gestion de projet, interaction avec l'environnement local et automatisation du poste.
* **Claude / Claude Code / Claude App (Anthropic)** : Modèle et assistant de code concurrent.  
  * **Statut :** Version gratuite disponible, abonnements payants (Claude Pro / Team / API).  
  * **Utilité :** Conception d'interfaces (UI), discussion et architecture ; l'auteur explique s'en servir en complément mais le trouver moins stable que l'API d'OpenAI.
* **mlv.sh/fc (Codelynx / AI Agents Setup)** : Script et configuration créés par l'auteur pour configurer des agents IA seniors (Claude Code, Codex CLI, Cursor).  
  * **Statut :** Gratuit (accessible sur inscription par e-mail).  
  * **Utilité :** Installer en une ligne de commande des compétences, rôles et règles de sécurité pour agents de programmation.
* **Thumbfa.st** : Application SaaS créée par l'auteur (générateur de miniatures YouTube par IA).  
  * **Statut :** Freemium / Payant (nécessite des crédits).  
  * **Utilité :** Sert d'exemple réel de projet en production testé et refactorisé en direct avec les agents.
* **Convex** : Plateforme de backend / base de données temps réel.  
  * **Statut :** Gratuit avec paliers payants (non précisé dans la vidéo).  
  * **Utilité :** Backend utilisé dans l'application *Thumbfast*.
* **Vercel** : Plateforme d'hébergement et déploiement cloud.  
  * **Statut :** Gratuit avec options payantes (non précisé dans la vidéo).  
  * **Utilité :** Déploiement du projet web et vérification du statut des builds/CI.
* **NordVPN** : Service de réseau privé virtuel (VPN).  
  * **Statut :** Payant.  
  * **Utilité :** Permet à l'auteur de localiser sa connexion aux États-Unis pour débloquer certains plugins OpenAI non disponibles dans son pays.
* **Spark Mail** : Client de messagerie électronique sur macOS.  
  * **Statut :** Gratuit / Freemium (non précisé dans la vidéo).  
  * **Utilité :** Utilisé pour faire la démonstration de la capture contextuelle multi-application.
* **Apple Notes (macOS)** : Application native de prise de notes d'Apple.  
  * **Statut :** Gratuit (inclus dans macOS).  
  * **Utilité :** Sert de cible pour tester la capture et l'écriture de texte via commandes et scripts d'agents.
* **Helium** : Navigateur web minimaliste / flottant pour Mac.  
  * **Statut :** Gratuit (non précisé dans la vidéo).  
  * **Utilité :** Utilisé pour afficher et vérifier localement le rendu de pages web.
* **Status.claude.com** & **Status.openai.com** : Tableaux de bord publics de suivi de la disponibilité des services Anthropic et OpenAI.  
  * **Statut :** Gratuits.  
  * **Utilité :** Vérifier les pannes et les taux de disponibilité (uptime) des différentes API.

---

### 3) Astuces concrètes et réutilisables

1. **Capture de contexte instantanée (*Appshots*) :**  
   En configurant un raccourci global (comme le double `Cmd + Cmd`), capturez la fenêtre d'une application ou d'un navigateur en cours pour l'injecter immédiatement dans la discussion de l'agent IA, évitant les copier-coller manuels d'erreurs ou de code.
2. **Structuration des objectifs itératifs (*Goal mode*) :**  
   Pour les tâches complexes, définissez explicitement une **intention**, des **conditions de validation** et des **règles**. Cela permet à l'agent de boucler en boucle fermée (modifier le code, relancer les tests, corriger) jusqu'à ce que les critères soient remplis, plutôt que de s'arrêter à une réponse unique.
3. **Spécification visuelle par le navigateur intégré :**  
   Utilisez l'inspecteur intégré de l'environnement pour modifier directement les propriétés CSS (taille de police, marges, bordures) sur la prévisualisation en direct. L'outil génère l'annotation technique exacte que l'agent appliquera sans ambiguïté.
4. **Parallélisation des tâches sur plusieurs agents :**  
   Lancez plusieurs conversations en simultané sur des branches différentes (par exemple : une pour la sécurité, une pour les tests, une pour l'UI) afin de ne pas attendre qu'un agent termine pour avancer sur d'autres aspects du projet.
5. **Contournement des restrictions régionales :**  
   Pour accéder aux plugins expérimentaux en avance de phase (comme *Computer Use*), basculez votre connexion sur une IP américaine via un VPN et relancez l'application.

---

### 4) Chiffres de revenus annoncés

* **Revenus personnels de l'auteur :** Aucun chiffre de chiffre d'affaires ou de gain personnel n'est formulé oralement par l'auteur dans la vidéo (*non précisé*).
* **Affiché à l'écran (tweet tiers à 15:20) :** Un profil Twitter mentionne l'objectif d'atteindre avec Melvyn les **« 10k MRR »** (10 000 $ de revenus récurrents mensuels) (*affirmé par l'auteur du tweet affiché à l'écran*).
