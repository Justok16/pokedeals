# Next.js 13: Les nouveautés à ABSOLUMENT connaître!

Vidéo : https://youtu.be/34Utg0x06rI · durée 15:54 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Comparaison entre Next.js 12 et Next.js 13, en mettant en avant les nouveautés majeures de la v13 (nouveau système de routing par dossiers, layouts, métadonnées simplifiées, gestion des erreurs, routes parallèles et interceptées, Server Actions et streaming).

2) **Outils, sites ou dépôts GitHub cités** :
- **Next.js 12** et **Next.js 13** (gratuit, framework React)
- **JSONPlaceholder** (gratuit, API de test)

3) **Astuces concrètes et réutilisables** :
- Utiliser le dossier `app/` de Next.js 13 pour structurer les routes et les layouts imbriqués de manière flexible.
- Définir un `layout.js` partagé pour envelopper automatiquement les pages d'un même dossier.
- Utiliser les fichiers `error.js` et `loading.js` pour gérer nativement les états d'erreur et de chargement avec les composants React `Suspense`.
- Remplacer l'ancienne balise `<Head>` par l'export de métadonnées `export const metadata = {}`.
- Utiliser les **Server Actions** (`"use server"`) pour exécuter du code côté serveur directement depuis les composants (ex: suppression d'un utilisateur sans API intermédiaire).
- Implémenter le **streaming** pour charger les composants de manière indépendante et améliorer les performances perçues.

4) **Chiffres de revenus** : Non précisé.

---
