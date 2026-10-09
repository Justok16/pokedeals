# Je teste ClawdBOT pour la première fois (Ok, je suis vraiment choquée)

Vidéo : https://youtu.be/AqntsJbJqv0 · durée 31:28 · résumé Gemini (gemini-3.5-flash-lite, lot de 6) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : La vidéo présente **Moltbot** (ex-Clawbot), un assistant IA open source qui permet de contrôler son ordinateur (applications, mails, calendrier, Telegram, etc.) et même d'interagir avec d'autres intelligences artificielles via une interface web ou des applications de messagerie. L'auteur explique comment installer, configurer et utiliser l'outil, tout en soulignant les risques de sécurité inhérents à un tel niveau d'accès.

2) **Outils, sites et dépôts GitHub cités** :
- **Moltbot** (ex-Clawbot / Molt Dev) : Gratuit (open source), assistant IA permettant de contrôler un ordinateur et d'exécuter des actions à distance.
- **Telegram** : Gratuit, application de messagerie utilisée pour interagir avec le bot.
- **Claude Code CLI** : Outil payant (nécessite un abonnement/clé API Claude), interface en ligne de commande utilisée pour alimenter le bot en logique conversationnelle et de code.
- **Brave Search** : Outil de recherche web (nécessite une clé API pour certaines fonctionnalités).
- **GitHub** : Dépôts et liens pour récupérer les configurations.
- **Thumbfa.st** : Site web payant/freemium (générateur de miniatures YouTube utilisé pour un exemple de test de code).
- **Vercel** : Plateforme d'hébergement et de déploiement (utilisée pour les tests de code).
- **ElevenLabs** : Outil de synthèse vocale (testé pour les messages audio).

3) **Astuces concrètes et réutilisables** :
- Installer et configurer Moltbot via la ligne de commande (`curl`) pour l'associer à Telegram et à un modèle d'IA (Claude Code).
- Gérer les intégrations de services (Telegram, Google, etc.) à l'aide de clés API (API keys) pour automatiser des tâches du quotidien (gestion des e-mails, recherches web, modifications de code).
- Configurer des "skills" (compétences) modulaires pour étendre les capacités du bot (gestion de fichiers PDF, recherche Google, interactions avec GitHub, etc.).
- Sécuriser l'environnement d'exécution (notamment via l'utilisation de conteneurs Docker pour le "sandboxing") afin d'éviter qu'un agent IA compromette l'ensemble du système d'exploitation.

4) **Chiffres de revenus annoncés** :
- Non précisé.
