# Apprendre NEXT.JS 15 en 1 HEURE | TOUT Comprendre en 2025

Vidéo : https://youtu.be/enyUdIyZmjU · durée 1:08:18 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

### 1) Idée principale
La vidéo est un tutoriel complet d’une heure pour apprendre à maîtriser **Next.js 15** en créant une application de gestion de citations (CRUD complet avec base de données, routes, composants et formulaires). L'objectif est de fournir les compétences fondamentales indispensables aux développeurs front-end et full-stack pour construire des applications web modernes et performantes.

---

### 2) Outils, sites et dépôts GitHub cités
*   **Next.js 15** (Framework web React) : Gratuit — Utilisé pour le développement frontend/backend et le routing.
*   **Tailwind CSS** (Framework CSS) : Gratuit — Utilisé pour le design et l'application rapide de styles.
*   **Shadcn/UI** (Bibliothèque de composants UI) : Gratuit — Utilisé pour intégrer rapidement des composants d'interface prêts à l'emploi.
*   **Prisma ORM** (ORM pour base de données) : Gratuit — Utilisé pour gérer et interagir avec la base de données.
*   **SQLite** (Base de données) : Gratuit — Utilisé pour stocker les données localement dans le projet.
*   **Visual Studio Code** (Éditeur de code) : Gratuit — Utilisé pour écrire et modifier le code source.
*   **iTerm / Terminal** (Interface de ligne de commande) : Gratuit — Utilisé pour exécuter les commandes du projet.
*   **Postman / HTTPie** (Testeurs d'API) : Gratuit — Utilisés pour tester les routes API (mentionné indirectement via les requêtes HTTP).

---

### 3) Astuces concrètes et réutilisables
*   **Utilisation de Shadcn/UI :** Initialiser rapidement un projet Next.js avec `npx shadcn@latest init` pour structurer et styliser l'application sans perdre de temps sur le design from scratch.
*   **Routing basé sur les dossiers (File-based routing) :** Structurer l'application via l'arborescence des dossiers (dossier `app`, segments dynamiques comme `[citationId]`) pour gérer automatiquement les chemins d'URL.
*   **Gestion des états de chargement et d'erreur :** Créer des fichiers spécifiques `loading.tsx` et `error.tsx` au même niveau que les pages pour gérer nativement l'expérience utilisateur pendant les requêtes ou les plantages.
*   **Server Actions & Formulaires :** Utiliser les Server Actions de Next.js combinées à l'attribut `action` des formulaires pour simplifier la mutation des données sans avoir à recoder manuellement des fetchs complexes côté client.
*   **Gestion des paramètres dynamiques et Search Params :** Récupérer proprement les identifiants d'URL via `params` et les paramètres de recherche via `searchParams` en gérant les promesses (`await props.params`).

---

### 4) Chiffres de revenus annoncés
*   *Revenus annoncés* : Non précisé.
