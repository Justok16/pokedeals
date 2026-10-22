# ARRÊTE D'UTILISER DES CONSOLE.LOG

Vidéo : https://youtu.be/bTAJAROtEdk · durée 1:00 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Remplacer les `console.log` par un logueur dédié (comme `ts-log`) pour un affichage plus propre et contrôlé selon l'environnement.
2) **Outils, sites ou dépôts GitHub cités :**
   - **ts-log** (non précisé, bibliothèque) : bibliothèque de journalisation pour afficher des logs formatés et conditionnels.
3) **Astuces concrètes et réutilisables :**
   - Stopper l'utilisation de `console.log` qui s'affiche aussi en production.
   - Utiliser `logger.debug` avec des paramètres personnalisés (`props.school.id`, etc.).
   - Configurer le niveau minimum de log (`minLevel`) via `process.env.NODE_ENV` (niveau 0 en dev, niveau 3 en production) pour masquer les logs de debug en production.
4) **Chiffres de revenus annoncés :**
   - Non précisé.
