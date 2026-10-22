# Je MIGRE Thumbfa.st à Convex + Tanstack Start ($1000 API Codex dépensé)

Vidéo : https://youtu.be/mB-uFu8snc0 · durée 15:19 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’auteur explique pourquoi et comment il a investi près de 1 000 $ en requêtes LLM/IA pour faire migrer entièrement son application SaaS (**Thumbfast**) par un agent d'intelligence artificielle (type Claude / Codex). La migration fait passer son application de l’ancienne stack (**Next.js + Prisma + PostgreSQL + QStash**) à la nouvelle stack **NowStack** (**TanStack Start + Convex**). 

L'intérêt majeur pour un créateur de SaaS ou de projets générateurs de revenus réside dans :
* **La simplification drastique du code et du backend** : Convex gère la base de données réactive, les jobs en arrière-plan et la synchronisation en temps réel sans nécessiter de logique de polling complexe ni de gestion d'invalidation de cache manuelle.
* **La réduction des coûts et des requêtes superflues** : éviter le *prefetching* agressif de Next.js qui peut générer des surcoûts d'API et de bases de données.
* **L'autonomie maximale de l'agent d'IA (Claude Code / Codex)** : l'architecture simplifiée permet à l'IA d'identifier les bugs, de lire les logs, de tester dans un navigateur automatisé et de corriger le code en production beaucoup plus facilement qu'avec une stack Next.js/PostgreSQL traditionnelle.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité / Rôle |
| :--- | :--- | :--- |
| **Thumbfast** (anciennement nommé Subfast, URL : `thumbfa.st` / `beta.thumbfa.st`) | Freemium / Payant (système de crédits et abonnements) | SaaS de génération automatique de miniatures YouTube créé et opéré par l'auteur. |
| **NowStack** (`codelynx.dev/nowstack`) | Formation/template payant (*803 € affichés sur la page*) basé sur des outils gratuits/freemium | Stack technique recommandée par l'auteur pour créer et lancer des SaaS. |
| **TanStack Start** | Gratuit (Open source) | Framework web React côté client/serveur remplaçant Next.js. |
| **Convex** (`convex.dev`) | Freemium (offre gratuite puis payant à l'usage) | Backend-as-a-service et base de données réactive temps réel gérant l'état, les mutations et les tâches d'arrière-plan. |
| **Next.js** | Gratuit (Open source) | Ancien framework React utilisé pour Thumbfast. |
| **Prisma** | Gratuit (Open source) | Ancien ORM utilisé avec PostgreSQL. |
| **PostgreSQL** | Gratuit (Open source) | Ancienne base de données relationnelle. |
| **QStash** (Upstash) | Freemium / Payant à l'usage | Système de file d'attente (message queue/background tasks) de l'ancienne stack. |
| **Codex / Claude Code** (interface d'agent de code) | Payant (consommation de tokens LLM / API Anthropic / OpenAI) | Agent autonome de développement qui lit les logs, modifie les fichiers, exécute les tests et pilote le navigateur. |
| **Better Auth** | Gratuit (Open source) | Solution d'authentification incluse dans NowStack. |
| **Stripe** | Gratuit à l'installation / Commission par transaction | Gestion des paiements et abonnements du SaaS. |
| **Tailwind CSS** | Gratuit (Open source) | Framework CSS pour le design de l'interface. |
| **Expo** | Gratuit (Open source) | Framework pour décliner le projet sur mobile (React Native). |
| **Playwright** | Gratuit (Open source) | Outil de test end-to-end automatisé dans le navigateur, visible dans les logs de vérification de l'agent. |
| **Cloudflare Workers** | Freemium | Mentionné dans la documentation de migration pour le traitement des watermarks. |
| **Excalidraw** (`app.excalidraw.com`) | Gratuit / Freemium | Outil de tableau blanc virtuel utilisé pour schématiser l'architecture. |
| **GitHub** | Freemium | Gestionnaire de code source et de versions (PRs, commits). |

---

### 3) Astuces concrètes et réutilisables pour gagner du temps et de l'argent

* **Déléguer la maintenance et les correctifs à l'agent IA avec un navigateur headless/testeur** :
  L'auteur connecte son agent IA (`dev-browser` / Playwright / Chrome) directement à son environnement local. L'agent peut reproduire les erreurs rencontrées par l'utilisateur, inspecter la console, corriger le code TypeScript et vérifier visuellement si le correctif fonctionne avant de déployer.
* **Supprimer la complexité d'état (polling & cache invalidation)** :
  Plutôt que d'écrire des dizaines de lignes de code pour interroger une API toutes les 2 secondes (polling) ou invalider des caches (Next.js server actions / tags de revalidation), utiliser une base réactive temps réel (comme Convex). Dès qu'un job d'arrière-plan (ex. génération d'image via IA) met à jour la base de données, l'interface utilisateur se met à jour instantanément sans logique supplémentaire côté client.
* **Maîtriser les coûts d'infrastructures liés au prefetching** :
  Le préchargement automatique des pages (prefetching) de Next.js peut multiplier les appels vers la base de données et les fonctions serverless. Passer à un chargement déclenché à la demande (ou géré via des abonnements temps réel) évite les factures surprises sur les requêtes non désirées.
* **Garder un fichier de runbook / documentation pour l'IA (`AGENTS.md` / `deploy-to-production.md`)** :
  L'auteur demande à l'agent d'écrire et de mettre à jour des guides pas-à-pas dans le dépôt. Cela permet à l'IA de connaître les règles strictes de déploiement et de ne pas répéter les mêmes erreurs de build ou de configuration de variables d'environnement.

---

### 4) Chiffres de revenus et coûts annoncés *(affirmé par l'auteur / affiché à l'écran)*

* **Dépenses d'IA pour la migration** : L'auteur indique avoir dépensé *« près de 1 000 $ »* en requêtes LLM (un tableau de suivi affiché au début de la vidéo montre un total cumulé de **1 488,35 $** sur des modèles de type gpt-5.5 / claude).
* **Revenu récurrent mensuel (MRR) de Thumbfast** : **152,00 $** *(affiché sur le tableau de bord administrateur à 09:59)*.
* **Statistiques utilisateurs de Thumbfast** *(au moment de la vidéo, affiché sur l'écran admin)* :
  * Utilisateurs totaux : **1 046**
  * Organisations totales : **1 053**
  * Abonnements payants actifs : **8**
* **Tarif de la formation NowStack** : **803 €** pour les 175 premiers inscrits *(affiché sur la page web à 00:15)*.
