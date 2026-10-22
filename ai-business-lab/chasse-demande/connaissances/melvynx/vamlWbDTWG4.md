# PERSONNE ne comprend OpenClaw : voici le VRAI usage que j'en fais

Vidéo : https://youtu.be/vamlWbDTWG4 · durée 26:14 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, spécialement conçu pour tirer parti de l'IA et de Claude Code dans le cadre d'une activité professionnelle :

---

### 1) Idée principale
L'auteur démontre qu'**OpenClaw** (un système d'agents IA autonome piloté depuis Telegram) n'est pas un simple gadget, mais un véritable assistant opérationnel. Connecté à des outils comme **Claude Code** et à divers services via le protocole **MCP**, cet agent permet d'automatiser la gestion complète d'un business en ligne depuis son smartphone (résolution de bugs de code, rédaction de newsletters, traitement du support client, négociation de sponsorings et suivi personnel).

---

### 2) Outils, sites et dépôts GitHub cités

*   **OpenClaw** : *Gratuit / Open-source* (nécessite un serveur VPS).
    *   *Rôle* : Système d'agents IA exécuté sur un serveur, pilotable par Telegram, capable de gérer des tâches en autonomie et d'orchestrer d'autres outils.
*   **Claude Code (Anthropic)** : *Payant* (Abonnement cité : plan **Claude Code MAX à 200 $/mois** ; existe aussi à 20 $/mois).
    *   *Rôle* : Outil CLI d'Anthropic pour analyser, écrire, tester et corriger du code de manière autonome.
*   **Telegram** : *Gratuit*.
    *   *Rôle* : Messagerie servant d'interface principale entre l'utilisateur et ses agents OpenClaw.
*   **Lumail (`lumail.io`)** : *Gratuit / Payant* (offre gratuite jusqu'à 10 000 emails/mois visible à l'écran).
    *   *Rôle* : Plateforme d'email marketing conçue pour être pilotée par prompt/IA via des serveurs/skills MCP.
*   **MCP (Model Context Protocol)** : *Gratuit / Standard Open-source*.
    *   *Rôle* : Protocole permettant aux agents IA de se connecter directement aux API d'outils tiers.
*   **GitHub** : *Gratuit / Payant*.
    *   *Rôle* : Hébergement du code source et gestion des *Pull Requests* (PR) créées automatiquement par l'agent.
*   **Dub.sh** : *Gratuit / Payant*.
    *   *Rôle* : Service de raccourcissement de liens doté d'une intégration MCP.
*   **Vercel / Vercel CLI** : *Gratuit / Payant*.
    *   *Rôle* : Déploiement web et suivi de l'état des *builds* et déploiements.
*   **Codeline** : *Payant pour les clients* (Outil interne à l'auteur).
    *   *Rôle* : Plateforme de formation de l'auteur connectée à l'agent pour créer des coupons de réduction.
*   **Typefully** et **SaveIt.now** : *Gratuit / Payant (non précisé)*.
    *   *Rôle* : Outils de création/publication de contenu et de gestion de marque-pages intégrés via MCP.
*   **Site `mlvynx.sh/fo`** : *Gratuit*.
    *   *Rôle* : Site de l'auteur proposant un guide/formation gratuite pour installer le bot OpenClaw sur un VPS en 10-20 minutes.

---

### 3) Astuces concrètes et réutilisables

1.  **Pilotage du codage à distance (Mobile → VPS → GitHub) :**
    *   Signalez un bug ou une fonction à ajouter sous forme de message ou capture d'écran sur Telegram.
    *   OpenClaw lance une commande `claude -p` sur votre VPS. Claude Code corrige le problème, teste la solution et soumet une *Pull Request* sur GitHub.
    *   Il ne vous reste plus qu'à valider et fusionner la PR depuis votre téléphone.
2.  **Gestion des sponsorings avec validation humaine ("Human-in-the-Loop") :**
    *   L'agent (nommé "Steve") lit les emails entrants de marques, répond avec votre kit média et vos tarifs officiels.
    *   En cas de contre-proposition (ex: négociation de prix), l'agent vous envoie une alerte Telegram synthétique avec 3 choix : *Accept*, *Negotiate*, *Decline*.
    *   Répondez simplement "decline" sur Telegram, et l'agent se charge de rédiger un email de refus poli et professionnel.
3.  **Support client autonome sécurisé :**
    *   L'agent vérifie dans la base de données (via Lumail MCP) si le client a réellement acheté avant de lui réinventer l'accès ou de renvoyer le lien.
    *   Pour les actions financières sensibles (ex: remboursements Stripe), l'agent prépare le dossier et demande une confirmation manuelle explicite avant d'agir.
4.  **Mise à jour automatique de la mémoire (CRON Jobs) :**
    *   Configurez une tâche automatisée (CRON) toutes les 12 heures. L'agent balaye l'historique des conversations, extrait les informations clés et met à jour des fichiers Markdown de contexte (ex: `situation.md`). Ainsi, l'IA "apprend" votre vie et votre business au quotidien.
5.  **Éviter la surconsommation de quotas et les blocages :**
    *   **Proportion d'usage** : Ne faites pas 100 % de vos requêtes lourdes de code via l'agent OpenClaw (qui ne prend pas encore en compte le *prompt caching* de la même façon que le CLI direct). Alternez à ~50 % OpenClaw et 50 % Claude Code en local.
    *   **Mise à niveau** : Si vous atteignez une limite, effectuez les *upgrades* d'abonnement directement depuis votre terminal ou votre navigateur, jamais via des liens suggérés dans un prompt d'agent tiers (pour éviter les vérifications de sécurité).
6.  **Protection contre l'injection de Prompt (*Prompt Injection*) :**
    *   Utilisez des modèles de pointe très robustes (ex: gamme Claude 3.5 / 3.7 / Opus) pour traiter les contenus externes (emails). L'agent balise les entrées externes comme `Untrusted Input` afin de refuser d'exécuter des instructions malveillantes dissimulées dans les messages reçus.

---

### 4) Chiffres de revenus annoncés

*   **Tarif standard pour une intégration sponsorisée YouTube** : 1 000 $ *(affirmé par l'auteur)*.
*   **Offre de sponsoring négociée (refusée dans la démonstration)** : 600 $ pour une intégration de 90 secondes *(affirmé par l'auteur)*.
*   **Revenus globaux du business** : non précisé.
