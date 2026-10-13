# NOUVEAU : Cursor 0.46 peut prendre CONTRÔLE de ton compte GitHub

Vidéo : https://youtu.be/_cOdbozzZtU · durée 11:51 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :**
La vidéo présente la mise à jour majeure de **Cursor (version 0.46)**, qui introduit le support complet du **Model Context Protocol (MCP)**. Cela permet à l'IA de l'éditeur de se connecter directement à des services externes (comme GitHub, des bases de données locales, etc.), couplé à une refonte de l'interface (menus déroulants unifiés) et à l'utilisation de serveurs de mémoire persistante.

2. **Outils, sites et dépôts GitHub cités :**
- **Cursor** (IDE / Modèle freemium à ~20$/mois) : Éditeur de code basé sur l'IA, dont la version 0.46 apporte le support MCP.
- **Model Context Protocol (MCP)** (Protocole / Open source, gratuit) : Standard créé par Anthropic pour connecter les assistants IA à des outils externes.
- **GitHub** (Dépôt/API / Gratuit) : Connecté via MCP pour lister et interagir avec des répertoires et des issues.
- **Docker** (Outil de virtualisation / Gratuit) : Utilisé pour lancer certains serveurs MCP (ex: PostgreSQL, Memory, etc.).
- **NPX / Node.js** (Environnement d'exécution / Gratuit) : Utilisé pour exécuter des packages MCP en ligne de commande.
- **MCP Servers (Dépôt GitHub officiel)** (`github.com/modelcontextprotocol/servers` / Gratuit) : Répertoire regroupant les serveurs de référence (Memory, GitHub, FileSystem, etc.).
- **Formation MLV (Site : `mlv.sh/ai`)** (Formation / Payant) : Programme de formation de l'auteur sur les agents IA et l'utilisation avancée de Cursor.

3. **Astuces concrètes et réutilisables :**
- Configurer un serveur MCP de mémoire (ex: `memory-server` via `npx`) dans Cursor pour permettre à l'agent IA de se souvenir d'informations persistantes d'une session à l'autre (ex: nom de l'utilisateur, OS utilisé).
- Activer le mode "Yolo Mode" dans Cursor pour autoriser l'IA à exécuter des commandes terminal et des modifications de fichiers de manière autonome sans demander de validation à chaque étape (nécessite de la vigilance).
- Connecter l'API GitHub via un Personal Access Token (PAT) dans le fichier de configuration MCP (`mcp.json`) pour permettre à l'IA de lister des issues, créer des branches, commiter du code et ouvrir des Pull Requests directement depuis le chat.

4. **Chiffres de revenus annoncés :**
- **20 $ / mois** : Coût de l'abonnement payant de Cursor (affirmé par l'auteur).
- **4,08 $** : Montant de la consommation API facturée à l'auteur pour ses requêtes sur Cursor (affirmé par l'auteur).

---
