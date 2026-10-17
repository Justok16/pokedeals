# Supprime tes skills maintenant (ou fais ça à la place)

Vidéo : https://youtu.be/GUvJsd964fA · durée 17:09 · résumé Gemini (gemini-3.8-flash) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
La « méta » des instructions et compétences (*skills*) pour les agents de programmation IA (Claude Code, Cursor, Codex) a radicalement changé. Avec les nouveaux modèles de raisonnement (comme Astra, Sol, Fable, etc.), les prompts et fichiers de règles trop longs, détaillés ou chargés de mémoire créent du « slop » (bruit, contradictions et baisse de performance). Pour maximiser l'efficacité et la productivité, la nouvelle règle d'or est la **simplicité radicale** : épurer massivement les fichiers de configuration (*skills* ramenés à quelques lignes percutantes), purger les mémoires/règles superflues et empêcher l'auto-invocation involontaire des outils par le modèle.

---

### 2) Outils, sites et dépôts cités

* **Claude Code** (Anthropic)
  * **Statut :** Payant (via abonnement / consommation API Anthropic).
  * **Usage :** Agent IA de codage en ligne de commande.
* **Cursor**
  * **Statut :** Gratuit / Freemium (version Pro payante).
  * **Usage :** Éditeur de code assisté par IA avec gestion d'agents et de règles personnalisées.
* **Codex** (OpenAI)
  * **Statut :** Payant (via API OpenAI).
  * **Usage :** Agent / environnement de génération de code IA.
* **Zed**
  * **Statut :** Gratuit (open-source).
  * **Usage :** Éditeur de code (visible dans la liste des interfaces d'agents).
* **AIBlueprint CLI (`docs.aiblueprint.dev`)**
  * **Statut :** Freemium (catalogue de base gratuit, catalogue de *skills* « PRO » payant).
  * **Usage :** Outil CLI (`npx aiblueprint-cli`) pour installer et synchroniser une configuration d'agents, de *skills* et de raccourcis partagés entre Claude Code, Cursor et Codex via des liens symboliques (*symlinks*).
* **Formation / Config Melvynx (`mlv.sh/fc`)**
  * **Statut :** Payant.
  * **Usage :** Espace proposant la configuration complète prête à l'emploi et les *skills* optimisés créés par l'auteur.
* **Dépôt GitHub (`melvynx/agents-config`)**
  * **Statut :** Gratuit (dépôt visible à l'écran).
  * **Usage :** Dépôt personnel de l'auteur contenant ses fichiers Markdown de compétences (`SKILL.md`) et configurations multi-agents.
* **DeepSWE Blog (`deepswe.datacurve.ai/blog`)**
  * **Statut :** Gratuit.
  * **Usage :** Benchmark indépendant évaluant les performances des modèles d'IA sur des tâches d'ingénierie logicielle (SWE).
* **X / Twitter**
  * **Statut :** Gratuit.
  * **Usage :** Veille technologique pour dénicher et tester les nouveaux *skills* créés par la communauté IA.

---

### 3) Astuces concrètes et réutilisables

1. **Raccourcir drastiquement la taille des *skills* :** Inutile de sur-expliquer comment réaliser une tâche (ex. comment faire une *code review* ou un *commit*). Le modèle sait déjà le faire. L'auteur a par exemple réduit un *skill* de 91 lignes à 17 lignes, et un autre de 3 000 lignes à 31 lignes. Donnez uniquement les étapes clés et les contraintes strictes.
2. **Désactiver l'auto-invocation du modèle (`disable-model-invocation: true`) :**
   * Dans Claude : ajouter `disable-model-invocation: true` dans l'en-tête du fichier de *skill*.
   * Dans l'écosystème OpenAI : définir `policy: allow_implicit_invocation: false`.
   * *Raison :* Si le modèle charge la description de 100 *skills* en permanence dans sa fenêtre de contexte, cela consomme des tokens inutilement et dégrade sa capacité de raisonnement. Ne laissez le modèle s'auto-invoquer que pour les outils d'assistance courante (ex. gestion des emails, récupération de documentation), et déclenchez les gros workflows manuellement (ex. `/apex`).
3. **Purger la mémoire et archiver l'inutile :** Créer un dossier `.archive/` (ou `.agents/archive/`) pour y déplacer tous les *skills* et règles non utilisés au lieu de les laisser polluer l'espace de travail.
4. **Créer un *skill* de vérification (`verify`) :** Mettre en place un prompt/skill strict qui oblige l'IA à tester le code, capturer des preuves réelles (captures d'écran, logs d'erreurs, tests de validation) et ne valider une tâche qu'avec un critère observable (`PASS` ou `NOT PROVEN`).
5. **Utiliser des liens symboliques (*symlinks*) :** Centraliser la configuration de vos agents dans un seul dossier et la lier à vos différents outils (Cursor, Claude Code, etc.) pour éviter d'avoir à réécrire ou synchroniser manuellement vos règles entre chaque environnement.

---

### 4) Chiffres de revenus annoncés

* **Revenus financiers :** **Non précisé** (l'auteur ne mentionne aucun montant en euros ou en dollars, ni chiffre d'affaires).
* *Note sur les métriques partagées par l'auteur (affirmé par l'auteur) :* Il indique avoir réuni **9 927 utilisateurs sur son offre gratuite** et **environ 500 clients sur son offre payante**.
