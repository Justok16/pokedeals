# Pourquoi j'ai arrêté d'utiliser Next.js (je sais... tu n'étais pas prêt)

Vidéo : https://youtu.be/4HphyoKblKI · durée 29:05 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1. Idée principale
L'auteur explique pourquoi il abandonne **Next.js** pour tous ses nouveaux projets SaaS au profit de **TanStack Start** (et d'une approche orientée *Single Page Application* / Client-Side Rendering avec Convex). 

Avec l'avènement du développement assisté par des agents IA (comme **Claude Code**), la complexité architecturale de Next.js (Server Components, directives `"use client"`, caches multi-niveaux, routes interceptées) génère de nombreux bugs et pertes de temps. À l'inverse, une architecture basée sur des standards web classiques (React Router, rendu côté client + API/requêtes de données brutes) permet à l'IA de coder des fonctionnalités du premier coup (*one-shot*), améliore radicalement la fluidité de navigation et réduit drastiquement les coûts d'infrastructure Vercel.

---

### 2. Outils, sites et projets cités

| Nom exact | Modèle tarifaire | Description / Rôle |
| :--- | :--- | :--- |
| **Next.js** | Gratuit (Open-source) | Framework React full-stack (orienté SSR et Server Components). |
| **TanStack Start** | Gratuit (Open-source) | Framework React full-stack basé sur TanStack Router. |
| **TanStack Router / Query** | Gratuit (Open-source) | Outils de routage et de gestion du cache de données côté client. |
| **React Router** | Gratuit (Open-source) | Bibliothèque de routage standard pour applications React SPA. |
| **Convex** | Freemium | Backend-as-a-service / base de données temps réel. |
| **Better-Auth** | Gratuit (Open-source) | Solution d'authentification open-source sans verrouillage fournisseur. |
| **Claude Code / Claude Agent** | Payant (via crédits Anthropic / API) | Agent IA de programmation utilisé par l'auteur dans son terminal/IDE. |
| **Vercel** | Freemium / Payant | Plateforme d'hébergement et d'exécution *serverless* pour applications web. |
| **NowStack** (`nowstack.melyvnx.dev` / `mlv.sh/fn`) | Payant (Accès bêta / Boilerplate) | Boilerplate SaaS créé par l'auteur combinant TanStack Start, Convex et Better-Auth. |
| **Codelynx** (`codelynx.app` / `codelynx.dev`) | Payant (Formations) | Plateforme de formations pour développeurs créée par l'auteur. |
| **Tchao.app** | Non précisé (SaaS de l'auteur) | Application de messagerie/support client pour les membres de formations. |
| **Lumail.io** | Non précisé (SaaS de l'auteur) | Outil d'email marketing conçu pour les agents IA. |
| **Thumbfa.st** | Non précisé (SaaS de l'auteur) | Générateur de miniatures YouTube assisté par IA. |

---

### 3. Astuces concrètes et réutilisables pour développer avec l'IA

1. **Privilégier les patterns web explicites et standards :**
   * L'IA (comme Claude Code) réussit beaucoup mieux à générer du code lorsqu'elle travaille avec des mécanismes prévisibles (ex. `React Router`, requêtes API JSON directes via `React Query`) plutôt qu'avec des abstractions propriétaires complexes (Directives Next.js, React Server Components).
2. **Adopter une architecture "App Shell" (SPA) pour les tableaux de bord / SaaS :**
   * Au lieu de refaire du rendu serveur (SSR) à chaque clic d'un utilisateur, charger la coquille de l'application une seule fois et ne mettre à jour que les données. Cela rend l'interface instantanée et évite les clignotements d'écrans de chargement.
3. **Réduire les coûts de calcul serveur (*Serverless Compute*) :**
   * Le SSR de Next.js ré-exécute du rendu de composant côté serveur à chaque changement de page, ce qui consomme des secondes de calcul Vercel facturées.
   * En passant sur du rendu côté client avec simple interrogation de base de données (ex. Convex), le serveur ne consomme du temps de calcul que pour renvoyer de la donnée brute.
4. **Éviter les fonctionnalités complexes de Next.js pour l'IA :**
   * Éviter les *Intercepted Routes* et les caches serveur imbriqués (`Full Route Cache`, `Data Cache`) qui perturbent les modèles de langage lors de la maintenance et du débogage.

---

### 4. Chiffres annoncés *(affirmés par l'auteur)*

* **Temps de compilation (*Build*) :**
  * Application sous *NowStack* / TanStack Start : **44 secondes** *(affirmé par l'auteur)*.
  * Application équivalente sous *Next.js* : **1 min 56 s** (pouvant monter à **3 min 44 s**, **5 min 34 s** ou **6 à 7 minutes** selon la taille) *(affirmé par l'auteur)*.
* **Temps de démarrage local (*Local Dev Startup*) :**
  * TanStack Start : **2 à 3 secondes** *(affirmé par l'auteur)*.
  * Next.js 15 : **10 à 12 secondes** *(affirmé par l'auteur)*.
* **Temps de chargement initial de page (*Initial Load*) :**
  * Démo TanStack Start : **2 à 3 secondes** *(affirmé par l'auteur)*.
  * Démo Next.js : **8 secondes** *(affirmé par l'auteur)*.
* **Coûts d'hébergement / factures Vercel :**
  * Auparavant, sous Next.js avec SSR intensif : jusqu'à **100 $** par facture et environ **5 $ par jour** simplement pour charger des pages de cours textuelles *(affirmé par l'auteur)*.
  * Après optimisation / passage en architecture App Shell : factures réduites à environ **50 $** *(affirmé par l'auteur)*.
* **Revenus de vente de formations :**
  * L'auteur affirme avoir gagné *« beaucoup beaucoup beaucoup d'argent »* en vendant des formations Next.js par le passé (montant exact non précisé).
