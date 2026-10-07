# I Built an FP&A Analyst That Monitors My Business 24/7 With Claude

Vidéo : https://youtu.be/KFYihErgHEk · chaîne Luke Finance · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-07 · envoyée par l'utilisateur le 07/10
(connaissances générales, non vérifiées : revenus et chiffres affirmés par l'auteur)

Voici un résumé structuré de la vidéo, répondant précisément à vos attentes, sans aucune information inventée.

---

### 1) Idée principale
L'auteur montre comment créer un **analyste FP&A (Financial Planning & Analysis) automatisé et autonome** qui fonctionne 24h/24 et 7j/7 grâce à l'IA (Claude) connectée en temps réel à un CRM (HubSpot). L'objectif est d'éliminer les tâches manuelles répétitives (exportation de données, nettoyage de feuilles de calcul) et de permettre au système d'analyser en continu les risques financiers (pipeline, renouvellements, tickets de support, marges) pour générer des tableaux de bord actualisés et des recommandations exploitables sans intervention humaine constante.

---

### 2) Outils, sites et dépôts GitHub cités
*   **Claude** (Anthropic) : 
    *   *Type* : Freemium / Payant (selon l'utilisation, mention d'Opus 3 / 5).
    *   *Rôle* : Moteur d'IA utilisé pour rédiger les instructions de la compétence (skill), interpréter les données du CRM, effectuer les calculs financiers et générer le tableau de bord (artifact).
*   **HubSpot** : 
    *   *Type* : Freemium (mention d'un CRM gratuit).
    *   *Rôle* : Couche de données commerciales servant de source unique de vérité (contacts, entreprises, transactions/deals, lignes de produits, tickets de support).
*   **Fable** : 
    *   *Type* : Non précisé (utilisé dans la démonstration pour configurer les invites/prompts).
    *   *Rôle* : Interface de test/gestion des prompts et compétences d'IA.
*   **AI Finance Academy** (communauté de l'auteur) : 
    *   *Type* : Gratuit.
    *   *Rôle* : Communauté en ligne où l'auteur partage gratuitement les prompts, les jeux de données, les compétences et les instructions de configuration présentés dans la vidéo.

---

### 3) Astuces concrètes et réutilisables
*   **Connexion directe au CRM sans export manuel** : Évitez d'exporter des fichiers CSV ou Excel à la main. Connectez l'IA directement au CRM (comme HubSpot) via un connecteur avec des permissions strictement en **lecture seule** (Read-Only) pour automatiser la récupération des données en temps réel.
*   **Règles de non-négociation pour l'IA** : Définissez des règles strictes dans les instructions de l'IA (ex: ne jamais inventer de chiffres, se baser uniquement sur les données brutes du CRM, ne pas supposer qu'un champ "Amount" représente la valeur totale du contrat sans vérification).
*   **Création d'une compétence réutilisable (*Skill*)** : Plutôt que de réécrire un prompt chaque matin, transformez votre processus analytique en une compétence structurée (composée d'un nom, d'une description et d'instructions détaillées) que l'IA pourra exécuter de manière identique à chaque cycle.
*   **Automatisation par tâche planifiée (*Scheduled Task*)** : Programmez l'exécution de l'analyste virtuel à heure fixe (ex: du lundi au vendredi à 9h00) avec l'option « approuver automatiquement », couplée à une condition d'éveil de l'ordinateur, pour obtenir un suivi financier automatisé sans avoir à lancer l'analyse manuellement.
*   **Utilisation d'un artefact persistant (lien unique)** : Faites en sorte que l'IA publie son tableau de bord sous forme d'artefact web avec une URL fixe. Ainsi, chaque nouvelle exécution met à jour la page existante au lieu d'en créer une nouvelle, ce qui permet de consulter le suivi depuis un simple favori (ou canal Slack).

---

### 4) Chiffres de revenus annoncés (affirmés par l'auteur)
*   **ARR (Annual Recurring Revenue) modélisé de référence (Jour 1)** : **2 437 338 $** (provenant de 18 clients, avec un taux de marge brute par ligne de 77,8 %). *(Affirmé par l'auteur)*
*   **Churn (Chiffre d'affaires en moins / pertes réalisées constatées au cours de la démonstration)** : 
    *   Étape de détection d'un risque : **251 400 $** de renouvellements exposés. *(Affirmé par l'auteur)*
    *   Montant réalisé après quelques jours : **251 400 $** de pertes reconnues (churn effectif). *(Affirmé par l'auteur)*
*   **Variation de l'ARR lors des exécutions suivantes** : 
    *   Passage à **2 617 520 $** suite à l'ajout de nouvelles réservations (soit une augmentation de 179 520 $ ou +7,4 % en 2 jours). *(Affirmé par l'auteur)*
