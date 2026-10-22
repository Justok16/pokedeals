# Comment le top 1 % utilise Claude Code différemment

Vidéo : https://youtu.be/RPS5U6oa03o · durée 17:20 · résumé Gemini (gemini-3-flash-preview) du 2026-10-22
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo pour une application concrète avec **Claude Code** :

### 1) Idée principale
L'approche de l'IA a changé : il ne faut plus utiliser Claude comme un outil de planification, mais comme un **agent autonome**. L'objectif est de passer d'un mode de "planification manuelle" à un système où l'IA exécute, teste et vérifie ses propres tâches en arrière-plan pour créer des "Personal Software" (SaaS personnels) et automatiser des business entiers (YouTube, réseaux sociaux, SAV).

---

### 2) Outils, sites et dépôts cités
*   **Claude Code (Anthropic)** : Outil de terminal (CLI) pour coder avec l'IA. *Payant (coûts API).*
*   **Claude Opus 5.5 & Sonnet 5.5** : Modèles de langage. L'auteur recommande Opus 5.5 pour sa supériorité intellectuelle. *Payant (coûts API).*
*   **DataImpulse** : Service de proxys résidentiels pour éviter d'être bloqué lors du scraping ou de la navigation. *Payant (1$/Go).*
*   **dev-browser (GitHub : SawyerHood/dev-browser)** : Skill permettant à Claude d'ouvrir un navigateur Chrome pour tester ses créations. *Gratuit (Open Source).*
*   **rules-manager (Dépôt Melvynx)** : Outil pour optimiser les instructions de l'IA. *Gratuit (via son dépôt).*
*   **skill-doctor** : Outil interne à Claude pour diagnostiquer les extensions (skills) inutiles. *Gratuit.*
*   **Hermes** : Orchestrateur de tâches en arrière-plan créé par l'auteur pour gérer ses SaaS. *Statut : Non précisé (logiciel personnel).*
*   **BMAD** : Méthodologie de développement pour l'IA, citée mais critiquée comme trop complexe. *Gratuit.*
*   **Convex / Cloudflare / Notion** : Outils de base pour la stack technique des SaaS. *Gratuit/Payant selon l'usage.*

---

### 3) Astuces concrètes et réutilisables
*   **Abandonner le "Plan Mode"** : Ne demandez plus à Claude de planifier. Donnez-lui un **Brief** contenant : 1) La tâche, 2) Les garde-fous (limites), 3) Le critère de fin ("Fini quand...").
*   **Optimiser le fichier CLAUDE.md** : Ce fichier de règles doit faire **moins de 200 lignes**. Trop d'instructions réduisent la performance de 3 % et augmentent le coût de 20 %.
*   **Vérification systématique** : Utilisez le skill `dev-browser` pour que Claude vérifie visuellement le résultat de son code et corrige les erreurs de manière itérative sans votre intervention.
*   **Préférer le CLI au MCP** : Au lieu d'utiliser des connecteurs "clés en main" (comme le connecteur Notion), apprenez à Claude à utiliser les outils en ligne de commande (CLI) officiels, car il est bien plus doué pour manipuler du texte brut.
*   **Sécurité déterministe** : Pour empêcher Claude de faire des bêtises (ex: supprimer des fichiers), n'utilisez pas de consignes textuelles. Utilisez des "hooks" (comme `PreToolUse`) pour bloquer techniquement certaines actions.

---

### 4) Chiffres de revenus
*   **Affirmé par l'auteur** : L'auteur mentionne avoir créé **6 SaaS en solo** grâce à cette méthode. 
*   **Revenus précis** : **Non précisé** (le tableau de bord montre des statistiques de vues et d'abonnés [64,7k sur YouTube], mais pas de chiffres de revenus financiers exacts).
*   **Coûts** : L'auteur mentionne un coût moyen de **0,50 $ à 1,82 $ par tâche** effectuée par l'agent.
