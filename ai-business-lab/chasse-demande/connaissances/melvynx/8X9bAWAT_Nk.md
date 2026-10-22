# JE Transforme TON Code React en Clean Code (Review)

Vidéo : https://youtu.be/8X9bAWAT_Nk · durée 11:14 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L'auteur analyse et corrige en direct le code source React/Next.js de membres de sa communauté Discord, en pointant les mauvaises pratiques (props drilling, mutations directes de tableaux, composants trop génériques, gestion maladroite des états) et en proposant des alternatives propres.

2) **Outils, sites ou dépôts GitHub cités :**
- **Discord :** Gratuit, plateforme de communauté utilisée pour collecter le code des abonnés.
- **VS Code :** Gratuit, éditeur de code.
- **GitHub :** Gratuit, plateforme de partage de code source.
- **Radix UI :** Gratuit, bibliothèque de composants accessibles (utilisée pour les accordéons/FAQ).
- **Tailwind CSS :** Gratuit, framework CSS.

3) **Astuces concrètes et réutilisables :**
- **Éviter de muter les props :** Ne jamais trier un tableau directement reçu en props (ex: `data.sort()`), mais utiliser des méthodes immutables comme `.toSorted()` ou dupliquer le tableau avant de le trier.
- **Typage et nommage des composants :** Éviter les noms de composants trop génériques comme `Card` ou `Legal` ; préférer des noms précis comme `ProductCard` ou `LegalDocument`.
- **Simplifier la gestion des états :** Éviter de multiplier les hooks `useState` pour chaque élément d'une liste ; centraliser l'état ou utiliser un store global (comme Zustand) si nécessaire.
- **Séparer les responsabilités :** Rendre les composants UI purs et réutilisables en évitant d'y imbriquer de la logique métier complexe (comme des appels API directs ou des switchs géants de rendu).

4) **Chiffres de revenus annoncés :**
- Non précisé.

---
