# La guerre invisible qui ENFLAMME Bitcoin !

Vidéo : https://youtu.be/eKqIYzXEpjw · durée 14:19 · résumé Gemini (gemini-3.8-flash) du 2026-10-17
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici la fiche de synthèse de la vidéo, structurée selon les exigences demandées :

---

### 1. Sujet et thèse principale
* **Sujet :** Le débat sur la gouvernance de Bitcoin suscité par la proposition **BIP-110**, qui vise à filtrer et restreindre les données non monétaires (inscriptions *Ordinals*, tokens BRC-20, Runes) sur la blockchain.
* **Thèse principale :** Tenter de censurer ou de restreindre des données au niveau du consensus de Bitcoin est à la fois inefficace techniquement (ces restrictions sont immédiatement contournables, ce qui alourdit encore plus le réseau) et dangereux sur le plan idéologique, car cela crée un précédent menaçant la neutralité et la résistance à la censure de Bitcoin.

---

### 2. Notions expliquées (définitions simples)
* **BIP (*Bitcoin Improvement Proposal*) :** Document décrivant formellement une proposition d’évolution ou de standard technique pour le protocole Bitcoin (ici, le BIP-110 : *Reduced Data Temporary Softfork*).
* **Soft fork :** Mise à jour des règles du réseau rétrocompatible, rendant les règles de validation plus strictes sans scinder obligatoirement la chaîne.
* **Nœud (*Node*) vs Mineur :** 
  * *Nœud :* Ordinateur validant et relayant les transactions selon les règles du protocole.
  * *Mineur :* Entité assemblant les transactions dans des blocs grâce à la puissance de calcul (Proof of Work).
* **OP_RETURN :** Commande dans le code d’une transaction Bitcoin permettant d’associer une petite quantité de données arbitraires (texte, etc.).
* **Ordinals / BRC-20 / Runes :** Méthodes techniques apparues à la suite de la mise à jour Taproot, permettant d'inscrire des images, des tokens ou des métadonnées directement dans les transactions Bitcoin.
* **UASF (*User Activated Soft Fork*) :** Mécanisme d'activation d'une mise à jour poussé directement par les opérateurs de nœuds, imposant des règles même sans le consentement majoritaire des mineurs.

---

### 3. Chiffres, dates, taux et règles cités
* **Dates clés :**
  * *Fin 2021 :* Activation de la mise à jour Taproot.
  * *2023 :* Explosion de l'usage des inscriptions Ordinals.
  * *Octobre 2025 :* Sortie de Bitcoin Core v30 et publication de la proposition BIP-110.
  * *6 février 2026 :* Démission de Gloria Zhao, développeuse de Bitcoin Core.
  * *2 mars 2026 :* Minage du premier bloc signalant BIP-110 par le pool Ocean (bloc 938903).
  * *Septembre 2026 :* Date butoir fixée dans le BIP-110 pour une activation forcée par UASF.
* **Chiffres et seuils techniques :**
  * *OP_RETURN :* Limite historique de 83 octets relevée à près de 100 000 octets (~100 ko) avec Bitcoin Core v30.
  * *Répartition des nœuds (début 2026) :* ~63 % pour Bitcoin Core, ~26 % pour Bitcoin Knots.
  * *Seuils d'activation :* 55 % de support des mineurs requis pour BIP-110 (contre 95 % pour SegWit en 2017 et 90 % pour Taproot en 2021).
  * *Adoption réelle de BIP-110 :* ~5 % des nœuds et ~2 % du hash rate mondial (uniquement la pool Ocean).
  * *Revenus des mineurs :* Environ 500 millions de dollars générés par les frais de transaction liés aux Ordinals, BRC-20 et Runes.
  * *Démonstration de contournement :* Inscription d’une image de 66 ko dans une transaction sans utiliser OP_RETURN ni Taproot.
* **Conditions commerciales Bybit (promotion partenaire) :**
  * Dépôt éligible à partir de 1 €.
  * Rendement promotionnel de 3 % calculé au prorata sur une période de 180 jours (fonds devant rester immobilisés pendant ces 180 jours).
  * Bonus de parrainage pouvant atteindre 15 USDC par filleul (sous condition de KYC et de dépôt de 100 € conservé 180 jours).
  * Rendements Bybit Earn présentés jusqu'à 20 % (*détails non précisés*).
* **Règles fiscales :** Aucune règle fiscale mentionnée (*à vérifier à la source officielle*).

---

### 4. Conseils concrets, limites et risques
* **Comprendre la neutralité d'un protocole décentralisé :** Vouloir interdire le « spam » (fichiers images, mèmes) crée un mécanisme de filtrage subjectif qui pourrait être détourné par des États pour censurer des transactions monétaires.
* **Limites techniques du filtrage :** Forcer les utilisateurs à contourner les restrictions oblige à découper les données en multiples sorties (*outputs*), ce qui alourdit paradoxalement l'espace mémoire (*UTXO set*) géré par les nœuds.
* **Risques liés à l'offre financière (Bybit) :**
  * *Risque de contrepartie :* Conservation des fonds sur un exchange centralisé.
  * *Risque de liquidité :* Obligation de conserver les dépôts pendant 180 jours pour toucher la prime de 3 %.

---

### 5. Produits, applications ou entreprises cités
* **Bybit :** Plateforme d'échange crypto (*partenariat commercial / publicité*).
* **Journal du Coin (Canal Telegram) & Steady Lads (Cara) :** Services, émissions et canaux d'information (*produits de l'auteur / média*).
* **Bitcoin Core :** Logiciel et implémentation de référence du nœud Bitcoin (*cité pour analyse*).
* **Bitcoin Knots :** Implémentation alternative de Bitcoin maintenue par Luke Dashjr (*citée pour analyse*).
* **Ocean Mining :** Pool de minage cofondé par Jack Dorsey et Luke Dashjr (*cité pour analyse*).
* **Blockstream :** Entreprise technologique Bitcoin dirigée par Adam Back (*citée pour analyse*).
* **Foundry USA, AntPool, F2Pool :** Principaux pools de minage Bitcoin (*cités pour analyse*).
