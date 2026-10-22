# Comment 1inch met la liquidité dormante de la DeFi au travail avec Aqua

Vidéo : https://youtu.be/6hEsGl2K4nQ · durée 23:29 · résumé Gemini (gemini-3.1-flash-lite, lot de 7) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Sujet et thèse** : Présentation du protocole "Aqua" par 1inch, un outil de liquidité partagée sur la finance décentralisée (DeFi). La thèse est que les modèles de liquidité traditionnels de type *UniSwap* présentent des problèmes d'inefficacité (pertes dues aux *mathbots*, dilution des actifs, et inutilisation de la majorité des fonds). Aqua propose une solution basée sur l'intention de l'utilisateur pour une meilleure efficacité du capital.

2) **Notions expliquées** : 
* **Liquidité partagée (ou regroupée)** : Capacité de fournir des actifs dans un pool pour faciliter les échanges, sans être limité à une seule paire de jetons.
* **Mathbots** : Algorithmes automatisés qui exploitent les inefficacités de prix dans les pools de liquidité, pénalisant souvent les fournisseurs de liquidité.
* **Just-in-time liquidity (JIT)** : Provision de liquidité de courte durée par des robots juste avant une transaction importante, capturant les frais au détriment des fournisseurs habituels.

3) **Chiffres et règles** :
* 85 % de la liquidité DeFi est inutilisée (selon une étude réalisée avec Dune, à vérifier à la source officielle).
* 95 % du temps, une grande partie de la liquidité ne bouge pas (selon l'auteur, à vérifier à la source officielle).
* **Règles fiscales/légales** : Non précisé.

4) **Conseils et limites** :
* Conseil : Utiliser des stratégies basées sur l'intention (*intent-based*) pour définir des plages de prix et des frais acceptables pour éviter de se faire exploiter par les robots (*MEV*).
* Limites/Risques : Le passage à un protocole de type Aqua demande une compréhension technique plus poussée des mécanismes de *market making* (tenue de marché).

5) **Produits et entreprises** :
* **1inch** : Co-fondée par l'intervenant (Sergej Kunz).
* **Aqua** : Produit de 1inch.
* **Dune** : Outil d'analyse.
* **Morpho, Aave, UniSwap, etc.** : Protocoles cités pour comparaison (non-publicitaire).
