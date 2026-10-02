# Comment je MULTI-task avec Codex (worktree, type de développeur et optimisation)

Vidéo : https://youtu.be/XVxVU3lilrk · durée 21:27 · résumé Gemini (gemini-3.8-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
Pour un développeur indépendant, freelance ou créateur de SaaS (*indie hacker*), la compétence clé pour démultiplier sa productivité (et donc son potentiel de revenus) est le **multitâche assisté par IA**. 

Plutôt que de superviser manuellement un seul agent ligne par ligne, l'auteur explique comment lancer **5 à 10 agents IA en parallèle** sur différentes fonctionnalités ou corrections de bugs. Pour que cela fonctionne sans perte de temps, la relecture manuelle du code et les tests humains dans le navigateur sont remplacés par des workflows complets où **les agents fournissent des preuves visuelles (captures d'écran)** et s'auto-vérifient avant intégration.

---

### 2) Outils, sites et dépôts cités

* **Codex** : Interface/application de développement agentique affichée tout au long de la vidéo pour gérer les sessions de chat, les agents en parallèle et exécuter du code (Claude / Cursor / Grok). *(Statut : Payant via abonnements ou crédits API)*.
* **Git / Git Worktree** : Fonctionnalité native de Git permettant de cloner/traiter plusieurs branches simultanément dans des répertoires séparés. Sert à isoler les gros chantiers de refactorisation. *(Statut : Gratuit / Open source)*.
* **Excalidraw (`app.excalidraw.com`)** : Application de tableau blanc virtuel utilisée pour schématiser les flux d'agents et l'organisation des branches. *(Statut : Gratuit avec options payantes)*.
* **GitHub & Pull Requests** : Plateforme d'hébergement de code et gestion des revues de code/PR. *(Statut : Gratuit / plans payants)*.
* **Vercel** : Plateforme d'hébergement web utilisée pour générer automatiquement des déploiements de prévisualisation (*preview deployments*) à chaque push pour valider le rendu en ligne. *(Statut : Freemium / Payant)*.
* **Playwright / Chrome sans tête (Headless / Dev)** : Outils d'automatisation de navigateur utilisés par les agents IA pour charger l'application locale, reproduire des actions et prendre des captures d'écran. *(Statut : Gratuit / Open source)*.
* **shadcn/ui** : Bibliothèque de composants React citée lors d'une tâche de refactorisation de composant chat. *(Statut : Gratuit / Open source)*.
* **Next.js** : Framework web React mentionné lors des tests sur serveur de dev local (`localhost:3002`). *(Statut : Gratuit / Open source)*.
* **Lumail (`lumail.io`)** : Application SaaS de l'auteur servant d'exemple dans la vidéo (plateforme d'emailing/newsletters gérée par agents IA). *(Statut : Payant)*.
* **Formation AI Blueprint (`mlv.sh/ia` ou `mlv.sh/fa`)** : Lien vers la page de capture de l'auteur proposant un modèle de configuration d'agents IA et des cours. *(Statut : Inscription gratuite par e-mail, formations payantes associées)*.

---

### 3) Astuces concrètes et réutilisables

1. **Remplacer le test manuel par le skill de « Preuve visuelle » (Verify) :**
   * Ne perdez pas de temps à ouvrir le navigateur et cliquer vous-même à chaque modification.
   * Ordonnez à l'agent de lancer un navigateur automatisé, d'exécuter le parcours utilisateur et de générer une galerie de captures d'écran (*Evidence Gallery* avec statuts PASS/FAIL).
2. **Itérer uniquement sur la base des screenshots :**
   * Consultez directement les images produites par l'agent dans le chat. Si le résultat ne convient pas (alignement, design, style SVG), renvoyez immédiatement une consigne textuelle de correction (*follow-up*) sans toucher au code.
3. **Faire « dépenser » l'agent pour fiabiliser le code :**
   * Un agent qui termine en 1 minute produit souvent un travail médiocre et vous force à faire du babysitting.
   * Imposez un pipeline rigoureux en 5 étapes : **Exploration/Analyse** $\rightarrow$ **Planification** $\rightarrow$ **Exécution** $\rightarrow$ **Examen de code (sous-agents)** $\rightarrow$ **Vérification**.
4. **Gestion des branches et Worktrees :**
   * Évitez de créer un *worktree* par tâche/agent sous peine d'un enfer de conflits de fusion (*merge conflicts*).
   * Faites converger la majorité des petites tâches sur **une seule branche commune** rattachée à une seule Pull Request globale, et réservez les *worktrees* uniquement aux refactorisations lourdes et indépendantes (ex. refonte complète d'un système).
5. **Adapter son budget API au parallélisme :**
   * Les abonnements standards à 20 $/mois sont rapidement saturés. Pour faire tourner 5 à 10 agents simultanés avec des phases de vérification et sous-agents, il faut prévoir un budget API plus élevé (100 $/mois ou plus).

---

### 4) Chiffres de revenus annoncés

* **Revenus personnels ou gains d'argent précis annoncés :** **Non précisé** *(affirmé par l'auteur : aucun montant de chiffre d'affaires ou de gain financier direct n'est dévoilé dans cette vidéo, l'auteur illustre uniquement l'effet de levier en productivité et mentionne des pertes potentielles pour de grosses entreprises en cas d'erreur de 10 000 € à 1 000 000 €)*.
