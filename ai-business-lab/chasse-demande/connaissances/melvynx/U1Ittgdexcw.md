# React 19 est cassé... drama

Vidéo : https://youtu.be/U1Ittgdexcw · durée 12:11 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Analyse des modifications apportées à l'API `Suspense` dans React 19, de leur impact sur le fonctionnement en cascade (*waterfall*) des requêtes et des solutions de contournement (*render-as-you-fetch*).

2) **Outils, sites ou dépôts GitHub cités** :
- **React 19** : Gratuit, bibliothèque JavaScript.
- **React Query** : Gratuit, bibliothèque de gestion de requêtes asynchrones pour React.
- **TanStack Router** : Gratuit, routeur pour applications React.
- **TanStack Query** : Gratuit, outil de gestion d'état serveur.

3) **Astuces concrètes et réutilisables** :
- Dans React 19, l'utilisation de `Suspense` avec des requêtes parallèles (comme `react-query`) peut provoquer des *waterfalls* si les requêtes se déclenchent de manière séquentielle au lieu d'être initiées en amont.
- Utiliser l'approche *render-as-you-fetch* (en déclenchant les requêtes le plus tôt possible, par exemple dans les chargeurs de routeurs comme TanStack Router) pour exécuter les requêtes en parallèle et éviter les temps de chargement en cascade.
- Ne pas afficher un composant `Suspense` unique pour l'ensemble d'un arbre lourd sans anticiper l'ordre de résolution des promesses, car un composant lent peut bloquer le rendu global.

4) **Chiffres de revenus annoncés** : Non précisé.

---
