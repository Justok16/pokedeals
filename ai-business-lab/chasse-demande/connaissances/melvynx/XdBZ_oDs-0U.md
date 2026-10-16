# TUTO / COURS React useEffect en 1 heure (3/5)

Vidéo : https://youtu.be/XdBZ_oDs-0U · durée 42:23 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Une masterclass complète sur le hook `useEffect` en React, expliquant son utilité principale, la gestion des dépendances, le cycle de vie (mount, update, unmount), le cleanup, le mode strict et les pièges courants.

2) **Outils, sites et dépôts GitHub cités :**
- **React / React DOM** (bibliothèque open-source gratuite) : Utilisé pour le développement web et la gestion des composants.
- **BeginReact / Codeline** (plateforme de formation gratuite/payante, lien `mlv.sh/react`) : Plateforme proposée par le créateur pour s'exercer sur React avec des exercices et des cours.
- **SWR** (bibliothèque open-source gratuite de Vercel) : Bibliothèque de data fetching pour React (mentionnée dans la conclusion).
- **TanStack Query** (bibliothèque open-source gratuite) : Alternative pour la gestion des données (mentionnée dans la conclusion).

3) **Astuces concrètes et réutilisables :**
- Utiliser `useEffect` pour gérer les "side effects" (effets de bord) qui échappent au cycle de rendu classique de React (comme la mise à jour du titre de la page avec `document.title` ou l'ajout d'écouteurs d'événements).
- Ne pas oublier de nettoyer les effets (cleanup) dans `useEffect` (par exemple avec `removeEventListener`) pour éviter les fuites de mémoire.
- Utiliser un tableau de dépendances vide `[]` pour exécuter un effet uniquement au montage du composant.
- Mettre en place un contrôleur d'annulation (`AbortController`) lors du fetch de données pour éviter les requêtes inutiles et synchroniser proprement les composants.

4) **Chiffres de revenus annoncés :**
- Non précisé.

---
