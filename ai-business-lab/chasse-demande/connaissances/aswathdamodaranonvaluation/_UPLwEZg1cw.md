# Session 20: Following up on optimizing debt mix

Vidéo : https://youtu.be/_UPLwEZg1cw · durée 1:34:01 · résumé Gemini (gemini-3-flash-preview) du 2026-10-22
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances synthétisant les concepts financiers présentés dans cette leçon d'Aswath Damodaran.

---

### 1) Sujet et thèse principale
**Sujet :** L’optimisation de la structure du capital via l’approche de la **Valeur Actuelle Ajustée (APV - Adjusted Present Value)** et les mécanismes pour atteindre cet optimal.

**Thèse principale :** La valeur d'une entreprise endettée est égale à sa valeur sans dette, plus les avantages fiscaux de la dette, moins les coûts attendus de faillite. L'objectif de la finance d'entreprise est de trouver le ratio d'endettement qui maximise cette valeur totale tout en alignant la nature de la dette sur celle des actifs.

---

### 2) Notions expliquées
*   **Valeur sans dette (Unlevered Firm Value) :** La valeur qu'aurait une entreprise si elle était financée à 100 % par des fonds propres (actions).
*   **Bouclier fiscal (Tax Benefits) :** Économie d'impôt réalisée car les intérêts de la dette sont déductibles du résultat imposable.
*   **Coûts de faillite (Bankruptcy Costs) :** 
    *   *Directs :* Frais juridiques et administratifs liés à la liquidation ou restructuration.
    *   *Indirects :* Perte de clients, de fournisseurs (exigeant du cash) et d'employés clés suite à la perception d'un risque d'insolvabilité.
*   **Notation synthétique (Synthetic Rating) :** Estimation de la note de crédit d'une entreprise basée sur ses ratios financiers (ex: ratio de couverture des intérêts).
*   **Sous-levier / Sur-levier (Under/Over-levered) :** Situation où une entreprise a respectivement trop peu ou trop de dettes par rapport à son point optimal de maximisation de la valeur.
*   **Dette pour fonds propres (Debt-for-equity swap) :** Échange de titres de créance contre des actions, utilisé pour modifier rapidement la structure du capital.

---

### 3) Chiffres, taux et règles fiscales
*   **Coûts directs de faillite :** Estimés entre **5 % et 10 %** de la valeur de l'entreprise selon les études empiriques (*à vérifier à la source officielle*).
*   **Coûts indirects de faillite :** Varient selon le secteur ; environ **5 %** pour une épicerie contre **40 %** pour une entreprise technologique ou aéronautique comme Boeing (*à vérifier à la source officielle*).
*   **Probabilités de défaut (Étude Altman sur 10 ans) :**
    *   Note AAA : **0,07 %**
    *   Note A- : **0,66 %**
    *   Note BB : **16,63 %**
    *   Note CCC : **59,01 %**
*   **Règle fiscale citée :** Avantage fiscal = Montant de la dette × Taux d'imposition (simplification pour une dette perpétuelle) (*à vérifier à la source officielle*).
*   **Exemple Disney (Données 2013/2014) :** Taux d'imposition de **36,1 %** ; ratio d'endettement optimal calculé à **40 %**.

---

### 4) Conseils concrets, limites et risques
*   **Conseil : Aligner la maturité.** Faire correspondre la durée de la dette à la durée de vie des actifs (ex: dette à 100 ans pour des projets de très long terme).
    *   *Risque :* Une dette trop courte crée un risque de refinancement ; une dette trop longue peut devenir inadaptée si l'entreprise change de métier.
*   **Conseil : Choisir le type de taux.** Utiliser de la dette à taux variable si l'entreprise a un fort pouvoir de fixation des prix (*pricing power*) lui permettant de répercuter l'inflation sur ses clients.
    *   *Limite :* Très risqué pour les secteurs à faibles marges et prix fixes (ex: transport aérien).
*   **Conseil : Utiliser la dette convertible.** Recommandé pour les entreprises en croissance pour maintenir des paiements d'intérêts bas au début.
    *   *Risque :* Dilution future des actionnaires si les obligations sont converties en actions.
*   **Conseil : Agir vite en cas de menace.** Si une entreprise est sous-endettée et risque une OPA hostile, elle doit augmenter son levier rapidement (rachats d'actions).
    *   *Risque :* Précipitation pouvant mener à un surendettement si les prévisions de flux de trésorerie sont trop optimistes.

---

### 5) Produits, applications ou entreprises cités
*   **Entreprises citées (exemples pédagogiques) :** Disney, Boeing, Tata Motors, Vale, Baidu, Microsoft, Apple, Siemens, Deutsche Telekom, Lehman Brothers.
*   **Produits/Outils :** 
    *   Étude Altman (modèle de probabilité de faillite).
    *   Terminaux **Bloomberg** et **S&P Capital IQ** (mentionnés comme sources de données pour extraire les ratios d'endettement).
*   **Logiciel :** Microsoft Excel (évoqué pour les feuilles de calcul de régression).
*   *Note : L'auteur ne fait pas de publicité, il utilise ces entreprises comme cas pratiques pour illustrer ses modèles théoriques.*

---
**Détails non précisés :** L'année exacte des données fiscales pour chaque pays (hors exemples datés de 2013-2014) et les formules mathématiques exactes des régressions statistiques utilisées dans les logiciels.
