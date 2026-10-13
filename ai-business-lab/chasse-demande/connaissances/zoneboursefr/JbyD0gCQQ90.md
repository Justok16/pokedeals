# Les algorithmes de trading

Vidéo : https://youtu.be/JbyD0gCQQ90 · durée 15:40 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Sujet et thèse principale** : Présentation des différents types d’algorithmes d’exécution utilisés par les professionnels pour passer de gros ordres sur les marchés, afin de comprendre leur impact sur le prix et le fonctionnement des carnets d’ordres. La thèse est que ces algorithmes (VWAP, TWAP, POV, Target close, Steps, Momentum/Value, Hunt, Implementation shortfall) cherchent à trouver le juste milieu entre rapidité d’exécution et impact sur le marché, et qu’il est essentiel pour les particuliers de les connaître pour éviter les mythes.

2) **Notions expliquées** :
- **Slippage** : Différence entre le prix au moment de la décision d’achat/vente et le prix moyen réellement obtenu.
- **Impact de marché temporaire / permanent** : Variation du prix causée par un ordre important, qui peut revenir à la normale après coup (temporaire) ou laisser une trace durable (permanent).
- **VWAP (Volume Weighted Average Price)** : Algorithme visant à obtenir un prix moyen proche du prix moyen pondéré par les volumes historiques sur la journée.
- **TWAP (Time Weighted Average Price)** : Algorithme lissant le passage d’ordres dans le temps, en achetant/vendant la même quantité à chaque intervalle.
- **POV (Percentage of Volume) ou Participate** : Algorithme maintenant un niveau de participation constant par rapport au volume total du marché en temps réel.
- **Target close** : Algorithme visant à se rapprocher du cours de clôture en participant au fixing.
- **Steps** : Algorithme accélérant les achats/ventes dans des zones de prix intéressantes et les diminuant ailleurs.
- **Momentum / Value** : Algorithmes agissant dans le sens du marché (momentum) ou à contre-sens (value) pour profiter des retours à la moyenne.
- **Hunt** : Algorithme cherchant à se cacher en ne plaçant des ordres que lorsque le cours est proche de l’objectif.
- **Implementation shortfall** : Stratégie cherchant le juste milieu entre impact sur le marché et vitesse d’exécution pour minimiser le slippage au maximum.

3) **Chiffres, taux, plafonds et règles fiscales** :
- Exemples chiffrés hypothétiques : ordre de 200 000 titres à 25 € (5 millions d’euros), participation de 20 %, part de 5 % du volume, etc.
- *Règle fiscale/légale* : Non précisé. (À vérifier à la source officielle)

4) **Conseils concrets et leurs limites ou risques** :
- Connaître le fonctionnement des algorithmes professionnels pour comprendre les mouvements sur les carnets d’ordres et déconstruire les mythes de la manipulation.
- Limite : Les algorithmes d’exécution ne suppriment pas le risque de marché ; un ordre mal calibré peut entraîner un slippage important ou une exécution partielle.

5) **Produits, applications ou entreprises cités** :
- Credit Suisse, Morgan Stanley, Goldman Sachs, City, BNP (mentionnés comme exemples de grandes banques disposant de desks d'exécution algorithmique / AES de Credit Suisse). Il ne s'agit pas de publicité explicite pour ces services, mais d'illustrations pédagogiques.
