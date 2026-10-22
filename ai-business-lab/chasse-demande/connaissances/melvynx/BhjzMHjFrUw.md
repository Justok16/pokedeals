# Configure Cursor comme ça ou juste arrête de coder !

Vidéo : https://youtu.be/BhjzMHjFrUw · durée 17:13 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo propose un tutoriel approfondi sur la configuration avancée de l'éditeur de code **Cursor** (basé sur VS Code), en montrant comment installer des thèmes, configurer le formatage automatique (Prettier), le linting (ESLint), la police Commit Mono, les icônes Material, et surtout en exploitant pleinement les fonctionnalités d'intelligence artificielle de Cursor (Composer, Supermaven, gestion des clés API, fichiers `.cursorules`, snippets et raccourcis clavier personnalisés) pour automatiser et accélérer le développement d'applications web.
2) **Outils, sites ou dépôts GitHub cités** :
   - **Cursor** : Éditeur de code (freemium / abonnement payant pour les fonctionnalités avancées d'IA) — l'IDE principal utilisé dans la vidéo.
   - **VS Code** : Éditeur de code (gratuit) — base sur laquelle Cursor est construit.
   - **GitHub** : Site web (gratuit) — source du thème visuel (`GitHub Dark`).
   - **Prettier** : Extension VS Code (gratuit) — outil de formatage automatique du code.
   - **ESLint** : Extension VS Code (gratuit) — outil d'analyse et de correction statique du code.
   - **Commit Mono** : Police de caractères (gratuite) — police monospacée idéale pour la programmation.
   - **Material Icon Theme** : Extension VS Code (gratuit) — pack d'icônes pour l'arborescence des fichiers.
   - **Supermaven** : Extension / Outil IA (freemium) — outil d'autocomplétion de code ultra-rapide par IA.
   - **Error Lens** : Extension VS Code (gratuit) — extension affichant les erreurs directement dans l'éditeur en fin de ligne.
   - **Pretty TypeScript Errors** : Extension VS Code (gratuit) — extension pour formater et rendre lisibles les erreurs TypeScript.
   - **Template String Converter** : Extension VS Code (gratuit) — extension pour transformer automatiquement les chaînes en template literals.
   - **Tailwind CSS** : Framework CSS (gratuit) — mentionné pour une extension potentielle.
   - **Prisma** : ORM (gratuit) — mentionné pour une extension potentielle.
   - **Anthropic (Claude)**, **OpenAI (GPT-4o)**, **Google (Gemini)** : Entreprises / APIs (payant) — fournisseurs de modèles d'IA dont les clés API peuvent être connectées à Cursor.
   - **Notion** : Application de prise de notes (gratuit/payant) — utilisée pour centraliser les snippets et les configurations de code.
3) **Astuces concrètes et réutilisables** :
   - Configurer le fichier `settings.json` de l'éditeur pour automatiser le flux de travail :
     - `"editor.defaultFormatter": "esbenp.prettier-vscode"` (Prettier par défaut).
     - `"files.autoSave": "onFocusChange"` (sauvegarde automatique lors du changement de focus).
     - `"editor.formatOnSave": true` (formatage à la sauvegarde).
     - `"editor.codeActionsOnSave": { "source.fixAll.eslint": "true" }` (correction ESLint automatique).
     - `"workbench.editor.limit.enabled": true` et `"workbench.editor.limit.value": 6` (limiter à 6 le nombre d'onglets ouverts simultanément pour garder un espace de travail propre).
     - `"editor.fontFamily": "CommitMono"` (appliquer la police Commit Mono).
     - `"editor.tabSize": 2` (définir la taille des tabulations à 2 espaces).
     - `"editor.inlayHints.variableTypes.enabled": true` et `"editor.inlayHints.parameterNames.enabled": "all"` (activer les indices de types TypeScript).
     - `"editor.codeActionsOnSave": { "source.fixAll.eslint": "always", "source.organizeImports": "always" }` (pour organiser les imports automatiquement).
   - Utiliser les raccourcis clavier et commandes de Cursor :
     - `CMD + K` (ou le raccourci d'auto-sélection/bloc) pour sélectionner rapidement un bloc de code.
     - `CMD + I` (Composer) pour générer ou modifier du code multi-fichiers par IA.
     - `CMD + B` (cacher/afficher la barre latérale) et `CMD + J` (cacher/afficher le terminal).
     - `CMD + P` (recherche rapide de fichiers) et `CMD + SHIFT + P` (palette de commandes).
     - `CTRL + TAB` (basculer entre les onglets récents).
   - Créer des snippets globaux (`User Snippets`) pour générer instantanément des structures de composants React avec TypeScript.
   - Configurer le fichier `.cursorrules` à la racine du projet pour donner des instructions précises à l'IA sur la stack technique utilisée (ex: Next.js App Router, Tailwind CSS, Prisma, conventions de nommage, interdiction d'utiliser certaines méthodes obsolètes).
   - Désactiver les extensions concurrentes inutiles (comme l'autocomplétion native de VS Code ou GitHub Copilot) lorsqu'on utilise Supermaven et les fonctionnalités intégrées de Cursor pour éviter les conflits de suggestions.
4) **Chiffres de revenus annoncés** : Non précisé.
