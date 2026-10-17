# Claude Code TUE Encore 3 Startup (Claude Review + /loop + /simplify etc.)

Vidéo : https://youtu.be/5EwqKKpLNB0 · durée 21:17 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé complet de la vidéo, structuré selon tes demandes et basé uniquement sur les informations qui y sont présentées :

---

### 1) Idée principale
La vidéo présente les nouveautés de **Claude Code** (outil d'assistance au codage par intelligence artificielle) et des outils/fonctionnalités associés. Pour quelqu'un cherchant à gagner de l'argent ou à optimiser son travail (et donc sa productivité et sa rentabilité) en tant que développeur ou freelance avec Claude Code, ces nouveautés permettent une automatisation accrue, une meilleure gestion des tâches (multitasking, automatisation de PRs, code review automatisé) et une mémoire persistante des projets, réduisant le temps de travail manuel.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Code (Voice Mode)**
    *   **Nom exact :** Claude Code (Voice Mode / commande `/voice`)
    *   **Prix :** Non précisé (fonctionnalité en cours de déploiement progressif).
    *   **Utilité :** Permet d'utiliser la voix pour interagir avec Claude Code, bien que l'auteur émette des réserves sur son efficacité actuelle en français.

*   **cmux**
    *   **Nom exact :** `cmux` (dépôt GitHub / application native macOS)
    *   **Prix :** Gratuit (4,7k étoiles sur GitHub).
    *   **Utilité :** Terminal conçu pour les agents de codage (construit sur Ghostty), avec des onglets verticaux, des notifications visuelles, un navigateur intégré, un support natif Swift, et un système multi-fenêtres pour gérer plusieurs agents en parallèle.

*   **AskUserQuestion (Claude Code / mises à jour d'UI)**
    *   **Nom exact :** Fonctionnalité `AskUserQuestion` dans Claude Code
    *   **Prix :** Inclus dans Claude Code (non précisé si payant ou gratuit).
    *   **Utilité :** Permet à Claude de proposer des interfaces utilisateur (UI) et des snippets Markdown interactifs (diagrammes, code, choix multiples) directement dans le terminal.

*   **Commandes `/simplify` et `/batch`**
    *   **Nom exact :** `/simplify` et `/batch`
    *   **Prix :** Inclus dans Claude Code.
    *   **Utilité :** 
        *   `/simplify` : Lance une analyse par plusieurs agents en parallèle pour simplifier le code et le nettoyer.
        *   `/batch` : Permet d'exécuter des migrations de code ou des tâches répétitives en parallèle à travers de multiples agents (worktrees).

*   **Auto-mémoire (`CLAUDE.md`)**
    *   **Nom exact :** `CLAUDE.md` / Auto-memory
    *   **Prix :** Inclus dans Claude Code.
    *   **Utilité :** Permet à Claude de se souvenir automatiquement des contextes, préférences, corrections et instructions entre différentes sessions de travail.

*   **Commandes `/loop` / Tâches planifiées (`scheduled tasks`)**
    *   **Nom exact :** `/loop` ou la planification de tâches (`cron`)
    *   **Prix :** Inclus dans Claude Code.
    *   **Utilité :** Permet de lancer des tâches de manière récurrente (ex. : vérifier les tests toutes les 2 minutes, lancer des actions à heure fixe).

*   **Configuration Claude Code (Lien d'accès de l'auteur)**
    *   **Nom exact :** `MLV.SH/FC` (lien fourni par l'auteur pour récupérer sa configuration de Claude Code : agents, commandes, scripts, etc.).
    *   **Prix :** Non précisé.
    *   **Utilité :** Permet de télécharger la configuration personnelle de l'auteur pour Claude Code.

*   **Code Review (Claude Code)**
    *   **Nom exact :** Code Review
    *   **Prix :** Payant (basé sur l'utilisation de jetons / *token usage*, estimé entre 15 $ et 25 $ par revue selon la complexité, payé par PR).
    *   **Utilité :** Permet à Claude de faire une revue de code automatisée sur les Pull Requests (PR) pour détecter les bugs et assurer la qualité du code.

---

### 3) Astuces concrètes et réutilisables

*   **Utiliser les fenêtres verticales (`cmux`) :** Multiplier les fenêtres de terminal en colonnes et lignes pour faire du multitâche efficace avec plusieurs agents IA en même temps.
*   **Automatiser les revues de code (`/simplify` et `/batch`) :** Lancer des agents en parallèle pour nettoyer le code ou appliquer des migrations sur plusieurs fichiers avant de créer des Pull Requests.
*   **Documenter avec la mémoire automatique (`CLAUDE.md`) :** Laisser Claude consigner ses propres instructions et règles de projet dans un fichier de mémoire pour ne pas avoir à répéter les mêmes prompts à chaque session.
*   **Planifier des boucles de vérification (`/loop`) :** Programmer des boucles récurrentes (ex. : `/loop` toutes les 2 minutes pour vérifier si les tests passent et corriger automatiquement les erreurs) pour automatiser le travail de maintenance et de correction.
*   **Structurer ses prompts avec `AskUserQuestion` :** Demander à Claude de proposer plusieurs options ou structures de code sous forme de choix interactifs pour valider rapidement une direction technique.

---

### 4) Chiffres de revenus annoncés (marqués « affirmé par l'auteur »)

*   **Coût horaire d'un ingénieur (basé sur 2080h/an à San Francisco) — *Affirmé par l'auteur via la documentation montrée dans la vidéo* :**
    *   **Junior :** 120k$ à 150k$ par an, soit **658 $ à 72 $ / heure** (selon la transcription affichée, l'auteur lit les chiffres de la table).
    *   **Mid (Médian) :** 160k$ à 200k$ par an, soit **77 $ à 96 $ / heure**.
    *   **Senior :** 200k$ à 300k$ par an, soit **96 $ à 144 $ / heure**.
    *   **Staff / Principal :** 140k$ à 240k$ par heure (ou de l'ordre de 144 $ à 240 $ / heure selon le calcul présenté).
*   **Coût de la fonctionnalité Code Review — *Affirmé par l'auteur* :**
    *   Généralement entre **15 $ et 25 $** par revue, payé sur la base de l'utilisation de jetons (*token usage*), augmentant selon la complexité de la Pull Request.
*   **Statistiques de performance de Code Review (données d'Anthropic citées par l'auteur) — *Affirmé par l'auteur* :**
    *   Les revues avec des commentaires substantiels sont passées de **16 % à 54 %**.
    *   Moins de **1 %** des revues sont marquées comme incorrectes.
    *   Sur les grandes PR (>1000 lignes), **94 %** des bugs sont trouvés directement par Claude Review.
