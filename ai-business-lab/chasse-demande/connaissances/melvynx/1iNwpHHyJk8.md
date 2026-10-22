# Comment j'utilise VRAIMENT Claude Code (après 300+ jours)

Vidéo : https://youtu.be/1iNwpHHyJk8 · durée 1:20:43 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, adapté à votre demande :

---

### 1. Idée principale
La vidéo présente comment optimiser l’utilisation de **Claude Code** (outil d’IA pour les développeurs) pour coder efficacement, automatiser la création d’applications, éviter les erreurs de l’IA, et gérer des projets de manière professionnelle afin de maximiser sa productivité et potentiellement ses revenus de développeur (freelance, création de SaaS, etc.).

---

### 2. Outils, sites et dépôts GitHub cités

*   **Claude Code**
    *   **Coût :** Gratuit (version Free) ou payant (Pro à 17$, Max à 100$ ou 200$).
    *   **Utilité :** Assistant de code IA en ligne de commande pour générer, déboguer et gérer des projets logiciels.
*   **Excalidraw** (`app.excalidraw.com`)
    *   **Coût :** Gratuit.
    *   **Utilité :** Outil de dessin/schématisation utilisé dans la vidéo pour illustrer les concepts et les graphiques de limites.
*   **Luma** (`lumal.io`)
    *   **Coût :** Non précisé (service en ligne).
    *   **Utilité :** Application de newsletter créée par l'auteur.
*   **CodeLine**
    *   **Coût :** Non précisé.
    *   **Utilité :** Application pour héberger et proposer des formations créée par l'auteur.
*   **Savile** (`savile.now`)
    *   **Coût :** Non précisé.
    *   **Utilité :** Projet de l'auteur géré en parallèle avec Claude Code.
*   **Ghostty** (`mitchellh/ghostty` ou site officiel)
    *   **Coût :** Gratuit (open-source).
    *   **Utilité :** Terminal moderne et minimaliste (utilisé sur macOS/Linux).
*   **MLV.sh / FC** (`mlv.sh/fc`)
    *   **Coût :** Gratuit / Configuration partagée.
    *   **Utilité :** Page de configuration/raccourcis et kit de démarrage pour configurer Claude Code en 10 secondes.
*   **CleanShot X**
    *   **Coût :** Payant (logiciel macOS).
    *   **Utilité :** Outil de capture d’écran et d’annotation pour envoyer des images à Claude Code.
*   **Thumbl.st** (`thumbfa.st`)
    *   **Coût :** Non précisé (SaaS de miniatures YouTube).
    *   **Utilité :** Boilerplate / SaaS créé par l'auteur pour générer des miniatures YouTube.
*   **Notest** (`nautes.app`)
    *   **Coût :** Non précisé (boilerplate).
    *   **Utilité :** Boilerplate / SaaS utilisé comme base pour coder de nouvelles applications avec l'IA.
*   **Tmux**
    *   **Coût :** Gratuit (open-source).
    *   **Utilité :** Multiplexeur de terminal pour exécuter et gérer plusieurs sessions de Claude Code en parallèle.

---

### 3. Astuces concrètes et réutilisables

*   **Choix de l’abonnement selon l’usage :**
    *   *Free* : Pour un usage très modéré.
    *   *Pro ($17)* : Pour un usage quotidien standard.
    *   *Max ($100 - $200)* : Indispensable pour un usage intensif (création de multiples SaaS, gestion de projets lourds), offrant jusqu'à 20x plus d'usage et évitant de saturer les limites (*Daily Limits* et *Session Limits* de 4h).
*   **Gestion du contexte et des erreurs :**
    *   Utiliser la commande `/clear` pour réinitialiser le contexte et éviter l'effet "perdu au milieu".
    *   Ajouter des fichiers de règles et de documentation (`CLAUDE.md`, dossiers `rules/`, `docs/`) pour donner un cadre strict à l'IA et éviter les erreurs de style ou de structure.
*   **Méthodes de prompt et de debug :**
    *   **Méthode Apex :** Pour des fonctionnalités générales et modulaires avec un taux de réussite très élevé (>99%).
    *   **Méthode Oneshot :** Pour des mini-fonctionnalités rapides sans prise de tête.
    *   **Méthode Debug (Logs & Screenshots) :** Envoyer des captures d’écran via CleanShot X ou exiger l’ajout de logs techniques (*Log Technique Reference*) pour que l'IA comprenne et résolve d’elle-même les bugs complexes.
    *   **Continuous Learning :** Expliquer itérativement à l'IA les erreurs commises et lui demander d'ajouter des règles persistantes dans `CLAUDE.md` pour qu'elle ne les reproduise plus.
*   **Multitasking avec Tmux :**
    *   Lancer plusieurs terminaux multiplexés avec Tmux pour travailler simultanément sur plusieurs projets ou fonctionnalités sans bloquer son flux de travail.

---

### 4. Chiffres de revenus annoncés (affirmés par l'auteur)
*   **Aucun chiffre de chiffre d'affaires ou de bénéfice net précis n'a été affirmé** concernant les gains financiers des applications présentées. Les seuls chiffres mentionnés sont les coûts des abonnements Claude Code ($17, $100, $200) et des équivalences de consommation en API (ex. : $160 à $3'200 d'équivalence de requêtes selon les plans).
