# Vidéo https://youtu.be/bBMp5tLxShQ

> Résumé produit par Gemini (via le relais Vercel) le 25/09/2026. Les chiffres de revenus sont **affirmés par l’auteur de la vidéo, non vérifiés**.

Absolument ! Voici un résumé de la vidéo, en français, pour quelqu'un qui cherche à monétiser l'IA de manière légale et efficace avec Claude Code :

---

**Idée principale :**
La vidéo présente comment Shopify a massivement reconstruit son application mobile (plus de 300 écrans) en utilisant des agents d'IA. Plutôt que de confier la tâche entière à un seul agent, ils ont mis en place un workflow structuré, appelé "Helix", basé sur des "checkpoints" (petites tâches) et des "gates" (étapes de validation strictes). AI Labs a recréé ce même workflow avec Claude Code, démontrant une approche systématique pour le développement de fonctionnalités d'applications complexes par l'IA, garantissant la qualité et la conformité aux standards.

**Outils, sites et dépôts GitHub cités :**

*   **Shopify App :** L'application mobile principale de Shopify, reconstruite avec l'IA. (non précisé si payant pour la développer, mais Shopify est une plateforme de commerce électronique payante).
*   **Claude Code :** L'environnement de développement AI utilisé par AI Labs pour implémenter et gérer le workflow. Il s'agit d'un outil pour le codage assisté par l'IA, utilisant des agents et des "skills". (La vidéo présente la version 2.1.281, Opus 5.5, avec 1 million de tokens de contexte. Non précisé s'il est gratuit ou payant directement, mais il est au cœur de l'approche d'AI Labs).
*   **Helix :** L'outil interne de Shopify qui a été utilisé pour leur migration d'application native. (Outil interne de Shopify, non accessible publiquement).
*   **Hedra :** Un sponsor de la vidéo, plateforme offrant des modèles et une infrastructure pour la génération de médias visuels (vidéo, image, audio) avec l'IA. Permet aux agents de générer du contenu média directement dans la session de codage. (Essai gratuit, puis payant. La vidéo offre un code promo "AILABS50" pour 50% de réduction le premier mois).
*   **AI Labs Pro :** La communauté et la source de ressources d'AI Labs, où les compétences (skills) et les workflows mentionnés sont disponibles. (Communauté payante).
*   **GitHub (implicite) :** La gestion de code est évoquée par les "commits" et "branches", suggérant l'utilisation de GitHub ou un système similaire pour le contrôle de version. (non précisé si gratuit ou payant, c'est une plateforme générale).

**Astuces concrètes et réutilisables pour gagner de l'argent avec l'IA et Claude Code :**

1.  **Découpage de tâches en "Checkpoints"** :
    *   Divisez les grandes fonctionnalités en petites tâches incrémentales ("checkpoints"). Chaque checkpoint doit être construit sur le précédent, en augmentant progressivement la complexité. Cela permet d'identifier et de corriger les erreurs tôt, lorsque le coût est minime.
    *   Utilisez un agent "checkpoint-planner" (comme celui créé par AI Labs) pour que l'IA planifie et structure automatiquement ces checkpoints dans un format JSON facile à lire par l'agent.
    *   Créez un "viewer" HTML pour visualiser et réviser facilement le plan généré par l'IA (le JSON étant difficile à lire pour un humain).

2.  **Mise en place de "Gates" pour la qualité** :
    *   Intégrez des points de contrôle stricts ("gates") que chaque checkpoint doit impérativement passer avant que l'agent ne puisse avancer. Une "gate" n'est pas un conseil, mais une exigence obligatoire.
    *   **Types de Gates (comme chez Shopify et AI Labs) :**
        *   **Gate de Comportement (Works) :** Vérifie que la fonctionnalité fonctionne comme prévu, en utilisant des tests unitaires ou d'intégration (CLI, API, règles).
        *   **Gate de Revue UI (Looks Right) :** Vérifie que l'interface utilisateur correspond au design souhaité. Shopify utilise des modèles Gemini pour leur "conscience spatiale" afin de détecter les différences de taille, espacement, alignement, etc. AI Labs a développé un skill `review-ui` pour comparer un prototype HTML avec l'application "live".
        *   **Gate de Revue de Code (Code Review / Adversarial Review) :** Évalue la qualité, la sécurité et la conformité du code aux conventions et règles d'architecture. AI Labs utilise une "boucle adversaire" où un agent (`adversarial-reviewer`) critique activement le code, et un autre (`fixer`) tente de corriger les problèmes.
        *   **Gate d'Approbation Humaine (You) :** Une étape finale où un humain vérifie et approuve la fonctionnalité terminée, surtout pour des aspects comme l'expérience utilisateur et les nuances qui échappent à l'IA.
    *   **Implémentation des Gates avec des Hooks :** Pour forcer le respect des gates, utilisez des "hooks" (scripts Python dans la vidéo) qui s'exécutent lorsqu'un agent tente de "terminer" une tâche. Si les gates ne sont pas passées, le hook déclenche une erreur d'exécution (par exemple `sys.exit(2)`) pour empêcher l'agent de progresser, le forçant à itérer.

3.  **Priorisation des Tests et Prototypage :**
    *   **Tests en premier :** Demandez à l'IA de planifier les tests (grâce à un agent "test-planner") *avant* de commencer le développement de la fonctionnalité. Cela fournit une feuille de route claire et des critères de succès.
    *   **Prototypage UI :** Pour les fonctionnalités d'interface utilisateur, demandez à l'agent de créer d'abord des prototypes HTML cliquables (via un skill "prototype"). Cela permet de valider le design et le flux avec les parties prenantes sans modifier le code de production.
    *   **Fichiers de Design Structurés (`DESIGN.md`) :** Pour les projets avec des exigences de design spécifiques, créez un fichier `DESIGN.md` structuré (éventuellement via un agent "design-md-planner") qui liste les couleurs, polices, tailles, etc. Les agents peuvent alors se référer à ce fichier pour garantir la cohérence visuelle.

4.  **Optimisation du travail de l'Agent ("Orchestrator") :**
    *   Créez une "compétence d'orchestration" (`orchestrator`) qui gère l'ensemble du workflow. C'est le seul "skill" que vous avez besoin de solliciter, et il s'occupe de lancer les sous-agents, de coordonner les checkpoints, les tests, la construction, les gates et la révision.
    *   L'orchestrateur demande une intervention humaine uniquement deux fois : après la planification des checkpoints pour approbation, et à la fin pour la revue de l'application.

5.  **Apprentissage et Itération :**
    *   Le système doit apprendre de vos retours. Les changements que vous demandez à l'orchestrateur sont convertis en nouveaux checkpoints et enregistrés dans un fichier `LEARNINGS.md`. Tous les agents lisent ce fichier avant de commencer leur travail, améliorant ainsi leur performance future.

6.  **Intégration d'Outils Externes (Hedra) :**
    *   Si votre projet nécessite la génération de médias (vidéo, images), intégrez des outils comme Hedra directement dans votre session Claude Code via un "serveur MCP". Cela permet à l'agent de générer et d'incorporer du contenu média sans quitter votre environnement de développement, évitant les blocages.

**Chiffres de revenus annoncés (affirmés par l'auteur) :**

*   La reconstruction de l'application Shopify concerne **plus de 300 écrans**.
*   La génération d'un clip vidéo de 5 secondes via Hedra coûte **1,61 $**.

---

Ce workflow structuré permet de maximiser l'efficacité des agents d'IA en les guidant à travers un processus rigoureux, réduisant les erreurs et garantissant que le produit final répond à des standards de qualité élevés.
