# Optimise le context avec Claude code

Vidéo : https://youtu.be/DreD7cRpHM4 · durée 2:11 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur montre comment la gestion du contexte dans Claude Code peut consommer beaucoup de tokens à cause de l'utilisation de MCP (Model Context Protocol), et comment désactiver les MCP inutiles pour réduire significativement les coûts.

2) **Outils, sites ou dépôts cités :**
- **Claude Code** : payant, assistant de codage en ligne de commande.
- **MCP (Model Context Protocol)** / fichiers de configuration (comme `mcp.json` ou `mcp.utils.json`) : gratuits (composants logiciels), servent à étendre les fonctionnalités de l'IA (comme `Thing`, `Playwright`, etc.).

3) **Astuces concrètes et réutilisables :**
- Vérifier la consommation de son contexte avec la commande `/context` pour identifier les MCP trop gourmands.
- Désactiver les MCP superflus en les retirant du fichier de configuration JSON pour faire baisser la consommation de tokens (passer par exemple de 14% à moins de 7%).
- Utiliser la commande `/rewind` (ou `escape escape`) pour revenir en arrière dans l'historique et restaurer le code d'une version précédente en cas d'erreur de l'IA.

4) **Chiffres de revenus annoncés (« affirmé par l'auteur ») :**
- Non précisé.

---
