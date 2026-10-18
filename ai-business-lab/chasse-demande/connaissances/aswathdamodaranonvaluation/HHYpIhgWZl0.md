# Séance 7 (Étudiants de premier cycle de Val) : Alternatives au bêta, coût des capitaux propres et...

Vidéo : https://youtu.be/HHYpIhgWZl0 · durée 1:17:02 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances en finances personnelles basée sur la vidéo :

---

# Fiche de Connaissances : Bêta et Coût du Capital

## 1. Sujet et Thèse Principale
* **Sujet :** L'estimation du bêta et du coût du capital, l'utilisation des régressions et des approches alternatives (comme le « bottom-up beta » et l'ajustement pour l'endettement) pour évaluer les entreprises.
* **Thèse principale :** Les bêtas traditionnels basés sur les prix historiques sont souvent bruités, en retard et inadaptés pour les investisseurs non diversifiés ou les entreprises aux structures de coûts et d'endettement spécifiques. Il est préférable d'utiliser des approches alternatives (bottom-up betas, mesures comptables ou ajustements de levier) pour obtenir une estimation plus robuste du coût du capital.

---

## 2. Notions Expliquées (Définitions Simples)
* **Bêta ($\beta$) :** Mesure du risque systématique d'une entreprise par rapport au marché. Il indique la sensibilité de l'action aux mouvements du marché.
* **Coût du capital / Coût des fonds propres :** Le taux de rendement exigé par les investisseurs pour investir dans une entreprise, souvent calculé via le CAPM (Modèle d'Évaluation des Actifs Financiers).
* **Diversification de l'investisseur marginal :** Hypothèse selon laquelle l'investisseur type est diversifié et ne se soucie que du risque de marché (capturé par le bêta).
* **ADR (American Depositary Receipt) :** Action étrangère cotée sur un marché boursier américain et libellée en dollars.
* **Bêta unlevered (non endetté) vs Levered (endetté) :** 
    * *Unlevered :* Bêta de l'entreprise sans tenir compte de sa dette (risque opérationnel pur).
    * *Levered :* Bêta intégrant le risque financier lié à l'endettement.
* **Levier opérationnel :** Proportion de coûts fixes par rapport aux coûts variables dans la structure de l'entreprise. Plus les coûts fixes sont élevés, plus le bêta est élevé.
* **Levier financier :** Impact de l'endettement sur le risque de l'action.
* **Dette brute vs Dette nette :** 
    * *Dette brute :* Total des dettes financières figurant au bilan (y compris les baux).
    * *Dette nette :* Dette brute moins la trésorerie et les équivalents de trésorerie.
* **Synthetic Ratings (Notes synthétiques) :** Notation de crédit estimée d'une entreprise basée sur son ratio de couverture des intérêts (EBIT / Frais financiers) lorsque l'entreprise n'a pas de notation officielle.
* **Intérêt Coverage Ratio (Ratio de couverture des intérêts) :** Mesure de la capacité d'une entreprise à payer ses charges d'intérêts (EBIT divisé par les charges d'intérêts).

---

## 3. Chiffres, Taux, Plafonds et Règles Fiscales
* **Exemples de bêtas (Vale et Embraer) :** 
    * Petrobras (Bovespa) : $R^2 = 69\%$, Bêta = $1,66$.
    * Petrobras (S&P 500 / ADR) : $R^2 = 21\%$, Bêta = $1,98$.
    * Embraer : Levery Debt/Equity = $18,95\%$, Unlevered Beta = $0,95$, Levered Beta = $1,07$.
* **Taux d'impôt et barèmes :** 
    * Mention de taux d'imposition effectifs des sociétés (ex. : taux de l'impôt sur les sociétés aux États-Unis, souvent historiquement autour de 35% avant la réforme de 2017, ou taux effectif global variable selon les États).
    * **Règle fiscale / légale :** L'intérêt de la dette est généralement déductible fiscalement (terme $(1 - t)$ dans les formules de coût du capital). *À vérifier à la source officielle selon la juridiction fiscale applicable.*
* **Taux d'intérêt de référence (Risk-Free Rate) :** Basé sur les obligations d'État (ex. : taux des obligations du Trésor américain ou brésilien).
* **Taux d'imposition des sociétés aux USA :** 
    * Historiquement à 35 %, abaissé à 21 % par la réforme fiscale de 2017 (*Tax Cuts and Jobs Act*). *À vérifier à la source officielle (Code des impôts américain / IRS).*

---

## 4. Conseils Concrets, Limites et Risques
* **Limites des bêtas régressés :** Ils sont rétrospectifs (« backward looking »), bruyants et influencés par les bruits de marché à court terme.
* **Conseil pour les entreprises sans historique :** Utiliser la méthode du *Bottom-up Beta* (prendre la moyenne des bêtas non endettés d'entreprises comparables du secteur et ajuster pour la structure financière de la société).
* **Risque de l'utilisation de la dette nette :** L'utilisation de la dette nette pour calculer le levier financier peut mener à des bêtas aberrants ou négatifs en cas de trésorerie excédentaire importante. Il est souvent plus prudent d'utiliser la dette brute (gross debt).
* **Attention aux notations synthétiques :** Les tableaux de correspondance entre ratio de couverture et notation par agence (Moodys, S&P) fournissent une estimation du risque, mais les spécificités pays (risque souverain) doivent être ajoutées (spread de pays / *Country Default Spread*).

---

## 5. Produits, Applications et Entreprises Cités
* **Entreprises et boursiers cités (exemples pédagogiques) :** 
    * **Vale** (compagnie minière brésilienne)
    * **Embraer** (aérospatiale brésilienne)
    * **Petrobras** (pétrole, Brésil)
    * **Apple** (technologie, USA)
    * **Tesla** (automobile, USA)
    * **Airbnb et Hyatt** (hôtellerie / location)
    * **Southwest Airlines vs Singapore Airlines** (compagnies aériennes)
    * **Walmart, Costco, Whole Foods** (grande distribution)
* **Outils et plateformes :** 
    * **Bloomberg** (terminal Bloomberg mentionné pour la récupération des bêtas et des données de régression).
    * **Capital IQ** (base de données financière mentionnée pour le screening sectoriel et l'obtention des bêtas *bottom-up*). *Note : Il s'agit d'un outil professionnel payant mentionné par l'orateur (Aswath Damodaran) dans le cadre de ses cours universitaires.*
* **Publicité :** Aucune publicité commerciale pour des produits tiers ; l'orateur utilise ses propres outils pédagogiques et bases de données gratuites ou académiques (disponibles sur son site web personnel).
