# Apprendre useEffect en 18 minutes

Vidéo : https://youtu.be/fmsTYrfZdao · durée 18:14 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé complet de la vidéo, structuré selon tes demandes :

---

### 1. Idée principale
La vidéo explique en détail le fonctionnement du hook `useEffect` en React, en clarifiant ses différentes parties (effet, cleanup effect, tableau de dépendances), son cycle de vie (mount, update, unmount), son comportement en mode strict (appelé 2 fois), et sa véritable utilité : la **synchronisation** (et non la réaction à des états ou la simple modification d'états). L'auteur aborde également les erreurs fréquentes (comme le "fetch on render" et les fuites de mémoire) et présente des alternatives ou solutions (comme TanStack Query, SWR, ou le pattern Suspense).

---

### 2. Outils, sites et dépôts GitHub cités

*   **BeginReact.dev**
    *   **Nom exact :** BeginReact.dev
    *   **Tarif :** Payant (formation proposée par l'auteur).
    *   **Utilité :** Formation pour apprendre React de zéro avec des exercices pratiques (plus de 50 exercices) pour maîtriser les fondamentaux (dont `useEffect`).
  
*   **TanStack Query (v4)**
    *   **Nom exact :** TanStack Query (ou React Query)
    *   **Tarif :** Gratuit (open source).
    *   **Utilité :** Bibliothèque de gestion de requêtes asynchrones et de cache pour le fetch de données en React, permettant d'éviter les erreurs liées au "fetch on render" et aux fuites de mémoire.

*   **SWR**
    *   **Nom exact :** SWR (par Vercel)
    *   **Tarif :** Gratuit (open source).
    *   **Utilité :** Bibliothèque de data-fetching pour React basée sur la stratégie "stale-while-revalidate", gérant le cache, la revalidation et la synchronisation des données.

*   **Remix**
    *   **Nom exact :** Remix
    *   **Tarif :** Gratuit (open source).
    *   **Utilité :** Framework full-stack React utilisant des patterns modernes comme le "Render-as-you-fetch" (Suspense) pour charger les données avant le rendu des composants.

*   **Next.js**
    *   **Nom exact :** Next.js
    *   **Utilité :** Framework React populaire permettant le rendu côté serveur (SSR), le rendu statique et l'intégration du pattern Suspense ("Render-as-you-fetch").

*   **CodeSandbox (exemples de code de la vidéo)**
    *   **Lien mentionné dans la vidéo (code source `use-effect`) :** `https://codesandbox.io/s/use-effect-ltxxuv`
    *   **Tarif :** Gratuit.
    *   **Utilité :** Environnement de test en ligne pour visualiser les exemples de code React présentés.

---

### 3. Astuces concrètes et réutilisables

*   **Comprendre la structure de `useEffect` :**
    *   **L'effet (`run effect`) :** Code exécuté au montage ou lors de la modification des dépendances.
    *   **Le cleanup effect (`return () => {}`) :** Code exécuté pour nettoyer l'effet précédent avant une mise à jour ou lors du démontage du composant (`unmount`).
    *   **Le tableau de dépendances `[]` :**
        *   Vide `[]` : l'effet ne s'exécute qu'une seule fois (au mount).
        *   Avec des variables `[count]` : l'effet s'exécute dès que l'une de ces valeurs change.
        *   Absent : l'effet s'exécute à **chaque** render (risque de boucle infinie si on modifie l'état à l'intérieur sans condition).
*   **Éviter les boucles infinies avec les dépendances :**
    *   Ne pas placer un setter (ex: `setCount(count + 1)`) dans un `useEffect` dont le tableau de dépendances contient cette même variable (`[count]`), à moins d'utiliser un callback d'état (`c => c + 1`) ou de bien gérer les conditions.
*   **Utiliser `useEffect` pour la synchronisation (Side Effects / Synchronized) :**
    *   Idéal pour synchroniser des éléments externes (ex: `document.title`, abonnements `addEventListener`, connexions `Socket`).
    *   Penser à toujours nettoyer ces abonnements ou connexions dans le `return` du `useEffect` pour éviter les fuites de mémoire.
*   **Gérer le "Fetch on render" pour éviter les bugs :**
    *   En React classique, si un composant se démonte pendant qu'un `fetch` est en cours, tenter de modifier l'état (`setState`) sur un composant démonté génère une fuite de mémoire et un avertissement (`memory leak`).
    *   *Astuce historique (moins recommandée aujourd'hui) :* Utiliser une variable `let canceled = false;` et vérifier `if (canceled) return;` dans le cleanup (`return () => { canceled = true; }`).
    *   *Astuce moderne :* Utiliser des bibliothèques dédiées comme **TanStack Query** ou **SWR**, ou migrer vers des architectures de type **Suspense / Render-as-you-fetch** (avec Remix ou Next.js).
*   **Comprendre le mode strict (`StrictMode`) :**
    *   En mode développement (`StrictMode`), React appelle intentionnellement les effets deux fois (Mount -> Cleanup simulé -> Mount) pour détecter les bugs de synchronisation et aider à écrire du code résilient.

---

### 4. Chiffres de revenus annoncés
*   **Non précisé** (aucun chiffre de revenus ou de gains financiers n'a été mentionné dans cette vidéo, qui est purement technique et pédagogique).
