# oghx90Kr2H4 — « Ces VIDÉOS ANIMÉS Claude ont ENVAHI les réseaux, je te montre comment faire ! »

- Auteur : Labo Des Réseaux ; lien : https://youtu.be/oghx90Kr2H4
- Envoyée par l'utilisateur ; résumée le 17/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (17/11)

- **Déjà en place** : nos vidéos « Le conseil » sont faites exactement ainsi (animation HTML filmée image par image avec Playwright, assemblage FFmpeg, voix Gemini « Algieba » gratuite) ; Three.js et Remotion déjà dans l'inventaire.
- **Vérifié à la source le 17/11** : `lemomo-ai/lemo-opuscar` (17 282 étoiles, actif le 12/11) : 66 styles d'animation ; code sous MIT, documentation CC BY-NC 4.0, et « les films faits avec la bibliothèque sont à vous, commerciaux compris, sans mention obligatoire » (README et LICENSE lus) ; `mromidev/claude-animated-shorts` (MIT, 3 733 étoiles, actif le 01/11).
- **Mis en réserve** (`connaissances/reserve-prete.md`, événement « vidéo ») : à installer et lire en entier à la reprise des nouvelles vidéos, c'est-à-dire après le premier client payant (pause en vigueur), ou pour la vidéo d'un client.
- **Écarté** : ElevenLabs (payant au-delà de l'essai, voix gratuite non commerciale ; notre voix Gemini suffit et est validée par l'utilisateur).

## Résumé (Gemini)

Voici le résumé structuré de la vidéo, rédigé pour une personne souhaitant exploiter ces méthodes pour créer du contenu vidéo et générer des revenus avec l'IA.

---

### 1) Idée principale
La vidéo explique comment créer gratuitement et de manière autonome des vidéos d'animation en *motion design* (format court pour Shorts/Reels/TikTok) grâce à l'IA **Claude** (et ses fonctionnalités de code/skills), sans acheter de formation payante. L'auteur présente une méthode stratégique basée sur le choix d'une niche précise et détaille 3 approches techniques de création (Débutant, Intermédiaire, et Avancé/Sur-mesure).

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude (par Anthropic)**
    *   *Statut* : Gratuit / Payant (Abonnement Pro requis pour les modèles avancés comme Sonnet 5.5 / Opus 3.5 / Fable 5.2).
    *   *Rôle* : Écriture de scripts, création de compétences (*Skills*), génération de code d'animation (HTML/CSS/JS/Python) et rendu vidéo via Claude Code.
*   **ElevenLabs**
    *   *Statut* : Gratuit (10 000 crédits offerts par mois) puis Payant.
    *   *Rôle* : Génération de voix off synthétiques très réalistes avec gestion des émotions à partir des scripts texte.
*   **Connecteur ElevenLabs MCP (dans Claude)**
    *   *Statut* : Gratuit (nécessite un compte ElevenLabs).
    *   *Rôle* : Permet à Claude d'appeler directement l'API d'ElevenLabs pour générer la voix off sans quitter l'interface.
*   **Dépôt GitHub `lemo-opuscar` (par lemo-ai)**
    *   *Statut* : Gratuit (Open-source).
    *   *Rôle* : Skill / boîte à outils contenant 66 styles d'animation pré-codés en motion design exécutables par Claude.
*   **Dépôt GitHub `claude-animated-shorts` (par mromidev / Mr omi)**
    *   *Statut* : Gratuit (Open-source).
    *   *Rôle* : Skill permettant de créer des vidéos animées 3D/2D (reproduisant le style de la chaîne *Ricks Clips*).
*   **Three.js**
    *   *Statut* : Gratuit (Open-source).
    *   *Rôle* : Moteur 3D JavaScript permettant d'afficher et animer des scènes 3D directement dans le navigateur.
*   **Remotion**
    *   *Statut* : Gratuit (Open-source pour individuel/petite entreprise).
    *   *Rôle* : Framework React servant à programmer et calculer des rendus vidéo.
*   **FFmpeg**
    *   *Statut* : Gratuit (Open-source).
    *   *Rôle* : Outil en ligne de commande pour assembler les images, animations et l'audio dans un fichier MP4 final.
