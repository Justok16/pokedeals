# Attention, Supabase n'est surement pas la bonne option pour toi

Vidéo : https://youtu.be/_vANs4TS-Oc · durée 14:38 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré selon tes demandes :

---

### 1) Idée principale
L'auteur explique pourquoi, contrairement aux recommandations automatiques de ChatGPT, **Convex** est un meilleur choix que **Supabase** pour créer un SaaS (notamment en termes de tarification, de facilité de scaling, de composants prêts à l'emploi et de gestion des erreurs en production), en particulier lorsqu'on développe de multiples projets avec l'aide d'agents IA (comme Claude Code).

---

### 2) Outils, sites et dépôts GitHub cités

* **Supabase**
  * *Type :* Payant (plusieurs plans, dont Supabase Pro à 25 $/mois, avec des coûts additionnels de compute, stockage et bande passante en cas de scaling).
  * *Rôle :* Outil backend et base de données relationnelle (PostgreSQL).
* **Convex**
  * *Type :* Payant (plan Convex Professional à 25 $/développeur/mois, avec facturation à l'usage sur les appels, le stockage et la bande passante).
  * *Rôle :* Backend temps réel complet (fonctions, cron, workflows, fichiers, authentification) avec des composants intégrés.
* **Excalidraw**
  * *Type :* Non précisé dans la vidéo (généralement gratuit/freemium).
  * *Rôle :* Outil de visualisation et de schéma utilisé par l'auteur pour présenter les comparaisons.
* **Claude / Claude Code**
  * *Type :* Non précisé (modèle d'abonnement ou API payante).
  * *Rôle :* Agent IA utilisé pour coder, automatiser des tâches et corriger la production à partir des logs.
* **Vercel**
  * *Type :* Payant (selon l'usage et les requêtes).
  * *Rôle :* Hébergement et gestion des applications front-end (Next.js) et des requêtes.
* **Prisma**
  * *Type :* Non précisé.
  * *Rôle :* Ancien outil ORM/base de données utilisé auparavant par l'auteur.

---

### 3) Astuces concrètes et réutilisables

* **Utiliser un assistant IA (comme Claude) avec des prompts spécialisés :** Copier les prompts d'installation fournis dans le catalogue de composants de Convex (ex. : composant Stripe ou *Rate Limiter*) pour configurer automatiquement les intégrations dans ton code sans avoir à tout coder manuellement.
* **Automatiser le débogage en production :** Créer un skill personnalisé (nommé « Runtime Incident » par l'auteur) qui se connecte aux logs réels de l'application via Convex pour permettre à l'IA de détecter et de corriger les erreurs de production instantanément, plutôt que d'essayer de deviner les bugs.
* **Éviter la duplication des coûts d'infrastructure :** Choisir un backend tout-en-un (comme Convex) plutôt que d'empiler plusieurs services payants séparés (base de données + requêtes + authentification sur Vercel et Supabase), ce qui réduit drastiquement les factures mensuelles à mesure que l'application grandit.
* **Privilégier les composants prêts à l'emploi :** Utiliser les composants officiels testés et validés par la communauté (gestion des files d'attente, rate limiting, authentification) pour gagner du temps et éviter les failles de sécurité liées au code « fait maison ».

---

### 4) Chiffres de revenus (et coûts) annoncés (affirmés par l'auteur)

* **Supabase Pro :** 25 $ / mois *(affirmé par l'auteur)*.
* **Convex Professional :** 25 $ / développeur / mois *(affirmé par l'auteur)*.
* **Coût pour un projet simple (Side project, trafic faible) :** 25 $ / mois pour Supabase contre 25 $ / mois pour Convex *(affirmé par l'auteur)*.
* **Coût pour un SaaS en phase de croissance (SaaS qui décolle) :** 95 $ / mois pour Supabase contre 25 $ / mois pour Convex *(affirmé par l'auteur)*.
* **Coût pour un SaaS à fort trafic (Scale, 100 millions d'appels, 3 dev) :** 395 $ / mois pour Supabase contre 285 $ / mois pour Convex *(affirmé par l'auteur)*.
* **Coût pour une organisation avec 7 projets à trafic faible :** 85 $ / mois pour Supabase (7 x 25 $ - 10 $ de crédits inclus) contre 25 $ / mois pour Convex *(affirmé par l'auteur)*.
