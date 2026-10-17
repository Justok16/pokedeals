# React Query est MORT à cause des Server Components ? (spoiler :)

Vidéo : https://youtu.be/cA1yJ63FDDI · durée 8:43 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-13
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : La vidéo démontre par la comparaison des statistiques de téléchargement et de la complexité du code que **Zustand** et **Tanstack Query** restent extrêmement pertinents et indispensables face aux React Server Components, en évitant la surcharge de code et de re-renders inutile par rapport à l'utilisation brute de `useContext`.
2) **Outils, sites ou dépôts GitHub cités** :
   - **Zustand** : Bibliothèque de gestion d'état pour React (gratuite).
   - **Tanstack Query (React Query)** : Bibliothèque de gestion des requêtes serveur pour React (gratuite).
   - **React / Next.js** : Frameworks et bibliothèque front-end (gratuits).
   - **mlv.sh/react** : Lien vers une formation sur React (non précisé).
3) **Astuces concrètes et réutilisables** :
   - Utiliser Zustand pour réduire drastiquement la quantité de code par rapport à une implémentation native avec `useContext` (qui nécessite provider, reducer, create context, hooks, etc.).
   - Profiter de l'optimisation des re-renders de Zustand grâce aux sélecteurs pour ne re-rendre un composant que lorsque la donnée ciblée change.
   - Utiliser Tanstack Query pour bénéficier du caching automatique entre les pages, de la revalidation ciblée et de la gestion des requêtes asynchrones sans alourdir les composants serveur.
4) **Chiffres de revenus annoncés** :
   - Non précisé.
