# Why MEV Will Always Be Controversial - Ep. 482

Vidéo : https://youtu.be/2rwu2ah4Crg · durée 1:08:46 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-27
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

---

### Fiche de connaissances : La distribution du MEV (Maximal Extractable Value)

#### 1. Sujet et thèse principale
* **Sujet :** Le MEV (Maximal Extractable Value), sa distribution, son impact sur l’équité des transactions et la sécurité des blockchains (notamment Ethereum), ainsi que l'évolution des modèles (rebetting, MEV Burn, proposer-builder separation).
* **Thèse principale :** La valeur générée par l'activité économique sur les blockchains est capturée soit par les utilisateurs, soit par les validateurs/mineurs. Les intervenants débattent de la juste répartition de cette valeur (qui doit en bénéficier ?) et des solutions techniques pour limiter le « front-running » tout en favorisant un écosystème décentralisé.

---

#### 2. Notions expliquées (définitions simples)
* **MEV (Maximal Extractable Value) :** La valeur maximale que les validateurs (ou mineurs) peuvent extraire en ré ordonnant, insérant ou censurant des transactions dans un bloc (par exemple via le sandwich trading).
* **Front-running / Back-running / Sandwiching :** Techniques de trading où un acteur observe une transaction en attente pour placer un ordre juste avant (front-running) et/ou juste après (back-running), capturant de la valeur au détriment de l'utilisateur initial.
* **Rebetting (rebattage) :** Processus consistant à reverser une partie de la valeur extraite (MEV) aux utilisateurs pour compenser le coût du front-running.
* **MEV Burn :** Mécanisme de destruction (burn) de certaines survaleurs ou frais pour éviter la centralisation et aligner les incitations économiques.
* **Proposer-Builder Separation (PBS) :** Séparation au niveau du protocole entre les validateurs (proposeurs de blocs) et les builders (constructeurs de blocs), permettant de réduire la complexité et les risques pour les validateurs ordinaires.
* **EigenLayer :** Plateforme de re-staking permettant d'optimiser le staking et les services de pré-confirmation.

---

#### 3. Chiffres, taux, plafonds et règles fiscales
* **Chiffres d'attaques :** 3,8 milliards de dollars de valeur volée à des projets Web3 en 2022 *(à vérifier à la source officielle)*.
* **Pertes liées à MEV Blocker :** Les exploiteurs de MEV auraient généré 1,38 milliard de dollars de profits aux dépens des utilisateurs ordinaires *(à vérifier à la source officielle)*.
* **Frais et rendements (Crypto.com) :** Jusqu'à 12 % p.a. sur les actifs crypto, 8,5 % p.a. sur le BTC, et jusqu'à 14 % p.a. sur les stablecoins ; cashback jusqu'à 5 % et rabais de 100 % sur Netflix et Spotify *(à vérifier à la source officielle)*.
* **Bonus promotionnel :** 25 $ offerts avec le code « laura » sur Crypto.com *(à vérifier à la source officielle)*.

---

#### 4. Conseils concrets, limites et risques
* **Conseils :** Utiliser des outils ou des portefeuilles intégrant des protections contre le front-running (ex. MEV Blocker, agrégateurs de transactions) pour éviter de subir des prix sous-optimaux.
* **Limites / Risques :** 
  * Le rebetting reste inefficace par définition car il nécessite une action supplémentaire sur la chaîne.
  * La centralisation des validateurs ou des constructeurs de blocs (builders) pose des risques de censure et de manipulation du réseau.
  * Les solutions de chiffrement (threshold encryption, SGX) alourdissent la latence des transactions.

---

#### 5. Produits, applications et entreprises cités
* **Crypto.com :** Application d'achat, de vente et d'épargne crypto (mentionné comme sponsor / publicité de l'hôte).
* **Halborn :** Société de sécurité blockchain proposant des audits et des tests de pénétration (mentionné comme sponsor / publicité de l'hôte).
* **Protocoles / Plateformes MEV :** Flashbots (MEV-share), bloXroute (BackrunME), Blocknative (Wallet Boost), OpenMEV (Manifold), CowSwap, Matcha, 1inch, Uniswap, EigenLayer, Rocket Pool.
