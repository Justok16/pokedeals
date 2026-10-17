# Codeline: ma plus grosse migration à Tanstack Start (je regrette pas)

Vidéo : https://youtu.be/YUhPm5Ljt2Q · durée 17:39 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur explique pourquoi et comment il a migré l'intégralité de sa plateforme de formation (*Codelynx* / *Codeline*) de **Next.js vers TanStack Start** à l'aide d'agents IA (Claude Code / Codex). Il démontre que TanStack Start surpasse Next.js sur trois points majeurs :
1. **Temps de build/déploiement divisé par près de 3** (passant d'environ 3m40s à 1m20s).
2. **Réactivité de l'application et meilleure UX** (chargements instantanés, suppression des loaders intempestifs).
3. **Compatibilité maximale avec l'IA (« IA friendly »)** : TanStack Start utilise une syntaxe déclarative et explicite (routes, server functions, typage) qui évite les hallucinations et erreurs de l'IA, contrairement à Next.js dont les changements fréquents de paradigmes perdent les LLMs.

---

### 2) Outils, sites et dépôts cités

* **TanStack Start / TanStack Router** : *Gratuit (Open source)* — Framework fullstack React moderne, déclaratif et typé de bout en bout.
* **Next.js** : *Gratuit (Open source)* — Framework React utilisé initialement pour la version legacy de la plateforme.
* **Codelynx / Codeline (`codeline.app` / `legacy.codeline.app`)** : *Payant (plateforme de cours de l'auteur)* — Application SaaS servant de cas d'étude pour la migration.
* **NowStack / NowStack SaaS (`mlv.sh/fn` ou `codelynx.dev/nowstack`)** : *Payant / Accès sur liste d'attente (Beta privée)* — Boilerplate SaaS créé par l'auteur intégrant TanStack Start, Convex, Expo, Better Auth et des compétences préconfigurées pour agents IA.
* **Claude Code / Codex CLI / Agents CLI (APEX)** : *Payant (consommation de tokens API / abonnements)* — Outils d'agents IA en ligne de commande utilisés pour orchestrer et automatiser la réécriture et la migration du code.
* **GitHub** : *Gratuit / Freemium* — Plateforme d'hébergement de code (présentation de la PR #315 de plus de 100 000 lignes ajoutées/supprimées).
* **Vercel** : *Freemium / Payant* — Plateforme de déploiement cloud utilisée pour héberger et compiler l'application.
* **Excalidraw (`excalidraw.com`)** : *Gratuit / Freemium* — Tableau blanc virtuel utilisé pour structurer les arguments visuels de la vidéo.
* **Zod** : *Gratuit (Open source)* — Librairie TypeScript de validation de schémas utilisée pour valider et typer les paramètres de recherche (`validateSearch`) et entrées serveur.
* **Convex** : *Freemium / Payant (non précisé en détail)* — Base de données / Backend temps réel recommandé par l'auteur pour donner une structure logique et un contrôle total aux agents IA.
* **Expo / React Native / Better Auth / Stripe** : *Statut variable (Open source / Gratuit / Commissions Stripe)* — Technologies intégrées au boilerplate NowStack mentionné à la fin.

---

### 3) Astuces concrètes et réutilisables

* **Privilégier le code déclaratif pour le code généré par IA** : Les syntaxes magiques ou implicites (ex. `'use server'`, conventions de dossiers complexes dans Next.js) génèrent beaucoup d'erreurs avec l'IA. Avec TanStack Start (`createFileRoute`, `createServerFn`), tout est explicite dans un seul bloc d'objet, ce qui permet à l'agent IA de générer du code fonctionnel en « one-shot ».
* **Créer des compétences (« Skills ») pour vos agents IA** : L'auteur a créé un fichier d'instructions (`migrate-nextjs-to-tanstack` / `SKILL.md`) qui liste systématiquement l'arborescence, extrait les loaders, transforme les paramètres d'URL et réécrit les routes une par une pour automatiser une migration lourde.
* **Réduire le temps de build pour itérer plus vite** : Un temps de déploiement de 1 minute au lieu de 4 minutes permet de corriger des bugs critiques en production et de tester les modifications de l'IA beaucoup plus rapidement.
* **Utiliser Zod pour le typage strict des paramètres d'URL** : Utiliser des fonctions comme `validateSearch` garantit que l'IA ne casse pas les filtres, la pagination ou les états de l'application.
* **Fournir un feedback visuel à l'IA pour corriger les régressions** : Faire des captures d'écran des éléments manquants après refactoring (ex. bouton de notification oublié) et les passer à l'agent IA (via la CLI) avec les logs Git pour qu'il restaure le composant proprement.

---

### 4) Chiffres de revenus annoncés

* **Revenus de l'auteur / de la plateforme** : *Non précisé* (aucun chiffre d'affaires ou revenu financier n'est mentionné dans la vidéo).
* **Coût de la migration en tokens IA** : « Plusieurs centaines de dollars en tokens » (*affirmé par l'auteur*).
