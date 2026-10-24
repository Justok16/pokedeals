# Comment PaperTrade propose-t-il un levier 1000x sans frais ?

Vidéo : https://youtu.be/DZ6FpZ4HORs · durée 13:51 · résumé Gemini (gemini-3-flash-preview) du 2026-10-24
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo sous forme de fiche de connaissances, basé sur l'entretien entre Laura Shin et Jason Pagoulatos.

### 1) Sujet et thèse principale
*   **Sujet :** Le fonctionnement et les controverses entourant **Papertrade**, un nouveau protocole de trading de cryptomonnaies à effet de levier extrême lancé sur le réseau HyperEVM.
*   **Thèse principale :** Bien que présenté comme une innovation financière « on-chain », Papertrade s'apparente davantage à un casino décentralisé basé sur le modèle historique des « bucket shops ». Son attrait (levier 1000x, absence de frais) cache des risques majeurs de manipulation de marché et des limites techniques structurelles.

### 2) Notions expliquées
*   **Papertrade :** Une plateforme de trading entièrement sur chaîne (on-chain) qui permet de parier sur les variations du Bitcoin (BTC) et de l'Ethereum (ETH).
*   **Effet de levier (Leverage) 1000x :** Technique permettant d'ouvrir une position 1000 fois supérieure au capital engagé. Jason Pagoulatos précise qu'à ce niveau, il ne s'agit plus de trading mais de jeu d'argent (gambling).
*   **Martingale LP (La Maison) :** Pool de liquidité contre lequel les utilisateurs tradent. Si le trader perd, ses fonds vont dans ce pool. Si le trader gagne, il est payé par ce pool.
*   **Bucket Shop :** Modèle de courtage (fin XIXe - début XXe siècle) où les parieurs misaient sur les prix des actions sans jamais posséder les actifs réels. Les ordres ne touchent jamais le marché réel.
*   **Token PAPER :** Jeton de « consolation » ou de « remise » (rebate). Lorsqu'un trader perd des USDC, il reçoit des jetons PAPER qu'il peut ensuite « staker » (immobiliser) pour toucher une partie des revenus générés par les futures pertes d'autres traders.
*   **Funding Rates (Taux de financement) :** Frais habituels dans le trading de produits dérivés pour maintenir le prix du contrat proche du prix du marché. Papertrade n'en utilise pas.

### 3) Chiffres, taux et règles cités
*   **Date de l'émission :** 22 octobre 2026.
*   **Date de lancement de Papertrade :** 10 octobre (année 2026 suggérée par le contexte).
*   **Effet de levier maximal :** 1000x.
*   **Volume de trading :** A dépassé ponctuellement le volume notionnel quotidien du NASDAQ.
*   **Dépôts initiaux :** Environ 140 millions de USDC déposés par la communauté avant le lancement.
*   **Distribution :** 57 millions de dollars ont déjà été versés aux détenteurs de jetons PAPER (via le staking).
*   **Règles de gains :** Le gagnant ne reçoit pas 100 % de son profit, mais environ **88 % à 90 %** (frais asymétriques).
*   **Règle fiscale/légale :** Aucune règle spécifique citée (**à vérifier à la source officielle**).

### 4) Conseils concrets, limites et risques
*   **Risque de liquidation extrême :** Avec un levier de 1000x, une variation de seulement **10 points de base (0,1 %)** du prix de l'actif suffit à liquider totalement la position du trader.
*   **Risque technique (Congestion) :** Le réseau HyperEVM peut saturer. Lors du lancement, des traders n'ont pas pu fermer leurs positions à cause d'une file d'attente (queue), entraînant des liquidations forcées avant que l'ordre ne soit traité.
*   **Risque de solvabilité :** Si le pool de liquidité (Martingale LP) est vide, les gagnants doivent attendre dans une file d'attente que de nouveaux traders perdent de l'argent pour être payés.
*   **Risque de manipulation de marché :** Papertrade utilise les prix d'Hyperliquid. Un acteur disposant de gros capitaux peut manipuler le prix sur Hyperliquid (marché réel) pour déclencher massivement des liquidations sur Papertrade et empocher les profits.

### 5) Produits, applications ou entreprises cités
*   **Papertrade :** Le protocole analysé (produit tiers).
*   **Hyperliquid / HyperEVM :** L'infrastructure technique et la source de prix (produits tiers).
*   **Delphi Digital :** Cabinet de recherche où travaille l'invité Jason Pagoulatos.
*   **Unchained :** Média de l'animatrice Laura Shin.
*   **Nexo :** **Publicité** (présentée en début et fin de vidéo). Plateforme de gestion de patrimoine numérique permettant de générer des intérêts sur ses cryptos ou d'emprunter des fonds (USDC) sans vendre ses actifs.
*   **1inch / Cape :** Sponsors apparaissant à l'écran (publicité/partenariat).
