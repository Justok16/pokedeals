# Je suis allé DEEP avec Claude Code — 13 TIPS que 99% ignorent

Vidéo : https://youtu.be/K5osMuKZHqM · durée 19:55 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Cette vidéo présente 13 astuces et fonctionnalités avancées pour utiliser efficacement l'outil CLI Claude Code (en mode multi-agents ou en solo), permettant d'optimiser le setup, les modes de fonctionnement, les commandes, la mémoire, la navigation et l'intégration de Model Context Protocol (MCP).

2) **Outils, sites ou dépôts GitHub cités :**
* **Claude Code** (outil CLI d'Anthropic) : Modèle payant/abonnement, utilisé pour coder et interagir avec la codebase via le terminal.
* **Cursor** (éditeur de code) : Gratuit/payant, éditeur de code IA.
* **VS Code** (éditeur de code) : Gratuit, éditeur de code.
* **GitHub Copilot** (assistant IA) : Payant, assistant de code.
* **GitHub CLI (`gh`)** : Gratuit, outil en ligne de commande pour interagir avec GitHub.
* **Playwright** (via le serveur MCP Playwright) : Gratuit (open-source), utilisé pour naviguer sur le web et automatiser des tests/actions du navigateur.
* **Context7** (serveur MCP) : Gratuit (open-source), utilisé pour fournir du contexte documentaire précis sur des frameworks (ex. Next.js).
* **dcp** / **dcp-research-analyst** (agents/scripts mentionnés) : Outils internes/custom agents pour la recherche approfondie.
* **Excalidraw** (outil de schéma) : Gratuit (freemium), utilisé pour illustrer des concepts.
* **iiblueprint.dev** (site web mentionné) : Site de formation et ressources sur l'IA (`iiblueprint.dev/dev`).

3) **Astuces concrètes et réutilisables :**
* **Tip 1 (Setup) :** Lancer la commande terminal `terminal setup` pour configurer les keybindings et le keybinding pour le saut de ligne, ou utiliser `/ide` pour configurer l'IDE et lier l'éditeur actif.
* **Tip 2 (Shortcut) :** Utiliser la commande `claude --continue` (ou `claude -c`) pour rouvrir directement Claude Code sur la dernière conversation sans avoir à relancer un `reasons` ou rechercher l'historique.
* **Tip 3 (Modes) :** Utiliser les modes de fonctionnement (via raccourci clavier majuscule `Shift + Tab`) : mode par défaut (demande confirmation à chaque modification), mode auto-accept edit on (modifie sans demander), et mode plan (génère un plan de modification à valider avant d'exécuter).
* **Tip 4 (Commandes) :** Utiliser le point d'exclamation (`!`) suivi d'une commande bash (ex. `!pnpm build`) directement dans Claude Code pour exécuter des scripts, lancer des tests ou résoudre des bugs identifiés par le terminal.
* **Tip 5 (Memory) :** Utiliser la commande `# memory` pour demander à Claude de retenir des consignes permanentes (ex. "rappelle-toi de toujours exécuter `pnpm ts` dans ce dossier"), qui seront stockées dans un fichier `CLAUDE.md`.
* **Tip 6 (Navigation) :** Appuyer deux fois sur la touche `Escape` (double escape) pour remonter dans l'historique des commandes et messages précédents dans le terminal.
* **Tip 7 (Config Claude / Master Rules) :** Créer et configurer un fichier `CLAUDE.md` à la racine pour définir des *Master Rules* globales (ex. interdire d'ajouter des mentions automatiques de co-auteur dans les commits, imposer l'utilisation de `gh` CLI).
* **Tip 8 (Config + Hooks) :** Configurer les fichiers `settings.json` et des hooks (via `/hooks`) pour automatiser des actions avant ou après l'exécution d'un outil (ex. jouer un fichier MP3 `finish.mp3` ou `need-human.mp3` lors d'événements comme le succès ou l'arrêt).
* **Tip 9 (Commandes globales) :** Créer des fichiers de commandes personnalisés (ex. dans un dossier `.claude/commands/`) pour définir des workflows réutilisables (comme un script de commit standardisé ou de gestion de worktrees).
* **Tip 10 (Skip permissions) :** Lancer Claude Code avec l'argument `--dangerously-skip-permissions` (ou le mode équivalent) pour contourner les invites de validation de permissions lors de l'exécution de scripts en mode agent autonome.
* **Tip 11 (MCP - Model Context Protocol) :** Intégrer des serveurs MCP comme **Playwright** (pour naviguer sur des sites web et prendre des captures d'écran) et **Context7** (pour récupérer de la documentation technique ultra-précise sur des technos comme Next.js).
* **Tip 12 & 13 (Multi Claude Code / Worktrees) :** Utiliser des scripts de worktrees Git combinés à Claude Code pour lancer plusieurs instances simultanées de Claude Code sur des branches différentes, permettant à plusieurs agents de travailler en parallèle sur la même codebase sans conflits.

4) **Chiffres de revenus annoncés :**
* Non précisé

---
