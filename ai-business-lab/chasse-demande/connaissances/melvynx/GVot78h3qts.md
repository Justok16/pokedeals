# LE CACHE EN NEXTJS

Vidéo : https://youtu.be/GVot78h3qts · durée 0:58 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Comment éviter les appels multiples et redondants de requêtes ou calculs dans les pages et layouts en Next.js / React en utilisant la fonction `cache` pour mémoriser les résultats.
2) **Outils, sites ou dépôts GitHub cités :**
- **React** (avec sa fonction `cache`, gratuit).
3) **Astuces concrètes et réutilisables :**
- Envelopper la méthode de requête ou de calcul avec la fonction `cache` de React pour que la requête ne s'exécute qu'une seule fois lors du rendu du contexte (page et layout confondus).
- Importer la fonction `cache` depuis `react` et l'appliquer autour de la fonction asynchrone (`cache(async () => ...)`).
4) **Chiffres de revenus annoncés :**
- Non précisé.
