# Vidéo https://youtu.be/Pk7W7BKMwqo

> Résumé produit par Gemini (via le relais Vercel) le 25/09/2026. Les chiffres de revenus sont **affirmés par l’auteur de la vidéo, non vérifiés**.

Voici un résumé de la vidéo, en français, pour quelqu'un souhaitant générer des revenus légalement grâce à l'IA et Claude Code :

---

**1) Idée Principale**

L'idée principale est de présenter comment combiner **Jev**, un modèle d'IA "Système Un" ultra-rapide et économique pour la classification et la prise de décision structurée, avec un **LLM (Grand Modèle Linguistique)** comme **Claude Code** (par Anthropic) ou **ChatGPT** pour l'idéation et la recherche de stratégies. Cette combinaison permet de créer des bots de trading à haute fréquence (HFT) ou de news trading avec une latence extrêmement faible (~0,5 seconde par décision), offrant potentiellement un avantage significatif sur les marchés financiers. Le système est également applicable aux workflows commerciaux nécessitant une consommation massive de données et une prise de décision rapide.

---

**2) Outils, Sites et Dépôts GitHub Citées**

*   **Jev:**
    *   **Nom exact:** Jev (appelé un "modèle de Système Un" par Typesafe).
    *   **Gratuit/Payant:** Payant (coûte une fraction de centime par "pensée" / décision).
    *   **Utilité:** Effectue des décisions structurées rapides en évaluant un état et en renvoyant des réponses typées avec des probabilités. Utilisé pour l'exécution des trades à faible latence et pour la classification rapide des informations.
