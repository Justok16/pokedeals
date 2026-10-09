# Claude Code ONE-SHOT un SaaS en 10 heures

Vidéo : https://youtu.be/nb3l5g82eN8 · durée 19:48 · résumé Gemini (gemini-3.5-flash, lot de 7) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :**
Développer et lancer une application SaaS (Thumbfast) de génération de miniatures YouTube par IA en moins de 10 heures, en automatisant l'intégralité du processus de développement (de la validation de l'idée à la création des tâches d'exécution) grâce à Claude Opus et des prompts de génération de code structurés.

2. **Outils, sites ou dépôts cités :**
* **Thumbfast** (`thumbfa.st` / `thumbfast.st`) : Application SaaS permettant de créer des miniatures YouTube originales et optimisées par IA. (Payant / système de crédits).
* **Claude Opus** (Anthropic) : Modèle d'IA utilisé comme moteur principal pour la génération de code et la conception de l'application. (Payant).
* **Claude Code / Claude CLI** : Outil d'interface en ligne de commande développé par Anthropic pour coder en interaction directe avec l'IA. (Payant).
* **Gemini** (Google) : Modèle d'IA utilisé pour la génération d'images et l'analyse de miniatures. (Payant / Essai gratuit).
* **NowTS** (ou boilerplate de Melvyn) : Boilerplate de démarrage rapide pour applications SaaS sous Next.js / TypeScript. (Payant / inclus dans sa configuration Premium).
* **Excalidraw** : Outil de modélisation visuelle utilisé pour concevoir le schéma de la base de données et du workflow. (Gratuit / Option payante).
* **YouTube Studio** : Plateforme d'analyse et de gestion des vidéos YouTube, utilisée pour mesurer les performances d'A/B testing des miniatures générées par l'IA. (Gratuit).
* **Bun** : Environnement d'exécution JavaScript utilisé pour lancer des scripts système (comme l'analyse des dépenses de l'API). (Gratuit et open-source).
* **Dépôt de prompts de Melvyn / Config Premium** : Dépôt contenant des prompts de développement structurés (tels que `saas-challenge-idea.md`, `saas-prd.md`, `saas-create-architecture.md`, `create-tasks.md`, `oneshot.md`). (Payant).

3. **Astuces concrètes et réutilisables :**
* Structurer le développement d'un projet SaaS avec l'IA en quatre phases distinctes et chronologiques :
  1. **Définition de l'idée** (`saas-challenge-idea.md`) : Analyser la concurrence et valider la viabilité commerciale du projet.
  2. **Rédaction du PRD** (Product Requirements Document - `saas-prd.md`) : Définir précisément les fonctionnalités de l'MVP, le public cible et la stratégie.
  3. **Architecture technique** (`saas-create-architecture.md`) : Concevoir la structure des dossiers, la base de données et les dépendances.
  4. **Planification des tâches** (`create-tasks.md`) : Diviser le projet en micro-tâches de développement atomiques exécutables par l'IA.
* Utiliser la commande `/oneshot` pour coder et appliquer des corrections ou des fonctionnalités mineures et ultra-ciblées directement sans lancer de workflow complexe de planification.
* Tester l'impact réel des miniatures générées par IA via l'A/B testing de YouTube Studio (l'auteur montre que les designs de l'IA surpassent parfois les versions faites à la main, par exemple 36,6 % de CTR contre 30 %).

4. **Chiffres de revenus annoncés :**
Non précisé (*affirmé par l'auteur* : l'auteur mentionne uniquement un coût de développement d'API de 403,19 $ au total, mais aucun revenu généré par son SaaS personnel n'est indiqué).
