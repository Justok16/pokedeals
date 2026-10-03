# Formation Codex : tout apprendre sur Codex en 1h gratuitement

Vidéo : https://youtu.be/wUCDDgxdRrQ · durée 1:00:44 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé complet et structuré de la vidéo :

---

### 1) Idée principale
Apprendre à maîtriser et configurer **OpenAI Codex** (l'outil d'agent IA autonome de développement concurrent de Claude Code) afin de concevoir rapidement des logiciels complets, SaaS et applications sans coder manuellement chaque ligne. La méthode repose sur l'exploitation des boucles agentiques (lecture, édition, validation autonome), la gestion optimisée de la mémoire (`AGENTS.md`), la création de compétences réutilisables (*skills*) et l'usage de sous-agents (*sub-agents*) pour économiser la consommation de tokens et de contexte.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité / Rôle |
| :--- | :--- | :--- |
| **OpenAI Codex (Desktop App)** | Inclus avec abonnement ChatGPT (Plus à ~20 $/mois ou Pro à ~200 $/mois, gratuit très limité) | Environnement de développement d'agents autonomes qui orchestre la modification de code, les tests et l'exécution sur la machine. |
| **Claude Code / Claude (Anthropic)** | Payant (via API / abonnement) | Outil agentique concurrent développé par Anthropic, utilisé comme point de comparaison. |
| **ChatGPT** | Gratuit / Payant (Plus à 20 $/mois, Pro à 200 $/mois / ~83 CHF affiché) | Plateforme LLM d'OpenAI servant de base d'authentification et de moteur pour Codex. |
| **VS Code (Visual Studio Code)** | Gratuit | Éditeur de code intégré et utilisé comme cible d'ouverture de fichiers. |
| **Zed (`zed.dev`)** | Gratuit (Open Source) | Éditeur de code léger et performant utilisé comme alternative à VS Code. |
| **Vite.js / React / TypeScript / Tailwind CSS** | Gratuit (Open Source) | Stack technique recommandée pour créer rapidement des applications web avec l'agent. |
| **shadcn/ui** | Gratuit (Open Source) | Bibliothèque de composants d'interface moderne pour React. |
| **Lumail.io** | Non précisé | SaaS de newsletter basé sur l'IA cité en exemple (créé par l'auteur). |
| **SaveIt.now** | Non précisé | SaaS de gestion intelligente de signets/bookmarks (cité en exemple). |
| **Thumbfa.st** | Non précisé | SaaS de génération de miniatures YouTube avec l'IA (créé par l'auteur). |
| **Tchao.app** | Non précisé | Application de messagerie développée à 100 % par l'IA sans coder une ligne. |
| **PadelTally.com** | Non précisé | Application mobile iOS de suivi de score de padel créée sans expertise iOS. |
| **`npx aiblueprint-cli`** | Gratuit (Outil de l'auteur) | Outil CLI (`agents unify`) pour unifier et synchroniser les configurations entre Codex, Claude Code et Cursor via des liens symboliques. |
| **`npx skills` (`makenotion/skills`)** | Gratuit (Open Source / Vercel) | CLI et dépôt GitHub permettant d'ajouter facilement des compétences (ex. Notion CLI) aux agents IA. |
| **FxTwitter / FixTweet API** | Gratuit | API tierce publique permettant de récupérer les données d'un tweet sans payer l'API officielle de X/Twitter. |
| **Typefully API / CLI** | Gratuit / Payant (clé API requise) | Outil de gestion et planification de tweets interfacé via un skill. |
| **Excalidraw** | Gratuit / Freemium | Outil de tableau blanc utilisé dans la vidéo pour schématiser les concepts agentiques. |
| **`mlv.sh/fc` (Melvynx)** | Inscription (Contenu/Formation de l'auteur) | Page de destination de l'auteur pour récupérer ses configurations clés en main. |

---

### 3) Astuces concrètes et réutilisables

* **Configuration idéale de Codex :**
  * Régler le *Work mode* sur **« For coding »**.
  * Activer impérativement l'option **« Full access »** et l'auto-review pour éviter que l'agent ne bloque et ne demande une autorisation manuelle à chaque lecture/écriture de fichier.
  * Configurer le *Follow-up behavior* sur **« Queue »** pour empiler les requêtes pendant que l'agent travaille.

* **Économie de fenêtre de contexte et de tokens :**
  * Utiliser la commande `/compact` dès que l'usage du contexte dépasse 50 % afin de réduire l'historique sans perdre la logique.
  * Déclencher des **sous-agents** (*sub-agents* comme `web-search` ou `code-explorer`) pour explorer la documentation ou analyser une codebase complexe : les sous-agents font la recherche dans leur propre contexte isolé et ne renvoient qu'une synthèse au *main agent*, ce qui permet d'économiser des milliers de tokens.

* **Gestion stricte de la mémoire (`AGENTS.md` / `CLAUDE.md`) :**
  * Définir un fichier global dans `~/.agents/AGENTS.md` (ou `.codex/`) avec les règles invariables (sécurité : interdiction de `rm -rf`, format de réponse, stack par défaut).
  * Créer un fichier `AGENTS.md` local à la racine de chaque projet contenant les commandes principales (`npm run dev`, `build`), la liste des bibliothèques et l'instruction de toujours lire le `README.md` avant d'agir.
  * Synchroniser `CLAUDE.md` et `AGENTS.md` via des liens symboliques (*symlinks*) avec `npx aiblueprint-cli@latest agents unify` pour pouvoir alterner entre Claude Code et Codex sans perdre ses règles.

* **Pilotage visuel par annotations :**
  * Utiliser le navigateur intégré de Codex pour prévisualiser l'application en direct.
  * Utiliser l'outil d'annotation/capture directement sur l'interface pour surligner un bouton ou une section et demander des modifications visuelles précises (couleurs, composants shadcn/ui).

* **Architecture d'un Skill réutilisable :**
  * Un skill doit être composé d'un dossier avec un fichier `SKILL.md` (contenant une balise `description` précise pour l'auto-déclenchement par l'IA), d'un script d'exécution (Python ou TypeScript/Bun) et de fichiers de référence Markdown.

* **Productivité de prompt :**
  * Utiliser la fonction dictée/microphone pour décrire des fonctionnalités complexes avec un maximum de contexte naturel plutôt que de taper des prompts abrégés au clavier.

---

### 4) Chiffres de revenus annoncés
* **Revenus financiers :** **Non précisé** (l'auteur ne mentionne aucun montant monétaire de chiffre d'affaires ou de bénéfice dans la vidéo).
* *Métriques d'usage des projets cités (affirmé par l'auteur) :*
  * Lumail.io : « plus de 3 millions d'e-mails envoyés » (affirmé par l'auteur).
  * Thumbfa.st : « plus de 1 000 utilisateurs » (affirmé par l'auteur).
