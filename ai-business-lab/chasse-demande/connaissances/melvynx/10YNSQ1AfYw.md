# COMMENT React PRESERVE ton State ?

Vidéo : https://youtu.be/10YNSQ1AfYw · durée 7:20 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Comprendre comment React identifie et préserve le state d'un composant grâce à sa position dans le DOM (son adresse) et à son type, et comment forcer la réinitialisation d'un state en utilisant la prop `key`.
2) **Outils, sites ou dépôts GitHub cités :**
   - **React :** Bibliothèque JavaScript (gratuite).
   - **CodeSandbox / Environnement de test en ligne :** Utilisé pour illustrer les exemples de code (gratuit).
3) **Astuces concrètes et réutilisables :**
   - **Règle 1 (Position) :** Deux composants ayant le même type mais situés à des emplacements différents dans le DOM auront des states séparés. Si on change l'emplacement d'un composant dans l'arbre sans changer sa structure, son state est préservé.
   - **Règle 2 (Type) :** Si le type d'un composant change au même endroit dans le DOM, son state est réinitialisé.
   - Utiliser la prop `key` pour forcer React à réinitialiser le state d'un composant lorsque cette clé change (utile pour réinitialiser un formulaire ou un compteur).
4) **Chiffres de revenus annoncés :** Non précisé.
