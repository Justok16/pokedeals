# Quelles sont les prochaines étapes pour l'infrastructure d'IA avec Amin Vahdat ? | Les bases de l...

Vidéo : https://youtu.be/k4sHsw55uEo · durée 27:35 · résumé Gemini (gemini-3.7-flash, lot de 4) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) Sujet et thèse principale**
Dans ce volet de la série « AI Basics », Jason Calacanis et Amin Vahdat (Google Cloud) détaillent l'évolution spectaculaire de l'infrastructure informatique sous-jacente à l'intelligence artificielle. La thèse centrale est que l'année 2025 marque le passage de l'ère de l'entraînement (*training*) des modèles à **l'ère de l'inférence** (*inference*). Avec un effondrement sans précédent du coût unitaire de l'intelligence et une démultiplication de la puissance de calcul (notamment via les TPU de Google), la contrainte de développement n'est plus l'infrastructure technique ou son coût, mais uniquement l'imagination humaine pour concevoir de nouveaux produits.

---

**2) Notions expliquées (définitions simples)**
- **Inférence :** Étape où un modèle d'IA déjà entraîné est sollicité pour générer une réponse, résoudre un problème ou exécuter un calcul en temps réel pour un utilisateur final.
- **TPU (Tensor Processing Unit) :** Processeur informatique sur mesure conçu spécifiquement par Google pour accélérer les opérations mathématiques matricielles propres aux réseaux de neurones profonds.
- **Unit Cost of Intelligence (coût unitaire de l'intelligence) :** Prix facturé ou coût énergétique nécessaire pour générer un résultat donné (requêtes/tokens) à un niveau de qualité prédéfini.
- **Méthode « ADD » (Automate, Deprecate, Delegate) :** Règle de gestion opérationnelle consistant à automatiser ce qui peut l'être, supprimer (*deprecate*) ce qui n'a plus de valeur, et déléguer le reste, afin d'optimiser l'allocation du temps humain.

---

**3) Chiffres, taux, plafonds et règles fiscales cités**
*(Aucune règle fiscale abordée dans cette vidéo)*
- **Amélioration de l'efficacité et baisse des coûts :**
  - Chez Google, les gains d'efficacité permettent régulièrement de multiplier la vitesse par 2 tous les 3 mois.
  - Sur un an, les coûts de traitement peuvent être divisés par un facteur 3, voire un facteur 10 (contre des baisses historiques de l'ordre de 5 % à 10 % par an pour le stockage informatique traditionnel).
- **Puissance des serveurs et puces :**
  - Une seule puce TPU moderne intègre une puissance équivalente à environ **100 serveurs traditionnels**.
  - Une requête de recherche complexe de type « Deep Research » mobilise en simultané l'équivalent de **256 puces TPU** (soit des dizaines de milliers d'équivalents-serveurs travaillant en parallèle sur 10, 20 ou 100 sous-requêtes).
  - Les générations actuelles de « TPU Pods » sont environ **10 fois plus puissantes** que les générations précédentes.
- **Historique du calcul et du stockage :**
  - 2004 : Lancement de Gmail avec 1 Go de stockage gratuit (perçu à l'époque comme une rupture gigantesque ou un poisson d'avril face aux disques durs limités).
  - 2013 : Google a calculé que si chaque utilisateur utilisait la recherche vocale pendant 3 secondes par jour, il aurait fallu tripler toute l'infrastructure mondiale de Google (ce qui a déclenché l'invention des TPU).
  - Évolution des services : passage de produits à 1 milliard d'utilisateurs vers 2 milliards (Search, YouTube, Android, Chrome, etc.).

---

**4) Conseils concrets et leurs limites ou risques**
- **Pour les créateurs d'entreprise et développeurs :**
  - *Conseil :* Ne pas concevoir son modèle économique ou son architecture logicielle en fonction des limites actuelles de coût ou de calcul. Lorsqu'un projet paraît financièrement « impossible » en raison du coût de l'infrastructure, diviser mentalement ce coût par 10 ou par 100, car les prix s'effondrent à un rythme exponentiel.
  - *Conseil de gestion (formule ADD) :* Auditer en continu le travail de ses équipes pour éliminer l'inutile, automatiser le répétitif par l'IA et déléguer les tâches à moindre valeur ajoutée.
  - *Risque / Limite :* Les gains d'efficacité ne doivent pas faire oublier la gestion de la trésorerie au jour le jour ; même si les prix baissent, une multiplication non maîtrisée des requêtes complexes peut faire exploser les factures d'API à court terme avant que les économies d'échelle ne s'appliquent.

---

**5) Produits, applications ou entreprises cités**
- **Partenariat de l'émission :**
  - *Google Cloud* (partenaire de la série « AI Basics » ; rapport *Future of AI: Perspectives for Startups 2025* sur goo.gle/futureofai).
- **Invité et outils Google cités :**
  - Amin Vahdat (VP et General Manager ML & Cloud AI chez Google Cloud).
  - *Google TPU* (Tensor Processing Units), *Google Gemini* (dont la fonction Deep Research), *Gmail*, *Google Docs*, *Google Search*, *Android*, *YouTube*, *Chrome*.
- **Autres entreprises ou produits cités :**
  - *Flickr* (pionnier du partage de photos).
  - *Uber*, *Robinhood*, *Airbnb*, *Calm* (exemples de modèles de rupture financés dans l'histoire de la tech).
  - *Hugging Face* (plateforme de modèles d'IA).
  - *Y Combinator* (accélérateur de startups).
  - *Superforecasting* (livre sur la méthodologie de prévision cité par Jason Calacanis).

---
