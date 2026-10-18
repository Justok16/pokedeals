# Pourquoi tu n'as PAS Besoin du NoSQL ?

Vidéo : https://youtu.be/FalP3P42Cek · durée 8:48 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** MongoDB ne convient pas à la plupart des projets car ils nécessitent un système relationnel, et l'auteur explique pourquoi le modèle relationnel (géré par SQL/PostgreSQL) avec ses principes ACID est souvent préférable.
2) **Outils, sites ou dépôts GitHub cités :**
   - **MongoDB :** non précisé (base de données NoSQL jugée inadaptée au relationnel).
   - **PostgreSQL / SQL :** non précisé (système de gestion de base de données relationnelle recommandé).
3) **Astuces concrètes et réutilisables :**
   - Vérifier si votre structure de données implique des relations complexes (liens entre utilisateurs, posts, commentaires) avant de choisir une base de données, pour privilégier un SGBD relationnel si c'est le cas.
   - S'appuyer sur les principes ACID (Atomicité, Consistance, Isolation, Durabilité) pour garantir l'intégrité et la cohérence des données lors des transactions.
4) **Chiffres de revenus annoncés :**
   - Non précisé.
