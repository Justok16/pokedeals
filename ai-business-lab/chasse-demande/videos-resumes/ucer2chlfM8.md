# Utiliser Claude et Codex ensemble

Vidéo : https://youtu.be/ucer2chlfM8 · envoyée par l'utilisateur le 28/09/2026 · résumé Gemini (gemini-3-flash-preview) du 2026-09-28
(chiffres et affirmations des auteurs : non vérifiés)

### 1) L'idée principale
L'idée centrale est qu'il ne faut pas choisir entre les modèles d'IA, mais les utiliser en tandem pour maximiser la productivité. L'auteur propose une synergie où **Claude (Opus 5.5)** sert de planificateur et de moteur de création principal, tandis que **GPT-6 Astra (Codex)** intervient comme réviseur critique et exécuteur de tâches complexes (comme la gestion des connexions ou l'analyse de sécurité) pour livrer des projets de niveau professionnel.

### 2) Outils, sites et dépôts GitHub
*   **Claude Code / Claude Opus 5.5** : (Anthropic) - Payant. Sert de « daily driver » pour la planification, la rédaction de code et la création de fonctionnalités.
*   **GPT-6 Astra / Codex** : (OpenAI) - Payant. Utilisé pour la révision de code, les tâches nécessitant des identifiants et l'exécution de processus longs.
*   **codex-plugin-cc (GitHub)** : Gratuit (dépôt `openai/codex-plugin-cc`). Plugin permettant d'intégrer les capacités de Codex directement dans l'interface de Claude Code.
*   **Gemini-skills (GitHub)** : Gratuit (dépôt cité). Outil que l'auteur utilisait auparavant pour les appels API, désormais remplacé par la combinaison Claude/Codex pour réduire les coûts.
*   **Skool (earlyaidopters)** : Site communautaire payant. Plateforme de l'auteur pour apprendre à devenir consultant en IA et vendre des solutions aux entreprises.

### 3) Astuces concrètes et réutilisables
*   **Le débat entre IA** : Demander à Claude de créer un plan (V1), puis demander à Astra de trouver les failles de ce plan. Répéter l'opération jusqu'à ce que les deux modèles soient d'accord.
*   **Gestion des identifiants** : Puisque Claude refuse souvent de manipuler des mots de passe ou des clés API par sécurité, déléguez spécifiquement ces étapes à Astra (Codex) qui est plus flexible (« plus chill »).
*   **Optimisation des coûts API** : Au lieu de payer pour des services tiers de génération d'images ou de diagrammes via API (comme Gemini), utilisez les capacités natives de Codex pour générer ces actifs et les réimporter dans Claude.
*   **Commandes de flux de travail** :
    *   Utilisez `/goal` avec Astra pour les problèmes complexes, en ajoutant une limite de temps (ex: « stop après 2 heures ») pour éviter la surconsommation de jetons.
    *   Utilisez `/handoff` à la fin d'une session pour générer un fichier `handoff.md` (résumé de l'état du projet).
    *   Utilisez `/prime` dans le second outil pour qu'il lise le fichier de transition et reprenne le travail exactement là où le premier s'est arrêté.

### 4) Chiffres de revenus annoncés
*   **Non précisé** : L'auteur mentionne qu'il est possible de gagner de l'argent en vendant des solutions IA aux entreprises ou en devenant consultant, mais il n'avance aucun chiffre de revenus précis ou de salaire dans cette vidéo.
