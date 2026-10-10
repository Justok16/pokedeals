# Formation Vibe Coding : Création d'un LinkTree

Vidéo : https://youtu.be/UdFZb_opBL8 · durée 26:51 · résumé Gemini (gemini-3.5-flash, lot de 4) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) Idée principale**
Tutoriel complet pour créer, personnaliser et déployer gratuitement sur Internet sa propre alternative à Linktree en utilisant l'agent IA Claude Code (ou Codex) sans avoir de compétences en programmation.

**2) Outils, sites ou dépôts GitHub cités**
*   **Linktree** : Payant (de ~3 €/mois jusqu'à 24 €+/mois selon les abonnements) — Service de page de liens en bio que le tutoriel vise à remplacer.
*   **Claude Code** : Payant (requiert un abonnement Claude Pro à 20 $/mois) — Agent IA CLI utilisé pour générer l'intégralité de l'application web.
*   **OpenAI Codex CLI** : Payant (requiert l'abonnement ChatGPT à 20 $/mois) — Cité comme alternative équivalente à Claude Code.
*   **GitHub & GitHub CLI (`gh`)** : Gratuit — Plateforme d'hébergement du code source et son outil en ligne de commande.
*   **Vercel & Vercel CLI (`vercel`)** : Gratuit — Plateforme d'hébergement web et son outil de déploiement automatique.
*   **Visual Studio Code (VS Code)** : Gratuit — Éditeur de code.
*   **Terminal macOS / Linux** : Gratuit — Interface de ligne de commande.
*   **Node.js / npm / Homebrew (`brew`)** : Gratuit — Environnement d'exécution et gestionnaires de paquets.
*   **Porkbun** : Payant (environ 7 à 8 $/an) — Registrar utilisé pour acheter un nom de domaine personnalisé à bas coût.
*   **Flat UI Colors** : Gratuit — Site web de palettes de couleurs utilisé pour choisir la couleur de fond.
*   **CSS-Tricks** : Gratuit — Site web d'astuces CSS cité pour ajouter des effets de grain/bruit.
*   **Next.js, Tailwind CSS, shadcn/ui, FontAwesome** : Gratuit — Stack technique web générée automatiquement par l'IA.
*   **`aiblueprint.dev/saas` / Document Notion** : Gratuit — Guide Notion avec les scripts et prompts fournis par l'auteur.

**3) Astuces concrètes et réutilisables**
*   **Préparation de l'environnement** : Installer les CLI indispensables via le terminal : Vercel CLI (`npm i -g vercel`), GitHub CLI (`brew install gh` ou via script), et Claude Code (`npm install -g @anthropic-ai/claude-code`).
*   **Connexion initiale aux CLI** : Exécuter `vercel login`, `gh auth login`, et `claude` dans le terminal pour authentifier votre machine avant de lancer la création.
*   **Utilisation d'un System Prompt** : Injecter un "System Prompt" complet définissant le rôle (Développeur Senior Full-Stack) et la stack imposée (Next.js, Tailwind, shadcn/ui) avant d'envoyer la demande métier.
*   **Saisie multiligne dans Claude Code** : Faire `Shift + Entrée` deux fois pour ajouter un saut de ligne sans envoyer prématurément le message à l'IA.
*   **Prompt de personnalisation** : Fournir à l'IA la couleur exacte (code HEX), l'URL de votre photo de profil, votre nom, votre bio et les liens réseaux sociaux souhaités.
*   **Autocorrection des erreurs** : Si le serveur local (`localhost:3000`) renvoie une erreur rouge, copier le message d'erreur du terminal et le coller directement dans le chat de Claude Code : l'IA analysera le bug et le corrigera d'elle-même.
*   **Lier un nom de domaine Porkbun à Vercel** : Dans Vercel (Project Settings > Domains), ajouter votre nom de domaine. Copier les enregistrements DNS fournis (CNAME et TXT) et les coller dans le panneau "Edit DNS Records" de Porkbun.

**4) Chiffres de revenus annoncés**
*   **Économies réalisées (affirmé par l'auteur)** : Remplacer un abonnement Linktree (qui coûte entre ~3 €/mois et 24 €+/mois, soit jusqu'à plus de 280 €/an) par une solution sur mesure hébergée à **0 $/mois sur Vercel**, avec pour unique dépense le nom de domaine sur Porkbun à **~7 à 8 $/an**. Aucun revenu direct encaissé n'est mentionné.
