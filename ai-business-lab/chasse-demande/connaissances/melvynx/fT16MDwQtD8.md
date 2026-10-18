# Null VS Undefined - Tu les utilises MAL ?

Vidéo : https://youtu.be/fT16MDwQtD8 · durée 5:30 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-18
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Pourquoi MongoDB n'est pas la bonne solution pour la grande majorité des projets et pourquoi il faut préférer les bases de données relationnelles (SQL / PostgreSQL).
2) **Outils / sites / dépôts GitHub** :
   - MongoDB : Gratuit/Payant (base de données NoSQL).
   - PostgreSQL (Postgres) : Gratuit (base de données relationnelle SQL).
   - MySQL : Gratuit (base de données relationnelle SQL).
   - Prisma : Gratuit (ORM).
3) **Astuces concrètes et réutilisables** :
   - Ne pas utiliser MongoDB pour des structures de données complexes avec de multiples relations (comme des utilisateurs, des posts et des commentaires reliés entre eux), car MongoDB est conçu pour du non-relationnel.
   - Vérifier que la base de données choisie respecte les propriétés ACID (Atomicity, Consistency, Isolation, Durability) pour garantir la cohérence et la sécurité des données, particulièrement pour les applications avec des transactions.
   - Préférer PostgreSQL ou MySQL pour les projets nécessitant des requêtes complexes, des jointures et une intégrité stricte des données.
   - Utiliser MongoDB uniquement pour des cas spécifiques nécessitant de gérer de très grands volumes de données non structurées sans relations complexes, ou pour de la flexibilité de schéma extrême.
4) **Chiffres de revenus annoncés** : Non précisé.
