# Pourquoi je suis addict aux Server Components (je ne retournerais pas en arrière)

Vidéo : https://youtu.be/k-TCrbADq54 · durée 11:25 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Analyse des React Server Components, de leurs avantages techniques (zéro bundle size, accès direct au backend, code splitting automatique) et de leur utilisation pratique avec Next.js.

2) **Outils, sites et dépôts GitHub cités** :
- **React** (gratuit, bibliothèque JavaScript).
- **Next.js** (gratuit, framework React).
- **Marked** (gratuit, bibliothèque de rendu Markdown).
- **Prisma** (gratuit/payant, ORM).
- **Better-Auth** (gratuit, bibliothèque d'authentification).
- **Tailwind CSS** (gratuit, framework CSS).
- **Lucide React** (gratuit, bibliothèque d'icônes).

3) **Astuces concrètes et réutilisables** :
- Utiliser les Server Components pour exécuter du code lourd côté serveur et ne renvoyer que le HTML final au client, réduisant ainsi la taille du bundle JavaScript.
- Effectuer des requêtes directement depuis les composants serveur (accès direct au système de fichiers ou à la base de données via Prisma).
- Tirer parti du code splitting automatique : seuls les composants affichés ou nécessaires sont chargés par le client.
- Mettre en place un système de cache par composant (ex. `unstable_cache` ou `use cache`) pour optimiser les performances des pages à fort trafic.
- Utiliser `Suspense` pour gérer les états de chargement de manière granulaire et non bloquante pour toute la page.
- Combiner Server Actions et Server Components pour simplifier les mutations de données sans API intermédiaire complexe.

4) **Chiffres de revenus annoncés** : Non précisé.
