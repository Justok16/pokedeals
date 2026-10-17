# Claude Desktop V2 : Ils ont tout copié de Cursor (et c'est bien)

Vidéo : https://youtu.be/iuNZTmH_-PQ · durée 24:56 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon vos exigences :

---

### 1) Idée principale
La vidéo présente la nouvelle interface Desktop de **Claude Code** (développée par Anthropic), fortement inspirée d'outils comme Cursor et Codex. L'objectif est de montrer comment exploiter cette interface pour faire du **"vibe coding" agentique et multitâche** : piloter plusieurs agents IA en parallèle, inspecter visuellement des composants web en un clic pour les envoyer dans le prompt, laisser l'IA planifier et auto-vérifier son propre code (via des captures d'écran et des tests), afin de développer des applications beaucoup plus rapidement.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Code / Claude Desktop App** (Anthropic)
    *   *Payant / Inclus dans l'abonnement Claude Pro/Team/Enterprise ou coût d'utilisation API.*
    *   *Usage :* Environnement de développement agentique et interface graphique pour coder avec le modèle Claude.
*   **Cursor**
    *   *Gratuit / Payant (Freemium - non détaillé dans la vidéo).*
    *   *Usage :* Éditeur de code avec IA, cité comme la référence dont s'inspire la nouvelle UI de Claude.
*   **Codex** (OpenAI)
    *   *Non précisé dans la vidéo.*
    *   *Usage :* Cité brièvement comme référence d'interface pour le développement assisté par IA.
*   **Site de formation / blueprint de l'auteur (`mlv.sh/fc` / `codelynx.dev`)**
    *   *Gratuit.*
    *   *Usage :* Page d'inscription pour télécharger gratuitement la configuration Claude Code privée de l'auteur (agents, skills, permissions, statusline) et accéder à des tutoriels d'installation (Windows/WSL et macOS/Linux).
*   **AI Blueprint (`github.com/Melvynx/aiblueprint`)**
    *   *Gratuit (Open Source).*
    *   *Usage :* Dépôt GitHub / outil CLI mentionné dans la formation de l'auteur pour configurer Claude Code.
*   **Next.js**
    *   *Gratuit (Open Source).*
    *   *Usage :* Framework React utilisé pour exécuter le serveur d'application frontend en local dans la fenêtre de prévisualisation.
*   **Convex**
    *   *Gratuit / Payant (Freemium).*
    *   *Usage :* Service de backend en temps réel exécuté en local pour l'application de démo.
*   **Zed**
    *   *Gratuit (Open Source).*
    *   *Usage :* Éditeur de code ouvert directement depuis l'interface Desktop de Claude pour inspecter les fichiers.
*   **VS Code**
    *   *Gratuit (Open Source).*
    *   *Usage :* Éditeur de code intégré comme option d'ouverture depuis l'interface.
*   **GitHub**
    *   *Gratuit / Payant.*
    *   *Usage :* Plateforme de gestion de version utilisée pour l'intégration des Pull Requests (PR) et des workflows CI/CD.
*   **OpenClaw / Hermes Agent**
    *   *Gratuit (Open Source).*
    *   *Usage :* Agents autonomes distants sur serveur cités comme alternative préférée aux "Routines" locales.

---

### 3) Astuces concrètes et réutilisables

1.  **Inspection et sélection visuelle d'éléments UI :**
    Dans l'onglet *Preview* de l'application, activez le bouton **"Select element"** et cliquez directement sur un bouton ou un composant React de votre application en direct. Claude capture automatiquement le composant et injecte sa structure exacte dans le champ de texte pour que vous puissiez lui demander des modifications ciblées.
2.  **Activer le "Full Bypass Permissions" :**
    Dans les paramètres de l'application (*Settings > Claude Code desktop settings*), activez **Allow bypass permissions mode**. Cela évite que l'IA ne s'arrête à chaque étape pour vous demander l'autorisation d'exécuter des commandes de terminal (comme des vérifications TypeScript ou des builds).
3.  **Travailler en mode "Plan" avec commentaires ciblés :**
    Avant de lancer des modifications lourdes, basculez en **Plan mode**. Relisez le plan généré dans le panneau latéral droit, surlignez du texte à la volée pour y laisser des commentaires/correctifs précis, puis validez le plan.
4.  **Multitasking par sessions / agents :**
    Créez plusieurs sessions en parallèle dans la barre latérale gauche (*New session*). Vous pouvez ainsi faire travailler un agent sur le backend pendant qu'un autre travaille sur le design frontend ou la résolution de bugs.
5.  **Configuration automatique des serveurs de Dev (`launch.json`) :**
    Créez ou laissez Claude générer un fichier `.claude/launch.json` dans votre projet. Cela permet de lancer vos serveurs locaux (Next.js, Convex, Stripe webhooks, React Email) directement depuis le menu déroulant *Preview* en un clic.
6.  **Auto-vérification visuelle autonome (Screenshots) :**
    Utilisez des commandes/skills de vérification (comme `/apex ax v`). L'agent va lancer le navigateur en arrière-plan, prendre une capture d'écran du rendu local après ses modifications et l'afficher dans le chat pour valider visuellement que le bug est résolu sans que vous n'ayez à tester vous-même.
7.  **Adopter le "Vibe Coding" orienté résultat :**
    Au lieu de dicter à l'IA fichier par fichier ce qu'elle doit modifier (méthode "old school"), décrivez simplement le problème utilisateur ou la fonctionnalité souhaitée. L'agent se charge de lire les fichiers, planifier, coder, exécuter les tests TypeScript/ESLint et vérifier l'UI de manière totalement autonome.

---

### 4) Chiffres de revenus annoncés
*   **Non précisé** dans la vidéo (aucun chiffre de revenus n'est mentionné par l'auteur).
