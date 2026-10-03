# I Fired my Video Editor... and Hired Claude Instead (RAW RESULTS) (vidéo YouTube 68v_T0jrysM, chaîne Albert Olgaard)

Source envoyée le 30/09/2026 : https://youtu.be/68v_T0jrysM — résumé Gemini (gemini-3.6-flash) du 30/09/2026. Affirmations de l'auteur, non vérifiées.

Voici la synthèse détaillée de la vidéo :

---

### 1) Idée principale
L'auteur explique comment il a remplacé son monteur vidéo humain par un système automatisé basé sur **Claude (Claude Skills)** et une API de transcription audio. Ce workflow produit des vidéos courtes (Reels/Shorts/TikTok) à fort fort potentiel viral de manière 100 % automatique à partir de rushs bruts, augmentant considérablement l'engagement tout en réduisant les coûts de production.

---

### 2) Outils, sites et ressources cités

*   **Claude (Anthropic) / Claude Code / Claude Skills**
    *   **Modèle/Prix :** Payant (l'auteur utilise l'offre *Claude Max* à **200 $/mois**, modèle Opus).
    *   **À quoi il sert :** Il sert d'agent monteur. Il analyse les rushs, exécute le script de montage (« skill »), génère des animations en code (HTML/CSS) et effectue une boucle de contrôle qualité sur le rendu final.
*   **Fish Audio (`fish.audio`)**
    *   **Prix :** Payant à l'usage (extrêmement peu cher : ~0,07 $ pour 11 minutes d'audio).
    *   **À quoi il sert :** Fournit une transcription textuelle et un horodatage (timestamps) ultra-précis pour permettre à Claude de couper la vidéo exactement au bon moment sans créer de silences gênants ni de coupes hachées.
*   **Communauté Skool ("AI Automation A-Z") & Google Drive "Claude Skills"**
    *   **Prix :** Gratuit.
    *   **À quoi il sert :** Espace communautaire partagé par l'auteur où télécharger gratuitement le fichier de compétence Claude (`albert-reel-dark`) utilisé dans la vidéo.

---

### 3) Astuces concrètes et réutilisables

1.  **Fiabiliser le découpage avec une API de transcription dédiée :** Le défaut majeur du montage par IA provient des mauvais timestamps. Passer par une API audio externe (comme Fish Audio) garantit des coupes nettes sans pauses bizarres.
2.  **Configurer le fichier d'environnement (`.env`) :** Demandez directement à Claude dans l'interface de créer/ouvrir le fichier `.env` pour y coller votre clé `FISH_API_KEY`, garantissant la communication sécurisée entre le script et l'API.
3.  **Masser l'affichage via du code HTML/UI :** Au lieu d'utiliser des outils de montage lourds, le script demande à Claude de générer des animations visuelles en HTML/code (rendu visuel moderne/premium), domaine dans lequel l'IA excelle.
4.  **Donner une consigne créative dès l'accroche (Hook) :** Glissez vos fichiers vidéo (`.MOV`) et audio (`.WAV`), activez le skill, puis ajoutez simplement une idée visuelle en langage naturel (ex. : *"Je veux afficher un viseur de sniper au début"*).
5.  **Ajuster par boucles de feedback en langage naturel :** Si un rythme ne convient pas, revoyez la prévisualisation générée par Claude et redonnez une consigne précise (ex. : *"Reste un peu plus longtemps sur Coinbase avant de tirer quand je dis 'base'"*).

---

### 4) Chiffres et performances annoncés (*affirmés par l'auteur*)

*   **Revenus du business de l'auteur :** Plus de **100 000 $/mois**.
*   **Vues Instagram globales :** **16,3 millions de vues** sur les 30 derniers jours grâce aux Reels montés par l'IA.
*   **Coûts d'utilisation :**
    *   Abonnement Claude Max : **200 $/mois**.
    *   Transcription Fish Audio : **0,07 $** pour ~11,4 minutes d'audio.
    *   Consommation de ressources : Un montage complet prend environ 30 minutes de traitement et consomme entre 1 % et 3 % de sa limite hebdomadaire Claude.
*   **Comparatif des vues par vidéo (Avant vs Après) :**
    *   *Avant (montage classique) :* ~12,7K à 27,4K vues par vidéo.
    *   *Après (montage 100 % IA) :* **106K**, **126K**, **262K** et jusqu'à **314K** vues par vidéo.
