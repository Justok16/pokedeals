# Je code 1 HEURE avec Codex devant toi (mes secrets devoilé)

Vidéo : https://youtu.be/qivtiZ3_8Ao · durée 46:17 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré et fidèle de la vidéo :

---

### 1) Idée principale
L'auteur montre comment maximiser sa productivité de développement pour construire et maintenir un SaaS rentable (ici *Thumbfa.st*) en **faisant travailler plusieurs agents IA en parallèle** dans l'application **Codex**. Plutôt que d'attendre qu'une IA termine une tâche pour lui en confier une autre, il lance simultanément 4 à 5 agents (sur différentes fonctionnalités, corrections de bugs ou refactorisations), dicte ses instructions à la voix avec des captures d'écran annotées, et laisse les agents coder, tester dans un navigateur automatisé et créer des Pull Requests (PR) sur GitHub pendant qu'il effectue des revues de code.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité |
| :--- | :--- | :--- |
| **Codex (application .codex / OpenAI Codex)** | Payant (*100 $/mois*, upgradé à *200 $/mois* avec l'app — *affirmé par l'auteur*) | Application centrale permettant d'exécuter plusieurs agents IA de codage en simultané sur différents projets et branches. |
| **Claude Code** | Payant (*100 $/mois* avec l'app — *affirmé par l'auteur*) | Outil d'agent IA de codage en ligne de commande. |
| **Cursor** | Gratuit (*tokens offerts de l'époque — affirmé par l'auteur*) | Éditeur de code assisté par IA. |
| **Zed** | Gratuit (utilisé avec l'abonnement Codex — *affirmé par l'auteur*) | Éditeur de code léger utilisé pour centraliser tous les projets, naviguer rapidement et faire tourner le terminal local. |
| **Hermes Agent + Telegram** | Gratuit / Inclus avec Codex (*affirmé par l'auteur*) | Agent IA accessible depuis Telegram pour coder à distance. |
| **Helium** | Gratuit (*navigateur*) | Navigateur web par défaut de l'auteur, choisi car il consomme très peu de batterie ; utilisé aussi pour les tests d'affichage de l'agent. |
| **Arc** | Gratuit | Navigateur web utilisé par l'auteur pour ses vidéos YouTube. |
| **Thumbfa.st** (`thumbfa.st`) | Payant (SaaS commercial de l'auteur) | SaaS développé dans la vidéo, servant à générer des miniatures YouTube par IA à partir d'inspirations. |
| **Convex** | Non précisé (Freemium dans les faits) | Solution de backend temps réel et base de données utilisée par le SaaS (avec le CLI Convex). |
| **Stripe** | Payant (commission par transaction) | Passerelle de paiement pour configurer les périodes d'essai gratuit (*free trial*) et les abonnements récurrents. |
| **Playwright / DevBrowser** | Gratuit (*open source*) | Outil de test automatisé permettant à l'agent IA d'ouvrir un navigateur réel, de se connecter avec un compte de test et de vérifier visuellement l'interface. |
| **Apify** | Non précisé (service tiers) | API utilisée en backend (combinée à un modèle d'image) pour générer les images de miniatures. |
| **GitHub** (`github.com/Melvynx/thumbfa.st`) | Gratuit / Freemium | Gestion des dépôts Git, revue de code des modifications faites par l'IA et suivi des Pull Requests. |
| **api2cli.dev (api2cli)** | Gratuit (*open source*, créé par l'auteur) | Registre open-source permettant de transformer n'importe quelle API en CLI utilisable directement par des agents IA. |
| **svgl-cli** | Gratuit (*open source*) | Outil CLI issu de api2cli permettant de rechercher et d'intégrer des logos vectoriels (SVG) officiels dans le projet. |
| **TanStack Start** | Gratuit (*open source*) | Framework web utilisé sur le projet (mentionné comme cause potentielle de rechargements intempestifs en dev). |
| **Codelynx (`mlv.sh/fa`, `mlv.sh/coding`, `codelynx.dev`)** | Payant | Sites de l'auteur présentant sa configuration d'outils IA et sa formation payante (*AI Blueprint / AI Engineer*). |

---

### 3) Astuces concrètes et réutilisables

* **Paralléliser le travail des agents (multi-agents)** : Ne jamais attendre qu'une IA finisse pour passer à la suite. Ouvrez plusieurs discussions/onglets simultanément sur des fonctionnalités indépendantes (ex. 1 agent refond un menu, 1 agent corrige un bug d'URL, 1 agent intègre un paiement Stripe).
* **Utiliser la saisie vocale pour des prompts denses et précis** : Dicter vocalement permet de donner un contexte riche, des cas limites et des exigences UI détaillées en quelques secondes sans passer de longues minutes à taper.
* **Annoter des captures d'écran** : Prendre une capture d'écran, dessiner dessus des rectangles/flèches rouges pour marquer précisément les boutons ou blocs à ajouter/déplacer, et la glisser directement dans le prompt de l'agent.
* **Créer des « Skills » (compétences réutilisables dans le repo)** :
  * Un skill de workflow comme `APEX` ou `Impeccable` pour forcer l'agent à analyser, planifier, implémenter et valider selon des règles strictes.
  * Un skill de revue qualité du code (ex. `Clean Code` / `Thermo Nuclear Code Quality Review`).
  * Un skill `create-pr` pour automatiser la création de branche, le push et la rédaction de la PR sur GitHub.
* **Mettre en place un protocole de vérification visuelle (`rules/verification-browser.md`)** : Rédiger un fichier de règles expliquant à l'agent comment démarrer le navigateur local, se connecter avec un compte de test via code OTP lu dans les logs Convex, et valider visuellement la fonctionnalité avec des captures d'écran avant de marquer la tâche comme terminée.
* **Interrompre et rediriger l'agent (*Steer*)** : Dès que l'agent prend une mauvaise décision ou tourne en boucle sur une erreur (par exemple des logs incohérents avec un modèle comme Opus), utiliser la fonction de modification/redirection (*Steer*) pour réorienter immédiatement sa démarche sans perdre le fil.
* **Isoler l'environnement serveur** : Faire tourner le serveur local (Vite, Convex) dans un terminal séparé (via un éditeur rapide comme Zed) pour garder la main sur l'état d'exécution et éviter que l'agent ne coupe ou ne redémarre les processus à mauvais escient.
* **Itérer via les reviews de PR** : Laisser l'agent créer une PR sur GitHub, relire le diff, ajouter des commentaires sur les lignes problématiques (ex. code trop lourd, mauvaise fonction), puis demander à un nouvel agent de traiter directement les commentaires de la PR (`fix pr-comments`).

---

### 4) Chiffres de revenus annoncés

* **Revenus personnels / gains générés par l'auteur** : **Non précisé** (aucun montant de chiffre d'affaires ou de bénéfice personnel n'est communiqué dans la vidéo).
* **Prix et coûts mentionnés par l'auteur** :
  * Dépenses outils IA de l'auteur : *200 $/mois* pour Codex, *100 $/mois* pour Claude Code (*affirmé par l'auteur*).
  * Tarification du SaaS montré à l'écran : essai gratuit de 7 jours, puis abonnement à *20 $/mois* (*affirmé par l'auteur*).
