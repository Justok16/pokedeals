# What Makes Uniswap v4 Special - Ep. 508

Vidéo : https://youtu.be/KNK-W8JDuWg · durée 1:19:30 · résumé Gemini (gemini-3-flash-preview) du 2026-10-26
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo sous forme de fiche de connaissances en finances personnelles, axée sur l'écosystème de la finance décentralisée (DeFi).

### 1) Sujet et thèse principale
**Sujet :** L'évolution technologique et stratégique d'Uniswap, le principal protocole d'échange décentralisé (DEX) sur la blockchain Ethereum.
**Thèse principale :** Avec l'annonce de la version 4 (V4), Uniswap ne se contente plus d'être un simple protocole d'échange automatisé, mais devient une infrastructure programmable. L'introduction des « Hooks » permet une personnalisation extrême des échanges et de la gestion des liquidités, visant à capter plus de valeur pour les utilisateurs tout en réduisant les coûts de transaction.

### 2) Notions expliquées
*   **AMM (Automated Market Maker) :** Un système qui remplace le carnet d'ordres traditionnel par des algorithmes (formule $x \times y = k$) pour permettre l'échange d'actifs de manière autonome grâce à des réserves de jetons (pools).
*   **Liquidité concentrée (V3) :** Concept introduit dans Uniswap V3 permettant aux fournisseurs de liquidité de choisir des plages de prix spécifiques pour leurs fonds, augmentant ainsi l'efficacité du capital.
*   **Hooks (V4) :** Contrats intelligents externes qui s'exécutent à des moments précis d'une transaction (avant/après un échange ou un dépôt). Ils permettent d'ajouter des fonctionnalités comme des ordres limites, des oracles personnalisés ou des frais dynamiques.
*   **Singleton (V4) :** Architecture où tous les pools de liquidité sont regroupés dans un seul contrat intelligent, ce qui réduit considérablement les frais de gaz lors de transactions impliquant plusieurs pools.
*   **TWAMM (Time-Weighted Average Market Maker) :** Une fonctionnalité permettant d'exécuter de très gros ordres en les divisant en petites portions sur une longue période pour minimiser l'impact sur le prix du marché.
*   **BSL (Business Source License) :** Type de licence logicielle qui rend le code public tout en restreignant son utilisation commerciale par des tiers pendant une période donnée.

### 3) Chiffres, taux et règles cités
*   **Historique :** Lancement d'Uniswap V1 en novembre 2018.
*   **Volume :** Plus de 1 500 milliards de dollars échangés sur le protocole depuis sa création.
*   **Part de marché :** Uniswap représente environ 85 % à 90 % du volume de trading « on-chain » sur Ethereum.
*   **Frais :** Historiquement fixés à 0,3 % (V1/V2). La V3 a introduit des paliers (0,01 %, 0,05 %, 0,3 %, 1 %). La V4 permettra des frais totalement dynamiques.
*   **Règle de licence :** Uniswap V4 utilise une licence BSL de **4 ans** (contre 2 ans pour la V3) avant de passer sous licence libre GPL (**à vérifier à la source officielle**).
*   **Mise à jour technique :** La V4 dépend de l'EIP-1153 d'Ethereum (stockage transitoire) pour optimiser les coûts de gaz (**à vérifier à la source officielle**).

### 4) Conseils concrets et risques
*   **Conseils :** 
    *   Pour les utilisateurs avancés (Whales), l'utilisation des hooks comme le TWAMM permettra de réduire le « slippage » (écart de prix) sur les grosses transactions.
    *   Pour les fournisseurs de liquidité, la V4 offre la possibilité de générer des rendements supplémentaires en déposant des fonds dans des pools qui réinvestissent la liquidité inactive.
*   **Limites et risques :**
    *   **Risque de sécurité des Hooks :** Contrairement au cœur du protocole Uniswap qui est immuable, les Hooks sont des contrats externes. Un Hook mal conçu ou malveillant peut compromettre les fonds d'un pool spécifique.
    *   **Fragmentation de la liquidité :** La multiplication des types de pools personnalisés peut diviser la liquidité et rendre certains échanges moins efficaces si les utilisateurs ne sont pas bien orientés par les interfaces (front-ends).

### 5) Produits, applications ou entreprises cités
*   **Unchained / Laura Shin :** Podcast et hôte de l'émission (Produits de l'auteur).
*   **Uniswap :** Protocole de DeFi (Sujet principal).
*   **OKX Wallet :** Portefeuille Web3 (Publicité).
*   **Token 2049 Singapore :** Conférence crypto (Publicité).
*   **Crypto.com :** Plateforme d'échange et application (Publicité).
*   **Sushiswap :** Concurrent cité pour son historique de « fork » du code d'Uniswap.
*   **CrocSwap (ou Croc) :** Cité dans le cadre de discussions sur l'antériorité de certaines innovations techniques.
*   **Baslancer V2 :** Cité pour son utilisation pionnière de l'architecture « Singleton ».
