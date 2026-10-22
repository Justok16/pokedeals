# TUTO : Upload GRATUITEMENT des images sur Cloudflare R2 avec Next.js

Vidéo : https://youtu.be/uSCmPzLWIm8 · durée 20:27 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Ce tutoriel compare les coûts de stockage et de transfert de données (Egress) pour l'upload d'images entre **Amazon S3**, **Cloudflare R2** et **UploadThing**, démontrant que Cloudflare R2 est nettement plus économique en raison de l'absence de frais d'egress, puis montre comment intégrer Cloudflare R2 dans une application Next.js.

2) **Outils, sites et dépôts GitHub cités** :
- **Amazon S3** : Service de stockage cloud d'AWS. (Payant / Tarification à l'usage).
- **Cloudflare R2** : Service de stockage cloud de Cloudflare sans frais d'egress. (Payant / Économique).
- **UploadThing** : Solution SaaS de gestion d'uploads de fichiers pour les développeurs (le "SaaS de Theo"). (Payant / Forfaitaire).
- **CCSeva** : Application de suivi en temps réel de la consommation de l'API Claude (mentionnée au début de la vidéo). (Gratuit / Open source).
- **Next.js** : Framework React utilisé pour l'application de démonstration. (Gratuit).
- **Origin UI** : Bibliothèque de composants UI (utilisée pour récupérer un composant d'upload d'avatar). (Gratuit).
- **Prisma** : ORM pour la base de données. (Gratuit).
- **AWS SDK pour JavaScript (@aws-sdk/client-s3)** : Bibliothèque officielle pour interagir avec S3/R2. (Gratuit).

3) **Astuces concrètes et réutilisables** :
- Pour un scénario de 10 000 fichiers uploadés par mois (1 Mo chacun) et 1 million de lectures par mois, privilégier Cloudflare R2 pour éviter les coûts exorbitants de sortie de données (egress) facturés par AWS S3.
- Configurer les variables d'environnement pour AWS S3/R2 (`AWS_S3_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_API_URL`, etc.).
- Utiliser un client S3 compatible avec une URL personnalisée (`endpoint`) pour pointer directement vers le stockage R2 de Cloudflare.
- Générer des noms de fichiers uniques lors de l'upload pour éviter les conflits (utilisation d'un préfixe, du timestamp et d'une extension).
- Configurer le domaine public de développement ou un domaine personnalisé sur Cloudflare R2 pour servir les fichiers directement via une URL propre.

4) **Chiffres de revenus annoncés** :
- **Affirmé par l'auteur** : Aucun chiffre de revenus n'est annoncé dans cette vidéo (l'auteur présente uniquement des coûts et estimations de dépenses pour l'hébergement, par exemple un total estimé sur 12 mois de 1 100 $ pour Amazon S3 contre 16 $ pour Cloudflare R2).

---
