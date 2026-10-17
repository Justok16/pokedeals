# Claude Code, OU Cursor, OU GitHub Copilot? Le meilleur outil IA en 2025.

Vidéo : https://youtu.be/qAWfoEhljfQ · durée 26:18 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Cette vidéo compare en conditions réelles trois assistants de code IA majeurs — **VS Code avec GitHub Copilot**, **Cursor**, et **Claude Code** (via ses agents custom et commandes CLI) — en résolvant la même issue sur un projet réel, et évalue leurs performances, leur ergonomie, leur coût et leur pertinence pour les développeurs.

2) **Outils, sites ou dépôts GitHub cités :**
* **Claude Code** (outil CLI d'Anthropic) : Payant (via API/abonnements), outil en ligne de commande pour le développement assisté par IA.
* **Cursor** (éditeur de code) : Payant (abonnement Pro à 20$/mois), éditeur de code basé sur VS Code avec IA intégrée.
* **GitHub Copilot** (dans VS Code) : Payant (abonnement d'environ 10$/mois), assistant de code intégré.
* **VS Code** (éditeur de code) : Gratuit, éditeur de code officiel de Microsoft.
* **Playwright** (via serveur MCP) : Gratuit (open-source), utilisé pour l'automatisation de navigateur et tests E2E.
* **Excalidraw** (outil de schéma) : Gratuit/freemium, utilisé pour créer des tableaux comparatifs.
* **iiblueprint.dev** (site web mentionné) : Site de formation et ressources sur l'IA (`iiblueprint.dev`).
* **GitHub CLI (`gh`)** : Gratuit, outil en ligne de commande pour interagir avec les issues et PRs GitHub.
* **Next.js** / **TypeScript** / **Prisma** : Frameworks et outils web utilisés dans le projet de test.

3) **Astuces concrètes et réutilisables :**
* **Utiliser les agents custom (Sub-agents) dans Claude Code :** Définir des agents spécialisés (ex. `deep-research-analyst`, QA, UI designer) dans un dossier `.claude/agents/` pour lancer des tâches parallèles et structurées.
* **Combiner Git Worktrees et Claude Code :** Créer des scripts de worktrees pour lancer plusieurs instances isolées de Claude Code en parallèle sur différentes branches et fonctionnalités.
* **Exploiter les serveurs MCP (Model Context Protocol) :** Connecter des outils externes (comme Playwright) à Claude Code pour lui permettre de naviguer, tester et inspecter l'interface utilisateur de manière autonome.
* **Configurer des règles globales (`CLAUDE.md`) :** Placer un fichier `CLAUDE.md` dans son projet pour imposer des consignes strictes aux agents (ex. interdire d'ajouter des mentions de co-auteur dans les commits, forcer l'utilisation de tests d'intégration plutôt qu'unitaires si nécessaire).
* **Gérer les limites de taux (Rate Limits) :** Utiliser des modèles adaptés et optimiser les prompts pour éviter d'épuiser les quotas d'API lors de l'utilisation intensive de Claude Code ou Cursor.

4) **Chiffres de revenus annoncés :**
* **20 $** : Coût mensuel de l'abonnement Cursor Pro.
* **10 $** : Coût mensuel de l'abonnement GitHub Copilot.
* **1 000 $** : Montant de dépenses en API pour certains utilisateurs lourds (ou 100$ / 200$ d'abonnements de base).
* **150 $** : Estimation de coût pour 300 requêtes avec Cursor.
* **24 $** : Estimation de coût alternatif pour Cursor.
* **5.52 $ / 5.44 $ / 7.67 $ / 8.14 $** : Exemples de coûts mesurés en direct via le moniteur de tokens de Claude Code lors de sessions de test.

---
