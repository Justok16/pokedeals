# Chelsea Finn : Construire des robots qui peuvent tout faire

Vidéo : https://youtu.be/a8-QsBHoH94 · durée 44:53 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré comme une fiche de connaissances :

### 1) Sujet et thèse principale
* **Sujet** : Le développement de modèles d'intelligence artificielle à usage général pour les robots, permettant d'apporter l'intelligence au monde physique.
* **Thèse principale** : Pour résoudre véritablement des applications en robotique, il faut concevoir des modèles généralistes entraînés à grande échelle sur des données réelles variées, combinant pré-entraînement et affinement sur des démonstrations de haute qualité, plutôt que de créer des solutions sur mesure à partir de zéro pour chaque tâche.

### 2) Notions expliquées
* **Modèles de fondation (Foundation models)** : Modèles d'IA entraînés sur de vastes volumes de données diverses, pouvant être adaptés ou affinés pour de nombreuses tâches spécifiques.
* **Modèles Vision-Langage-Action (VLA)** : Modèles qui intègrent des données visuelles, linguistiques et des actions robotiques (commandes de mouvements).
* **Imitation learning (Apprentissage par imitation)** : Technique où le robot apprend à réaliser une tâche en observant et en imitant des démonstrations faites par des humains (téléopération).
* **Pré-entraînement et affinement (Pre-training and fine-tuning)** : Processus consistant d'abord à entraîner un modèle sur une base de données très large et généraliste, puis à l'affiner sur des données plus spécifiques et de haute qualité.
* **Données synthétiques** : Données générées artificiellement (par exemple par des modèles de langage) pour simuler des interactions ou des instructions humaines variées.

### 3) Chiffres, taux, plafonds et règles
* **Taille de modèle (premiers tests)** : Environ 100 millions de paramètres (à vérifier à la source officielle).
* **Fréquence de contrôle** : 50 Hz sur les robots (à vérifier à la source officielle).
* **Taille du modèle VLM** : Modèle PaliGemma de 3 milliards de paramètres (à vérifier à la source officielle).
* **Part des données de manipulation mobile** : Environ 2,4 % du mélange de pré-entraînement global (à vérifier à la source officielle).
* **Taux de suivi de langage** : Amélioration de 20 % à environ 80 % de taux de suivi avec l'architecture optimisée (à vérifier à la source officielle).
* **Chronologie des tests** : Compagnie fondée mi-mars 2024 ; premiers tests en mai 2024 ; signes de vie en juin 2024 ; améliorations en septembre et octobre 2024 (à vérifier à la source officielle).

### 4) Conseils concrets et limites ou risques
* **Conseils concrets** :
  * Commencer par des tâches simples (par exemple plier un seul type de chemise) avant d'augmenter progressivement la complexité.
  * Utiliser un modèle de fondation pré-entraîné sur des données globales et l'affiner sur un ensemble restreint de démonstrations cohérentes et de haute qualité.
  * Exploiter des données synthétiques pour élargir la compréhension des instructions en langage naturel sans multiplier à l'infini les démonstrations physiques coûteuses.
* **Limites et risques** :
  * L'apprentissage par imitation et la collecte de données robotiques à grande échelle restent coûteux, complexes et difficiles à mettre à l'échelle.
  * Les modèles généralistes peuvent encore ignorer les instructions textuelles dans les premières phases de développement ou commettre des erreurs de manipulation dans de nouveaux environnements.
  * L'évaluation de la généralisation des robots dans des dizaines ou centaines d'environnements inédits demeure un défi technique majeur.

### 5) Produits, applications ou entreprises cités
* **Physical Intelligence** : Entreprise co-fondée par l'intervenante (produit/entreprise de l'auteur).
* **PaliGemma (Google)** : Modèle de vision-langage open source (produit tiers cité).
* **Astribot** : Robot humanoïde externe sur lequel le modèle a été testé (produit tiers cité).
* **Y Combinator** : Programme d'accélération et école de startups (publicité/partenaire mentionné dans la vidéo, ex. *ycombinator.com/apply*).
