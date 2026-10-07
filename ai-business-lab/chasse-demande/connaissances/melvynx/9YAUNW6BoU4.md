# COMPOSER 2.0 MEILLEUR QUE OPUS pour 10x moins cher ? (oui...)

Vidéo : https://youtu.be/9YAUNW6BoU4 · durée 34:42 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes consignes :

---

### 1) Idée principale
Cursor a introduit **Composer 2** (avec sa variante rapide *Composer 2 Fast*) et **Cursor Glass**, deux innovations majeures dans ses modèles de code et ses interfaces. L'objectif est de proposer des modèles ultra-performants, très économiques par rapport à la concurrence (OpenAI, Anthropic), et une refonte complète de l'expérience utilisateur avec des "agents" intégrés directement dans l'interface de développement pour créer, tester et modifier des applications de manière quasi autonome.

---

### 2) Liste des outils, sites et dépôts GitHub cités

*   **Cursor**
    *   *Type :* Payant / Freemium (tarifs des modèles de Composer 2 : $0,50/M tokens en input, $2,50/M tokens en output).
    *   *Rôle :* Éditeur de code basé sur l'IA (fork de VS Code) intégrant les nouveaux agents Composer et Cursor Glass.
*   **Composer 1.5 / Composer 2 / Composer 2 Fast**
    *   *Type :* Intégré à Cursor (modèles de codage).
    *   *Rôle :* Modèles de code frontières ultra-économiques et performants pour générer, modifier et déboguer du code en mode agent.
*   **Cursorbench**
    *   *Type :* Outil interne à Cursor.
    *   *Rôle :* Benchmark interne pour mesurer la performance, la qualité du code et l'interaction des agents de codage.
*   **Terminal-Bench 2.0 / SWE-bench Multilingual**
    *   *Type :* Benchmarks externes d'évaluation.
    *   *Rôle :* Permettent de tester les capacités des modèles sur des tâches de terminal et de multilinguisme.
*   **Code.melynx.dev** (ou les *testing prompts* de l'auteur)
    *   *Type :* Gratuit (site personnel/ressource de l'auteur).
    *   *Rôle :* Héberge des prompts de test (Bouncing Ball, Rocket Launch, Spongebob 3D, Timezone Checker, YouTube Thumbnail Generator).
*   **Masterclass Claude Code (mlv.sh/fa)**
    *   *Type :* Gratuit / Promotionnel (via le lien de l'auteur).
    *   *Rôle :* Formation pour configurer et maîtriser l'outil *Claude Code* sur Windows et macOS.
*   **Cursor Glass (cursor.com/glass)**
    *   *Type :* Gratuit (inclus dans Cursor).
    *   *Rôle :* Nouvelle interface pour travailler avec les agents de manière claire, intuitive et centralisée (gestion des projets et des fenêtres).
*   **VS Code**
    *   *Type :* Gratuit (Open Source).
    *   *Rôle :* Éditeur de code d'origine sur lequel Cursor était basé, bien que Cursor s'en émancipe désormais en tant que fournisseur de modèles à part entière.

---

### 3) Astuces concrètes et réutilisables

*   **Utiliser les modes Agent et Plan :** Pour les modifications complexes (comme remplacer un texte par un nombre dynamique de vignettes avec calcul de crédits), basculer en mode agent (`Composer Agent`) permet à l'IA de planifier, coder, tester et corriger le code de manière autonome.
*   **Combiner les fenêtres avec `Cmd + Shift + P` -> `Merge All Windows` :** Permet d'avoir une vue multi-fenêtres pour comparer rapidement plusieurs projets ou prompts de test en simultané.
*   **Tirer parti des modèles économiques :** Utiliser *Composer 2* ou *Composer 2 Fast* pour réduire drastiquement les coûts en tokens tout en obtenant des performances comparables, voire supérieures, à des modèles plus onéreux comme GPT-5.4 ou Opus.
*   **Gérer intelligemment le Local Storage et les États (`State`) :** Laisser les agents générer du code propre avec des reducers ou des états centralisés pour éviter la redondance et garder une architecture claire.

---

### 4) Chiffres de revenus annoncés

*   **Revenus annoncés :** **Non précisé** (la vidéo se concentre sur les performances techniques, les coûts d'utilisation des tokens, et l'efficacité des modèles de code, sans mentionner de chiffres d'affaires ou de gains financiers précis pour l'utilisateur).
