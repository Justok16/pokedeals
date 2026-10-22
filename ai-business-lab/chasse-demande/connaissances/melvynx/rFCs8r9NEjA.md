# Convex : la MEILLEUR Database pour tes SaaS (j'arrête Prisma)

Vidéo : https://youtu.be/rFCs8r9NEjA · durée 26:31 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur explique pourquoi il a abandonné la stack traditionnelle **Next.js + Prisma** au profit de **Convex** pour développer ses applications SaaS et projets gérés par des agents IA (comme Claude Code / Codex). Convex regroupe en une seule solution la base de données réactive (temps réel natif), les fonctions backend en TypeScript, les jobs asynchrones/CRON, les webhooks et la gestion de cache. Cela élimine la complexité de synchronisation d'état et d'invalidation de cache, permettant à un développeur solo et à des agents IA de construire, tester, déboguer et déployer des applications SaaS beaucoup plus vite.

---

### 2) Outils, sites et dépôts GitHub cités

* **Convex** (`convex.dev` / dépôt GitHub `get-convex/convex-backend`)
  * **Modèle de prix :** Gratuit (plan *Free & Starter* avec quotas généreux) / Payant (*Professional* à 25 $/mois/membre + consommation au-delà des quotas, ou *Business & Enterprise* à 2 500 $/mois). Option *Self-hosted* (open source) gratuite à héberger soi-même.
  * **Rôle :** Backend tout-en-un réactif (base de données, fonctions backend TypeScript, jobs/CRON, actions HTTP/webhooks, synchronisation temps réel automatique, vector search, etc.).

* **Prisma**
  * **Modèle de prix :** Gratuit / Open source (pour l'ORM).
  * **Rôle :** ORM TypeScript / gestionnaire de schéma et de migrations SQL, remplacé par l'auteur par Convex.

* **TanStack Start**
  * **Modèle de prix :** Gratuit / Open source.
  * **Rôle :** Framework web full-stack utilisé comme client frontend connecté à Convex.

* **NowStack** (`codelynx.dev/nowstack`)
  * **Modèle de prix :** Proposé par l'auteur (avec formation/mini-formation offerte sur liste d'attente/page de capture, boilerplate complet).
  * **Rôle :** Boilerplate SaaS prêt à l'emploi combinant TanStack Start, Convex, Better Auth, Stripe, Tailwind CSS et Expo pour le mobile, optimisé pour être piloté par des agents IA (Claude Code / Codex).

* **Better Auth** (`better-auth`)
  * **Modèle de prix :** Gratuit / Open source.
  * **Rôle :** Solution d'authentification intégrée dans la stack.

* **Stripe** / Composant `@convex-dev/stripe`
  * **Modèle de prix :** Gratuit à intégrer (commission sur transactions).
  * **Rôle :** Gestion des paiements, abonnements et webhooks.

* **Resend** / Composant Convex `Resend`
  * **Modèle de prix :** Gratuit (avec quotas) / Payant.
  * **Rôle :** Service d'envoi d'emails transactionnels.

* **Mux** / Composant Convex `Mux Convex Component`
  * **Modèle de prix :** Freemium / Payant à l'usage.
  * **Rôle :** Gestion et streaming vidéo.

* **Webhook Sender** (`convex-webhook-sender`)
  * **Modèle de prix :** Gratuit / Open source (composant Convex).
  * **Rôle :** Envoi et gestion fiabilisée de webhooks sortants avec signatures HMAC et retries automatiques.

* **Link Shortener** (`@the_shujaa/link-shortener`)
  * **Modèle de prix :** Gratuit / Open source (composant Convex).
  * **Rôle :** Raccourcisseur d'URL auto-hébergé avec analytics intégrés.

* **Claude Code / Codex**
  * **Modèle de prix :** Payant via clés API (Anthropic / OpenAI).
  * **Rôle :** Agents IA utilisés dans le terminal/IDE pour générer du code, corriger des bugs, lire les logs Convex et tester directement les interfaces via un navigateur automatisé.

* **Excalidraw**
  * **Modèle de prix :** Gratuit.
  * **Rôle :** Outil de tableau blanc virtuel utilisé pour schématiser les explications architecturales dans la vidéo.

* **Tchao.app**
  * **Modèle de prix :** Non précisé (application propriétaire de l'auteur).
  * **Rôle :** Exemple concret d'application de chat/support client en temps réel développée avec Convex.

---

### 3) Astuces concrètes et réutilisables

1. **Supprimer la plomberie d'invalidation de cache :** En adoptant un backend réactif par défaut (comme Convex), chaque mutation met à jour l'interface automatiquement via WebSockets. Plus besoin d'écrire de logique complexe d'invalidation TanStack Query ou de revalidation Next.js.
2. **Coupler l'agent IA aux logs Convex CLI :** Fournir l'accès au `convex-cli` à votre agent IA (Claude Code / Codex). Lorsqu'une erreur survient en production ou en local, l'agent peut directement inspecter les logs réels, identifier le message d'erreur précis et appliquer le correctif sans intervention manuelle.
3. **Tester les flux de webhooks en local sans CLI tierce :** Avec l'architecture Cloud de Convex (même en environnement dev), vous obtenez une URL publique dev directement joignable par Stripe pour tester les webhooks sans avoir à configurer de tunnel local complexe.
4. **Surveiller la bande passante de la base de données (*Database Bandwidth*) :** Assurez-vous d'ajouter des index appropriés sur vos tables Convex pour éviter que chaque requête ne scanne l'intégralité de la base, ce qui peut engendrer des coûts imprévus de lecture/écriture de données.
5. **Utiliser des agents spécialisés avec navigateur intégré :** Donner à l'agent un outil de navigation (ex. Dev Browser / extension Chrome) lui permet de reproduire les bugs dans l'UI, d'interagir avec les formulaires, de lire les toasts d'erreur et de valider les correctifs de bout en bout.

---

### 4) Chiffres de revenus annoncés

* **Affirmé par l'auteur sur sa page de présentation :**
  * **L'umail** : *« plus de 1 millions d'euros »* (sic).
  * **Thumbfat** : *« 2000 miniatures et plusieurs milliers d'euros »*.
  * **PadelTally** : *« plus de 30 000 téléchargements »*.
  * Coût d'infrastructure Convex personnel pour le projet *Tchao* (~911k fonctions exécutées, 186 GB de stockage DB) : **0,26 $** de facture affichée (sur un plan Pro à 25 $/mois).
