# OpenAI vs. Deepseek vs. Qwen : Comparaison des architectures LLM open source

Vidéo : https://youtu.be/raTbhtKZTZA · durée 12:32 · résumé Gemini (gemini-3.1-flash-lite) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de synthèse basée sur le contenu technique et comparatif de la vidéo :

### 1) Sujet et thèse principale
**Sujet :** Analyse comparative de l'architecture et des méthodes d'entraînement des récents modèles de langage open-source (LLM), notamment **GPT-OSS**, **Qwen3** et **DeepSeek-V3**.
**Thèse principale :** La performance exceptionnelle des nouveaux modèles open-source ne repose pas uniquement sur leur taille (nombre de paramètres), mais sur des innovations techniques précises (méthodes d'entraînement, techniques d'attention, et optimisation du contexte) qui permettent d'atteindre des résultats de pointe avec moins de ressources.

### 2) Notions expliquées
*   **MoE (Mixture of Experts) :** Architecture où le modèle divise ses paramètres en « experts ». Seule une petite partie des paramètres est activée pour chaque requête, permettant d'être puissant sans être trop lourd.
*   **Tokeniseur :** Outil qui transforme le texte en unités numériques (tokens) pour le traitement par l'IA.
*   **RoPE (Rotary Positional Embeddings) :** Méthode permettant au modèle de comprendre la position des mots dans une phrase, facilitant la gestion de longs contextes.
*   **YaRN :** Technique d'optimisation permettant d'étendre la "fenêtre de contexte" (la capacité du modèle à "se souvenir" de longs textes) sans avoir à ré-entraîner entièrement le modèle.
*   **Distillation :** Méthode consistant à transférer les connaissances d'un modèle large et puissant vers un modèle plus petit et plus efficace.

### 3) Chiffres, taux et règles cités
*   **GPT-OSS :** Modèle disponible en 120 milliards et 20 milliards de paramètres. Fenêtre de contexte de 131 072 tokens.
*   **Qwen3 :** Pré-entraîné sur 36 trillions de tokens (4 fois plus que la série Qwen 2.5). Les modèles denses incluent une version à 0,6 milliard de paramètres.
*   **DeepSeek-V3 :** 671 milliards de paramètres totaux, dont 37 milliards activés par token.
*   **Règles fiscales :** Aucune règle fiscale ou légale citée dans cette vidéo (aucune vérification nécessaire).

### 4) Conseils concrets, limites et risques
*   **Conseil d'analyse :** Ne pas se fier uniquement aux statistiques de performance globale (top-line) ou à la taille des modèles. Il faut regarder les méthodes techniques utilisées pour atteindre ces scores.
*   **Risques/Limites :** 
    *   **Opacité :** Il est très difficile de savoir précisément ce qui compose les jeux de données d'entraînement des différents modèles.
    *   **Accessibilité :** Certains modèles sont optimisés pour fonctionner sur du matériel grand public, mais les versions non quantifiées (plus précises) nécessitent une puissance matérielle importante.
    *   **Sécurité :** Bien que des mesures de sécurité soient intégrées par "alignement" (post-training), certains utilisateurs cherchent activement à contourner ces protections (jailbreak).

### 5) Produits, applications et entreprises cités
*   **OpenAI :** Développeur de GPT-OSS.
*   **Alibaba Cloud :** Développeur de la famille de modèles Qwen3.
*   **DeepSeek :** Entreprise chinoise, développeur des modèles DeepSeek-V3 et R1.
*   **Autres mentions (outils/modèles) :** Llama (Meta), Google Gemma 3, Kimi K2.
*   *Note : Cette vidéo est une analyse technique comparative réalisée par la chaîne Y Combinator (YC) ; il ne s'agit pas d'une publicité rémunérée pour ces produits, mais d'une revue technologique.*
