# Séance 6 (MBA de Val) : Primes de risque implicites sur actions et bêtas

Vidéo : https://youtu.be/b_ixJHotsCc · durée 1:21:05 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo sous forme de fiche de connaissances en finance personnelle, structurée selon vos consignes :

---

# Fiche de connaissances : Tests de prime de risque implicite et évaluation financière

## 1. Sujet et thèse principale
* **Sujet :** L’estimation de la prime de risque implicite sur les actions (ERP - *Equity Risk Premium*), son évolution historique, son comportement en période de crise, et les limites des mesures du risque relatives (notamment le bêta) en finance d'entreprise.
* **Thèse principale :** Les primes de risque historiques fondées sur le passé sont inadaptées car figées et incapables de refléter les changements structurels ou les crises. L'approche « forward-looking » (implicite, basée sur les flux de trésorerie actualisés et les cours boursiers) est plus dynamique, mais sensible aux chocs macroéconomiques (inflation, crises). Par ailleurs, les mesures traditionnelles du risque (comme le bêta du CAPM) présentent de graves limites statistiques et conceptuelles, justifiant le recours à des approches alternatives (comme les bêtas *bottom-up*).

---

## 2. Notions expliquées
* **Prime de risque historique :** Prime calculée en regardant les rendements passés des actions par rapport aux obligations d'État (souvent sur de longues périodes). Inconvénient : ne s'adapte pas aux changements du présent.
* **Prime de risque implicite (ERP) :** Prime calculée à partir des cours boursiers actuels, des dividendes/rachats d'actions attendus, et d'un taux de croissance futur escompté, en résolvant le taux d'actualisation (TRI) qui équilibre la valeur actuelle et les flux futurs.
* **Taux sans risque (Risk-Free Rate) :** Rendement d'un investissement théoriquement sans risque (souvent adossé aux obligations d'État à long terme, ex. T-Bond).
* **Bêta (CAPM) :** Mesure de la volatilité d'une action par rapport au marché global. Le bêta de régression mesure la pente de la droite entre les rendements de l'action et ceux de l'indice de marché.
* **Bêta dé-levieré (Unlevered Beta) :** Bêta d'une entreprise purgée de sa structure financière (endettement), mesurant uniquement le risque opérationnel.
* **Bêta bottom-up :** Méthode consistant à estimer le bêta d'une entreprise en prenant la moyenne des bêtas dé-levierés de sociétés comparables opérant dans le même secteur, puis en ré-ajustant selon sa propre structure financière et opérationnelle.

---

## 3. Chiffres, taux, plafonds et règles fiscales cités
* **Janvier 2020 :** Prime de risque implicite (ERP) évaluée à **5,20 %** (pour un taux sans risque de 1,92 % et un rendement attendu des actions de 7,12 %).
* **14 février 2020 (avant COVID) :** ERP à environ **4,00 % à 4,50 %**.
* **23 mars 2020 (crise COVID) :** ERP grimpant à **7,75 % - 8,00 %** (chute de 36 % du S&P 500).
* **Septembre 2020 :** Retour de l'ERP à environ **4,50 %**.
* **Fin 2021 / Début 2022 :** ERP à **4,24 %** (plus bas historique ou proche, pour un taux sans risque autour de 1,51 % et un rendement attendu des actions de 5,74 %).
* **Fin 2023 :** Prime de risque historique à long terme (1928-2023) : **8,32 %** ; ERP historique moyen : **4,25 %** ; ERP à fin 2023 : **4,60 %** ; Taux sans risque (T-Bond) : environ **3,88 %** (monté à près de 4 % plus tard).
* **Années 1960 :** ERP stable entre **3,0 % et 3,5 %**.
* **Années 1970 (Crise pétrolière, stagflation) :** Pic d'inflation et de l'ERP (ex. 1978 : ERP à **6,5 %**, Dow Jones à **7,50 %**).
* **Années 1990 (.com boom) :** Baisse de l'ERP aux États-Unis jusqu'à environ **2 %**.
* **Règle fiscale / légale :** *À vérifier à la source officielle* pour toute application des taux d'actualisation, déductibilité fiscale des intérêts de la dette (terme $(1-t)$ dans les formules de levier financier) et règles comptables locales.

---

## 4. Conseils concrets, limites et risques
* **Ne pas se fier aveuglément aux primes historiques :** Utiliser des moyennes arithmétiques historiques fige les valorisations et conduit à surévaluer massivement les actions en période de taux bas ou de fortes turbulences.
* **Privilégier l'approche implicite et forward-looking :** Elle permet d'aligner la valorisation sur les conditions actuelles du marché.
* **Risque de l'inflation :** L'inflation est « corrosive » et détruit la valeur des actifs risqués (actions), car elle accroît l'incertitude et fait fuir les investisseurs vers la sécurité.
* **Limites des bêtas de régression (CAPM) :** Les bêtas calculés par régression historique ont une forte erreur standard, sont rétrospectifs (ne prédisent pas l'avenir), dépendent du choix de l'indice de référence, et subissent le bruit du marché (ex. cas extrêmes comme GameStop).
* **Alternative robuste :** Utiliser les bêtas *bottom-up* par secteur pour s'affranchir du bruit statistique des actions individuelles.

---

## 5. Produits, applications ou entreprises cités
* **S&P 500 / Dow Jones / MSCI :** Indices boursiers de référence (utilisés comme proxys du marché).
* **Bloomberg :** Terminal et outil de données financières mentionné pour l'extraction des bêtas de régression et graphiques historiques (*publicité / outil professionnel de l'orateur*).
* **GameStop (GME) :** Exemple extrême de volatilité boursière et de « bruit » statistique rendant le bêta historique caduc en période de spéculation de détail.
* **Nokia / GoDaddy :** Exemples d'entreprises aux bêtas aberrants ou fortement dépendants du choix de l'indice de référence.
* **Airbnb (ABNB) / Hôtels vs. Sociétés immobilières (REITs) :** Exemples sectoriels pour illustrer l'impact de l'levier opérationnel et financier sur le risque.
* **Netflix / Amazon Prime :** Exemples de consommation récurrente et de coûts fixes/variables pour illustrer l'élasticité de la demande et le risque opérationnel.
