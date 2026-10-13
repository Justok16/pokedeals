# Apprendre GIT en 1 HEURE (Tout comprendre en 2025)

Vidéo : https://youtu.be/_WBBiGiCOEA · durée 1:00:22 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo en français, structuré selon vos consignes :

### 1) Idée principale
La vidéo est un tutoriel complet d’une heure pour apprendre à utiliser **Git** et **GitHub**, de zéro à la collaboration sur un dépôt distant, en passant par la configuration, les commandes de base (init, add, commit, log, status, diff, restore, rm), la gestion des branches et le *merging*. Le formateur présente aussi brièvement sa plateforme de formation payante *BeginWeb* pour devenir développeur web.

---

### 2) Outils, sites et dépôts GitHub cités
*   **Git** : Outil de contrôle de version (gratuit, open source).
*   **GitHub** (site : `github.com`) : Plateforme d’hébergement de code et de gestion de dépôts Git (gratuit pour les fonctionnalités de base).
*   **VS Code (Visual Studio Code)** : Éditeur de code / IDE utilisé pour le tutoriel (gratuit).
*   **GitKraken** : Client Git graphique (version gratuite/payante non précisée).
*   **GitHub Desktop** : Client Git graphique officiel de GitHub (gratuit).
*   **Vim** : Éditeur de texte en ligne de commande (gratuit).
*   **ChatGPT** (site : `chatgpt.com`) : IA conversationnelle utilisée pour poser des questions de configuration et de commandes Git (gratuit/payant, non précisé).
*   **Excalidraw** (site : `app.excalidraw.com`) : Outil de dessin et de schématisation utilisé pour expliquer le fonctionnement de Git (gratuit).
*   **BeginWeb / Codelynx** (site : `mlv.sh/git` ou `codelynx.dev`) : Plateforme de formation payante du créateur pour devenir développeur web (cours, exercices, playgrounds interactifs).
*   **GitLens** : Extension VS Code pour visualiser l'historique des commits et le graphe des branches (gratuite).

---

### 3) Astuces concrètes et réutilisables
*   **Vérifier l'installation de Git** : `git --version`.
*   **Configurer son identité globale** : 
    *   `git config --global user.name "Ton Nom"`
    *   `git config --global user.email "[adresse e-mail retirée]"`
*   **Lier VS Code au terminal** : Dans VS Code, ouvrir la *Command Palette* (Ctrl/Cmd + Shift + P) et taper `Shell Command: Install 'code' command in PATH`.
*   **Définir l'éditeur par défaut** : `git config --global core.editor "code --wait"`.
*   **Gérer les fins de ligne multi-plateformes (Windows vs Mac/Linux)** : 
    *   Sur Windows : `git config --global core.autocrlf true`
    *   Sur Mac/Linux : `git config --global core.autocrlf input`
*   **Activer l'autocorrection des commandes Git** : `git config --global help.autocorrect 1`.
*   **Activer l'autocomplétion (auto-correct des branches, etc.)** : `git config --global help.autocorrect 7s` (ou `true`).
*   **Initialiser un dépôt** : `git init`.
*   **Créer un fichier `.gitignore`** : Pour exclure du suivi Git certains fichiers ou dossiers sensibles/générés (ex: `node_modules`, mots de passe, etc.).
*   **Visualiser l'historique de manière lisible** : 
    *   `git log --oneline` (affichage condensé sur une ligne).
    *   `git log --pretty=format:...` (affichage personnalisé avec hash, date, auteur, message).
*   **Afficher les dossiers/fichiers cachés (sous macOS)** : Raccourci `Cmd + Shift + .` dans le Finder.
*   **Supprimer un fichier du suivi Git sans le supprimer du disque** : `git rm --cached <fichier>`.
*   **Annuler les modifications locales non stagées d'un fichier** : `git restore <fichier>`.
*   **Réinitialiser un commit non poussé** : `git reset --soft HEAD~1`.
*   **Gérer les branches** : 
    *   Créer et basculer sur une branche : `git switch -c <nom-de-branche>` (ou `git checkout -b`).
    *   Fusionner une branche : `git merge <nom-de-branche>`.
*   **Connecter un dépôt local à GitHub** : `git remote add origin <URL-du-repo>` puis `git push -u origin main`.
*   **Récupérer les modifications distantes** : `git pull` (ou `git fetch` + `git merge`).

---

### 4) Chiffres de revenus annoncés
*   **Non précisé** (aucun chiffre de revenus n'est mentionné dans la vidéo, hormis le nombre d'élèves inscrits sur la plateforme *BeginWeb* affiché à l'écran : « 105 étudiants »).
