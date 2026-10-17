# Comment fonctionnent les Server Actions en NextJS ?

Vidéo : https://youtu.be/IyzyMviOkIo · durée 11:01 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Cette vidéo explique en détail le fonctionnement interne des Server Actions dans Next.js, en montrant notamment comment le code s'exécute côté serveur, comment le client appelle ces méthodes via des requêtes HTTP (avec des IDs d'actions et des en-têtes spécifiques), et comment Next.js gère le routage et le revalidation (rafraîchissement des pages) de manière transparente.
2) **Outils, sites ou dépôts GitHub cités** :
   - **Next.js** : Logiciel/Framework (gratuit) — utilisé pour construire l'application web et gérer les Server Actions.
   - **Escalidraw** : Site/Application (gratuit avec options payantes) — utilisé pour dessiner les schémas explicatifs du fonctionnement des Server Actions.
   - **TypeScript** : Langage (gratuit) — utilisé pour le code.
   - **Webpak** : Outil (gratuit) — utilisé en interne par Next.js pour bundler et traiter les modules.
   - **GitHub** : Site (gratuit/payant) — utilisé pour consulter le code source des packages internes de Next.js (`server-action-reducer.ts`, `router-reducer-types.ts`, etc.).
   - **Typefully** : Application/Site (payant/freemium) — utilisé pour tester les requêtes HTTP et les Server Actions.
3) **Astuces concrètes et réutilisables** :
   - Définir une Server Action en écrivant `"use server"` au début d'un fichier ou d'une fonction asynchrone pour exécuter du code exclusivement côté serveur.
   - Utiliser l'inspecteur réseau du navigateur pour observer les en-têtes personnalisés (comme `Next-Action` avec l'ID de l'action) et le payload envoyés lors de l'appel d'une Server Action.
   - Comprendre que Next.js analyse automatiquement les Server Actions importées dans une page lors du chargement initial pour générer les identifiants uniques (IDs d'actions).
   - Gérer les redirections et les revalidations de données (`revalidatePath`, etc.) directement depuis les en-têtes de réponse des Server Actions (`x-action-redirect`, `x-action-revalidated`).
4) **Chiffres de revenus annoncés** : Non précisé.
