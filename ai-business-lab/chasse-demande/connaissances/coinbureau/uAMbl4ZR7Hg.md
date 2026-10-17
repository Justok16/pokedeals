# Prochain fork de Bitcoin ? Explication des menaces quantiques et des conflits de développement

Vidéo : https://youtu.be/uAMbl4ZR7Hg · durée 23:09 · résumé Gemini (gemini-3.5-flash-lite, lot de 4) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Sujet et thèse principale** : La vidéo explore les propositions de Bitcoin Core visant à supprimer la limite technique du champ `OP_RETURN` (le plafond de 80 octets) et analyse si cela pourrait mener à un « hard fork » ou diviser la communauté Bitcoin, tout en abordant la menace théorique des ordinateurs quantiques sur la cryptographie de Bitcoin. La thèse principale est que la suppression de cette limite est une modification de politique (et non de consensus) qui ne devrait pas casser le réseau, mais qu'elle ravive le débat sur la gestion des données sur la blockchain, tandis que le risque quantique à court terme est largement exagéré.
2) **Notions expliquées** :
- **OP_RETURN** : Fonction de Bitcoin permettant d'inclure de petites quantités de données arbitraires dans une transaction non dépensable (UTXO).
- **Ordinals et Inscriptions** : Protocole permettant d'attacher des métadonnées (images, texte) à un satoshi spécifique, créant des actifs uniques sur Bitcoin (NFTs).
- **Hard Fork** : Modification majeure du protocole de la blockchain créant une division permanente en deux réseaux incompatibles si tous les nœuds ne se mettent pas à jour.
- **SegWit (Segregated Witness)** : Mise à jour ayant séparé les données de signature des transactions pour augmenter la capacité des blocs et résoudre la malléabilité.
- **Qubits** : Unités d'information quantique de base utilisées par les ordinateurs quantiques, dont le nombre détermine la puissance de calcul pour casser le chiffrement.
3) **Chiffres, taux, plafonds et règles fiscales citées** :
- **Date de la source** : Mai 2025 (année mentionnée dans les articles affichés).
- **Limite actuelle d'OP_RETURN** : 80 octets.
- **Offre totale de Bitcoin** : 21 millions.
- **Bitcoins perdus ou inaccessibles** : Estimés à environ 3,8 millions de BTC.
- **Nombre de qubits nécessaires pour casser RSA-2048** : Estimé à environ 4 000 qubits logiques.
- **Nombre de qubits nécessaires pour casser SHA-256 (Bitcoin)** : Estimé à environ 8 000 qubits logiques.
- **Règle fiscale/légale** : Aucune règle fiscale ou légale spécifique n'est citée (à vérifier à la source officielle).
4) **Conseils concrets, limites et risques** :
- **Risques** : La suppression de la limite `OP_RETURN` pourrait encourager le stockage de données non financières (spam), augmentant la taille de la blockchain et la charge des nœuds.
- **Risques (Quantique)** : Bien que les ordinateurs quantiques représentent une menace théorique à long terme pour la cryptographie asymétrique (RSA, ECC), les ordinateurs quantiques actuels sont encore trop instables et loin de disposer du nombre de qubits nécessaires pour menacer Bitcoin.
5) **Produits, applications ou entreprises cités** :
- **Bitcoin Core / Bitcoin Knots** : Implémentations logicielles majeures du protocole Bitcoin.
- **Lightning Network** : Solution de couche 2 pour des paiements rapides sur Bitcoin.
- **Coin Bureau Deals** : Plateforme promue par l'auteur pour des offres sur des portefeuilles et services crypto (publicité/produit de l'auteur).
