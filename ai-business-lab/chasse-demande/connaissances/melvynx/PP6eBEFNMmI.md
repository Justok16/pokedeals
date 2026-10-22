# Voici les Nouveautées de NextJS 13.3 ! (Tout ce qu'il faut savoir)

Vidéo : https://youtu.be/PP6eBEFNMmI · durée 13:31 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** Présentation des nouveautés de la version 13.3 de Next.js, incluant la gestion avancée des métadonnées, la génération dynamique d'images Open Graph, le support de l'export statique, et les fonctionnalités expérimentales de routage parallèle et d'interception.
2. **Outils et dépôts cités :**
   - **Next.js 13.3 :** Gratuit, framework web React.
   - **Vercel :** Gratuit/Payant, plateforme de déploiement.
   - **Tailwind CSS :** Gratuit, framework CSS.
3. **Astuces concrètes :**
   - Utiliser l'objet `metadata` (ou `generateMetadata`) pour gérer le SEO (titre, description, etc.).
   - Configurer des fichiers dédiés à la racine (`favicon.ico`, `sitemap.js`, `robots.txt`, `manifest.js`).
   - Utiliser `ImageResponse` de `next/server` pour générer dynamiquement des images Open Graph personnalisées via JSX, HTML et CSS.
   - Configurer `output: 'export'` dans `next.config.js` pour un export statique de l'application Node.
   - Utiliser la convention des dossiers nommés avec `@` (slots) pour les *Parallel Routes* et les dossiers entre parenthèses avec `..` pour les *Intercepting Routes*.
4. **Chiffres de revenus :** Non précisé.
