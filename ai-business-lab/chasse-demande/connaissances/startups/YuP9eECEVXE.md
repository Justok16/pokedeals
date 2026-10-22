# It’s a boat, it’s a plane, it’s REGENT’s Seaglider | E2205

Vidéo : https://youtu.be/YuP9eECEVXE · durée 1:15:14 · résumé Gemini (gemini-3.8-flash) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche synthétique récapitulant les informations issues de la vidéo :

---

### 1) Sujet et thèse principale

* **Sujet :** L'émission *This Week in Startups* (animée par Alex) présente trois jeunes pousses technologiques en développement :
  1. **REGENT :** Développe un « seaglider » électrique (véhicule hybride combinant bateau à hydrofoils et vol en effet de sol) destiné au transport côtier de passagers, de fret et à des missions de défense.
  2. **Convexia :** Entreprise appliquant des agents d'intelligence artificielle (IA/ML) pour détecter, évaluer et relancer des molécules pharmaceutiques sous-exploitées ou abandonnées, notamment pour traiter les maladies rares et ultra-rares.
  3. **Archil :** Système de mise en cache distribuée de données cloud (ex. AWS S3) pour faire apparaître le stockage cloud comme un stockage local ultra-rapide (compatible POSIX) à moindre coût.
* **Thèse principale :** Les avancées récentes en matériel, en modèles d'apprentissage automatique (ML) et en architectures logicielles permettent de repenser des secteurs industriels lourds (transport régional, développement pharmaceutique, infrastructure cloud) avec des modèles de coûts nettement plus compétitifs et de meilleures performances.

---

### 2) Notions expliquées

