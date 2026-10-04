# J'abandonne Claude Code pour Codex... je te présente ça

Vidéo : https://youtu.be/RGR5jTyyPuI · durée 28:02 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur explique pourquoi il a abandonné l'utilisation principale de **Claude Code** pour migrer sur l'application **Codex** (OpenAI). Selon lui, l'abonnement forfaitaire à 200 $/mois (plan 20x / Pro) offre un rapport coût/utilisation imbattable par rapport au paiement au token de l'API Claude Opus (ou Claude Code). L'intérêt majeur repose sur la capacité de Codex à exécuter en parallèle plusieurs agents autonomes en multitâche (via des *worktrees* Git indépendants), capables de travailler en autonomie pendant plusieurs dizaines de minutes ou heures (tests, refactoring complet d'applications, vérification visuelle par navigateur intégré) sans intervention constante de l'humain.

---

### 2) Outils, sites et dépôts cités

* **Codex (Desktop App & CLI / OpenAI)** :
  * *Statut* : Payant (l'auteur utilise la formule à 200 $/mois avec le modèle de type GPT-5.5 / Spark).
  * *Usage* : Application de bureau et CLI d'agents IA pour piloter le code, lancer des sous-agents en parallèle, interagir avec le terminal, réviser des diffs et naviguer sur le web.
* **Claude Code (Anthropic)** :
  * *Statut* : Payant (au token ou via abonnement Anthropic).
  * *Usage* : CLI de codage par agent IA d'Anthropic (utilisé comme point de comparaison).
* **Cursor** :
  * *Statut* : Freemium / payant (*prix non précisé dans la vidéo*).
  * *Usage* : Éditeur de code assisté par IA.
* **Zed (zed.dev)** :
  * *Statut* : Gratuit (l'éditeur en lui-même) / intégration nécessitant un abonnement ChatGPT/Codex.
  * *Usage* : Éditeur de code léger supportant l'agent Zed connecté aux quotas de l'abonnement OpenAI.
* **OpenClaw (Hermes)** :
  * *Statut* : Gratuit / projet open source ou script interne (*détails exacts non précisés*), branché sur l'abonnement pour éviter le coût API.
  * *Usage* : Agent IA autonome tournant 24h/24 pour exécuter des tâches continues en arrière-plan.
* **Artificial Analysis (artificialanalysis.ai)** :
  * *Statut* : Gratuit (site web d'information).
  * *Usage* : Plateforme indépendante de benchmarks mesurant l'intelligence, la vitesse et le coût des modèles d'IA pour le code.
* **Excalidraw (app.excalidraw.com)** :
  * *Statut* : Gratuit / Freemium (version Plus visible).
  * *Usage* : Tableau blanc virtuel utilisé pour la prise de notes pendant la présentation.
* **Better Auth** :
  * *Statut* : Gratuit / open-source.
  * *Usage* : Système d'authentification TypeScript (utilisé dans la démo pour implémenter les Passkeys).
* **Convex** :
  * *Statut* : Backend-as-a-service / base de données temps réel (*tarification exacte non précisée*).
  * *Usage* : Gestion des données et exécution du backend des applications montrées.
* **TanStack Start** :
  * *Statut* : Gratuit / open-source.
  * *Usage* : Framework React fullstack vers lequel l'auteur fait migrer ses projets Next.js.
* **CodeLynx / Plateforme de formation (`mlv.sh/fc` ou `codelynx.dev`)** :
  * *Statut* : Payant (*montant exact non précisé*).
  * *Usage* : Pack de scripts, commandes CLI et agents personnalisés configurés pour Claude Code, Codex et Cursor.
* **Dépôts / Projets de l'auteur montrés à l'écran** :
  * `nowstack-saas` : Boilerplate SaaS de l'auteur.
  * `tchao-app` / `tchao.app` : Application Web de l'auteur en cours de refactoring.
  * `thumbfa.st` : SaaS de génération de miniatures.

---

### 3) Astuces concrètes et réutilisables

1. **Isolation par *Worktrees* Git** : Plutôt que de faire travailler l'agent sur la branche courante, configurez des *worktrees* Git indépendants. Chaque sous-agent dispose ainsi de sa copie isolée du dépôt et peut travailler en parallèle sans bloquer votre espace de travail.
2. **Environnements de test jetables et isolés (`environment.toml`)** : Configurer un script d'environnement qui, à la création d'un worktree, clone les variables d'environnement, génère un port dédié (ex. `localhost:3010` au lieu de `3004`), lance un backend isolé (ex. instance dev Convex dédiée) et injecte un cookie de session séparé. Cela permet de tester simultanément plusieurs variantes de l'application sans conflit de sessions ou de base de données.
3. **Gestion unifiée des compétences/agents via des liens symboliques (*symlinks*)** :
   * Regrouper tous les prompts d'agents et compétences (*skills*) dans un dossier unique central (ex. `~/.agents/`).
   * Créer un lien symbolique (*symlink*) vers ce dossier dans `~/.claude/` et dans la configuration de Codex. Toute modification apportée à une compétence ou à un agent est ainsi instantanément synchronisée sur tous vos outils IA.
4. **La commande `/goal` (ou "Send as goal")** : Structurer les demandes sous forme d'objectifs fermés avec critères de validation (tests Playwright/Vitest, vérifications TypeScript, vérification visuelle dans le navigateur). L'agent boucle et itère en autonomie jusqu'à ce que les critères soient verts.
5. **Vérification visuelle intégrée (*In-app Browser*) avec capture de contexte** : Utiliser le navigateur intégré pour inspecter le rendu local et annoter directement une zone défectueuse à l'écran. L'outil transmet la capture d'écran ciblée et l'élément DOM sélectionné directement à l'agent pour correction.
6. **Utiliser Claude pour le design UI et Codex pour la logique lourde** : L'auteur note que la génération purement visuelle/UI reste supérieure chez Claude, tandis que Codex excelle sur les refactorings d'architecture, la correction de bugs complexes et l'endurance sur les longues sessions.

---

### 4) Chiffres de revenus annoncés

* **Revenus directs / Gains générés** : **Aucun chiffre de revenus n'est mentionné dans la vidéo** (*non précisé*).
* **Économies de coûts et dépenses affirmées par l'auteur** :
  * Coût de l'abonnement Codex : **200 $/mois** (*affirmé par l'auteur*).
  * Économie estimée sur la consommation de tokens API (OpenClaw / Opus) : entre **1 000 $ et 2 000 $ / mois** (*affirmé par l'auteur*).
  * Consommation équivalente théorique en tokens API absorbée par son forfait en une journée : **578,96 $** le 15 mai et **387,71 $** le 16 mai (*affirmé par l'auteur*).
