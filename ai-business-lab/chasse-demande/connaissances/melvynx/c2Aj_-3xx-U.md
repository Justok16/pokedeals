# TailwindCSS V4 est disponible (encore mieux que prévu)

Vidéo : https://youtu.be/c2Aj_-3xx-U · durée 13:38 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** :
   Présentation de la nouvelle version de Tailwind CSS (v4.0), de ses performances accrues, de sa nouvelle configuration simplifiée basée sur CSS et Vite, et démonstration pratique de son installation et de sa mise à jour dans un projet.

2) **Outils, sites ou dépôts GitHub cités** :
   - **Tailwind CSS (v4.0)** : Framework CSS gratuit, servant à styliser des applications web plus rapidement.
   - **Vite** : Outil de build et de bundling gratuit, intégré via un nouveau plugin officiel (`@tailwindcss/vite`).
   - **Ghosty** : Petit terminal / invite de commandes utilisé par l'auteur (gratuit).
   - **VS Code** : Éditeur de code (gratuit).
   - **GitHub / CodeLine** : Mentionnés pour des dépôts ou applications d'exemple.

3) **Astuces concrètes et réutilisables** :
   - Installer Tailwind v4 avec Vite via la commande `pnpm install tailwindcss @tailwindcss/vite`.
   - Importer Tailwind directement dans le fichier CSS principal (`@import "tailwindcss";`) au lieu de multiplier les fichiers de configuration complexes.
   - Configurer les thèmes et les variables directement dans le CSS en utilisant la syntaxe `@theme` (`--color-*: ...`, `--font-*: ...`, `--radius-*: ...`) au lieu du fichier `tailwind.config.js`.
   - Utiliser la commande de migration automatique `npx tailwindcss@latest upgrade next` pour passer un projet de v3 à v4 sans tout réécrire manuellement.

4) **Chiffres de revenus annoncés (affirmés par l'auteur)** :
   - *Non précisé* (aucun chiffre de revenu).

---
