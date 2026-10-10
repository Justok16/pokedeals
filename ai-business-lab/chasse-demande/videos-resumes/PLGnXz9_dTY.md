# Connecteur (MCP) TradingView pour Claude et ChatGPT

Vidéo : https://youtu.be/PLGnXz9_dTY · envoyée par l'utilisateur le 28/09/2026 · résumé Gemini (gemini-3-flash-preview) du 2026-09-28
(chiffres et affirmations des auteurs : non vérifiés)

### 1) L'idée principale
La vidéo présente l'intégration officielle du **Model Context Protocol (MCP)** de TradingView avec des IA comme **Claude**, **ChatGPT** et **Codex**. Cela permet à l'IA de « lire » les graphiques, de scanner le marché en temps réel, de gérer des alertes et de créer des listes de surveillance (*watchlists*) automatiquement sans que l’utilisateur ait besoin de coder manuellement des scripts complexes.

### 2) Outils, sites et dépôts cités
*   **TradingView** (Freemium/Payant) : Plateforme d'analyse technique. Sert ici de source de données et de terminal d'exécution.
*   **Claude** (Anthropic) (Freemium/Payant) : L'IA utilisée pour analyser les données et exécuter les commandes via le protocole MCP.
*   **Codex** (Anthropic) (Statut de prix non précisé, lié à l'écosystème Claude) : Environnement de développement et d'automatisation pour les scripts.
*   **ChatGPT** (OpenAI) (Freemium/Payant) : Autre IA compatible avec l'installation du serveur MCP.
*   **OKX Europe** (Payant/Frais de transaction) : Broker (courtier) utilisé pour l'exécution des trades et le scan d'actifs spécifiques.
*   **Serveur MCP TradingView** (Gratuit/Inclus) : L'URL de connexion est `https://mcp.tradingview.com/mcp`. Il sert de pont (« port USB ») entre l'IA et les données boursières.

### 3) Astuces concrètes et réutilisables
*   **Installation du connecteur :** Dans Claude ou ChatGPT, allez dans les paramètres (Plugins ou Connecteurs), ajoutez un serveur MCP personnalisé, choisissez le type « diffusion HTTP en continu » et entrez l'URL officielle de TradingView.
*   **Auto-Journaling :** Utiliser l'outil `get_ohlcv` pour que l'IA récupère l'historique de tes trades passés et les analyse afin d'identifier tes erreurs récurrentes.
*   **Scanner de marché personnalisé :** Plutôt que de chercher à la main, demande à Claude : *"Scanne tous les actifs sur OKX qui sont au-dessus de la moyenne mobile 200 avec un RSI inférieur à 40"*. L'IA te sortira un tableau propre instantanément.
*   **Synchronisation des watchlists :** Une fois que l'IA a trouvé des opportunités, elle peut directement créer ou mettre à jour une liste dans ton compte TradingView via la commande `watchlist: create/add`.
*   **Veille Macro automatique :** Interroger le serveur MCP pour obtenir le calendrier économique et les news sans quitter l'interface de discussion.

### 4) Chiffres de revenus annoncés
*   **Affirmé par l'auteur :** **Non précisé.** L'auteur se concentre sur le gain de temps et l'efficacité technique plutôt que sur des promesses de gains financiers spécifiques. Il mentionne toutefois l'accès gratuit à son groupe privé de trading pour un mois sous certaines conditions de dépôt chez un broker.
