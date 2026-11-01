# Can dYdX Become a Decentralized BitMEX? How It Is Scaling With StarkWare - Ep.218

Vidéo : https://youtu.be/y_jOcpsj8EA · durée 1:09:11 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-31
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances en finances personnelles, basée sur le contenu de la vidéo :

---

# Fiche de connaissances : Scalabilité et finance décentralisée (DeFi)

## 1. Sujet et thèse principale
* **Sujet :** L'utilisation des solutions de passage à l'échelle (Layer 2, et notamment les rollups de type STARK) dans la finance décentralisée (DeFi), à travers l'exemple de la plateforme de dérivés d'actifs d'échange *dYdX* propulsée par la technologie de *StarkWare*.
* **Thèse principale :** Pour que la DeFi et le trading de dérivés sur cryptomonnaies se développent massivement, il est indispensable de surmonter la saturation et les frais élevés de la couche 1 (Ethereum) en adoptant des technologies de scalabilité performantes (comme les rollups validés par des preuves mathématiques), garantissant rapidité, sécurité et faibles frais de transaction, tout en rivalisant avec les bourses centralisées.

---

## 2. Notions expliquées (définitions simples)
* **Produits dérivés synthétiques / perpétuels :** Contrats financiers permettant de trader (spéculer sur le prix) des actifs sans détenir réellement l'actif sous-jacent (par exemple, un contrat perpétuel Bitcoin sans détenir de Bitcoin physique), souvent combinés avec du levier pour multiplier gains et pertes.
* **Effet de levier :** Mécanisme permettant d'amplifier sa mise (et donc ses gains ou pertes potentiels) en empruntant du capital sur la plateforme.
* **Layer 1 (L1) :** La blockchain principale (ex. : Ethereum), sécurisée mais limitée en termes de capacité (débit de transactions) et coûteuse en frais de gaz lors des pics d'utilisation.
* **Layer 2 (L2) / Solutions de passage à l'échelle :** Technologies construites au-dessus du Layer 1 pour traiter un grand nombre de transactions hors de la chaîne principale avant de les valider en bloc, réduisant ainsi drastiquement les coûts et augmentant la vitesse.
* **Rollups (Optimistic vs ZK Rollups) :** 
  * *Optimistic Rollups* : Supposent que les transactions sont valides par défaut, avec une période de contestation (« *withdrawal time* » pouvant aller jusqu'à une semaine) avant finalité complète sur le L1.
  * *ZK Rollups (Validité / STARKs)* : Utilisent des preuves cryptographiques (preuves mathématiques de validité, telles que les *STARKs*) pour garantir l'instantanéité et l'intégrité des transactions dès leur validation sans attendre de période de contestation.
* **Oracles :** Services externes qui fournissent les prix des actifs en temps réel aux contrats intelligents de la plateforme (pour gérer les liquidations, etc.).
* **Composabilité :** Capacité pour différents protocoles DeFi de s'interconnecter et de se composer mutuellement (comme des briques de Lego), permise par l'architecture ouverte des blockchains.

---

## 3. Chiffres, taux, plafonds et règles fiscales cités
* **Frais de transaction sur Layer 1 :** Entre 100 $ et parfois 1 000 $ par transaction lors des pics de congestion sur Ethereum *(à vérifier à la source officielle)*.
* **Performances démontrées (TPS - Transactions par seconde) sur L1 :** Environ 3 000 TPS atteints lors d'un test spécifique *(à vérifier à la source officielle)*.
* **Performances démontrées avec les solutions L2 (ex. : Diversifi) :** Jusqu'à 9 000 TPS pour le trading et 18 000 TPS pour les paiements *(à vérifier à la source officielle)*.
* **Effet de levier proposé :** Démarrage à 25x sur le nouveau produit L2 de dYdX *(à vérifier à la source officielle)*.
* **Période de finalité (retrait) :** Instantanée avec les solutions de type *STARKs* (ZK rollups), contrairement aux rollups optimistes qui peuvent nécessiter jusqu'à une semaine *(à vérifier à la source officielle)*.
* **Règles fiscales / Légales :** *Non précisé dans la vidéo (le sujet aborde la technique et l'infrastructure, pas la fiscalité des plus-values).*

---

## 4. Conseils concrets et leurs limites ou risques
* **Conseil/Opportunité :** S'intéresser et s'orienter vers les protocoles et technologies de couche 2 (Layer 2) pour réduire les coûts de transaction et améliorer l'expérience utilisateur dans la DeFi.
* **Limites et Risques :** 
  * Risque lié à l'effet de levier élevé (les positions peuvent être rapidement liquidées en cas de forte volatilité des marchés si les oracles de prix accusent un retard de mise à jour).
  * Complexité technique de l'écosystème DeFi et nécessité de bien maîtriser le fonctionnement de ses portefeuilles et des contrats intelligents.
  * Période de transition et d'apprentissage pour les développeurs et utilisateurs migrant vers de nouveaux langages (comme *Cairo* pour StarkWare).

---

## 5. Produits, applications ou entreprises cités
* **dYdX :** Plateforme de trading de dérivés décentralisée (fondateur : Antonio Juliano). *(Partenaire / Invité, non présenté comme une publicité directe payante dans cet extrait).*
* **StarkWare :** Entreprise technologique fournissant des solutions de scalabilité basées sur les preuves STARK (cofondateur : Eli Ben-Sasson). *(Partenaire / Invité).*
* **Crypto.com :** Application mobile d'achat, de vente et d'épargne en cryptomonnaies, proposant des cartes Visa de débit avec cash-back et des taux d'intérêt (Crypto Earn). *(Publicité / Sponsor de l'émission).*
* **Square (API) :** Solutions de paiement en ligne pour applications web. *(Publicité / Sponsor de l'émission).*
* **Autres protocoles cités à titre d'exemples ou de comparaison :** *Uniswap*, *Solana*, *Near*, *Optimism*, *Arbitrum*, *DeversiFi*, *Immutable X*, *Badger DAO*.
