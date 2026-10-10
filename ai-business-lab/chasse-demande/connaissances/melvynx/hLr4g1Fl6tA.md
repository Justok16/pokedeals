# INCROYABLE : L'IA code et teste toutes ses features en autonomie (triples tests)

Vidéo : https://youtu.be/hLr4g1Fl6tA · durée 17:31 · résumé Gemini (gemini-3.8-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
L’auteur présente un workflow d’agents IA optimisé pour le développement d’applications (web et mobiles), articulé autour du skill **APEX** (notamment la commande `/apex -axv`). La clé du système réside dans le paramètre de **vérification automatique (`-v`)** : l’agent ne se contente pas d’écrire du code, il lance l’application, exécute les tests et prend automatiquement des **captures d’écran** (web via un navigateur headless ou mobile via un simulateur iOS). 

Cela crée une **boucle de rétroaction (feedback loop)** autonome :
1. L'agent analyse et planifie la tâche.
2. Il code la fonctionnalité.
3. Il lance les linters et des sous-agents de revue de code (sécurité, logique, architecture).
4. Il vérifie visuellement le rendu par capture d'écran.
5. En cas d'échec ou d'imperfection, il corrige lui-même avant de soumettre le résultat final au développeur.

L'intérêt pour gagner de l'argent légalement est d'augmenter drastiquement sa vélocité pour concevoir, prototyper et livrer des applications SaaS ou mobiles sans perdre de temps en tests manuels.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité |
| :--- | :--- | :--- |
| **Codex** (application de bureau) | Non précisé (modèle avec quotas / abonnements visibles à l'écran) | Environnement d'exécution et de chat pour orchestrer les agents IA et exécuter des tâches en local. |
| **Skywork.ai** | Freemium (version d'essai/gratuite et options Plus visibles) | Outil sponsorisé tout-en-un avec agents pour générer des présentations, visuels publicitaires, intégrations GitHub, Google Suite, Slack, etc. |
| **Excalidraw** (`app.excalidraw.com`) | Gratuit / Freemium | Tableau blanc en ligne utilisé par l'auteur pour schématiser les workflows d'agents et l'architecture APEX. |
| **Playwright / `dev-browser`** | Gratuit (Open source) | Automatisation du navigateur web permettant à l'agent de naviguer, tester l'interface web et prendre des captures d'écran. |
| **iOS Simulator / `simctl` (`xcrun simctl`)** | Gratuit (inclus avec Xcode sur macOS) | Simulateur d'appareils Apple piloté par l'agent en ligne de commande pour lancer l'app mobile et capturer les écrans de test. |
| **Convex** | Freemium | Backend / base de données temps réel utilisé dans la pile technique de l'auteur (visible dans les scripts de vérification). |
| **Stripe** | Gratuit à intégrer (commission sur transactions) | Passerelle de paiement testée par l'agent sur les démonstrations d'écrans de checkout et de gestion des factures. |
| **OpenClaw / Hermes** | Non précisé (mentionné au vol comme comparatif d'agents) | Références d'architectures d'agents citées brièvement par l'auteur. |
| **`mlv.sh/formation-mobile`** / `codelynx.dev/builder-mobile/get` | Gratuit (ressources / 3 skills gratuits) avec options payantes potentielles | Page de ressources / mini-formation de l'auteur offrant la stack mobile, le workflow APEX et la documentation de configuration. |
| **`mlv.sh/formation-config`** (`codelynx.dev/agents`) | Payant (formation / configuration clé en main pour Claude Code, Cursor, Codex) | Pack de configuration de l'auteur pour transformer les agents IA en « développeurs seniors ». |

---

### 3) Astuces concrètes et réutilisables

* **Découper le flux en fichiers d'instructions modulaires (`step-*.md`) :** Pour éviter le phénomène de *« Lost in the middle »* (où le LLM oublie les consignes situées au milieu d'un trop long prompt), l'auteur scinde les étapes en une douzaine de petits fichiers exécutés successivement.
* **Exiger des preuves visuelles (screenshots) systématiques :** Intégrer dans les règles de l'agent l'obligation de démarrer le serveur de dev, d'effectuer l'action et de renvoyer une image du résultat. Cela permet de valider le travail depuis son téléphone sans toucher à son ordinateur.
* **Interdire le contrôle direct de la souris (*Computer Use*) :** Dans ses règles (`verification.md`), l'auteur interdit expressément les outils de contrôle de curseur génériques pour les simulateurs ou le web, car ils bloquent l'ordinateur et manquent de fiabilité ; il impose à la place des scripts CLI directs (`simctl`, `dev-browser`).
* **Automatiser la connexion avec comptes de test et OTP :** Documenter dans un fichier Markdown (`AGENTS.md` ou `verification.md`) la procédure exacte pour que l'agent récupère les identifiants de test, lise les codes OTP dans les logs de backend (ex. Convex) et se connecte seul aux interfaces privées.
* **Faire tourner des agents spécialisés en parallèle :** Lancer des sous-agents dédiés uniquement à des tâches précises (un pour la revue de sécurité OWASP, un pour le linter/TypeScript, un pour l'analyse des cas limites) avant la validation finale.

---

### 4) Chiffres de revenus annoncés

* **Affirmé par l'auteur : non précisé.** L'auteur ne partage aucun chiffre d'affaires ni revenu personnel dans la vidéo (les seuls montants visibles, comme 300 $, 390 € ou 159 €, sont des données de démonstration sur des pages de paiement Stripe).
