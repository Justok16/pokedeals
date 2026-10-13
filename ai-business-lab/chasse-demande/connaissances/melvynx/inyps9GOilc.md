# TUTO/COURS sur NextJS 15 : Le Routing / Metadata / Setup d'application (1/5)

Vidéo : https://youtu.be/inyps9GOilc · durée 1:02:20 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

### 1. Idée principale
La vidéo propose un tutoriel complet d’une heure pour maîtriser les fondamentaux de **Next.js** (framework React). Le créateur explique la mise en place d'un projet, la structure des dossiers et le **routing (basé sur les dossiers)**, la gestion des composants dynamiques et statiques, ainsi que l'utilisation de bibliothèques UI (shadcn/ui) pour créer des applications web performantes. L'objectif est d'apprendre à créer des applications robustes pour potentiellement décrocher des missions ou des emplois bien rémunérés.

---

### 2. Outils, sites et dépôts GitHub cités

*   **Next.js** ([nextjs.org](https://nextjs.org))
    *   *Coût :* Gratuit (Open Source)
    *   *Rôle :* Framework React pour le développement d'applications web full-stack (SSR, routage basé sur les fichiers, etc.).
*   **Node.js** ([nodejs.org](https://nodejs.org))
    *   *Coût :* Gratuit
    *   *Rôle :* Environnement d'exécution JavaScript côté serveur (requis pour exécuter Next.js).
*   **VS Code / Cursor**
    *   *Coût :* Gratuit (avec options payantes pour Cursor)
    *   *Rôle :* Éditeurs de code source utilisés pour le développement.
*   **shadcn/ui** (UI Components)
    *   *Coût :* Gratuit
    *   *Rôle :* Bibliothèque de composants accessibles et stylisés (boutons, cartes, alertes, etc.) pour Tailwind CSS.
*   **Lucide React** (ou icônes similaires)
    *   *Coût :* Gratuit
    *   *Rôle :* Bibliothèque d'icônes intégrée via shadcn/ui.

---

### 3. Astuces concrètes et réutilisables

*   **Initialisation rapide d'un projet Next.js :** Utiliser la commande `npx create-next-app@latest` avec les options par défaut (TypeScript, Tailwind CSS, App Router, etc.).
*   **Gestion des imports propres :** Configurer `components.json` et `tsconfig.json` pour utiliser des alias de chemins (ex. `src/components/...` au lieu de chemins relatifs complexes).
*   **Utilisation du Routing par dossiers (*App Router*) :** Organiser les pages et sous-pages via l'arborescence des dossiers (`app/formations/[videoId]/[lessonId]/page.tsx`).
*   **Gestion des erreurs et chargements personnalisés :** Créer des fichiers spécifiques comme `error.tsx` (pour attraper les erreurs d'une route) et `loading.tsx` (pour afficher des squelettes de chargement pendant la récupération des données).
*   **Génération statique et dynamique :** Maîtriser `generateStaticParams()` pour pré-rendre des routes dynamiques lors du build et améliorer les performances (SEO et rapidité).

---

### 4. Chiffres de revenus annoncés

*   **Affirmés par l'auteur :** Non précisé (la vidéo se concentre uniquement sur l'apprentissage technique de Next.js et ne mentionne pas de chiffres de revenus spécifiques).
