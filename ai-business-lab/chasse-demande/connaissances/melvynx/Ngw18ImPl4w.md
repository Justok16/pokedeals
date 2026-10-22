# ARRÊTE d'utiliser useState, met plutôt le state dans l'URL !

Vidéo : https://youtu.be/Ngw18ImPl4w · durée 19:28 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Ce tutoriel explique pourquoi et comment synchroniser l'état d'une application (filtres de recherche, pagination, etc.) avec les paramètres de l'URL (Search Params) dans Next.js. L'auteur montre d'abord une implémentation native avec `useEffect` et `window.history.pushState`, puis démontre l'utilisation de la bibliothèque **nuqs** pour simplifier considérablement ce code et le rendre plus propre.

2) **Outils, sites et dépôts GitHub cités** :
- **Next.js** : Framework React utilisé pour l'application de démonstration. (Gratuit).
- **Prisma** : ORM pour interroger la base de données. (Gratuit).
- **SaveIt** : Application/extension de bookmarking (mentionnée pour illustrer le partage de liens). (Gratuit/Payant - non précisé).
- **nuqs** : Bibliothèque de gestion d'état sécurisée par les types pour les search parameters de React/Next.js (`?n=u&q=s`). (Gratuit / Open source).

3) **Astuces concrètes et réutilisables** :
- Garder l'état de l'application dans l'URL permet aux utilisateurs de partager le site en conservant exactement la même vue, de sauvegarder l'URL (bookmark) et d'utiliser les boutons de navigation (précédent/suivant) du navigateur.
- Utiliser le hook `useSearchParams` combiné avec `useRouter` (ou `window.history.pushState`) pour mettre à jour l'URL sans recharger la page entière.
- Utiliser la bibliothèque `nuqs` avec `useQueryState` pour synchroniser automatiquement l'état des composants (comme les sélecteurs de couleur) avec l'URL de manière déclarative.
- Configurer l'option `{ shallow: false }` ou utiliser les options de `nuqs` pour déclencher une requête serveur (Server Component revalidation) lors de la modification des paramètres.
- Parser les paramètres d'URL avec des validateurs (comme `parseAsStringEnum` ou `parseAsInteger`) pour s'assurer de la validité des données reçues.

4) **Chiffres de revenus annoncés** :
- **Affirmé par l'auteur** : Aucun chiffre de revenus n'est annoncé dans cette vidéo.

---
