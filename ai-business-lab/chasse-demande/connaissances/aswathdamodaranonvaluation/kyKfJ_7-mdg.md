# Valuation Modeling: Excel as a tool

Vidéo : https://youtu.be/kyKfJ_7-mdg · durée 49:11 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo sous forme de fiche de connaissances en finances personnelles :

---

# Fiche de connaissances : Guide d'utilisation du tableur de valorisation (Aswath Damodaran)

## 1) Sujet et thèse principale
* **Sujet :** Comment utiliser un tableur Excel de valorisation d’entreprise (modèle de flux de trésorerie actualisés / FCFF) créé par l'auteur.
* **Thèse principale :** Le tableur n'est qu'un outil simple (sans macros complexes ni boîtes noires) conçu pour évaluer une entreprise à partir de données financières fondamentales. Chaque calcul doit pouvoir être fait manuellement ; l’utilisateur doit s'approprier l'outil, l'adapter à ses besoins et conserver l'entière responsabilité de son évaluation.

---

## 2) Notions expliquées (définitions simples)
* **FCFF (Free Cash Flow to Firm / Flux de trésorerie disponible pour l'entreprise) :** Modèle de valorisation qui évalue l'ensemble de l'entreprise (capitaux propres et dette).
* **FCFE (Free Cash Flow to Equity) :** Variante du modèle qui évalue uniquement les capitaux propres.
* **R&D (Recherche & Développement) :** Dépenses converties en capital (immobilisées) dans le modèle pour refléter leur impact à long terme sur la valeur.
* **Leasing (contrats de location) :** Dépenses de location transformées en dette dans le modèle.
* **Taux sans risque (Risk-Free Rate) :** Taux d'intérêt de référence (généralement le taux des obligations d'État) selon la monnaie de valorisation.
* **Prime de risque sur actions (Equity Risk Premium) :** Prime exigée par les investisseurs pour investir en actions par rapport aux actifs sans risque.
* **Bêta :** Mesure de la volatilité ou du risque systématique d'une action par rapport au marché.
* **Coût du capital (Cost of Capital) :** Taux de rendement exigé par l'ensemble des financeurs de l'entreprise (dette et capitaux propres).
* **Marge opérationnelle (Operating Margin) :** Pourcentage du chiffre d'affaires restant après déduction des coûts d'exploitation (avant impôts et intérêts).
* **Ventes sur capital (Sales-to-Capital Ratio) :** Indicateur mesurant l'efficacité des investissements (combien de dollars de ventes sont générés par dollar de capital investi).
* **NOL (Net Operating Losses / Reports déficitaires) :** Pertes fiscales accumulées par le passé pouvant être utilisées pour réduire les impôts futurs (*à vérifier à la source officielle* selon les législations fiscales locales).

---

## 3) Chiffres, taux, plafonds et règles fiscales cités
* **Date de la version présentée :** Février 2024 (version 2024 du tableur).
* **Exemple concret mentionné (Amazon) :**
  * 10-K pour l'exercice 2023 (clôturé au 31 décembre 2023).
  * Chiffre d'affaires récent / revenus : exprimés en milliers (ex. : 574 milliards de dollars de revenus pour Amazon dans l'exemple).
  * Dépenses de R&D (Amazon, février 2024) : 85,6 milliards de dollars pour les 12 derniers mois.
  * Frais de location opérationnelle convertis en dette (Amazon) : ~295 millions de dollars.
  * Options d'achat d'actions et actions en circulation : incluses dans le calcul de la valeur par action.
* **Règles fiscales / comptables (à vérifier à la source officielle) :**
  * Traitement des baux (*leases*) : normes comptables IFRS et GAAP modifiées en 2019 pour intégrer certains contrats de location au bilan comme des dettes (*à vérifier à la source officielle*).
  * Reports déficitaires (*NOL*) : utilisables pour déduire les pertes passées des bénéfices imposables futurs (*à vérifier à la source officielle*).
  * Prime de risque sur actions (ERP) : actualisée chaque mois par l'auteur pour le S&P 500 (ex. : mise à jour au début de février 2024).

---

## 4) Conseils concrets, limites et risques
* **Conseils concrets :**
  * Rassembler les documents financiers (au moins 1 an de comptes complets, idéalement un rapport annuel ou 10-K, ou un rapport trimestriel récent) et les données de marché (taux sans risque, cours de l'action, nombre d'actions, capitalisation boursière) avant d'ouvrir le tableur.
  * Utiliser des unités cohérentes (ex. : milliers de dollars) pour éviter des erreurs de saisie sur les grands nombres.
  * Vérifier les options de calcul dans Excel : s'assurer que les calculs itératifs (*Iterative Calculations*) sont cochés (fixés par défaut à 100 itérations).
  * Ajuster les dépenses de R&D et les contrats de location (*leases*) en capitalisant ces postes pour refléter la réalité économique de l'entreprise.
  * Rester prudent sur les prévisions de croissance à long terme et s'appuyer sur les moyennes sectorielles fournies dans l'outil si nécessaire.
* **Limites et risques :**
  * Le modèle repose sur des hypothèses subjectives (croissance future, marges cibles, taux d'actualisation, taux de défaillance).
  * Une mauvaise estimation des flux de trésorerie ou des taux de réinvestissement fausse totalement la valorisation finale.
  * Les options d'achat d'actions (*stock options*) et les participations minoritaires peuvent compliquer l'évaluation si elles ne sont pas correctement retraitées.

---

## 5) Produits, applications ou entreprises cités
* **Entreprises citées à titre d'exemple pédagogique :** Amazon, Home Depot, Apple, Tesla, SoftBank, Coca-Cola.
* **Outils / Logiciels :** Microsoft Excel (et tableurs compatibles).
* **Ressources de l'auteur :** Le tableur présenté est mis à disposition gratuitement par l'auteur (Aswath Damodaran) sur son site internet universitaire (*https://pages.stern.nyu.edu/~adamodar/pc/fcffsimpleginzu.xlsx*). Il s'agit d'un outil pédagogique personnel de l'auteur, et non d'un produit commercial ou publicitaire payant.
