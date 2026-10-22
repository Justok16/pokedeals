# React a été hacké. Ce n'est pas une blague (important).

Vidéo : https://youtu.be/MlW3ZKGlu58 · durée 14:58 · résumé Gemini (gemini-3-flash-preview, lot de 4) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Démonstration technique et exploitation d'une faille de sécurité critique (CVE-2025-55182 nommée "React2Shell") impactant React et Next.js, montrant comment un attaquant peut prendre le contrôle total d'un serveur via les *Server Actions*. L'auteur utilise l'IA pour aider à corriger et automatiser son script d'exploitation à des fins de démonstration.

2) **Outils, sites ou dépôts cités** :
*   **React / Next.js** (Open-source, gratuit) : Frameworks web servant de base à l'analyse.
*   **Claude Code** (Payant) : Utilisé via l'outil `Claude Code` pour corriger des erreurs de syntaxe et suggérer des imports dynamiques dans le script d'exploitation.
*   **Bun** (Open-source, gratuit) : Runtime JavaScript utilisé pour exécuter les scripts d'exploitation (`bun run`).
*   **GitHub** (Gratuit/Payant) : Cité comme source pour trouver le Proof of Concept (PoC) original de la faille.
*   **Excalidraw** (Gratuit/Payant) : Utilisé pour schématiser le fonctionnement des échanges de données entre Backend et Frontend.

3) **Astuces concrètes et réutilisables** :
*   **Mise à jour impérative** : Toujours utiliser les dernières versions de React et Next.js pour corriger les failles d'exécution de code à distance (RCE).
*   **Utilisation de l'IA pour le débogage** : En cas d'erreur de syntaxe ou de bibliothèque manquante dans un script technique, soumettre l'erreur à Claude Code pour obtenir un correctif immédiat (ex: passage aux imports dynamiques).
*   **Sécurisation des entrées** : Ne jamais faire confiance aux données envoyées par l'utilisateur, même via des champs cachés ou encodés.

4) **Chiffres de revenus annoncés** : Aucun chiffre de revenu direct mentionné.
