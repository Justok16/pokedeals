# 15 Bonnes Pratiques à Avoir en Next.JS (IMPORTANT)

Vidéo : https://youtu.be/XW4AQYG86z8 · durée 37:48 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo détaille 15 erreurs de sécurité et de conception très courantes commises par les développeurs utilisant Next.js (en particulier avec le routeur d'application et les Server Actions), et explique comment les corriger pour éviter d'exposer des données sensibles ou de perturber l'expérience utilisateur.
2) **Outils, sites ou dépôts GitHub cités** :
   - **Next.js** : Framework (gratuit) — technologie principale utilisée pour l'application web.
   - **Prisma** : ORM (gratuit) — utilisé pour interagir avec la base de données et manipuler les données.
   - **TypeScript** : Langage (gratuit) — utilisé pour typer le code.
   - **Zod** : Bibliothèque de validation de schémas (gratuit) — utilisée pour valider les données entrantes (validation des types et des contraintes de sécurité).
   - **Typefully** : Application/Site (freemium/payant) — utilisée pour tester les requêtes HTTP (PATCH, GET, etc.).
   - **Prisma Studio** : Outil d'interface (gratuit) — utilisé pour visualiser et modifier la base de données.
   - **Next Safe Action** (bibliothèque `next-safe-action` créée par `richardsolomos`) : Bibliothèque / Dépôt GitHub (gratuit) — outil tiers recommandé pour sécuriser et valider les Server Actions de manière robuste.
   - **NowTest** (`nowtes.app`) : Site/Application (gratuit/payant) — plateforme de test et de formation du créateur de la vidéo.
3) **Astuces concrètes et réutilisables** :
   - **Erreur 1 (Layouts routes)** : Ne jamais supposer qu'un layout protège une page contre l'accès aux données : si un layout redirige ou bloque l'affichage, les requêtes réseau (fetch) ou les Server Actions associées à la page enfant continuent de s'exécuter en arrière-plan et peuvent retourner des données sensibles. Il faut valider l'authentification et les autorisations à chaque niveau (dans les layouts, les middlewares et les Server Actions ou routes API).
   - **Erreur 2 (API routes)** : Toujours valider les données reçues dans les routes API et les Server Actions en utilisant une bibliothèque comme **Zod** (via `schema.safeParse()`) pour empêcher les injections ou les modifications non autorisées (par exemple, s'assurer qu'un utilisateur ne modifie pas des avis sans vérifier son identité ou ses limites).
   - **Erreur 3 (Server Actions)** : Ne pas faire confiance aux Server Actions sans validation : les Server Actions exposent des endpoints implicites que n'importe qui peut appeler en inspectant le code ou via des requêtes HTTP directes. Il faut y appliquer la même rigueur de validation (Zod, vérification de session) que pour les routes API classiques.
   - **Erreur 6 (Suspense)** : Toujours envelopper les composants asynchrones ou ceux qui effectuent des requêtes lourdes dans des limites `Suspense` avec un fallback adapté (comme un squelette de chargement) pour éviter le blocage du rendu global de la page et améliorer l'expérience utilisateur.
   - **Erreur 8 (Utilisation excessive de `use client`)** : Éviter de propager le directive `"use client"` inutilement sur des composants parents, ce qui alourdit le bundle JavaScript et expose des fonctions interactives ou des états non nécessaires ; isoler l'interactivité (comme les boutons de suppression ou de like) dans de petits composants clients spécifiques.
   - **Erreur 9 (Hydration Error)** : Ne pas utiliser directement `new Date()` ou `window.location` dans le rendu initial d'un composant serveur ou dans un composant client sans protection, car cela provoque des erreurs d'hydratation (différence entre le rendu serveur et le rendu client). Utiliser le hook `useIsClient` pour conditionner l'affichage au montage côté client.
   - **Erreur 11 (Requêtes dupliquées)** : Utiliser la fonction `cache` de React (`import { cache } from 'react'`) pour mémoriser (cacher) les résultats des requêtes de données (comme `getUsers`) et éviter de dupliquer les appels vers la base de données ou l'API au sein d'un même cycle de rendu.
   - **Erreur 14 (Variables d'environnement)** : Valider les variables d'environnement au démarrage de l'application (par exemple avec Zod ou via la bibliothèque `t3-oss/env-nextjs`) pour s'assurer que des clés secrètes (comme les clés Stripe ou les URLs de base de données) ne sont pas manquantes ou mal configurées, et séparer clairement les variables publiques (`NEXT_PUBLIC_`) des variables strictement privées (serveur).
   - **Erreur 15 (Secrets dans les Client Components)** : Ne jamais importer de fonctions ou de variables contenant des secrets (comme les clés API Stripe privées) dans des composants clients, sous peine de voir Next.js lever une erreur de compilation bloquante (avertissant qu'un module serveur est importé dans un composant client). Utiliser des modules dédiés côté serveur ou des Server Actions.
4) **Chiffres de revenus annoncés** : Non précisé.
