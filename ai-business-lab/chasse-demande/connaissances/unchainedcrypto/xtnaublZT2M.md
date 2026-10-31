# Ethereum's EIP-1559 Will Solve Some Problems But Big Ones Will Remain - Ep.250

Vidéo : https://youtu.be/xtnaublZT2M · durée 1:13:11 · résumé Gemini (gemini-3-flash-preview) du 2026-10-31
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo sous forme de fiche de connaissances, basée sur les échanges entre Laura Shin, Taylor Monahan (MyCrypto) et Tim Beiko (Fondation Ethereum).

### 1) Sujet et thèse principale
**Sujet :** L’implémentation de la proposition d’amélioration **EIP-1559** sur le réseau Ethereum.

**Thèse principale :** L'EIP-1559 est une réforme structurelle majeure du système de frais d'Ethereum. Elle vise à rendre l'expérience utilisateur (UX) plus fluide en stabilisant les frais de transaction et à transformer la politique monétaire de l'Ether (ETH) en introduisant un mécanisme de destruction de jetons (*burn*), rendant l'actif potentiellement déflationniste.

### 2) Notions expliquées
*   **EIP (Ethereum Improvement Proposal) :** Un document standard pour proposer des changements techniques au réseau Ethereum.
*   **Enchère de premier prix (First-price auction) :** Le système actuel (avant EIP-1559) où les utilisateurs misent les uns contre les autres pour passer dans le prochain bloc. Cela pousse à la surenchère et à l'inefficacité.
*   **Frais de base (Base Fee) :** Un montant minimum fixé algorithmiquement par le protocole pour qu'une transaction soit incluse dans un bloc. Ce montant est **détruit (*burned*)** et ne revient pas aux mineurs.
*   **Pourboire de priorité (Priority Fee / Tip) :** Un incitatif supplémentaire payé par l'utilisateur directement au mineur pour être priorisé au sein d'un bloc.
*   **Burn (Destruction) :** Mécanisme qui retire définitivement des ETH de la circulation, réduisant l'offre totale.
*   **MEV (Miner Extractable Value) :** Profit supplémentaire que les mineurs peuvent tirer en choisissant l'ordre des transactions dans un bloc (arbitrage, etc.).
*   **Sound Money / Ultra Sound Money :** Concept suggérant que l'ETH devient une monnaie "plus solide" que le Bitcoin car son offre pourrait diminuer avec l'usage du réseau.

### 3) Chiffres, taux et règles cités (Juin 2021)
*   **Ajustement des frais :** Le *Base Fee* peut augmenter ou diminuer de **12,5 %** maximum d'un bloc à l'autre selon la congestion.
*   **Taille des blocs :** Le système cible des blocs remplis à 50 %. La capacité maximale passe de 15 millions à **30 millions de "gas"** par bloc pour absorber les pics de demande.
*   **Émission vs Destruction :**
    *   Sous le système de l'époque (Proof of Work), environ **13 000 à 15 000 ETH** étaient créés par jour.
    *   Pour que l'ETH devienne déflationniste (en Proof of Work), les frais de base devraient être d'environ **150 gwei**.
    *   Après le passage à la Proof of Stake (le "Merge"), ce seuil tomberait à environ **15 gwei** pour devenir déflationniste.
*   **Calendrier de déploiement :** Prévu sur le réseau principal (*Mainnet*) entre **fin juillet et mi-août 2021** (déjà passé au moment de la lecture).
*   **Règles fiscales :** Aucune règle fiscale n'est mentionnée dans la vidéo. (**À vérifier à la source officielle** pour tout traitement fiscal des revenus de minage ou de staking).

### 4) Conseils concrets, limites et risques
*   **Pour l'utilisateur :**
    *   **Conseil :** Ne plus essayer de "deviner" les frais. Les portefeuilles compatibles proposeront un prix juste. Si vous fixez un "frais maximum" élevé, le protocole ne prélèvera que le strict nécessaire et vous **remboursera la différence**.
    *   **Risque :** En cas de congestion extrême (ex: vente massive de NFT), les frais peuvent encore grimper de façon exponentielle très rapidement.
*   **Pour les mineurs :**
    *   **Risque :** Une baisse de revenus (jusqu'à 50 % selon certaines estimations anciennes) puisque les frais de base sont brûlés au lieu de leur être versés.
    *   **Limite :** Le MEV (Miner Extractable Value) restera une source de profit non brûlée pour les mineurs.

### 5) Produits, applications et entreprises cités
*   **Publicités intégrées à la vidéo :**
    *   **Crypto.com :** Application pour acheter, épargner (taux jusqu'à 8,5 % sur BTC et 14 % sur stablecoins) et dépenser des cryptos (carte Visa).
    *   **Tezos :** Protocole blockchain auto-évolutif.
    *   **Conjure.Finance :** Plateforme pour créer des actifs synthétiques décentralisés.
*   **Intervenants :**
    *   **Taylor Monahan :** PDG de **MyCrypto** (portefeuille Ethereum, produit de l'intervenante).
    *   **Tim Beiko :** Représentant de la **Fondation Ethereum** (organisation à but non lucratif supervisant le protocole).
*   **Outils mentionnés :** **MetaMask** (cité comme exemple de portefeuille gérant les estimations de frais).
