# L'erreur que les SaaS B2B font le plus...

Vidéo : https://youtu.be/qVsZ2i-ETck · durée 8:21 · résumé Gemini (gemini-flash-lite-latest, lot de 10) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) L'idée principale est d'expliquer pourquoi la plupart des SaaS adoptent un modèle « multi-tenant » (organisations avec plusieurs utilisateurs et rôles) plutôt qu'un modèle « single-tenant », et comment cela change la structure des données, la gestion des accès et la tarification.
2)
- Excalidraw : outil de dessin/schéma (gratuit/freemium) utilisé pour illustrer l'architecture des modèles SaaS.
- BulkCorrector : application SaaS de l'auteur (non précisé) fonctionnant en modèle single-tenant.
- Typefully : application SaaS (non précisé) citée comme exemple de modèle single-tenant avec limitations par compte.
- nowts.app : application/boilerplate SaaS de l'auteur (non précisé) intégrant nativement le modèle multi-tenant avec organisations, abonnements et gestion des membres.
3) Astuces :
- Structurer sa base de données et ses routes autour d'une entité « Organisation » (slug dans l'URL) plutôt que de lier directement les abonnements à un utilisateur unique, pour faciliter l'invitation de collaborateurs.
- Gérer les permissions par rôle (owner, admin, member) au niveau des actions de serveur (safe actions) pour sécuriser les ressources de l'organisation.
- Anticiper l'architecture multi-tenant dès le début du projet pour éviter une refonte technique complexe et coûteuse par la suite.
4) Chiffres :
- Coût de base estimé à 7 $ / mois par base de données standard (pour 256 Mo de RAM, 0.1 CPU, 1 Go de SSD), pouvant grimper rapidement avec plusieurs bases en single-tenant (affirmé par l'auteur).
- Exemples de tarifs de plans SaaS présentés à 19 $, 49 $, 99 $, 229 $ / mois par siège (affirmé par l'auteur).
- 522 personnes inscrites sur nowts.app au moment de la vidéo (affirmé par l'auteur).