*   **Claude Code (par Anthropic) / Claude Opus 5.5:**
    *   **Nom exact:** Claude Code / Claude Opus 5.5.
    *   **Gratuit/Payant:** Payant (mentionné comme coûtant plus cher pour l'inférence).
    *   **Utilité:** Idéation de stratégies, backtesting, recherche ouverte, génération de code pour les bots. Le "cerveau" qui conçoit la stratégie.
*   **ChatGPT:**
    *   **Nom exact:** ChatGPT.
    *   **Gratuit/Payant:** Non précisé (implicitement payant pour les usages avancés).
    *   **Utilité:** Mentionné comme exemple de LLM pour la conception de stratégies (comme Claude).
*   **Astra:**
    *   **Nom exact:** Astra.
    *   **Gratuit/Payant:** Non précisé (semble être un outil développé ou utilisé par l'auteur).
    *   **Utilité:** Utilisé pour la conception des backtests et stratégies.
*   **Hyperliquid:**
    *   **Nom exact:** Hyperliquid.
    *   **Gratuit/Payant:** Non précisé.
    *   **Utilité:** Une plateforme où le bot de trading démo est exécuté pour les transactions en direct.
*   **JevLoop:**
    *   **Nom exact:** JevLoop.
    *   **Gratuit/Payant:** Non précisé (semble être l'interface de tableau de bord du système Jev).
    *   **Utilité:** Tableau de bord affichant les prix en direct, les appels de Jev (achat/vente), les profits et pertes, la latence.
*   **Jev Newsroom:**
    *   **Nom exact:** Jev Newsroom.
    *   **Gratuit/Payant:** Non précisé (fait partie du système Jev).
    *   **Utilité:** Tableau de bord qui reçoit des titres d'actualité en direct, Jev lit les titres et assigne une probabilité (haussière, baissière, neutre) et un score d'impact, puis montre comment le prix de l'actif a évolué après le titre. Utilisé pour le news trading automatisé.
*   **LangChain:**
    *   **Nom exact:** LangChain.
    *   **Gratuit/Payant:** Non précisé (un framework pour le développement d'agents LLM).
    *   **Utilité:** Jev s'intègre dans la boucle d'agent de LangChain.
*   **Alpaca (Paper Trading):**
    *   **Nom exact:** Alpaca.
    *   **Gratuit/Payant:** Offre le paper trading gratuit, ainsi que le trading en direct.
    *   **Utilité:** Plateforme d'échange pour le paper trading et le trading en direct de cryptos et d'actions. Mentionné comme ayant des frais légèrement plus élevés.
*   **Bybit:**
    *   **Nom exact:** Bybit.
    *   **Gratuit/Payant:** Non précisé (mais mentionné comme ayant des frais plus bas que Alpaca).
    *   **Utilité:** Plateforme d'échange de crypto-monnaies (crypto, perpétuels, actions). Préférée pour sa profondeur et ses frais réduits.
*   **Hostinger:**
    *   **Nom exact:** Hostinger.
    *   **Gratuit/Payant:** Payant (fournisseur de VPS, l'auteur a un code de réduction).
    *   **Utilité:** Pour héberger un serveur VPS "always-on" afin que le bot de trading puisse fonctionner 24h/24 et 7j/7 sans interruption.
*   **Trigger.Trade:**
    *   **Nom exact:** Trigger.Trade.
    *   **Gratuit/Payant:** Non précisé.
    *   **Utilité:** Permet d'exécuter des stratégies basées sur Pine Script dans le cloud. Peut réduire le besoin d'un VPS, mais n'est pas aussi efficace si l'on souhaite intégrer Jev.
*   **Quantpedia / NNFx:**
    *   **Nom exact:** Quantpedia, NNFx.
    *   **Gratuit/Payant:** Non précisé.
    *   **Utilité:** Ressources pour trouver des stratégies de trading.
*   **TradingView:**
    *   **Nom exact:** TradingView.
    *   **Gratuit/Payant:** Offre des versions gratuites et payantes.
    *   **Utilité:** Pour visualiser et backtester des stratégies de trading (via Pine Script).
*   **Lewis Jackson (chaîne YouTube) & Roan (@RohOnChain sur X):**
    *   **Noms exacts:** Lewis Jackson, Roan.
    *   **Gratuit/Payant:** Non applicable (créateurs de contenu).
    *   **Utilité:** Sources d'inspiration pour le développement de bots de trading IA.
*   **`JEV_STARTER_PROMPT.md`:**
    *   **Nom exact:** `JEV_STARTER_PROMPT.md`.
    *   **Gratuit/Payant:** Gratuit (disponible dans la communauté School de l'auteur).
    *   **Utilité:** Fichier de prompt d'installation pour Claude Code qui construit l'architecture Jev pour le paper trading.
*   **AI_HEDGE_FUND_BUFFETT_INSTALL.md:**
    *   **Nom exact:** `AI_HEDGE_FUND_BUFFETT_INSTALL.md`.
    *   **Gratuit/Payant:** Gratuit (disponible dans la communauté School de l'auteur).
    *   **Utilité:** Fichier d'installation et guide pour un "AI Hedge Fund" de style Buffett, configurant Jev pour l'analyse fondamentale.

---

**3) Astuces Concrètes et Réutilisables**

*   **Complémentarité des IA:** Utiliser les LLM (Claude, ChatGPT) pour la conceptualisation, la recherche de stratégies et l'analyse ouverte, car ils sont excellents pour l'inférence complexe. Utiliser Jev pour la classification rapide, la prise de décision structurée et l'exécution des ordres, car il est optimisé pour la vitesse et le coût par décision, ce qui est crucial pour le HFT et le news trading.
*   **Processus de Développement de Stratégie:**
    1.  **Idéation:** Utiliser un LLM pour concevoir des stratégies.
    2.  **Backtesting:** Exécuter des centaines ou des milliers de backtests avec un moteur de backtesting (comme celui développé par l'auteur ou en demander un à Claude Code) pour identifier les stratégies potentiellement rentables *hors échantillon*.
    3.  **Filtrage et Optimisation:** Affiner les stratégies prometteuses en comprenant pourquoi elles fonctionnent et ce qui peut être amélioré.
    4.  **Paper Trading (Obligatoire):** Avant de risquer de l'argent réel, déployer la stratégie sur un compte de paper trading (Alpaca, Bybit) pour vérifier sa rentabilité et s'habituer au système.
    5.  **Trading en Direct (Optionnel):** Une fois la confiance établie avec le paper trading, passer au trading en direct avec de l'argent réel.
*   **Gestion des Risques:** Toujours intégrer des règles de risque strictes (position maximale, perte journalière, "kill switch") dans le code du bot.
*   **Surveillance et Alertes:** Pour les stratégies à enjeux élevés, configurer des systèmes d'alerte (ex: sur téléphone via Telegram) pour recevoir des notifications et permettre une approbation manuelle avant l'exécution de certains trades.
*   **Optimisation de la Latence:** Pour le news trading, la vitesse est primordiale. Utiliser des sources d'actualités payantes (plus rapides) et s'assurer que Jev peut lire et traiter les titres en moins d'une seconde.
*   **Infrastructure "Always-On":** Pour un fonctionnement 24h/24 et 7j/7 sans interruption, héberger le bot sur un serveur VPS ou un PC local dédié qui reste toujours allumé.
*   **Sécurité des Clés API:** Utiliser des clés API "trade-only" (permettant uniquement de trader, pas de retirer des fonds) et les lier à l'adresse IP du serveur pour une sécurité accrue.
*   **Documentation et Communauté:** Rejoindre la communauté de l'auteur sur School pour accéder aux prompts d'installation et aux mises à jour.

---

**4) Chiffres de Revenus Annoncés (affirmés par l'auteur)**

*   Le bot de trading présenté dans la vidéo a généré **15 $ de profit** durant la période d'enregistrement de la vidéo sur un compte de paper trading.
*   L'auteur a "donné à un AI Warren Buffett 100 000 $ à trader" et le bot a généré **+11 938 $** (non précisé sur quelle période).
*   L'auteur mentionne qu'il a un bot IA qui lui a rapporté **8 262 $** (non précisé sur quelle période).
*   Lewis Jackson (une de ses inspirations) est mentionné avec des revenus mensuels de "environ **1,5 K $**" (selon TubeBuddy) et une de ses vidéos s'intitule "GPT-4 Auto is INSANE for Trading (Full Test) (avec **3 285.42 $/jour** visible sur la miniature)".
