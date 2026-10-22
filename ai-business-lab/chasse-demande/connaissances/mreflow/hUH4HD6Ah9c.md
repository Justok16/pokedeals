# Le benchmark que personne n'a demandé !

Vidéo : https://youtu.be/hUH4HD6Ah9c · durée 1:03 · résumé Gemini (gemini-3.5-flash-lite, lot de 9) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Présentation d'un benchmark (« Busey Bench ») consistant à demander à différents modèles d'IA de dessiner la personnalité de Gary Busey en écrivant directement du code SVG (Scalable Vector Graphics).

2) **Outils, sites ou dépôts GitHub cités :**
*   **GPT-3.5 Turbo / OpenAI :** Payant (via API). Modèle de langage testé pour générer du code SVG.
*   **Fable :** Non précisé. Outil ou framework utilisé pour construire la page de benchmark et le site web comparatif.

3) **Astuces concrètes et réutilisables :**
*   Comprendre que les fichiers SVG sont intrinsèquement du code (balises `<svg>`, `<path>`, `<circle>`, `<line>`, etc.) et que les modèles de langage peuvent générer des graphiques vectoriels complexes en écrivant directement ce code géométrique, sans passer par un générateur d'images matricielles traditionnel.
*   Créer des benchmarks personnalisés pour comparer objectivement différents LLM sur des tâches spécifiques (coût, temps d'exécution, nombre de tokens utilisés, qualité du code généré).

4) **Chiffres de revenus annoncés :**
*   **0,0036 $ à 0,0059 $ :** Coût par exécution/génération selon les modèles testés (ex. GPT-3.5 Turbo) (« affirmé par l'auteur » en montrant le tableau comparatif des coûts par token de l'interface de benchmark).
