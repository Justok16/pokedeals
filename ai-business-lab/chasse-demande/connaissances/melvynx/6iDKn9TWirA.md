# LES DEVS ARRÊTENT D'UTILISER CLAUDE : c'est de pire en pire...

Vidéo : https://youtu.be/6iDKn9TWirA · durée 22:07 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
Anthropic a modifié la tarification et les limites d'utilisation programmatique de **Claude Code / Agent SDK**, réduisant drastiquement les quotas inclus dans les abonnements et facturant l'excédent au tarif API. L'auteur explique pourquoi et comment il a réorganisé son workflow en basculant une grande partie de son développement sur **Codex (OpenAI)** pour les tâches lourdes et l'automatisation par agents (meilleur rapport coût/limite d'utilisation), tout en conservant **Claude** pour le design front-end, et comment rendre ses projets compatibles avec les deux écosystèmes.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité / Rôle |
| :--- | :--- | :--- |
| **Claude Code / Claude Agent SDK / `claude -p`** (Anthropic) | **Payant** (plans de 20 $ à 300 $/mois selon le palier Pro/Team/Max + facturation API au-delà des crédits) | CLI et SDK d'Anthropic pour faire exécuter des tâches de programmation et de modification de code par des agents IA. |
| **Codex / Codex App** (OpenAI) | **Payant** (abonnements à 20 $/mois ou 100 $/mois pour les gros volumes) | Outil et application desktop de codage par agents autonomes d'OpenAI. |
| **T3 Code** (`t3.codes` par Theo / t3.gg) | **Gratuit / Open source** | Interface et plan de contrôle open source pour orchestrer différents agents de code (Claude Code, Codex, OpenCode, Cursor). |
| **T3 Chat** (par Theo / t3.gg) | **Payant / Freemium** (non précisé en détail) | Application de chat IA créée par Theo. |
| **OpenClaw** & **Hermes Agent** | **Non précisé** (outils open source / communautaires) | Outils d'agents autonomes utilisables notamment via Telegram pour exécuter des commandes et automatiser du code. |
| **Cursor** | **Freemium / Payant** | Éditeur de code assisté par IA, utilisé par l'auteur comme solution de secours (*fallback*) lorsque les quotas d'autres outils sont atteints. |
| **Zed / Zed Agents** | **Gratuit / Freemium** | Éditeur de code léger avec intégration d'agents IA, utilisé pour les petites modifications rapides. |
| **Codex Monitor** (par Thomas Ricouard / `@Dimillian`) | **Gratuit / Open source** | Application macOS/iOS permettant de monitorer et gérer les agents Codex. |
| **NowStack** (`nowstack.melvynx.dev` / `codelynx.dev/nowstack`) | **Payant** | Boilerplate et formation de l'auteur pour créer des SaaS en une semaine (TanStack Start, Convex, Tailwind, etc.). |
| **Excalidraw** (`app.excalidraw.com`) | **Freemium** | Tableau blanc virtuel utilisé pour illustrer la transition de stack et les données de consommation de tokens. |
| **CodeLynx / Liens de l'auteur** (`codelynx.dev/coding-tools`, `mlv.sh/coding`, `mlv.sh/fn`) | **Gratuit** (accès aux listes et waitlists) | Pages récapitulatives de la stack technique de l'auteur et inscription à la bêta de NowStack. |

---

### 3) Astuces concrètes et réutilisables

1. **Rendre son projet agnostique (Symlinks Claude $\leftrightarrow$ Codex) :**
   * Placer les compétences dans `agents/skills` et créer un lien symbolique (*symlink*) vers `.claude/skills`.
   * Faire de même entre `agents/AGENTS.md` (pour Codex/outils génériques) et `CLAUDE.md`. Une simple commande passée à l'agent permet de migrer tout le projet d'un coup.
2. **Architecture modulaire des règles (`Rules Index`) :**
   * Au lieu de surcharger le fichier principal d'instructions, créer un index de règles dans `AGENTS.md` renvoyant vers des fichiers dédiés dans un dossier `agents/rules/` (ex. `rules-auth.md`, `rules-styling.md`, `rules-convex.md`). L'agent ne charge que les fichiers pertinents selon la tâche, économisant ainsi du contexte et des tokens.
3. **Création de *Skills* "One-Shot" :**
   * **`init-project`** : Automatiser l'initialisation complète d'un projet (création du dépôt GitHub via `gh`, configuration de la base de données / Convex, choix du thème Shadcn UI, configuration Cloudflare R2 et premier push).
   * **`setup-stripe`** : Automatiser la liaison des clés API Stripe et la configuration des paiements.
4. **Séparation des rôles selon les forces des LLMs :**
   * Utiliser **Codex / OpenAI** pour les tâches d'infrastructure, de backend, d'exécution longue et de refactorisation lourde (bénéficie de limites de tokens plus généreuses à coût fixe).
   * Utiliser **Claude** spécifiquement pour le design d'interface et le front-end (Tailwind CSS, composants Shadcn UI), domaine où il reste supérieur.

---

### 4) Chiffres de revenus annoncés
* **Revenus directs générés :** *Non précisé* (aucun chiffre d'affaires ou revenu personnel n'est mentionné dans la vidéo).
* **Dons/Engagements tiers cités :** Theo a promis d'offrir 10 $ à l'open source par personne résiliant Claude Code (dans la limite de 20 000 $, soit 2 000 personnes) (*affirmé par l'auteur*).
