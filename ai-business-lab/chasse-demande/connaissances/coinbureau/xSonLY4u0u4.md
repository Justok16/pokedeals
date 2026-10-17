# CB : 100 millions de dollars dérobés dans le portefeuille crypto le plus sûr

Vidéo : https://youtu.be/xSonLY4u0u4 · durée 16:53 · résumé Gemini (gemini-3.5-flash-lite, lot de 9) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Sujet et thèse principale** :
- Sujet : Une vulnérabilité critique (bug de génération de nombres aléatoires) découverte dans la bibliothèque logicielle MicroPython/Libbitcoin utilisée par certains wallets matériels (notamment Coldcard Mk2 et Mk3), ayant entraîné le vol de millions de dollars en Bitcoin.
- Thèse : Un défaut de configuration dans le code source de certains wallets (désactivation de la source matérielle d'aléa RNG au profit d'un générateur logiciel prévisible) a compromis la sécurité de la génération des clés privées et des seed phrases, illustrant les limites de l'auto-garde (self-custody) lorsque le code sous-jacent présente des failles non audités.

2) **Notions expliquées** :
- **Seed phrase (Phrase mnémonique)** : Suite de 12 ou 24 mots générée selon la norme BIP-39 permettant de restaurer l'intégralité d'un portefeuille crypto.
- **RNG (Random Number Generator)** : Générateur de nombres aléatoires, essentiel pour créer des clés cryptographiques uniques et imprévisibles.
- **Multisig (Multi-signature)** : Configuration de sécurité nécessitant plusieurs clés privées distinctes pour valider une transaction.
- **Entropy (Entropie)** : Mesure du caractère aléatoire nécessaire pour garantir la sécurité d'une clé privée.

3) **Chiffres, taux, plafonds et règles fiscales** :
- Montant total drainé sur les wallets Coldcard vulnérables : Plusieurs millions de dollars (plus de 100 millions de dollars au total sur divers wallets affectés par des failles similaires par le passé, comme 160 millions de dollars pour Wintermute en 2022).
- Période de fabrication concernée : Wallets créés avec le firmware v4.0.0 à v5.0.3 sur Coldcard Mk2 et Mk3 (les modèles Mk4, Mk5 et Q utilisent 72 bits d'entropie et ne sont pas affectés par ce même bug spécifique de 32 bits).
- Perte individuelle rapportée : Un entrepreneur canadien (Jonathan Goodman) a perdu 18,25 BTC (~1,6 million de dollars) en moins de 7 minutes.
- *Règle fiscale/légale : À vérifier à la source officielle (responsabilités juridiques des fabricants de hardware wallets en cas de faille de sécurité).*

4) **Conseils concrets et risques** :
- Vérifier la version du firmware et la date de création de sa seed phrase (si elle a été générée sur un firmware ancien de type v4.0.0 à v5.0.3 sur Coldcard Mk2/Mk3, la considérer comme compromise).
- Mettre à jour le firmware ne suffit pas à réparer une seed déjà compromise : il faut générer un **nouveau** portefeuille sur un firmware corrigé et transférer les fonds.
- Ne jamais taper sa seed phrase sur un site web de vérification ou un "bogue/vulnerability checker" (risque de phishing massif).

5) **Produits, applications ou entreprises cités** :
- Coldcard (Make, Mk2, Mk3, Mk4, Mk5, Q), Coinkite (fabricant).
- Trust Wallet, Libbitcoin, Ledger, Trezor, BitBox.
- Coin Bureau Club (club de l'auteur – **produit de l'auteur / autopromotion**).

---
