# Séance 4 : Vue d’ensemble du DCF et premiers pas vers les taux sans risque

Vidéo : https://youtu.be/oFz94rZbc4c · durée 1:24:47 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

---

### 1. Sujet et thèse principale

* **Sujet :** L’utilisation des taux sans risque dans l’évaluation financière par flux de trésorerie actualisés (DCF) et les complexités liées aux devises, aux taux bas/négatifs et au risque souverain.
* **Thèse principale :** Le choix du taux sans risque et la cohérence entre la devise des flux de trésorerie et celle du taux d’actualisation sont essentiels. L'inflation est le principal moteur des taux et des variations de change, ce qui garantit qu'une évaluation correcte (en termes nominaux ou réels) donne la même valeur finale quelle que soit la monnaie choisie.

---

### 2. Notions expliquées (définitions simples)

* **Taux sans risque (Risk-free rate) :** Le rendement théorique d'un investissement sans risque de défaut (généralement adossé à des obligations d'État à long terme, comme les bons du Trésor américain).
* **Inflation :** La hausse générale des prix ; elle est présentée comme le moteur fondamental des taux d'intérêt et des taux de change.
* **Taux nominaux vs Réels :** Les taux nominaux incluent l'attente d'inflation, tandis que les taux réels s'en affranchissent.
* **Quantitative Easing (Assouplissement quantitatif) :** Politique monétaire des banques centrales visant à injecter des liquidités pour faire baisser les taux d'intérêt (phénomène ayant maintenu les taux bas pendant la décennie précédant la vidéo).
* **Taux d'intérêt négatifs :** Situation observée dans certaines devises (ex. : en Europe en septembre 2019) où les obligations d'État affichent des rendements inférieurs à zéro. L'orateur insiste sur le fait qu'en valorisation, il faut normaliser ces taux plutôt que d'utiliser des taux négatifs aberrants.
* **Valeur de l'entreprise (Firm Value) vs Valeur des capitaux propres (Equity Value) :**
  * *Firm Value :* Basée sur les flux de trésorerie vers l'entreprise (FCFF) actualisés au coût du capital (WACC).
  * *Equity Value :* Basée sur les flux vers les actionnaires (FCFE) actualisés au coût des fonds propres.
* **Principe de cohérence :** Ne jamais mélanger des flux de trésorerie post-dette (capitaux propres) avec un taux d'actualisation pré-dette (coût du capital), sous peine de fausser complètement l'évaluation.
* **Économies d'échelle / Effet de levier opérationnel :** Relation entre la croissance des revenus et celle des charges d'exploitation. Un modèle d'économies d'échelle implique que les coûts croissent plus lentement que les revenus.

---

### 3. Chiffres, taux, plafonds et règles fiscales cités (avec dates)

* **Exemple brésilien (Cours) :**
  * Taux sans risque en Reais (BRL) : **7,5 %**
  * Taux sans risque en USD : **2,5 %**
* **États-Unis :**
  * Taux des bons du Trésor à 10 ans mentionnés dans un test de valorisation : **4,36 %** (3 mois), **4,58 %** (10 ans), **4,80 %** (30 ans), **2,26 %** (TIPS - protégés contre l'inflation). *(À vérifier à la source officielle)*
* **Europe :**
  * Taux sans risque négatif pour l'euro en **septembre 2019**. *(À vérifier à la source officielle)*
* **Exemple chiffré de valorisation (Diapositive 9-10) :**
  * Coût des capitaux propres : **13,625 %**
  * Coût de la dette (avant impôt) : **10 %** ; taux d'impôt : **50 %** -> Coût de la dette après impôt : **5 %**.
  * Coût du capital (WACC) : **9,94 %**.
  * Valeur de marché des capitaux propres : **1 073 millions $** ; Valeur de la dette : **800 millions $**.
* **Exemples de spreads souverains (janvier 2024 / janvier 2025) :**
  * Brésil (USD) : Taux de l'obligation de **7,75 %** (avec un taux sans risque de **4,58 %**), soit un *Default Spread* de **3,17 %**.
  * Inde (janvier 2025) : Taux de l'obligation en roupies à 10 ans : **6,82 %** ; spread de défaut souverain (notation Baa3) : **2,18 %**.

---

### 4. Conseils concrets et leurs limites ou risques

* **Conseil :** Toujours maintenir la cohérence de la devise. Si l'on évalue en monnaie locale (ex. : Reais ou Roupies), il faut intégrer l'inflation locale et un taux sans risque ajusté du risque de défaut souverain (via le *default spread* ou les *CDS spreads*).
* **Limite / Risque :** Ne jamais appliquer des taux sans risque ou d'intérêt aberrants (négatifs ou artificiellement bas suite à des politiques monétaires extrêmes) sans procéder à une « normalisation ».
* **Piège comptable majeur :** Ne pas oublier de traiter les contrats de location (*leases*) comme de la dette lors du calcul du capital investi et de la valeur de l'entreprise.

---

### 5. Produits, applications ou entreprises cités

* **Goldman Sachs :** Mentionné comme exemple d'institution financière fournissant des salaires ou des offres (sans lien publicitaire direct).
* **Microsoft, Tesla, Nvidia, Coca-Cola, Apple :** Utilisés comme exemples théoriques pour illustrer la croissance, les marges brutes, les économies d'échelle et les structures de capital. *(Il s'agit d'exemples pédagogiques de l'auteur, non de recommandations d'investissement publicitaires).*
* **Cabinets / Manuels de référence mentionnés :** Damodaran (l'auteur lui-même), Damodaran & Fells, Kroll, S&P, Moody's.
