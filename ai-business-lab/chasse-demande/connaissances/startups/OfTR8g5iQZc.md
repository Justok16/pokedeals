# Orchestrer des systèmes d'IA plus intelligents avec Yoav Shoham | Les bases de l'IA avec Google C...

Vidéo : https://youtu.be/OfTR8g5iQZc · durée 22:27 · résumé Gemini (gemini-3.8-flash, lot de 4) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) Sujet et thèse principale**  
La vidéo examine la fiabilité des grands modèles de langage (LLM) en entreprise, les limites du « raisonnement » artificiel, l'état de développement des agents IA autonomes et les protocoles de communication d'agent à agent (A2A). La thèse centrale est que l'engouement actuel pour les agents autonomes dépasse la réalité technique : pour les entreprises, la valeur réside aujourd'hui dans l'orchestration rigoureuse, la fiabilité déterministe et l'automatisation de flux précis plutôt que dans l'illusion d'une intelligence générale capable d'improviser sans erreur.

**2) Notions expliquées**
- **Fiabilité vs Hallucination en entreprise :** Les LLM sont intrinsèquement probabilistes. Une précision de 95 % peut suffire pour le grand public, mais un taux d'erreur de 5 % est inacceptable dans des processus d'entreprise critiques (comptabilité, code de production, service client).
- **Orchestration externe :** Méthode consistant à encadrer les modèles par une logique logicielle extérieure (vérification d'étapes, tests unitaires, appels à des API et bases de données) plutôt que de laisser le LLM gérer le flux de bout en bout.
- **Modèles de langage de petite taille (SLM) :** Modèles plus légers, spécialisés sur des domaines restreints (droit, finance), réduisant les coûts de calcul et la latence.
- **Protocoles Agent-à-Agent (A2A) :** Standards permettant à des agents autonomes conçus par différentes entités de communiquer, de négocier et d'exécuter des tâches interdépendantes.

**3) Chiffres, taux, plafonds et règles fiscales cités**
- Ratio entre expérimentations et déploiements réels en entreprise : estimé entre 10 pour 1 et 20 pour 1 (les déploiements en production restent rares).
- Publication du papier fondateur sur l'architecture Transformer par Google : 2017.
- Complexité algorithmique de l'attention dans l'architecture Transformer standard : quadratique par rapport à la longueur du contexte (longueur au carré).
- Horizon temporel des premières spécifications de protocoles A2A : évoqué dans les 60 à 90 jours précédant l'enregistrement.

**4) Conseils concrets et leurs limites ou risques**
- *Conseils :*  
  - Concentrer les déploiements d'IA sur des processus bien délimités et répétitifs (« le travail ennuyeux » mais à fort impact) plutôt que de viser une autonomie générale.  
  - Mettre en place des tests unitaires et de validation déterministes à chaque étape du flux de travail de l'IA.  
  - Pour les entreprises, privilégier des architectures hybrides ou des modèles spécialisés pour maîtriser la facture de calcul et la latence.
- *Limites et risques :*  
  - Le concept d'« agent » est souvent galvaudé (« agent washing ») et risque de décevoir si on lui confie des flux sans supervision sémantique.  
  - Dans la communication entre agents de différentes entreprises, l'incompatibilité des sémantiques et la divergence d'intérêts économiques (théorie des jeux) créent des risques d'incohérence et de blocage.

**5) Produits, applications ou entreprises cités**
- **Partenaires / Sponsors :**  
  - *Google Cloud* (partenaire de la série « AI Basics » et diffuseur du rapport *Future of AI: Perspectives for Startups*).
- **Entreprises et modèles cités :**  
  - *AI21 Labs* (entreprise cofondée par Yoav Shoham, créatrice des modèles Jurassic-2, Wordtune, Jamba et du produit d'orchestration Maestro).  
  - *Jamba* (famille de modèles hybrides combinant State-Space Models et Transformer).  
  - *OpenAI (modèles o1, o3, ChatGPT)*, *DeepSeek (R1)*, *Coursera*, *Udacity*.

---
