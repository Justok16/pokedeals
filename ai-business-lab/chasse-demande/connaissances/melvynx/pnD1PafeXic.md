# Comment AVOIR Claude en illimité et arrêter de cramer tes limites

Vidéo : https://youtu.be/pnD1PafeXic · durée 26:08 · résumé Gemini (gemini-flash-lite-latest, lot de 3) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** 
Optimiser l'utilisation de Claude (avec notamment Claude Code et les modèles Opus, Sonnet, Haiku) et gérer les limites de tokens (limites de session, weekly) pour maximiser sa productivité sans détruire son abonnement ou exploser ses coûts.

2) **Outils, sites ou dépôts GitHub cités :**
- **Claude (Anthropic) / Claude Code :** Modèles d'IA (Haiku, Sonnet, Opus 5.5). L'accès aux modèles et aux abonnements est payant (ex : abonnement Claude à 200 $/mois, tarification au million de tokens selon les modèles).
- **agent-burn (agent-burn.melvynx.dev) :** Application gratuite pour monitorer son usage et ses limites (séances, weekly).
- **Artificial Analysis (artificialanalysis.ai) :** Site/outil gratuit permettant de comparer les performances, l'intelligence et le coût par tâche des modèles d'IA (benchmark mondial).
- **Tella MCP / MCP Tool / etc. :** Outils et serveurs d'intégration (MCP) mentionnés dans l'écosystème de Claude.

3) **Astuces concrètes et réutilisables :**
- **Monitorer son usage :** Utiliser des outils de suivi (comme *agent-burn*) pour surveiller sa consommation de tokens (limites de 5 heures et limites hebdomadaires) afin d'éviter d'être bloqué en plein travail.
- **Réduire le niveau d'effort ("Effort level") :** Ne jamais utiliser le niveau **Max** (comparé à un « poisson-chat débile » qui consomme énormément de tokens pour rien) pour les tâches courantes. Utiliser les modes **Low**, **Medium**, **Average** ou **High** selon la complexité, ce qui réduit drastiquement les coûts en tokens tout en conservant d'excellents résultats.
- **Croiser les données de tarification et d'intelligence :** Utiliser des comparateurs (comme *Artificial Analysis*) pour choisir le meilleur compromis (par exemple, un modèle de niveau supérieur avec un effort plus bas, ou un modèle intermédiaire comme Sonnet ou Opus en mode medium) plutôt de céder au réflexe du modèle maximal.
- **Mettre en place des "sub-agents" (sous-agents) :** Pour des tâches complexes (comme l'audit de compétences ou de code), déléguer à des sous-agents utilisant Haiku plutôt que de faire tout reposer sur un agent principal très coûteux, ce qui permet un gain de temps et d'efficacité considérable.
- **Ajuster le contexte et la lecture (Input/Output caching) :** Limiter le contexte (utiliser des fenêtres de contexte adaptées, par exemple éviter les modèles à 1 million de tokens si 200 000 suffisent) pour réduire le coût des lectures et écritures en cache.

4) **Chiffres de revenus annoncés :**
- Non précisés (l'auteur mentionne uniquement qu'il a dépensé environ 100 000 $ en usage d'IA sur ses abonnements/API, mais aucun chiffre de *revenus* gagnés n'est affirmé).

---
