# Reel de Julien (@julien.massey)

https://www.instagram.com/reel/DfRUPVVoPSK/ · résumé Gemini (gemini-3-flash-preview) du 2026-11-04 (affirmations non vérifiées)

Voici un résumé complet de la vidéo :

### 1) Idée principale
La vidéo explique comment créer des sites web avec des effets d'animation 3D au défilement (scroll) en utilisant l'intelligence artificielle (notamment Claude et Claude Code) en seulement 20 minutes, afin de pouvoir les revendre à un prix élevé (plus de 5 000 €).

### 2) Outils, sites, skills ou dépôts GitHub cités
*   **ChatGPT** : Utilisé pour générer deux images de produit (exemple : une montre). *Prix : non précisé dans la vidéo.*
*   **fal (fal.ai)** : Site utilisé pour l'outil **minimax/h3-max/image-to-video**. Il sert à transformer les deux images générées en une vidéo animée. *Prix : non précisé dans la vidéo.*
*   **Skill Claude** : Un "skill" spécifique pour Claude. Usage : permettre la création de sites avec scroll animé. *Prix : **Gratuit** (mentionné explicitement).*
*   **scroll-world (dépôt GitHub)** : Dépôt par l'utilisateur "monk-emils" (à vérifier sur l'image). Usage : bibliothèque ou code de base pour réaliser du scroll animé sur des sites. *Prix : gratuit (Open Source).*
*   **Claude Code** : Outil d'IA utilisé pour assembler le tout (vidéo + skill + instructions) et générer le code complet du site web. *Prix : non précisé dans la vidéo.*

### 3) Astuces concrètes
*   Générer **deux images distinctes** du même produit pour créer une transition fluide en vidéo.
*   Utiliser une IA de type "image-to-video" pour créer l'animation 3D plutôt que de la coder à la main.
*   Installer un "skill" spécifique dans Claude pour lui apprendre à manipuler les bibliothèques de scroll animé.
*   Donner des instructions textuelles précises (prompt) à Claude Code en incluant la vidéo et le skill pour qu'il construise l'architecture du site automatiquement.

### 4) Chiffres annoncés
*   **Plus de 5 000 €** (ou "5 000 balles") : Prix de vente potentiel de ce type de site.
*   **20 minutes** : Temps nécessaire pour réaliser le site présenté dans la vidéo.

### 5) Texte affiché à l'écran (listes et éléments clés)
*   "FAIRE DES SITES WEB 3D GRÂCE À CLAUDE"
*   "minimax/h3-max/image-to-video" (sur le site fal)
*   "scroll-world" (nom du dépôt GitHub)
*   Le prompt affiché sur Claude commence par : *"À partir de la vidéo et du skill que je t'ai transmis, tu vas faire un site animé avec du scroll pour faire un site qui présente cette montre..."*
*   "Commente **scroll** et je t'envoie tout le guide complet en privé"

## Vérification à la source (04/11/2026)

- Dépôt cité : **oso95/scroll-world** (github.com/oso95/scroll-world), licence MIT (fichier LICENSE lu le 04/11).
- README lu en entier le 04/11 : le skill lui-même est gratuit, mais **la fabrication des vidéos est payante** :
  Monid (Seedance 2.0, facturé à la vidéo ; « a 6-scene 1080p chain ≈ $27 » selon le README) et/ou crédits
  Higgsfield ; images via GPT Image (Higgsfield ou abonnement ChatGPT). fal.ai (montré dans le reel) est aussi payant à l'usage.
- Seule partie réutilisable à 0 € : le moteur `references/scrub-engine.js` (vidéo lue image par image au défilement, MIT),
  à coupler avec une vidéo fabriquée gratuitement sur le PC de l'utilisateur (MiniMax H3 / Wan2GP, guide
  `supports/Dig-Guide-MiniMax-H3.pdf`) ou avec les photos du client.
- « 5 000 € en 20 minutes » : affirmation de l'auteur, non vérifiée ; le reel sert à collecter des contacts (« commente scroll »).

**Tri : 📦 réserve** (budget 0 € et nouvelles démos en pause jusqu'au premier client payant). Le ressortir pour un
site Prestige ou un client qui veut un site « animé haut de gamme » : lire alors SKILL.md et scrub-engine.js en entier,
fabriquer les vidéos en local (gratuit), jamais via Monid/Higgsfield/fal sans accord de dépense de l'utilisateur.
