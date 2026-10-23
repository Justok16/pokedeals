# Session 21: Closure on Pricing

Vidéo : https://youtu.be/z7vtmMaKObo · durée 1:18:35 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-23
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances en finances personnelles basée sur la vidéo :

### 1) Sujet et thèse principale

*   **Sujet :** L'évaluation relative des actions (par rapport à des comparables ou à l'ensemble du marché) et les méthodes pour contrôler les différences fondamentales entre entreprises (croissance, risque, rentabilité).
*   **Thèse principale :** L'évaluation relative ne se limite pas à comparer des ratios (comme le P/E ou le P/BV) au sein d'un même secteur. Pour être rigoureuse, elle doit intégrer des contrôles statistiques (régressions multiples) afin de tenir compte des différences structurelles (croissance, risque, rentabilité) entre les entreprises, sous peine d'erreurs d'appréciation majeures.

---

### 2) Notions expliquées

*   **Évaluation intrinsèque :** Estimation de la valeur d'une entreprise basée sur ses flux de trésorerie futurs actualisés (DCF), indépendamment du marché.
*   **Évaluation relative (ou *pricing*) :** Valorisation d'une entreprise par comparaison avec d'autres entreprises similaires (les comparables) ou avec l'ensemble du marché, en utilisant des multiples (P/E, P/BV, EV/EBITDA, etc.).
*   **Multiple (ex: P/E, P/BV) :** Rapport entre le prix d'une action et un indicateur financier (bénéfice par action pour le P/E, valeur comptable par action pour le P/BV).
*   **Comparables :** Entreprises partageant des caractéristiques similaires (secteur, taille, modèle économique) utilisées comme point de référence pour l'évaluation.
*   **Régression multiple :** Outil statistique permettant d'expliquer une variable dépendante (un multiple) par plusieurs variables indépendantes (croissance, risque, rentabilité, etc.) pour contrôler leurs différences.
*   **Variable muette (*dummy variable*) :** Variable statistique qui prend la valeur 0 ou 1 pour indiquer l'appartenance à une catégorie (ex: marché émergent ou développé).
*   **R-carré ($R^2$) :** Mesure statistique indiquant la part de variance d'une variable expliquée par le modèle de régression. Un $R^2$ élevé indique un bon ajustement.
*   **Statistique t (*t-statistic*) :** Mesure de la significativité statistique d'un coefficient dans une régression (supérieur à 2 indique généralement une bonne significativité).

---

### 3) Chiffres, taux, plafonds et règles fiscales

*   *Note importante : Toutes les données financières, statistiques et méthodologiques présentées dans cette section proviennent d'exemples académiques et historiques (exemples sur les marchés des années 2000, 2010 et 2023). **À vérifier à la source officielle** pour toute application en investissement réel ou analyse financière actualisée.*
*   Exemple de valorisation (Zyloft Inc.) : Valeur intrinsèque (DCF) = 10 \$/action ; Cours de l'action = 15 \$/action ; Valeur estimée par ratio P/E = 20 \$/action.
*   Exemples d'analyses sectorielles présentées :
    *   Secteur des boissons (ex: Coca-Cola, Anheuser-Busch, etc.) : analyse du P/E, de la croissance attendue et de l'écart-type.
    *   Secteur des télécoms (ex: Telebras, Telefonica, etc.) : régression de la régression P/E avec la croissance et l'indicateur de marché émergent ($R^2$ de 66,2 % et 63,1 % ajusté).
    *   Secteur bancaire européen (2010) : analyse du P/BV en fonction du rendement des capitaux propres (ROE) et de l'écart-type ($R^2$ de 79 %).
    *   Secteurs technologiques et *start-ups* (ex: Amazon, Twitter, Whole Foods, Sprouts) : utilisation de multiples de chiffre d'affaires et de variables de survie (trésorerie, croissance des revenus).

---

### 4) Conseils concrets, limites et risques

*   **Conseils :**
    *   Ne jamais faire la moyenne simple de deux valorisations divergentes (intrinsèque et relative).
    *   Ne pas se fier aveuglément à un multiple bas (un P/E faible ne signifie pas nécessairement qu'une action est bon marché si la croissance est faible ou le risque élevé).
    *   Utiliser des régressions multiples pour contrôler les différences fondamentales entre entreprises (croissance, risque, rentabilité) lorsque la comparaison directe est imparfaite.
    *   Adapter la taille de l'échantillon de comparables pour équilibrer la similarité et la robustesse statistique (idéalement 10 entreprises ou plus pour une régression).
*   **Limites et risques :**
    *   **Biais de sélection des comparables :** Les secteurs ne sont plus homogènes (ex: comparer des géants de la tech comme Microsoft ou Adobe avec de petites entreprises logicielles).
    *   **Non-linéarité :** Les relations entre multiples et fondamentaux ne suivent pas toujours une ligne droite.
    *   **Non-stationnarité :** Les coefficients des régressions changent d'une année à l'autre (ex: impact des crises comme le COVID-19).
    *   **Multicolinéarité :** Les variables indépendantes peuvent être corrélées entre elles, faussant les coefficients (ex: corrélation entre bêta, croissance et ratio de distribution).
    *   **Problème d'interception négative :** Dans certaines régressions, l'ordonnée à l'origine négative peut générer des prédictions de multiples absurdes (négatifs).

---

### 5) Produits, applications ou entreprises cités

*   **Zyloft Inc.** : Entreprise fictive utilisée comme exemple académique.
*   **Coca-Cola** : Entreprise citée dans l'exemple du secteur des boissons (comparaison de marché).
*   **Anheuser-Busch** : Entreprise citée dans le secteur des boissons.
*   **Microsoft / Adobe** : Entreprises citées pour illustrer l'hétérogénéité du secteur des logiciels.
*   **GM / Ford** : Entreprises citées pour l'analyse historique des analystes automobiles.
*   **Home Depot** : Entreprise citée pour l'analyse du secteur de la distribution spécialisée.
*   **Telebras / Indosat / Telefonica** : Entreprises de télécommunications (ADR) utilisées dans les régressions.
*   **Bayerische Hypo- und Vereinsbank / Commerzbank / Deutsche Bank / BNP Paribas / Intesa Sanpaolo / Banco Bilbao / Société Générale / Royal Bank of Scotland / Barclays / Unicredit / Bankinter / Erste Bank / Raiffeisen / HSBC / Lloyds TSB** : Banques européennes citées dans l'analyse des ratios P/BV en 2010.
*   **Google / Infospace / Genta / ConocoPhillips / Exxon Mobil / Nokia** : Entreprises utilisées dans les graphiques et régressions de marché (exemples historiques).
*   **Whole Foods / Sprouts** : Entreprises de distribution alimentaire (analyse des ratios P/S et marges nettes).
*   **Amazon / Twitter / Pandora / Groupon / Yelp / OpenTable / Zillow / TripAdvisor** : Entreprises technologiques et réseaux sociaux cités pour l'évaluation par multiples de revenus et de nombre d'utilisateurs.
*   **Tesla** : Entreprise citée pour l'analyse de l'évaluation par flux de trésorerie actualisés (DCF) et de la tarification prévisionnelle (*forward pricing*).

*Note : Tous les exemples d'entreprises proviennent du support de cours académique présenté dans la vidéo.*
