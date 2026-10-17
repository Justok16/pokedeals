# Comment ONE-SHOT toutes tes features avec l'IA (fais-la travailler pendant 2 heures non-stop)

Vidéo : https://youtu.be/_vpxSaUTJzI · durée 23:29 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur détaille une méthodologie en plusieurs étapes pour implémenter des fonctionnalités logicielles très complexes en « one-shot » (ou quasi one-shot) avec des agents d'intelligence artificielle (notamment **Claude Code**). Plutôt que de déléguer la conception aveuglément à l'IA, le développeur doit investir du temps en amont pour cadrer précisément le plan produit (« ping-pong » de cadrage), puis exécuter le code via un workflow structuré combinant plusieurs agents spécialisés (développement, audit de sécurité/code) et une boucle de rétroaction autonome via un navigateur réel pour vérifier et corriger l'interface.

---

### 2) Outils, sites et dépôts cités

* **Claude Code / Claude (Anthropic)**
  * *Statut :* Payant (nécessite une clé API ou un abonnement selon l'usage).
  * *Rôle :* Agent d'assistance au développement en ligne de commande pour explorer, coder, tester et débugger.
* **Codex (application / interface Codex)**
  * *Statut :* Non précisé (associé aux modèles d'IA / interface d'agents).
  * *Rôle :* Outil d'interaction avec les agents pour concevoir les spécifications et lancer les tâches.
* **Zed (`zed.dev`)**
  * *Statut :* Gratuit (open-source).
  * *Rôle :* Éditeur de code utilisé pour coder, visualiser les fichiers markdown et piloter des agents intégrés pour les retouches rapides.
* **dev-browser (dépôt GitHub : `SawyerHood/dev-browser`)**
  * *Statut :* Gratuit (open-source).
  * *Rôle :* Skill/outil CLI permettant à Claude Code de manipuler un navigateur Chromium/Playwright, cliquer sur des boutons, inspecter les pages et vérifier le bon fonctionnement de l'application en conditions réelles.
* **Excalidraw (`excalidraw.com`)**
  * *Statut :* Gratuit (version en ligne freemium).
  * *Rôle :* Tableau blanc virtuel utilisé par l'auteur pour illustrer les concepts de contextes et de workflow.
* **mlv.sh/fa / mlv.sh/fc (CodeLynx - Formation / Setup de l'auteur)**
  * *Statut :* Gratuit (annoncé comme formation gratuite par l'auteur dans la vidéo).
  * *Rôle :* Page de configuration et formation pour installer le setup Claude Code, commandes et agents personnalisés.
* **Convex**
  * *Statut :* Freemium (non précisé dans la vidéo, mais plateforme backend tierce).
  * *Rôle :* Backend réactif/base de données utilisé dans l'un des exemples pour interroger les logs et les tables.
* **Stripe**
  * *Statut :* Service commercial de paiement (frais par transaction).
  * *Rôle :* Gestion des abonnements testée en direct par l'agent IA via le navigateur.
* **Lumail.io & NowTS**
  * *Statut :* Projets SaaS présentés en démo (applications propriétaires).
  * *Rôle :* Cas pratiques pour illustrer le développement d'un moteur de workflow complet et d'un flux d'upgrade de forfait.

---

### 3) Astuces concrètes et réutilisables

1. **La règle de l'input précis (le « Ping-Pong » de planification) :**
   * Ne jamais demander à l'IA de coder une fonctionnalité complexe d'un seul coup.
   * Utiliser une commande de type `/brainstorm` pour lister exhaustivement les critères, règles métier et spécifications.
   * Faire relire et critiquer le plan par un second modèle ou un second chat pour relever les incohérences avant d'écrire la moindre ligne de code.
   * Sauvegarder le plan final dans un fichier Markdown dédié (ex. `workflow-v2.md`).

2. **Éviter le phénomène *« Lost in the middle »* (découverte progressive des prompts) :**
   * L'IA accorde plus d'attention au début et à la fin de son contexte. Les instructions placées au milieu ont tendance à être ignorées au fur et à mesure que la discussion s'allonge.
   * Découper l'exécution en étapes progressives (initialisation, analyse, plan, exécution, validation, audit) où chaque sous-tâche charge dynamiquement ses instructions au moment opportun au lieu de charger un prompt monolithique géant.

3. **Définir des critères d'acceptation stricts (*Acceptance Criteria Mapping*) :**
   * Lors de la phase de plan, exiger que l'IA formalise les tests et conditions qui permettront de valider que la tâche est terminée (tests unitaires, types TypeScript, lint, statut de la page).

4. **Multi-agents d'audit contradictoire (Examine/Review) :**
   * Spawner des agents spécialisés (sécurité, logique, clean code) qui attaquent le code produit et forcent l'agent principal à auto-corriger ses failles avant de livrer.

5. **La boucle de rétroaction visuelle (*Dev-Browser*) :**
   * Obliger l'IA à tester elle-même les fonctionnalités dans le navigateur (cliquer, remplir des formulaires, vérifier les réponses API et les logs). Si une erreur apparaît (ex. client Stripe manquant), l'IA le constate directement et modifie le code en conséquence sans intervention humaine.

6. **Séparer les macros et les micro-tâches :**
   * Utiliser le flux lourd et automatisé (type `/apex`) pour poser l'architecture globale en une passe.
   * Utiliser un chat plus léger dans l'éditeur de code (comme dans Zed) pour les petits ajustements d'UI ou de design.

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de revenus n'est mentionné ou promis par l'auteur dans cette vidéo** (affirmé par l'auteur : *non précisé*).
  *(Seuls des tarifs d'abonnements fictifs/d'exemple à l'écran apparaissent sur les interfaces développées, ex. 0 $ ou 100 $/mois, mais ils ne représentent pas des gains annoncés).*
