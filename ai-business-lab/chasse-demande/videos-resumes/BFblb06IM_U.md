# BFblb06IM_U — « Comment créer 40 annonces IA avec FABLE 5.2 et Claude Code »

- Auteur : Novoads  ; lien : https://youtu.be/BFblb06IM_U
- Envoyée par l'utilisateur ; résumée le 17/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (17/11)

- **Écarté** : service payant (NovoAds, crédits à partir de 15 $/mois selon l'auteur) et publicités pour boutiques en ligne ; DIG16 n'a pas de budget publicitaire.
- **Déjà appliqué chez nous** : montrer d'abord le plan (tableau style / concept / texte) et le faire valider avant de fabriquer les visuels (règle « validation d'abord »).
- **Idée gardée** : après une série, repérer le style qui a le mieux marché et décliner seulement celui-là ; rejoint l'analyse sur 90 jours prévue au bilan du 01/12 (réserve).

## Résumé (Gemini)

Voici un résumé structuré du tutoriel vidéo pour utiliser l'IA et **Claude Code** dans la création et la vente de contenus publicitaires :

---

### 1) Idée principale
L'objectif est d'automatiser la création de **campagnes de publicités statiques déclinées à grande échelle** (ex. 40 annonces uniques aux styles variés avec ou sans texte) pour des produits e-commerce. En connectant l'agent **Claude Code** à l'API de la plateforme **NovoAds**, l'utilisateur peut générer automatiquement un catalogue complet d'images publicitaires haute qualité à partir d'une simple photo de produit, prêtes à être vendues à des clients ou utilisées pour du marketing.

---

### 2) Outils, sites et dépôts GitHub cités

1. **Claude Code**
   * **Nom exact :** Claude Code (CLI / Terminal agent d'Anthropic)
   * **Modèle économique :** Payant (nécessite des crédits API Anthropic ou un abonnement Claude payant).
   * **Utilité :** Exécute les commandes, gère la structure des dossiers locaux, planifie les concepts publicitaires et orchestre la génération en masse via le terminal.

2. **NovoAds.ai**
   * **Nom exact :** `novoads.ai`
   * **Modèle économique :** Payant (système de crédits, par exemple l'offre de départ mentionnée à 15 $/mois pour 200 crédits).
   * **Utilité :** Plateforme de création d'annonces IA fournissant l'API et les clés d'accès aux modèles d'images/vidéos publicitaires.

3. **Dépôt GitHub Agent Skills NovoAds**
   * **Nom exact :** `https://github.com/novo-ads/agent-skills`
   * **Modèle économique :** Gratuit (Open Source).
   * **Utilité :** Contient le pack de compétences (« *skills* ») à installer dans Claude Code pour lui apprendre à générer des annonces automatiquement.

4. **Modèles de génération d'image IA (via NovoAds)**
   * **Noms exacts :** `gpt-image-2.6`, `nano-banana-pro`, `seedream-5-pro`.
   * **Modèle économique :** Inclus via la consommation de crédits de l'API NovoAds.
   * **Utilité :** Moteurs de rendu d'images. L'auteur recommande spécifiquement `gpt-image-2.6` pour son rendu visuel et la précision de son intégration de texte.

---

### 3) Astuces concrètes et réutilisables

* **Installation automatique de l'agent :** Dans le terminal Claude Code (en travaillant dans un dossier local), il suffit de coller le lien GitHub suivi de sa clé API NovoAds : 
  `https://github.com/novo-ads/agent-skills help me set this up key: [VOTRE_CLE_API]`
* **Placement des assets du produit :** Placez la photo du produit (ex. un paquet de gummies) dans le dossier généré : `reference/product/`.
* **Prompting structuré pour génération par lot :**
  > *"Create 40 static ads for the gummies that are in the products folder. Use different styles, some ads with text others without text. Use gpt-image-2.6"*
* **Workflow de validation :** L'agent IA commence par afficher un tableau récapitulatif (style, concept visuel, texte/slogan). Validez ce plan avant de lancer la génération pour éviter d'imprimer des images inutiles.
* **Itération par style gagnant :** Une fois le lot de 40 visuels généré, repérez le style graphique qui fonctionne le mieux et demandez à Claude Code de générer davantage de déclinaisons basées uniquement sur ce style.

---

### 4) Chiffres de revenus annoncés
* **Affirmé par l'auteur :** **Non précisé** (l'auteur présente l'outil technique et le workflow, mais n'annonce pas de chiffre d'affaires ou de revenus financiers personnels dans cette vidéo).
