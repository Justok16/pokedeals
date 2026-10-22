# Comment terminer TOUS tes projets (l'IA ne t'aide pas, désolé)

Vidéo : https://youtu.be/LAJsStj-TjA · durée 28:30 · résumé Gemini (gemini-3.1-flash-lite) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo axé sur la création d'applications avec l'IA et le développement rapide :

### 1) Idée principale
L'auteur explique comment surmonter l'échec courant des projets jamais terminés en utilisant des **"boilerplate templates"** (modèles de code complets) et l'IA (Claude Code). L'approche consiste à automatiser la configuration technique complexe (authentification, base de données, paiement) pour se concentrer uniquement sur la valeur ajoutée du produit et accélérer drastiquement la mise en production.

### 2) Outils, sites et dépôts cités
*   **Claude Code :** Outil central utilisé pour coder et automatiser les tâches (statut gratuit/payant : non précisé dans la vidéo, bien que lié à l'API d'Anthropic).
*   **NowStack (nowstack.melvynx.dev) :** Plateforme créée par l'auteur pour fournir des modèles de code "prêts à l'emploi" pour SaaS ou applications mobiles.
*   **Stripe :** Outil de gestion des paiements (service payant/commission).
*   **Convex (convex.dev) :** Backend réactif "tout-en-un" (base de données, authentification, flux de travail). Il propose un répertoire de "components" (gratuits/payants).
*   **TanStack Start :** Framework utilisé pour le développement web, présenté comme optimisé pour l'IA.
*   **Vercel :** Plateforme de déploiement d'applications.
*   **Resend :** Service de gestion d'e-mails transactionnels (utilisé pour les codes OTP).
*   **PostHog :** Outil de suivi analytique.
*   **Cloudflare R2 :** Solution de stockage de fichiers (objets).
*   **Apex, UseGoal, Verify :** Outils mentionnés comme faisant partie du flux de travail pour valider les étapes de développement.
*   **mlv.sh (mlv.sh/fn) :** Site web personnel de l'auteur pour accéder à sa formation (payante).

### 3) Astuces concrètes et réutilisables
*   **Méthode de travail :** Passer 1 heure sur l'idée, 2 heures sur le MVP, et le reste sur la finalisation (plutôt que 5 minutes d'idée et 6 mois de développement).
*   **Gestion de la "dette technique" :** L'auteur insiste sur l'utilisation de tests automatisés (Vitest, Playwright) pour éviter que l'IA ne génère des erreurs en chaîne.
*   **Architecture "Agentique" :** Utiliser une structure où l'IA suit des étapes de réflexion (Init, Discovery, Brainstorm, Validation, Architecture) pour éviter le développement anarchique.
*   **Utilisation des "Components" :** Au lieu de tout recoder, utiliser des composants pré-validés (Rate Limiter, Authentification, etc.) via le répertoire Convex pour gagner un temps précieux en débogage.

### 4) Chiffres de revenus annoncés
*   Revenus générés par le "Pentest" (service de test de sécurité) : **"100 $"** (par client).
*   Prix de la formation NowStack : **non précisé**.
*   Prix des abonnements NowStack : **49 $** (plan Pro) et **100 $** (plan Ultra).
*   Gains potentiels par rapport au temps passé : L'auteur compare un projet à **"7 000 €"** de valeur travail contre **"14 jours"** de développement réel, tout cela **"affirmé par l'auteur"**.
