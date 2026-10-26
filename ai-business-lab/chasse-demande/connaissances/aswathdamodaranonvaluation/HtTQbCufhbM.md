# Session 8: Betas and beyond!

Vidéo : https://youtu.be/HtTQbCufhbM · durée 1:23:04 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-26
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances en finances personnelles basée sur la vidéo de cours universitaire (animée par Aswath Damodaran) :

---

# Fiche de connaissances : Évaluation et analyse du Bêta et du Coût des capitaux propres

## 1. Sujet et thèse principale
* **Sujet :** L'estimation empirique du **Bêta** (mesure du risque systématique), l'analyse des régressions (Bêta, Intercept / Jensen's Alpha, $R^2$) et le calcul du **coût des capitaux propres** (taux de rendement exigé) à partir du modèle CAPM (Modèle d'Évaluation des Actifs Financiers).
* **Thèse principale :** Les régressions historiques (comme celles fournies par les services financiers) sont utiles pour obtenir une base de travail, mais elles sont rétrospectives, « bruyantes » et comportent des erreurs d'estimation. L'utilisation mécanique de ces chiffres sans compréhension fondamentale des risques de l'entreprise ou de la diversification de l'investisseur conduit à des décisions erronées.

---

## 2. Notions expliquées (définitions simples)
* **Bêta ($\beta$) :** Mesure de la sensibilité ou du risque systématique d'une action par rapport aux mouvements du marché global. Un Bêta supérieur à 1 indique une action plus risquée (plus volatile) que le marché ; inférieur à 1, moins risquée.
* **Intercept (Jensen's Alpha) :** Mesure de la surperformance ou de la sous-performance d'une action par rapport au rendement attendu par le CAPM, après ajustement pour le risque et le rendement du marché, sur la période de régression passée.
* **$R^2$ (Coefficient de détermination) :** Le pourcentage de la variance du rendement d'une action qui est expliqué par les mouvements du marché global (macroéconomiques). Le reste ($1 - R^2$) correspond au risque spécifique de l'entreprise (diversifiable).
* **Erreur standard (Standard Error) :** L'incertitude statistique rattachée à l'estimation d'un paramètre (comme le Bêta).
* **Coût des capitaux propres (Expected Return / Hurdle Rate) :** Le taux de rendement minimum exigé par les actionnaires pour investir dans une entreprise, servant de taux d'actualisation ou de seuil de rentabilité pour les projets internes.
* **Risque de marché vs Risque spécifique :** Le risque de marché (systémique) ne peut pas être éliminé par la diversification et est seul récompensé par un rendement plus élevé ; le risque spécifique est propre à l'entreprise et peut être diversifié.

---

## 3. Chiffres, taux, plafonds et règles fiscales cités
*(Note : Les exemples datent de la période 2009–2013 et ne constituent pas des règles fiscales ou légales sujettes à des plafonds fiscaux).*
* **Exemple Walt Disney (décembre 2009 / novembre 2013) :**
  * Période de régression : 5 ans (données mensuelles).
  * Indice de marché de référence : S&P 500.
  * Bêta brut (Raw Beta) : 1,25 (ou 1,247 selon Bloomberg).
  * $R^2$ : 73 % (73 % du risque provient de sources macroéconomiques, 27 % de sources spécifiques à Disney).
  * Taux sans risque (U.S. T-Bond, nov. 2013) : 2,75 %.
  * Prime de risque sur actions (ERP) : 5,76 %.
  * Rendement attendu / Coût des capitaux propres calculé : $2,75\% + 1,25 \times 5,76\% = 9,95\%$.
* **Exemple Tata Motors (Inde) :**
  * Bêta : 1,83 (intervalle de confiance à 67 % : 1,67 – 1,99).
  * $R^2$ : 69 %.
* **Statistiques globales pour les actions US :**
  * Erreur standard médiane des Bêtas : entre 0,20 et 0,25.
  * Évolution du $R^2$ moyen des entreprises US : historiquement de 20 à 25 %, passé à 45–50 % depuis 2008 (globalisation accrue des risques).
* **Règles fiscales ou légales :** *Non précisé dans la vidéo (ce cours relève de la finance d'entreprise et de l'évaluation financière).*

---

## 4. Conseils concrets, limites et risques
* **Pour les investisseurs diversifiés :** Le risque spécifique (firm-specific risk) est éliminé par la diversification d'un portefeuille. Seul le risque de marché (capté par le Bêta) importe et est récompensé. Un investisseur diversifié ne doit pas se laisser influencer par un faible ou un haut $R^2$ s'il détient déjà un portefeuille diversifié.
* **Pour les investisseurs non diversifiés :** Ils s'exposent à l'intégralité du risque de l'entreprise (spécifique + marché). Acheter des actions de sociétés très volatiles ou concentrées sans diversification expose à des pertes importantes.
* **Piège du Bêta historique (rétrospectif) :** Le Bêta d'une régression est « bruyant » et regarde uniquement dans le passé. Il ne garantit pas la performance future.
* **Attention au « Momentum Chasing » :** Acheter des actions qui ont fortement monté dans le passé (chasser les performances récentes) en espérant de superbes rendements futurs est souvent une mauvaise stratégie en investissement.

---

## 5. Produits, applications ou entreprises cités
* **Bloomberg (Terminal) :** Application/logiciel professionnel utilisé pour collecter des données boursières et exécuter des régressions de Bêta. L'auteur explique comment il utilise l'outil tout en critiquant sa méthode de calcul « standardisée » (ajustement du Bêta vers 1 via la formule $2/3 \text{ Raw Beta} + 1/3 \times 1$). *(Mentionné comme un outil de travail professionnel, non comme de la publicité pour l'auteur).*
* **Yahoo Finance :** Source de données boursières gratuite mentionnée pour récupérer les prix historiques.
* **Entreprises et marques citées à titre d'exemples académiques :** Walt Disney, Amgen, ExxonMobil, Tesla, Bed Bath & Beyond, Tata Motors, Vale, Deutsche Bank, Baidu, Bulgari, Qwest Communications, Microsoft, GE, Philip Morris, Harmony Gold Mining, General Motors, Jaguar Land Rover, AT&T, Adobe. *(Utilisées uniquement pour illustrer les concepts théoriques de la finance).*
