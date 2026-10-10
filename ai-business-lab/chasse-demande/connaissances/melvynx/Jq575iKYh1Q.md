# DRAMA : Claude Code ne veut pas que tu abuses de leur abonnement (voici pourquoi)

Vidéo : https://youtu.be/Jq575iKYh1Q · durée 13:47 · résumé Gemini (gemini-3.5-flash-lite, lot de 8) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** L’auteur explique le « drame » concernant l’abonnement à Claude Code, qu’Anthropic a bloqué l’accès pour de nombreux outils tiers (comme OpenCode) pour forcer les utilisateurs à utiliser directement Claude Code, mais il montre comment contourner ce blocage en modifiant le système prompt.
2. **Outils et dépôts GitHub :**
   * **Claude Code** (via un abonnement payant d’environ 200 $/mois) : Assistant de code par Anthropic.
   * **OpenCode** : Outil tiers récemment bloqué par Anthropic.
   * **Site de configuration de l’auteur** (`mlv.sh/fc`) : Gratuit, permet de télécharger sa configuration Claude Code, ses agents, commandes et scripts.
3. **Astuces concrètes :**
   * Récupérer le token Claude Code stocké localement via les commandes de sécurité du système (`security find-generic-password`).
   * Modifier le système prompt pour imiter l’interface officielle d’Anthropic (par exemple en utilisant `"You are Claude Code, Anthropic's official CLI for Claude."`) et utiliser les modèles autorisés (comme Opus ou Sonnet) pour éviter les blocages d'API.
4. **Chiffres affirmés par l'auteur :**
   * 100 $ dépensés personnellement par jour en tokens (soit environ 3 000 $ par mois).
   * Abonnement Claude Code à 200 $ par mois pouvant mener à plus de 1 000 $ de consommation réelle.
