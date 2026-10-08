# J'ai recodé la stratégie de ce fonds, et c'est béton

Vidéo : https://youtu.be/zcPrD1RJE6k · durée 15:15 · résumé Gemini (gemini-flash-lite-latest, lot de 4) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Sujet et thèse principale :**
   - **Sujet :** Stratégie de « cash & carry » sur les cryptomonnaies (Bitcoin et Ethereum) présentée par Étienne Mansot (responsable de la recherche et du développement chez Zonebourse) dans le cadre de la liste "Big Data" et tirée de son livre *Superformer*.
   - **Thèse principale :** Il est possible d'obtenir un rendement supérieur au taux sans risque (voire un rendement attractif et décorrélé des fluctuations directionnelles du marché) en mettant en place une stratégie d'arbitrage de type *cash & carry* sur les contrats à terme (futures) de cryptomonnaies (Bitcoin, Ethereum), en profitant de la structure de prix en *contango* ou *backwardation*.

2) **Notions expliquées :**
   - **Cash & Carry :** Stratégie d'arbitrage consistant à acheter un actif au comptant (spot) tout en vendant simultanément un contrat à terme (future) sur le même actif pour une échéance ultérieure, afin de figer un écart de prix (rendement) sans s'exposer au risque de variation de l'actif (Delta neutre).
   - **Spot :** Marché au comptant (achat ou vente immédiate de l'actif).
   - **Contrat à terme (Future) :** Contrat financier standardisé engageant à acheter ou vendre un actif à un prix fixé aujourd'hui pour une date future déterminée.
   - **Contango :** Situation où le prix du contrat à terme (future) est supérieur au prix au comptant (spot).
   - **Backwardation :** Situation inverse du contango, où le prix du futur est inférieur au prix spot.
   - **Taux sans risque :** Rendement d'un placement garanti ou sans risque de défaut (ex. bons du Trésor américain).
   - **Delta neutre :** Position sur un portefeuille dont la valeur globale est insensible aux variations de prix de l'actif sous-jacent (couverture parfaite contre la baisse ou la hausse).
   - **Rolling contract (Contrat reconductible) :** Contrat à terme reconduit automatiquement à chaque échéance pour maintenir une position continue sans intervention manuelle.

3) **Chiffres, taux, plafonds et règles fiscales :**
   - **Date du livre / support :** Livre *Superformer* (chapitre 11).
   - **Données de test (Backtest) :** Période d'étude de 730 jours (du 2 janvier 2024 au 26 janvier 2026).
   - **Actifs testés :** Bitcoin (BTC) et Ethereum (ETH).
   - **Résultat du backtest (Ethereum / ETH) :**
     - Rendement total (Total Return) sur la période : ~19,07% (entre janvier 2024 et janvier 2026).
     - Volatilité annualisée : ~3,32%.
     - Taux de croissance annuel composé (CAGR / CAGR_like) : ~9,52%.
     - Rendement annualisé moyen observé sur certains contrats (ex. du 2 janvier au 26 janvier) : ~15,7% (avec un rendement brut de période de 0,97% pour un écart de 30,1 dollars).
   - **Capital immobilisé (exemple ETH) :** ~3081,45 $ (prix spot + marge requise).
   - **Règle fiscale/légale :** À vérifier à la source officielle pour toute imposition sur les plus-values de cryptomonnaies ou de produits dérivés (futures).

4) **Conseils concrets et leurs limites ou risques :**
   - **Conseil :** Utiliser les contrats à terme sur plateformes régulées ou reconnues (comme le CME pour le Bitcoin et l'Ethereum) pour appliquer la stratégie *cash & carry* lorsque le contango offre un rendement supérieur au taux sans risque.
   - **Limites et Risques :**
     - *Risque d'exécution :* Décalage entre les cours spot et futures (basis risk), notamment en cas de forte volatilité ou de divergence des prix.
     - *Risque de marge :* Nécessité de bloquer du capital pour couvrir la marge exigée par le courtier (frais de levier / appel de marge).
     - *Fermeture anticipée :* Risque de sortie de position si la base (écart entre spot et futur) se réduit de manière inattendue ou si le coût de financement augmente.
     - *Risque calendaire :* Décalage des fuseaux horaires ou des fermetures de marchés (le spot est ouvert 24h/24, 7j/7, tandis que certains futures ont des horaires ou des jours de clôture spécifiques, ce qui peut fausser le backtest intraday).

5) **Produits, applications ou entreprises cités :**
   - Zonebourse / Service "Big Data" (Étienne Mansot) [Support du podcast / livre]
   - Livre : *Superformer* (Édition / Auteur : Étienne Mansot)
   - Spiko (Produits : Spiko Cash & Carry, Spiko Euro, Spiko Dollar, Spiko Pound) [Mentionné comme exemple de mise en place de la stratégie]
   - CME (Chicago Mercantile Exchange) [Marché de contrats à terme régulés]
   - Binance, Yahoo Finance [Sources de données]
   - *Publicité / produits de l'auteur :* Le livre *Superformer* et les services de Zonebourse sont mentionnés et présentés par l'auteur lui-même (autopromotion/produit de l'auteur).
