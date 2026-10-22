# Tutoriel Blog en NextJS pour débutant | Français

Vidéo : https://youtu.be/r1CHyYX9ZqY · durée 30:00 · résumé Gemini (gemini-3.1-flash-lite-preview) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, en répondant point par point à vos attentes :

### 1) Idée principale
L'auteur explique comment créer un **blog dynamique et performant** en utilisant le framework **Next.js**. Il montre pas à pas comment combiner le React (pour l'interactivité des composants), le MDX (pour écrire les articles en Markdown enrichi avec du code JSX) et Tailwind CSS (pour le stylisme), afin d'obtenir un site moderne et rapide.

### 2) Outils, sites et dépôts cités
*   **Next.js** : Framework React (gratuit) – Sert à construire l'application fullstack.
*   **Vercel** : Plateforme de déploiement (freemium) – Sert à héberger et publier le site web.
*   **VS Code** : Éditeur de code (gratuit) – Outil principal pour le développement.
*   **Tailwind CSS** : Framework CSS (gratuit) – Sert à styliser l'interface du blog.
*   **MDX** : Format de fichier (gratuit) – Permet d'intégrer du code JSX dans du Markdown.
*   **GitHub** : Service d'hébergement de code (gratuit) – Utilisé pour la gestion du dépôt.
*   **NPM / Yarn** : Gestionnaires de paquets (gratuits) – Utilisés pour installer les bibliothèques.
*   **Rehype-prism-plus** : Plugin NPM (gratuit) – Sert à la coloration syntaxique du code dans les articles.
*   **Prism-themes** : Dépôt GitHub (gratuit) – Fournit des thèmes visuels pour la coloration syntaxique.
*   **Gray-matter** : Bibliothèque NPM (gratuit) – Sert à extraire les métadonnées (titre, description, etc.) des fichiers MDX.
*   **Mdx-bundler** : Bibliothèque NPM (gratuit) – Sert à transformer les fichiers MDX en code compréhensible par le navigateur.

### 3) Astuces concrètes et réutilisables
*   **Utiliser le SSR (Server-Side Rendering)** : Le fait de pré-générer le HTML sur le serveur permet un affichage immédiat et améliore le référencement (SEO).
*   **Utiliser le routage dynamique (`/post/[slug]`)** : Cette structure permet de créer automatiquement une nouvelle page de blog pour chaque fichier ajouté dans le dossier, sans devoir créer de fichier individuel pour chaque article.
*   **Centraliser les composants MDX** : Créer un dossier dédié aux composants (ex: `MDXCounter`) et utiliser `mdx-bundler` permet d'insérer des éléments interactifs directement dans les articles de texte.
*   **Utiliser `getStaticProps` et `getStaticPaths`** : Ces fonctions Next.js sont indispensables pour récupérer les données au moment du build du site, garantissant ainsi une performance optimale.
*   **Gestion des erreurs 404** : En ne configurant pas spécifiquement certaines routes, Next.js gère automatiquement l'affichage d'une page 404, ce qui simplifie le travail de développement.

### 4) Chiffres de revenus annoncés
*   **Revenus annoncés** : **Non précisé.** L'auteur se concentre uniquement sur la partie technique du développement.
