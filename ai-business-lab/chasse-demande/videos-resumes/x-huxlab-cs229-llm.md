# Stanford CS229 — « Building Large Language Models » (Yann Dubois, été 2024)

Source envoyée le 30/09/2026 : message X de @huxlab (republication d'une vidéo de @_HimanshuBuilds présentée à tort comme « Claude AI full course »). Original : https://youtu.be/9vM4p9NN0Ts (1 h 42). Résumé : piste son écoutée par Gemini (gemini-3.5-flash-lite) en 4 parties, le 30/09/2026. Connaissances générales, non vérifiées.

## Partie 1 sur 4


### 2) Idées principales (dans l’ordre)
1. **Introduction aux LLM :**
   - Définition des *Large Language Models* (les chatbots récents).
   - Présentation des grands modèles existants : ChatGPT (OpenAI), Claude (Anthropic), Gemini (Google), Llama, etc.
   - Objectif de la session : expliquer comment ces modèles fonctionnent (vue d’ensemble).

2. **Les 5 composants clés pour entraîner un LLM :**
   - **Architecture :** Choix de l'architecture de réseau de neurones (ex. réseaux de neurones).
   - **Perte et algorithme d'entraînement (*training loss / training algorithm*) :** Comment entraîner les modèles.
   - **Données (*data*) :** Sur quoi les entraîner.
   - **Évaluation :** Mesurer les progrès vers l'objectif.
   - **Composants système :** Faire tourner les modèles sur du matériel moderne (enjeu majeur car les modèles sont très grands).

3. **Pré-entraînement (*pre-training*) vs Post-entraînement (*post-training*) :**
   - **Pré-entraînement :** Modélisation de langage classique (ex. GPT-3, GPT-2). Apprentissage sur de vastes corpus de texte pour prédire les mots/tokens.
   - **Post-entraînement :** Tendance plus récente (depuis ChatGPT) pour transformer ces grands modèles en assistants IA.

4. **Modélisation du langage :**
   - Définition probabiliste : les LLM modélisent la distribution de probabilité d'une séquence de tokens ou de mots ($P(X_1, X_2, \dots, X_L)$).
   - Exemple avec la phrase « *The mouse ate the cheese* » vs « *The cheese ate the mouse* » (gestion de la syntaxe, des erreurs grammaticales et du sens sémantique).
   - **Modèles génératifs :** Capacité à générer du texte, des phrases ou des données en échantillonnant à partir de la distribution apprise.

5. **Modèles autorégressifs (*auto-regressive language models*) :**
   - Le principe : décomposer la probabilité conjointe en un produit de probabilités conditionnelles (règle de chaine des probabilités).
   - Chaque mot est prédit en fonction des mots précédents.
   - Inconvénients : complexité et coût de génération séquentielle pour les phrases longues.

6. **Tokenisation (*tokenization*) :**
   - **Définition :** Découpage du texte en unités plus petites (tokens) avant traitement par le modèle.
   - **Rôle :** Représentation sous forme d'identifiants (IDs) numériques passés à travers un réseau de neurones.
   - **Algorithmes de tokenisation :**
     - Le conférencier mentionne le « *byte-pair encoding* » (BPE), une méthode courante.
     - Processus : tokenisation initiale d'un grand corpus de texte, fusion itérative des paires de tokens les plus fréquentes pour construire un vocabulaire.
     - Gestion des cas particuliers (espaces, ponctuation, mots inconnus).
   - **Impact de la taille du vocabulaire :** La taille du vocabulaire et le nombre de tokens déterminent la sortie du modèle.

7. **Évaluation des LLM :**
   - Évaluation via la **perplexity** (complexité) : mesure mathématique basée sur le logarithme de la probabilité inverse par token. Une perplexité plus faible indique un meilleur modèle.
   - Benchmarks académiques et industriels (ex. *HELM*, *Open LLM Leaderboard* de Hugging Face) pour comparer les performances sur des tâches de questions-réponses, de code, de médecine, etc.

---

### 3) Méthodes, outils et commandes concrets cités
* **Modèles / Outils :**
  - **ChatGPT** (OpenAI)
  - **Claude** (Anthropic)
  - **Gemini** (Google)
  - **Llama** (Meta)
  - **GPT-3** et **GPT-2** (OpenAI)
* **Concepts et méthodes mathématiques/informatiques :**
  - *Large Language Models* (LLM)
  - Réseaux de neurones (*neural networks*)
  - *Byte-Pair Encoding* (BPE) (pour la tokenisation)
  - Fonction *Softmax*
  - Entropie croisée (*cross-entropy loss*)
  - Règle de chaine des probabilités (*chain rule of probability*)
* **Benchmarks de référence cités :**
  - **HELM** (benchmark de Stanford)
  - **Open LLM Leaderboard** (Hugging Face)

---

### 4) Chiffres cités (affirmés par l'orateur)
* *Note : Aucun chiffre statistique précis sur la taille de modèles spécifiques (en milliards de paramètres) ou de jeux de données n’a été donné avec exactitude dans cet extrait, l'orateur se concentrant sur les principes théoriques.*
* L'orateur mentionne à plusieurs reprises des exemples de séquences de tokens de taille petite (ex. 2, 3, 4 tokens, ou des phrases de quelques mots pour illustrer les probabilités).
* Il indique que l'évolution de la perplexité s'est mesurée sur des datasets entre **2017 et 2023**, faisant passer le nombre moyen de tokens par mot/phrase de ~70 à moins de 10 tokens. *(Affirmé par l'orateur).*

---


## Partie 2 sur 4


### 1) Sujet et intervenant
* **Intervenant** : Non nommé dans cet extrait (partie 2 d'un cours de 1 h 42).
* **Sujet** : La méthodologie d'évaluation des modèles de langage (LLM), l'exploration des problèmes de données (nettoyage, duplication, filtrage) et l'utilisation des lois de mise à l'échelle (*scaling laws*) appliquées aux LLM.

---

### 2) Idées principales dans l'ordre
1. **Évaluation des LLM** : Il existe plusieurs manières d'évaluer un MMLU, et les résultats varient grandement selon la méthode et le benchmark utilisés (ex. LLaMA-65B vs autres modèles).
2. **Contamination des ensembles d'entraînement (*train test contamination*)** : C’est un enjeu critique en académie, moins crucial pour les entreprises qui connaissent leurs données d'entraînement. Pour les autres, détecter si un jeu de test est inclus dans l'entraînement se fait par des astuces comme trier les données et tester la prédictibilité.
3. **Qualité des données d'Internet** : Les données du web brut sont "sales" et non représentatives de la pratique réelle. 
4. **Nettoyage et filtrage des données** : 
   - **Extraction de texte** depuis le HTML (attention aux difficultés comme l'extraction de maths ou de boilerplate).
   - **Filtrage de contenu indésirable** (contenus non sécurisés, PII, *blacklists* de sites).
   - **Déduplication** (très lourd et chronophage à l'échelle du web : nettoyage des URLs, des textes dupliqués 1 000 fois).
   - **Filtrage heuristique** (basé sur des règles pour supprimer les documents de faible qualité : tokens aberrants, longueurs de mots, ratio de mots).
5. **Filtrage basé sur des classifieurs** : Utiliser un classifieur ou Wikipédia pour identifier la provenance des textes et ne garder que les sources de haute qualité.
6. **Poids et importance des domaines** : Allouer ou sous-pondérer certains domaines (ex. augmenter le code améliore le raisonnement, les livres et les codes sont privilégiés par rapport au web brut).
7. **La loi de mise à l'échelle (*scaling laws*)** : 
   - Plus on entraîne un modèle sur de grandes quantités de données et plus le modèle est grand, meilleures sont ses performances.
   - Il est possible de prédire l'amélioration des performances en augmentant les ressources de calcul (*compute*), le nombre de paramètres ou la taille du jeu de données.
   - Les "perplexités" ou pertes diminuent de manière prévisible lorsque l'on augmente ces facteurs.

---

### 3) Méthodes, outils et commandes concrets cités
* **Modèles cités** : LLaMA (ex. LLaMA 65B), LLaMA 2, LLaMA 3, GPT-4, LLaCM.
* **Outils / Concepts techniques** : 
  * *Web crawlers* (robots d'indexation web) et *Common Crawl* (base de données de crawls web).
  * Classifieurs de texte et filtres heuristiques.
  * Déduplication (suppression des doublons textuels).
  * *Hugging Face* (implicitement suggéré pour les jeux de données).
* **Commandes / Formules conceptuelles** : 
  * Échelles logarithmiques ($log\_log$ scale) pour analyser les *scaling laws*.
  * Utilisation de *tokens*, de paramètres ($N$), et d'unités de calcul (*compute* $C$).

---

### 4) Chiffres cités (affirmés par l'orateur)
* **Taille d'Internet indexé** : Environ **250 milliards de pages web** (soit environ **1 pétaoctet** de données) pour *Common Crawl*.
* **Taille d'un *Common Crawl*** : Représente environ **1 6 gigaoctets** de données.
* **Taille de certains modèles (tokens)** : 
  * LLaMA 2 : Entraîné sur **2 billions de tokens** (ou plus selon les variantes).
  * Modèles académiques ou industriels récents : **15 billions de tokens** (taille comparable ou supérieure au nombre de paramètres des meilleurs modèles actuels).
* **Autres estimations** : Un site web d'entreprise standard comporte en moyenne 3 mots (exemple ironique pour illustrer la faible qualité d'une partie du web).

---


## Partie 3 sur 4


### 1) Sujet et intervenant
* **Sujet :** L'entraînement et l'optimisation des modèles de langage (LLM), l'inférence, l'estimation des coûts, et les techniques de réglage (*fine-tuning*, SFT, apprentissage par renforcement) appliquées aux modèles d'IA.
* **Intervenant :** Non nommé dans l'extrait.

---

### 2) Idées principales dans l'ordre
1. **Inférence et taille des modèles :** Les petits modèles dépensent moins de temps et d'argent en inférence. La meilleure taille pour l'entraînement actuel se situe autour de 150 tokens par paramètre.
2. **Coût de l'inférence :** L'inférence est coûteuse (données sur l'utilisation massive de ChatGPT).
3. **Réglages et tuning :** Il existe de nombreuses méthodes pour optimiser les modèles (données, mélanges, pondération de mélange, architecture, largeur/profondeur, GPU, etc.).
4. **Loi d'échelle (*scaling laws*) :** Plus un modèle a de calculs, meilleurs sont ses résultats. Cependant, l'architecture et les données comptent plus que l'augmentation aveugle de la taille.
5. **Complexité inutile :** Il ne faut pas sur-compliquer ; appliquer des méthodes simples et bien les exécuter est la clé (approche d'OpenAI).
6. **Évaluation des coûts de calcul :** Présentation d'exemples chiffrés sur le coût d'entraînement (ex. : modèle Llama 3 400B).
7. **Filtrage et "Sur-scrutation" (*over-scrutiny*) :** Les nouveaux ordres exécutifs et règles de sécurité imposent des critères stricts sur les modèles (paramètres vs. flops), forçant souvent à réduire les risques réglementaires.
8. **Complexité des calculs :** Explications sur les flops, les tokens de données et les heures GPU.
9. **Post-entraînement (*post-training*) :** Nécessaire pour faire des assistants IA. La modélisation de langage seule ne suffit pas ; il faut aligner le modèle pour répondre précisément aux humains (ex. : éviter les hallucinations).
10. **Alignement et Supervised Fine-Tuning (SFT) :** Utiliser des ensembles de données de questions-réponses humains et du *fine-tuning* pour adapter le modèle aux préférences humaines.
11. **Apprentissage par renforcement (*RLHF*) :** Utiliser les retours humains pour optimiser le modèle, mais attention aux limites (clonage comportemental, hallucinations, biais de préférence).

---

### 3) Méthodes, outils et commandes concrets cités
* **Modèles cités :** ChatGPT, Llama 3 400B, Llama 7B.
* **Concepts techniques et algorithmes :** Inférence, Tokens par paramètre, Mélange de données (*data mixing*), Lois d'échelle (*scaling laws*), Loi de Moore, *Over-scrutiny*, Ordre exécutif de Biden (mentionné pour ses limites sur les paramètres), Post-entraînement, *Supervised Fine-Tuning* (SFT), Modélisation de langage, *Open Assistant*, Clonage comportemental, *Reinforcement Learning from Human Feedback* (RLHF), *Softmax*, *Direct Preference Optimization* (DPO, évoqué indirectement via les modèles de récompense).

---

### 4) Chiffres cités (affirmés par l'orateur)
* **150 tokens par paramètre :** Taille optimale pour l'entraînement des meilleurs modèles actuels.
* **600 millions :** Nombre estimé d'utilisateurs de ChatGPT (donnée approximative de l'orateur).
* **Llama 3 400B :** Entraîné sur **15,6 trillions** de tokens, possède **405 milliards** de paramètres.
* **Allocation de tokens :** Environ **40** (tokens par paramètre pour un modèle optimal selon certaines directives, l'orateur cite ce chiffre autour de 40).
* **Entraînement de Llama 3 400B :** **16 100** (référence à des grappes de GPU ou serveurs, l'orateur mentionne l'entraînement sur 16 000+ équipements).
* **Temps de calcul :** Environ **70 jours** ou **26 millions d'heures GPU** (l'orateur mentionne que ses calculs indiquent 30 millions au lieu de 26 millions d'heures GPU en raison de défis techniques).
* **Coût de location de serveurs pour H100 :** Environ **2 dollars par heure** pour un H100.
* **Émissions de CO2 :** Environ **4 400 tonnes d'équivalent CO2** pour certains entraînements massifs (comparé à 2 000 billets de voyage JFK-Londres).
* **Génération de données d'entraînement :** **52 000** LLM générés de questions-réponses pour affiner certains modèles (ex. Llama 7B).

---


## Partie 4 sur 4

