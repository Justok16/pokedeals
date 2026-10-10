# YKFpSe28mlg — Montage vidéo et motion design par le code avec Claude Code

Vidéo envoyée par l'utilisateur le 30/09/2026 : https://youtu.be/YKFpSe28mlg
Résumé automatique (Gemini, 30/09/2026). Prix des outils et chiffres de revenus : **affirmés par l'auteur, non vérifiés**.

### 1) Idée principale
L'auteur démontre comment utiliser **Claude Opus 5.5** et **Claude Code** pour devenir un monteur vidéo et motion designer "augmenté". L'idée n'est pas d'utiliser des modèles de génération vidéo (type Sora), mais de demander à Claude de **générer du code** (JavaScript, SVG, Three.js) pour manipuler des médias et créer des vidéos professionnelles. Cette approche permet de créer des contenus complexes (showreels, publicités, tutoriels) seul et beaucoup plus rapidement qu'avec des méthodes traditionnelles.

### 2) Outils, sites et dépôts cités

*   **Claude Opus 5.5 (Anthropic)** : Modèle d'IA utilisé pour le raisonnement et la génération de code. *Prix : Payant (abonnement Pro ou via API).*
*   **Claude Code** : Interface en ligne de commande (CLI) d'Anthropic pour interagir directement avec les fichiers et exécuter des tâches de code. *Prix : Non précisé (généralement lié à l'usage API).*
*   **Three.js** : Librairie JavaScript pour la 3D sur le web. *Prix : Gratuit (Open source).* Utilisé pour les éléments 3D des vidéos.
*   **FFmpeg** : Outil de traitement vidéo utilisé par l'IA pour assembler les frames et l'audio. *Prix : Gratuit (Open source).*
*   **SVG (Format)** : Recommandé pour les icônes et diagrammes car Claude peut les éditer et les animer directement par le code. *Prix : Gratuit.*
*   **Remotion / Hyperframes** : Bibliothèques de montage vidéo par le code. *Prix : Gratuit (Open source).* Citées comme alternatives populaires pour le montage via Claude.
*   **Rubric (getrubric.app)** : Outil en version bêta développé par l'auteur pour gérer le storyboard et donner des feedbacks précis à l'IA sur la timeline vidéo. *Prix : Non précisé (Bêta).*
*   **RoboNuggets (sur Skool)** : Communauté et plateforme de formation de l'auteur ("Agents-as-a-Service"). *Prix : Payant.*
*   **Excalidraw** : Utilisé dans la vidéo pour schématiser les processus de travail. *Prix : Gratuit (version de base).*

### 3) Astuces concrètes et réutilisables

*   **Privilégiez le format SVG** : Contrairement aux images classiques (raster), demandez à Claude de créer des icônes en SVG. Cela permet à l'IA de changer les couleurs ou d'animer les formes selon vos besoins sans perte de qualité.
*   **Centralisez vos instructions** : Utilisez un seul fichier `AGENTS.md` à la racine de votre projet pour synchroniser les instructions entre différents agents de code (Claude Code, Cursor, etc.).
*   **Travaillez par étapes (Les 3 Niveaux)** :
    *   *Niveau 1 (One-shot) :* Une seule commande pour tester une idée ou créer un portfolio rapidement.
    *   *Niveau 2 (Storyboarding) :* Demandez d'abord une série d'images fixes (storyboard) avant de lancer le rendu final pour économiser des tokens et du temps de calcul.
    *   *Niveau 3 (Directing) :* Donnez des feedbacks horodatés (ex: "à 2,5s, change la couleur du texte") pour peaufiner le résultat.
*   **Le code plutôt que les pixels** : Pour un rendu professionnel, ne demandez pas à l'IA de "dessiner" la vidéo, mais de générer le code (HTML/CSS/JS) qui créera le mouvement.

### 4) Chiffres de revenus (Affirmé par l'auteur)

L'auteur présente des témoignages de membres de sa communauté ayant obtenu les résultats suivants :
*   Un contrat de **30 000 $** pour le développement d'une application mobile via des agents.
*   Un premier client à **2 000 $** pour la création d'un agent, complété par un abonnement de **500 $ par mois**.
*   Un projet spécifique livré pour un montant de **40 000 $**.
