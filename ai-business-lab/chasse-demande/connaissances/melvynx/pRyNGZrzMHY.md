# Claude Opus 5 vient de sortir et il est incroyable (je mens pas promis)

Vidéo : https://youtu.be/pRyNGZrzMHY · durée 30:14 · résumé Gemini (gemini-3.8-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur teste et compare les performances du modèle **Claude Opus 5** (utilisé via **Claude Code**) face à d'autres modèles (*Claude Fable 5*, *GPT-5.6 Sol*, *Kimi K3*) sur diverses tâches de développement web, d'animations 3D, de refonte d'interfaces utilisateur et d'optimisation de performance. L'objectif est de démontrer qu'Opus 5 surpasse les modèles précédents tout en coûtant deux fois moins cher au token, et d'analyser la gestion de ses coûts et de ses modes de raisonnement (*thinking*) pour des projets logiciels concrets.

---

### 2) Outils, sites et dépôts cités

* **Claude Code / Claude Opus 5 / Claude Fable 5 (Anthropic)** : 
  * *Statut* : Payant (via abonnement Claude / crédits API Anthropic).
  * *Utilité* : Agent IA en ligne de commande pour le code, la création d'interfaces, le débogage et l'automatisation de développement logiciel.
* **Claude Platform Docs (platform.claude.com)** :
  * *Statut* : Gratuit d'accès (tarification des API payante).
  * *Utilité* : Documentation officielle pour consulter le pricing des modèles (notamment la division par deux du prix d'Opus 5 par rapport à Fable).
* **agent-burn (`agent burn summary today`)** :
  * *Statut* : Outil CLI créé par l'auteur (statut gratuit/open-source exact : non précisé).
  * *Utilité* : Script interne permettant de suivre la consommation exacte de tokens, le coût dépensé en API et l'état des quotas journaliers/hebdomadaires.
* **DeepSWE (deepswe.datascurve.ai)** :
  * *Statut* : Gratuit d'accès.
  * *Utilité* : Benchmark technique mesurant les performances d'agents de code sur des tâches d'ingénierie logicielle longue durée.
* **Artificial Analysis (artificialanalysis.ai)** :
  * *Statut* : Gratuit d'accès (avec formule Premium payante).
  * *Utilité* : Comparateur indépendant des modèles d'IA sur l'intelligence, la vitesse, le coût par tâche et le volume de tokens générés.
* **Excalidraw (app.excalidraw.com)** :
  * *Statut* : Gratuit (avec options payantes).
  * *Utilité* : Tableau blanc en ligne utilisé dans la vidéo pour noter ses retours d'expérience à chaud.
* **Vercel (vercel.com)** :
  * *Statut* : Freemium (gratuit avec plans payants).
  * *Utilité* : Hébergement et déploiement d'applications web, utilisé pour tester l'optimisation des temps de *build*.
* **X (Twitter)** :
  * *Statut* : Gratuit (avec options payantes).
  * *Utilité* : Veille technologique, partage de benchmarks et consultation des annonces officielles.
* **AI Blueprint (codelynx.dev)** :
  * *Statut* : Payant.
  * *Utilité* : Formation en ligne vendue par l'auteur pour apprendre à utiliser les agents de code (Claude Code, Cursor, Codex).
* **Saveit.now / Thumbfa.st** :
  * *Statut* : Non précisé (projets/applications de l'auteur servant de cas d'usage réels).
  * *Utilité* : Applications web réelles servant de support de test pour la refonte de landing pages, l'ajout de filtres anti-spam et la migration API.

---

### 3) Astuces concrètes et réutilisables pour gagner de l'argent avec l'IA et Claude Code

* **Privilégier le mode de réflexion « High » plutôt que « Max » :** Le mode *Thinking Max* consomme des millions de tokens superflus, allonge les temps de réponse à plus d'une heure par tâche, augmente la facture de 15 $ à 25 $ par exécution et génère parfois des blocages/bugs. Le mode *High* produit des résultats d'excellente qualité à un coût nettement inférieur.
* **Remplacer les anciens modèles par Opus 5 dans vos workflows :** Opus 5 offre un meilleur niveau d'ingénierie et de design (génération de 3D, interfaces complexes, animations au curseur) tout en consommant moins vite les quotas hebdomadaires des abonnements.
* **Automatiser l'optimisation des performances de production :** Demander à Claude Code d'auditer les fichiers de configuration de build (comme sur Vercel/Next.js/Turbopack). L'auteur montre comment l'agent a divisé par deux le temps de build (de 6 minutes à 3 minutes) en isolant les fonctions serverless et les paquets trop lourds, ce qui réduit les coûts d'infrastructure cloud.
* **Créer des interfaces et maquettes interactives à partir d'un simple prompt visuel :** En fournissant seulement quelques images d'inspiration et une consigne textuelle minimale, Claude Code est capable de générer en une seule passe une landing page complète, responsive, avec mode sombre/clair et micro-interactions.
* **Monitorer rigoureusement sa consommation de tokens :** Mettre en place un outil de suivi de vos dépenses d'API ou de vos quotas de forfait pour éviter les coupures en plein milieu de la livraison d'un projet client.

---

### 4) Chiffres de revenus annoncés

* **Salaire / TJM d'un « AI Engineer » :** **200 000 $+** (*affirmé par l'auteur* dans sa promotion pour la formation *AI Blueprint* à 15:35).
