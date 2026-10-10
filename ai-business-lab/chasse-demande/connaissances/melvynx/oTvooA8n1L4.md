# MiniMax M3 : le nouveau modèle chinois meilleur que Fable ?

Vidéo : https://youtu.be/oTvooA8n1L4 · durée 18:39 · résumé Gemini (gemini-3.8-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur teste et compare en conditions réelles de développement un nouveau modèle d'IA : **MiniMax M3** (modèle à grand contexte de 1M de tokens, multimodal et orienté agents autonomes). Il démontre que ce modèle est capable d'écrire du code modulaire et propre (React/Tailwind), d'implémenter des fonctionnalités complètes sur un SaaS réel et de créer lui-même des scripts de tests pour s'auto-valider, tout en coûtant **jusqu'à 25 fois moins cher** que GPT-5.5. Pour un développeur ou entrepreneur souhaitant rentabiliser l'IA (notamment avec Claude Code ou OpenCode), l'intérêt est de réduire drastiquement les coûts d'exécution de code agentique tout en conservant une qualité proche des meilleurs modèles.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité |
| :--- | :--- | :--- |
| **MiniMax M3** | Payant (abonnements à 20 $, 50 $, 120 $/mois ou API au token ; poids ouverts / open-weight) | Modèle de fondation multimodal avec 1M de contexte optimisé pour le codage et les tâches agentiques autonomes. |
| **OpenRouter** (`openrouter.ai`) | Payant à l'usage | Agrégateur d'API d'IA permettant d'accéder à différents LLM (dont MiniMax M3 et la gamme GPT) et de comparer leurs tarifs. |
| **OpenCode** | Gratuit / open-source (*non précisé* dans le détail des licences, mais mentionné comme alternative libre d'agent CLI) | Environnement/interface de terminal pour exécuter des agents de développement de manière autonome. |
| **Claude Code** | Payant (via crédits/API Anthropic) | Agent CLI de développement en ligne de commande développé par Anthropic. |
| **Cursor / Codex** | Freemium / Payant | Outils et assistants de programmation IA cités comme compatibles avec sa configuration d'agents. |
| **code.melvynx.dev** | Gratuit (site public) | Site créé par l'auteur regroupant des prompts de test standardisés (benchmarks) pour évaluer la capacité des modèles à créer des applications complètes. |
| **mlv.sh/fc** / **codelynx.dev** | Payant (99 €/an affiché sur la page) | Pack de configuration et de commandes ("AI Agents Setup") créé par l'auteur pour équiper les agents CLI (Claude Code, OpenCode, etc.) d'outils et de workflows automatisés. |
| **Ghostty** | Gratuit | Émulateur de terminal visible à l'écran pour lancer les lignes de commande et serveurs locaux. |
| **Zed** | Gratuit (open-source) | Éditeur de code utilisé par l'auteur pour inspecter les fichiers générés et les commits Git. |
| **Stack web (Vite, React, Tailwind CSS, pnpm)** | Gratuit / open-source | Outils et bibliothèques frontend utilisés par le modèle pour générer les projets de test. |

---

### 3) Astuces concrètes et réutilisables

* **Optimiser les coûts de tokens grâce aux modèles alternatifs** : Utiliser des modèles comme MiniMax M3 (facturé 0,30 $/M tokens en entrée et 1,20 $/M en sortie sur OpenRouter, contre 5 $/M et 30 $/M pour GPT-5.5) pour diviser par 25 le coût de production de code agentique.
* **Activer le mode « Thinking » (raisonnement étendu)** : Cela force l'agent à planifier l'architecture, ce qui évite les hallucinations sur les contextes longs et produit un découpage propre en plusieurs composants réutilisables plutôt qu'un unique fichier monolithique.
* **Laisser l'agent écrire ses propres scripts de validation** : Sans commande explicite, MiniMax M3 a écrit des scripts Node.js pilotant un navigateur Chrome sans tête (*headless*) pour vérifier le rendu visuel et la syntaxe avant de finaliser la tâche. C'est une méthode à systématiser dans vos instructions d'agent pour fiabiliser le travail rendu à des clients.
* **Préciser l'usage d'un design system (ex. Tailwind CSS)** : Demander explicitement du Tailwind évite au modèle d'inventer du CSS custom lourd et garantit un code maintenable et cohérent avec l'existant.
* **Vérification pas à pas des sélecteurs DOM** : Lors de l'ajout d'interactions complexes (comme un clic droit personnalisé), l'agent peut échouer s'il cible un wrapper global ; il faut lui fournir le lien vers le composant UI exact ou le composant parent (ex. `ContextMenuTrigger`).

---

### 4) Chiffres de revenus annoncés

* **Revenus issus de la vente de services ou de gains avec Claude Code** : **Non précisé** (l'auteur ne formule aucune promesse ou chiffre de revenu financier personnel réalisable dans la vidéo).
* **Données de revenus visibles à l'écran** : Dans le dashboard de son application de test Codelynx, un montant de **1 440,00 €** de ventes cumulées est affiché pour un produit de formation, mais il s'agit d'une donnée de démonstration sur son environnement local (*affirmé par l'auteur / affiché à l'écran*).
