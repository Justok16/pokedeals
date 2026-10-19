# Utiliser AXIOS est une ERREUR !

Vidéo : https://youtu.be/1nUR-cyblPo · durée 11:33 · résumé Gemini (gemini-3.1-flash-lite, lot de 9) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Critiques de la bibliothèque Axios et présentation d'alternatives plus légères, tout en expliquant pourquoi la gestion globale des requêtes est une mauvaise pratique.
2) **Outils/Sites :**
*   Axios : gratuit, bibliothèque de requêtes HTTP.
*   Ky (github.com/sindresorhus/ky) : gratuit, alternative légère à Axios basée sur Fetch.
*   Mande (github.com/developit/mande) : gratuit, alternative ultra légère à Axios.
*   Redux : gratuit, outil de gestion d'état (déconseillé par l'auteur).
3) **Astuces concrètes :** Créer des fonctions "wrapper" autour de l'API `fetch` native pour simplifier les requêtes au lieu d'installer des bibliothèques lourdes. Éviter d'utiliser des instances globales d'Axios qui peuvent causer des bugs difficiles à tracer.
4) **Revenus :** Non précisé.
