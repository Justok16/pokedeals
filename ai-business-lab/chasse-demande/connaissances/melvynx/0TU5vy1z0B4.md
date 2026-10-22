# Better-Auth : l'outil d'authentification ultime avec Convex (évite Clerk)

Vidéo : https://youtu.be/0TU5vy1z0B4 · durée 14:50 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’auteur explique pourquoi il est préférable de ne pas utiliser de solutions d’authentification tierces et coûteuses comme **Clerk** (qui créent un fort verrouillage fournisseur / *vendor lock-in* pour une valeur ajoutée devenue faible) au profit d'une bibliothèque contrôlée et intégrée comme **Better Auth**. Grâce aux agents IA modernes (comme **Claude Code**), il est désormais très simple et rapide de générer et tester ses propres interfaces et règles d'authentification/administration complètes, ce qui permet de réduire drastiquement les coûts récurrents lors de la création de projets SaaS.

---

### 2) Outils, sites et solutions cités

* **Better Auth** (`better-auth.com`) :
  * **Statut :** Gratuit / Open source.
  * **Rôle :** Librairie TypeScript d'authentification exécutée directement dans l'application et la base de données (supporte sessions, OTP, OAuth, organisations, passkeys, impersonation, etc.).
* **Clerk** (`clerk.com`) :
  * **Statut :** Freemium / Payant (options avancées payantes, ex. administration/impersonation à 100 $/mois, frais par organisation).
  * **Rôle :** Service managé d'authentification et de gestion d'utilisateurs.
* **NowStack** (`codelynx.dev/nowstack` / `mlv.sh`) :
  * **Statut :** Payant (sur liste d'attente / accès bêta).
  * **Rôle :** Boilerplate SaaS prêt à l'emploi conçu par l'auteur, basé sur Convex et Better Auth, optimisé pour le développement avec des agents IA.
* **Claude Code** (et Cursor) :
  * **Statut :** Modèle payant / freemium (*coût exact non précisé dans la vidéo*).
  * **Rôle :** Outils et agents IA en ligne de commande ou dans l'éditeur pour écrire, itérer et tester le code de l'application de façon autonome.
* **Convex** (`convex.dev`) :
  * **Statut :** Freemium (gratuit jusqu'à plusieurs milliers d'utilisateurs).
  * **Rôle :** Base de données réactive et backend temps réel.
* **TanStack Start** :
  * **Statut :** Gratuit / Open source.
  * **Rôle :** Framework web fullstack TypeScript.
* **Next.js** :
  * **Statut :** Gratuit / Open source.
  * **Rôle :** Framework React fullstack.
* **Vercel** :
  * **Statut :** Freemium / Payant.
  * **Rôle :** Plateforme d'hébergement et de déploiement cloud.
* **PostgreSQL & Prisma** :
  * **Statut :** Gratuits / Open source.
  * **Rôle :** Base de données relationnelle et ORM TypeScript.
* **Excalidraw** (`excalidraw.com`) :
  * **Statut :** Gratuit / Freemium.
  * **Rôle :** Outil de schéma interactif utilisé pour la présentation.

---

### 3) Astuces concrètes et réutilisables

* **Éviter le « Sync Tax » et le verrouillage auth :** L'authentification touche directement vos utilisateurs, votre facturation, vos permissions et vos middlewares. L'externaliser oblige souvent à mettre en place des webhooks complexes pour synchroniser les métadonnées. L'intégrer dans sa propre base via Better Auth simplifie les requêtes SQL/NoSQL directes.
* **Déléguer la création d'UI/Admin aux agents IA :** Au lieu de payer un service tiers pour avoir un tableau de bord d'administration ou des fonctionnalités comme l'*impersonation* (usurpation temporaire d'identité utilisateur pour le support), confiez cette tâche à un agent IA (Claude Code) qui sait générer ces vues en quelques minutes.
* **Automatiser les tests avec un navigateur de test via l'IA :** Laisser l'agent IA exécuter des tests d'authentification de bout en bout (connexion, invitations, redirection, changement de rôle) directement dans un navigateur automatisé pour s'assurer que les flux fonctionnent du premier coup.
* **Privilégier la simplicité de la stack :** Concevoir une stack minimale avec des règles claires permet à l'agent IA d'être bien plus performant et d'éviter les bugs de « *vibe coding* » incontrôlés.

---

### 4) Chiffres de revenus annoncés

* **Revenus financiers :** Non précisé (aucun chiffre d'affaires ou montant précis en €/$ n'a été annoncé dans la vidéo).
* **Métriques de projets présentées sur le site :** *10 SaaS et 3 applications mobiles créés en 2 ans, plus de 2 millions d'e-mails envoyés, plus de 10 000 utilisateurs et plus de 50 000 téléchargements* (*affirmé par l'auteur*).
