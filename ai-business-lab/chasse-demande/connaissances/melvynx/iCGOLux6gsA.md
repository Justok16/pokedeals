# TUTO / Cours Next.js SaaS : Déployer et ajouter Stripe sur une app Next.js (5/5)

Vidéo : https://youtu.be/iCGOLux6gsA · durée 54:55 · résumé Gemini (gemini-flash-lite-latest, lot de 5) du 2026-10-12
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Apprendre à déployer une application Next.js, la monétiser en mode SaaS avec Stripe (abonnements et paiements), gérer les utilisateurs, ajouter des limitations et des webhooks, et utiliser des outils de paiement et de base de données.

2) **Outils, sites ou dépôts cités** :
- **Next.js** : Framework web (gratuit).
- **Stripe** : Solution de paiement (payant / commissions sur transactions).
- **Neon** : Base de données serverless (gratuit / payant).
- **Vercel** : Plateforme de déploiement (gratuit / payant).
- **Prisma** : ORM de base de données (gratuit).
- **GitHub** : Plateforme de code (gratuit).

3) **Astuces concrètes et réutilisables** :
- Mettre en place un lien de partage unique par utilisateur (basé sur le `userId`) pour permettre à d'autres de laisser des avis.
- Limiter le nombre de revues à 10 et conditionner l'accès au-delà à un abonnement payant via Stripe (99 € one-time).
- Utiliser Prisma pour interroger et mettre à jour les données utilisateurs et stocker les identifiants Stripe (`stripeCustomerId`).
- Configurer les webhooks Stripe pour écouter les événements de paiement (`checkout.session.completed`) et mettre à jour le plan de l'utilisateur en base de données.
- Gérer les variables d'environnement pour adapter les URLs de redirection selon l'environnement (développement, preview, production) avec les helpers Vercel (`VERCEL_ENV`).

4) **Chiffres de revenus annoncés** :
- Abonnement d'achat one-time de **99 €** (affirmé par l'auteur).

---
