# Codex App ou Claude App : laquelle tu dois utiliser maintenant (comparatif 2026)

Vidéo : https://youtu.be/WD1uMtZJn4Y · durée 29:41 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’auteur compare l’usage des applications de bureau pour le développement assisté par IA : **Codex** (OpenAI) face à l’application **Claude** (Anthropic). Bien qu’il apprécie toujours la qualité d'écriture du modèle Claude, il montre pourquoi l'interface desktop de **Codex** est actuellement plus adaptée aux développeurs avancés (*power users*) grâce à une meilleure gestion du multitâche (agents en tâche de fond), des environnements isolés (*git worktrees* automatisés), de la file d’attente des instructions (*message queuing*), et un navigateur de prévisualisation sans restrictions arbitraires.

---

### 2) Outils, sites et dépôts cités

* **Codex (Desktop App - OpenAI)** :
  * *Statut :* Payant (nécessite un abonnement/plan OpenAI, mention d’un plan à 100 $).
  * *Utilité :* Interface de développement IA permettant de lancer des agents en tâche de fond, gérer les branches Git/PR, inspecter les diffs et automatiser les environnements locaux.
* **Claude / Claude Code (Desktop App & CLI - Anthropic)** :
  * *Statut :* Payant (nécessite un abonnement Claude/Anthropic, mention d'un plan à 200 $).
  * *Utilité :* Outil d'assistance au code et d'exécution d'agents IA en environnement local.
* **T3 Code** :
  * *Statut :* Gratuit / Open source (*non précisé* en détail).
  * *Utilité :* Outil de code IA créé par Theo, mentionné brièvement à titre de comparaison.
* **cmux** :
  * *Statut :* Gratuit / Open source (*non précisé*).
  * *Utilité :* Gestionnaire/multiplexeur de terminaux pour exécuter plusieurs sessions en parallèle (méthode précédente de l'auteur).
* **GitHub** :
  * *Statut :* Gratuit (options payantes).
  * *Utilité :* Hébergement de code, suivi des Pull Requests (PR) et exécution des tests d'intégration continue (GitHub Actions/CI).
* **Lumail.io** :
  * *Statut :* Non précisé (projet SaaS personnel de l'auteur).
  * *Utilité :* Plateforme d’envoi d’emails/newsletters servant d’exemple concret pour le développement de composants.
* **mlv.sh/fa** (ou `mlv.sh/fc`) :
  * *Statut :* Formation offerte / gratuite avec inscription (modules avancés payants non précisés).
  * *Utilité :* Plateforme de formation de l’auteur dédiée à la configuration et l'optimisation de Claude Code et des agents IA.
* **broll.gabin.io** :
  * *Statut :* Non précisé (site web gratuit).
  * *Utilité :* Générateur/éditeur de miniatures YouTube utilisé pour tester l'intégration d'images et d'aperçus dans son application.
* **shadcn/ui** :
  * *Statut :* Gratuit / Open source.
  * *Utilité :* Bibliothèque de composants React pour concevoir rapidement des interfaces modernes et cohérentes.
* **TipTap** :
  * *Statut :* Gratuit / Open source (options pro).
  * *Utilité :* Framework d'édition de texte enrichi intégré dans le projet pour l'éditeur d'emails.

---

### 3) Astuces concrètes et réutilisables

1. **Activer le mode « Full Access / Bypass permissions » :** Évite de valider manuellement chaque lecture/écriture de fichier ou commande terminal, ce qui permet à l'IA de travailler en autonomie complète.
2. **Utiliser le « Message Queuing » (mise en file d'attente) :** Dans Codex, vous pouvez saisir plusieurs retours ou corrections pendant que l'agent travaille. Les instructions s'exécutent séquentiellement une fois la tâche en cours achevée, sans saturer le contexte.
3. **Automatiser les *Git Worktrees* avec des scripts de cycle de vie :**
   * Configurer un script `worktree-up.sh` (qui clone la branche, duplique la base de données locale PostgreSQL, copie les variables `.env` et lance les migrations).
   * Configurer un script `worktree-down.sh` pour nettoyer la base temporaire et fermer les ports une fois la tâche validée.
4. **Déléguer les vérifications à des sous-agents spécialisés :** Utiliser des prompts pour lancer des agents de revue de code (sécurité, performances React, typage TypeScript) avant l'ouverture automatique d'une Pull Request.
5. **Annoter visuellement les éléments à modifier :** Prendre des captures d'écran directement dans le volet *preview* et y apposer des commentaires textuels ciblés pour guider précisément l'IA dans ses modifications CSS/UI.

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de chiffre d'affaires ou de gain financier n'est mentionné** dans la vidéo.
*(Seuls les tarifs d'abonnement aux outils IA ont été évoqués : plan Claude à 200 $/mois et plan Codex à 100 $/mois – affirmé par l'auteur).*
