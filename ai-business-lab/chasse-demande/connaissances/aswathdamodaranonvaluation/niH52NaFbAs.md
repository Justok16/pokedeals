# Session 8 : Bêtas et au-delà !

Vidéo : https://youtu.be/niH52NaFbAs · durée 1:22:06 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré sous forme de fiche de connaissances en finances personnelles, basé sur le contenu de la vidéo :

---

# Fiche de Connaissances : Mesure du Risque et Performance des Actions (Modèle CAPM et Régression)

## 1. Sujet et Thèse Principale
* **Sujet :** L’estimation du bêta, du risque de marché, et la mesure de la performance (Jensen’s Alpha) des actions à l’aide de la régression statistique et du Modèle d’Évaluation des Actifs Financiers (CAPM).
* **Thèse principale :** L’évaluation du risque d’une action (bêta) et sa performance historique via une régression statistique dépend fortement des choix méthodologiques (période d’estimation, fréquence des données et choix de l’indice de référence). Les investisseurs doivent analyser ces données avec discernement et se méfier des approximations automatisées fournies par les services financiers.

---

## 2. Notions Expliquées (Définitions simples)
* **Bêta ($\beta$) :** Mesure de la sensibilité ou de la volatilité d’une action par rapport aux mouvements du marché (et non sa volatilité absolue). Un bêta supérieur à 1 indique une action plus risquée que le marché.
* **Taux sans risque ($R_f$) :** Le rendement d’un investissement sans risque de défaut (ex. : obligations d’État à 10 ans).
* **Prime de risque sur actions (Equity Risk Premium) :** Le rendement excédentaire exigé par les investisseurs pour investir dans des actions par rapport au taux sans risque.
* **R-carré ($R^2$) :** Pourcentage du risque (variance) d’une entreprise qui peut être attribué au marché (risque de marché vs risque spécifique à l’entreprise).
* **Jensen’s Alpha ($\alpha$) :** Mesure de la surperformance ou sous-performance d’une action par rapport au rendement attendu par le CAPM, ajustée au risque.
* **Ordinay Least Squares (OLS) :** Méthode statistique de régression linéaire « des moindres carrés » qui minimise les distances carrées pour tracer la ligne de meilleur ajustement.

---

## 3. Chiffres, Taux, Plafonds et Règles Fiscales Cités
* **Exemple Walt Disney (Novembre 2009) :**
  * Prix de l’action (fin nov. 2009) : **30,22 $**
  * Prix de l’action (fin déc. 2009) : **32,25 $**
  * Dividende versé (déc. 2009) : **0,35 $**
  * Rendement mensuel calculé de Disney : **7,88 %**
  * Indice S&P 500 (nov. 2009) : **1095,63**
  * Indice S&P 500 (déc. 2009) : **1115,10**
  * Dividendes de l’indice (déc. 2009) : **1,683**
  * Rendement mensuel calculé du S&P 500 : **1,78 %**
* **Exemple Disney (Période 2008-2013) :**
  * Bêta brut estimé : **1,25** (Erreur standard : **0,10**)
  * R-carré : **73 %**
  * Intercepte mensuel (Jensen’s Alpha) : **0,712 %** (annualisé à **9,02 %**).
* **Exemple Tata Motors (Inde) :**
  * Bêta : **1,83** (plage à 67 % de confiance : **1,67 - 1,99**)
  * R-carré : **69 %** (marché) / **31 %** (spécifique)
  * Alpha de Jensen annualisé : **35,4 %**
* **Règles et intervalles statistiques :**
  * Intervalles de confiance standards : **67 %** ($\pm 1$ erreur standard), **95 %** ($\pm 2$ erreurs standards), **99 %** ($\pm 3$ erreurs standards).
  * Erreur standard médiane des actions américaines : **0,20 à 0,25**.
  * Échelle d’ajustement du bêta de Bloomberg : $\text{Bêta ajusté} = (\text{Bêta brut} \times \frac{2}{3}) + (\frac{1}{3} \times 1)$ _(À vérifier à la source officielle)_.

---

## 4. Conseils Concrets, Limites et Risques
* **Conseils concrets :**
  * Pour estimer le bêta ou le rendement attendu d’une entreprise, privilégiez des périodes de référence cohérentes (2 à 5 ans) et des données de fréquence hebdomadaire ou mensuelle pour éviter le « bruit » des données journalières.
  * Utilisez un indice de marché large et pertinent (ex. : S&P 500 pour les actions US, CAC pour la France, DAX pour l’Allemagne) correspondant à la géographie d’exploitation des revenus de l’entreprise.
  * Payez ou remboursez vos dettes si vous gérez une entreprise afin de réduire le risque global (effet de levier de la dette).
* **Limites et risques :**
  * Les bêtas calculés par régression intègrent toujours une **erreur standard** importante ; ils ne doivent pas être pris comme des vérités absolues.
  * Les investisseurs diversifiés ne sont pas récompensés pour le risque spécifique de l’entreprise, mais uniquement pour le risque de marché.
  * Le « chasing past winners » (rechercher les gagnants passés) est une stratégie risquée et inefficace à long terme.

---

## 5. Produits, Applications ou Entreprises Cités
* **Bloomberg Terminal :** Service de données financières et de calcul de bêta mentionné (produit tiers, non affilié à l’auteur, payant et onéreux).
* **Yahoo Finance :** Source gratuite pour obtenir les prix historiques et rendements des indices (produit tiers, non publicitaire).
* **Walt Disney, Amgen, Nvidia, Tata Motors, Ford, General Motors, ExxonMobil, Baidu, Deutsche Bank :** Entreprises citées à titre d'exemples pédagogiques et d’études de cas par l’auteur (Professeur Aswath Damodaran).
