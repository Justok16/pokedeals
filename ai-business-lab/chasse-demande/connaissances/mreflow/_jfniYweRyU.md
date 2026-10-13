# Comment installer et utiliser le nouvel agent IA de Claude

Vidéo : https://youtu.be/_jfniYweRyU · durée 14:15 · résumé Gemini (gemini-3.5-flash-lite, lot de 4) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Démonstration pratique et test complet de la nouvelle fonctionnalité révolutionnaire d'Anthropic : **Computer Use** (utilisation d'ordinateur), permettant à Claude (via Claude 3.5 Sonnet / Haiku) de contrôler un ordinateur à distance, d'ouvrir des applications (navigateur Firefox, LibreOffice Calc, Paint), de naviguer sur le web, d'extraire des données météo, de créer des feuilles de calcul et de réaliser des tâches multi-étapes de manière autonome à partir de prompts textuels.
2) **Outils, sites ou dépôt GitHub cités :**
- **Claude 3.5 Sonnet / Claude 3.5 Haiku (Anthropic) :** Payant (via l'API Anthropic et des crédits de compte).
- **Docker / Docker Desktop :** Gratuit (docker.com), outil indispensable pour exécuter l'environnement conteneurisé de démonstration *computer-use*.
- **Console Anthropic (console.anthropic.com) :** Gratuit pour la création de compte et de clés API (nécessite d'ajouter des crédits/financements).
- **LibreOffice Calc :** Gratuit / Open source, tableur manipulé par l'agent IA.
- **Firefox :** Gratuit, navigateur utilisé par l'agent IA pour chercher la météo ou des images sur Google.
- **Paint / KolourPaint :** Gratuit, logiciel de dessin testé par l'agent IA.
- **FutureTools.io (futuretools.io) :** Gratuit, site de l'auteur pour retrouver des actualités, des outils d'IA et une base de données de monétisation.
3) **Astuces concrètes et réutilisables :**
- Configurer un conteneur **Docker** sur son ordinateur et y injecter une clé API Anthropic pour tester localement la fonctionnalité *Computer Use* via l'adresse `localhost:8080`.
- Donner des instructions textuelles complexes en plusieurs étapes à l'agent IA (ex: « Trouve la météo à San Diego pour les 3 prochains jours, crée un tableur Calc avec les dates, températures max et min, et sauvegarde le fichier »).
- Comprendre que l'agent fonctionne par boucles : il reçoit une commande, prend une capture d'écran de l'ordinateur virtuel, analyse l'état, décide de l'action suivante (clic, frappe clavier, scroll) et répète jusqu'à l'obtention du résultat.
- Gérer les limites de taux d'utilisation (*Rate Limits*) de l'API Anthropic en approvisionnant son compte (passer du niveau Free au Tier 1 ou supérieur) pour éviter les erreurs de type 429 lors de l'exécution de processus longs impliquant de nombreuses requêtes par minute.
- Utiliser le site de l'auteur (*futuretools.io*) pour accéder à la newsletter gratuite et à la base de données d'outils d'IA générateurs de revenus.
4) **Chiffres de revenus annoncés :**
- *Non précisé* (l'auteur mentionne uniquement ses propres dépenses pour les tests d'API : environ 1,49 $ à 25 $ de rechargement de crédits pour les tests de l'agent, et un coût global de test estimé à environ 1,50 $ pour la session de démonstration).
