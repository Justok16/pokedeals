# Why the Celestia Team Sees a Future With 10,000 Roll-Ups - Ep. 610

Vidéo : https://youtu.be/kjSGqVbX4t8 · durée 1:09:32 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-23
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré comme une fiche de connaissances en finances personnelles :

### 1. Sujet et thèse principale
* **Sujet :** L’approche modulaire des blockchains, illustrée par le projet Celestia et le développement des roll-ups (L2) et de la scalabilité de la couche de base.
* **Thèse principale :** Pour dépasser les limites des blockchains monolithiques traditionnelles (lenteur, coûts élevés, centralisation), l'avenir réside dans la séparation des fonctions de consensus, de disponibilité des données et d'exécution. Les blockchains modulaires (comme Celestia) permettent de publier et rendre disponibles les données de manière ultra-évolutive et bon marché, permettant aux développeurs de lancer des roll-ups et des chaînes personnalisées à moindre coût, tout en préservant la sécurité et la décentralisation.

---

### 2. Notions expliquées (définitions simples)
* **Blockchain monolithique :** Une blockchain qui gère toutes ses fonctions (consensus, disponibilité des données, exécution) sur une seule et même couche, ce qui la rend lourde et peu scalable (ex. : Ethereum, Bitcoin).
* **Blockchain modulaire / Couche de disponibilité des données (Data Availability Layer) :** Une blockchain spécialisée dans la publication et l'ordonnancement des données de transactions, sans exécuter les smart contracts (ex. : Celestia).
* **Roll-up (ou L2 / L3) :** Une chaîne d'exécution secondaire qui gère les transactions et smart contracts en s'appuyant sur une autre blockchain (comme Celestia ou Ethereum) pour la sécurité, l'ordre et la disponibilité des données.
* **Disponibilité des données (Data Availability) :** Le fait de pouvoir prouver et garantir publiquement que toutes les données d'un bloc ont bien été publiées et sont accessibles à tous, sans avoir à télécharger l'intégralité de la chaîne.
* **Échantillonnage de la disponibilité des données (Data Availability Sampling) :** Une technique mathématique (utilisant l'effacement de codes) permettant aux nœuds légers de vérifier avec une très haute certitude que l'intégralité d'un bloc a été publiée en ne téléchargeant que de petits morceaux aléatoires.
* **Souveraineté (Sovereign roll-up) :** Un roll-up ou une chaîne qui possède sa propre gouvernance et son propre droit de fork (hard fork) sans dépendre des décisions de la chaîne sous-jacente (contrairement aux roll-ups classiques liés à un smart contract L1).
* **Blobstream :** Un pont unidirectionnel permettant de relayer les engagements de données de Celestia vers Ethereum pour alimenter des L2 de manière économique.

---

### 3. Chiffres, taux, plafonds et règles fiscales
* **Octobre 2022 :** Lancement du Mainnet de Celestia.
* **Règles et limites techniques (à vérifier à la source officielle) :**
  * Limite initiale de taille de bloc de Celestia : 8 mégaoctets (environ 20 fois plus que l'EIP-4444 d'Ethereum).
  * Durée de disponibilité garantie sur Celestia via le CIP proposé : 30 jours (comparé aux 21 jours de l'EIP-4844 sur Ethereum).
  * Taux d'utilisation de Celestia cité : environ 70 % du volume de trading des options DeFi (via des projets comme Aevo) sécurisés par Celestia pour des raisons de coût.

---

### 4. Conseils concrets, limites et risques
* **Conseils pour les développeurs/projets :**
  * Utiliser des solutions modulaires et des couches de disponibilité des données (comme Celestia) pour réduire drastiquement les frais de gaz (jusqu'à 99 % d'économie par rapport au L1 Ethereum) lors du lancement de roll-ups ou d'applications DeFi/Gaming.
  * Privilégier les roll-ups ou chaînes souveraines pour garder le contrôle de la gouvernance et de la sécurité via le hard fork, plutôt que de dépendre entièrement d'un L1 monolithique.
* **Limites et risques :**
  * **Complexité de la composabilité :** Multiplier les roll-ups ou les chaînes indépendantes complique l'interopérabilité et les transferts de liquidité cross-chain.
  * **Risque de centralisation des nœuds légers / validateurs :** Sur certaines structures, la résistance à la censure dépend de métriques hors-chaîne encore en phase de construction communautaire (ex. : réseau de nœuds légers sur Celestia).
  * **Risques de sécurité inhérents au code et aux ponts :** Même avec l'aide des couches modulaires, auditer les contrats et les mécanismes de roll-up reste indispensable.

---

### 5. Produits, applications ou entreprises cités
* **Celestia (et Celestia Labs) :** Projet principal discuté, présenté par ses fondateurs et dirigeants (entreprise des invités, donc promotion/présentation officielle de leur produit).
* **VaultCraft (par Popcorn) :** Boîte à outils on-chain pour déployer des stratégies DeFi automatisées (mentionné dans une publicité/sponsor au début et à la fin de la vidéo).
* **Polkadot :** Présenté comme layer 0 (mentionné dans une publicité sponsorisée par le réseau Polkadot au début et à la fin).
* **Aevo, Mantle, Starknet, Polygon, Arbitrum, Optimism :** Projets L2 ou d'infrastructure cités comme exemples d'adoption ou d'intégration.
* **Filecoin, Arweave :** Protocoles de stockage de données à long terme (distingués de la simple disponibilité des données de Celestia).
* **BitVM, Chainway :** Projets évoquant des roll-ups ZK sur Bitcoin.
