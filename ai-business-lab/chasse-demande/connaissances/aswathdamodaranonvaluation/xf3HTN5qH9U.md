# Session 2A : Données d'évaluation - Taux d'actualisation

Vidéo : https://youtu.be/xf3HTN5qH9U · durée 1:50:04 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-31
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici la fiche de connaissances de la vidéo.

---

# Fiche de connaissances – Évaluation d’entreprise et choix financiers

---

### 1. Sujet et thèse principale

*   **Sujet :** L’évaluation financière des entreprises, avec un focus sur les méthodes d’actualisation (flux de trésorerie actualisés ou DCF), le traitement des données comptables, l’utilisation des bêtas et le choix de la devise et du taux sans risque.
*   **Thèse principale :** Les chiffres comptables et les estimations automatiques (fournis par les bases de données ou les analystes) comportent de nombreux biais ; pour obtenir une valorisation réaliste, il faut retraiter les postes clés (comme les baux et la R&D), privilégier les bêtas sectoriels (« bottom-up betas ») et maintenir une cohérence stricte entre la devise, l’inflation, le taux sans risque et la croissance.

---

### 2. Notions expliquées

*   **DCF (Discounted Cash Flow) :** Méthode d'évaluation d'une entreprise basée sur l'actualisation des flux de trésorerie futurs.
*   **Coût du capital :** Le rendement minimum exigé par les apporteurs de capitaux (dettes et capitaux propres).
*   **Taux sans risque :** Le rendement d'un actif considéré comme sans risque de défaut (généralement un emprunt d'État), utilisé comme base de calcul du coût des capitaux propres.
*   **Bêta :** Mesure de la sensibilité (ou de la volatilité) d'une action par rapport aux fluctuations du marché.
    *   **Bêta désendetté (unlevered beta) :** Mesure le risque lié uniquement à l'activité opérationnelle de l'entreprise, abstraction faite de sa structure financière.
    *   **Bêta endetté (levered beta) :** Prend en compte l'effet de levier de la dette.
*   **Capitalisation de la R&D et des baux (Operating Leases) :** Pratique consistant à retraiter ces dépenses pour les traiter comme des investissements (actifs) et des dettes, plutôt que comme de simples charges d'exploitation de la période.
*   **Différentiel d'inflation :** Méthode d'estimation d'un taux sans risque dans une devise sans obligation gouvernementale fiable en ajustant le taux d'une autre devise (comme le dollar) par l'écart d'inflation attendue.

---

### 3. Chiffres, taux, plafonds et règles cités

*   **Amgen (valeur et données 2007) :**
    *   Taux de la dette / coût de la dette (rating A) : **5,63 %**.
    *   Valeur actuelle des engagements de location (Operating Leases) : **869,55 millions de dollars** (base 2007).
    *   Bêta désendetté des firmes pharmaceutiques : **1,59**.
    *   Bêta endetté (calculé) : **1,73**.
*   **Arcelik (octobre 2019) :**
    *   Cours de l'action à la date du 14 octobre 2019 : **14 livres turques**.
    *   Taux des obligations gouvernementales turques (14 octobre 2019) : **15,12 %**.
    *   Notation de la Turquie (octobre 2019) : **Ba3**, avec un spread de défaut de **4,06 %**.
    *   Taux sans risque estimé en livre turque : **11,06 %**.
*   **Taux sans risque (janvier 2022) :**
    *   Obligation gouvernementale indienne (1er janvier 2022) : **6,45 %** (Rating Baa3, spread de défaut **1,87 %**, taux sans risque en roupies = **4,58 %**).
*   **Exemples d'inflation et de taux (Égypte / USA) :**
    *   Taux sans risque en USD (31 décembre 2015) : **2,27 %**.
    *   Inflation attendue aux USA (2015) : **1,50 %**.
    *   Inflation attendue en Égypte (2015) : **9,70 %**.
    *   Taux sans risque estimé en livres égyptiennes : **10,53 %**.
*   **Règles fiscales ou légales :** *Non précisé (les normes comptables IFRS/GAAP imposent désormais la capitalisation des baux au bilan, mais l'orateur discute de la logique financière sous-jacente).* **À vérifier à la source officielle** pour toute application normative ou fiscale spécifique.

---

### 4. Conseils concrets, limites et risques

*   **Conseils :**
    *   Mettre à jour les données financières avec les chiffres les plus récents possibles (données des 12 derniers mois ou moyennes sur 5 ans selon les postes).
    *   Capitaliser les baux et la R&D pour corriger les distorsions comptables et refléter la véritable structure de risque et de capital.
    *   Utiliser les bêtas « bottom-up » (moyenne sectorielle désendettée réajustée par la structure financière de l'entreprise cible) plutôt que les bêtas de régression historiques, qui sont trop instables (« bruyants »).
    *   Maintenir la cohérence des devises : si l'on évalue en roupies ou en livres turques, intégrer l'inflation locale et ajuster le taux sans risque en conséquence (ou faire ses calculs en USD et appliquer un taux de change cohérent).
*   **Limites et risques :**
    *   Le recours aux bêtas de régression (issus de Bloomberg ou d'autres terminaux) peut conduire à des erreurs d'évaluation importantes en raison d'un $R^2$ faible et d'une forte variabilité propre à l'entreprise.
    *   Le mélange des devises (ex. : emprunter ou évaluer dans une devise instable avec des hypothèses de croissance d'une autre devise) fausse totalement le coût du capital et la valorisation finale.

---

### 5. Produits, applications ou entreprises citées

*   **Entreprises citées (exemples d'analyse) :** Arcelik, Amgen, Tata Motors, Coca-Cola, Netflix, Nokia, Heineken, Apple, General Electric, Walmart, Goldman Sachs, Moody's, S&P.
*   **Outils et bases de données :** Terminaux Bloomberg (mentionnés pour l'extraction des bêtas et régressions historiques).
*   **Nature des citations :** Exemples pédagogiques et analyses de cas présentés par l'auteur (Aswath Damodaran). **Ce ne sont pas des placements publicitaires.**
