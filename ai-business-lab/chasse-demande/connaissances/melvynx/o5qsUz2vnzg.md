# Fetch API pour les nuls en 10 minutes

Vidéo : https://youtu.be/o5qsUz2vnzg · durée 12:49 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Apprendre à utiliser la fonction `fetch` en JavaScript pour récupérer et envoyer des données (GET, POST, DELETE) vers un serveur via le protocole HTTP, en gérant les promesses et les réponses JSON.
2) **Outils, sites ou dépôts cités :**
- **JSONPlaceholder** (gratuit, API en ligne pour les tests et le prototypage).
- **ChatGPT / IA** (mentionné pour l'utilisation potentielle d'outils d'assistance).
3) **Astuces concrètes et réutilisables :**
- Utiliser `fetch(url)` qui retourne une promesse (`Promise`), puis chaîner avec `.then(res => res.json())` pour transformer la réponse en objet JavaScript.
- Vérifier la propriété `ok` de la réponse pour s'assurer que la requête a réussi (statut 200–299).
- Pour une requête POST, passer un objet de configuration avec `method: 'POST'`, les `headers`, et un `body` sérialisé via `JSON.stringify()`.
- Utiliser l'onglet "Network" des outils de développement du navigateur pour inspecter les requêtes HTTP, le payload et les headers.
4) **Chiffres de revenus :** Non précisé.
