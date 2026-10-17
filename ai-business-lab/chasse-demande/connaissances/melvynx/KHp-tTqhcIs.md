# 1 an Après NextJS App Router (14) : Mon retour après 7 applications

Vidéo : https://youtu.be/KHp-tTqhcIs · durée 7:14 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo fait le bilan après plus d'un an d'utilisation quotidienne du nouveau **Next.js App Router**, en détaillant ses points forts (Server Components, gestion des Data Fetching avec `async/await`, layouts imbriqués, Server Actions) et ses points faibles (absence d'accès direct à la Request HTTP dans certains contextes, performances du serveur de dev, gestion des erreurs en production).

2) **Outils, sites ou dépôts GitHub cités** :
   - **Next.js (App Router)** : Gratuit, framework React.
   - **Prisma** : Gratuit (ORM open source), utilisé pour la base de données dans les exemples.
   - **TurboPack** : Gratuit, le bundler ultra-rapide successeur de Webpack.
   - **YouCode** : Payant / Freemium (plateforme de formation de l'auteur mentionnée en description), projet complet développé de A à Z.
   - **mlv.sh/react** : Gratuit (lien vers la formation de l'auteur).

3) **Astuces concrètes et réutilisables** :
   - Utiliser les **Server Components** pour effectuer des requêtes de données directement dans le composant avec `async/await` sans avoir besoin de méthodes complexes comme `getServerSideProps` ou de typages verbeux.
   - Utiliser **`<Suspense>`** pour afficher des loaders de manière déclarative pendant le chargement des données asynchrones.
   - Structurer l'application avec des **Layouts** imbriqués (`layout.tsx`) pour partager des structures d'interface (menus, barres latérales) entre plusieurs pages de manière propre et performante.
   - Remplacer les routes API traditionnelles par des **Server Actions** (`"use server"`) combinées au hook `useAction` pour simplifier la validation des props et la mise à jour des données en quelques lignes de code.

4) **Chiffres de revenus annoncés** : Non précisé.

---
