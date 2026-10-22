# Coolify: L'alternative GRATUITE À Vercel (ou presque)

Vidéo : https://youtu.be/jdrhA1kq3Vw · durée 10:40 · résumé Gemini (gemini-flash-lite-latest, lot de 9) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Le vidéaste présente **Coolify**, un outil open-source et auto-hébergé permettant de déployer facilement des applications (notamment Next.js) sur son propre VPS, en tant d'alternative gratuite et puissante à des services comme Heroku, Vercel ou Netlify.

2) **Outils, sites ou dépôts GitHub cités** :
- **Coolify** (coolify.io) : Outil de déploiement et d'auto-hébergement open-source (gratuit en auto-hébergé, avec options payantes pour le cloud).
- **DigitalOcean** : Hébergeur cloud de VPS (payant).
- **Hetzner** : Hébergeur cloud (mentionné comme sponsor, payant).
- **Vercel** / **Netlify** / **Heroku** : Plateformes de déploiement cloud (mentionnées comme alternatives, payantes/freemium).
- **Ubuntu** : Système d'exploitation serveur (gratuit).
- **Docker** : Technologie de conteneurisation (utilisée en arrière-plan, gratuite).
- **GitHub** : Plateforme de gestion de code source (gratuite/payante).
- **Hostinger** : Hébergeur web (mentionné pour ses tarifs de VPS, payant).
- **AWS (Amazon Web Services)** : Fournisseur cloud (mentionné pour ses services VPS/pricing, payant).
- **Versel** (mentionné dans la vidéo, coquille pour Vercel) : Plateforme cloud.

3) **Astuces concrètes et réutilisables** :
- Acheter un VPS (par exemple sur DigitalOcean ou Hostinger) et y installer Coolify via une simple commande `curl` fournie sur le site.
- Connecter son dépôt GitHub public ou privé à Coolify pour configurer le déploiement automatique (Buildpack Nixpacks, port, etc.).
- Configurer un nom de domaine personnalisé et pointer son enregistrement DNS (type A) vers l'adresse IP du VPS pour accéder à l'application en HTTPS.
- Gérer les variables d'environnement directement depuis l'interface de Coolify.

4) **Chiffres de revenus annoncés** : Non précisé.
