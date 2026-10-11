# J’utilisais les Sub-Agent n’importe comment : voici comment il faut faire

Vidéo : https://youtu.be/bsQ5Sz-qEh0 · durée 22:37 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :**
La vidéo critique l'utilisation superficielle et anarchique des « sub-agents » (sous-agents) de Claude Code sur Twitter et expose en détail leur fonctionnement interne, leurs limites et la manière rigoureuse de les intégrer dans un workflow de développement.

2) **Outils, sites ou dépôts GitHub cités :**
- **Claude Code :** Outil principal d'IA pour le code.
- **Grok Code (modèle Grok 4 supposé / Grok Fast) :** Modèle d'IA de xAI, présenté comme extrêmement bon marché ($0.2 / 1M tokens en input, $1.5 / 1M en output) et disponible gratuitement dans Cursor pendant une semaine.
- **Anthropic / Claude (Opus 4.1, Sonnet, Haiku 3.5) :** Modèles d'IA mentionnés pour comparer les tarifs des tokens.
- **SaveIt.now (saveit.now) :** Application SaaS personnelle de l'auteur pour bookmarker des sites (utilisée pour les démos).
- **Supabase / PostgreSQL :** Base de données utilisée dans les exemples.
- **JSON Hero (jsonhero.io) :** Outil pour visualiser et inspecter des fichiers JSON.
- **ChatGPT (GPT-4o) :** Modèle d'IA utilisé pour comparer les prompts et les system reminders.
- **Next.js / TypeScript / Prettier / ESLint :** Frameworks et outils de l'écosystème de développement.
- **ABlueprint.dev (ablueprint.dev / mlv.sh/bpvideo / mlv.sh/cccli) :** Site/ressource de l'auteur proposant une Masterclass et un CLI (Claude Code CLI setup) pour configurer ses agents et sa config (payant via la formation/le site).

3) **Astuces concrètes et réutilisables :**
- Ne pas lancer des dizaines de sub-agents sans structure (« FOMO » sur Twitter), car ils n'ont pas l'historique du chat principal et manquent de visibilité.
- Structurer le fichier `CLAUDE.md` et les instructions système (`System Reminder`) pour forcer l'IA à inclure les instructions globales et les règles de code.
- Utiliser des agents spécialisés (comme *NextJS Research* ou *Snipper*) de manière ciblée pour des recherches précises sans polluer le thread principal (« Main Agent »).
- Réduire le nombre d'exemples inutiles dans les prompts pour économiser les tokens et améliorer la pertinence des réponses.
- Utiliser l'outil de configuration CLI proposé par l'auteur (`ablueprint.dev`) pour automatiser les raccourcis, les statuts et les styles de sortie.

4) **Chiffres de revenus annoncés (« affirmé par l'auteur ») :**
- Non précisé.
