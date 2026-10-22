# Claude Now Does Video (FOR FREE) Thanks To JavaScript (Chase AI)

Vidéo : https://youtu.be/rscb1DgJtNg · résumé Gemini (gemini-3.8-flash) du 2026-10-07, envoyée par l'utilisateur
(connaissances générales, non vérifiées : tout chiffre ou prix est à contrôler à la source officielle)

### 1) Idée principale
Créer des vidéos d'animation et de motion design professionnelles entièrement programmées en JavaScript (HTML5 Canvas) grâce à **Claude Code**, sans recourir aux logiciels d'animation classiques (After Effects, Remotion) ni aux générateurs vidéo IA conventionnels coûteux. 

Le principe repose sur une fonction mathématique $frame(t)$ : le code calcule chaque image pour un instant $t$ donné (ex. 60 images par seconde). Claude Code lance un navigateur sans interface (*headless browser*) pour prévisualiser les images, analyse les éventuels défauts, corrige son code en boucle autonome, et assemble le résultat final en fichier MP4 avec FFmpeg.

---

### 2) Outils, logiciels, sites et dépôts cités

1. **Claude Code (Anthropic)**
   * **Statut :** Payant (facturation à l'usage des tokens de l'API Anthropic / abonnement).
   * **Rôle :** Agent de développement en ligne de commande qui écrit le code JavaScript, pilote les outils locaux, inspecte visuellement les images et corrige les bugs.
2. **JavaScript / Canvas HTML5**
   * **Statut :** Gratuit / Open source standard.
   * **Rôle :** Moteur graphique procédural dans lequel chaque image de la vidéo est dessinée.
3. **Playwright**
   * **Statut :** Gratuit / Open source.
   * **Rôle :** Navigateur Chromium headless automatisé permettant à Claude d'exécuter le script JavaScript en arrière-plan et de capturer les différentes frames.
4. **FFmpeg**
   * **Statut :** Gratuit / Open source.
   * **Rôle :** Outil en ligne de commande servant à générer les planches de contact de vérification (*contact sheets*) et à assembler l'ensemble des images et l'audio en fichier vidéo MP4 final.
5. **Dépôt GitHub `cbh991/animate`**
   * **Statut :** Gratuit / Open source (licence MIT).
   * **Rôle :** « Skill » pour Claude Code conçu par l'auteur. Il structure tout le cycle de production (questions de cadrage, scénario, validation de style, storyboard, compilation, rendu et vérification) avec 8 styles prédéfinis ou sur mesure.
6. **ElevenLabs**
   * **Statut :** Payant (l'auteur mentionne environ 5 $/mois ; offre gratuite limitée existante mais non précisée dans le détail).
   * **Rôle :** Génération de la voix off par synthèse vocale IA.
7. **Whisper / Faster-Whisper (Python)**
   * **Statut :** Gratuit / Open source.
   * **Rôle :** Transcription audio mot à mot avec horodatage (*timestamps*) précis pour synchroniser les animations au rythme exact de la voix.
8. **Skilry (`skilry.dev`)**
   * **Statut :** Freemium / Payant (aperçu gratuit ; abonnements affichés à l'écran : 9,99 $/mois, 79 $/an ou 169 $ à vie).
   * **Rôle :** Bibliothèque de vidéos d'animation faites par IA avec leurs prompts et styles pour trouver l'inspiration.
9. **Compte X (Twitter) de Kevin Ngo (`@kevin_ngo`)**
   * **Statut :** Gratuit.
   * **Rôle :** Profil de référence recommandé pour s'inspirer de créations avancées en *creative coding* / JavaScript Canvas.
10. **Adobe After Effects & Remotion**
    * **Statut :** After Effects est payant ; Remotion est open source / freemium.
    * **Rôle :** Outils traditionnels cités en début de vidéo pour préciser qu'ils ne sont **pas nécessaires** avec cette méthode.
11. **Chase AI+** (Communauté / Plateforme de l'auteur)
    * **Statut :** Payant (tarif non précisé dans la vidéo).
    * **Rôle :** Formations / masterclasses sur Claude Code, Codex et système "Jarvis / Astra".

---

### 3) Astuces concrètes et réutilisables

* **Exiger un storyboard avant tout codage lourd :** Demander d'abord à Claude de générer une planche de storyboard (quelques images clés représentatives des moments charnières / *beats*). Cela évite de gaspiller du temps et des tokens à générer une vidéo complète si la direction visuelle ne convient pas.
* **Le workflow « Audio-first » :** Générer d'abord la voix off (ElevenLabs), extraire les timestamps précis de chaque mot avec Whisper, puis donner ce fichier à Claude pour qu'il synchronise les déclenchements graphiques sur le rythme de la parole.
* **Boucle d'auto-évaluation en boucle fermée (*Feedback loop*) :** Intégrer dans le prompt la consigne formelle d'exporter une planche contact avec FFmpeg, d'analyser les frames via Playwright (ex. texte coupé, élément qui déborde) et de corriger le code avant de livrer la version finale.
* **Fournir une vidéo de référence pour le style :** Donner à Claude une vidéo existante ou des captures d'écran en lui demandant d'en copier la composition, la palette et le style typographique tout en créant un sujet totalement neuf.
* **Optimiser le temps de génération :** Un niveau d'effort basique ("low") produit déjà une vidéo solide en une vingtaine de minutes, tandis qu'un niveau très poussé ("ultracode") peut tourner pendant 8 heures pour un gain marginal. La précision du prompt initial prime sur la durée de réflexion brute.

---

### 4) Chiffres de revenus annoncés

* **Chiffres de revenus / gains financiers :** non précisé (aucun montant de gain ou de chiffre d'affaires n'est annoncé ou promis par l'auteur dans la vidéo).
