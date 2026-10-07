# Session 8 (of 42): Market Efficient II - Testing market-beating schemes and strategies

Vidéo : https://youtu.be/91yKnqGSb48 · durée 24:19 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Sujet et thèse principale** : La mise à l’épreuve de l’efficience des marchés et l’évaluation des stratégies d’investissement dites « de battage du marché ». La thèse est qu’il est extrêmement difficile de prouver de manière définitive qu’une stratégie bat le marché, car tout test d'efficience est un test conjoint de la stratégie et du modèle de risque utilisé.

2) **Notions expliquées** :
- **Efficience du marché** : Capacité des marchés à intégrer rapidement et correctement l'information disponible dans les prix.
- **Test conjoint** : Fait qu'un test de performance évalue simultanément la validité de la stratégie testée et la justesse du modèle de calcul des rendements attendus (comme le MEDF).
- **Ratio de Sharpe** : Mesure du rendement excédentaire par rapport à l'écart-type (volatilité) de la stratégie.
- **Ratio d'information** : Mesure du rendement excédentaire par rapport à l'erreur de suivi (tracking error) par rapport à un indice.
- **Alpha de Jensen** : Mesure de la performance ajustée au risque basée sur le modèle CAPM (rendement réel moins rendement attendu).
- **Indice de Treynor** : Rendement ajusté par le risque systématique (bêta).
- **Étude d'événement (Event Study)** : Analyse de l'impact d'un événement spécifique (ex. taux de la Fed, résultats) sur les cours boursiers.

3) **Chiffres, taux, plafonds et règles fiscales** :
- **Période de l’étude sur les options et les rendements** : 1983–2018 (mentionnée dans les graphiques et exemples historiques).
- **Exemple de rendement au jour J-10** : Rendement excédentaire moyen de 0,17 % sur les actions testées (statistiquement non significatif avec un t-stat de 1,30).
- **Règles fiscales/légales** : Les modèles de valorisation et les exigences de déclaration reposent sur les normes comptables et financières standard des régulateurs boursiers (*à vérifier à la source officielle*).

4) **Conseils concrets, limites et risques** :
- **Conseil** : Être extrêmement rigoureux lors de la conception d'une stratégie de test (éviter le forage de données ou "data mining", utiliser des périodes de test distinctes et des échantillons neutres).
- **Limites et risques** :
  - Les biais d'échantillonnage, le biais de survie (ignorer les entreprises en faillite) et les coûts de transaction non comptabilisés peuvent fausser les résultats apparents d’une stratégie.
  - La corrélation statistique n'équivaut pas à la causalité : trouver une relation passée ne garantit pas la réussite future d'une stratégie.

5) **Produits, applications ou entreprises cités** :
- Indice de référence mentionné : S&P 500. (Aucune application commerciale ou produit vendu par l'orateur).

---
