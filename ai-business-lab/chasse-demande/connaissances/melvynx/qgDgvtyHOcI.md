# Supprime ton AGENTS.md maintenant ou continue de faire de la m...

Vidéo : https://youtu.be/qgDgvtyHOcI · durée 16:15 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé demandé :

1. **Idée principale** :
   La vidéo explique que la gestion de la mémoire (fichiers `agents.md`, `CLAUDE.md`, etc.) est souvent mal faite. De nombreux développeurs y incluent du contenu inutile ou obsolète, ce qui « pollue » l'IA et nuit à la qualité du code. L'auteur montre comment auditer et nettoyer ces documentations pour obtenir de meilleurs résultats avec Claude Code et d'autres agents IA, en insistant sur le fait que la base de code existante prime sur les règles textuelles.

2. **Outils, sites et dépôts GitHub cités** :
   * **Claude Code** (outil IA, tarification non précisée dans la vidéo) : Assistant de codage en ligne de commande.
   * **Raycast** (outil, tarification non précisée) : Lanceur d'applications et d'outils.
   * **Zed** (éditeur de code, tarification non précisée) : Éditeur de code.
   * **GitHub** (plateforme de code, modèle freemium) : Hébergement de code source.
   * **Next.js** (framework, open-source / gratuit) : Framework React.
   * **Shadcn/ui** (bibliothèque de composants, open-source / gratuit) : Composants d'interface utilisateur.
   * **Prisma** (ORM, modèle freemium) : Gestionnaire de base de données.
   * **PostgreSQL** (base de données, open-source / gratuit) : Système de gestion de base de données.
   * **Vercel** (plateforme de déploiement, modèle freemium) : Hébergement et déploiement.
   * **Stripe** (outil de paiement, payant par commission) : Gestion des paiements en ligne.
   * **Vitest / Playwright** (outils de test, open-source / gratuit) : Tests unitaires et end-to-end.
   * **Mailersend / MailerLite** (outils d'emailing, payant) : Gestion des emails.
   * **Formation Nostack** (programme de formation créé par l'auteur, **payant : 5 € par mois**, avec un premier lien gratuit pour la formation) : Boilerplate et formation pour créer une stack SaaS sans code complexe avec l'IA.

3. **Astuces concrètes et réutilisables** :
   * **Auditer la mémoire de l'agent** : Créer un script (ou utiliser un outil comme `audit-memories`) pour analyser tous les fichiers Markdown et HTML de documentation afin de détecter les contradictions, les références obsolètes ou les liens brisés.
   * **Désactiver l'invocation implicite des skills** : Dans les fichiers de configuration YAML des skills, ajouter `disable-model-invocation: true` pour empêcher l'IA d'appeler des sous-compétences sans autorisation, ce qui évite d'encombrer le contexte avec des descriptions inutiles.
   * **Alléger le fichier `agents.md` / `CLAUDE.md`** : Supprimer le code verbeux, les listes de commandes redondantes et les documentations obsolètes. Conserver uniquement la source de vérité (stack technique actuelle, commandes essentielles et règles de sécurité strictes).
   * **Centraliser et ranger les skills** : Éviter d'avoir des skills globaux mal rangés ; les déplacer dans des dossiers de projets spécifiques (par exemple dans le projet de vidéo-editing) pour ne les charger qu'en cas de besoin.

4. **Chiffres de revenus annoncés (affirmés par l'auteur)** :
   * **Non précisé** (aucun chiffre de chiffre d'affaires ou de revenus personnels n'est mentionné, hormis le tarif de la formation à 5 € par mois).
