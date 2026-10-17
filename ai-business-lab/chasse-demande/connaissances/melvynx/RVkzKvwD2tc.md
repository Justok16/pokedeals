# Raccourcis MINIMUM à connaître si tu es DEV (sinon arrête le métier)

Vidéo : https://youtu.be/RVkzKvwD2tc · durée 13:17 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo présente les raccourcis clavier indispensables de l'éditeur VS Code (et de sa version Cursor) pour les développeurs, permettant de gagner un temps précieux en navigation, édition, suppression, sélection multiple et manipulation de lignes ou de fichiers.
2) **Outils, sites ou dépôts GitHub cités** :
   - **VS Code** : Logiciel / Éditeur de code (gratuit) — l'environnement de développement principal utilisé dans la vidéo.
   - **Cursor** : Logiciel / Éditeur de code (freemium/payant selon les fonctionnalités IA) — l'éditeur utilisé par l'auteur, basé sur VS Code.
   - **Prettier** : Extension VS Code (gratuit) — formateur de code automatique.
   - **ESLint** : Extension VS Code (gratuit) — outil d'analyse de code pour détecter les erreurs.
   - **GitHub** : Site (gratuit/payant) — mentionné pour le thème visuel (`GitHub Dark`).
   - **Material Icon Theme** : Extension VS Code (gratuit) — pack d'icônes pour l'arborescence des fichiers.
   - **Commit Mono** : Police de caractères (gratuite) — police "monospace" recommandée pour la programmation.
   - **Supermaven** : Extension / Outil IA (freemium) — extension de complétion de code par IA pour l'éditeur.
   - **Error Lens** : Extension VS Code (gratuit) — outil pour afficher les erreurs directement sur la ligne de code.
   - **Template String Converter** : Extension VS Code (gratuit) — outil de conversion automatique de chaînes de caractères.
   - **Tailwind CSS** : Framework CSS (gratuit) — mentionné pour une extension potentielle.
   - **Prisma** : ORM (gratuit) — mentionné pour une extension potentielle.
3) **Astuces concrètes et réutilisables** :
   - Configurer le formateur par défaut sur Prettier dans les paramètres JSON (`"editor.defaultFormatter": "esbenp.prettier-vscode"`), activer la sauvegarde automatique au changement de focus (`"files.autoSave": "onFocusChange"`), et forcer le formatage à la sauvegarde (`"editor.formatOnSave": true`).
   - Limiter le nombre d'onglets ouverts simultanément pour plus de clarté en configurant `"workbench.editor.limit.enabled": true` et `"workbench.editor.limit.value": 6`.
   - Activer la correction automatique des erreurs ESLint à la sauvegarde avec `"editor.codeActionsOnSave": { "source.fixAll.eslint": "true" }`.
   - Utiliser les raccourcis de base : `CMD + C` (copier), `CMD + V` (coller), `CMD + X` (couper et supprimer la ligne sans tout sélectionner), `CMD + Z` (annuler) et `CMD + SHIFT + Z` (rénitialiser/rétablir).
   - Naviguer efficacement dans le texte avec `OPTION + Flèche gauche/droite` (sauter de mot en mot), et sélectionner du texte avec `OPTION + SHIFT + Flèche`.
   - Déplacer des lignes de haut en bas avec `OPTION + Flèche haut/bas`, et dupliquer des lignes avec `OPTION + SHIFT + Flèche haut/bas`.
   - Sélectionner des occurrences multiples avec `CMD + D` (sélectionner le texte identique suivant) ou `CMD + SHIFT + L` (sélectionner toutes les occurrences du mot sélectionné), tout en activant la recherche sensible à la casse (`match case`) si nécessaire.
   - Basculer rapidement entre les onglets ouverts avec `CTRL + TAB`, ou ouvrir le sélecteur de fichiers avec `CMD + P`.
   - Ouvrir la palette de commandes avec `CMD + SHIFT + P` pour accéder à toutes les actions de l'éditeur, masquer ou afficher les panneaux (barre latérale avec `CMD + B`, terminal avec `CMD + J`).
   - Utiliser `CMD + A` pour tout sélectionner, et `CMD + W` pour fermer un onglet (ou `CMD + SHIFT + T` pour le rouvrir).
   - Configurer les "Inlay Hints" pour afficher le type des variables et des paramètres directement dans le code TypeScript (`"typescript.inlayHints.variableTypes.enabled": true`, etc.).
   - Utiliser les snippets personnalisés ou les raccourcis clavier de recherche d'importation automatique (`CMD + SHIFT + I` ou `CMD + SHIFT + O` pour le symbole re-name).
4) **Chiffres de revenus annoncés** : Non précisé.
