# Les SECRETS de Claude Code dévoilés

Vidéo : https://youtu.be/NnHEXeQfsLs · durée 17:39 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :**
La vidéo dévoile les mécanismes secrets de fonctionnement de *Claude Code* (mémoire, agents, commandes et styles de sortie) afin d'expliquer comment l'utiliser correctement et éviter les erreurs courantes commises par la majorité des développeurs.

2) **Outils, sites ou dépôts GitHub cités :**
- **Claude Code (Anthropic) :** L'outil principal d'IA pour le code.
- **Proxyman :** Outil de proxy/inspection réseau utilisé pour analyser les requêtes HTTP entre l'ordinateur et l'API d'Anthropic.
- **JSON Hero (jsonhero.io) :** Outil pour visualiser et inspecter les structures JSON des requêtes et réponses.
- **ChatGPT (GPT-4o) :** Modèle d'IA utilisé pour comparer, formater et tester les system prompts et styles de sortie.
- **Obsidian :** Mentionné pour structurer des notes en Markdown.
- **ABlueprint.dev :** Site de l'auteur proposant des ressources et abonnements liés à ses formations (payant).

3) **Astuces concrètes et réutilisables :**
- Comprendre l'architecture interne de Claude Code : la mémoire (`Claude.md`), le fil principal (*Main Thread* / chat principal), les sous-agents (*Sub-agents*), les commandes (`/commands`) et les styles de sortie (`Output-styles`).
- Ne pas abuser des sous-agents sans contexte : un sous-agent est une boîte noire qui n'a pas l'historique du chat principal ; il faut lui fournir un prompt précis, des instructions claires et limiter le bruit (tokens inutiles) pour obtenir de bons résultats.
- Injecter explicitement les instructions et les fichiers de configuration (comme `Claude.md`) dans les prompts personnalisés (par exemple dans ChatGPT ou via des configurations personnalisées) pour forcer l'IA à respecter les consignes de code et à éviter les hallucinations.
- Utiliser des outils de proxy (comme Proxyman) pour auditer ce qui est réellement envoyé aux API d'Anthropic et optimiser la taille du contexte.

4) **Chiffres de revenus annoncés (« affirmé par l'auteur ») :**
- Non précisé.
