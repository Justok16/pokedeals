# Zed AI Agents : La nouvelle feature Zed qui change TOUT

Vidéo : https://youtu.be/0b8uthIvixw · durée 12:50 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'éditeur de code **Zed** intègre désormais le protocole standard ouvert **ACP (Agent Client Protocol)**. Cela permet d’utiliser dans une même interface unifiée et légère différents agents de programmation IA (Claude Agent / Claude Code, Cursor, Codex CLI, OpenCode, etc.) en exploitant directement vos abonnements ou clés existants, sans surcoût d'API interne imposé par l'éditeur.

---

### 2) Outils, sites et protocoles cités

* **Zed (`zed.dev`)**
  * **Prix :** Gratuit (version *Personal*) / 10 $/mois (version *Pro* avec crédits de tokens inclus).
  * **Utilité :** Éditeur de code natif en Rust très performant, gérant les Git Worktrees, le multi-dépôt et l'intégration directe de plusieurs agents IA.
* **Agent Client Protocol (ACP)**
  * **Prix :** Gratuit / Protocole open-source.
  * **Utilité :** Standard de communication permettant de connecter des agents d'IA externes directement à l'interface de Zed.
* **Claude Agent / Claude Code**
  * **Prix :** Gratuit ou payant selon votre clé API / abonnement Anthropic.
  * **Utilité :** Agent d'IA autonome en ligne de commande pour générer, modifier et analyser du code.
* **Codex CLI / Codex**
  * **Prix :** Payant (via abonnement / consommation d'API).
  * **Utilité :** Agent d'aide au développement et complétion de code.
* **Cursor (Agent / Cursor SDK / Composer 2)**
  * **Prix :** Payant (via abonnement Cursor).
  * **Utilité :** Outil de génération et d'édition de code par IA, utilisable directement dans Zed sans ouvrir l'application Cursor.
* **OpenCode (`opencode.ai`)**
  * **Prix :** Formule payante (mentionné à 5 $/mois d'essai / tarification low-cost selon modèle).
  * **Utilité :** Accès à des modèles de code open-source via API/CLI.
* **`mlv.sh/fa` (Plateforme de formation CodeLynx)**
  * **Prix :** Gratuit (au moment de la vidéo).
  * **Utilité :** Mini-formation proposée par l'auteur pour configurer Claude Code, ses agents, sa *statusline* et ses scripts de workflow.
* **Autres agents mentionnés dans le registre ACP de Zed :**
  * *Agonogentic, Amp, Auggie Code, AutoHand Code, Cline, Codebuddy Code, Factory Droid, Gemini CLI, Goose, Mistral Vibe, Nova, Qwen Code, etc.* (Utilité : Agents de développement alternatifs).

---

### 3) Astuces concrètes et réutilisables

1. **Centraliser plusieurs IA dans une interface unique :** Au lieu de jongler entre plusieurs applications lourdes (Cursor, terminal Codex, Claude Code), connectez tous vos abonnements dans Zed via le registre **ACP Registry** (Menu *Settings > External Agents*).
2. **Économiser sur les coûts d'API :** Utiliser ACP permet d'exploiter directement vos abonnements existants sans payer de surtaxe de plateforme.
3. **Mise en parallèle (Multi-thread) :** Ouvrez plusieurs onglets de chat dans Zed avec des agents différents (ex. : demander une explication à GPT-5 via Codex, lancer une tâche de refactorisation sur Cursor Composer 2 et une analyse sur Claude Agent en parallèle).
4. **Mode Follow / Visualisation temps réel :** Activez l'option *Follow* pour que Zed affiche automatiquement les fichiers édités par l'agent IA au fil de ses modifications.
5. **Gestion multi-dépôts et Git Worktrees :** Utilisez la navigation native de Zed pour basculer facilement entre plusieurs branches de travail sans faire crasher l'environnement.

---

### 4) Chiffres de revenus annoncés

* **Revenus :** *Non précisé* (aucun chiffre de revenus n'est mentionné par l'auteur dans cette vidéo).
