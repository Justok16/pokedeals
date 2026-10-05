# Agents d'utilisation de robots : pourquoi les modèles polyvalents pourraient s'imposer en robotique

Vidéo : https://youtu.be/Jv5B5CEaPJI · durée 29:49 · résumé Gemini (gemini-3.1-flash-lite) du 2026-10-05
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une synthèse des informations contenues dans la vidéo, structurée sous forme de fiche de connaissances :

### 1) Sujet et thèse principale
*   **Sujet :** L’utilisation des grands modèles de langage (LLM - *Large Language Models*) pour contrôler des robots.
*   **Thèse :** Nous entrons dans l’ère des « agents d'utilisation de robots » (*Robot-use agents*). Les modèles d'IA généralistes (comme GPT-6 ou Claude) deviennent suffisamment intelligents pour contrôler directement des robots, remplaçant ainsi les anciennes méthodes de programmation spécialisées par une approche plus flexible et performante.

### 2) Notions expliquées
*   **LLM (*Large Language Models*) :** Modèles d'intelligence artificielle capables de comprendre et de générer du langage humain, mais désormais capables d'exécuter des tâches complexes (comme coder).
*   **Agent d'utilisation de robots :** Une IA capable de traduire une instruction humaine en commandes informatiques ("code") pour qu'un robot réalise une action physique.
*   **Approche « *Code as Policies* » :** Méthode consistant à utiliser le code informatique comme langage de contrôle pour les robots, permettant une exécution rapide et flexible.
*   **In-context learning :** Capacité du modèle à apprendre et à s'ajuster en temps réel au cours d'une interaction, sans nécessiter de réentraînement complet.
*   **Transduction (*transduction*) :** Méthode d'apprentissage consistant à mapper des données d'entrée vers des données de sortie, jugée moins efficace que l'approche par induction de code.

### 3) Chiffres et données (à vérifier à la source officielle)
*   **Performance (Septembre 2026) :** Le modèle "GPT-6-Astra" est présenté comme ayant un taux de réussite de 95 % dans les tâches de contrôle de robots, contre 40 % pour le modèle "Fable 5.1", avec un coût 2,3 fois inférieur et une production de jetons (*tokens*) 6,2 fois moindre.
*   **Latence :** Les intervenants notent une amélioration de la latence de traitement des modèles de l'ordre de 2x par mois.
*   **Saturation :** Il est mentionné qu'après 20 à 40 exemples fournis au modèle, celui-ci atteint une « saturation » de son apprentissage (capacité maximale d'utilisation du contexte).

### 4) Conseils concrets, limites et risques
*   **Conseil :** Privilégier des modèles qui intègrent des capacités de vision complexes (entraînement sur de grandes quantités de données visuelles type "cat data") pour mieux comprendre le monde physique.
*   **Limites :** 
    *   La latence des modèles reste un frein majeur pour le contrôle robotique en temps réel.
    *   Le risque est la dépendance à la « fenêtre de contexte » (taille de la mémoire à court terme du modèle) : une fois cette fenêtre dépassée, le modèle ne peut plus s'améliorer.
*   **Risques :** La technologie évolue si vite que la société et les cadres réglementaires sont jugés « non préparés » à l'arrivée massive de robots autonomes généralistes.

### 5) Produits, applications et entreprises cités
*   **Waddle Labs (Non précisé si c'est une publicité, mais les fondateurs interviennent) :** Entreprise spécialisée dans le développement de modèles de langage pour le contrôle robotique.
*   **Robocurve (Non précisé si c'est une publicité) :** Entreprise spécialisée dans l'évaluation et les tests (*evals*) de robots et modèles d'IA.
*   **OpenAI / Claude :** Cités en tant qu'outils de référence pour les modèles de langage.
*   **Y Combinator (YC) :** L'entreprise organisatrice de la table ronde (le présentateur est partenaire chez YC). Il s'agit d'un appel à candidatures pour leur prochain programme ("YC's next batch is now taking applications").
*   **Blender / Autodesk / SolidWorks :** Logiciels cités comme exemples d'outils de CAO (*Conception Assistée par Ordinateur*) pour illustrer l'interface homme-machine.
