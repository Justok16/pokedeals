# Test de Codex pour la première fois avec GPT-5 (c’est plutôt bien)

Vidéo : https://youtu.be/uf7jQ6Q5FxQ · durée 31:33 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Comparer deux outils d'IA pour le développement (OpenAI Codex / Codex CLI et Claude Code) sur des tâches pratiques (ex : ajouter un chargement infini sur une extension Raycast), en analysant leur fonctionnement (prompts, outils, modèle) et leurs performances pour automatiser le code.

2) **Outils, sites et dépôts GitHub cités** :
* **OpenAI Codex / Codex CLI** (`openai/codex` sur GitHub) : Outil open-source (ligne de commande CLI) permettant de remplacer les flux de code par un outil OpenAI. Fonctionne avec le modèle Codex / GPT-5 (non précisé si gratuit ou payant, modèle payant/API).
* **Claude Code** (développé par Anthropic) : Outil de développement propulsé par des modèles comme Sonnet et Opus (non précisé si gratuit ou payant).
* **Cursor** : Éditeur / outil de code utilisant différents modèles (Sonnet, Opus, GPT-5) (non précisé si gratuit ou payant).
* **Raycast** : Lanceur d'applications / écosystème d'extensions (utilisé pour l'exemple de code) (non précisé si gratuit ou payant).
* **escalidraw.com** : Outil de schématisation en ligne utilisé pour les diagrammes (non précisé si gratuit ou payant).

3) **Astuces concrètes et réutilisables** :
* Le logiciel (Claude Code, Codex, Cursor) définit un « prompt pour les outils » et gère les outils disponibles (ex : WebSearch, WebFetch) pour décider automatiquement quand les utiliser.
* Utiliser les commandes CLI (ex : `npm run dev`, `git`, etc.) pour lancer des tâches de construction (« build ») ou de test afin de valider automatiquement le code généré par l'IA.
* Fournir à l'agent des liens vers la documentation officielle (ex : `https://.../api-docs`) pour lui permettre d'auto-corriger son code en lisant la doc exacte plutôt que de deviner.
* Lancer des scripts de test (ex : Playwright) en arrière-plan pour que l'IA puisse vérifier elle-même si ses modifications fonctionnent.

4) **Chiffres de revenus annoncés** :
* Aucun chiffre de revenus n'est annoncé dans cette vidéo.

---
