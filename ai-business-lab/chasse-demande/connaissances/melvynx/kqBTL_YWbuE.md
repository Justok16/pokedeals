# Comment setup des tests React avec Vitest - Guide pour débutants

Vidéo : https://youtu.be/kqBTL_YWbuE · durée 9:46 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** Guide complet pour configurer et écrire des tests unitaires dans une application React en utilisant **Vitest** et **React Testing Library**.
2. **Outils et dépôts cités :**
   - **Vitest :** Gratuit, test runner rapide basé sur Vite.
   - **@vitejs/plugin-react :** Gratuit, plugin Vite pour React.
   - **@testing-library/react :** Gratuit, bibliothèque de test pour composants React.
   - **@testing-library/dom :** Gratuit, utilitaires DOM pour les tests.
   - **@testing-library/jest-dom :** Gratuit, matchers Jest personnalisés pour le DOM.
   - **jsdom :** Gratuit, implémentation JavaScript du DOM pour l'environnement Node.
   - **@types/testing-library__jest-dom :** Gratuit, types TypeScript.
   - **@testing-library/user-event :** Gratuit, simulation d'événements utilisateur.
   - **Codeline :** Plateforme de formation du créateur (mention de cours sur les tests).
3. **Astuces concrètes :**
   - Installer les dépendances de test nécessaires via npm (vitest, testing-library, jsdom, etc.).
   - Configurer `vitest.config.ts` en y ajoutant le plugin React, l'environnement global (`globals: true`), l'environnement DOM (`environment: 'jsdom'`), et le fichier de setup (`setupFiles`).
   - Créer un fichier `setup.ts` pour étendre les matchers (ex. `expect.extend(matchers)` avec `@testing-library/jest-dom`).
   - Ajouter un script de test dans `package.json` (ex. `"test": "vitest"`).
   - Utiliser `screen.getByText` ou `screen.getByLabelText` pour interroger les éléments dans les tests de composants React et simuler des interactions avec `userEvent`.
4. **Chiffres de revenus :** Non précisé.
