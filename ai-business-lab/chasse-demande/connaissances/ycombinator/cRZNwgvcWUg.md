# Chelsea Finn : Voici l'état de l'art en robotique

Vidéo : https://youtu.be/cRZNwgvcWUg · durée 58:18 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la conférence de Chelsea Finn (Physical Intelligence) présentée à Startup School 2026, structuré comme une fiche de connaissances :

---

# Fiche de connaissances – IA physique et robotique générale (Chelsea Finn, Startup School 2026)

## 1. Sujet et thèse principale
* **Sujet :** L’état de l’art de l’intelligence artificielle appliquée au monde physique (robotique générale).
* **Thèse principale :** Pour que les robots deviennent réellement utiles dans le monde réel, ils doivent acquérir une **autonomie à long terme** (via des recettes de renforcement automatisé et de la mémoire multi-échelle) et une **généralité out-of-the-box** (capacités de généralisation compositionnelle sans réentraînement spécifique), s'inscrivant dans la trajectoire historique similaire à celle de l'IA textuelle et visuelle.

---

## 2. Notions expliquées (définitions simples)
* **Intelligence physique (Physical AI) :** Systèmes d'IA dotés de capacités d'apprentissage et de raisonnement qui opèrent et prennent des décisions directement dans le monde physique à travers des robots autonomes.
* **Modèle Vision-Langage-Action (VLA) :** Un modèle multimodal qui prend en entrée des images/vidéos et des instructions textuelles pour prédire directement des actions robotiques (commandes de joints ou de préhenseurs).
* **Généralisation compositionnelle :** Capacité d'un modèle à combiner des concepts appris séparément (ex. : un fauteuil + un avocat) pour réussir des tâches inédites ou manipuler des objets/appareils jamais vus dans les données d'entraînement.
* **Apprentissage par renforcement post-entraînement (RL) :** Méthode où le système apprend de ses échecs de manière autonome (grâce à des modèles d'estimation de valeur ou des interventions humaines ciblées) pour atteindre des taux de fiabilité élevés (90%+).
* **Mémoire multi-échelle :** Architecture combinant une mémoire vidéo à court terme (quelques secondes) et une mémoire textuelle à long terme (résumé des actions sur plusieurs minutes ou heures) pour maintenir le contexte sur des tâches longues.

---

## 3. Chiffres, taux, plafonds et règles fiscales cités
* **2003–2006 :** Premiers lancements majeurs de ML pour les recommandations de produits.
* **2005–2009 :** ML pour le classement des publicités.
* **Milieu des années 2010 :** Apprentissage profond pour la publicité, les moteurs de recherche et la traduction.
* **2022 :** Lancement de ChatGPT (atteint 1 million d'utilisateurs en 5 jours).
* **Février 2025 :** Lancement de Claude Code.
* **Avril 2025 :** Waymo atteint 250 000 courses autonomes hebdomadaires.
* **90%+ de réussite :** Taux de succès atteints sur des tâches complexes (fabrication d'expres/lattes, assemblage de boîtes, pliage de vêtements) après apprentissage par renforcement et modèles génériques.
* **Règles fiscales/légales :** *Non précisé (aucune mention de fiscalité ou de réglementation légale dans la vidéo).* -> **À vérifier à la source officielle**.

---

## 4. Conseils concrets et leurs limites ou risques
* **Conseils :**
  * Privilégier des modèles fondationnels généralistes (type VLA) plutôt que d'entraîner des modèles spécifiques (finement réglés) pour chaque tâche isolée.
  * Utiliser l'apprentissage par renforcement automatisé couplé à des interventions humaines ciblées sur les impasses pour éliminer les trajectoires mortes et accélérer la fiabilité.
  * Intégrer un système de mémoire contextuelle pour les tâches longues (ex. : nettoyage de cuisine durant 10 à 15 minutes).
* **Limites et risques :**
  * Le coût computationnel de la mémoire brute (ex. : stocker toutes les images à haute fréquence s'avère prohibitif en tokens).
  * Le risque de sur-spécialisation si les modèles dépendent de données trop restreintes ou de réglages manuels fastidieux (fatigue humaine).
  * La vitesse et la latence d'exécution des robots par rapport aux humains restent perfectibles.

---

## 5. Produits, applications ou entreprises cités
* **Physical Intelligence** (entreprise de la conférencière, développe des modèles d'IA pour robots) – *Produit de l'auteur / pas de publicité commerciale explicite.*
* **ChatGPT / OpenAI** (mentionné pour son jalon d'adoption rapide) – *Entreprise tierce.*
* **Claude / Anthropic** (mentionné pour Claude Code) – *Entreprise tierce.*
* **Waymo** (mentionné pour ses courses autonomes) – *Entreprise tierce.*
* **DALL-E** (mentionné pour la généralisation compositionnelle) – *Entreprise tierce.*
* **Weave, Dandelion Chocolate, Actor Labs** (partenaires ou environnements de test cités pour les déploiements réels) – *Partenaires de recherche/application.*
