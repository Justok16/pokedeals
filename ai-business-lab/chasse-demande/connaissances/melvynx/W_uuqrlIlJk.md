# LE TUEUR DE DIA : Aside Browser, le premier "vrai" AI Browser ?

Vidéo : https://youtu.be/W_uuqrlIlJk · durée 17:21 · résumé Gemini (gemini-3.6-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale

La vidéo évalue le navigateur web orienté IA **Aside**, qui promet d'exécuter des actions de manière autonome sur Internet (connexion aux sites, gestion des e-mails, achats, etc.). L'auteur conclut que les navigateurs IA actuels restent trop lents et inefficaces pour les tâches complexes, notamment en raison des blocages liés à la double authentification (2FA). Il préconise plutôt l'utilisation d'outils et d'agents IA spécialisés pour les développeurs (comme **Claude Code**, **Codex** ou **TestSprite**) et promeut sa formation pour apprendre à créer des automatisations et coder avec l'IA.

---

### 2) Outils, sites et dépôts cités

*   **Aside** (`aside.com`)
    *   **Statut :** Payant (offre gratuite limitée à 500 crédits/mois ; formule Pro à 20 $/mois ; formule Max à 200 $/mois. Permet aussi d'associer ses abonnements existants).
    *   **Utilisation :** Navigateur web intégrant un assistant IA capable d'interagir avec les pages web (lecture d'e-mails, recherche d'offres sur Amazon, interaction avec des applications).
*   **TestSprite** (`testsprite.com`)
    *   **Statut :** Essai gratuit d'un mois / Payant.
    *   **Utilisation :** Outil de test automatisé (E2E, API, régression) pour les applications et agents IA. Il s'intègre au terminal et à **Claude Code** via un serveur MCP (`/testsprite-verify`) pour générer et exécuter des tests avec preuves vidéo/captures d'écran.
*   **ChatGPT / OpenAI** (`auth.openai.com`)
    *   **Statut :** Payant (abonnements connectables dans Aside).
    *   **Utilisation :** Moteur de modèle d'IA (GPT-4.5 / GPT-5 mentionnés) utilisable dans le navigateur Aside ou pour le codage.
*   **Claude / Anthropic** (`claude.ai`)
    *   **Statut :** Payant (abonnements connectables).
    *   **Utilisation :** Modèle IA / agent utilisé en développement (avec Claude Code) et pour la génération de scripts.
*   **1Password**
    *   **Statut :** Non précisé (service tiers).
    *   **Utilisation :** Gestionnaire de mots de passe intégré pour permettre à un agent IA d'avoir accès aux identifiants sans exposer les clés en clair.
*   **OpenClaw** (mentionné verbalement)
    *   **Statut :** Non précisé.
    *   **Utilisation :** Agent/outil d'automatisation cité comme alternative plus performante aux navigateurs IA.
*   **Claude Code / Codex / Cursor**
    *   **Statut :** Non précisé dans le détail des prix.
    *   **Utilisation :** Outils d'aide au développement et agents IA pour écrire du code et automatiser des workflows de développement.
*   **Formation "Deviens AI Engineer"** (`mlv.sh/fa`)
    *   **Statut :** Payant.
    *   **Utilisation :** Formation proposée par l'auteur pour apprendre à maîtriser les outils d'IA (Claude Code, Codex, Cursor, MCP) et créer des applications/automatisations.

---

### 3) Astuces concrètes et réutilisables

*   **Automatisation des tests avec Claude Code & MCP :** Configurer la CLI TestSprite dans son projet (`testsprite setup` avec la clé API), puis demander directement à Claude Code d'exécuter des requêtes de vérification (`/testsprite-verify`). Cela génère des scénarios de test complets enregistrés en vidéo sans rédaction manuelle de scripts.
*   **Éviter de repayer des abonnements IA dans les wrappers :** Dans les outils comme Aside, choisir l'option d'association de compte (*Bring Your Own Subscription*) pour utiliser son abonnement ChatGPT Plus/Pro ou Claude sans payer un surcoût mensuel.
*   **Sécuriser les actions d'un agent IA :** Lors de l'utilisation d'un agent IA ayant accès au navigateur, configurer des autorisations strictes (ex: option *Final confirm*) pour que l'agent demande une confirmation humaine avant toute suppression, envoi de message ou paiement.
*   **Privilégier les agents CLI pour la rapidité :** Pour automatiser des tâches complexes ou du code, privilégier les agents en ligne de commande (Claude Code, OpenClaw, Codex) plutôt que les navigateurs IA basés sur l'analyse visuelle, qui souffrent actuellement de lenteurs importantes et de blocages sur la 2FA.

---

### 4) Chiffres de revenus annoncés

*   Revenus générés direct/méthode : **non précisé**.
*   *Autres chiffres mentionnés dans la vidéo :*
    *   Poste d'« AI Engineer » présenté avec un potentiel de rémunération allant jusqu'à **200 000 $+/an** (*affirmé par l'auteur / affiché sur sa page de formation*).
    *   **14 000 personnes** ont rejoint la formation d'AI Engineer de l'auteur (*affirmé par l'auteur*).
    *   Une vidéo X d'un créateur (Michael) mentionnée comme ayant fait **660 000 vues** (*affirmé par l'auteur*).