* **Seaglider (Planeur marin) :** Véhicule hybride fonctionnant en trois modes : flottaison (*float*), sustentation sur foils marins (*foil*) à vitesse intermédiaire, puis vol en effet de sol (*fly*).
* **Effet de sol (*Ground effect*) :** Phénomène aérodynamique par lequel l'air est comprimé entre l'aile et la surface de l'eau, créant un coussin d'air qui augmente considérablement la portance et réduit la consommation d'énergie.
* **Réglementation maritime pour aéronefs à effet de sol (*Wing-in-Ground Craft*) :** Véhicules naviguant/volant très bas (ex. 30 pieds / ~9 mètres au-dessus de l'eau) et réglementés juridiquement comme des navires (sous l'autorité des garde-côtes) et non comme des avions civils.
* **Molécules « shelved » (mises au placard) :** Molécules pharmaceutiques dont le développement a été stoppé non pas pour cause d'inefficacité intrinsèque, mais pour des raisons stratégiques de laboratoire, de changements de priorités ou de design d'essais cliniques défaillant.
* **Digital Twin (Jumeau numérique) en pharma :** Modélisation informatique simulant le comportement d'un essai clinique (fabrication, stratification des patients, posologie) pour anticiper les chances de succès avant les tests réels.
* **Modèles ML vs Modèles physiques :** Passage d'outils de bio-informatique basés sur des simulations physiques traditionnelles (*in silico*) à des modèles prédictifs fondés sur l'apprentissage automatique (plus rapides et capables d'analyser des ensembles de données massifs).
* **Object Storage (Stockage objet, ex. S3) :** Stockage cloud économique mais à latence élevée, facturé au volume de données stockées et aux opérations, par opposition au stockage en blocs / disques SSD locaux.
* **Compatible POSIX :** Norme permettant à des applications logicielles classiques d'interagir avec des fichiers et dossiers distants comme s'ils étaient stockés directement sur le disque dur local.

---

### 3) Chiffres, taux, règles et dates cités

* **Date de l'émission :** Vendredi 7 novembre 2025 (*remarque : date formulée dans le podcast*).
* **REGENT :**
  * Trajet Providence – New York : environ 180 miles (~290 km) réalisable sur batterie en environ 1 heure pour un prix estimé inférieur à 100 $.
  * Vitesse sur hydrofoils : environ 50 mph (~80 km/h).
  * Altitude de vol en effet de sol : environ 30 pieds (~9 mètres) au-dessus de l'eau. Tolérance aux vagues jusqu'à 5 pieds (~1,5 m).
  * Prototype *Viceroy* : capacité de 12 passagers ou 3 500 livres (~1 580 kg) de charge utile.
  * Carnet de commandes / réservations : estimé à 7 milliards de dollars fin 2023, 9 milliards en 2024, dépassant 10 milliards de dollars au moment de l'enregistrement.
  * Contrats avec le corps des Marines américains (*US Marine Corps*) : 15 millions de dollars sur 3 ans.
  * Usine de fabrication à Quonset (Rhode Island) : 250 000 pieds carrés (~23 200 m²), projet d'un coût de 50 millions de dollars.
  * Levée de fonds de REGENT : 60 millions de dollars levés au total jusqu'à la Série A.
  * Calendrier annoncé : ouverture de l'usine au printemps, premières livraisons commerciales prévues en 2027.
* **Pharmacie & Convexia :**
  * Taux d'échec : seuls 5 % à 10 % des médicaments entrant en phase 1 atteignent le marché. Moins de 5 % des maladies rares connues bénéficient d'un traitement approuvé.
  * Définition citée d'une maladie rare (selon les critères américains) : touche moins de 200 000 personnes aux États-Unis par an (*à vérifier à la source officielle*).
  * Définition citée d'une maladie ultra-rare : touche moins de 50 000 personnes aux États-Unis (*à vérifier à la source officielle*).
  * Mention des mécanismes d'incitation réglementaire de la FDA : bons de revue prioritaire (*Priority Review Vouchers* / PRV, CNPV) (*à vérifier à la source officielle*).
* **Archil :**
  * Performances annoncées : réduction des coûts de stockage jusqu'à 90 % par rapport à l'utilisation de disques SSD cloud traditionnels (EBS) et latence jusqu'à 30 fois inférieure à celle d'AWS S3.
  * Coût indicatif mentionné : S3 Express One Zone à environ 0,11 $ par Go ; Archil facturé environ 0,26 $ par « Go actif » par mois.

---

### 4) Conseils concrets, limites et risques

* **Transport & mobilité :**
  * *Intérêt :* Les liaisons côtières via véhicules à effet de sol offrent une alternative plus rapide et potentiellement moins coûteuse que les trains ou ferries lents, tout en contournant la saturation et les contraintes des aéroports.
  * *Limites/Risques :* Dépendance aux conditions météo marines (houle importante) ; nécessité d'obtenir des autorisations d'exploitation et de navigation dans des zones maritimes denses ; calendrier de commercialisation dépendant de la certification des prototypes (horizon 2027).
* **Développement de médicaments (Biotech) :**
  * *Intérêt :* Se focaliser sur le repositionnement de molécules et les maladies rares permet à des structures légères de cibler des marchés rentables (dépenses R&D réduites, accès à des incitations réglementaires) sans nécessiter les milliards de dollars des grands groupes pharmaceutiques.
  * *Limites/Risques :* Incertitude scientifique et biologique résiduelle ; risque d'échec clinique même après modélisation algorithmique ; accès contractuel difficile à la propriété intellectuelle privée mise au placard par les grands laboratoires.
* **Infrastructure Cloud & Gestion des coûts d'ingénierie :**
  * *Intérêt :* Adapter les architectures de stockage pour ne payer que les données réellement lues/utilisées (« actives ») au lieu de pré-allouer des volumes SSD sous-utilisés.
  * *Limites/Risques :* Risque de surcoût si les algorithmes de pré-chargement en cache (*pre-caching*) anticipent mal les données nécessaires ; dépendance opérationnelle vis-à-vis des hébergeurs sous-jacents (AWS, GCP, etc.).

---

### 5) Produits, applications et entreprises cités

* **Startups invitées :**
  * **REGENT** (regentcraft.com) : Fabricant de seagliders.
  * **Convexia** (convexia.bio) : Plateforme d'IA dédiée à la R&D et au repositionnement pharmaceutique.
  * **Archil** (archil.com / disc.new) : Infrastructure logicielle de mise en cache cloud pour développeurs.
* **Sponsors et publicités (clairement identifiés comme tels dans l'émission) :**
  * **Pipedrive** (pipedrive.com/twist) : Logiciel CRM pour PME.
  * **LinkedIn Ads** (linkedin.com/thisweekinstartups) : Plateforme publicitaire B2B.
  * **Sentry** (sentry.io/twist) : Outil de suivi des erreurs logicielles et de débogage applicatif par IA.
* **Autres entreprises, produits ou entités mentionnés :**
  * *Transport / Aérospatiale :* Boeing, Cessna, Twin Otter, SailGP, America's Cup, Amtrak, Southwest Airlines.
  * *Défense :* Anduril, Raytheon / RTX, Saab, General Dynamics, Naval Undersea Warfare Center, US Marine Corps.
  * *Tech / Cloud :* AWS (Amazon Web Services, S3, EBS), Google Cloud Platform (GCP), Microsoft Azure, Snowflake, Databricks, Vercel, Modal, CoreWeave.
  * *Biotech / Pharma :* Schrödinger, Recursion, Pfizer, Merck.
  * *Investisseurs :* Felicis Ventures (et son associée Astasia Myers), Redpoint.