*   **Blender**
    *   *Statut* : Gratuit (Open-source).
    *   *Rôle* : Logiciel 3D (mentionné lors d'essais de génération vidéo locale par code).
*   **Higgsfield (Xfield)**
    *   *Statut* : Gratuit (avec limites) / Payant.
    *   *Rôle* : Générateur d'images/assets IA (utilisant GPT Image 2.6) servant à créer des mascottes sous plusieurs angles, des éléments découper et des décors (ex: style *Paper Craft*).
*   **Whisper (par OpenAI / Hugging Face)**
    *   *Statut* : Gratuit (Open-source).
    *   *Rôle* : Outil de retranscription audio servant à synchroniser l'animation image par image sur chaque mot prononcé.
*   **Fish Audio**
    *   *Statut* : Gratuit / Payant.
    *   *Rôle* : Alternative citée pour la génération de voix off.
*   **Ricks Clips (@RicksClips3000)**
    *   *Statut* : Chaîne YouTube (Gratuit d'accès).
    *   *Rôle* : Exemple de référence d'une chaîne accumulant des dizaines de millions de vues avec des vidéos animées.
*   **Mr omi (@mr_omix)**
    *   *Statut* : Chaîne YouTube (Gratuit d'accès).
    *   *Rôle* : Créateur ayant décomposé et partagé le code/skill pour copier le style de *Ricks Clips*.

---

### 3) Astuces concrètes et réutilisables

1.  **Structure d'un script vidéo court viral** :
    *   *0 à 3 s (Hook)* : Arrêter le scroll avec une promesse visuelle et orale forte.
    *   *3 à 8 s (Retainer/Transition)* : Donner une raison de regarder jusqu'au bout.
    *   *8 à 40 s (Corps/Valeur)* : Délivrer l'histoire de manière rythmée (changement visuel toutes les 1,5 à 2 secondes).
    *   *Fin (CTA/Boucle)* : Terminer par une phrase qui s'enchaîne parfaitement avec le tout premier mot de la vidéo pour créer une boucle infinie (*seamless loop*) et faire grimper le taux de rétention.
2.  **Stratégie de Micro-Niche en pyramide** :
    *   Niveau 1 (Sujet global) : Le football.
    *   Niveau 2 (Sous-thématique) : Histoire du foot et anecdotes.
    *   Niveau 3 (Micro-niche ciblée) : Équipe de France et clubs français.
3.  **Création de "Skills" personnalisés dans Claude** :
    *   Utiliser la fonction *Skill Creator* pour enregistrer la structure de vos prompts et règles de génération sous un mot-clé (ex: `/script-anim-foot`). Cela évite de répéter vos consignes à chaque nouveau script.
4.  **Optimisation de la voix off IA** :
    *   Les voix générées directement par le code de Claude étant de mauvaise qualité, injecter des balises d'intention dans le texte destiné à ElevenLabs (ex: `[curious]`, `[surprised]`, `[dramatic]`, `[short pause]`) pour dynamiser le rendu.
5.  **Méthode pour créer son propre style visuel unique (Méthode 3 - recommandée)** :
    *   Créer un dossier local avec des sous-dossiers : `Moteurs`, `Projets`, `Assets/Mascotte`, `Sons`.
    *   Générer votre propre mascotte sous plusieurs angles/expressions (de face, profil, dos, surpris, joyeux) et vos décors avec un outil comme Higgsfield en imposant une direction artistique précise (ex: *Paper Craft*).
    *   Laisser Claude Code découper les mascottes et gérer l'assemblage/animation par script local (Python/Remotion/FFmpeg). Cela vous protège d'être une simple « copie » d'autres chaînes.

---

### 4) Chiffres de revenus annoncés

*   **Chiffres de revenus de l'auteur** : **Non précisé** (l'auteur ne mentionne aucun montant financier gagné personnellement).
*   **Performances des chaînes citées en exemple (affirmé par l'auteur)** : La chaîne *Ricks Clips* génère entre **15 millions et 33 millions de vues** par vidéo sur ses meilleurs contenus.
