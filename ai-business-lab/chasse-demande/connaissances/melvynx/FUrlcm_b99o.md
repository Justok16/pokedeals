# NOUVEAU : La commande qui tiens plus longtemps que toi 🍆

Vidéo : https://youtu.be/FUrlcm_b99o · durée 19:59 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
La vidéo présente la commande **/goal** (disponible dans Codex et Claude Code CLI). Contrairement à un échange classique où l’IA effectue une tâche puis s'arrête en attendant la validation humaine, la commande `/goal` force l'agent à travailler en boucle autonome : **Travailler $\rightarrow$ Vérifier $\rightarrow$ Prochaine étape $\rightarrow$ Boucler jusqu'à ce que la condition de validation soit atteinte** (ou qu'un échec avéré soit constaté). Cela permet de déléguer des tâches complexes et longues (corrections de tests/linter, refactoring, déploiement) sans supervision continue.

---

### 2) Outils, sites et dépôts cités

* **Codex (OpenAI)** : Outil/agent de programmation autonome basé sur les modèles OpenAI. *(Modèle économique : payant / consommation de jetons API - non précisé en détail dans la vidéo)*.
* **Claude Code (Anthropic)** : Interface CLI en ligne de commande pour piloter Claude (ex. Opus 4.7 / 3.5 Sonnet) directement dans le terminal. *(Modèle économique : payant via API / jetons - non précisé en détail dans la vidéo)*.
* **Excalidraw (`app.excalidraw.com`)** : Application de dessin vectoriel et de schématisation utilisée par l'auteur pour expliquer les flux d'agents. *(Gratuit / freemium)*.
* **Site de formation / AI Blueprint (`mlv.sh/formation-ai` ou `codelynx.dev`)** : Plateforme de l'auteur vendant une formation et des configurations prêtes à l'emploi pour les agents IA (Claude Code, Codex, Cursor). *(Payant)*.
* **OpenAI Developers Documentation (`developers.openai.com`)** : Page documentaire montrant l'implémentation et le cycle de vie de la commande `Goals in Codex`. *(Gratuit)*.
* **GitHub** : Plateforme de versioning où sont exécutés les tests d'intégration continue (CI) et les Pull Requests vérifiées par l'IA. *(Freemium)*.
* **Vercel** : Plateforme d'hébergement web utilisée pour vérifier la réussite des builds et des déploiements preview/production. *(Freemium)*.
* **Playwright** : Outil d'automatisation de tests end-to-end exécuté par l'IA pour valider les checks. *(Gratuit / Open-source)*.
* **TypeScript & ESLint** : Compilateur/linter de code vérifié par l'agent pour éliminer les erreurs et warnings. *(Gratuit / Open-source)*.
* **TanStack Start & Next.js** : Frameworks web servant d'exemples lors d'une migration/refactor de code. *(Gratuit / Open-source)*.
* **Convex & Neon Postgres / Prisma** : Outils de base de données et backend cités lors des exemples de refactorisation. *(Freemium / Open-source)*.
* **Utilitaires CLI (`curl`, `sips`, `magick / ImageMagick`)** : Commandes terminal exploitées par l'agent pour redimensionner des favicons/logos et tester des endpoints HTTP. *(Gratuits)*.

---

### 3) Astuces concrètes et réutilisables

1. **Structure optimale du prompt `/goal`** :
   ```text
   /goal <résultat attendu> vérifier par <évidence/preuve> tout en respectant <contraintes>
   ```
2. **Définir une « évidence » mesurable et prouvable** :
   * L'agent ne doit pas s'arrêter sur une simple supposition. Il faut lui indiquer comment tester : exécuter une commande (`pnpm test`, `tsc`, `eslint`), surveiller un check GitHub, inspecter un build Vercel, ou utiliser un outil de navigation headless (Dev Browser).
3. **Spécifier des contraintes explicites anti-triche** :
   * Les modèles d'IA peuvent avoir tendance à « tricher » pour valider un objectif (ex. désactiver les règles ESLint, supprimer des fichiers de test ou vider des pages). Spécifiez toujours : *« Ne triche pas, ne désactive pas les règles, ne supprime aucune vue/page »*.
4. **Quand utiliser `/goal`** :
   * **À utiliser pour** : Résolution de tous les checks CI d'une PR, refactorings d'envergure (ex. migration de dépendances), correction intégrale des erreurs de typage et de linting, implémentation d'une feature avec tests.
   * **À éviter pour** : Questions simples, one-line fixes rapides, réflexions/planifications ou tâches dont le résultat ne peut pas être testé automatiquement.
5. **Relance en cas de blocage** :
   * Si l'agent reste en attente ou s'arrête prématurément alors que le goal est actif, taper simplement `continue` dans le prompt pour forcer la reprise du cycle de vérification.

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de revenus n'est mentionné** dans la vidéo (*non précisé*).
* *(Mention connexe : la page de vente affichée à l'écran promet une « économie de 500h de R&D » grâce aux configurations fournies, affirmé par l'auteur).*
