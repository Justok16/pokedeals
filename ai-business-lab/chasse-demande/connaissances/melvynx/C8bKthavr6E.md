# Récupérer et Afficher des Données d’API avec HTML / JavaScript et Fetch

Vidéo : https://youtu.be/C8bKthavr6E · durée 6:08 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Apprendre à récupérer des données depuis une API avec `fetch` et à les afficher dynamiquement dans le DOM HTML en manipulant les éléments en JavaScript pur.
2) **Outils, sites ou dépôts cités :**
- **JSONPlaceholder** (gratuit, API de test pour récupérer des utilisateurs).
- **Codeline** (plateforme de formation payante de l'auteur, mentionnée pour ses cours).
3) **Astuces concrètes et réutilisables :**
- Utiliser `fetch(url).then(res => res.json())` pour récupérer et parser des données JSON.
- Sélectionner un élément du DOM avec `document.querySelector()`.
- Créer des éléments dynamiquement avec `document.createElement()`, définir leur texte avec `innerText` (plutôt que `innerHTML` pour éviter les failles XSS), et les insérer dans un parent avec `appendChild()`.
- Itérer sur un tableau de données avec une boucle `for...of` pour générer du contenu HTML itératif.
4) **Chiffres de revenus :** Non précisé.
