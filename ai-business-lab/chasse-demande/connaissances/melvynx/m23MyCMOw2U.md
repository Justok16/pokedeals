# CETTE ERREUR NEXTJS

Vidéo : https://youtu.be/m23MyCMOw2U · durée 1:00 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Résoudre l'erreur d'hydratation « Text content does not match server-rendered HTML » en utilisant un hook personnalisé pour forcer le rendu côté client uniquement.
2) **Outils, sites ou dépôts GitHub cités :**
- React (framework, gratuit).
3) **Astuces concrètes et réutilisables :**
- Créer un hook personnalisé (ex: `useIsClient`) utilisant `useState` (initialisé à `false`) et `useEffect` pour basculer l'état à `true` dès que le JavaScript est activé.
- Conditionner le rendu d'un composant lourd ou sensible (ex: calcul dynamique basé sur `Date.now()`) à cet état `isClient` : si le client n'est pas prêt, retourner un état de chargement (`loading`) ou ne rien rendre pour éviter le décalage entre le serveur et le client.
4) **Chiffres de revenus annoncés :**
- Non précisé.
