# Why Inference Matters 12x More Than Training | YC Paper Club

Vidéo : https://youtu.be/mHNKuH-9OxU · durée 1:50:49 · résumé Gemini (gemini-3-flash-preview) du 2026-10-26
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré comme une fiche de connaissances en finances/investissement dans le secteur de l'IA.

### 1) Sujet et thèse principale
**Sujet :** L’économie et l’optimisation technique de l’inférence (l’exécution) des modèles de langage (LLM).
**Thèse :** Alors que l’attention se porte souvent sur l’entraînement des IA, c'est l'**inférence** qui constitue le véritable goulot d'étranglement financier et technique. L'optimisation de cette phase est la clé de la rentabilité (marges brutes élevées) et de la viabilité économique des entreprises de logiciels à l'ère de l'IA.

### 2) Notions expliquées
*   **Inférence :** L'action de faire tourner un modèle d'IA déjà entraîné pour répondre à une requête utilisateur.
*   **COGS (Cost of Goods Sold) :** En IA, cela représente principalement les coûts de calcul (puces GPU) et d'énergie nécessaires pour générer des réponses.
*   **Tokens :** Unités de base de texte (mots ou morceaux de mots) traitées par l'IA.
*   **Quantisation (Quantization) :** Processus de réduction de la précision numérique des paramètres d'un modèle (ex. passer de 16 bits à 4 bits) pour réduire la mémoire utilisée et le coût, au risque de perdre un peu de "qualité" intellectuelle.
*   **TTFT (Time to First Token) :** Temps de latence avant que l'IA ne commence à afficher le premier mot de sa réponse.
*   **TPS (Tokens Per Second) :** Mesure de la vitesse de lecture/génération du texte par l'IA.
*   **KV Cache :** Mémoire temporaire stockant le contexte d'une conversation pour éviter de recalculer tout le texte précédent à chaque nouveau mot.

### 3) Chiffres, taux et règles cités
*   **Valorisation du secteur :** 220 milliards de dollars de capitalisation boursière créés par des entreprises focalisées sur l'inférence en moins de 10 ans.
*   **Réduction des coûts :** Le coût des tokens pour les modèles de classe GPT-3.5 a chuté de 20 $ à 0,07 $ par million de tokens en deux ans (soit une réduction de ~10x par an).
*   **Rentabilité (DeepSeek) :** DeepSeek parviendrait à une marge brute d'environ 80 % uniquement sur les coûts GPU grâce à des optimisations extrêmes de l'inférence (chiffre de 2024/2025).
*   **Poids des modèles :** Un modèle comme Kimi K3 possède 3 000 milliards de paramètres (3T).
*   **Règles fiscales ou légales :** Non précisé (À vérifier à la source officielle si des régulations spécifiques s'appliquent à l'hébergement de données).

### 4) Conseils concrets, limites et risques
*   **Pour les entreprises (Investissement/Stratégie) :**
    *   L'objectif financier pendant l'entraînement d'un modèle devrait être de minimiser une fonction combinant le coût d'entraînement et, surtout, 12 fois le coût d'inférence (pour anticiper l'usage massif).
    *   **Risque :** Utiliser des modèles trop "quantisés" (compressés) peut entraîner des erreurs silencieuses ou une baisse de performance sur des tâches complexes comme le code.
*   **Pour les développeurs (Efficacité) :**
    *   Privilégier les modèles "Open Weights" (poids ouverts) dont les coûts d'inférence chutent plus vite que les modèles fermés.
    *   Mettre en place un système de "routage" : envoyer les requêtes simples à des petits modèles peu coûteux et réserver les modèles massifs aux tâches complexes.
    *   **Limite :** La performance est plafonnée par la bande passante mémoire des puces (Memory-bound) plutôt que par leur puissance de calcul brute.

### 5) Produits, applications ou entreprises cités
*   **Entreprises des intervenants (Produits d'auteurs) :**
    *   **Together AI :** Plateforme de cloud pour l'inférence rapide.
    *   **Ollama :** Outil pour faire tourner des modèles localement.
    *   **Luminal :** Compilateur optimisé pour le calcul tensoriel.
    *   **SGLang :** Infrastructure logicielle pour la gestion du cache et du débit.
*   **Autres entreprises et produits :**
    *   **DeepSeek :** Cité pour son efficacité économique et son infrastructure d'inférence.
    *   **NVIDIA :** Puces H100 et architecture Blackwell (matériel de référence).
    *   **Meta :** Modèles Llama (8B à 405B).
    *   **Moonshot AI :** Modèles Kimi.
    *   **MiniMax :** Modèles M3.
    *   **Google :** Gemini (cité pour la comparaison de trafic).
    *   **Anthropic :** Claude Code (cité comme exemple d'usage intensif).
