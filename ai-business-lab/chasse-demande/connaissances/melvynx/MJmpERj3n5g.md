# Les DEVS sont amoureux de Claude (et arrêtent de vouloir tester de nouvelles choses)

Vidéo : https://youtu.be/MJmpERj3n5g · durée 19:51 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
Ne jamais être « amoureux » d'un outil, d'une entreprise ou d'un modèle d'IA en particulier (comme Anthropic/Claude ou OpenAI). Les développeurs et solopreneurs doivent adopter une approche strictement **pragmatique** et **flexible** : comparer en permanence les coûts réels, les limites d'utilisation (compute/rate limits) et la valeur apportée, afin de basculer instantanément vers l'outil le plus rapide, le plus économique et le plus performant sans subir de verrouillage technologique (*lock-in*).

---

### 2) Outils, sites et dépôts cités

* **Excalidraw (`app.excalidraw.com`)** : 
  * *Statut :* Gratuit (version web de base).
  * *Rôle :* Tableau blanc virtuel utilisé par le créateur pour illustrer sa présentation.
* **Claude / Claude Code / Claude Desktop (Anthropic)** :
  * *Statut :* Payant (abonnements mentionnés à 20 $, 100 $ et 200 $/mois ; usage API payant).
  * *Rôle :* Modèles de langage (notamment Claude Opus) et outils d'assistance au code (CLI Claude Code et application Claude Desktop).
* **Cursor** :
  * *Statut :* Modèle freemium / payant (*non précisé en détail dans la vidéo*).
  * *Rôle :* Éditeur de code assisté par IA.
* **OpenClaw** :
  * *Statut :* *Non précisé*.
  * *Rôle :* Outil / orchestrateur d'agents autonomes utilisé pour déléguer des tâches de développement.
* **Zed** :
  * *Statut :* Gratuit / Open source (*non précisé dans la vidéo*).
  * *Rôle :* Éditeur de code utilisé ici avec le protocole ACP pour exécuter des modèles.
* **Codex / Codex App (OpenAI)** :
  * *Statut :* Inclus/accessible via les forfaits OpenAI / ChatGPT (20 $, 100 $ ou 200 $/mois selon l'usage).
  * *Rôle :* Environnement et CLI d'agents autonomes d'OpenAI permettant de paralléliser des tâches de développement, d'ouvrir des discussions annexes (*side chat*), de créer des pull requests et de gérer les commits.
* **Hermes / Hermes Agent** :
  * *Statut :* *Non précisé*.
  * *Rôle :* Framework/orchestrateur d'agents IA pour le code.
* **OpenCode / T3 Code** :
  * *Statut :* *Non précisé*.
  * *Rôle :* Environnements / orchestrateurs d'agents pour le code cités comme alternatives.
* **Gemini Code (Google)** :
  * *Statut :* Projet futur / hypothétique cité à titre d'exemple.
  * *Rôle :* Potentiel futur concurrent dans le domaine des agents de code.
* **mlv.sh/fc (redirige vers `codelynx.dev`) / AI Blueprint CLI** :
  * *Statut :* Payant (formation / configuration propriétaire de l'auteur).
  * *Rôle :* CLI et ensemble de configurations centralisées pour agents IA (prompts, compétences, scripts de statut, gestion de sauvegardes et liens symboliques).

---

### 3) Astuces concrètes et réutilisables

1. **Découpler la configuration de l'outil pour éviter le *lock-in* :**
   * Centralisez l'ensemble de vos prompts, compétences (*skills*) et instructions d'agents dans un dossier agnostique unique (ex. `.agents/`).
   * Utilisez des **liens symboliques** (*symlinks*) vers les dossiers spécifiques des outils (ex. faire pointer `.claude/` ou les configurations Codex vers le dossier maître `.agents/`). Si vous devez changer d'outil demain, toute votre infrastructure reste intacte.
2. **Mesurer la valeur subventionnée du *compute* :**
   * Surveillez le ratio jetons/prix : un abonnement à 100 $ ou 200 $/mois chez OpenAI ou Claude offre un volume de calcul souvent bien supérieur à ce qu'il coûterait à l'usage pur par API.
   * L'auteur recommande, pour un usage intensif, de souscrire un forfait à 100 $ chez OpenAI et 100 $ chez Claude (ou 200 $ chez l'un lors de gros sprints) pour cumuler le meilleur des deux mondes et éviter les blocages de quotas.
3. **Paralléliser le travail avec des agents :**
   * Plutôt que de tout exécuter séquentiellement dans un terminal, utilisez une interface (comme Codex App) capable de lancer plusieurs sous-agents en arrière-plan pour exécuter des vérifications, des migrations ou des tests pendant que vous continuez à coder.
4. **Pragmatisme sur les forces des modèles :**
   * Réservez les modèles de type Claude Opus pour les tâches exigeant un sens poussé du design et de l'interface.
   * Utilisez les modèles OpenAI (ex. GPT 5.5 / Codex) pour la logique pure d'ingénierie logicielle et l'exécution rapide de code.

---

### 4) Chiffres de revenus annoncés

* **Revenus directs / chiffre d'affaires :** Aucun chiffre de chiffre d'affaires ou de gain généré n'est divulgué (*non précisé*).
* **Économies / Coûts d'infrastructure (*affirmé par l'auteur*) :**
  * L'auteur déclare la règle suivante : *« Chaque dollar que j'économise est un dollar que je gagne »* (*affirmé par l'auteur*).
  * Le blocage par Anthropic sur l'usage intensif via OpenClaw lui aurait coûté environ **50 $ par jour**, soit **1 500 $ par mois** en consommation API (*affirmé par l'auteur*).
  * Selon lui, le forfait à 200 $/mois d'OpenAI équivaudrait à plus de **4 000 $ de valeur de calcul subventionnée** (*affirmé par l'auteur*), contre moins de **2 000 $ à 3 000 $** chez Claude en raison de limites plus strictes (*affirmé par l'auteur*).
