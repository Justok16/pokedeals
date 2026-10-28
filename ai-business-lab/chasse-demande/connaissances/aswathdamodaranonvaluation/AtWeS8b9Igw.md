# Session 6 : Bêtas ascendants

Vidéo : https://youtu.be/AtWeS8b9Igw · durée 1:37:53 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-28
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances en finances personnelles basée sur la vidéo :

---

### **Fiche de Connaissances : Évaluation des Risques et du Bêta**

#### **1. Sujet et Thèse principale**
* **Sujet :** L’analyse du risque des actions à travers le « bêta » (mesure de la volatilité d'une action par rapport au marché), les limites des régressions historiques, et la méthode "bottom-up" (approche ascendante) pour estimer le coût des capitaux propres et le risque des entreprises, en particulier pour les conglomérats ou les entreprises ayant des structures de capital complexes.
* **Thèse principale :** Les bêtas de régression issus des données historiques sont souvent inefficaces, car rétroactifs, sensibles à la manipulation, et « bruyants ». L'approche « bottom-up », qui consiste à moyenner les bêtas de comparables non endettés (unlevered betas) par secteur d'activité, permet d'obtenir une mesure du risque beaucoup plus précise, adaptable et robuste, notamment pour les entreprises diversifiées.

---

#### **2. Notions expliquées (Définitions simples)**
* **Taux sans risque (Risk-free rate) :** Le rendement d'un investissement considéré comme sans risque de défaut (généralement un emprunt d'État à long terme), utilisé comme base pour calculer le rendement attendu.
* **Bêta (Beta) :** Mesure de la sensibilité ou de la volatilité d'une action par rapport aux fluctuations du marché global.
  * Un bêta > 1 indique une action plus volatile que le marché.
  * Un bêta < 1 indique une action moins volatile.
  * Un bêta négatif (très rare, ex: mines d'or) évolue à l'inverse du marché.
* **Bêta non endetté / Bêta d'actif (Unlevered Beta) :** Le risque propre des opérations d'une entreprise, isolé de l'effet de sa dette financière.
* **Bêta endetté (Levered Beta) :** Le bêta d'une action qui prend en compte à la fois le risque opérationnel de l'entreprise et son niveau d'endettement.
* **Coût des capitaux propres (Cost of Equity) :** Le rendement minimum exigé par les actionnaires pour investir dans une entreprise, calculé via le modèle CAPM (Taux sans risque + Bêta × Prime de risque des actions).
* **Levier opérationnel (Operating Leverage) :** La proportion des coûts fixes par rapport aux coûts totaux. Un fort levier opérationnel accentue la volatilité des bénéfices.
* **Levier financier (Financial Leverage) :** L'utilisation de la dette par une entreprise pour financer ses activités, ce qui augmente le risque des capitaux propres.
* **Enterprise Value (Valeur d'entreprise) :** La valeur totale d'une entreprise, calculée comme la valeur de marché des capitaux propres plus la dette, moins la trésorerie.

---

#### **3. Chiffres, Taux, Plafonds et Règles fiscales**
*(Note : À vérifier à la source officielle)*
* **Taux sans risque (États-Unis, nov. 2013) :** 2,75 % (rendement des obligations du Trésor américain à 10 ans).
* **Prime de risque sur actions (Equity Risk Premium) :** 5,76 % (utilisée pour Disney en nov. 2013).
* **Alpha de Jensen (exemple Disney, période non précisée précisément dans l’extrait, mais analysée sur plusieurs années) :** 7,19 %.
* **Règle fiscale (déductibilité des intérêts de la dette) :** Dans de nombreuses juridictions (notamment aux États-Unis), les intérêts payés sur la dette sont fiscalement déductibles, créant un « bouclier fiscal » (tax shield) représenté par le facteur $1 - t$ (où $t$ est le taux marginal d'imposition).
* **Règle fiscale locale :** Les règles fiscales varient selon les pays (ex. : aux États-Unis et dans d'autres pays développés vs. pays du Moyen-Orient où l'impôt sur le revenu n'est pas structuré de la même manière). *À vérifier à la source officielle selon la juridiction.*

---

#### **4. Conseils concrets et Leurs Limites / Risques**
* **Conseil 1 : Ne pas se fier uniquement aux bêtas de régression historiques.**
  * *Limites / Risques :* Ils regardent le passé, sont trop bruyants (fortes marges d'erreur) et peuvent être manipulés en changeant la période d'analyse ou l'indice de référence.
* **Conseil 2 : Utiliser l'approche "Bottom-Up" pour estimer les bêtas des entreprises diversifiées.**
  * *Limites / Risques :* Nécessite de trouver des entreprises comparables pertinentes et d'ajuster correctement les ratios de structure financière (dette/fonds propres) et les taux d'imposition marginaux.
* **Conseil 3 : Éviter d'appliquer un coût du capital global unique à des divisions multiples dans une grande entreprise.**
  * *Limites / Risques :* Subventionner des projets risqués avec des divisions sûres conduit à de mauvaises décisions d'allocation du capital (surinvestissement dans les activités à haut risque et sous-investissement dans les activités sûres).

---

#### **5. Produits, Applications ou Entreprises cités**
* **Bloomberg (Terminal) :** Mentionné comme source pour les données financières et de régression bêta (fourni par l'intervenant pour les exercices). *(Outil professionnel payant / Pas de publicité de l'auteur)*
* **Yahoo Finance, Value Line, Google Finance :** Mentionnés comme sources alternatives pour trouver des bêtas et des données financières. *(Outils tiers / Pas de publicité de l'auteur)*
* **Entreprises citées à titre d'exemples pédagogiques :**
  * *Tata Motors*
  * *The Walt Disney Company*
  * *Google (Alphabet), Apple, General Electric (GE), ExxonMobil, Altria (Philip Morris), Bulgari, Qwest Communications, Harmony Gold Mining, Vale, Deutsche Bank, Coca-Cola, New York Times, Southwest Airlines, United Airlines, Starbucks, Kmart, Banana Republic, Old Navy.*
  * *(Toutes ces citations reliennent à des cas pratiques d’analyse financière et ne constituent pas des recommandations d'achat ou de la publicité commanditée).*
