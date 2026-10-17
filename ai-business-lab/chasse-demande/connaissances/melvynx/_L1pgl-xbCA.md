# Claude MAX : Nouveau modèle SANS LIMITE (mais très chère) | Cursor

Vidéo : https://youtu.be/_L1pgl-xbCA · durée 10:08 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :**
L'auteur teste et analyse les performances, l'utilité et le coût de l'utilisation de la nouvelle option **Claude 3.7 Max** (et du mode *Thinking*) intégrée dans l'éditeur Cursor pour effectuer des tâches complexes de refactoring de code et de correction de bugs.

3) **Outils, sites, dépôts GitHub et services cités :**
* **Cursor** (payant/abonnement) : Éditeur de code basé sur l'IA (utilisé avec les modèles Claude).
* **Claude 3.7 Sonnet / Claude 3.7 Max** (propriétaire/payant via API ou abonnement Cursor) : Modèles d'IA d'Anthropic utilisés pour le code.
* **TypeScript** (gratuit/open source) : Langage de programmation.
* **GitHub** (gratuit) : Plateforme de code source.
* **Lien de formation payant de l'auteur :** `mlv.sh/ia` ou `mlv.sh/fullstack` (mentionné à la fin de la vidéo).

3) **Astuces concrètes et réutilisables :**
* Utiliser les modèles avancés avec une grande fenêtre de contexte (comme Claude 3.7) pour permettre à l'IA de voir l'ensemble du projet et de faire des refactorings globaux de composants sans se limiter.
* Désactiver ou limiter l'autocorrection automatique de l'IA lors des modifications en chaîne (tool calls) pour éviter de consommer trop de requêtes et de faire exploser les coûts facturés à l'appel.
* Spécifier clairement à l'agent IA de ne pas corriger à l'infini les erreurs de type mineures (`tsc`) si cela entraîne une boucle de facturation excessive.
* Utiliser des instructions précises pour cibler les composants à modifier (ex: timeline de composants partagés) afin d'optimiser le nombre de tokens consommés.

4) **Chiffres de revenus annoncés (et coûts) :**
* Coût de Claude 3.7 Max (selon les captures d'écran et dires de l'auteur) : **0,05 $ par requête** + **0,05 $ par tool call**.
* Exemple de coût d'une session de refactoring montrée dans la vidéo : **5,64 $ au total** (dont 0,10 $ + 0,50 $ pour le prompt actuel, et d'autres sessions coûtant par exemple 20 tool calls soit ~1,20 $ à 1,50 $ l'appel).

---
