# Mon Workflow CHEATÉ pour monter mes vidéos avec Opus 5.5 (Melvynx)

Vidéo : https://youtu.be/ySLnUg8xNcg · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-07, envoyée par l'utilisateur
(connaissances générales, non vérifiées : tout chiffre, prix ou licence est à contrôler à la source officielle)

### 1. Idée principale
L'auteur explique comment automatiser entièrement le montage vidéo (notamment pour les Shorts YouTube, TikTok et Instagram) en combinant **l'IA (via Claude Code)** et des moteurs de rendu web légers (comme un Canvas maison/Playwright), afin de produire rapidement du contenu de haute qualité à grande échelle, sans dépendre d'un monteur humain.

---

### 2. Outils, sites et dépôts GitHub cités
* **Claude Code** (via Anthropic)
  * *Statut* : Payant (basé sur la consommation de l'API).
  * *Rôle* : Agent IA principal qui écrit et gère le code, les styles, et orchestre le workflow d'édition.
* **Remotion**
  * *Statut* : Open source (payant pour un usage commercial/entreprise).
  * *Rôle* : Bibliothèque React de génération de vidéos par programmation.
* **HyperFrames** (hyperframes.dev)
  * *Statut* : Open source (créé par HeyGen).
  * *Rôle* : Éditeur vidéo orienté agents IA pour composer des vidéos par le code (HTML, CSS, GSAP).
* **Playwright**
  * *Statut* : Gratuit (open source).
  * *Rôle* : Utilisé en mode headless pour dessiner les composants HTML et effectuer les rendus rapidement dans un navigateur Chrome.
* **MediaPipe**
  * *Statut* : Gratuit (open source).
  * *Rôle* : Bibliothèque de traitement multimédia.

---

### 3. Astuces concrètes et réutilisables
* **Éviter les moteurs lourds (Remotion/HyperFrames) pour de l'IA simple :** Ils sont souvent overkill, consomment énormément de CPU et ralentissent les rendus. Préférer un moteur personnalisé basé sur des composants HTML/CSS rendus avec Playwright et Chrome headless.
* **Le cycle de feedback itératif :** 
  1. L'IA génère une première version brute de la vidéo.
  2. L'auteur utilise un studio de review pour ajouter des commentaires visuels précis (dessins, flèches, texte) directement sur la timeline.
  3. Il copie le prompt de feedback et le renvoie à Claude Code pour corriger et améliorer la vidéo itération par itération.
* **Centraliser les styles dans un fichier (`style.json` ou `kit.js`) :** Permet à l'IA d'avoir une cohérence graphique stricte sur toutes les vidéos (police, ombres, couleurs, etc.).
* **Cuts ultra-agressifs :** Supprimer tous les silences de la vidéo pour maximiser la rétention.
* **Accélération du rythme :** Augmenter légèrement la vitesse de lecture (x1,1 ou x1,2) pour dynamiser le contenu.
* **Parallélisation des rendus :** Lancer plusieurs instances de Chrome en parallèle pour accélérer considérablement le rendu de vidéos longues.

---

### 4. Chiffres de revenus annoncés
* **40 € par short** (*affirmé par l'auteur*) : Le montant qu'un monteur vidéo classique facturerait pour un short.
* **Revenus de shorts générés par IA sur une petite chaîne (100 abonnés)** (*affirmé par l'auteur*) : 
  * 1 100 vues
  * 1 400 vues
  * 1 200 vues
  * 100 vues
  * 216 vues
  * 26 vues
  * 180 vues
  * 94 vues
  * 923 vues
  * 73 vues
  * 1 185 vues (pour une vidéo spécifique « Je sors mon chapeau de martien »)
  * 164 vues (version sans le montage IA)
