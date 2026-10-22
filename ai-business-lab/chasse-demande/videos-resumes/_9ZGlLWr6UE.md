# Faire travailler Claude Code et Codex ensemble

Vidéo : https://youtu.be/_9ZGlLWr6UE · envoyée par l'utilisateur le 28/09/2026 · résumé Gemini (gemini-3.7-flash) du 2026-09-28
(chiffres et affirmations des auteurs : non vérifiés)

### 1) Idée principale
Plutôt que de choisir exclusivement entre les deux modèles de pointe (**Claude Opus 5.5** d'Anthropic et **GPT-6 Astra** d'OpenAI), la stratégie la plus productive et rentable consiste à **les combiner et les faire collaborer directement sur votre ordinateur** (via leurs interfaces en ligne de commande/applications locales : **Claude Code** et **Codex**). Un modèle peut ainsi déléguer des tâches, générer des images, relayer le travail en cas de limite de quota ou auditer de manière critique les productions de l'autre.

---

### 2) Outils, sites et dépôts cités

* **Claude Code / Application Claude (onglet Code)**
  * *Statut :* Payant (nécessite l'abonnement **Claude Pro** à ~22 €/mois TTC ou Claude Max à 100 €–200 €).
  * *Utilité :* Agent d'exécution local permettant à Claude de lire, créer, modifier des fichiers et lancer des commandes système sur votre machine.
  * *Installation citée :* `curl -fsSL https://claude.ai/install.sh | bash`
* **Codex (CLI OpenAI / `@openai/codex`) & ChatGPT Work**
  * *Statut :* Payant (nécessite l'abonnement **ChatGPT Plus** à ~22,99 €/mois TTC via l'App Store). Inaccessible sur les offres gratuites/Go.
  * *Utilité :* Outil CLI d'OpenAI exécutant du code, gérant des fichiers et permettant l'appel de GPT-6 Astra en local.
  * *Installation citée :* `npm install -g @openai/codex`
* **Extension Chrome (Computer Use)**
  * *Statut :* Payant (inclus dans les offres payantes / abonnements compatibles).
  * *Utilité :* Permet à l'IA de prendre le contrôle du navigateur pour naviguer, cliquer et remplir des formulaires à votre place en réutilisant vos sessions actives.
* **Fichiers de configuration du projet (`AGENTS.md` et `CLAUDE.md`)**
  * *Statut :* Gratuit (fichiers texte Markdown locaux).
  * *Utilité :* `AGENTS.md` centralise l'ensemble des règles métier, consignes et contraintes pour Codex et Claude Code. Dans `CLAUDE.md`, une simple ligne `@AGENTS.md` permet à Claude de synchroniser ses instructions avec celles de Codex.

---

### 3) Astuces concrètes et réutilisables

1. **Interconnexion en langage naturel :** Demandez à Claude d'installer Codex ou d'invoquer Codex avec une commande en ligne de commande (ex. : `codex exec -c model_reasoning_effort=medium "Relis plan.md"`), et inversement.
2. **Harmonisation des règles :** Créez un fichier `AGENTS.md` unique à la racine du projet avec toutes vos exigences, et importez-le dans `CLAUDE.md` avec `@AGENTS.md`.
3. **Optimisation des coûts/tokens :** Comparez les deux modèles sur vos tâches spécifiques. GPT-6 Astra via Codex a tendance à consommer moins de tokens sur les tâches d'exécution rapides grâce à un temps de réflexion plus court.
4. **Délégation croisée de tâches :** Faites rédiger un plan global par Claude en réflexion élevée, puis faites exécuter les tâches répétitives (ex. traduction en masse de 30 fichiers) par Codex.
5. **Gestion du niveau d'effort (*Reasoning Effort*) :**
   * *Medium :* Par défaut pour la grande majorité des tâches (bon équilibre vitesse/coût).
   * *High :* Pour concevoir un plan complexe, une architecture ou une critique.
   * *Extra-High / Max :* À réserver très rarement car très coûteux en quota sans gain systématique.
6. **Création d'images depuis Claude :** Demandez à Claude de déléguer la génération d'images à Codex (qui utilise les modèles d'OpenAI comme GPT Image 2.5), stockant automatiquement les fichiers dans le bon dossier de travail.
7. **Passage de relais en cas de quota épuisé :** Si la limite de messages de Claude ou de ChatGPT est atteinte, demandez à l'autre modèle de lire la dernière conversation dans `~/.claude/projects/...` et de reprendre exactement où le premier s'est arrêté.
8. **Recherche de failles en lecture seule (*Read-Only*) :** Ne demandez pas « Que penses-tu de ce plan ? », mais plutôt une invite stricte : *« Trouve tous les angles morts et toutes les failles de ce plan, en lecture seule »* (`--read-only`), ce qui force une analyse critique impartiale.
9. **Séparation du contrôle et de l'exécution :** Faites fixer les conditions de succès/cahier des charges par un modèle (ex. Codex), faites produire le travail par l'autre (Claude), et faites vérifier le résultat final selon la liste stricte sans modification possible de celle-ci.

---

### 4) Chiffres de revenus annoncés

* **Revenus / Gains financiers :** **Non précisé** (la vidéo ne mentionne aucun chiffre de revenus ou de gains financiers ; elle détaille uniquement le coût des abonnements d'environ **45 €/mois** pour le duo d'outils, *affirmé par l'auteur*).
