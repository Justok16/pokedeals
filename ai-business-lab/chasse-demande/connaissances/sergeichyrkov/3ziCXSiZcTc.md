# Claude Opus 5.5 — Motion Design and 3D Worlds (Sergei Chyrkov)

Vidéo : https://youtu.be/3ziCXSiZcTc · résumé Gemini (gemini-flash-latest) du 2026-10-07, envoyée par l'utilisateur
(connaissances générales, non vérifiées : tout chiffre, prix ou licence est à contrôler à la source officielle)

### 1) L'idée principale
Au lieu d'utiliser des modèles de génération vidéo IA traditionnels (souvent imprécis ou difficiles à contrôler), l'approche consiste à utiliser **Claude Code** pour **générer directement du code** (via des frameworks comme **Remotion** et **Three.js**). 
Ce code compile ensuite soit en **vidéos MP4 haute définition parfaitement contrôlables** (animations d'interfaces, présentations de produits, pitch decks Figma), soit en **expériences web 3D interactives** (boutiques virtuelles, visualisations 3D). Pour un prestataire ou un créateur, cela permet de produire en quelques minutes des livrables de motion design et d'expériences 3D interactives habituellement longs et coûteux à réaliser.

---

### 2) Outils, sites et dépôts cités

1. **Claude Code / Modèle Claude Opus** *(mentionné ironiquement/en avance comme « Opus 5.5 » dans la vidéo)*
   * **Tarif :** Payant (accès via abonnement Anthropic ou clés API).
   * **Utilité :** Agent de développement IA qui lit les consignes, structure le projet, écrit le code React/TypeScript/Three.js et gère les dépendances en ligne de commande.
2. **Remotion**
   * **Tarif :** Gratuit / Open-source (licence commerciale payante pour les grandes entreprises selon leur modèle, non précisé en détail dans la vidéo).
   * **Utilité :** Framework React permettant de créer des vidéos programmatiques et des animations de motion design image par image, rendues ensuite au format MP4.
3. **Three.js**
   * **Tarif :** Gratuit / Open-source.
   * **Utilité :** Bibliothèque JavaScript WebGL pour concevoir des mondes 3D interactifs dans le navigateur (lumières, caméras, maillages, contrôles clavier/souris).
4. **Figma**
   * **Tarif :** Freemium (version gratuite avec options payantes).
   * **Utilité :** Outil de design d'interface. L'auteur fournit un lien de présentation Figma à Claude pour que celui-ci convertisse automatiquement les maquettes en vidéo animée rythmée.
5. **Vite & npm**
   * **Tarif :** Gratuit / Open-source.
   * **Utilité :** Outils d'environnement de développement et gestionnaire de paquets JavaScript recommandés par l'auteur pour assembler les projets web rapidement.
6. **Vercel** *(mentionné via l'URL `3d-boutique.vercel.app`)*
   * **Tarif :** Freemium.
   * **Utilité :** Hébergement et mise en ligne en un clic de l'application web 3D interactive.
7. **Monlio (`monlio.app`)**
   * **Tarif :** Présenté comme gratuit avec option d'abonnement intégrée (application personnelle de l'auteur).
   * **Utilité :** Exemple d'application financière dont Claude a extrait le contenu pour concevoir une vidéo promotionnelle automatisée.
8. **After Effects / Final Cut** *(cités en comparaison)*
   * **Tarif :** Payants.
   * **Utilité :** Outils de montage et motion design classiques, cités pour souligner le gain de temps obtenu grâce à Claude Code.

---

### 3) Astuces concrètes et réutilisables

* **Choisir la bonne technologie selon le livrable :**
  * **Remotion** pour les vidéos linéaires : pitch decks, vidéos explicatives de produits SaaS, animations de posts réseaux sociaux, transitions d'écrans.
  * **Three.js** pour les expériences spatiales et interactives : boutiques e-commerce 3D, configurateurs d'objets, mini-jeux promotionnels.
  * **Hybride (Remotion + Three.js) :** Intégrer un rendu Three.js au sein d'une composition Remotion pour créer une publicité vidéo montrant un produit 3D tournant sous plusieurs angles.
* **Structurer un cahier des charges textuel (Prompt MVP) :**
  * Définir la stack technique souhaitée (`Three.js`, `Vite`, `React`, `HTML/CSS`).
  * Définir les interactions souhaitées (ex. : contrôles FPS `WASD` / `ZQSD`, `Pointer Lock API` pour la souris, système de panier/essayage virtuel).
  * Laisser Claude poser des questions de clarification sur la direction artistique (couleurs néon, style brutaliste/minimaliste, assets procéduraux) avant de lancer l'écriture.
* **Transformer une présentation Figma en vidéo commerciale en 5 à 10 minutes :**
  * Partager l'URL du fichier Figma directement dans Claude Code.
  * Spécifier le timing (ex. : 1 minute totale, 4 secondes par slide, format 16:9 en 4K ou 1080p).
  * Demander l'animation automatique des composants SVG et l'ajout d'une piste audio/effets sonores.

---

### 4) Chiffres de revenus annoncés

* **Revenus financiers générés :** **Non précisé** (l'auteur ne mentionne aucun chiffre de revenus ni montant en dollars gagné directement avec ces méthodes).
* **Gains de productivité :** L'auteur affirme qu'une vidéo de démo produit qui lui prenait habituellement « plusieurs heures voire 1 à 2 jours » sur After Effects ou Final Cut a été réalisée en **5 à 10 minutes** avec cette méthode *(affirmé par l'auteur)*.
