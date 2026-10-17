# GPT SOL VS TERRA VS LUNA : lequel choisir ?

Vidéo : https://youtu.be/7hpnjicnfBo · durée 20:48 · résumé Gemini (gemini-3.8-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur analyse et teste rigoureusement les nouveaux modèles d'IA pour le code (notamment les versions fictives/anticipées *GPT-5.6 Sol, Terra, Luna* face à *Claude Fable 5* et *Claude Sonnet 5*) au sein d'agents de code tels que **Claude Code** et **Codex**. À travers des benchmarks concrets (création d'une landing page de luxe avec animations, dashboard d'analyse de séismes connecté à une API publique, simulation physique d'un crash test), il démontre que les benchmarks théoriques sont trompeurs : les modèles allégés comme Luna ou Terra déçoivent fortement en pratique. Pour rentabiliser son travail et produire des interfaces professionnelles, sa recommandation est de privilégier le modèle haut de gamme (**Sol** ou **Claude Fable**) configuré en mode de réflexion *Medium* la majorité du temps, et *High/Max* pour les tâches complexes.

---

### 2) Outils, sites et dépôts cités

1. **Claude Code**
   - **Statut** : Payant (consommation de crédits API / abonnement).
   - **Rôle** : Agent de développement IA en ligne de commande développé par Anthropic, capable de lire le terminal, planifier, écrire du code et manipuler des fichiers.
2. **Codex (Agent / Harness)**
   - **Statut** : Non précisé.
   - **Rôle** : Environnement d'exécution et d'orchestration utilisé par l'auteur pour lancer automatiquement ses suites de tests et benchmarks de code.
3. **Artificial Analysis (Coding Agent Index)**
   - **Statut** : Gratuit (plateforme web publique).
   - **Rôle** : Benchmark comparatif évaluant l'intelligence des modèles d'IA de code en fonction de leur coût API.
4. **DeepSWE (Leaderboard)**
   - **Statut** : Gratuit / non précisé.
   - **Rôle** : Classement public comparant la performance des modèles sur des tâches de génie logiciel (score SWE) par rapport au coût moyen par tâche.
5. **code.melvynx.dev** (section `Testing Prompts`)
   - **Statut** : Gratuit.
   - **Rôle** : Site web de l'auteur mettant à disposition les prompts complets, la documentation et les instructions système pour tester les assistants IA.
6. **Backgrounds Supply** (`backgrounds.supply`)
   - **Statut** : Gratuit (un pack gratuit est mentionné par l'auteur).
   - **Rôle** : Bibliothèque d'illustrations et d'arrière-plans graphiques utilisables pour habiller des sites web.
7. **API USGS Earthquake** (`earthquake.usgs.gov`)
   - **Statut** : Gratuit (API publique sans clé API requise).
   - **Rôle** : Fournit en direct les données mondiales des séismes (flux GeoJSON) pour alimenter des applications.
8. **mlv.sh/fa** (ou `mlv.sh/formation-ai`) / **AI Blueprint**
   - **Statut** : Gratuit (inscription par e-mail requise).
   - **Rôle** : Mini-formation / masterclass de l'auteur contenant sa configuration d'agents (Claude Code, Cursor, Codex, MCP, skills) pour apprendre le métier d'AI Engineer.
9. **Dokploy**
   - **Statut** : Non précisé (solution d'auto-hébergement).
   - **Rôle** : Outil de déploiement sur VPS envisagé par l'auteur pour héberger son outil de comparaison de benchmarks en ligne.

---

### 3) Astuces concrètes et réutilisables (pour monétiser ses compétences)

- **Structure de prompt pour livrer des applications vendables :**
  - Spécifier un style éditorial fort (ex. : *"editorial, luxurious, slightly surreal"*) au lieu de laisser l'IA générer des designs génériques.
  - Fournir directement les URLs des assets (images haute résolution) dans le prompt pour forcer l'agent à concevoir l'interface autour de ces visuels.
  - Fixer des exigences fonctionnelles strictes (ex. : chargement initial avec skeleton sous 5 secondes, synchronisation des données, gestion d'API publiques sans authentification).
- **Optimisation des coûts d'API et du temps de développement :**
  - **70 % à 80 % du temps** : Utiliser le meilleur modèle disponible (ici *Sol* ou *Claude Fable*) réglé avec un niveau d'effort de réflexion intermédiaire (**Thinking Medium**). Cela garantit un rendu soigné, du bon code et un temps de réponse contenu (ex. : 14 à 20 minutes par projet complet).
  - **20 % du temps** : Réserver le mode de réflexion approfondie (**Thinking High / Max**) aux composants critiques ou aux algorithmes complexes.
  - **Éviter les modèles intermédiaires dits « économiques »** (comme *Luna* ou *Terra*) pour la création d'UI : ils génèrent des hallucinations graphiques, brisent la physique/UX et font perdre du temps de correction.
- **Validation avant livraison client :**
  - Mettre en place un banc d'essai (harness) pour comparer en écran scindé (*side by side*) le code généré par différents modèles sur la même tâche avant de choisir la version finale à intégrer.

---

### 4) Chiffres de revenus annoncés

- **Salaire d'un « AI Engineer » : « 200k$+ »** (*affirmé par l'auteur* sur la page de présentation de sa formation).
- Autres chiffres financiers : Aucun autre chiffre d'affaires, tarif de prestation ou revenu spécifique n'est mentionné dans la vidéo (*non précisé*).
