# Séance 6 : Taux sans risque et primes de risque sur actions

Vidéo : https://youtu.be/oeRtLInQTAM · durée 1:22:27 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

---

# Fiche de Connaissances : Les Limites du MEDAF (CAPM) et les Alternatives pour l'Évaluation du Risque

## 1. Sujet et Thèse Principale
*   **Sujet :** L’analyse critique du Modèle d’Évaluation des Actifs Financiers (MEDAF ou CAPM en anglais), ses limites empiriques et théoriques, ainsi que la présentation des alternatives pour mesurer le risque et le coût du capital (modèles multifactoriels, proxy models).
*   **Thèse principale :** Bien que le MEDAF soit massivement utilisé en finance par habitude et simplicité, il repose sur des hypothèses irréalistes, est difficile à estimer précisément, et fonctionne mal empiriquement. L’utilisation de taux sans risque adaptés aux devises et l’estimation correcte de la prime de risque de marché (ERP) sont des étapes cruciales mais complexes, nécessitant souvent des ajustements pour le risque pays (spreads de défaut).

---

## 2. Notions Expliquées (Définitions Simples)
*   **MEDAF (CAPM) :** Modèle qui relie le rendement attendu d’un actif à son risque systématique, mesuré par son **bêta ($\beta$)** par rapport au portefeuille de marché.
*   **Bêta ($\beta$) :** Mesure de la sensibilité du rendement d’une action par rapport aux fluctuations du marché global.
*   **Taux sans risque ($R_f$) :** Le rendement d’un actif considéré comme sans risque de défaut (souvent un emprunt d’État à long terme).
*   **Prime de Risque de Marché / Equity Risk Premium (ERP) :** Le surplus de rendement exigé par les investisseurs pour investir dans des actions risquées par rapport au taux sans risque.
*   **Modèle Multifactoriel (APM) / Arbitrage Pricing Theory :** Modèle expliquant les rendements boursiers à l'aide de plusieurs facteurs macroéconomiques et statistiques (taille, valeur, etc.) plutôt que par un seul bêta.
*   **Spread de Défaut (Default Spread) :** Différence de rendement entre une obligation souveraine risquée et une obligation souveraine sans risque (ex. : taux américain).
*   **CDS (Credit Default Swap) Souverain :** Assurance contre le risque de défaut d'un État, servant de proxy pour évaluer le risque de défaut d'un pays.
*   **Prime de Risque Implicite (Implied ERP) :** Prime de risque calculée à partir des prix actuels du marché (valeur actuelle des flux de trésorerie futurs attendus, comme les dividendes et rachats d'actions).
*   **Approche Historique de l'ERP :** Estimation de la prime de risque en se basant sur les rendements passés sur de longues périodes (ex. : depuis 1928).

---

## 3. Chiffres, Taux, Plafonds et Règles Fiscales Cités
*   **Novembre 2013 (Exemples empiriques) :**
    *   Taux des obligations du Trésor américain à 10 ans : **2,75 %** (utilisé comme taux sans risque).
    *   Inflation aux États-Unis : **3 %**.
    *   Prime de risque implicite (ERP) aux États-Unis : **5,50 %**.
    *   Taux des obligations souveraines chinoises et locales (Novembre 2013) : Taux sans risque en renminbi estimé à **4,30 %**, spread de défaut à **0,80 %** (Total ERP Chine : **6,30 %**).
    *   Inde (Novembre 2013) : Spread de défaut de **2,25 %**, ERP total de **9,10 %**.
    *   Brésil (Novembre 2013) : Spread de défaut de **2,75 %** (via obligation en dollar) ou **2,50 %** (via CDS), ERP total d'environ **8,04 % à 8,50 %**.
    *   Argentine : Historique de défauts multiples au XXIe siècle (plusieurs défauts récents cités, avec des conférences de gestionnaires en Argentine signalant le retour du risque souverain).
*   **Règles et limites légales/fiscales :** *À vérifier à la source officielle* pour toute application pratique en fiscalité ou réglementation financière internationale.

---

## 4. Conseils Concrets et Leurs Limites ou Risques
*   **Principe de correspondance des devises (Currency Matching) :** Toujours utiliser un taux sans risque libellé dans la même monnaie que les flux de trésorerie du projet ou de l'entreprise analysée. *Limite :* Difficulté d'obtenir un taux sans risque dans des pays où l'État présente un risque de défaut (nécessité d'ajuster via le *default spread*).
*   **Ajustement du risque pays :** Pour les marchés émergents ou sans entité sans risque, ajuster le taux sans risque local en soustrayant le spread de défaut souverain (ou en utilisant les CDS / notations de crédit).
*   **Éviter la moyenne de taux hétérogènes :** Ne jamais faire la moyenne simple des taux d'obligations d'États de notations différentes au sein d'une même zone monétaire (ex. zone euro en 2013 : de l'Allemagne à la Grèce) pour définir un taux sans risque unique.
*   **Prudence avec les primes historiques :** L'utilisation de primes de risque historiques souffre d'un biais passé (*backward-looking*), sensible à la période choisie (effet de survie du marché américain).
*   **Aversion au risque et âge :** L'aversion au risque des investisseurs varie selon l'âge, les conditions économiques et les chocs de marché (ex. : une baisse brutale des marchés boursiers de 25 % augmente temporairement la prime de risque exigée).

---

## 5. Produits, Applications ou Entreprises Cités
*   **Entreprises et indices boursiers :**
    *   *S&P 500* (Indice boursier américain de référence).
    *   *Moody's, S&P, Fitch* (Agences de notation financière citées pour les notations souveraines).
    *   *Apple, Pepsi, Goldman Sachs, Berkshire Hathaway* (Warren Buffett cité comme référence pour l'aversion au risque et la richesse liée aux primes de capital).
    *   *Silicon Valley Bank (SVB)* (Citée pour illustrer les risques de duration et de non-respect de l'appariement des échéances bancaires).
    *   *Yahoo Finance, Bloomberg* (Outils de données financières mentionnés pour trouver des informations sur les investisseurs et les taux).
*   **Nature des citations :** Ces entités et outils sont mentionnés à des fins purement pédagogiques et analytiques par le professeur Aswath Damodaran (NYU Stern School of Business). Il ne s'agit pas de placements publicitaires.
