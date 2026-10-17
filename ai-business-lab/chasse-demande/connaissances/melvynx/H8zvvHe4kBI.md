# Les PROBLEMES de SaaS qui commence à marcher | Lumail 10k$ #3

Vidéo : https://youtu.be/H8zvvHe4kBI · durée 23:37 · résumé Gemini (gemini-3.5-flash-lite) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Bien sûr, voici le résumé de la vidéo :

1) **Idée principale** : Partager les retours d'expérience sur la gestion et le développement de son SaaS (« Lumail »), ainsi que les problèmes rencontrés et les solutions apportées pour les résoudre.

2) **Outils, sites ou dépôts GitHub cités** :
   - **Ingest** : Gratuit ou payant (selon les abonnements), sert d'orchestrateur de jobs.
   - **AWS** : Payant, fournisseur de services cloud (utilisé ici pour l'hébergement et l'envoi d'e-mails).
   - **Next.js** : Gratuit, framework pour le développement web.
   - **Fable** : Non précisé.
   - **Astra** : Non précisé.
   - **Hostinger Lite** : Payant, VPS (Virtual Private Server) utilisé pour l'hébergement.
   - **Neon.tech** : Payant, base de données PostgreSQL.
   - **Stripe** : Payant, service de paiement en ligne.
   - **Hatchet** : Gratuit et open-source (contrôle d'orchestration), moteur d'orchestration pour les équipes de développement.
   - **Woodpecker** : Gratuit (ou open source), utilisé pour exécuter des tests CI (Continuous Integration).

3) **Astuces concrètes et réutilisables** :
   - Mettre en place un système de contrôle de la délivrabilité des e-mails pour éviter les bannissements de domaine.
   - Établir un « cooldown » (période de pause) dans l'envoi d'e-mails en cas de taux de rebond élevé pour préserver la réputation du domaine.
   - Remplacer des technologies gourmandes en ressources (comme Next.js) par des solutions plus légères si l'on rencontre des problèmes de performance ou de temps de build.
   - Préférer le self-hosting (hébergement sur ses propres serveurs) pour réduire les coûts de cloud et mieux contrôler l'infrastructure.
   - Utiliser des outils d'orchestration robustes comme Hatchet pour gérer les workflows complexes et éviter les pannes.

4) **Chiffres de revenus annoncés (marqués « affirmé par l'auteur »)** :
   - Aucun chiffre précis de revenus (MRR ou chiffre d'affaires) n'est annoncé dans cette vidéo. L'auteur mentionne uniquement vouloir scaler à **10 000 euros** de MRR (objectif mentionné au début de la série).
