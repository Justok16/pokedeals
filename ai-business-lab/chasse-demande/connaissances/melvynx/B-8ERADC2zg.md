# N'UTILISE PAS MongoDB : voici pourquoi

Vidéo : https://youtu.be/B-8ERADC2zg · durée 17:19 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo, rédigé en français selon vos critères :

---

### 1) L'idée principale

L'auteur (Melvyn) explique pourquoi il déconseille fortement l'utilisation de **MongoDB (NoSQL)** pour créer un projet ou un SaaS, tout particulièrement lorsqu'on utilise l'intelligence artificielle (comme Claude Code) pour coder. 

Son message central est que **95 % à 99 % des applications ont besoin d'une base de données relationnelle structurée (SQL / PostgreSQL)**. L'IA a besoin de règles strictes, de types rigides et de messages d'erreur immédiats pour détecter ses propres erreurs et se corriger automatiquement en boucle de rétroaction. MongoDB accepte les données incohérentes sans lever d'erreur ("échec silencieux"), ce qui crée rapidement du chaos et du code défensif ingérable.

---

### 2) Outils, sites et dépôts cités

Voici la liste exacte des outils et sites mentionnés dans la vidéo :

*   **MongoDB / MongoDB Atlas**
    *   *Statut :* Gratuit (offre de départ) / Payant (piège tarifaire à long terme selon l'auteur).
    *   *Utilité :* Base de données NoSQL orientée documents. Déconseillée par l'auteur pour la quasi-totalité des SaaS.
*   **PostgreSQL**
    *   *Statut :* Gratuit (Open Source) / Payant selon l'hébergeur.
    *   *Utilité :* Base de données relationnelle (SQL) recommandée par défaut pour 95 % des projets.
*   **Convex (`convex.dev`)**
    *   *Statut :* Gratuit (offre starter) / Payant (*détails exacts non précisés*).
    *   *Utilité :* Backend temps réel et base de données relationnelle réactive. Recommandé en alternative n°2 par l'auteur.
*   **Neon (`neon.tech`)**
    *   *Statut :* Gratuit (plan gratuit disponible) / Payant (*non précisé*).
    *   *Utilité :* Base de données PostgreSQL *serverless* économique et rapide pour agents IA.
*   **Render (`render.com`)**
    *   *Statut :* Gratuit (limité) / Payant à prix fixe selon la taille.
    *   *Utilité :* Hébergement et déploiement de bases PostgreSQL managées.
*   **DigitalOcean**
    *   *Statut :* Payant (*non précisé*).
    *   *Utilité :* Hébergeur cloud proposant des bases de données managées (PostgreSQL, Kafka, etc.).
*   **Supabase**
    *   *Statut :* Gratuit (plan gratuit disponible) / Payant (*non précisé*).
    *   *Utilité :* Backend-as-a-Service basé sur PostgreSQL.
*   **Upstash / Redis**
    *   *Statut :* Gratuit (offre starter) / Payant (*non précisé*).
    *   *Utilité :* Base de données NoSQL clé-valeur / mémoire vive pour la gestion du cache.
*   **Tinybird (`tinybird.co`)**
    *   *Statut :* Gratuit ("Try for free") / Payant (*non précisé*).
    *   *Utilité :* Base de données analytique temps réel (basée sur ClickHouse) pour ingérer de gros volumes de logs et métriques.
*   **Firebase / Firestore**
    *   *Statut :* Gratuit (starter) / Payant (*non précisé*).
    *   *Utilité :* Base NoSQL conseillée uniquement pour du prototypage rapide ou des applications mobiles *offline-first*.
*   **Cloudflare R2**
    *   *Statut :* Gratuit (volume de départ) / Payant (*non précisé*).
    *   *Utilité :* Stockage d'objets / fichiers volumineux (ex: sauvegardes d'emails HTML).
*   **TypeScript, Zod, ESLint, Prisma, Drizzle**
    *   *Statut :* Gratuits (Open Source).
    *   *Utilité :* Outils de typage, de validation de schéma et ORM pour imposer des contraintes strictes au code généré par l'IA.
*   **Claude Code / Cursor / Windsurf**
    *   *Statut :* Gratuits / Payants selon les abonnements (*non précisé*).
    *   *Utilité :* Outils et agents IA d'aide au développement informatique.
*   **NOWTS (`nowts.app`)**
    *   *Statut :* Payant (*non précisé*).
    *   *Utilité :* Starter kit / Boilerplate SaaS créé par l'auteur pour générer des applications avec l'IA.
*   **Formation SaaS Melvyn (`mlvx.sh/fs-formation-saas`)**
    *   *Statut :* Payant (*non précisé*).
    *   *Utilité :* Mini-formation pour créer son SaaS avec Claude Code sans compétences préalables en dev.
*   **Excalidraw**
    *   *Statut :* Gratuit.
    *   *Utilité :* Tableau blanc virtuel utilisé pour la présentation graphique dans la vidéo.

---

### 3) Astuces concrètes et réutilisables

1.  **Forcer l'IA à travailler avec des contraintes strictes :** Utilisez TypeScript, Zod, ESLint et PostgreSQL. Si le schéma est rigide, l'IA ne génèrera pas de champs manquants ou incohérents au fil du temps.
2.  **Exploiter les erreurs comme boucle de rétroaction (Feedback Loop) :** En SQL, une erreur de frappe ou de typage fait planter la requête immédiatement. Ce message d'erreur clair permet à Claude Code / l'IA de lire le problème et de se corriger automatiquement tout seule.
3.  **Multiplier les bases de données spécialisées plutôt que tout mettre dans une seule :**
    *   *Base principale (Core) :* PostgreSQL ou Convex (données utilisateurs, projets, facturation).
    *   *Cache :* Redis / Upstash.
    *   *Logs et analytiques haute fréquence :* Tinybird.
    *   *Fichiers lourd / HTML :* Cloudflare R2 (en ne stockant que la clé dans PostgreSQL).
4.  **Le test simple pour savoir si vous avez besoin de NoSQL :** Posez-vous la question : *"Est-ce que mon application fait plus de 1 million d'insertions par seconde ?"*. Si la réponse est NON, utilisez **PostgreSQL**.
5.  **Utiliser un Boilerplate pré-configuré pour l'IA :** Pour éviter que l'IA ne génère du code brouillon, utilisez un template contenant déjà les règles de test, de validation et de typage strict.

---

### 4) Chiffres de revenus annoncés

*   **50 000 $ / mois de MRR (Revenu Récurrent Mensuel) :** Cité par l'auteur sur ses schémas comme un objectif de SaaS parfaitement gérable avec une simple base SQL (*affirmé par l'auteur*).
*   **6 000 € à 10 000 € d'économies en temps facturable :** Témoignage client (Julien Martini) affiché sur le site `nowts.app` présenté dans la vidéo (*affirmé par l'auteur / affiché à l'écran*).
