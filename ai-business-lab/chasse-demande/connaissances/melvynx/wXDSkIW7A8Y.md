# Bypass Permission sur Claude : est-ce vraiment dangereux ?

Vidéo : https://youtu.be/wXDSkIW7A8Y · durée 1:07 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-14
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :** Sécuriser l'utilisation de l'assistant de code Claude en configurant les permissions et en créant des règles strictes (notamment pour interdire la suppression accidentelle de fichiers) afin d'éviter les risques liés au mode "bypass permissions".
2. **Outils, sites ou dépôts GitHub cités :**
   - **Claude** : assistant IA de programmation (freemium / payant).
   - **Trash** (Corbeille) : outil système de gestion des fichiers supprimés (gratuit / intégré aux OS).
3. **Astuces concrètes et réutilisables :**
   - Ne pas utiliser aveuglément le mode "bypass permissions" sans garde-fous pour éviter que l'IA ne modifie ou ne supprime des fichiers critiques.
   - Configurer le fichier `setting.json` (ou demander à Claude de le faire) pour ajouter une règle de refus (`deny`) sur certaines commandes destructrices (ex: `rm`, `git push --force`).
   - Forcer l'utilisation de la corbeille (`Trash`) plutôt que la suppression définitive des fichiers en cas d'intervention de l'IA.
4. **Chiffres de revenus annoncés :** Non précisé.
