# Séance 13 : Gérer l'incertitude et approfondir les analyses de projet

Vidéo : https://youtu.be/vxuuxJ68Dj8 · durée 1:16:17 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances basée sur la vidéo de cours de finances animée par Aswath Damodaran (NYU Stern) :

---

# Fiche de connaissances – Analyse de projets, incertitude et évaluation d'entreprise

## 1. Sujet et thèse principale
* **Sujet :** La gestion de l'incertitude dans l'analyse de projets d'investissement, l'évaluation d'entreprises (Disney, Vale, Harman) et la prise de décision financière (actualisation, VAN, TRI, analyse de sensibilité, simulations et fusions-acquisitions).
* **Thèse principale :** Face à l'incertitude inhérente aux prévisions (tous les chiffres sont des estimations faillibles), les méthodes simplistes (payback, attente) sont insuffisantes. Il faut modéliser rigoureusement le risque (via des simulations, des taux d'actualisation adaptés et une analyse des flux de trésorerie) et se méfier des couvertures de risques (hedging) systématiques qui ne créent pas nécessairement de valeur pour les actionnaires diversifiés.

---

## 2. Notions expliquées (définitions simples)
* **VAN (Net Present Value / Valeur Actuelle Nette) :** Somme des flux de trésorerie futurs actualisés moins l'investissement initial. Si elle est positive, le projet crée de la valeur.
* **TRI (Internal Rate of Return / Taux de Rendement Interne) :** Taux d'actualisation pour lequel la VAN d'un projet est nulle. Il doit être supérieur au coût du capital pour que le projet soit rentable.
* **Payback (Délai de récupération) :** Nombre d'années nécessaires pour récupérer l'investissement initial grâce aux flux de trésorerie générés.
* **Payback actualisé / Discounted Payback :** Payback calculé à partir de flux de trésorerie actualisés (prenant en compte la valeur temps de l'argent).
* **Analyse de sensibilité / What-if Analysis :** Test de l'impact de la variation d'une ou plusieurs variables clés sur le résultat (VAN/TRI).
* **Simulation de Monte-Carlo :** Méthode statistique qui génère des milliers de scénarios en combinant des distributions de probabilités pour différentes variables afin d'obtenir une distribution des résultats possibles (ex. : moyenne, médiane, probabilité de perte).
* **Hurdle Rate (Taux seuil / Coût du capital) :** Taux de rendement minimum exigé pour qu'un investissement soit accepté.
* **ROE (Return on Equity / Rentabilité des capitaux propres) :** Résultat net divisé par la valeur comptable des capitaux propres.
* **Hedging (Couverture de risque) :** Stratégie financière visant à se protéger contre les fluctuations de prix (matières premières, taux de change).
* **Synergie :** Valeur additionnelle créée par la fusion ou l'acquisition de deux entreprises, supérieure à la somme de leurs valeurs individuelles.
* **Working Capital (Besoin en fonds de roulement - BFR) :** Capitaux nécessaires pour financer le cycle d'exploitation à court terme.

---

## 3. Chiffres, taux, plafonds et règles fiscales
* **Exemple Disney (Thérapies / Projets) :**
  * VAN initiale estimée à **3,3 milliards de dollars** en dollars US.
  * Taux d'actualisation en réals brésiliens (BRL) : augmentation à près de **16 %** (en raison de l'inflation).
* **Exemple Radio / Top 40 (Années 1980) :**
  * Syndication à **520 stations** de radio.
  * Coût pour les stations : **1 000 $ par semaine**.
  * Rémunération du DJ (Casey Kasem) : **50 000 $ par semaine** (*à vérifier à la source officielle*).
