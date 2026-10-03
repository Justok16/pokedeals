# ATTENTION : 1 million de contexte est LA PIRE chose que tu puisses faire

Vidéo : https://youtu.be/OTxy6NabllI · durée 13:01 · résumé Gemini (gemini-3.1-flash-lite) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo structuré selon vos besoins :

### 1) Idée principale
L'auteur déconseille d'utiliser de très larges fenêtres de contexte (comme les 1 million de tokens de GPT-5.6) lors de l'utilisation de modèles d'IA pour le développement (avec Claude Code), car cela multiplie inutilement les coûts. Il recommande plutôt de privilégier des contextes "compacts" qui permettent de maintenir la performance tout en réduisant drastiquement les frais, en évitant les zones de performance dégradée ("dumb zone").

### 2) Outils, sites et dépôts GitHub cités
*   **OpenAI Developers (Pricing) :** Site officiel pour consulter les tarifs des modèles. Payant (selon la consommation). Sert à comparer les coûts des tokens en entrée/sortie et les options de cache.
*   **Claude Code :** Outil de développement assisté par IA. Payant (via abonnement API). Sert à coder et automatiser des tâches de développement.
*   **Lumail :** Logiciel créé par l'auteur pour envoyer des e-mails marketing. Payant/Freemium. Sert à gérer des e-mails de manière contrôlée et agentique.
*   **AIHero (AI Coding Crash-Course) :** Cours de programmation cité par l'auteur. Gratuit (selon le bandeau). Sert à se former sur les "modes d'échec" des modèles, comme la "smart zone".
*   **CodeLynx / Cursor :** Mentionnés comme outils de développement. Payants/Freemium. Servent à optimiser le flux de travail avec l'IA.

### 3) Astuces concrètes et réutilisables
*   **Gestion du contexte :** Ne jamais saturer la fenêtre de contexte (ex: 1 million de tokens). Privilégiez des cycles de "compaction" pour réinitialiser le contexte, ce qui réduit les coûts de requête.
*   **Utilisation du "Cache" :** Exploiter le *tool caching* pour diviser par 10 les coûts de certaines requêtes.
*   **Éviter la "Dumb Zone" :** Rester en dessous de 125k-150k tokens pour éviter que le modèle ne devienne "paresseux" (hallucinations, erreurs de logique, perte d'attention).
*   **Découpage des tâches :** Diviser les projets complexes en petites sous-tâches gérables pour que le modèle reste efficace à chaque étape (approche "one-shot").

### 4) Chiffres de revenus annoncés ("affirmé par l'auteur")
*   **Coût mensuel d'un abonnement Claude Max 20x :** 200 $
*   **Valeur API équivalente mensuelle pour Claude Max 20x :** 18 883 $
*   **Valeur API équivalente mensuelle pour Codex :** 8 610 $
*   *Note : L'auteur insiste sur le fait que ces montants ne sont pas des revenus directs, mais une estimation de la valeur que l'utilisation de ces abonnements apporte par rapport à une utilisation directe de l'API au tarif public.*
