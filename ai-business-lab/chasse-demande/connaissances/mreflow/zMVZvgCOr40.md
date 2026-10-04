# Actu IA : Le nouveau modèle qui vaut bien une fable

Vidéo : https://youtu.be/zMVZvgCOr40 · durée 20:01 · résumé Gemini (gemini-3-flash-preview) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré pour répondre à vos besoins :

### 1) Idée principale
La vidéo présente les dernières actualités de l'IA, mettant l'accent sur les **modèles d'orchestration** (comme Sakana Fugu) qui gèrent plusieurs LLM à la fois, et l'intégration d'agents IA directement dans les outils de travail (comme **Claude Tag** dans Slack). L'idée est de montrer comment ces outils peuvent automatiser des tâches complexes (clonage de sites web, création de jeux, gestion de projets) pour gagner en productivité ou créer des actifs numériques.

### 2) Outils, sites et dépôts cités

*   **Sakana Fugu (Sakana.ai)** :
    *   **Statut** : Payant (Standard : 25 $/mois, Pro : 100 $/mois, Max : 200 $/mois ou paiement à l'usage).
    *   **Utilité** : C'est un modèle "orchestrateur" qui dirige vos requêtes vers le meilleur modèle disponible (OpenAI, Anthropic, etc.). Très puissant pour le code et les tâches complexes.
*   **Codex CLI** :
    *   **Statut** : Gratuit (nécessite une clé API Sakana pour fonctionner).
    *   **Utilité** : Interface en ligne de commande pour installer et exécuter Fugu localement et générer des applications entières.
*   **Nexos.ai** :
    *   **Statut** : Payant (abonnement unique pour plusieurs outils).
    *   **Utilité** : Plateforme centralisée regroupant ChatGPT, Claude et Gemini. Inclut un constructeur d'agents sans code pour automatiser les e-mails, calendriers et Slack.
*   **Claude Tag (Anthropic)** :
    *   **Statut** : Payant (inclus dans les plans Teams et Enterprise de Claude).
    *   **Utilité** : Permet de mentionner @Claude directement dans Slack pour qu'il gère des projets, écrive du code et apprenne le contexte de l'entreprise.
*   **Seedance 2.5 (ByteDance)** :
    *   **Statut** : Non précisé (en cours de déploiement).
    *   **Utilité** : Modèle de génération vidéo capable de créer des clips de 30 secondes à partir d'un seul prompt.
*   **Krea 2 Raw & Turbo (Krea AI)** :
    *   **Statut** : Gratuit (poids du modèle ouverts/"open weights").
    *   **Utilité** : Modèles de génération d'images haute qualité que l'on peut télécharger et entraîner sur ses propres styles artistiques.
*   **AI Watchdog (The Atlantic)** :
    *   **Statut** : Gratuit.
    *   **Utilité** : Base de données consultable pour savoir si vos musiques ou vidéos ont été utilisées pour entraîner des IA. Site : `theatlantic.com/category/ai-watchdog`.

### 3) Astuces concrètes et réutilisables

*   **Orchestration pour la fiabilité** : Utilisez des outils comme Sakana Fugu pour que vos applications ne tombent pas en panne si un fournisseur d'IA (comme OpenAI) a une interruption ; le système bascule automatiquement sur un autre modèle.
*   **Clonage rapide d'actifs** : Pour créer un site web ou un jeu similaire à un existant, utilisez le mode "Extra High" de Fugu-Ultra via Codex CLI en décrivant précisément l'URL ou les mécaniques de jeu cibles.
*   **Économie d'abonnement** : Centralisez vos besoins via des agrégateurs comme Nexos pour éviter de payer 20 $ par mois à chaque fournisseur différent (ChatGPT, Claude, Perplexity).
*   **Prudence sur les coûts de "raisonnement"** : Les modèles ultra-performants consomment énormément de jetons (tokens). L'auteur a dépensé **30 $** en jetons pour générer seulement deux applications complexes.
*   **Personnalisation d'IA** : Puisque les poids de Krea 2 sont ouverts, vous pouvez créer un service légal de génération d'images personnalisées en entraînant le modèle sur le visage d'un client ou un style de marque spécifique.

### 4) Chiffres de revenus / économies (affirmés par l'auteur)

*   **Économies** : Jusqu'à **200 $/mois** d'économie en utilisant Nexos au lieu de multiples abonnements individuels.
*   **Productivité** : Anthropic affirme que **65 %** de leur propre code interne est désormais généré via leur outil Claude Tag.
*   **Revenus générés** : **Non précisé**. (L'auteur se concentre sur les coûts de production et les fonctionnalités plutôt que sur ses profits personnels directs).
