# Je change complètement ma stack... introduction de Now-Stack (secret project)

Vidéo : https://youtu.be/ag5GOJfL-a8 · durée 13:46 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur présente **NowStack**, un boilerplate (modèle prêt à l'emploi) conçu pour créer et déployer des applications SaaS rentables très rapidement à l'aide d'agents IA (notamment **Claude Code**, **Cursor** et **Codex**). Pour maximiser l'efficacité de l'IA et éliminer les erreurs récurrentes des composants serveur de Next.js, l'auteur a conçu une nouvelle pile technique (TanStack Start + Convex + Better-Auth) pilotée par des invites et « skills » (commandes d'agents) automatisés qui gèrent la configuration, l'authentification, les paiements Stripe et le déploiement en production.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Modèle économique | À quoi il sert |
| :--- | :--- | :--- |
| **NowStack** (`nowts.app` / `mlv.sh/fn`) | **Payant** (place waitlist affichée à 190 €) | Boilerplate SaaS de l'auteur tout-en-un intégrant backend temps réel, dashboard admin complet, blog, changelog, documentation et commandes IA automatisées. |
| **TanStack Start** | **Gratuit** (Open source) | Framework React full-stack servant à la gestion des pages, du routing côté client (instantané), des APIs et du rendu. Build ~2,2 fois plus rapide que Next.js et plus simple à manipuler pour les IA. |
| **Convex** (`convex.dev`) | **Gratuit / Freemium** | Base de données et backend serverless temps réel réactif (synchronisation instantanée multi-onglets/utilisateurs, gestion des requêtes, cron jobs, transactions et webhooks). |
| **Better-Auth** | **Gratuit** (Open source) | Système d'authentification complet et auto-hébergé, servant d'alternative gratuite aux fonctionnalités de gestion de sessions et d'utilisateurs. |
| **Claude Code** (Anthropic) | **Payant** (à l'usage via API) | Agent de code CLI en terminal utilisé pour exécuter les scripts de création autonome du SaaS. |
| **Cursor** | **Freemium / Payant** | Éditeur de code assisté par IA supportant l'exécution des règles/skills du boilerplate. |
| **Codex** | **Non précisé** | Outil d'IA cité par l'auteur en tâche de fond pour l'automatisation du code. |
| **Next.js** | **Gratuit** (Open source) | Framework React traditionnel, cité comme point de comparaison pour illustrer ses lenteurs de compilation et ses erreurs fréquentes avec l'IA. |
| **Stripe** | **Gratuit à l'installation** (frais par transaction) | Gestion des abonnements et paiements SaaS. |
| **Vercel** | **Freemium / Payant** | Plateforme d'hébergement et de déploiement cloud one-shot. |
| **GitHub** | **Gratuit / Freemium** | Hébergement de code et gestion des branches / worktrees. |
| **Clerk** | **Freemium / Payant** | Solution d'authentification tierce dont l'auteur a reproduit les fonctionnalités dans son propre panneau admin. |
| **Thumbfa.st** | **Freemium / Payant** | SaaS de l'auteur servant d'exemple (générateur de miniatures YouTube par IA). |

---

### 3) Astuces concrètes et réutilisables

1. **Privilégier une stack simplifiée pour l'IA :** L'architecture *TanStack Start + Convex* évite les directives complexes (`use client`, `use server`, Server Components) qui piègent régulièrement les LLMs, améliorant nettement la qualité du code généré par Claude Code.
2. **Utiliser des « Skills » (workflows d'agents standardisés) en Markdown :**
   - `init-project` : Initialise le projet, la landing page, le style et connecte la base de données automatiquement.
   - `setup-stripe` : Configure les tarifs, les clés API, les plans et les webhooks sans quitter le terminal.
   - `publish-to-production` : Lie GitHub, Vercel et Convex pour déployer le SaaS en ligne en une commande.
   - `/ai:builder-create-saas` : Démarre un guidage interactif pas à pas d'environ 1 heure avec l'IA pour définir et implémenter toutes les fonctionnalités métier du SaaS.
3. **Isoler les environnements de données :** Associer une base de données Convex distincte à chaque branche Git (*worktree*) et à chaque prévisualisation de déploiement pour tester sans impacter la production.

---

### 4) Chiffres de revenus annoncés

- **Chiffre d'affaires généré :** *Non précisé* (aucun montant de gains personnels réalisé n'est mentionné dans la vidéo).
- **Tarification affichée à l'écran :** Prix de lancement de la licence NowStack à **190 €** (*affirmé par l'auteur / visible sur la page d'inscription*).
