# Vidéo https://youtu.be/hopcesPukiA

> Résumé produit par Gemini (via le relais Vercel) le 25/09/2026. Les chiffres de revenus sont **affirmés par l’auteur de la vidéo, non vérifiés**.

Voici un résumé de la vidéo, axé sur l'utilisation légale de l'IA pour générer des revenus et l'emploi de Claude Code :

---

**Résumé : Gagner de l'argent légalement avec l'IA et Claude Code pour le trading algorithmique**

**1) Idée Principale :**
La vidéo présente comment utiliser l'agent conversationnel Claude Opus 5.5 d'Anthropic, via l'environnement Claude Code, pour rechercher, développer, tester (backtest) et valider des stratégies de trading algorithmique, spécifiquement pour le trading de l'or (XAU-USD) sur données personnalisées. L'objectif est de créer des stratégies rentables et non sur-optimisées, en tenant compte des conditions réelles du marché (heures de trading, frais, slippage) et en utilisant le framework Jesse pour l'exécution et l'analyse.

**2) Outils, Sites et Dépôts GitHub Cités :**

*   **Anthropic Claude Opus 5.5**
    *   **Statut:** Payant.
    *   **Objectif:** Modèle d'IA de pointe, présenté comme le "meilleur modèle jamais créé". Utilisé comme agent intelligent pour la recherche, le codage, l'analyse et la validation de stratégies de trading. La vidéo montre des benchmarks où il surpasse ses concurrents.
    *   **Prix annoncés par l'auteur:**
        *   Mode standard : **4 $** par million de tokens d'entrée, **20 $** par million de tokens de sortie.
        *   Mode rapide (jusqu'à 2.5x plus rapide) : **8 $** par million de tokens d'entrée, **40 $** par million de tokens de sortie.

*   **Claude Code** (version v2.1.280)
    *   **Statut:** Payant (utilise Claude Opus 5.5).
    *   **Objectif:** Environnement de développement intégré (IDE) permettant d'interagir directement avec les modèles Claude. Il est utilisé pour écrire et exécuter des requêtes à l'IA pour générer le code et les analyses de trading.

*   **Jesse** (Framework de trading algorithmique)
    *   **Statut:** Open-source (licence MIT), basé sur Python.
    *   **Dépôt GitHub:** `github.com/jesse-ai/jesse`
    *   **Site Web:** `jesse.trade`
    *   **Objectif:** Framework avancé de trading crypto pour la recherche, la définition, le backtesting, l'optimisation et le trading en direct de stratégies. Il sert de moteur d'exécution et d'analyse pour les stratégies générées par l'IA.

*   **Lighter Exchange**
    *   **Statut:** Non précisé pour le statut général, mais les frais Maker/Taker pour XAU sont de 0%.
    *   **Site Web:** `app.lighter.xyz/trade/XAU`
    *   **Objectif:** Plateforme d'échange pour le trading de l'or (XAU-USD). La vidéo l'utilise comme référence pour les frais réels et le slippage, même si les frais affichés sont de 0% pour Maker/Taker, le slippage doit être pris en compte.

*   **Jesse.Trade Telegram Channel**
    *   **Statut:** Gratuit.
    *   **Objectif:** Canal de communication où l'auteur partage des liens utiles, des mises à jour sur ses projets et du contenu lié au trading algorithmique.

*   **Jesse Discord Server**
    *   **Statut:** Gratuit.
    *   **Objectif:** Communauté de plus de 6000 traders algorithmiques pour discuter et échanger des connaissances.

**3) Astuces Concrètes et Réutilisables :**

