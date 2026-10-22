# Vidéo https://youtu.be/tTnUcSj-QPA

> Résumé produit par Gemini (via le relais Vercel) le 25/09/2026. Les chiffres de revenus sont **affirmés par l’auteur de la vidéo, non vérifiés**.

Voici un résumé de la vidéo, spécialement pour quelqu'un cherchant à monétiser l'IA avec Claude Code :

### Idée Principale

La vidéo présente **Jev**, un nouveau modèle d'IA "System 1" (pensée rapide) conçu par un co-inventeur de ChatGPT. Contrairement aux LLM traditionnels (dits "System 2", pensée lente) qui génèrent du texte, Jev est optimisé pour les décisions rapides, la classification et le routage. Il est 20 à 200 fois plus rapide et 40 à 400 fois moins cher (avec les tokens de sortie gratuits), ce qui le rend idéal pour des automatisations de masse et la réduction des coûts, surtout lorsqu'il est combiné avec des modèles "System 2" comme Claude.

---

### Outils, Sites et Dépôts GitHub Citées

1.  **Jev** (modèle d'IA)
    *   **Gratuit/Payant :** Payant pour les tokens d'entrée (0,042 $ par 1 million de tokens), gratuit pour les tokens de sortie.
    *   **À quoi il sert :** Un nouveau type de modèle d'IA frontalier, optimisé pour la classification, la prise de décision, et le routage rapide. Il ne génère pas de texte mais répond en 3 formats : vrai/faux (avec un score de confiance), sélection d'options, ou une échelle (ex: 0 à 10).
2.  **TypeSafe AI Console** (`console.typesafe.ai`)
    *   **Gratuit/Payant :** Payant (0,042 $ par 1 million de tokens d'entrée).
    *   **À quoi il sert :** Plateforme pour accéder directement à Jev (sans liste d'attente désormais).
3.  **OpenRouter** (`openrouter.ai`)
    *   **Gratuit/Payant :** Payant (0,042 $ par 1 million de tokens d'entrée pour `typesafe/jev-1.13`, facturé exactement).
    *   **À quoi il sert :** Un service qui agrège les derniers modèles d'IA, y compris Jev, offrant une interface unifiée. C'est la méthode d'accès que l'auteur utilise.
4.  **Vercel AI Gateway** (`typesafe-ai/jev`)
    *   **Gratuit/Payant :** Payant (0,042 $ par 1 million de tokens d'entrée, gratuit jusqu'au 25 septembre [non précisé l'année]).
    *   **À quoi il sert :** Une passerelle AI pour accéder à Jev.
5.  **Cloudflare Workers AI** (`typesafe/jev`)
    *   **Gratuit/Payant :** Payant (le prix est affiché sur le tableau de bord Cloudflare).
    *   **À quoi il sert :** Une plateforme pour exécuter Jev.
6.  **Claude Code** (ou "Agentic Harnesses")
    *   **Gratuit/Payant :** Non précisé.
    *   **À quoi il sert :** L'environnement de travail de l'auteur pour interagir avec les agents AI et intégrer des modèles comme Jev.
7.  **"Thinking, Fast and Slow"** (livre de Daniel Kahneman)
    *   **Gratuit/Payant :** Payant (livre).
    *   **À quoi il sert :** Référence conceptuelle pour la distinction entre "System 1" (pensée rapide et intuitive) et "System 2" (pensée lente et délibérative), appliquée aux modèles AI.
8.  **The RoboNuggets Community** (`skool.com/robonuggets`)
    *   **Gratuit/Payant :** Non précisé (cours et communauté).
    *   **À quoi il sert :** Une communauté et des cours ("The Claude Living Masterclass", "Agents-as-a-Service") pour apprendre à construire et vendre des systèmes d'IA aux entreprises.
9.  **Guide PDF "Jev + Claude the setup guide"**
    *   **Gratuit/Payant :** Gratuit (disponible via un lien sous la vidéo).
    *   **À quoi il sert :** Un guide détaillé pour configurer Jev et l'intégrer à votre agent Claude.
10. **Unclutter** (extension Chrome)
    *   **Gratuit/Payant :** Open source et gratuit (mais utilise Jev, qui est payant).
    *   **À quoi il sert :** Une extension qui nettoie automatiquement les pages web en supprimant les éléments "superflus" (publicités, bannières de cookies, upsells, dialogues), Jev étant utilisé en coulisses pour la classification.

---

### Astuces Concrètes et Réutilisables

1.  **Combiner les forces "System 1" et "System 2" :** Utilisez Jev (System 1) pour prendre des décisions rapides et classer les données, puis transmettez les tâches plus complexes nécessitant une génération de texte ou un raisonnement approfondi à un LLM comme Claude (System 2).
2.  **Optimiser les coûts avec le routage de modèles (Model Routing) :** Configurez votre agent pour que Jev évalue la complexité d'une tâche et la route vers le modèle Claude le plus approprié (Haiku pour les tâches simples, Sonnet pour le moyen, Opus/Fable pour le complexe). Cela permet des économies significatives (jusqu'à **70% affirmé par l'auteur**).
    *   *Astuce concrète :* Utilisez le prompt fourni dans la vidéo (visible à 5:45) pour créer un routeur de modèles basé sur Jev.
3.  **Accélérer le choix des compétences (Skill Routing) :** Pour les agents qui ont de nombreuses "compétences" (instructions enregistrées), utilisez Jev pour identifier la compétence pertinente en une fraction de seconde, plutôt que de faire lire toute la liste à un LLM plus lent. C'est 5.7x plus rapide qu'Opus 5 (affirmé par l'auteur).
    *   *Astuce concrète :* Utilisez le prompt fourni dans la vidéo (visible à 7:56) pour créer un "Skill Router" avec Jev.
4.  **Construire des automatisations à grande vitesse :** Exploitez la rapidité et le coût réduit de Jev pour classer de gros volumes de données (e-mails, tickets de support, factures, statuts clients).
    *   *Exemples :* Classification d'e-mails (chaud/froid/pas un lead), détection de fraude sur les factures, modération de contenu, identification de clients à risque de désabonnement.
5.  **Créer de nouvelles applications économiquement viables :** Jev permet le développement d'applications qui étaient auparavant trop coûteuses ou lentes avec des LLM.
    *   *Exemple :* Recherche sémantique d'images et de vidéos (par "signification" plutôt que par nom de fichier), détection et suppression automatique d'éléments indésirables sur une page web.
6.  **Intégrer Jev à votre Agentic OS :** Le guide PDF et le prompt de démarrage vous aideront à configurer Jev dans votre environnement de développement (ex: Claude Code) pour commencer à l'utiliser immédiatement.

---

### Chiffres de revenus annoncés (affirmé par l'auteur)

*   **Martin Ebongue (membre de la communauté) :** A remporté un contrat de 30 000 $ pour développer une application mobile.
*   **Ryan Ayler (membre de la communauté) :** A réalisé une "construction de 2k et un abonnement de 500$/mois".
*   **Mark Brandon (membre de la communauté) :** A livré un projet de 40 000 $.
