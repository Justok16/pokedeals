# Session 23 (Val MBAs): Real Option Applications

Vidéo : https://youtu.be/3I2rlw-Hr3I · durée 1:21:37 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

---

### 1. Sujet et thèse principale
* **Sujet :** L’évaluation des projets d’investissement et des entreprises à travers le prisme des **options réelles** (application de la théorie des options financières aux décisions stratégiques : option de retarder, option d’abandonner, option d’étendre).
* **Thèse principale :** Les méthodes d’évaluation traditionnelles (comme la VAN ou le DCF) sont trop rigides et ignorent la valeur de la flexibilité managériale. L’intégration d’options réelles permet de mieux valoriser des actifs risqués, incertains ou non viables à court terme (brevets, ressources naturelles, R&D, flexibilité financière).

---

### 2. Notions expliquées (définitions simples)
* **Option réelle :** Droit (mais non obligation) d’entreprendre une action (investir, retarder, étendre, abandonner) dans le monde réel, valorisé de la même manière qu’une option financière.
* **Valeur actuelle nette (VAN / NPV) :** Somme des flux de trésorerie futurs actualisés moins l’investissement initial. Un projet à VAN négative est traditionnellement rejeté, sauf s'il contient des options stratégiques cachées.
* **Arbre binomial / Arbre de décision :** Représentation graphique des différents scénarios possibles à chaque nœud pour évaluer un actif incertain.
* **Modèle de Black-Scholes :** Modèle mathématique d'évaluation d'options (principalement conçu pour les options européennes, mais souvent adapté ou critiqué pour les options réelles).
* **Volatilité et incertitude :** Contrairement à la finance classique où l'incertitude détruit de la valeur, l'incertitude et la volatilité augmentent la valeur d'une option réelle (car on peut profiter des scénarios haussiers tout en limitant les baisses).
* **Coût du capital / Taux d'actualisation :** Taux de rendement exigé par les investisseurs pour actualiser les flux futurs.
* **Option de retarder :** Le droit d'attendre pour obtenir plus d'informations avant d'engager des capitaux.
* **Option d'abandonner :** Le droit d'arrêter un projet en cours de route pour limiter les pertes (valeur de sortie ou de revente).
* **Option d'étendre (ou de croissance) :** Le droit d'utiliser un investissement initial comme tremplin pour saisir de futures opportunités à forte valeur (ex : R&D, plateformes technologiques).

---

### 3. Chiffres, taux, plafonds et règles fiscales cités
* **Exemple de la start-up (diapo 2) :**
  * Coût de mise en œuvre : 2 milliards de dollars.
  * Valeur actuelle des flux espérés : 1,5 milliard de dollars (VAN négative de -0,5 milliard).
* **Exemple du brevet pharmaceutique (Avonex / Biogen) :**
  * Valeur actuelle des flux futurs (S) : 3,422 milliards de dollars.
  * Coût de développement (K) : 2,875 milliards de dollars.
  * Durée de vie du brevet : 17 ans.
  * Taux sans risque : 6,7 % (taux des obligations d'État).
  * Volatilité (variance des valeurs actuelles) : 0,224.
  * Coût de retard (rendement en dividendes implicite) : $\gamma = 1 / 17 = 5{,}89\,\%$.
  * Valeur calculée par le modèle d'option : 907 millions de dollars (contre une VAN classique négative ou non optimale si exercée trop tard).
* **Exemple de Gulf Oil (ressources naturelles) :**
  * Prix d'acquisition de référence (prise de contrôle au début des années 1980) : 70 $ par action (165,30 millions d'actions, dette totale de 9,9 milliards).
  * Réserves estimées : 3 038 millions de barils.
  * Coût moyen de développement des réserves : 10 $ par baril.
  * Durée de vie des concessions : 12 ans.
  * Prix du baril au moment de l'analyse : 22,38 $.
  * Coût de production, taxes et redevances : environ 7 $ par baril.
  * Taux d'actualisation des obligations (taux sans risque) : 9,00 %.
  * Revenu de production nette (dividende implicite) : environ 5 % de la valeur des réserves développées.
  * Variance des prix du pétrole : 0,03.
  * Valeur des réserves non développées estimée par option : 13,306 milliards de dollars.
