# VIBE CODEUR : Quel stack utilisé pour un nouveau projet (j'ai tout tester)

Vidéo : https://youtu.be/GCVFv_yEfws · durée 24:13 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé complet et structuré de la vidéo :

---

### 1) Idée principale
L'auteur explique quelle **pile technique (stack)** choisir pour créer des SaaS (web), des applications mobiles (iOS/Android) ou desktop assistés par l'IA (Claude Code, vibe coding), sans obtenir un code de mauvaise qualité (« slop »), instable ou rempli de failles de sécurité. 

La règle fondamentale est d'**imposer un cadre strict et des abstractions simplifiées à l'IA** (notamment en utilisant **Convex** au lieu de configurations Next.js/Prisma complexes) ainsi que des *boilerplates* pré-structurés.

---

### 2) Outils, sites, paquets et dépôts GitHub cités

#### **Web / SaaS & Backend / Base de données**
* **Convex** : *Freemium / Gratuit avec offres payantes (non précisé en détail, mais décrit comme beaucoup moins cher que Vercel/Next.js/Supabase)* – Backend-as-a-Service (BaaS) réactif en temps réel. Gère la base de données, la logique serveur, les tâches asynchrones, les *cron jobs* et les *webhooks*.
* **Convex Stripe (`@convex-dev/stripe`)** : *Gratuit (composant open-source Convex)* – Composant prêt à l'emploi pour gérer les abonnements, paiements et webhooks Stripe.
* **Convex Resend (`@convex-dev/resend`)** : *Gratuit (composant open-source Convex)* – Composant pour l'envoi d'e-mails transactionnels via Resend.
* **TanStack Start** : *Gratuit (Open-source)* – Framework frontend/routing léger pour React, recommandé comme alternative à Next.js lorsqu'il est couplé à Convex.
* **TanStack Form / TanStack Query** : *Gratuit (Open-source)* – Bibliothèques pour la gestion de formulaires et de données côté client.
* **Next.js** : *Gratuit (Open-source)* – Framework React fullstack (critiqué ici pour sa lenteur en mode dev et ses frictions avec l'IA sur le middleware, proxy et les Server Functions).
* **Prisma / Drizzle** : *Gratuit (Open-source)* – ORM pour base de données SQL (critiqué avec l'IA car nécessite trop de boilerplate technique).
* **Better-Auth** : *Gratuit (Open-source)* – Bibliothèque d'authentification autonome et sécurisée.
* **PostgreSQL** : *Gratuit (Open-source)* – Système de gestion de base de données relationnelle.

#### **Outils / Services déconseillés par l'auteur**
* **Supabase** : *Payant / Freemium (déconseillé)* – Déclaré trop coûteux par projet.
* **MongoDB** : *Payant / Freemium (déconseillé)* – Qualifié de « pire décision » et d'« énorme piège ».
* **Clerk / Auth0** : *Payant / Freemium (déconseillé)* – Reproché de faire perdre le contrôle des données utilisateur et de brider la flexibilité.

#### **Applications Mobiles**
* **React Native** : *Gratuit (Open-source)* – Framework pour le développement d'applications mobiles cross-plateformes.
* **Expo** : *Gratuit (Open-source)* – Écosystème d'outils pour développer et déployer facilement avec React Native.

#### **Applications Desktop**
* **Tauri** : *Gratuit (Open-source)* – Framework léger écrit en Rust pour créer des applications de bureau.
* **Electron** : *Gratuit (Open-source)* – Framework (C++/JavaScript) utilisé par VS Code, Cursor et l'application desktop Claude.
* **Handy.Computer (`Handy.Computer`)** : *Gratuit (Open-source)* – Dépôt/projet open-source d'application desktop servant de boilerplate.
* **Parler** : *Projet de l'auteur (non précisé)* – Application desktop développée par l'auteur via un *fork* de `Handy.Computer` avec Tauri.

#### **Boilerplates / Projets présentés par l'auteur**
* **NOW.TS V2** : *Prix non précisé* – Boilerplate SaaS web créé par l'auteur combinant TanStack Start + Convex + Better-Auth.
* **NOW.TS Mobile** : *Prix non précisé* – Boilerplate mobile combinant Expo + React Native + Convex.
* **Thumbfa.st** : *Service de l'auteur (non précisé)* – SaaS de génération de miniatures YouTube re-développé avec Convex et TanStack Start.
* **Claude Code** : *Payant (Anthropic)* – Agent d'IA CLI utilisé dans le terminal pour générer du code et déboguer.

---

### 3) Astuces concrètes et réutilisables

1. **Privilégier un backend temps réel / réactif (Live Data)** :
   * Pour les fonctionnalités basées sur l'IA (comme la génération d'images), créez d'abord un enregistrement avec `url = null` en base. Dès que le traitement arrière-plan est terminé, mettez à jour l'URL en base : l'interface utilisateur s'actualise instantanément sans avoir à gérer du *polling*, des requêtes d'invalidation complexes ou des états locaux instables.
2. **Ne jamais laisser l'IA coder la sécurité de zéro** :
   * Sans cadre pré-établi, l'IA crée souvent des fonctions non sécurisées (ex: passer simplement un `userId` en paramètre d'URL/API sans vérifier le jeton d'authentification).
   * Utilisez une base de code (*boilerplate*) existante ou un composant pré-sécurisé afin que l'IA ne fasse qu'ajouter des fonctionnalités dans un cadre sain.
3. **Exploiter la CLI de Convex avec Claude Code** :
   * Donnez accès à Claude Code au terminal pour qu'il puisse exécuter les commandes CLI (`convex run`, `convex data`). L'agent d'IA pourra ainsi lire directement les tables de la base de données, vérifier les schémas et inspecter les logs de production pour corriger lui-même les bugs.
4. **Réduire les couches d'abstraction serveur** :
   * Évitez de cumuler les API Routes, Server Functions, ORM et TanStack Query au-dessus de Next.js pour le *vibe coding*. Plus il y a de couches, plus l'IA a tendance à tourner en rond et générer des erreurs de nommage ou de middleware.
5. **Éviter les mono-repos complexes pour les projets assistés par IA** :
   * Les structures en mono-repo complexifient le contexte pour les agents IA et deviennent rapidement chaotiques à déployer.

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de revenus n'est annoncé par l'auteur** dans la vidéo *(les montants visibles à l'écran lors des démonstrations sont uniquement des données fictives de mockups/dashboard)*.
