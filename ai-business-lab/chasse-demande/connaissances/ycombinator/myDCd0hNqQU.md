# Pourquoi la robotique n'est toujours pas au point – mais pourrait bientôt l'être | YC Paper Club

Vidéo : https://youtu.be/myDCd0hNqQU · durée 1:24:13 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances finance personnelle basée sur la transcription de la vidéo :

---

# Fiche de connaissances : Tendances et applications de l'IA physique et de la robotique

## 1. Sujet et thèse principale
* **Sujet :** L'état actuel et futur de l'intelligence artificielle appliquée à la robotique, en se concentrant sur la manipulation robotique, la mémoire, le raisonnement et les modèles d'action mondiaux.
* **Thèse principale :** Bien que la robotique progresse rapidement grâce aux modèles de vision-langage-action (VLA) et à la simulation, des défis majeurs persistent — notamment l'écart « sim-to-real », la dérive d'incarnation (*embodiment drift*), la complexité de la mémoire à long terme et le coût computationnel. L'émergence de « sociétés d'applications robotiques » (ou intégrateurs néo) centrées sur la résolution de problèmes métier de bout en bout représente la prochaine grande opportunité économique, semblable à l'essor des logiciels SaaS.

---

## 2. Notions expliquées (définitions simples)
* **Modèles VLA (Vision-Language-Action) :** Modèles d'IA multimodaux qui prennent en entrée des images/perceptions et des instructions textuelles pour générer des actions robotiques (commandes de direction, positions d'effecteurs).
* **Écart « Sim-to-Real » (*Sim-to-Real Gap*) :** La difficulté pour un modèle entraîné en simulation de fonctionner correctement dans le monde réel en raison des imperfections physiques (dynamique de contact, déformabilité).
* **Dérive d'incarnation (*Embodiment Drift*) :** L'usure physique des actionneurs, capteurs et composants d'un robot au fil du temps, qui altère l'exécution des politiques apprises.
* **Modèles d'Action Mondiaux (*World Action Models* - WAM) :** Des modèles qui prédisent à la fois la dynamique future de l'environnement (vidéo) et les actions associées, combinant prédiction et contrôle en boucle fermée.
* **Apprentissage par renforcement en simulation (*Sim-to-Real RL*) :** Technique consistant à accélérer massivement l'entraînement des robots en simulation GPU avant de les déployer sur du matériel réel.

---

## 3. Chiffres, taux, plafonds et règles fiscales
*(Aucune règle fiscale ou légale pure n'est abordée dans cette présentation technique. Les éléments ci-dessous concernent des performances techniques et coûts matériels cités par les intervenants) :*
* Latence par bloc d'action dans certains modèles optimisés : ~0,15 seconde (avec du matériel haut de gamme comme des configurations GPU à plusieurs dizaines de milliers de dollars).
* Coût de déploiement estimé pour certains modèles de pointe : ~70 000 $ en matériel (à vérifier à la source officielle).
* Évolution des modèles VLA et WAM : horizon 2022-2028 (selon les mèmes et présentations de la communauté de recherche).

---

## 4. Conseils concrets, limites et risques
* **Conseils pour entreprendre dans la robotique (*Robotics Application Companies*) :**
  * Résoudre des problèmes métier réels de bout en bout.
  * S'appuyer initialement sur la télé-opération (*teleop*) et du matériel standard du commerce (*off-the-shelf*).
  * Réduire au maximum le matériel personnalisé (*custom hardware*).
  * Commencer par des tâches simples (« *Hello World* » de la robotique) et itérer rapidement sur la qualité et la collecte de données.
* **Limites et risques :**
  * Fragilité du matériel physique dans le monde réel (les actionneurs s'usent, se corrodent ou se décalent).
  * Manque de données tactiles (*sensorimotor void*) et difficulté à modéliser la physique des objets déformables ou des contacts complexes.
  * Coût prohibitif et lourdeur computationnelle des modèles de prédiction vidéo en temps réel (nécessité d'optimisations lourdes).

---

## 5. Produits, applications ou entreprises cités
* **Entreprises et laboratoires de recherche mentionnés :**
  * *Physical Intelligence* (recherche en mémoire et modèles d'action).
  * *Waymo* (véhicules autonomes, conduite).
  * *Rerun* (couche de données unifiée pour l'IA physique – mentionné par son cofondateur Niko West).
  * *General Instinct* (modèles d'action mondiaux, présentés par Bill Jiao et Guangming Wang).
  * *Nvidia* (modèles et outils de simulation type DreamZero / *Isaac*).
* **Nature des mentions :** Présentations de projets de recherche et retours d'expérience entrepreneuriale par leurs fondateurs/chercheurs (pas de publicité commerciale directe, mais présentation de leurs propres solutions logicielles/matérielles).