*   **Prompt Engineering Avancé :**
    *   **Soyez très précis** : Définissez clairement tous les critères pour la stratégie (ratio de Sharpe minimum, période de backtest, risque par transaction, objectifs d'optimisation, simulations de Monte Carlo).
    *   **Exigez l'exhaustivité** : Demandez à l'IA de continuer à chercher jusqu'à ce que les critères soient atteints ou qu'elle ait essayé un nombre défini de variations (ex: "au moins 200 variations de stratégie"). Cela pousse l'IA à être plus "intelligente" et moins "paresseuse".
    *   **Spécifiez les conditions de marché** : Incluez des détails comme le timeframe (1h de trading, 4h d'ancrage), les positions (longues et courtes), le type de marché (futures, pas spot) et les frais de trading (ex: 0.02% pour anticiper le slippage).

*   **Validation et Prévention du Sur-apprentissage (Overfitting) :**
    *   **Simulations de Monte Carlo** : Utilisez-les pour évaluer la robustesse de la stratégie. Une courbe d'équité originale qui se situe *au milieu* des simulations de Monte Carlo indique une robustesse ; si elle est parmi les meilleures (en haut), c'est un signe de sur-apprentissage.
    *   **Test sur données "out-of-sample"** : Validez la stratégie sur des périodes de données que l'IA n'a pas vues pendant sa phase d'optimisation. La vidéo montre des backtests sur des fenêtres de temps différentes pour confirmer la performance.
    *   **Analyse visuelle avec graphiques détaillés** : Utilisez les graphiques générés par Jesse pour visualiser les points d'entrée/sortie, les stops, les take-profits et les indicateurs. Cela permet de vérifier que la stratégie se comporte comme prévu.

*   **Gestion des Frais et Conditions Réelles :**
    *   **Intégrer les frais et le slippage** : Même si une plateforme annonce des frais de 0%, le slippage peut avoir un impact significatif. Fixez des frais réalistes dans le backtest (ex: 0.02% pour l'or).
    *   **Gérer les heures de trading des marchés traditionnels** : Pour des actifs comme l'or, qui ne se négocient pas 24h/24 et 7j/7 comme les cryptomonnaies, l'IA doit intégrer les heures de trading spécifiques (ex: heures du marché CME Globex de New York, jours fériés). Jesse propose une fonction `trading_hours` pour cela, et `utils.filter_candles_by_hours` pour s'assurer que les indicateurs ne sont calculés que sur des données de marché actives.

**4) Chiffres de Revenus Annoncés (affirmé par l'auteur) :**

Les chiffres suivants proviennent des backtests effectués avec Jesse, non du trading réel :

*   **Stratégie XAUSTBreak0 (cible 2024-2026) :**
    *   Sharpe Ratio : **2.03**
    *   Profit net : **+170%**
    *   Max Drawdown : **-19.2%**

*   **Stratégie XAUSTBreak0 (hors échantillon, 2 dernières années) :**
    *   Sharpe Ratio : **2.03**
    *   Profit net : **+139%**
    *   Max Drawdown : **-18.4%**

*   **Stratégie XAUSTBreak0 (hors échantillon, 2022-2023) :**
    *   Sharpe Ratio : **1.40**
    *   Profit net : **+85%**
    *   Max Drawdown : **-20.7%**

*   **Simulation de Monte Carlo (stratégie initiale, sur 200 scénarios) :**
    *   Profit net (Original / Pire 5% / Médian / Meilleur 5%) : **169.6% / 145.2% / 329.8% / 667.7%**
    *   Sharpe Ratio (Original / Pire 5% / Médian / Meilleur 5%) : **2.03 / 2.03 / 3.21 / 4.17**
    *   Taux de gain (Original / Pire 5% / Médian / Meilleur 5%) : **35.0% / 37.7% / 47.3% / 59.0%**
    *   Le résultat original (2.03 Sharpe) est situé dans le pire 5% des simulations, ce qui indique que la stratégie est "chanceuse" ou sur-optimisée si on ne considère que les backtests standards.

*   **Stratégie XAUSTBreak0 (backtest sur 10 ans, 2016-2026, après amélioration) :**
    *   Profit net total : **2709.63%**
    *   Solde de départ -> Solde final : **10000 -> 280962.75**
    *   Rendement annuel : **37.32%**
    *   Sharpe Ratio : **1.41**

*   **XAUSTBreakPremium (version améliorée disponible sur jesse.trade) :**
    *   Profit net : **$4793.52**
    *   Taux de gain : **66.67%**
    *   Max Drawdown : **-8.90** (non précisé si c'est en % ou en valeur absolue, mais implicitement en % vu le format)
    *   Sharpe Ratio : **4.29**

---
