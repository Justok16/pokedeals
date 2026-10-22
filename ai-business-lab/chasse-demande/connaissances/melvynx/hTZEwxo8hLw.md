# Mon Setup OpenClaw pour Coder : Tout via Telegram depuis n'importe où

Vidéo : https://youtu.be/hTZEwxo8hLw · durée 24:16 · résumé Gemini (gemini-3.5-flash-lite, lot de 5) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Utiliser un agent de code autonome (Cloud Bot / OpenClaw) piloté par des commandes vocales ou textuelles sur Telegram couplé à **Claude Code** pour automatiser la création de tâches et de pull requests sur des projets de développement.
2) **Outils, sites ou dépôts cités** :
   * **OpenClaw** / **Cloud Bot** (agent de code autonome, non précisé payant/gratuit).
   * **Telegram** (application de messagerie, gratuite).
   * **Gemini AI** / **Gemini 1.5 Pro** (modèle de langage, payant selon l'API, tarifs mentionnés : ~$2 par million de tokens en entrée).
   * **Claude Code** / **Claude** (outil de code, tarification par tokens non précisée en globalité, mais détails de consommation de tokens mentionnés : ex. ~3,8 millions de tokens, API à $25 par million de tokens de sortie, etc.).
   * **Liuma.io** (plateforme de marketing e-mail propulsée par l'IA, non précisée payant/gratuit).
   * **Dub** (service de raccourcissement de liens avec UTM, non précisé).
   * **GitHub** (plateforme de gestion de code, gratuite/payante).
   * **mlv.sh/fa** (lien vers une formation/masterclass payante sur Claude Code, non précisé le tarif exact).
3) **Astuces concrètes et réutilisables** :
   * Lancer des tâches de code en arrière-plan à l'aide de scripts cron configurés pour vérifier régulièrement l'avancement via l'IA.
   * Utiliser des workflows asynchrones où l'agent gère les modifications, crée les branches, lance les tests, et fusionne la pull request de manière autonome.
   * Utiliser des outils d'API personnalisés (MCP / Tool APIs) pour interagir avec des services tiers (comme Liuma.io ou Dub) directement depuis les scripts de l'agent.
4) **Chiffres de revenus affirmés par l'auteur** : Aucun chiffre de revenu personnel n'est affirmé.
