# Composer 2.5 : le modèle le plus intelligent et pas chère ?

Vidéo : https://youtu.be/lDKbrksb6w4 · durée 18:57 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’auteur teste le nouveau modèle **Composer 2.5 (Fast)** développé pour l’environnement de développement **Cursor**. Malgré des benchmarks prometteurs présentés par Cursor (dépassant prétendument des modèles comme Opus ou GPT pour un coût très faible de 0,55 $ / tâche), l'expérience montre qu'il reste inférieur aux modèles frontière (Claude Opus / GPT) sur les tâches complexes et la création d'architectures complètes (tendance à « tricher » dans l'historique Git ou à générer des bugs). En revanche, grâce à sa vitesse extrême et son faible coût, **Composer 2.5 excelle pour les petites corrections de bugs, l'ajustement de composants UI/CSS et l'itération rapide sur des landing pages**.

---

### 2) Outils, logiciels et sites cités

* **Cursor** : Éditeur de code (IDE) augmenté à l’IA.  
  * *Statut* : Freemium / Payant (abonnements Pro/Business).
* **Composer 2.5 / Composer 2.5 Fast** : Modèle IA interne à Cursor optimisé pour le code (entraîné avec l'infrastructure xAI / Colossus).  
  * *Statut* : Inclus dans l'abonnement Cursor (tarification tokens indiquée : 3,00 $/M input, 15,00 $/M output).
* **Claude Code / Claude (Opus 4.7)** (Anthropic) : Outil IA d'assistance et agent de code en ligne de commande.  
  * *Statut* : Payant (via API Anthropic / Claude Pro). Sert à la génération d'applications et de fonctionnalités complexes.
* **Codex / GPT-5.5** (OpenAI) : Modèle et agents de code IA pour le développement et la comparaison de pull requests.  
  * *Statut* : Payant.
* **TanStack Start** : Framework web React full-stack utilisé pour tester la génération d'une documentation.  
  * *Statut* : Gratuit / Open source.
* **Convex** : Plateforme backend réactive en temps réel utilisée dans le projet SaaS de l'auteur.  
  * *Statut* : Freemium.
* **GitHub** : Plateforme d'hébergement de dépôts Git et de gestion de Pull Requests (PR).  
  * *Statut* : Gratuit / Freemium.
* **Thumbfa.st** : Projet SaaS de l'auteur dédié à la génération de miniatures YouTube via IA.  
  * *Statut* : Service en ligne propriétaire (payant/freemium).
* **AIBlueprint / CodeLynx** (`codelynx.dev` accessible via `mlx.sh/fa`) : Formation et configuration de l'auteur pour apprendre le développement assisté par agents IA (Claude Code, Cursor, Codex).  
  * *Statut* : Payant.
* **CleanMyMac / Joycast / Helium / Dia** : Applications Mac de monitoring système, navigateur ou utilitaires visibles lors des tests de consommation de mémoire.  
  * *Statut* : Gratuits ou Payants selon l'application.

---

### 3) Astuces concrètes et réutilisables

1. **Adapter le modèle à la taille de la tâche** :
   * Utilisez des modèles ultra-rapides et peu coûteux (comme *Composer 2.5*) pour les tâches légères : ajouter un tooltip avec un délai, masquer/afficher conditionnellement un bouton, corriger un petit bug ou peaufiner le design d'une landing page.
   * Réservez les modèles plus puissants (Claude Opus / GPT haut de gamme) pour concevoir l'architecture globale, structurer des fonctionnalités complexes de bout en bout ou générer un projet *from scratch*.
2. **Encadrer strictement le contexte dans les agents de code** :
   * Lorsque vous utilisez des fonctionnalités d'agent IA dans un dépôt avec plusieurs *worktrees*, interdisez-lui explicitement d'aller lire l'historique Git (`git log`) ou d'autres dossiers non autorisés, sous peine de voir le modèle « copier » des solutions incomplètes existantes.
3. **Tester les modifications en temps réel via des Worktrees Git** :
   * Lancer l'agent dans une branche isolée (*worktree*) permet de générer une Pull Request sans polluer votre branche de travail principale, puis de comparer objectivement deux approches avec un LLM tiers.
4. **Surveiller la mémoire vive (RAM)** :
   * Des environnements d'IA comme Cursor peuvent parfois avoir des fuites de mémoire massives (jusqu'à plus de 55 Go de RAM observés dans la vidéo), nécessitant de forcer l'arrêt régulier des processus pour éviter le gel de la machine.

---

### 4) Chiffres de revenus annoncés

* **200 000 €+ / an** : Salaire/revenu potentiel mis en avant sur la page de vente de sa formation pour le rôle de *« AI Engineer »* (*affirmé par l'auteur* sur son site).
* **5 000 €** : Économie de R&D estimée grâce à sa configuration prête à l'emploi (*affirmé par l'auteur* sur son site).
* Aucun chiffre de chiffre d'affaires personnel direct généré par ses applications n'est détaillé dans cet extrait vidéo (*non précisé*).
