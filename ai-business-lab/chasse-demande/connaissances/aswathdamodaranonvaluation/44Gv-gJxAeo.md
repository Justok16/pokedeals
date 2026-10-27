# Session 4: Risk and Risk free Rates

Vidéo : https://youtu.be/44Gv-gJxAeo · durée 1:22:44 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-26
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

---

# Fiche de Connaissances : Les Taux Sans Risque en Évaluation Financière

---

## 1. Sujet et Thèse Principale

*   **Sujet :** La détermination et l'utilisation du **taux sans risque** (*Risk-Free Rate*) dans les modèles d'évaluation d'entreprises (comme le MEDAF / CAPM), ainsi que la gestion des devises et de l'inflation dans l'évaluation.
*   **Thèse principale :** Le taux sans risque n'est pas un chiffre universel ou dicté par les banques centrales. Il varie selon l'horizon temporel, la devise et le risque souverain. De plus, il doit être cohérent avec les flux de trésorerie (nominaux ou réels) et ne doit pas être « normalisé » artificiellement selon les humeurs du marché.

---

## 2. Notions Expliquées (Définitions Simples)

*   **Taux sans risque (*Risk-Free Rate*) :** Le rendement théorique d'un investissement ne comportant aucun risque de défaut ni de réinvestissement sur la période. En pratique, on utilise souvent les obligations d'État à long terme (ex. : bons du Trésor à 10 ans).
*   **Prime de risque d'actions (*Equity Risk Premium*) :** Le rendement supplémentaire exigé par les investisseurs pour investir dans des actions risquées plutôt que dans des actifs sans risque.
*   **Spread de défaut souverain (*Sovereign Default Spread*) :** Le risque de défaut d'un État, souvent mesuré par la différence de taux entre ses obligations émises en monnaie locale (ou en USD) et les obligations souveraines des pays développés (ex. : États-Unis).
*   **Évaluation en termes nominaux vs réels :**
    *   *Nominal* : Intègre l'inflation attendue dans les flux de trésorerie et le taux d'actualisation.
    *   *Réel* : Ignore l'inflation (utilisation de titres indexés sur l'inflation comme les TIPS).
*   **Modèle d'évaluation des actifs financiers (MEDAF / CAPM) :** Modèle qui calcule le coût des capitaux propres en combinant le taux sans risque, le bêta (sensibilité au marché) et la prime de risque du marché.

---

## 3. Chiffres, Taux, Plafonds et Règles Fiscales Cités

*(Tous les chiffres datent du **1er janvier 2023** sauf indication contraire)*

*   **Exemple Brésil (1er janvier 2023) :**
    *   Taux des obligations souveraines brésiliennes en reais (10 ans) : **12,76 %**.
    *   Taux sans risque en USD : **2,5 %** (dans l'exemple d'introduction) / Taux des bons du Trésor US (10 ans) : **3,88 %**.
    *   Spread de défaut par défaut de l'État brésilien (notation Baa3) : **2,69 %**.
    *   Spread de défaut souverain (CDS) pour le Brésil : **3,52 %**.
    *   Spread basé sur la notation Ba2 : **2,56 %**.
*   **États-Unis (1er janvier 2023) :**
    *   Taux du bon du Trésor à 3 mois : **4,42 %**.
    *   Taux du bon du Trésor à 10 ans : **3,88 %** (en janvier 2022 : **1,51 %**, qualifié de « historiquement bas »).
    *   Taux du bon du Trésor à 30 ans : **3,97 %**.
    *   Taux des TIPS (titres indexés sur l'inflation) : **1,53 %**.
*   **Règle empirique de l'inflation :**
    *   Formule d'ajustement du taux sans risque en devise étrangère :  
        $$\text{Taux sans risque}_{\text{devise}} = \frac{(1 + \text{Taux sans risque}_{\text{base}}) \times (1 + \text{Inflation}_{\text{devise}})}{1 + \text{Inflation}_{\text{base}}} - 1$$
    *   Exemple : Taux US = 2 %, inflation US = 1,5 %, inflation égyptienne = 15 % $\rightarrow$ Taux sans risque en livres égyptiennes = **15,57 %**.
*   *Note juridique / fiscale : Aucune règle fiscale stricte ou loi n'est citée dans cette vidéo académique de finance d'entreprise (cours de l'auteur Aswath Damodaran). **À vérifier à la source officielle** (normes comptables IFRS/GAAP ou manuels de valorisation financière).*

---

## 4. Conseils Concrets, Limites et Risques

*   **Conseil 1 (Horizon temporel) :** Faites correspondre la maturité du taux sans risque à la durée de vos flux de trésorerie (privilégiez le 10 ans pour le long terme, évitez les taux à 3 mois pour des flux perpétuels).
*   **Conseil 2 (Ne pas "normaliser" les taux) :** N'essayez pas de corriger un taux sans risque jugé "trop bas" ou "trop haut" par rapport à l'historique. Utilisez le taux réel du marché au moment de l'évaluation ; ajustez plutôt vos hypothèses de croissance si nécessaire.
*   **Conseil 3 (Attention au double comptage du risque) :** Ne déduisez pas deux fois le risque de défaut d'un pays en combinant un taux local élevé et une prime de risque pays redondante.
*   **Conseil 4 (Cohérence monétaire) :** Si vous évaluez une entreprise dans une devise, utilisez le taux sans risque de cette devise (ou ajustez via le différentiel d'inflation).
*   **Limites et Risques :**
    *   L'utilisation de taux sans risque négatifs (observés par le passé en Suisse, au Japon ou dans la zone euro) perturbe les modèles traditionnels si elle n'est pas cohérente avec les prévisions d'inflation et de croissance à long terme.
    *   Le marché des CDS souverains comporte du bruit et des risques de contrepartie (ex. : faillite de Lehman Brothers en 2008).

---

## 5. Produits, Applications ou Entreprises Cités

*   **Entreprises / Entités citées à titre d'exemples pédagogiques :**
    *   *Tesla* (exercice de valorisation sur tableur Excel).
    *   *Siemens* (entreprise européenne en euros).
    *   *Gazprom* (entreprise russe).
    *   *Lehman Brothers* (exemple de faillite et de risque de contrepartie sur les CDS).
*   **Outils cités :**
    *   **Microsoft Excel** (pour les calculs de flux de trésorerie actualisés et les feuilles de données).
    *   **Bloomberg Terminal** (pour obtenir les courbes de rendement et les taux sans coupon des obligations d'État).
    *   **Yahoo Finance** (mentionné comme source potentielle de données financières).
*   **Agences de notation citées :** **Moody's** et **S&P** (utilisées pour les notations souveraines et l'estimation des spreads de défaut).
*   *Note publicitaire : Aucun produit commercial, logiciel payant tiers ou service personnel de l'auteur n'est promu. Il s'agit d'un cours universitaire (matériel pédagogique gratuit d'Aswath Damodaran, professeur à la Stern School of Business de l'Université de New York).*
