# Je teste OpenAI Codex pour la première fois ! (c'est dingue)

Vidéo : https://youtu.be/pxqnojSVyz8 · durée 13:34 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : L'auteur teste **Codex** (le nouvel outil d'OpenAI basé sur ChatGPT pour exécuter des tâches de développement de manière agentique sur un dépôt GitHub) en essayant de migrer un service d'envoi d'e-mails de Resend vers AWS SES, tout en évaluant ses fonctionnalités, sa gestion des environnements et ses limites par rapport à Cursor.

2) **Outils, sites et dépôts GitHub cités** :
- **Codex (OpenAI)** : Outil de développement propulsé par l'IA pour assigner des tâches et générer des pull requests sur des dépôts de code. (Payant : abonnement à 20 $/mois mentionné par l'auteur).
- **ChatGPT** : Assistant conversationnel d'OpenAI. (Gratuit / Payant).
- **Resend** : Service d'envoi d'e-mails (utilisé initialement dans le projet). (Modèle freemium/payant).
- **AWS SES** : Service d'e-mails d'Amazon (cible de la migration). (Payant à l'usage).
- **Cursor** : Éditeur de code concurrent basé sur l'IA (mentionné pour comparaison). (Modèle tarifaire non précisé).
- **GitHub** : Plateforme d'hébergement de code source (intégrée avec Codex). (Gratuit / Payant).
- **Vercel** : Plateforme de déploiement (mentionnée pour les vérifications de CI). (Gratuit / Payant).
- **shadcn/ui** : Bibliothèque de composants (mentionnée lors de la consultation de la documentation). (Gratuit).

3) **Astuces concrètes et réutilisables** :
- Configurer les variables d'environnement, les secrets et les scripts de setup (` npm install`) dans l'interface de l'outil agentique pour lui permettre d'installer les dépendances et d'exécuter le code.
- Créer des compétences personnalisées ("Custom Skills") dans l'outil pour définir des instructions spécifiques (par exemple, un correcteur orthographique ou grammatical pour les commentaires de code).
- Décomposer les tâches complexes en plusieurs tickets ou instructions claires pour l'agent afin de minimiser les erreurs de refactoring global.
- Utiliser les fonctionnalités de Pull Request générées automatiquement par l'agent pour examiner les modifications ligne par ligne (diff) avant de les fusionner dans la branche principale.

4) **Chiffres de revenus annoncés** :
- **Affirmé par l'auteur** : Aucun chiffre de revenus n'est annoncé dans cette vidéo (l'auteur mentionne uniquement le coût de l'abonnement à 20 $/mois pour l'outil).

---
