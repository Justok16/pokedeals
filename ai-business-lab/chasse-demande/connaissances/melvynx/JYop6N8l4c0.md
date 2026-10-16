# J’arrête d’utiliser VSCode, voici ce qui le remplace (Cursor)

Vidéo : https://youtu.be/JYop6N8l4c0 · durée 24:28 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :**
   Cette vidéo présente **Cursor**, un nouvel éditeur de code basé sur l'IA (un « fork » de VS Code) qui intègre nativement des fonctionnalités avancées d'intelligence artificielle (génération de code de zéro, chat intelligent connecté à toute la codebase avec indexation par embeddings d'OpenAI, référence de fichiers/docs, et l'utilisation de clés API personnalisées).

2. **Outils, sites ou dépôts GitHub cités :**
   * **Cursor** (Gratuit avec options payantes pour les modèles avancés / Pro plan à 20$ par mois) : Éditeur de code basé sur l'IA, fork de VS Code.
   * **VS Code / IntelliJ** (Gratuit / Payant) : Anciens éditeurs de l'auteur, remplacés par Cursor.
   * **GitHub Copilot** (Payant) : Assistant IA de GitHub, comparé au système de chat intégré de Cursor.
   * **OpenAI (GPT-4 / GPT-4o)** (Payant via clé API) : Modèles d'IA utilisés pour alimenter le chat et la génération de code.
   * **Anthropic (Claude 3 / Claude 3.5)** (Payant via clé API) : Modèles d'IA alternatifs utilisables dans Cursor.
   * **Azure OpenAI** (Payant) : Autre fournisseur de clé API supporté par Cursor.
   * **AI SDK / Vercel AI SDK** (Gratuit) : Utilisé pour les démos de code et la génération de tool/stream text.

3. **Astuces concrètes et réutilisables :**
   * Créer un fichier `.cursorrules` à la racine du projet pour définir des instructions spécifiques à l'IA (ex. : préciser qu'on utilise React, Next.js, Tailwind, et interdire l'utilisation de `React.FC`).
   * Utiliser la syntaxe `@Codebase` ou faire référence directement à des fichiers et de la documentation pour que l'IA comprenne le contexte global du projet lors des questions ou de la génération de code.
   * Utiliser la fonctionnalité de revue de code (« Review Working State ») pour obtenir des feedbacks de l'IA sur les modifications en cours et corriger les erreurs de tokens ou de logique.

4. **Chiffres de revenus annoncés :**
   * Le plan Pro de Cursor est mentionné à **20$ par mois** (coût de l'abonnement, non un revenu généré). Aucun chiffre de revenus personnels n'est annoncé.

---
