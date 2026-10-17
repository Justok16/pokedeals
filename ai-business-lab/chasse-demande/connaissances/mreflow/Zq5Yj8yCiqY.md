# 30+ effets visuels par IA pour transformer des vidéos simples en pure magie

Vidéo : https://youtu.be/Zq5Yj8yCiqY · durée 29:37 · résumé Gemini (gemini-3.6-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé complet et structuré de la vidéo en français :

---

### 1) Idée principale
La vidéo explique comment utiliser divers outils d'intelligence artificielle (générateurs vidéo, modèles de langage et assistants de code comme **Claude Code**) pour créer des effets visuels (VFX), des intros dynamiques, des transitions de lieu, du B-roll de présentation de site web, des métamorphoses et des habillages graphiques (logos animés, *lower thirds*). L'objectif est d'améliorer la qualité et l'engagement de ses propres contenus vidéo (ou pour des clients) de manière légale et professionnelle, sans avoir à maîtriser des logiciels complexes comme After Effects.

---

### 2) Liste des outils, sites et compétences cités

*   **DaVinci Resolve**
    *   **Statut** : Gratuit (version Studio payante optionnelle).
    *   **Usage** : Logiciel de montage vidéo principal. Utilisé pour capturer des images fixes (*stills*), faire du dérochage, enregistrer la voix off, appliquer des transitions d'atténuation (*Smooth Cut*) et supprimer les fonds verts (*Delta Keyer* dans la page Fusion).
*   **Runway**
    *   **Statut** : Payant (freemium / crédits).
    *   **Usage** : Plateforme de génération vidéo IA. Utilisée pour animer des transitions entre deux images fixes (*Keyframing* début/fin) et pour la synchronisation labiale d'images fixes à partir d'un fichier audio (*Character Script to Video*).
*   **Seedance (2.0 / Mini / Fast par ByteDance)**
    *   **Statut** : Payant (via crédits sur plateformes IA).
    *   **Usage** : Modèle vidéo multimodal performant pour créer des métamorphoses (*morphing*), des transitions dynamiques et des habillages de bas d'écran (*lower thirds*).
*   **Kling (Kling 3.0 / O3 / Turbo par Kuaishou)**
    *   **Statut** : Freemium / Payant selon la plateforme.
    *   **Usage** : Modèle vidéo IA spécialisé dans les transitions de scènes et le *keyframing* d'images.
*   **Google Veo (3 / 3.1) / Gemini Omni Flash**
    *   **Statut** : Freemium / Payant.
    *   **Usage** : Édition et génération vidéo (in-painting vidéo). Permet d'ajouter des éléments dans une vidéo existante (Yeti en arrière-plan, Godzilla, explosions, pluie, fumée sur la tête, texte géant derrière une personne).
*   **Krea.ai, Higgsfield AI, Leonardo.ai**
    *   **Statut** : Freemium / Payant.
    *   **Usage** : Plateformes génératives alternatives intégrant divers modèles d'images et de vidéos IA.
*   **ChatGPT (OpenAI / DALL-E)**
    *   **Statut** : Freemium / Payant.
    *   **Usage** : Génération d'images modifiées à partir d'un décor réel (ex. insérer un loup sur une chaise dans une pièce vide).
*   **Claude / Claude Cowork (Anthropic)**
    *   **Statut** : Payant (abonnements Pro/Max/Enterprise).
    *   **Usage** : Agent IA capable d'exécuter du code, de naviguer sur le web, de capturer des pages, d'animer le défilement et le surlignage de textes d'un article, puis d'exporter directement un fichier vidéo MP4 pour du B-roll. (*Modèles cités : Opus 4.8, Fable 5, Sonnet 5, Haiku 4.5*).
*   **Codex / Claude Code**
    *   **Statut** : Payant / Accès développeur.
    *   **Usage** : Environnement d'exécution d'agents IA permettant d'exécuter des scripts/plugins de génération graphique.
*   **Remotion / Remotion Best Practices (Skill / Plugin)**
    *   **Statut** : Gratuit / Open-source (Framework React).
    *   **Usage** : Compétence/Plugin pour Codex ou Claude Code permettant de générer par programmation du *motion design* parfait : révélations de logos par particules, animations de fausses conversations SMS, *data-visualization* (graphiques SVG animés) et *lower thirds*.
*   **NotebookLM (Google)**
    *   **Statut** : Gratuit.
    *   **Usage** : Analyse de sources/documents et génération automatique d'une synthèse vidéo animée (*Video Overview / Explainer*) utilisable comme B-roll thématique.

---

### 3) Astuces concrètes et réutilisables

1.  **Technique de transition par images clés (*Keyframing*)** :
    *   Enregistrez votre scène vidéo.
    *   Exportez la première image où le décor est vide (Frame 1) et l'image juste avant que vous ne commenciez à parler sur votre chaise (Frame 2).
    *   Chargez Frame 1 en *First Video Frame* et Frame 2 en *Last Video Frame* dans un générateur vidéo (ex. Runway/Seedance).
    *   Rédigez un prompt décrivant l'action (ex: *"The man bursts through the back wall and sits in the chair"*).
    *   Réinsérez le clip généré dans votre logiciel de montage et raccordez-le avec l'effet **Smooth Cut** de DaVinci Resolve.
2.  **Astuce anti-bafouillage dans les prompts vidéo IA** :
    *   Pour éviter que l'IA ne génère du mouvement de lèvres désordonné ou un charabia visuel à la fin d'un effet, ajoutez toujours à la fin du prompt : *"The person does not speak"* ou *"Make it so I don't react or notice it happened"*.
3.  **In-painting vidéo simple avec Gemini/Veo** :
    *   Découpez un extrait de 5 à 10 secondes de vous en train de parler.
    *   Uploadez la séquence et demandez l'ajout d'un élément (ex: *"Add an explosion behind me, don't change anything else"*). L'IA conserve votre visage et modifie uniquement l'arrière-plan.
4.  **B-roll d'article de presse avec Claude Cowork/Code** :
    *   Fournissez l'URL d'un article web à l'agent IA.
    *   Demandez-lui de créer une vidéo qui montre la page, défile jusqu'à un paragraphe clé, zoome dessus et applique un effet de surligneur jaune. L'agent écrit le code, effectue la capture et livre un fichier MP4 prêt à l'emploi.
5.  **Incrustation de Titres / Lower Thirds via Fond Vert** :
    *   Générez une animation de titre ou de sous-titre sur fond vert uni (*green screen*).
    *   Dans DaVinci Resolve (page Fusion), appliquez un nœud **Delta Keyer**, sélectionnez la couleur verte avec la pipette pour supprimer le fond et superposez l'élément sur votre vidéo principale.
6.  **Génération de Motion Design au pixel près via Code (Remotion + Claude Code)** :
    *   Les modèles vidéo classiques ont souvent du mal avec la lisibilité du texte.
    *   Utilisez la compétence **Remotion** dans Claude Code/Codex. Comme la vidéo est rendue programmatiquement en React/SVG, le texte, les sous-titres, les animations de graphiques boursiers ou les bulles de texte SMS sont parfaitement nettes.

---

### 4) Chiffres de revenus annoncés

*   **Aucun chiffre de revenu n'est mentionné** dans la vidéo (*non précisé / non applicable*). L'auteur partage ses techniques de création de contenu pour optimiser la rétention d'audience sur YouTube, sans avancer de bilan financier.
