# J'ai tradé avec cette IA codé par Claude pendant 24h (Résultat Dingue) (vidéo YouTube e2JSCYig10g, chaîne Kasper)

Source envoyée le 30/09/2026 : https://youtu.be/e2JSCYig10g — résumé Gemini (gemini-3.6-flash) du 30/09/2026. Affirmations de l'auteur, non vérifiées.

Voici un résumé détaillé de la vidéo, structuré selon vos demandes :

---

### 1) L'idée principale
Utiliser une IA (Claude) pour générer automatiquement du code Python et des scripts de configuration sans savoir coder, afin de connecter un bot de trading automatisé à une plateforme **MetaTrader 5** hébergée sur un **VPS**. Le but est d'exécuter des stratégies de trading (notamment basées sur les *Imbalances* / *Fair Value Gaps*) 24h/24 en mode automatique et sécurisé.

---

### 2) Outils, sites et logiciels cités

*   **MetaTrader 5 (MT5)** (*MetaQuotes*)
    *   **Statut :** Gratuit.
    *   **Rôle :** Plateforme de trading utilisée pour passer les ordres sur les marchés (Forex, Or, etc.).
*   **Claude (Anthropic) / Claude Code**
    *   **Statut :** Gratuit (version de base) / Payant (abonnement Pro/API selon l'usage).
    *   **Rôle :** IA servant de « traducteur » et développeur : elle génère les prompts, les scripts PowerShell et les scripts Python nécessaires à la connexion et à la stratégie de trading.
*   **ForexVPS.net**
    *   **Statut :** Payant (Abonnements présentés : *Core* à ~25,60$/mois en annuel ou 32$/mois ; *Edge* à ~38$/mois ; *Prime* à ~51$/mois).
    *   **Rôle :** Serveur virtuel (VPS) hébergé à distance permettant de faire tourner le logiciel MT5 et le bot 24h/24 sans interrompre le fonctionnement si l'ordinateur personnel est éteint.
*   **Windows App / Remote Desktop (Microsoft)**
    *   **Statut :** Gratuit.
    *   **Rôle :** Application permettant de se connecter à distance au VPS Windows depuis un Mac ou un PC.
*   **Windows PowerShell**
    *   **Statut :** Gratuit (intégré à Windows).
    *   **Rôle :** Invite de commande sous Windows servant à exécuter les scripts d'installation automatique des dépendances Python.
*   **Python & dépendances (`MetaTrader5`, `pandas`, `numpy`, `scipy`)**
    *   **Statut :** Gratuit / Open Source.
    *   **Rôle :** Langage et bibliothèques de code utilisés par le bot pour communiquer avec l'API MetaTrader 5.

---

### 3) Astuces concrètes et réutilisables

1.  **Commencer obligatoirement sur un compte Démo :** Configurer un dépôt fictif réaliste (ex. 3 000 € à 5 000 €) sur MT5 pour tester le bot pendant 24h à 48h avant d'envisager du capital réel.
2.  **Activer les notifications push sur mobile :** Dans les réglages de l'application smartphone MT5, activer *« Notifications de Trading »* pour recevoir une alerte instantanée à chaque prise de position du bot et pouvoir intervenir à tout moment.
3.  **Choix de la localisation du VPS :** Lors de la configuration du VPS, choisir la localisation **Londres** pour réduire la latence réseau vers les serveurs de courtage MT5.
4.  **Gestion de contexte sur Claude :** Ouvrir systématiquement une **nouvelle conversation vierge** sur Claude pour chaque étape ou script afin d'éviter le mélange d'instructions et les erreurs de code.
5.  **Encadrement strict des risques dans le prompt :**
    *   Régler le risque à **1 % du capital** par trade.
    *   Fixer des limites de perte (*Stop Loss* serré, *Kill Switch* quotidien à -3 %).
    *   Restreindre les horaires de trading (ex. 09h00–22h00 heure de Paris) pour éviter les sessions à faible liquidité ou forte volatilité incontrôlée (session asiatique, week-end).
6.  **Script de surveillance (Monitoring/Check) :** Ajouter un script de contrôle automatique qui effectue un bilan toutes les 15 minutes dans la console pour vérifier que le bot est actif, connecté et sans erreur bloquante.

---

### 4) Chiffres de revenus annoncés (*affirmés par l'auteur*)

*   **150,30 €** de profit généré en un peu plus de 24 heures de test automatisé avec Claude (*affirmé par l'auteur*).
*   **Plus de 6 000 $** de gain réalisé sur un trade d'achat (AUD/USD) grâce à un outil d'analyse OrderBlocks IA (*affirmé par l'auteur*).
*   **200 € à 1 000 €+** économisés par stratégie (et plus de 10 000 € au total) en évitant d'embaucher des développeurs externes pour coder les bots (*affirmé par l'auteur*).
