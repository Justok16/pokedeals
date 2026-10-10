# Trader des actions 24h/24 et 7j/7 SANS courtier

Vidéo : https://youtu.be/om38rjz4jw8 · durée 13:28 · résumé Gemini (gemini-3.1-flash-lite) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré comme une fiche de connaissances en finance :

### 1) Sujet et thèse principale
**Sujet :** L'adaptation des plateformes d'échange crypto pour répondre aux besoins des investisseurs institutionnels.
**Thèse :** Pour être viables, les échanges doivent proposer des solutions de liquidité robustes, une gestion des risques avancée et une infrastructure technique (API) capable de supporter un trading haute fréquence, même en dehors des horaires de fermeture des marchés boursiers traditionnels.

### 2) Notions expliquées
*   **Tokenisation des actions :** Actifs basés sur la blockchain liés à la valeur d'une action ou d'un ETF (représentation numérique).
*   **Slippage :** Écart entre le prix espéré d'une transaction et le prix réellement exécuté (très important sur les gros volumes).
*   **Stock Perps (Perpétuels d'actions) :** Produits dérivés permettant de spéculer sur la hausse ou la baisse d'une action sans détenir l'actif sous-jacent.
*   **UTA (Unified Trading Account) :** Compte de trading unifié permettant de regrouper plusieurs produits (spot, marge, contrats à terme) sous un seul fonds de garantie.
*   **REST et WebSocket API :** Interfaces permettant aux logiciels de trading de se connecter à la plateforme pour automatiser l'exécution des ordres et recevoir des données en temps réel.
*   **Proof of Reserves (PoR) :** Méthode de preuve de détention des actifs par la plateforme pour assurer la transparence envers les utilisateurs.

### 3) Chiffres, taux et règles citées (date : 2026)
*   **Performance Bitget :** Le volume de liquidité "stock perps" a atteint 6,97 millions $ dans un écart de 5 bps, 16,22 millions $ dans un écart de 10 bps, et 55,92 millions $ dans un écart de 50 bps (juillet 2026, benchmark).
*   **Capacité API (à partir du 3 septembre 2026) :** Jusqu'à 600 requêtes par seconde (RPS) par utilisateur et jusqu'à 120 000 RPS via une structure de comptes liés.
*   **Ratio de collatéral :** Jusqu'à 95% pour les actifs éligibles (données de juillet 2026).
*   **Fonds de protection :** 5 500 BTC, avec une valeur maintenue au-dessus de 300 millions $ (valeur moyenne de 351 millions $ en juillet 2026).
*   **Réglementation :** *À vérifier à la source officielle* pour tout ce qui concerne la conformité, la fiscalité des actifs numériques et les garanties de protection des investisseurs dans votre juridiction.

### 4) Conseils concrets, limites et risques
*   **Conseil :** Utiliser des API pour automatiser les transactions et limiter les risques manuels, tout en restreignant l'accès via des adresses IP autorisées pour la sécurité.
*   **Limites :** Le trading 24/7 ne garantit pas une liquidité constante ; celle-ci est plus faible les week-ends et la nuit (vérifier le carnet d'ordres avant tout trade important).
*   **Risques :** Le partage d'un compte de garantie unique (UTA) signifie qu'une perte importante sur un produit peut impacter la marge disponible pour les autres positions.

### 5) Entreprises et produits cités
*   **Bitget :** Plateforme d'échange (l'ensemble de la vidéo est une **publicité sponsorisée** pour leurs services).
*   **Reality Protocol :** Fournisseur de la technologie d'émission et d'attestation des "rTokens" (rAAPL, etc.).
*   **The Network Firm :** Entreprise fournissant les attestations de réserve.
*   **Alpaca Securities :** Courtier détenant les titres sous-jacents.
*   **Solutions de garde tierce :** Copper ClearLoop, Cactus Custody, Fireblocks, Bitfire, OSL MirrorEX (partenaires tiers pour la sécurité).
*   **Promotions :** Le présentateur propose un lien de parrainage offrant jusqu'à 50 000 $ de bonus (conditionné à un dépôt initial de 5 000 $ et à la réalisation d'un trade) ainsi qu'un essai VIP 3.