* **Exemple de l'option d'expansion (Logiciel Secure Mail) :**
  * Valeur actuelle des flux de l'expansion (S) : 40 millions sur 10 ans à 12 % = 226 millions de dollars.
  * Prix d'exercice (coût du développement du nouveau logiciel) (K) : 500 millions de dollars.
  * Période (T) : 5 ans.
  * Volatilité ($\sigma$) : 50 %.
  * Taux sans risk ($r$) : 3 % (rendement des emprunts d'État à 5 ans).
  * Valeur de l'option d'expansion : 56 millions de dollars (portant la valeur totale de la société de 115 millions en DCF simple à 171 millions avec l'option).
* **Règles juridiques et fiscales :** 
  * Les brevets garantissent l'exclusivité (propriété intellectuelle), condition sine qua non pour valoriser l'option.
  * _À vérifier à la source officielle_ pour l'application des règles fiscales d'amortissement de la R&D et des brevets selon les juridictions locales.

---

### 4. Conseils concrets et leurs limites ou risques
* **Conseils :**
  * Ne rejetez pas automatiquement un projet à VAN négative s'il offre des droits exclusifs ou une flexibilité future (options de croissance ou de retard).
  * Considérez l'incertitude non pas comme un danger absolu, mais comme un facteur créateur de valeur pour les projets modulables.
  * Intégrez la valeur de la flexibilité (abandon, extension, report) dans l'évaluation globale de l'entreprise (notamment dans la tech et la pharma).
* **Limites et risques :**
  * **Complexité des modèles :** L'utilisation de Black-Scholes ou de modèles binomiaux sur des actifs réels repose sur des estimations subjectives (volatilité, coûts futurs, flux espérés) qui peuvent générer des résultats très bruités ou erronés.
  * **Double comptage :** Attention à ne pas surévaluer une entreprise en additionnant des flux de trésorerie actualisés (DCF) optimistes avec des taux de croissance élevés *et* la valeur de brevets ou de R&D future sans ajuster les hypothèses.
  * **Exclusivité requise :** Si le projet ou le brevet n'est pas protégé par des barrières légales solides (exclusivité), l'option perd toute sa valeur car des concurrents peuvent s'emparer du marché sans payer le coût initial.

---

### 5. Produits, applications ou entreprises cités
* **Entreprises et marques mentionnées (exemples d'analyse pédagogique) :**
  * *Apple, Samsung* (fabricants de téléphones portables - exemples hypothétiques).
  * *Tesla* (options d'achat/vente sur actions, capitalisation boursière et valorisation de l'innovation/conduite autonome).
  * *Biogen* (médicament Avonex pour la sclérose en plaques - cas réel d'évaluation de brevet).
  * *Merck, Pfizer, Upjohn, Glaxo* (industrie pharmaceutique et gestion des brevets).
  * *Novartis, Roche* (comparaisons sectorielles).
  * *Gulf Oil* (valorisation des réserves pétrolières non développées).
  * *Exxon* (comparaisons sur le secteur pétrolier).
  * *Airbus et Lear Aircraft* (joint-venture et option d'abandon).
  * *Facebook (Meta)* (analyse critique de la valorisation de la plateforme publicitaire et de la "marge de sécurité").
  * *Google* (comparaison sur la capitalisation et la R&D).
  * *Bloomberg* (mentionné comme source potentielle de données de volatilité, bien que jugé insuffisant pour les options réelles).
* **Statut :** Tous ces noms de sociétés sont utilisés par le professeur **Aswath Damodaran** (auteur du cours et de la présentation) à des fins **uniquement pédagogiques et d'illustration académique**. Il ne s'agit en aucun cas de publicité commerciale ou de recommandations d'investissement personnelles.
