# Séance 5 (MBA de Val) : Conclusion sur les taux sans risque et premiers pas sur les primes de ris...

Vidéo : https://youtu.be/l2ZDQ3HHaNM · durée 1:23:48 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo sous forme de fiche de connaissances en finance :

---

# Fiche de Connaissances : Évaluation du Risque, de la Prime de Risque et des Taux Sans Risque

## 1. Sujet et Thèse Principale
* **Sujet :** L’estimation des taux sans risque, des primes de risque historiques et des primes de risque de pays (ou d'entreprise) dans le cadre de la valorisation d'actifs et de multinationales.
* **Thèse principale :** L'utilisation de données historiques ou de taux étrangers sans ajustement rigoureux (notamment concernant l'inflation et la monnaie) conduit à des erreurs majeures en valorisation. L'orateur soutient qu'il ne faut pas « normaliser » les taux sans risque, que l'inflation est le facteur clé expliquant les différences de taux entre pays, et que l'exposition géographique d'une entreprise se mesure par ses **revenus** et non par son pays d'incorporation.

---

## 2. Notions Expliquées (Définitions Simples)
* **Taux sans risque (Risk-Free Rate) :** Le taux de rendement attendu d'un investissement sans risque de défaut (généralement adossé à des obligations d'État, comme les T-Bonds américains).
* **Prime de risque historique sur actions (Historical Equity Risk Premium - ERP) :** La différence de rendement annualisé entre l'investissement en actions et un actif sans risque sur une période passée.
* **Prime de risque de pays (Country Risk Premium - CRP) :** Un supplément de rendement exigé par les investisseurs pour investir dans des pays émergents ou présentant un risque politique/économique supérieur.
* **Inflation :** Le moteur principal expliquant la divergence des taux sans risque entre différentes monnaies.
* **Lambda ($\lambda$) :** Facteur mesurant l'exposition relative d'une entreprise au risque d'un pays (basé généralement sur la répartition de ses revenus).
* **Biais de survie (Survivorship Bias) :** Erreur statistique consistant à n'étudier que les marchés qui ont "survécu" et prospéré (comme les États-Unis au XXe siècle), surévaluant ainsi les primes de risque passées.
* **Moyenne Arithmétique vs Géométrique :** 
  * *Arithmétique :* Somme des rendements divisée par le nombre de périodes (souvent utilisée pour estimer l'année suivante).
  * *Géométrique :* Taux de croissance composé annualisé (utilisé pour le long terme).

---

## 3. Chiffres, Taux, Plafonds et Règles Fiscales Cités
*(Attention : règles et données historiques mentionnées par le conférencier — à vérifier à la source officielle)*

* **Exemple de multinationale suisse :**
  * 10 % en francs suisses (taux sans risque : 0,5 %)
  * 30 % en euros (taux sans risque : 1 %)
  * 40 % en dollars US (taux sans risque : 2,5 %)
  * 20 % en roupies indiennes (taux sans risque : 6 %)
* **Exemple d'inflation et de taux (Égypte / USA) :**
  * Taux sans risque USD : 2,00 % | Inflation USA : 1,50 %
  * Inflation égyptienne : 15 %
  * Taux sans risque en livres égyptiennes calculé par différentiel d'inflation : **15,57 %**
* **Exemple d'obligations US (1er janvier 2022) :**
  * Taux des obligations à 10 ans aux États-Unis : **1,51 %** (historiquement bas).
* **Primes de risque historiques aux USA (exemples de tableaux cités) :**
  * Période 1928-2023 (Arithmétique) : Actions vs T-Bonds = **8,32 % - 6,80 %**
  * Période 1928-2023 (Géométrique) : Actions vs T-Bonds = **6,50 % - 5,23 %**
* **Exemples d'entreprises et d'expositions (données passées) :**
  * *Tata Motors* : ~91,37 % de revenus en Inde, TCS ~7,62 %.
  * *Embraer* (2004) : 97 % des revenus hors du Brésil (Europe/Amérique du Nord).
  * *Ambev* (2011) : Répartition multi-pays (Brésil 70 %, Argentine 4 %, etc.).
  * *Royal Dutch Shell* (2015) : Répartition mondiale de production pétrolière (taux ERP global de référence : **8,26 %**).
  * *Coca-Cola* (2012) : Répartition du chiffre d'affaires par région (Europe 19 %, Amérique du Nord 40%, etc. ; ERP global : **7,14 %**).
* **Exemple Brésil (janvier 2024) :**
  * Prime de défaut pour le Brésil (basée sur le spread des obligations) : **3,28 %**
  * ERP Mature : **4,60 %**
  * ERP Total pour le Brésil (somme) : **7,88 %** (ou calculé par volatilité relative : **9,52 %**).
* **Exemple d'évaluation d'Embraer (septembre 2004) :**
  * Taux sans risque US : **4 %**
  * CRP (Brésil) : **7,89 %**
  * Coût des capitaux propres selon différentes approches : entre **11,48 %** et **18,72 %**.

---

## 4. Conseils Concrets, Limites et Risques
* **Ne jamais moyenner les taux sans risque :** Calculer une moyenne simple ou pondérée de taux libellés dans des monnaies différentes n'a aucun sens financier.
* **Ne jamais normaliser le taux sans risque :** Modifier artificiellement un taux sans risque historiquement bas (par exemple, remplacer 1,51 % par une moyenne historique de 5-6 %) fausse toute la valorisation et mène à des incohérences majeures (sous-évaluation des actions).
* **Règle de consistance monétaire et d'inflation :** Si vous estimez les flux futurs d'une entreprise dans une devise, utilisez le taux sans risque et l'inflation de cette même devise (ou ajustez par le différentiel d'inflation).
* **Attention aux primes historiques :** Utiliser une seule année de données (ex: l'année précédente) conduit à des aberrations (primes négatives ou nulles en cas de crise). Il faut des horizons longs, mais les données historiques lointaines intèrent un biais de survie et une forte volatilité (erreurs types élevées).
* **Exposition géographique :** Pour évaluer le risque pays d'une multinationale, basez-vous sur la **répartition géographique de ses revenus** (ou de sa production) plutôt que sur son pays d'immatriculation légale.

---

## 5. Produits, Applications ou Entreprises Cités
* **Bloomberg** (mentionné pour l'accès aux données obligataires et aux taux, outil professionnel).
* **FMI (Fonds Monétaire International)** (source de prévisions d'inflation et de données macroéconomiques).
* **Moody’s / S&P** (agences de notation souveraine utilisées pour déterminer les spreads de défaut et les notes des pays).
* **MSCI / Emerging Markets Government Bonds** (indices de référence).
* **Entreprises citées à titre pédagogique (études de cas) :** Nestlé, Heineken, Embraer, Ambev, Tata Motors, TCS, Royal Dutch Shell, Coca-Cola, Microsoft, S&P 500, Bovespa.
  * *Note :* Aucune de ces entreprises ni aucun outil n'est présenté sous forme de placement publicitaire ; il s'agit d'exemples académiques et pratiques présentés par l'auteur (Aswath Damodaran) pour illustrer ses modèles financiers.
