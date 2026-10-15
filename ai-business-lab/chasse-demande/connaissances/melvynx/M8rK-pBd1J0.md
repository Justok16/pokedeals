# Comment Setup TailwindCSS avec React ?

Vidéo : https://youtu.be/M8rK-pBd1J0 · durée 10:21 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Guide pratique pour installer Tailwind CSS dans une application React avec Vite, configurer VS Code, et mettre en place les outils d'autocomplétion et de linting.

2) **Outils, sites ou dépôts GitHub cités :**
* *Node.js* (gratuit, nodejs.org) : environnement d'exécution JavaScript pour installer les dépendances.
* *Vite* (gratuit, vitejs.dev) : outil de bundling et de scaffolding pour projets web.
* *Tailwind CSS* (gratuit, tailwindcss.com) : framework CSS utility-first.
* *VS Code* (gratuit) : éditeur de code.
* *Tailwind CSS IntelliSense* (extension VS Code gratuite) : extension pour l'autocomplétion des classes Tailwind.
* *eslint-plugin-tailwindcss* (gratuit, npm) : plugin ESLint pour ordonner et valider les classes Tailwind.

3) **Astuces concrètes et réutilisables :**
* Installer Tailwind via `npm install -D tailwindcss postcss autoprefixer` puis initialiser avec `npx tailwindcss init -p`.
* Configurer la clé `content` dans `tailwind.config.js` pour cibler `index.html` et les fichiers source (`./src/**/*.{js,ts,jsx,tsx}`).
* Ajouter les directives `@tailwind base;`, `@tailwind components;` et `@tailwind utilities;` dans le fichier CSS principal (`index.css`).
* Configurer ESLint pour trier automatiquement les classes et détecter les conflits avec `eslint-plugin-tailwindcss`.

4) **Chiffres de revenus annoncés (affirmés par l'auteur) :**
* Non précisé.

---
