# ARRÊTE d'utiliser useState, mets plutôt le state dans l'URL

Vidéo : https://youtu.be/zt18IWj9nF0 · durée 15:55 · résumé Gemini (gemini-flash-lite-latest, lot de 4) du 2026-10-16
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :**
La vidéo présente la bibliothèque **nuqs** pour Next.js, qui permet de gérer l'état des paramètres de recherche dans l'URL de manière sécurisée (*type-safe*), en synchronisant l'interface utilisateur avec l'URL côté client et côté serveur.

2) **Outils, sites ou dépôts GitHub cités :**
- **Next.js** (Gratuit, framework React) ;
- **nuqs** (Gratuit, bibliothèque open-source de gestion d'état des search params pour Next.js) ;
- **Prisma** (Gratuit, ORM pour bases de données) ;
- **TypeScript** (Gratuit, sur-ensemble de JavaScript typé) ;
- **VS Code** (Gratuit, éditeur de code) ;
- **Excalidraw** (Gratuit, outil de dessin de schémas) ;
- **NOW.TS** (Payant, template/cours payant de l'auteur pour créer des applications de production).

3) **Astuces concrètes et réutilisables :**
- Utiliser `useQueryState` (provenant de `nuqs`) pour lier l'état d'un input de recherche directement à l'URL.
- Utiliser `createSearchParamscache` et les fonctions de parsing (`parseAsInteger`, `parseAsString`) côté serveur pour valider et typer les paramètres de l'URL sans utiliser de composants clients superflus.
- Désactiver le paramètre `shallow` (`shallow: false`) pour forcer le re-rendu et la mise à jour des props serveur et des composants parents lors d'un changement dans l'URL.
- Utiliser l'option `throttleMs` (ex. `500` ms) pour limiter la fréquence des requêtes lors de la saisie rapide de l'utilisateur dans un champ de recherche.
- Récupérer les search params directement depuis les `props` d'une page Next.js et les parser avec `.parse(searchParams)`.

4) **Chiffres de revenus annoncés :**
- Non précisé.

---
