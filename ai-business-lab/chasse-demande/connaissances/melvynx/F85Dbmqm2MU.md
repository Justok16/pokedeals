# Convex : 0 €, 1 million d'appels, le backend parfait du vibecodeur

Vidéo : https://youtu.be/F85Dbmqm2MU · durée 5:27 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-27
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

### 1) Idée principale
Convex est présenté comme une alternative moderne, économique et performante à Supabase pour la gestion de bases de données, particulièrement adaptée aux développeurs utilisant l'IA et Claude Code. Il simplifie la création d'applications réactives et sécurisées en gérant l'ensemble de la pile technique (base de données, API, fichiers, temps réel) au sein d'une seule solution intégrée, éliminant ainsi le besoin de connecter et configurer de multiples outils complexes.

---

### 2) Outils, sites et dépôts GitHub cités
* **Supabase** : Alternative (payante selon l'usage), outil traditionnel de base de données que Convex remplace.
* **Convex** : Alternative (freemium), base de données backend-as-a-service tout-en-un, sécurisée et temps réel.
* **Claude Code** : Outil de développement assisté par IA.
* **convex-authz** : Librairie / skill pour l'audit de sécurité des fonctions connectées.
* **convex-billing** : Skill pour gérer les abonnements et les paiements avec Stripe.
* **convex-test** : Skill pour automatiser les tests.
* **convex-self-heal** : Skill pour transformer les erreurs de production en correctifs.
* **convex-auth** : Skill pour l'authentification (mot de passe, Google, passkey).
* **convex-cost** : Skill pour l'analyse des coûts.
* **Dépôt GitHub / Plugin officiel** : `/plugin install convex@claude-plugins-official` (permet à l'agent IA d'apprendre Convex, de lire les tables et de protéger la production).

---

### 3) Astuces concrètes et réutilisables
* **Architecture simplifiée** : Utiliser un outil tout-en-un comme Convex pour éviter d'avoir à assembler manuellement une base de données, une API, un gestionnaire de fichiers et un système temps réel.
* **Utilisation d'un agent IA** : Interagir avec Claude Code en utilisant des instructions textuelles simples axées sur les concepts de *frontend*, *base de données* et *mutation*, en laissant l'agent coder et gérer les prévisualisations.
* **Sécurité par défaut** : S'assurer que les bases de données (le « frigo ») sont fermées à l'accès direct et que chaque requête passe par la couche backend sécurisée pour valider les droits de l'utilisateur.
* **Gestion des conflits de stock** : Utiliser la synchronisation en temps réel de Convex pour éviter les soldes de stock négatifs lors d'achats simultanés par plusieurs clients.
* **Intégration de skills** : Installer des plugins ou skills spécifiques pour automatiser des tâches complexes (paiements Stripe, authentification, audit de sécurité, tests).

---

### 4) Chiffres de revenus annoncés (affirmés par l'auteur)
* **Plan Free / Starter Convex** : 0 $ / mois (inclut 1 million d'appels à la cuisine/mois, 0,5 Go de données, 1 Go de fichiers, 40 déploiements gratuits). *(Affirmé par l'auteur)*
* **Plan Pro Convex** : 25 $ par développeur et par mois (inclut 25 millions d'appels/mois, 50 Go de données). *(Affirmé par l'auteur)*
* **Exemple d'abonnement configuré par l'agent** : 5 € par mois (pour un plan « Pro » de tâches). *(Affirmé par l'auteur)*
