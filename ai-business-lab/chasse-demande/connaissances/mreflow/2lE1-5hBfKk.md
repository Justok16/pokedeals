# Pourquoi tout le monde s'affole à propos de Fable 5 (Mythos)

Vidéo : https://youtu.be/2lE1-5hBfKk · durée 20:45 · résumé Gemini (gemini-3-flash-preview) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo pour vous aider à comprendre comment tirer parti de ce nouveau modèle :

### 1) Idée principale
La vidéo présente **Claude Fable 5**, le nouveau modèle d'Anthropic de la classe "Mythos". Il est conçu pour les tâches de codage et de réflexion ("reasoning") extrêmement complexes. S'il est capable de générer des projets entiers en une seule fois (jeux 3D, applications mobiles), il est également critiqué pour son coût élevé, sa lenteur et sa censure ("safeguards") parfois excessive.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Statut (Gratuit/Payant) | Utilité |
| :--- | :--- | :--- |
| **Claude Fable 5** | Payant (via abonnement Pro/Max/Team) | Modèle IA haut de gamme pour le codage complexe et les migrations de bases de code. |
| **Claude Mythos 5** | Payant (Accès restreint) | Version non censurée de Fable 5, réservée aux experts en cybersécurité et gouvernements. |
| **Claude Desktop App** | Inclus dans l'abonnement | Interface bureau pour utiliser les modèles Claude localement. |
| **Artificial Analysis** | Gratuit (site web) | Agrégateur de benchmarks pour comparer les performances des modèles IA. |
| **Arena Leaderboard (LMSYS)** | Gratuit (site web) | Classement basé sur des tests à l'aveugle où les utilisateurs votent pour la meilleure réponse. |
| **SWE-bench Pro** | Non précisé | Benchmark de référence pour évaluer les capacités de codage d'un agent IA. |
| **DeepSWE** | Non précisé | Nouveau benchmark de code sans "contamination" (évite que l'IA ne triche en connaissant déjà la solution). |
| **MegaBonk** | Non précisé | Jeu 3D (style Vampire Survivors) utilisé par l'auteur pour tester les capacités de création de Fable 5. |

---

### 3) Astuces concrètes et réutilisables
*   **Ciblez les tâches "One-Shot" :** Utilisez Fable 5 pour générer des prototypes complets (ex: un clone de Minecraft ou une application mobile) en une seule instruction. Il brille par sa capacité à gérer des milliers de lignes de code de manière cohérente.
*   **Réaction en temps réel :** Comme l'a fait un utilisateur (Todd Saunders), vous pouvez utiliser l'IA en arrière-plan pendant un appel client pour coder une fonctionnalité demandée en direct (15 min de travail pendant la réunion).
*   **Surveillance de la censure :** Soyez conscient que le modèle peut basculer silencieusement vers une version plus faible (Opus 4.8) s'il détecte des mots-clés liés à la biologie, la cybersécurité ou la chimie (même pour des contextes innocents comme "cancer" ou "fonctionnement du cœur").
*   **Économie de jetons :** Ne l'utilisez pas pour des tâches simples (rédaction d'e-mails, questions de base). Il est très "gourmand" en jetons. Réservez-le pour les tâches lourdes qui demandent des heures de travail humain.

---

### 4) Chiffres de revenus et performances
*   **Efficacité de migration (Stripe) :** Migration d'une base de code Ruby de **50 millions de lignes** réalisée en **1 jour** avec Fable 5, une tâche qui aurait pris **2 mois** à une équipe complète d'ingénieurs (*affirmé par Anthropic/l'auteur*).
*   **Performances au benchmark :** Score de **91/100** sur un test d'ingénierie senior, contre **63** pour Claude Opus et **62** pour GPT-4.5 (*affirmé par l'auteur via Dan Shipper*).
*   **Coût d'utilisation :** **10 $** par million de jetons en entrée et **50 $** par million en sortie (*chiffres officiels cités par l'auteur*).
*   **Chiffres de revenus :** **Non précisé**. La vidéo se concentre sur les gains de temps et de productivité technique plutôt que sur des bénéfices financiers directs.