* **Exemple Mine de fer Vale (Brésil) :**
  * Investissement initial : **1,25 milliard de dollars**.
  * Capacité de production : **8 millions de tonnes par an** (atteinte à partir de l'année 4).
  * Valeur de récupération (salvage value) : **250 millions de dollars** à la fin de l'an 10.
  * Taux d'inflation supposé : **2 % par an**.
  * Coût variable (exploitation, main-d'œuvre, matériel) : **45 $ par tonne**.
  * BFR : **20 % du total des revenus** de l'année.
  * Taux d'impôt sur les sociétés : **34 %** (*à vérifier à la source officielle*).
  * Emprunt (emprunt à terme / term loan) : **500 millions de dollars** au taux de **4,05 %** sur **10 ans** en annuités constantes.
  * Coût du capital (fonds propres) pour l'activité minerai de fer : **11,13 %**.
  * VAN finale (en fonds propres) : **304 millions de dollars**.
  * ROE moyen sur la période : **31,36 %**.
* **Exemple Harman International / Tata Motors :**
  * Valeur de marché des capitaux propres de Harman (novembre 2013) : **5,428 milliards de dollars**.
  * Coût du capital (WACC) estimé pour l'acquisition (sans synergie) : **10,28 %**.
  * Bêta sans effet de levier (unlevered beta) : **1,17**.
  * Revenu d'exploitation (Operating income) 2013 : **313,19 millions de dollars** pour **4,297 milliards de dollars** de revenus.
  * Taux d'imposition effectif : **18,21 %**.
  * Croissance à perpétuité (g) : **2,75 %**.
  * Valeur estimée de Harman (avant synergie) : **2,5 milliards de dollars** (comparé au prix du marché de 5,4 milliards, conduisant à une VAN négative d'environ **3 milliards de dollars** sans synergies).
* **Simulation de Monte-Carlo (Disney) :**
  * Probabilité d'avoir une VAN négative : **18 %**.
  * Moyenne de la VAN simulée : **3,40 milliards de dollars** ; Médiane : **3,28 milliards de dollars** (proche du cas de base à 3,29 milliards).
* **Règles fiscales et comptables :**
  * Les charges d'intérêts sont déductibles fiscalement (*à vérifier à la source officielle*), contrairement au remboursement du principal.
  * La dépréciation (amortissement) réduit l'impôt mais n'est pas un décaissement de trésorerie.

---

## 4. Conseils concrets, limites et risques
* **Conseils concrets :**
  * **Ne jamais coder en dur (hardcoder) des chiffres** dans un tableur Excel ; utiliser une page d'entrées (inputs) et une page de sorties (outputs) pour faciliter les modifications.
  * **Moins, c'est plus (Less is more) :** En analyse de sensibilité, ne pas multiplier les variables à l'infini ; se concentrer sur les 2 ou 3 variables motrices (drivers) qui impactent le plus la VAN.
  * **Privilégier la simplicité visuelle :** Utiliser des graphiques clairs (ou des représentations visuelles adaptées comme le graphique de Minard pour Napoléon) plutôt que des tableaux indigestes.
  * **Pour les projets à durée de vie finie (ex. mines) :** Ne pas oublier de comptabiliser la valeur de récupération des actifs et la récupération du BFR à la fin du projet.
  * **Dans le cadre d'une acquisition :** S'assurer que le taux d'actualisation (coût du capital) reflète le risque de la cible (entreprise achetée) et non de l'acquéreur, et que la structure de capital (dette/fonds propres) est cohérente.
* **Limites et risques :**
  * **L'illusion de la certitude :** Toutes les prévisions (revenus, coûts, taux de change, impôts) sont faillibles.
  * **Le piège du Hedging (couverture) :** Hedger systématiquement les risques (taux de change, matières premières) pour des entreprises diversifiées dont les actionnaires ont déjà diversifié leur portefeuille détruit de la valeur ou est inutile (coûts de couverture sans bénéfice réel pour l'actionnaire). Le hedging se justifie principalement pour les entreprises très endettées risquant la faillite (risque de défaut).
  * **Le biais des fusions-acquisitions (M&A) :** Payer une prime d'acquisition trop élevée en se basant sur des synergies hypothétiques mène souvent à détruire de la valeur pour l'actionnaire de l'entreprise acheteuse.

---

## 5. Produits, applications ou entreprises cités
* **Entreprises et marques :**
  * **Disney / Disney+ :** Utilisé comme étude de cas pour l'évaluation de parcs à thèmes (Rio) et la stratégie de streaming (comparaison avec Netflix et HBO). *Exemple académique / pédagogique.*
  * **Vale (Brésil) :** Mine de fer de Vale – étude de cas d'investissement industriel sur 10 ans. *Exemple académique / pédagogique.*
  * **Harman International & Tata Motors :** Étude de cas sur l'acquisition d'Harman par Tata Motors. *Exemple académique / pédagogique.*
  * **Netflix & HBO :** Mentionnés pour comparer leurs modèles de production de contenu et de croissance des abonnés. *Exemples macroéconomiques / sectoriels.*
  * **ExxonMobil / Berkshire Hathaway :** Mentionnés pour illustrer la diversification des investisseurs et l'inutilité du hedging pour les grands groupes mondiaux. *Exemples illustratifs.*
  * **McKinsey & Co. :** Cabinet de conseil mentionné pour illustrer la pratique professionnelle du conseil en stratégie. *Mention contextuelle.*
* **Logiciels et outils :**
  * **Microsoft Excel :** Outil de modélisation financière et de calcul de VAN/TRI.
  * **Crystal Ball :** Logiciel de simulation de Monte-Carlo sous Excel. *Présenté comme un outil puissant d'analyse probabiliste.*
* **Note sur la publicité :** Aucun de ces produits n'est présenté sous forme de placement publicitaire commercial ; ils sont exclusivement utilisés par le professeur Aswath Damodaran comme supports d'enseignement universitaire (NYU Stern).
