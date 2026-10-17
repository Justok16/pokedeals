# Nouveau Fork Bitcoin : le réseau doit évoluer, mais à quel prix ?

Vidéo : https://youtu.be/Mm0-whHFK5c · durée 1:16:11 · résumé Gemini (gemini-3.5-flash) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo sous forme de fiche de connaissances, structuré selon vos consignes :

### 1) Sujet et thèse principale
* **Sujet** : Les conflits de gouvernance technique du réseau Bitcoin (notamment via la proposition de mise à jour **BIP-110** visant à restreindre les inscriptions de données non monétaires comme les *Ordinals*) et la menace théorique à long terme de l'informatique quantique sur la cryptographie de Bitcoin.
* **Thèse principale** : L'utilisation de l'espace de bloc pour des données non monétaires crée de fortes tensions au sein de la communauté Bitcoin (partisans de *Bitcoin Core* vs *Bitcoin Knots*). Bien que le BIP-110 propose un filtre temporaire pour désengorger le réseau, il présente un risque majeur de scission (fork) de la blockchain s'il est activé sans consensus massif. Quant à la menace quantique, elle est réelle sur le papier mais reste lointaine (estimée entre 5 et 50 ans par les experts), et le réseau dispose de solutions de transition à l'étude.

---

### 2) Les notions expliquées
* **Soft Fork** : Une mise à jour du protocole d'une blockchain qui est rétrocompatible. Elle restreint généralement les règles du réseau plutôt que de les élargir (contrairement à un *Hard Fork*).
* **BIP (Bitcoin Improvement Proposal)** : Une proposition d'amélioration formelle soumise par des développeurs ou membres de la communauté pour faire évoluer le protocole Bitcoin.
* **Client / Nœud Bitcoin** : Le logiciel que les utilisateurs et validateurs font tourner pour participer au réseau, vérifier les transactions et maintenir l'historique de la blockchain (ex. *Bitcoin Core*, *Bitcoin Knots*).
* **Ordinals / Inscriptions** : Procédé permettant d'inscrire des données arbitraires (images, textes, jetons) directement dans des transactions Bitcoin, assimilable à des NFT sur Bitcoin.
* **ECDSA (Elliptic Curve Digital Signature Algorithm)** : L'algorithme cryptographique de signature actuellement utilisé par Bitcoin pour sécuriser les paires de clés publiques et privées.
* **Menace quantique (cryptographie)** : Le risque théorique que de futurs ordinateurs quantiques surpuissants parviennent, via l'algorithme de Shor, à déduire une clé privée à partir d'une clé publique visible sur la blockchain.
* **Bloc orphelin** : Un bloc valide qui est rejeté de la blockchain principale car un autre nœud a propagé un bloc concurrent de même hauteur plus rapidement.

---

### 3) Les chiffres, taux, plafonds et règles fiscales cités
* **Règles fiscales ou légales** : Aucun aspect fiscal ou légal n'est abordé dans cette vidéo (*sans objet / non précisé*).
* **Chiffres et taux techniques** :
  * **Part de marché de Bitcoin Knots** : Représente entre 10 % et 20 % des nœuds du réseau au moment de la vidéo (contre moins de 1 % un an auparavant).
  * **Seuil d'activation du BIP-110** : Fixé à **55 %** de signalement par les mineurs sur une période de 2016 blocs (environ 2 semaines), contrairement au seuil historique de 95 % utilisé pour SegWit en 2017.
  * **Dates clés du déploiement de BIP-110** (*visuelles à l'écran, à vérifier à la source officielle*) : Début de la signalisation le **1er décembre 2025**, limite d'activation le **1er septembre 2026** (hauteur maximale de bloc), avec une expiration du soft fork **1 an après l'activation**.
  * **Activité quantique en Chine** : Non précisé en tant que tel, mais la part des mineurs de Bitcoin situés en Chine est estimée entre **20 % et 30 %** du réseau global.
  * **Clés de Satoshi Nakamoto** : Environ **1 million de BTC** (soit près de 5 % de la supply totale) dorment sur des adresses dont les clés publiques sont exposées, ce qui les rendrait vulnérables à une attaque quantique.

---

### 4) Conseils concrets et leurs limites ou risques
* **Profiter des marchés baissiers (Bear Market)** : L'auteur conseille d'utiliser les périodes de baisse pour se former, approfondir ses connaissances techniques et comprendre le fonctionnement des protocoles.
* **Inspecter la blockchain** : Utiliser des outils d'exploration visuelle comme *Mempool.space* pour observer l'encombrement du réseau, le coût des frais de transaction et la proportion de données de type "inscription".
* **S'impliquer localement** : Rejoindre des meetups physiques via des plateformes communautaires pour échanger et réaliser des transactions de gré à gré (Peer-to-Peer).
* **Risques identifiés** :
  * **Risque de scission (Fork)** : Un soft fork forcé par une faible majorité (comme le seuil de 55 % du BIP-110) risque d'exclure les nœuds minoritaires ou de provoquer des pertes de fonds pour les utilisateurs non informés.
  * **Risques de bugs logiciels** : L'auteur mentionne l'existence de failles critiques (comme un bug dans la version Bitcoin Core v30.0 lié à la gestion des portefeuilles), rappelant qu'il faut être prudent lors de l'implémentation de nouvelles versions.
  * **Adresses exposées au quantique** : Les adresses Bitcoin les plus anciennes (génération P2PK) ou les adresses réutilisées exposent leur clé publique, ce qui les rend vulnérables. La recommandation implicite est de migrer vers des formats d'adresses modernes (comme Taproot ou Native Segwit) et de ne jamais réutiliser une adresse.

---

### 5) Produits, applications ou entreprises cités
* **Bitcoin Core & Bitcoin Knots** : Logiciels clients de nœuds Bitcoin (gratuits, open-source).
* **Citrea & BitVM** : Projets de réseaux de seconde couche (Layer 2) sur Bitcoin (cités à titre informatif).
* **Mempool.space** : Outil d'exploration de blocs et de file d'attente des transactions (mentionné comme ressource d'analyse).
* **communautesbitcoin.org & btcmap.org** : Annuaires et cartes interactives pour localiser les meetups Bitcoin en France (mentionnés comme ressources gratuites).
* **Anduro (et la société Marathon)** : Initiative de recherche travaillant sur des solutions de résistance quantique comme le protocole *BIP-360*.
* **Ocean Pool & Binance Pool** : Coopératives de minage (mining pools).
* **XRP (Ripple)** : Mentionné brièvement ; l'auteur conseille de "fuir" ce produit en raison de sa faible utilité selon lui.

*Note : La vidéo ne contient aucune communication publicitaire rémunérée ni de produit vendu directement par l'auteur.*
