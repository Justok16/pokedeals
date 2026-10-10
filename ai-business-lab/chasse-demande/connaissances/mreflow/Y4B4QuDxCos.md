# Cet agent IA vient d'écrire un livre en 60 secondes

Vidéo : https://youtu.be/Y4B4QuDxCos · durée 22:43 · résumé Gemini (gemini-3.5-flash-lite, lot de 6) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale** : La vidéo montre comment créer un agent IA complet capable d'écrire un livre de 10 chapitres de A à Z (du titre et du synopsis jusqu'à la rédaction détaillée de chaque chapitre) en utilisant l'outil d'automatisation MindStudio.
2. **Outils, sites ou dépôts GitHub cités** :
   - **MindStudio (mindstudio.ai)** : payant/freemium, plateforme sans code (no-code) pour concevoir, construire et déployer des agents IA (sponsor de la vidéo).
   - **Perplexity** : payant/freemium, modèle IA utilisé comme source d'information dans les workflows.
   - **GPT-5** : payant, modèle de langage d'OpenAI utilisé pour la génération de texte (mentionné dans l'interface de test).
   - **Claude 3 (Haiku / Sonnet)** : payant, modèle de langage d'Anthropic (mentionné dans l'interface de test).
   - **Future Tools (futuretools.io)** : gratuit (newsletter), site de veille sur l'IA (sponsor).
3. **Astuces concrètes et réutilisables** :
   - Structurer un agent IA en blocs séquentiels : d'abord récupérer les entrées utilisateur (titre, genre, description), puis utiliser un bloc logique (Logic) pour déterminer si une description est fournie ou doit être générée automatiquement.
   - Utiliser un bloc de génération de texte pour créer une table des matières (TOC) détaillée basée sur le synopsis, puis injecter cette table dans les blocs suivants pour guider l'écriture chapitre par chapitre.
   - Faire en sorte que chaque chapitre généré prenne en compte le texte du chapitre précédent (en injectant la variable du chapitre antérieur dans le prompt) pour assurer la continuité narrative de l'histoire.
   - Configurer des limites de jetons élevées (Max Response Size) dans les paramètres du modèle (comme GPT-5) pour permettre la rédaction de longs chapitres (minimum 2 000 mots).
   - Utiliser un bloc de type « Word Document » pour afficher et exporter proprement le résultat final de l'agent.
4. **Chiffres de revenus annoncés** : non précisé.
