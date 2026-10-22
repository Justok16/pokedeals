# 5 Optimisation Next.js 15 à faire maintenant dans ton CODE !

Vidéo : https://youtu.be/2HirbEqTzY4 · durée 12:26 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Cinq techniques d'optimisation des performances pour les applications **Next.js** afin d'améliorer la vitesse de chargement et l'expérience utilisateur (utilisation de **Suspense**, de skeletons de chargement, de **React Cache**, du placement bas des `use client`, et du filtrage des données dans les requêtes Prisma/API).
2) **Outils, sites ou dépôts GitHub cités :**
   - **Next.js** : Gratuit (open-source), framework React.
   - **React** : Gratuit (open-source), bibliothèque JavaScript.
   - **Prisma ORM** : Gratuit, gestion de base de données PostgreSQL.
   - **NextAuth** : Gratuit, solution d'authentification.
   - **Zustand** : Gratuit, gestionnaire d'état.
   - **Tailwind CSS** : Gratuit, framework CSS.
   - **VS Code** : Gratuit, éditeur de code.
3) **Astuces concrètes et réutilisables :**
   - **1. Utiliser `<Suspense>`** : Enrober les composants lents ou asynchrones dans des balises `<Suspense>` avec un `fallback` (comme des skeletons) pour afficher instantanément la structure de la page pendant que les données chargent.
   - **2. Utiliser `loading.tsx` avec des placeholders** : Créer des fichiers de chargement dédiés pour les routes afin d'améliorer le retour visuel immédiat pour l'utilisateur.
   - **3. Utiliser `react/cache` pour dupliquer les requêtes** : Mettre en cache les requêtes de données répétées (comme `getCurrentOrg()`) avec la fonction `cache()` de React pour éviter les appels multiples et superflus à la base de données lors d'un même rendu.
   - **4. Placer les composants client (`"use client"`) le plus bas possible dans l'arbre** : Garder un maximum de composants côté serveur (Server Components) pour réduire le JavaScript envoyé au client et améliorer le SEO et les performances.
   - **5. Sélectionner uniquement les données utiles (Prisma / API)** : Éviter de récupérer des objets complets ou des relations non nécessaires (`include` massif) en filtrant précisément les champs requis dans les requêtes Prisma pour alléger la charge réseau et base de données.
4) **Chiffres de revenus annoncés :** Non précisé.
