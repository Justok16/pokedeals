# Pi AGENT : le remplacement ultime de Claude Code

Vidéo : https://youtu.be/aiZP-7xzyQ8 · durée 26:52 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur teste pour la première fois **Pi** (`pi.dev`), un orchestrateur d'agents de programmation en ligne de commande (*agent harness*) open-source et hautement extensible en TypeScript. Conçu comme une alternative modulaire à des outils comme Claude Code, Pi permet d'intégrer de nombreux fournisseurs d'IA, de connecter son abonnement OpenAI/Codex, et d'étendre dynamiquement les fonctionnalités de l'agent (création de sous-agents en parallèle, interfaces TUI plein écran sur mesure, gestion de tâches). L'auteur souligne sa puissance de personnalisation tout en alertant sur la dérive potentielle des coûts en tokens et le piège de passer trop de temps à configurer ses outils plutôt qu'à produire.

---

### 2) Outils, sites et dépôts cités

* **Pi / `pi-coding-agent`** (`pi.dev` / dépôt GitHub `earendil-works/pi`) : **Gratuit et open-source** (les modèles IA restent payants). Harnais/orchestrateur d'agents de code pour terminal, modulaire et extensible via TypeScript/npm.
* **Catalogue d'extensions de Pi** (`pi.dev/packages`) : **Gratuit** (écosystème communautaire). Permet d'installer des extensions prêtes à l'emploi (ex. : `pi-subagents` pour déléguer des tâches à des sous-agents en parallèle, `rpiv-todo` pour une to-do interactive en direct, `pi-web-access` pour la recherche web, `pi-mcp-adapter` pour le protocole MCP, `context-mode`).
* **OpenAI Codex / ChatGPT Plus & Pro** : **Payant** (abonnement). Permet de se connecter directement dans Pi via OAuth (`/login`) pour exécuter des modèles (comme GPT-5.5 / GPT-5 Codex) via son abonnement plutôt que de payer les tokens à l'unité.
* **OpenRouter** (`openrouter.ai`) : **Payant à l'usage**. Passerelle d'API pour modèles tiers (testée au début avec le modèle `kimi-k2.6` de Moonshot AI).
* **Claude Code / Anthropic** : **Payant**. Mentionné comme référence concurrente pour les agents de dev en terminal.
* **Thumbfa.st** (`thumbfa-st-codelynx.vercel.app`) : Projet SaaS de l'auteur (générateur de miniatures YouTube par IA) servant de base de code réelle pour le test.
* **mlv.sh/fc** (Codelynx) : **Gratuit**. Lien promotionnel partagé par l'auteur pour obtenir ses configurations d'agents IA et son CLI gratuit.

---

### 3) Astuces concrètes et réutilisables

* **Connecter un abonnement existant plutôt que payer les tokens à l'API** : En utilisant la commande `/login` dans Pi, il est possible de relier son compte ChatGPT Plus/Pro (Codex). Cela évite de consommer des centaines de dollars d'API lors de l'exécution en boucle de multiples agents.
* **Délégation à des sous-agents en parallèle (`pi-subagents`)** : Vous pouvez lancer plusieurs sous-agents simultanément ayant chacun un rôle spécifique (ex. : révision de code par un profil sécurité, performance, tests, typage TypeScript) afin d'obtenir un audit complet sans bloquer la fenêtre principale.
* **Auto-modification et création d'interfaces en direct** : Pi peut concevoir et injecter lui-même des extensions TypeScript (ex. : un cockpit TUI complet comme `apex-ui` pour visualiser l'avancement, le temps passé par étape et les logs).
* **Rechargement à chaud (`/reload`)** : Après modification ou création d'une extension par l'IA, utilisez `/reload` dans le terminal pour appliquer immédiatement les nouveaux plugins et configurations sans redémarrer le terminal.
* **Inspection de l'arborescence des actions (`/tree`)** : La commande `/tree` permet de visualiser et de naviguer dans l'historique des modifications outil par outil pour revenir en arrière si nécessaire.
* **Éviter le « piège de la personnalisation »** : L'auteur met en garde contre le fait de consacrer des heures (et beaucoup d'argent en requêtes) à créer des extensions secondaires au lieu de livrer les fonctionnalités de son produit.

---

### 4) Chiffres de revenus annoncés
* Revenus ou gains financiers personnels : **Non précisé** (aucun chiffre d'affaires ni revenu n'est mentionné).
* Coûts de fonctionnement cités :
  * *10 $ dépensés en 30 minutes de test de tokens API* [affirmé par l'auteur].
  * *Estimation d'un coût de 160 $ pour une journée de 8 heures de travail intensif via API* [affirmé par l'auteur].
