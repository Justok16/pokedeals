# 500 heures à maîtriser Claude Code expliqué en 15 minutes (tricks, tips, modèles)

Vidéo : https://youtu.be/kkkQKAPxna8 · durée 15:19 · résumé Gemini (gemini-3.5-flash-lite, lot de 5) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Comment configurer et utiliser Claude Code de manière efficace et sécurisée grâce à la gestion de la mémoire, des commandes personnalisées, des hooks et des MCP (Model Context Protocols).

2) **Outils, sites et dépôts GitHub cités** :
   - **Claude Code** : Outil de développement en ligne de commande (CLI) d'Anthropic (gratuit/payant selon l'API/abonnement Claude).
   - **Cursor** : IDE mentionné ou utilisé (non précisé si gratuit ou payant).
   - **GitHub** : Plateforme de gestion de code (mentionnée pour les dépôts) (gratuit/payant).
   - **Context7** (`context7.com`) : Service/outil MCP pour récupérer de la documentation technique à jour (gratuit/payant).
   - **Exa** (`exa.ai`) : Moteur de recherche pour l'IA et service MCP de recherche web (gratuit/payant).
   - **Stripe** : Service de paiement mentionné comme MCP (gratuit/payant).
   - **Supabase** : Service de base de données mentionné comme MCP (gratuit/payant).
   - **Chatbase** : Service de chatbot mentionné comme MCP (gratuit/payant).

3) **Astuces concrètes et réutilisables** :
   - Structurer la mémoire de Claude Code à trois niveaux : global (`.claude/CLAUDE.md`), par projet (`project/CLAUDE.md`), et spécifique par dossier.
   - Créer des fichiers de commandes réutilisables (ex: `commands/journal.md`, `commands/debug.md`) pour automatiser des tâches répétitives avec des workflows précis (étapes de commit, analyse, push).
   - Utiliser l'alias `cc` pour lancer Claude Code en mode YOLO (`--dangerously-skip-permissions`) tout en protégeant les actions dangereuses via des hooks `before-tools` (ex: bloquer un `rm -rf`).
   - Activer ou désactiver sélectivement les MCPs (comme Context7 ou Exa) via la commande `@` pour économiser l'espace de contexte du modèle (limité à 200k tokens).
   - Utiliser des "sub-agents" pour des modifications de code ciblées et de petite envergure (ex: correction de grammaire fichier par fichier en parallèle) afin d'éviter les pertes de contrôle en mode "one-shot".
   - Personnaliser la ligne de commande (`statusline`) pour suivre en temps réel la consommation des tokens, la session active, et le temps restant.

4) **Chiffres de revenus annoncés** :
   - « 10 000 € par mois » (affirmé par l'auteur : cible potentielle de l'application ou du développeur SaaS).
