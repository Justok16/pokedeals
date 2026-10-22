# TUTO OpenCode : L'AGENT AI sans limites (mieux que Codex)

Vidéo : https://youtu.be/51xbklWiZag · durée 23:26 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. L'idée principale : La vidéo présente OpenCode, un agent de codage open source pour le terminal compatible avec n'importe quel LLM, offrant une alternative flexible à Claude Code qui est limité aux modèles d'Anthropic. Il détaille l'installation, l'authentification avec différents fournisseurs (Zen, Anthropic, GitHub Copilot, OpenAI, Z.AI) et la gestion des agents (Primary et Subagents) pour automatiser des tâches de développement.

2. Outils et sites cités :
- OpenCode (opencode.ai) : gratuit (open source), agent de codage pour le terminal adaptable à n'importe quel modèle.
- Anthropic Claude Pro / Max : payant, service LLM d'Anthropic.
- GitHub Copilot : payant, assistant de codage.
- OpenAI : payant, fournisseur de modèles d'IA.
- Z.AI / ZAI Coding Plan : payant (selon abonnement), plateforme proposant des modèles et plans de codage (ex: GLM-4.5).
- Escalidraw (app.excalidraw.com) : gratuit, outil de schématisation.

3. Astuces concrètes :
- Installer OpenCode via la commande terminal (`npm install -g opencode-ai` ou `brew install -g opencode-bin`).
- Configurer l'authentification avec `opencode auth login` pour choisir et connecter son fournisseur (Zen, Anthropic, GitHub Copilot, OpenAI, Z.AI).
- Créer ou mettre à jour le fichier de configuration `AGENTS.md` (ou `CLAUDE.md`) avec la commande `opencode` puis `/init` pour définir les règles, commandes et agents.
- Utiliser le mode "Plan" (`/plan` ou touche Tab) pour demander à l'IA d'analyser et de concevoir une tâche sans modifier directement le code, puis passer au mode "Build" pour l'implémenter.
- Gérer l'historique des modifications avec les commandes `/undo` et `/redo`.
- Configurer des commandes personnalisées dans le répertoire `.opencode/command.md` ou en créant des fichiers markdown pour automatiser des tâches récurrentes (ex: `pnppm lint`, `pnppm format`).

4. Chiffres de revenus : Non précisé.
