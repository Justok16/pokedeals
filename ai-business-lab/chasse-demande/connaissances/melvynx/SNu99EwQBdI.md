# Je m'étais TROMPÉ : Claude Code est tellement puissant (comparaison Cursor)

Vidéo : https://youtu.be/SNu99EwQBdI · durée 18:09 · résumé Gemini (gemini-flash-lite-latest, lot de 8) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de comparer en détail deux outils de développement assistés par IA, Cursor et Claude Code, à travers une grille multicritère (prix, facilité d'utilisation, résultats, workflow), en démontrant la supériorité de Claude Code malgré un coût d'API potentiellement plus élevé mais compensé par une absence de limites restrictives d'abonnement fixe et une autonomie poussée via le terminal.

2) Outils, sites et dépôts cités :
- Cursor : Éditeur de code (version Hobby gratuite, version Pro à 20 $/mois incluant une limite de requêtes d'agent).
- Claude Code : Assistant CLI en terminal (utilisant les clés API Claude ou un abonnement, évalué ici à environ 64 $/mois en usage intensif, ou 20 $/mois avec Claude Pro).
- GitHub / GitHub CLI (gh) : Outil de gestion de code et de recherche d'issues (gratuit).
- Excalidraw : Outil de tableau blanc (gratuit) utilisé pour dessiner le tableau comparatif.
- ChatGPT (OpenAI) : Outil d'IA (gratuit/payant) utilisé pour comparer la qualité de deux codes générés.

3) Astuces concrètes et réutilisables :
- Utiliser un script de configuration "git worktree" (`setup-worktree.sh`) combiné avec Claude Code pour isoler chaque tâche (résolution d'issue GitHub) dans une branche et un dossier séparé sans perturber le projet principal.
- Automatiser la création de "pull requests" et l'exécution de tâches complexes en combinant Claude Code, `gh issue view` et des fichiers de consignes (`run-tasks.md`).
- Comparer l'efficacité des assistants de code en analysant objectivement le prix au token, la facilité d'intégration dans le terminal et la qualité du code généré (via des tests comparatifs de code cleaners).

4) Chiffres de revenus annoncés (affirmés par l'auteur) :
- Non précisé.
