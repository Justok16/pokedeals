# Chalk, le « prochain Databricks » ? + Le bot paywall de Tollbit pour les agents IA | E2167

Vidéo : https://youtu.be/RrBEbnswtVk · durée 59:16 · résumé Gemini (gemini-3.8-flash, lot de 5) du 2026-10-17
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) Sujet et thèse principale**
L'émission présente deux entreprises technologiques (Chalk et Tollbit) opérant dans l'infrastructure de données pour l'intelligence artificielle. La thèse principale est que l'écosystème de l'IA bascule de la phase d'entraînement pur vers l'inférence et la recherche en temps réel (RAG/agents). Cette transition exige de nouveaux pipelines de données ultra-rapides et crée un déséquilibre économique pour les créateurs de contenu en ligne, nécessitant un nouveau modèle de monétisation (péage/paywall pour bots).

**2) Notions expliquées**
* **Inférence vs Entraînement (IA) :** L'entraînement est l'étape où le modèle apprend sur de grands volumes de données (souvent en différé/batch). L'inférence correspond à l'exécution du modèle au moment où l'utilisateur envoie une requête pour obtenir une réponse immédiate.
* **RAG (Retrieval-Augmented Generation) :** Méthode consistant, lors d'une requête utilisateur, à aller chercher des informations fraîches et à jour sur le Web ou dans des bases documentaires pour les injecter dans le contexte du modèle avant qu'il ne réponde.
* **Transpilation (Python vers C++/Rust) :** Conversion automatique d'un code écrit dans un langage simple d'utilisation pour les scientifiques des données (Python) vers des langages compilés beaucoup plus rapides (C++, Rust) pour l'exécution en production.
* **Fichier Robots.txt :** Fichier texte public sur un site web indiquant aux robots d'indexation les pages qu'ils ont le droit ou non de visiter, historiquement respecté sur la base de la bonne foi sans verrouillage technique strict.
* **Paywall pour bots / péage API :** Barrière mise en place par les éditeurs de sites web pour faire payer aux robots d'IA l'accès à leurs données et compenser les coûts d'infrastructure (bande passante / CDN).

**3) Chiffres, taux, plafonds et règles fiscales cités**
* **Chalk :** Levée de 15 millions de dollars sur une valorisation de 500 millions de dollars. Temps de latence des requêtes optimisé pour descendre bien sous la barre des 2 secondes.
* **Tollbit :** Levée de 24 millions de dollars en Série A (menée par Lightspeed).
* **Statistiques sur les robots (Rapport Q1 2025 de Tollbit) :** Les requêtes/aspirations par robots de type RAG ont augmenté de 49 % entre le T4 2024 et le T1 2025 (2,5 fois plus vite que les robots d'entraînement). Le trafic global des bots d'IA a presque doublé au T1 2025.
* **Cas pratique d'un éditeur média (football au Royaume-Uni) :** Sur 30 jours, 16 millions d'explorations par Google ont apporté des millions de visiteurs humains ; sur la même période, 13 millions d'explorations par des bots d'IA n'ont généré que 650 visiteurs réels.
* **Adoption :** Environ 1 400 éditeurs actifs sur Tollbit et 1 000 en cours d'activation.
* *Fiscalité :* Aucune règle fiscale citée.

**4) Conseils concrets et leurs limites ou risques**
* **Pour les entreprises manipulant de la donnée IA :** Exécuter le calcul des données fraîches au moment de l'inférence directement dans l'environnement cloud du client pour garantir la confidentialité et la conformité, plutôt que d'externaliser les données sensibles.
  * *Limite / risque :* Complexité technique de maintenir une latence très basse sans gonfler les coûts de calcul.
* **Pour les éditeurs de contenu web :** Analyser le trafic des robots pour évaluer les coûts CDN engendrés par les agents d'IA sans contrepartie d'audience humaine, et envisager des mécanismes de rémunération à la requête.
  * *Limite / risque :* Bloquer aveuglément les robots risque d'enclencher une course aux armements (robots contournant les filtres) ou de réduire la visibilité dans les moteurs de recherche IA.

**5) Produits, applications ou entreprises cités**
* **Chalk** (invité : Mark Fridman) : plateforme de pipeline de données en temps réel pour l'IA.
* **Tollbit** (invité : Tosit Panigrahi) : place de marché et barrière payante pour bots d'IA.
* **Sponsors / Publicités :**
  * **.tech domains** (`get.tech/twist`) : vente de noms de domaine.
  * **Lemon.io** (`lemon.io/twist`) : recrutement de développeurs à distance (-15 % sur 4 semaines).
  * **Squarespace** (`squarespace.com/twist`) : création de sites web (-10 % avec code TWIST).
* **Autres entreprises / outils cités :** Databricks, Snowflake, AWS, GCP, Google, Perplexity, OpenAI / ChatGPT, Meta (projet open source Velox), Whatnot, Affirm, Credit Karma, Bloomberg, TED, NPR, USA Today, AP, Forbes, Time.

---
