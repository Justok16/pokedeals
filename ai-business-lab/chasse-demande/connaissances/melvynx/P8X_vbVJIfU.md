# COMMENT BIEN GÉRER TES METADATAS

Vidéo : https://youtu.be/P8X_vbVJIfU · durée 1:00 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Gérer les métadonnées de pages dynamiques et améliorer le système de journalisation (logs) en Next.js.
2) **Outils, sites ou dépôts GitHub cités :**
   - **Next.js** (non précisé, framework web) : utilisé pour la gestion des pages et des layouts.
   - **ts-log** (non précisé, bibliothèque) : bibliothèque de journalisation.
3) **Astuces concrètes et réutilisables :**
   - Utiliser `unstable_cache` pour éviter les requêtes inutiles lors de la récupération des métadonnées d'un produit.
   - Placer les métadonnées dans le fichier `layout.tsx` pour que tous les enfants de la page en héritent.
   - Utiliser `generateParentMetadata` avec un suffixe pour réutiliser et enrichir les métadonnées du parent.
   - Remplacer les `console.log` par `logger.debug` (de `ts-log`) en configurant le `minLevel` selon l'environnement (0 en dev, 3 en production) pour un affichage plus lisible et masqué en production.
4) **Chiffres de revenus annoncés :**
   - Non précisé.
