# Tout le monde peut désormais créer des jeux incroyables (facilement)

Vidéo : https://youtu.be/qK4nV_LnXxQ · durée 28:51 · résumé Gemini (gemini-3.6-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé détaillé de la vidéo, structuré spécifiquement pour une démarche de création de valeur et d'automatisation avec l'IA.

---

### 1) Idée principale
L'auteur démontre comment concevoir un jeu vidéo 3D complet ("The Librarian 2") en seulement quelques heures sans coder manuellement, en combinant des agents d'IA (*Claude Code* et *Codex / GPT-5.6*). 

Son objectif est double :
1. Prouver que l'IA permet de franchir le blocage technique (scaffolding, génération de 10 000+ lignes de code, assets procéduraux, correction de bugs).
2. Démontrer que **le développement de jeux n'est pas "mort" (cooked)** : si l'IA automatise l'écriture du code, la vraie valeur commerciale réside dans le *game design*, l'équilibrage, l'expérience utilisateur et l'intention créative humaine.

---

### 2) Outils, sites et dépôts GitHub cités

| Nom exact | Gratuit / Payant | À quoi il sert |
| :--- | :--- | :--- |
| **Claude Code** (avec modèle **Claude 3.5 Opus / Opus 5**) | **Payant** (Abonnement / Clé API Anthropic) | Agent IA en ligne de commande utilisé pour le *scaffolding* initial, l'écriture du code de base (10 000+ lignes), la génération procédurale et l'auto-test du jeu. |
| **ChatGPT / Codex** (avec modèles **5.6 Sol High / Sol Ultra**) | **Payant** (Abonnement ChatGPT Plus/Pro) | Agent/Environnement de dev IA d'OpenAI utilisé pour le débogage fin, l'analyse de code complexe, l'équilibrage et le peaufinage graphique. |
| **Whisper Flow** | **Non précisé** (Gratuit/Payant selon intégration) | Outil de dictée vocale vers texte utilisé pour fournir de longs cahiers des charges (prompts) à l'IA sans taper au clavier. |
| **GitHub** | **Gratuit** | Hébergement du code source, gestion de version (git), sauvegarde et partage du projet avec la communauté. |
| **Dépôt `mreflow/the-librarian-game`** | **Gratuit** | Dépôt GitHub du premier jeu 2D de l'auteur, fourni en référence à l'IA. |
| **Dépôt `the-librarian-2`** | **Gratuit** | Dépôt GitHub créé durant la vidéo contenant tout le code source du jeu 3D généré. |
| **Vercel / GPT Sites** (`the-librarian-game.vercel.app`) | **Freemium / Gratuit** | Plateforme de déploiement web pour héberger le jeu en HTML5/JS afin qu'il soit jouable gratuitement via un lien. |
| **Three.js** | **Gratuit** (Open Source) | Moteur 3D JavaScript utilisé en arrière-plan par l'IA pour générer les graphismes 3D procéduraux. |

---

### 3) Astuces concrètes et réutilisables

*   **Stratégie du changement d'agent (Scaffolding vs Finition) :**
    *   Utilisez un premier agent puissant en génération globale (**Claude Code / Opus**) pour bâtir la structure, l'architecture et les systèmes de base du projet.
    *   Passez ensuite sur un modèle spécialisé dans l'analyse et la logique (**Codex / GPT-5.6 Sol Ultra**) pour corriger les bugs subtils, régler la caméra, l'éclairage et équilibrer les paramètres.
*   **Technique du fichier miroir `DESIGN.md` (Transfert de contexte sans perte) :**
    *   Avant de changer d'outil d'IA, demandez à l'IA initiale de générer un fichier `DESIGN.md` ultra-détaillé décrivant l'architecture complète, la logique métier, les formules mathématiques et la liste des bugs.
    *   Fournissez ce fichier au nouvel outil (ex: Codex) pour qu'il comprenne immédiatement l'intégralité du projet sans halluciner ni casser le code existant.
*   **Développement 100% procédural ("Zero-Asset") :**
    *   Demandez à l'IA de générer l'ensemble des graphismes, textures, modèles 3D (Three.js), sons et musiques **directement par du code** au démarrage de l'application. Cela évite d'avoir à créer ou acheter des fichiers multimédias externes.
*   **Auto-tests et rééquilibrage automatisés par l'IA :**
    *   L'agent IA peut exécuter le jeu localement (`npm run dev`), lancer un navigateur headless, simuler des parties avec des bots, détecter les plantages (logs d'erreur) et ajuster lui-même la difficulté (ex: baisser la vitesse des ennemis ou augmenter le temps de recharge).
*   **Prompting multimodal (Image vers modèle 3D) :**
    *   Pour ajouter un personnage personnalisé, fournissez une image/miniature à l'IA et demandez-lui d'analyser les traits visuels (casquette, barbe, chemise) pour générer les blocs de code et textures 3D correspondants.

---

### 4) Chiffres de revenus annoncés

*   **Revenus générés par le jeu :** **Aucun** (*affirmé par l'auteur*).
    *   L'auteur précise explicitement qu'il n'a pas l'intention de vendre le jeu ni de le publier sur Steam. Le projet est distribué gratuitement en open-source sur GitHub.
*   **Temps de développement économisé :** Le prototype 3D jouable (~10 400 lignes de code, 33 modules) a été généré en **1 h 30** par Claude Code, suivi de **30 minutes** de finition sous Codex.
