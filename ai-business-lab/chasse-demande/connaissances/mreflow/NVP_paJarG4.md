# Actualités IA : Fable est de retour, mais ce nouveau modèle est-il meilleur ?

Vidéo : https://youtu.be/NVP_paJarG4 · durée 29:21 · résumé Gemini (gemini-3.6-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon vos critères :

---

### 1) Idée principale
La vidéo présente les dernières nouveautés majeures dans le domaine de l'IA (notamment les modèles de code d'Anthropic et d'OpenAI) et montre comment l'auteur utilise ces intelligences artificielles (comme Claude Fable 5) pour **développer rapidement des applications concrètes et des outils d'automatisation de contenu** (générateurs de jeux 3D, créateurs automatiques de scripts/vidéos courtes, convertisseurs d'articles en vidéos B-roll, et outils de benchmark de code).

---

### 2) Outils, sites et dépôts cités

1. **Claude Fable 5 / Mythos 5 (Anthropic)**
   * **Statut :** Payant (Inclus dans les forfaits Pro/Team jusqu'au 7 juillet, puis accessible uniquement via des crédits payants à l'usage).
   * **Usage :** Modèle d'IA de pointe pour le développement informatique complexe et la création d'applications complètes.

2. **Shorts Maker / Script Library (Application personnalisée)**
   * **Statut :** Non précisé (Outil interne développé par l'auteur avec Fable 5).
   * **Usage :** Dashboard autonome pour générer des vidéos courtes : écrit les scripts, vérifie les faits (fact-checking), génère le B-roll vidéo via ReMotion, intègre un téléprompteur et analyse les performances des vidéos sur les réseaux sociaux pour optimiser les futurs scripts.

3. **News Animator (Application personnalisée)**
   * **Statut :** Non précisé (Outil interne développé par l'auteur).
   * **Usage :** Transforme un article web en vidéo d'illustration (B-roll) animée en surbrillance, zoomant sur les paragraphes et images sélectionnés.

4. **BuseyBench**
   * **Statut :** Gratuit (Site de benchmark créé par l'auteur).
   * **Usage :** Test comparatif mesurant la capacité des différents modèles d'IA à générer du code SVG (dessin vectoriel de visage) et des images.

5. **OpenRouter**
   * **Statut :** Freemium / Payant à l'usage (API).
   * **Usage :** Plateforme permettant de lancer des requêtes de génération de contenu en masse ("bulk generate") sur des dizaines de modèles d'IA différents.

6. **GenSpark.ai (Sponsor)**
   * **Statut :** Freemium (Crédits gratuits au démarrage, abonnement payant pour l'illimité).
   * **Usage :** Espace de travail IA comprenant l'agent autonome *GenSpark Claw*, une suite bureautique (AI Slides, AI Sheets, AI Docs) et des outils de recherche automatisés.

7. **GPT-5.6 Sol / Terra / Luna (OpenAI)**
   * **Statut :** Payant (Accessible en aperçu limité via API / Codex pour certains partenaires).
   * **Usage :** Nouvelle gamme de modèles OpenAI orientée travail agentique et exécution de commandes terminal. *Sol* étant le modèle phare, *Terra* le modèle équilibré et *Luna* le modèle rapide.

8. **Claude Sonnet 5 (Anthropic)**
   * **Statut :** Payant (API à tarif réduit par rapport à Fable/Opus : 2 $/M tokens en entrée, 10 $/M en sortie).
   * **Usage :** Modèle de code et de raisonnement intermédiaire, plus rapide et économique que Fable/Opus.

9. **Google Nano Banana 2 Lite**
   * **Statut :** Payant à l'usage via API (environ 0,034 $ pour 1 000 images) / Inclus dans certains forfaits Google.
   * **Usage :** Modèle de génération d'images ultra-rapide (4 secondes).

10. **Google Gemini Omni Flash**
    * **Statut :** Payant via Google AI Studio / API (0,10 $ par seconde de vidéo générée).
    * **Usage :** Outil de création, d'édition et de modification de séquences vidéo par IA.

11. **Google NotebookLM (Short Video Overviews)**
    * **Statut :** Gratuit.
    * **Usage :** Génère automatiquement de courtes vidéos explicatives au format vertical (type Shorts/Reels) à partir de vos notes ou documents texte.

12. **Claude Science (Anthropic)**
    * **Statut :** Inclus dans les abonnements payants d'Anthropic (App Mac/Linux).
    * **Usage :** Environnement de travail IA spécialement conçu pour la recherche scientifique (analyse de données, molécules, graphes).

13. **Cursor (App iOS)**
    * **Statut :** Freemium / Payant.
    * **Usage :** Application mobile permettant de piloter et surveiller à distance ses agents de codage IA (exécutés sur PC ou dans le cloud) depuis son smartphone.

14. **X MCP Server (Model Context Protocol)**
    * **Statut :** Gratuit pour les développeurs.
    * **Usage :** Serveur officiel permettant aux agents d'IA de lire et interagir plus facilement avec les données en temps réel de la plateforme X (Twitter).

15. **Google Meet Note-taking (Gemini)**
    * **Statut :** Payant (Réservé aux abonnés Google AI Pro / Ultra).
    * **Usage :** Transcription et prise de notes automatique des réunions vidéo avec envoi du compte-rendu par e-mail.

16. **Gemini Spark (macOS)**
    * **Statut :** Payant (Réservé aux abonnés Gemini Ultra).
    * **Usage :** Agent IA local pour Mac capable de manipuler l'ordinateur, trier et ranger automatiquement des dossiers physiques sur le disque dur.

17. **Clavier/Macro-pad OpenAI x Work Louder pour Codex**
    * **Statut :** Payant (Teaser matériel physique, annonce prévue le 15 juillet).
    * **Usage :** Boîtier physique à boutons programmables dédié au lancement de raccourcis pour l'outil de code Codex.

---

### 3) Astuces concrètes et réutilisables

* **Méthode de développement de projets "Gros volume" :** Lorsque des modèles très puissants mais chers (comme Fable 5) sont temporairement inclus gratuitement dans votre abonnement, confiez-leur le gros du travail de création d'applications (80 à 90 % du code). Une fois la période d'essai expirée, basculez sur des modèles plus économiques (Sonnet 5, Opus ou GPT-5.5) pour effectuer les ajustements mineurs.
* **Création d'un flux de contenu automatisé :** Vous pouvez demander à un LLM orienté code d'assembler une application qui prend une URL/un texte, crée le script, génère les animations B-roll (via la librairie *ReMotion*) et prépare un texte pour téléprompteur.
* **Boucle de rétroaction (Feedback Loop) :** Connectez l'outil de génération de scripts à l'API de vos réseaux sociaux afin qu'il analyse quelles vidéos font le plus de vues, puis réinjectez ces métriques dans le prompt de création pour améliorer automatiquement les prochains scripts.
* **Gestion d'agents en déplacement :** Associez un agent de code (via des applications comme *Cursor iOS*) à votre machine de travail pour lancer du développement de code lourd en votre absence et suivre sa progression depuis votre téléphone.

---

### 4) Chiffres de revenus annoncés
* **Affirmé par l'auteur :** Aucun chiffre de revenus personnels ou de gains financiers nets n'est mentionné dans la vidéo (*non précisé*). L'auteur partage uniquement des éléments de coûts d'utilisation d'API (ex. : 4 $ pour générer une image complexe sur GPT-5.5 Pro, 0,034 $ les 1 000 images sur Nano Banana 2, 0,10 $/sec de vidéo sur Omni Flash).
