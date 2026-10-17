# Bittensor (TAO) : La Masterclass Ultime pour Tout Comprendre ! - avec Gustave Laurent

Vidéo : https://youtu.be/N0EapkqEHVM · durée 1:07:04 · résumé Gemini (gemini-3.5-flash) du 2026-10-17
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de synthèse récapitulative sous forme de fiche de connaissances :

---

### 1) Sujet et thèse principale

*   **Sujet :** Le fonctionnement, l'architecture et le modèle économique du protocole Bittensor (token **TAO**), un réseau spécialisé dans l'intelligence artificielle et la coordination d'incitations économiques décentralisées.
*   **Thèse principale :** Bittensor ne doit pas être vu uniquement comme une crypto d'IA, mais comme une architecture globale de « réseaux d'incitations » (*Subnets*). Il permet de récompenser la production de n'importe quelle ressource numérique (calcul, recherche médicale, génération de texte/image) en utilisant le jeton TAO comme unité de valeur et de bande passante.

---

### 2) Notions expliquées (définitions simples)

*   **Bittensor ($TAO) :** Blockchain de couche 1 (fondée sur la technologie Substrate) qui orchestre l'émission et la distribution du jeton TAO pour rémunérer la création de ressources numériques.
*   **Subnet (Sous-réseau) :** Application ou sous-système dédié à une tâche spécifique au sein du réseau Bittensor (ex. : calcul décentralisé, modèles de langage, repliement de protéines).
*   **Subnet Owner (Propriétaire de Subnet) :** L'équipe ou l'entité qui crée le Subnet et définit son système d'évaluation et de récompense pour inciter les participants à effectuer un travail précis.
*   **Mineur (Miner) :** Acteur qui fournit la ressource informatique ou effectue le travail requis par le Subnet (ex. : mettre à disposition de la puissance GPU, entraîner une IA).
*   **Validateur (Validator) :** Acteur qui évalue la qualité du travail produit par les mineurs et vote pour déterminer l'attribution des récompenses du réseau.
*   **Dynamic TAO (dTAO) :** Mise à jour importante visant à décentraliser le vote d'attribution des émissions de TAO en permettant à chaque détenteur de staker directement ses jetons sur des Subnets spécifiques.
*   **Recyclage (Recycling) :** Mécanisme par lequel le TAO payé pour enregistrer un mineur ou un Subnet est remis dans la réserve d'émissions futures, réduisant l'inflation nette et retardant le *halving*.
*   **Weight Copying :** Attaque ou mauvaise pratique consistant pour un validateur à copier automatiquement les notes attribuées par un autre validateur au lieu de vérifier lui-même le travail des mineurs.

---

### 3) Chiffres, taux, plafonds et règles fiscales cités

*   **Offre maximale (Hard Cap) :** 21 000 000 de jetons TAO (similaire au Bitcoin).
*   **Émission de TAO :** 1 TAO émis par bloc (environ 7 200 TAO émis par jour).
*   **Nombre de Subnets :** Limité à 64 Subnets en parallèle (au moment de l'interview).
*   **Coût d'enregistrement d'un Subnet :** Environ 2 000 TAO (ajustable selon l'offre et la demande).
*   **Répartition des émissions d'un Subnet :**
    *   **18 %** au Subnet Owner ;
    *   **41 %** aux mineurs du Subnet ;
    *   **41 %** aux validateurs du Subnet.
*   **Rendements du staking (APY) :**
    *   Staking passif/généraliste auprès des grands validateurs : **12 % à 14 % APY**.
    *   Staking optimisé ciblant les meilleurs validateurs par Subnet : **19 % à 20 % APY**.
*   **Halving & Blocs :**
    *   Halving théorique tous les 4 ans (comme le Bitcoin, calé initialement sur 10 500 000 TAO émis). Contrairement au Bitcoin, le recyclage de TAO ralentit la baisse des émissions en reportant la date effective du halving. *(À vérifier à la source officielle)*.
*   **Délais techniques (Tempo) :** Changement d'allocation de staking soumis à une fenêtre de 360 blocs (environ 24 heures) pour éviter la perte de rewards.
*   **Règles fiscales :** Non précisées dans la vidéo *(à vérifier à la source officielle)*.

---

### 4) Conseils concrets, limites et risques

*   **Conseils concrets :**
    *   **Optimisation du Staking :** Pour obtenir le meilleur rendement (APY), il est préférable de diversifier et d'allouer ses jetons auprès de validateurs spécialisés par Subnet plutôt que de déléguer l'ensemble de ses TAO à un seul grand validateur généraliste.
    *   **Développement de Subnet :** Tester impérativement ses algorithmes d'incitation sur le *Testnet* pour s'assurer que les mineurs ne trouvent pas de failles d'exploitation (tricherie) avant de passer sur le réseau principal (*Mainnet*).

*   **Limites et risques :**
    *   **Risque de centralisation temporaire :** Avant l'implémentation complète de Dynamic TAO, les 64 plus gros validateurs concentrent le pouvoir de vote sur les émissions allocated aux Subnets.
    *   **Risque de perte de jetons / Coût d'entrée :** Le coût de réservation d'un slot de mineur ou de Subnet est variable et non remboursable si le sous-réseau se fait remplacer par un concurrent plus performant.
    *   **Pénalité sur les rotations de Staking :** Déplacer constamment ses TAO sans respecter le délai technique de rotation (tempo) fait perdre immédiatement plusieurs jours de rémunération.
    *   **Risque de gaming/triche :** Si un Subnet Owner conçoit mal ses critères d'évaluation, les mineurs peuvent percevoir des récompenses sans fournir de travail réel de valeur.

---

### 5) Produits, applications et entreprises cités

*   **MantaMinds :** Entreprise cofondée par l'invité (Gustave Laurent), spécialisée dans l'optimisation non-custodiale de l'allocation de staking de TAO *(Produit de l'intervenant)*.
*   **Bittensor ($TAO) :** Le protocole central abordé dans la vidéo.
*   **Subnets spécifiques mentionnés :**
    *   *Subnet 9 :* Modèles de langage décentralisés (LLM).
    *   *Subnet 19 :* Génération d'images par IA.
    *   *Subnet 25 (Protein Folding) :* Calcul scientifique pour la recherche médicale sur le repliement des protéines.
    *   *Subnet 51 (Compute) :* Location décentralisée de puissance de calcul GPU/CPU.
*   **Projets, applications et fonds tiers cités :**
    *   *Corcel, Corcel/Macrocosmos :* Applications utilisant les Subnets Bittensor.
    *   *Digital Currency Group (DCG) / Barry Silbert / Yuma :* Investisseurs et incubateurs de Subnets.
    *   *Grayscale, Polychain Capital, Pantera Capital :* Fonds d'investissement positionnés sur l'écosystème.
    *   *Angle Protocol :* Précédent projet DeFi mentionné par l'intervenant.
    *   *Kaggle :* Plateforme Web2 citée à titre de comparaison pour la recherche collaborative en Data Science.
*   **Nature de la vidéo :** Interview informative et éducative organisée par Cryptoast ; promotion des services de MantaMinds par son cofondateur (non identifiée comme publicité payée explicite).
