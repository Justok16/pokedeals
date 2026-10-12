# 2 MCP pour Cursor VRAIMENT utiles (pas comme les autres nuls)

Vidéo : https://youtu.be/G_E1kOWjYoc · durée 16:28 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Utiliser les protocoles de contexte de modèle (MCP), notamment via *shadcn* et *Context7*, pour enrichir l'IA de documentation à jour et automatiser la configuration de projets et de composants.

2) **Outils, sites ou dépôts cités** :
- **Model Context Protocol (MCP)** : Protocole de contexte pour assistants IA (gratuit).
- **Context7 (context7.com)** : Service de documentation à jour pour LLMs (gratuit).
- **Cursor** : Éditeur de code compatible MCP (gratuit / payant).
- **GitHub** : Hébergement de code et de templates (gratuit).

3) **Astuces concrètes et réutilisables** :
- Configurer un serveur MCP dans Cursor (via un fichier `mcp.json`) pour permettre à l'IA d'interagir directement avec des registres de composants (ex: registre Alpine de *shadcn*).
- Utiliser la commande d'initialisation MCP pour cloner et structurer automatiquement un projet à partir d'un template distant.
- Intégrer Context7 dans le fichier de règles globales (`mcp.mdc` ou `global.mdc`) pour forcer l'IA à récupérer la documentation la plus récente avant d'écrire du code.
- Vectoriser et indexer la documentation de bibliothèques tierces (comme Zod ou Next.js) pour que l'IA génère du code précis et sans hallucination.

4) **Chiffres de revenus annoncés** :
- Non précisé.

---
