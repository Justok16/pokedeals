# Comment j’ai refactor toute une codebase avec l’AI

Vidéo : https://youtu.be/JI8N8oMBV7U · durée 9:25 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de présenter une automatisation complète de la migration de plus de 255 fichiers d'une bibliothèque vers une version majeure à l'aide d'un script Node.js couplé à l'IA (OpenAI), puis de la correction automatique des erreurs de syntaxe via ESLint.
2)
- next-safe-action : bibliothèque (non précisé si payant) pour les Server Actions dans Next.js (passage de la v6 à la v7).
- OpenAI API : service d'intelligence artificielle (payant à l'usage) utilisé via un script pour réécrire les fichiers de code.
- ESLint : outil de lointain/analyse statique (gratuit/open-source) utilisé pour détecter et corriger automatiquement les erreurs de type et de syntaxe (via un script de correction).
3) Astuces :
- Créer un script de refactoring automatisé qui parcourt les dossiers, applique un prompt structuré décrivant les changements de la v6 à la v7, et réécrit les fichiers.
- Utiliser un délai (timeout) entre les requêtes à l'API pour éviter les dépassements de quotas (rate limits).
- Automatiser la correction des erreurs résiduelles du compilateur ou du linter en injectant les rapports d'erreurs dans l'IA pour un nettoyage final.
4) Chiffres :
- Plus de 255 fichiers refactorisés (affirmé par l'auteur).
