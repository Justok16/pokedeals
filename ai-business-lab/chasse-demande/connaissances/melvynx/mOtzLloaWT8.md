# Cursor ont leur propre modèle ! (et la feature la plus inutile ?)

Vidéo : https://youtu.be/mOtzLloaWT8 · durée 23:29 · résumé Gemini (gemini-3.5-flash, lot de 6) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) L'idée principale**
Revue des fonctionnalités majeures de Cursor 2.0, notamment l'introduction du modèle d'IA propriétaire "Composer", la possibilité de lancer plusieurs agents IA en parallèle dans des Worktrees Git, et l'intégration d'un navigateur interne pour le débogage d'interface.

**2) Chaque outil, site ou dépôt GitHub cité**
*   **Cursor / Cursor 2.0** : Éditeur de code IA. *Payant (20 $/mois pour l'offre Pro, version gratuite limitée).*
*   **Composer** : Modèle d'IA propriétaire de codage à très faible latence développé par Cursor. *Inclus dans l'abonnement Cursor.*
*   **Claude 3.5 Sonnet / Claude 4.5** : Modèle d'IA d'Anthropic. *Payant (Inclus via quota/API dans Cursor).*
*   **GPT-5 / Codex** : Modèle d'IA d'OpenAI. *Payant (Inclus via quota/API dans Cursor).*
*   **Lumail** (`lumail.io`) : Application SaaS d'e-mailing développée par l'auteur (utilisée comme projet de test). *Payant.*
*   **Claude Code** : Outil CLI d'agent de codage d'Anthropic. *Payant via API.*
*   **mlv.sh/ai** : Site de l'auteur offrant une formation/masterclass gratuite et sa configuration CLI. *Gratuit.*
*   **Excalidraw** : Outil de dessin et tableau blanc. *Gratuit / Payant.*

**3) Les astuces concrètes et réutilisables**
*   Utiliser le navigateur intégré (`Command+Shift+P > Browser: Open Browser`) pour sélectionner directement un composant DOM à l'écran et envoyer son contexte/chemin exact au prompt IA.
*   Employer la fonction multi-agents pour soumettre une tâche complexe simultanément à plusieurs modèles (ex: Composer, Sonnet 3.5, GPT-5) et garder la meilleure réponse.
*   Combiner Composer pour la rapidité de mise en place initiale et Claude 3.5 Sonnet pour corriger les erreurs de typage ou de logique complexe.
*   Ajuster l'usage des agents parallèles avec modération pour ne pas épuiser son quota mensuel trop rapidement.

**4) Les chiffres de revenus annoncés**
*   Prix de l'abonnement Cursor Pro : 20 $/mois *(affirmé par l'auteur)*.
*   Coût de la session de test multi-agents (1 feature générée en parallèle par 3 modèles) : 1,44 $ au total (0,68 $ pour GPT-5 Codex, 0,49 $ pour Sonnet 3.5, 0,27 $ pour Composer) *(affirmé par l'auteur)*.
*   Dépense de quota de l'auteur en une journée de tests : 13 $ *(affirmé par l'auteur)*.
*   Gains personnels : non précisé.

---
