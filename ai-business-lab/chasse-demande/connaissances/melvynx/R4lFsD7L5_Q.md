# Apprendre les Worktrees avec Codex en 30 minutes

Vidéo : https://youtu.be/R4lFsD7L5_Q · durée 28:09 · résumé Gemini (gemini-3.5-flash) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, spécialement conçu pour comprendre comment utiliser Codex, Git et l'IA pour optimiser le flux de travail de développement :

---

### 1) L'idée principale
La vidéo explique comment démultiplier sa productivité en utilisant les **Worktrees Git** combinés avec des agents d'intelligence artificielle (via l'outil **Codex**). Plutôt que de faire travailler l'IA sur une seule branche à la fois dans un unique dossier local, l'utilisation de worktrees permet de créer des environnements de travail locaux séparés. Cela permet de lancer plusieurs agents IA en parallèle sur différentes tâches (comme du refactoring, du design ou l'ajout de pages) sans bloquer ou corrompre la branche principale (`main`), avant de tout fusionner proprement.

---

### 2) Outils, sites ou dépôts GitHub cités

*   **Codex** : Plateforme / outil de développement assisté par IA qui orchestre les agents.
    *   *Tarif* : Payant (*tarif exact de l'abonnement non précisé*, mais la formation dédiée à l'outil est vendue au prix de **99 €**).
    *   *Usage* : Permet de donner des instructions en langage naturel pour coder, configurer des environnements et gérer le cycle de vie du code (Git, commits, PRs).
*   **GitHub (github.com)** : Service d'hébergement et de gestion de dépôts de code Git.
    *   *Tarif* : Gratuit (pour les comptes de base).
    *   *Usage* : Utilisé pour héberger les projets, stocker les branches et créer des Pull Requests (PR).
*   **Environments Manager (`$environments-manager`)** : Compétence (skill) intégrée à Codex.
    *   *Tarif* : Gratuit / Intégré dans Codex.
    *   *Usage* : Automatise la configuration de l'environnement de développement pour chaque nouveau worktree (copie des fichiers `.env` ignorés, installation des dépendances via `npm`, allocation de ports, etc.).
*   **safe-ship** : Compétence interne à Codex.
    *   *Tarif* : Gratuit / Intégré dans Codex.
    *   *Usage* : Utilisé par l'IA pour contrôler l'état Git, valider les fichiers, effectuer les commits et pousser le code sur GitHub.
*   **Portly** : Superviseur d'environnement local pour macOS (brièvement visible à l'écran).
    *   *Tarif* : *Non précisé*.
    *   *Usage* : Permet de visualiser et de gérer les serveurs locaux en cours d'exécution.
*   **Zoxide** : Outil en ligne de commande.
    *   *Tarif* : Gratuit (Open source).
    *   *Usage* : Permet de naviguer rapidement dans les répertoires (génère une erreur dans le terminal de l'auteur car non installé dans l'environnement du worktree).
*   **Dépôt GitHub `Melvynx/lumail.io`** : Dépôt personnel de l'auteur.
    *   *Tarif* : *Non précisé*.
    *   *Usage* : Projet de système d'envoi d'emails utilisé par l'auteur comme exemple de refactoring lourd géré par un worktree.
*   **Dépôt GitHub `formation-codex`** : Dépôt de test créé pour la démonstration.
    *   *Tarif* : Gratuit / Privé.
    *   *Usage* : Sert de support pratique pour montrer l'initialisation de l'outil et l'envoi vers GitHub.
*   **Site `mlv.sh/fa` (Mini-formation AI Engineer)** : Page de destination de l'auteur.
    *   *Tarif* : Gratuit.
    *   *Usage* : Permet de s'inscrire à une formation d'introduction pour apprendre à coder 10 fois plus vite avec l'IA.
*   **Site `mlv.sh/fc` (Formation Codex complète)** : Page d'achat de la masterclass de l'auteur.
    *   *Tarif* : Payant (**99 €**).
    *   *Usage* : Permet d'acheter la formation complète pour maîtriser l'outil Codex.

---

### 3) Les astuces concrètes et réutilisables

*   **Séparer les environnements avec Git Worktree** : Au lieu de simplement changer de branche (ce qui bloque votre répertoire de travail sur une seule version du code), utilisez les worktrees pour cloner temporairement votre projet dans des dossiers séparés. Cela permet de faire tourner simultanément plusieurs serveurs locaux sur différentes versions de votre code.
*   **Éviter les conflits de ports réseaux** : Lors du lancement simultané de plusieurs applications locales avec l'IA, configurez vos scripts de démarrage pour attribuer un port unique par worktree (ex. port `3910` pour un agent, port `3002` pour un autre, port `3003` pour un troisième), évitant ainsi que les serveurs locaux ne se bloquent mutuellement.
*   **Exploiter les canaux parallèles avec `/side` ou `/parallel`** : Dans Codex, utilisez ces commandes pour ouvrir une discussion parallèle sur le même worktree. Cela permet de donner de nouvelles consignes à l'IA ou de corriger des détails sans perdre l'historique et le contexte de la tâche en cours.
*   **Déléguer la résolution de conflits Git à l'IA** : En cas de conflit lors d'une fusion de branche (merge), écrivez simplement à l'agent : *"fix les conflits et merge"*. L'IA analysera les différences, choisira les modifications prioritaires et finalisera la fusion de manière autonome.

---

### 4) Les chiffres de revenus annoncés

*   **Plus de 200 000 $ (200k$+) par an** : Salaire annuel potentiel estimé pour le rôle d'**AI Engineer** (*affirmé par l'auteur* sur sa page de présentation `mlv.sh/fa`).
