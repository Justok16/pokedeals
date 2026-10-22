# Claude Code fonctionne 100x mieux via cette application

Vidéo : https://youtu.be/QG7aDk5om9I · durée 15:31 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo structuré selon vos critères :

---

### 1) Idée principale
L'auteur présente son flux de travail optimisé pour coder plus efficacement avec **Claude Code** sur macOS, en s'appuyant principalement sur **Cemux** (un terminal multi-onglets avec navigateur web intégré) et **Helium** (un navigateur ultra-léger). L'objectif est d'exécuter et piloter plusieurs instances de Claude Code et d'agents IA en parallèle sans s'encombrer d'environnements lourds ou sur-configurés.

---

### 2) Outils, sites et dépôts cités

*   **Cemux**
    *   **Statut :** Non précisé (gratuit/payant non explicité dans la vidéo).
    *   **Rôle :** Application de terminal pour macOS permettant la gestion multi-projets (espaces de travail, onglets, vues séparées avec navigateur Safari intégré) et le suivi en temps réel de plusieurs sessions de Claude Code.
*   **Claude Code (par Anthropic)**
    *   **Statut :** Non précisé en détail (outil CLI lié aux abonnements/API Anthropic).
    *   **Rôle :** Agent d'IA en ligne de commande utilisé pour générer, déboguer et réviser du code de manière autonome.
*   **Helium**
    *   **Statut :** Non précisé (présenté comme alternative légère).
    *   **Rôle :** Navigateur web très sobre basé sur Chromium, conçu pour consommer très peu de mémoire RAM (~120 Mo contre ~600-700 Mo pour Arc/Chrome) pendant le développement.
*   **Arc**
    *   **Statut :** Gratuit.
    *   **Rôle :** Navigateur web cité à titre de comparaison pour illustrer sa consommation de RAM supérieure à celle d'Helium.
*   **Superset / Conductor**
    *   **Statut :** Non précisé.
    *   **Rôle :** Environnements/éditeurs de code dédiés aux agents IA et aux *git worktrees*, cités comme alternatives que l'auteur trouve trop rigides ou trop complexes par rapport à Cemux.
*   **`mlv.sh/fa` (Masterclass / Formation Claude Code)**
    *   **Statut :** **Gratuit** (*« 100% gratuitement »*, affirmé par l'auteur).
    *   **Rôle :** Plateforme de formation de l'auteur proposant un guide de configuration (Windows/macOS) et des astuces pour utiliser Claude Code et ses agents.
*   **Script `/crab-review` (Configuration personnelle Claude Code)**
    *   **Statut :** Inclus dans la config partagée par l'auteur.
    *   **Rôle :** Commande personnalisée lançant simultanément 15 sub-agents IA pour effectuer une revue complète du code (sécurité, performances, style, etc.).
*   **OpenClaude (sur VPS)**
    *   **Statut :** Payant (**20 $ / mois** pour le serveur VPS, affirmé par l'auteur).
    *   **Rôle :** Installation de Claude Code sur un serveur distant privé.

---

### 3) Astuces concrètes et réutilisables

1.  **Paralléliser les tâches d'IA :** Ouvrir plusieurs onglets dans son terminal pour faire tourner plusieurs instances de Claude Code en même temps (par exemple : un onglet pour coder une fonctionnalité, un autre pour résoudre des erreurs de logs).
2.  **Raccourcis clavier Cemux recommandés :**
    *   `Cmd + T` : Créer un nouvel onglet dans l'espace de travail.
    *   `Ctrl + 1`, `Ctrl + 2`... : Basculer instantanément d'un onglet/session à un(e) autre.
    *   `Cmd + Shift + R` : Renommer l'espace de travail/projet.
3.  **Organisation par Split View (vue partagée) :** Placer le terminal avec Claude Code à gauche et le navigateur intégré à droite affichant l'application en cours d'exécution (`localhost`) pour tester immédiatement les modifications.
4.  **Économie de mémoire système :** Utiliser un navigateur épuré (comme Helium) pendant les sessions de dev pour éviter le gaspillage de RAM causé par les navigateurs plus lourds.
5.  **Revue de code multi-agents :** Utiliser des commandes personnalisées capables de diviser la revue de code entre plusieurs agents spécialisés (sécurité, lisibilité, performances) pour obtenir une analyse plus approfondie sans dépasser les limites de contexte d'un seul agent.

---

### 4) Chiffres de revenus annoncés

*   **Revenus générés :** Non précisé / Aucun chiffre de chiffre d'affaires ou de gain financier n'est mentionné dans la vidéo.
*   **Coût d'infrastructure mentionné :** 20 $ / mois (*affirmé par l'auteur*) pour l'hébergement de son instance sur VPS.
