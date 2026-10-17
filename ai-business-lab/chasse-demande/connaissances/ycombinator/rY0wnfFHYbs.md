# Open Models Change The Economics of AI

Vidéo : https://youtu.be/rY0wnfFHYbs · durée 57:16 · résumé Gemini (gemini-3.1-flash-lite-preview) du 2026-10-05
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances basée sur les informations contenues dans cette vidéo :

### 1) Sujet et thèse principale
*   **Sujet :** L'état actuel de l'intelligence artificielle (IA) et l'évolution de l'utilisation des modèles "open source" (modèles ouverts) versus les modèles propriétaires (fermés).
*   **Thèse principale :** Les entreprises (notamment dans l'industrie) opèrent une transition massive vers l'usage de modèles IA "open source" ou "open weights" pour leurs besoins internes. Cette adoption est portée par le besoin de réduire les coûts, de conserver le contrôle sur les données et d'améliorer la sécurité, malgré la montée en puissance des modèles propriétaires accessibles via API.

### 2) Notions expliquées
*   **Modèles "Open Source" / "Open Weights" :** Modèles d'IA dont les paramètres sont accessibles publiquement, permettant aux entreprises de les héberger et de les personnaliser localement sur leurs propres infrastructures.
*   **Modèles propriétaires / fermés :** Modèles d'IA dont le code et les paramètres sont contrôlés par une entreprise unique (type OpenAI ou Google), accessibles uniquement via des interfaces ou des API.
*   **Fine-tuning (affinage) :** Processus consistant à adapter un modèle IA pré-entraîné à une tâche spécifique ou un domaine métier particulier.
*   **Inférence :** L'étape où le modèle IA traite une donnée pour produire une réponse (le moment où le modèle est "utilisé").

### 3) Chiffres et données clés
*   **Utilisation d'Ollama :** 9 millions de développeurs.
*   **Adoption d'Ollama :** 178 000 étoiles sur GitHub.
*   **Part de marché entreprise :** 85 % des entreprises du "Fortune 500" utiliseraient Ollama (données citées par l'interlocuteur).
*   **AT&T :** L'entreprise a transféré 40 % de sa consommation de jetons (tokens) vers des modèles open source.
*   **Évolution de la consommation de jetons :** Augmentation de 150x depuis le début de l'année 2024 (pour Ollama Cloud).
*   **Comparaison technique :** Le modèle Qwen 3.8B est cité comme ayant des performances comparables au modèle Opus 4.6 (modèle fermé) pour les tâches de codage.

### 4) Conseils concrets, limites et risques
*   **Conseils :**
    *   Privilégier les modèles "open source" pour les tâches métier pour réduire les coûts par jeton.
    *   Utiliser une approche hybride : modèles locaux pour les tâches simples et à faible latence, modèles cloud pour les tâches complexes nécessitant plus de puissance.
    *   Réaliser des tests de performance (benchmarks) rigoureux sur les modèles avant de les déployer.
*   **Limites et risques :**
    *   **Sécurité ("Supply chain poisoning") :** Comme tout logiciel open source, il existe un risque de compromission de la chaîne d'approvisionnement des dépendances.
    *   **Complexité :** Gérer soi-même son infrastructure d'IA est nettement plus complexe qu'utiliser une solution "clé en main" (PaaS).
    *   **Coûts :** L'achat de matériel (GPU, type B200 ou B300) représente un investissement initial lourd.

### 5) Produits, applications et entreprises cités
*   **Entreprises (non publicitaires) :** AT&T, OpenAI, Google, NVIDIA, Apple.
*   **Produits et services (Ollama) :** Ollama, Ollama Cloud. *Il s'agit du produit central de l'auteur de la vidéo (Jeffrey Morgan), ce qui constitue un aspect promotionnel.*
*   **Modèles :** Qwen, DeepSeek (et sa variante "Flash"), Llama 3.8B/70B, Gemma.
*   **Outils :** Docker, Kubernetes, MLX (projet Apple).
*   **Publicité :** À 28:43, l'hôte (Garry Tan) fait la promotion de son accélérateur de start-ups, Y Combinator, en invitant les entrepreneurs à postuler.

***Note sur les règles fiscales/légales :** Aucune règle fiscale ou légale n'a été abordée dans cette vidéo. Les données fournies sur l'adoption des modèles par les entreprises sont des déclarations de l'invité et doivent être vérifiées auprès de sources indépendantes ou de rapports annuels des entreprises concernées.*
