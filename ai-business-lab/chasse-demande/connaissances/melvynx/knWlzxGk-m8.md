# TUTO / COURS NextJS Server Component + Database Prisma COMPLET en 1 HEURE (2/5)

Vidéo : https://youtu.be/knWlzxGk-m8 · durée 52:29 · résumé Gemini (gemini-flash-lite-latest, lot de 4) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Maîtriser l'utilisation conjointe de Next.js (notamment les Server Components), de Prisma et d'une base de données PostgreSQL pour optimiser le rendu et la gestion des données (avec le cas pratique d'un système de gestion de reviews et de likes).
2) **Outils, sites ou dépôts GitHub cités** :
   - **Next.js** : Framework React (gratuit).
   - **Prisma** : ORM pour interagir avec les bases de données (gratuit/freemium).
   - **Prisma Studio** : Interface graphique pour Prisma (gratuit).
   - **GitHub** : Plateforme de code (gratuit).
   - **JSONPlaceholder** : API de test (gratuit).
   - **Lucide React** : Librairie d'icônes (gratuit).
3) **Astuces concrètes et réutilisables** :
   - Utiliser `use client` uniquement dans les composants interactifs nécessitant des hooks (`useState`, etc.).
   - Gérer le rendu côté serveur par défaut pour les composants Next.js afin d'améliorer les performances et de sécuriser les requêtes vers la base de données.
   - Utiliser `revalidatePath` pour rafraîchir dynamiquement les pages après une mutation de données (comme l'ajout ou la mise à jour d'une review).
   - Tirer parti de l'API `useOptimistic` pour une mise à jour instantanée de l'interface utilisateur avant la confirmation du serveur.
4) **Chiffres de revenus annoncés** : Non précisé.
