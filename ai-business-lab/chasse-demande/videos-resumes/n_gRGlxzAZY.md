# n_gRGlxzAZY — « La seule formation montage vidéo IA dont tu as besoin (21 min) »

- Auteur : Melvynx ; lien : https://youtu.be/n_gRGlxzAZY
- Envoyée par l'utilisateur le 11/11/2026 ; résumée le 11/11 par Gemini (via le relais, modèle gemini-3.5-flash-lite)
- Les prix et les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (11/11)

- **Méthode retenue pour la reprise des vidéos** (en pause jusqu'au premier client payant) : trois dossiers (`rushs`, `references`, `exports`) ; donner des vidéos de référence et des règles précises (couleurs, taille et position des sous-titres) au lieu de laisser deviner ; avancer par petites corrections.
- **Déjà en place** : FFmpeg (montage, contrôle du son) et la transcription (`faster-whisper` dans l'inventaire).
- **En réserve** : whisper.cpp (transcription locale, libre) comme solution de rechange à `faster-whisper`.
- **Écartés** : Treg (treg.to), récupération de vidéos Instagram et TikTok de tiers, à crédits : payant au-delà de l'essai et contraire à nos règles sur les contenus d'autrui ; Remotion et HyperFrames : sans usage pour l'instant.

## Résumé (Gemini)

Voici le résumé détaillé de la vidéo, structuré selon vos consignes :

### 1) Idée principale
La vidéo explique comment automatiser et améliorer le montage vidéo (pour Instagram, TikTok, YouTube Shorts) en utilisant Claude Code de manière locale, sans s'encombrer d'outils payants complexes ou de « slop » (contenu généré sans âme par l'IA). L'auteur montre comment configurer Claude Desktop, installer des outils open source comme FFmpeg et Whisper.cpp, et utiliser des prompts précis pour copier des styles de montage performants.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Desktop**
    *   **Prix :** Gratuit (version basique) / Payant (abonnements Pro à partir de 17-20 $ ou plus par mois — affirmé par l'auteur).
    *   **Rôle :** Application de bureau permettant d'exécuter Claude Code directement sur l'ordinateur de l'utilisateur pour manipuler des fichiers locaux et exécuter des tâches.
*   **Claude.ai**
    *   **Prix :** Non précisé.
    *   **Rôle :** Version web (le cloud) — mentionnée car elle ne fonctionne pas directement sur l'ordinateur pour modifier des fichiers locaux (l'auteur précise qu'il faut utiliser Claude Desktop).
*   **FFmpeg (dépôt GitHub : `FFmpeg/FFmpeg`)**
    *   **Prix :** Gratuit (Open Source).
    *   **Rôle :** Outil de traitement multimédia pour couper, coller et convertir des fichiers vidéo et audio sur l'ordinateur.
*   **Whisper.cpp (dépôt GitHub : `ggerganov/whisper.cpp`)**
    *   **Prix :** Gratuit (Open Source).
    *   **Rôle :** Outil de transcription audio pour transformer la voix en texte et générer des sous-titres précis (avec téléchargement de modèles comme `ggml-large-v3-turbo`).
*   **Treg (site : `treg.to`)**
    *   **Prix :** Freemium (Offre un crédit de départ gratuit — affirmé par l'auteur).
    *   **Rôle :** Outil d'agent intelligent (OpenRouter for agent tools) utilisé pour scraper, rechercher et télécharger des vidéos depuis Instagram ou TikTok (fournisseur de données).
*   **HyperFrames / Remotion**
    *   **Prix :** Non précisé.
    *   **Rôle :** Moteurs de rendu vidéo (cités par l'auteur comme étant trop lents ou non optimisés par rapport à sa propre solution).

---

### 3) Astuces concrètes et réutilisables

1.  **Travailler en local avec Claude Desktop :** Ne pas utiliser le site web Claude.ai, mais bien installer l'application Claude Desktop, créer un dossier dédié sur son ordinateur (ex. `montage-video`), ouvrir l'onglet code, pointer vers ce dossier en mode « This computer » (Cet ordinateur), et y coller les prompts.
2.  **Structurer son espace de travail :** Demander à Claude de créer trois sous-dossiers fondamentaux : `rushs` (prises brutes), `references` (vidéos dont on veut copier le style) et `exports` (vidéos finies).
3.  **Donner des règles précises pour éviter le "slop" :** Ne laissez pas l'IA deviner. Donnez-lui des exemples de liens vidéo (Instagram/TikTok), spécifiez vos couleurs, la taille et la position des sous-titres (ex. : sous-titres au milieu, fond noir, texte mono, couleur orange).
4.  **Itérer pas à pas :** Le montage automatisé par IA est un jeu d'itérations. Il faut tester, corriger, ajuster le niveau de "thinking" de Claude sur *High* ou *Extra High*, et lui demander de modifier les éléments jusqu'à obtenir un résultat satisfaisant.
5.  **Optimiser le moteur de rendu :** Préférer un moteur de rendu simple et optimisé directement dans le navigateur pour accélérer les itérations (au lieu de passer par des moteurs lourds comme Remotion).

---

### 4) Chiffres de revenus annoncés
*   **Affirmé par l'auteur :** Aucun chiffre de revenus monétaires précis n'a été annoncé dans la vidéo (l'auteur parle uniquement de milliers de vues générées sur ses comptes Instagram et TikTok, et du gain de 10 à 15 heures de travail grâce aux skills).
