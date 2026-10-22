# Tailwind V4 va TOUT Changer 🤯

Vidéo : https://youtu.be/pzyvlWsNiDQ · durée 9:24 · résumé Gemini (gemini-flash-lite-latest, lot de 4) du 2026-10-17
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :**  
Présentation des nouveautés majeures de l'alpha de **Tailwind CSS v4**, qui a été entièrement réécrit (notamment en Rust) pour devenir 10 fois plus rapide, adopter une approche "CSS-first" et s'intégrer sous forme de plugin natif avec une configuration simplifiée via `@theme` et l'autodétection des classes.

2) **Outils, sites ou dépôts GitHub cités :**  
- **Tailwind CSS v4 (version alpha) :** gratuit, framework CSS.
- **Vite.js :** gratuit, bundler / outil de build utilisé pour les exemples d'application.
- **Lightning CSS :** gratuit, outil de *build*, parseur et transformateur/minifieur de CSS écrit en Rust, plus rapide que CSS Nano ou ES Build.
- **PostCSS :** gratuit, outil de traitement CSS (utilisé historiquement et transformé en plugin dans la v4).
- **CodeLine (plateforme de formation de l'auteur, mentionnée pour l'exemple de configuration) :** payante, plateforme de formation de l'auteur.

3) **Astuces concrètes et réutilisables :**  
- Profiter d'une vitesse de compilation 10 fois plus rapide grâce à la nouvelle engine en Rust et Lightning CSS.
- Utiliser l'instruction `@import "tailwindcss";` dans son fichier CSS principal pour remplacer l'ancienne configuration JavaScript (`tailwind.config.js`).
- Utiliser les sélecteurs groupés composables (comme `group-has-focus:`) pour appliquer des styles conditionnels selon l'état d'un élément parent.
- Configurer les variables de thème directement dans le fichier CSS natif via la règle `@theme` (ex: `--color-blue-pink`, `--spacing-special`) au lieu d'utiliser un fichier de configuration JS externe.
- Laisser l'outil détecter automatiquement les classes utilisées dans les fichiers HTML/JS sans avoir besoin de configurer manuellement le tableau `content` ou d'importer des plugins de purge de manière complexe.

4) **Chiffres de revenus annoncés :**  
- **Affirmé par l'auteur :** non précisé.

---
