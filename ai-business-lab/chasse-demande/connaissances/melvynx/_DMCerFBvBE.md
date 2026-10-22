# La boilerplate la plus abouttie en NextJS....

Vidéo : https://youtu.be/_DMCerFBvBE · durée 8:00 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de raconter comment l'auteur a utilisé l'IA (notamment un script avec GPT-4o) pour automatiser la migration de plus de 255 fichiers d'une bibliothèque vers une nouvelle version majeure (v6 vers v7), économisant ainsi un travail manuel fastidieux.
2)
- next-safe-action : bibliothèque (non précisé si payant) de gestion d'actions de serveur dans Next.js, dont la v7 introduit des changements majeurs.
- OpenAI API / GPT-4o : outil d'intelligence artificielle (payant à l'usage) utilisé via un script de refactoring pour réécrire automatiquement les fichiers de code.
- nowts : application/boilerplate (non précisé) développé par l'auteur.
3) Astuces :
- Écrire un script Node.js automatisé qui lit les fichiers de code, envoie un prompt précis à l'IA (ex. : instructions de refactoring de v6 à v7 avec Zod et server actions), et réécrit les fichiers corrigés.
- Ajouter un délai (timeout/pause) dans les boucles de traitement par IA pour éviter les problèmes de limites de taux (rate limits).
- Traiter les erreurs de migration par vagues en s'appuyant sur les retours du linter (ESLint) pour corriger les derniers détails si nécessaire.
4) Chiffres :
- Plus de 255 fichiers migrés automatiquement (affirmé par l'auteur).
