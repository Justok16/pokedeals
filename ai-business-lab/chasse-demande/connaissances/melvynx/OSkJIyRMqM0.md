# Ils ont révolutionné les Database PostgreSQL (je n'avais jamais vu ça)

Vidéo : https://youtu.be/OSkJIyRMqM0 · durée 13:27 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est de comparer les bases de données traditionnelles (coûteuses et actives 24h/24) aux bases de données serverless modernes (qui séparent calcul et stockage et se mettent en veille lorsqu'elles ne sont pas utilisées), permettant de réduire drastiquement les coûts pour les développeurs gérant de multiples projets.
2)
- Render : plateforme d'hébergement et de bases de données (payante/freemium).
- Heroku : plateforme de cloud (payante).
- Neon.tech : service de base de données PostgreSQL serverless (freemium/payant) qui sépare le calcul (compute) du stockage (storage) et met en veille le serveur en cas d'inactivité.
- Upstash : service de base de données / Redis (freemium/payant) utilisé pour le suivi des vues de blog.
3) Astuces :
- Utiliser une base de données avec séparation calcul/stockage (comme Neon) pour les projets secondaires ou SaaS à faible trafic, afin de ne payer que lorsque la base est réellement sollicitée.
- Profiter des fonctionnalités de clonage de branches (branching) sur Neon pour créer des environnements de test isolés reliés à des branches Git, facilitant le déploiement et la validation des modifications.
- Configurer les variables d'environnement de manière dynamique sur Vercel en fonction des branches de déploiement (production vs preview/test).
4) Chiffres :
- Environ 70 $ / mois pour une base de données standard (soit 7 $ par mois pour 10 bases de données) (affirmé par l'auteur).
- Tarifs Neon présentés : plan gratuit (0.5 Go de stockage, 0.1 CPU, 1 Go SSD) ou plan Launch à 19 $ / mois (10 Go de stockage, 300 heures de calcul incluses) (affirmé par l'auteur).
- Coût total estimé à 56 $ / mois pour 8 bases de données traditionnelles peu utilisées, contre une alternative beaucoup plus économique avec Neon (affirmé par l'auteur).
