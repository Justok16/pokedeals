# À quoi ressemblera Ethereum avec son nouvel accent sur la confidentialité

Vidéo : https://youtu.be/ZarQsQy_czc · durée 1:12:41 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Bien sûr, voici une fiche de connaissances basée sur la vidéo :

### 1) Sujet et thèse principale
* **Sujet** : La confidentialité (privacy) dans l'écosystème Ethereum et l'évolution des technologies et des mentalités vers plus de protection des données personnelles sur les blockchains publiques.
* **Thèse principale** : Par défaut, les blockchains publiques comme Ethereum ou Bitcoin ne sont pas privées mais pseudonymes ; toutes les actions y sont enregistrées définitivement. Face aux risques réglementaires, de sécurité et financiers pour les particuliers et les institutions, la confidentialité est devenue un enjeu prioritaire. L'écosystème s'organise (via des initiatives comme le *Privacy Cluster* et le groupe de travail IPTF) pour développer et intégrer des technologies de confidentialité à tous les niveaux, rendant possible leur adoption par des acteurs institutionnels et grand public.

---

### 2) Notions expliquées
* **Pseudonymat (contrairement à l'anonymat)** : En crypto, les actions ne sont pas anonymes mais rattachées à une adresse publique permanente. N'importe qui peut tracer ces actions, ce qui présente des risques de fuite de données personnelles, financières ou juridiques.
* ***Privacy Cluster*** : Une initiative lancée début octobre par la Fondation Ethereum, regroupant 47 chercheurs, ingénieurs et cryptographes (coordonnée par BlokScout et l'équipe Xord, avec Igor Barinov) pour faire de la confidentialité une priorité de premier ordre sur Ethereum.
* **IPTF (*Institutional Privacy Task Force*)** : Task force (groupe de travail) de la Fondation Ethereum active depuis 2019 (dirigée par Oskar Thorén), se concentrant sur la résolution des besoins de confidentialité des institutions sur les blockchains publiques.
* **PSE (*Privacy and Scaling Explorations*)** : Équipe de recherche de la Fondation Ethereum (dirigée par Andy Guzman) explorant de nouveaux cas d'usage autour de la confidentialité et de la scalabilité (ZKP, etc.).
* ***Private Reads & Writes*** : Technologies ou méthodes permettant de lire et d'écrire sur une blockchain sans révéler publiquement les données sensibles de l'utilisateur.
* **Preuves à divulgation nulle de connaissance (*Zero-Knowledge Proofs* ou ZKP)** : Cryptographie permettant de prouver la véracité d'une information (par exemple, posséder l'âge requis ou un solde bancaire suffisant) sans révéler l'information elle-même (ni nom, ni document d'identité).
* **ZK-Rollups et ZK-EVMs** : Technologies de seconde couche (*Layer 2*) utilisées par Ethereum pour la mise à l'échelle et la confidentialité.
* ***Stealth Addresses*** : Adresses furtives qui génèrent une nouvelle adresse à chaque réception de fonds, améliorant la confidentialité du destinataire (similaire au modèle UTXO).
* **MPC (*Multi-Party Computation*)** : Calcul multipartite sécurisé, permettant à plusieurs parties d'effectuer des calculs sur des données chiffrées sans révéler les données sous-jacentes.
* **Homomorphic Encryption (Chiffrement homomorphe)** : Technologie permettant d'effectuer des calculs sur des données chiffrées sans les déchiffrer au préalable.
* **TEE (*Trusted Execution Environment*)** : Environnement d'exécution de confiance basé sur le matériel (*hardware*) pour sécuriser les opérations sensibles.
* **Kohaku** : Implémentation de référence et kit de développement logiciel (*SDK*) intégrant plusieurs protocoles de confidentialité existants sur Ethereum, facilitant leur adoption par les développeurs de portefeuilles (*wallets*).

---

### 3) Chiffres, taux, plafonds et règles fiscales cités
* **Octobre 2023** (*à vérifier à la source officielle*) : Annonce du lancement du *Privacy Cluster* par la Fondation Ethereum.
* **2019** : Début des activités de l'IPTF (*Institutional Privacy Task Force*).
* **3,3 trillions de dollars** : Volume total sécurisé par le protocole Uniswap, avec zéro hack (*à vérifier à la source officielle*).
* **1,3 milliard d'utilisateurs** : Nombre d'utilisateurs en Inde utilisant des programmes d'identité numérique centralisée (comme Aadhaar) (*à vérifier à la source officielle*).
* **25 % à 30 %** : Part estimée des transactions sur Tornado Cash qui étaient privées/conformes (*à vérifier à la source officielle*).

---

### 4) Conseils concrets et leurs limites ou risques
* **Conseil 1** : Ne pas supposer que la crypto est privée par défaut ; comprendre que chaque action sur une blockchain publique est enregistrée pour toujours.
  * **Risques/limites** : Risque de fuite d'informations personnelles, financières et juridiques (harcèlement, piratage physique, censure).
* **Conseil 2** : Utiliser des technologies de confidentialité émergentes (ZKP, *Stealth Addresses*, MPC) pour protéger ses données lors de transactions ou d'interactions décentralisées.
  * **Risques/limites** : Complexité technique de ces outils, courbe d'apprentissage élevée pour le grand public, et compromis entre vitesse, coût (*gas*) et niveau de confidentialité.

---

### 5) Produits, applications ou entreprises cités
* **Uniswap (Uniswap Labs)** : Plateforme d'échange décentralisée et API de trading citées dans la vidéo. (*Publicité / Partenaire de l'émission*).
* **Zcash** : Mentionné comme pionnier de la confidentialité (*Non sponsorisé*).
* **Tornado Cash** : Mentionné comme protocole de mixage de transactions (*Non sponsorisé*).
* **Aave** : Mentionné pour des exemples de transactions sur *Layer 2* (*Non sponsorisé*).
* **BlokScout** : Mentionné comme coordinateur du *Privacy Cluster* (*Non sponsorisé*).
* **Xord** : Mentionné comme co-fondateur du *Privacy Cluster* (*Non sponsorisé*).
* **Aadhaar** : Système d'identité numérique en Inde (*Non sponsorisé*).
* **Unchained** : Nom du podcast hébergé par Laura Shin (*Produit de l'auteur*).
