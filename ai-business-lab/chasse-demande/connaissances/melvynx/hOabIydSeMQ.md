# Fable 5 est de retour (c'est vraiment le meilleur modèle ok...)

Vidéo : https://youtu.be/hOabIydSeMQ · durée 15:16 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’auteur présente le déploiement/retour du modèle expérimental très avancé **Claude Fable 5** d'Anthropic (accessible via Claude et intégrable dans des outils comme Cursor). Il montre comment il l'a utilisé pour développer en une seule passe (« one-shot ») une fonctionnalité complexe de canevas de dessin (type Excalidraw) pour son propre SaaS de création de miniatures YouTube (**Thumbfa.st**). 

Le message central pour un créateur ou développeur souhaitant monétiser avec l'IA : ces modèles de pointe permettent de créer des fonctionnalités et des produits logiciels à une vitesse décuplée (10x à 30x), mais ils consomment énormément de quota/crédits en très peu de requêtes. Il faut donc réserver ces modèles ultra-puissants uniquement aux blocages techniques ou fonctionnalités lourdes, et gérer son flux de travail avec des agents et des modèles plus économiques au quotidien.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit ou Payant | Utilité / Fonction |
| :--- | :--- | :--- |
| **Claude / Claude Code** | Payant (accès aux modèles avancés et à Fable 5 soumis aux plans Pro/Team/Enterprise et aux crédits d'utilisation *usage credits*) | Suite et interface CLI d'Anthropic pour interagir avec les modèles Claude et automatiser le codage avec des agents. |
| **Claude Fable 5** (et mention de **Mythos 5**) | Payant (inclus partiellement dans la limite hebdomadaire jusqu'à 50 %, puis facturé sur les crédits d'usage) | Modèle IA d'Anthropic à très fortes capacités de raisonnement et de codage. |
| **Cursor** | Payant (version gratuite limitée, abonnement Pro/Business requis pour les fonctionnalités complètes et modèles avancés) | Éditeur de code assisté par IA permettant d'exécuter des agents et de choisir les modèles (Composer, Fable, Opus, etc.). |
| **Composer (ex: Composer 2.5)** | Inclus dans l'abonnement Cursor | Fonctionnalité d'agent de génération et d'édition de code multi-fichiers au sein de Cursor. |
| **Codex / Codex CLI** (OpenAI) | Payant (consommation API / abonnement OpenAI) | Outil/agent d'OpenAI pour coder dans le terminal ou via une interface dédiée. |
| **Thumbfa.st** | Payant (SaaS commercial de l'auteur) | Application web permettant de concevoir et générer des miniatures YouTube par IA à partir de croquis et références. |
| **Excalidraw** | Gratuit (version en ligne open-source) | Outil de tableau blanc virtuel cité comme référence pour le canevas de dessin développé. |
| **X (anciennement Twitter)** | Gratuit (options payantes Premium) | Réseau social utilisé par l'auteur pour faire de la veille et partager ses démos. |
| **Jomo** | Non précisé dans la vidéo | Application Mac de blocage de distractions apparaissant brièvement à l'écran. |
| **AI Blueprint** (accessible via `mlv.sh/fa` ou `codelynx.dev`) | Non précisé (présente une section gratuite de tutoriels, le tarif global complet n'est pas détaillé) | Formation / espace d'apprentissage créé par l'auteur pour apprendre le rôle d'« AI Engineer » (Claude Code, Cursor, Codex, agents). |
| **GitHub Copilot** | Payant | Assistant de code IA mentionné comme alternative disponible en entreprise. |
| **Dépôts GitHub spécifiques** | Aucun dépôt GitHub public n'est partagé ou cité par un lien dans la vidéo (les dossiers montrés sont ses projets privés en local). |

---

### 3) Astuces concrètes et réutilisables

1. **Stratégie d'économie de crédits et quotas :**
   * Ne lancez jamais un modèle très lourd (comme Fable 5) pour du simple benchmark, des retouches mineures ou des tests futiles.
   * Faites 90 à 95 % du développement avec des modèles plus rapides et moins coûteux (Claude Sonnet, Opus ou Composer).
   * Réservez le modèle le plus intelligent uniquement lorsque les autres échouent ou pour générer une architecture complète complexe en une passe.
2. **Définition de règles globales pour agents (`agents.md`) :**
   * Configurez un fichier de règles (comme `agents.md` dans votre projet ou dans Cursor Rules) pour forcer l'outil à déléguer des tâches à des sous-agents avec des modèles moins coûteux en priorité (ex. Opus/Sonnet/Composer), et n'hériter de Fable que sur instruction explicite.
3. **Spécification visuelle et contextuelle (Sketch-to-Code) :**
   * Pour faire implémenter un composant d'interface rapidement, fournissez un schéma ou dessin minimaliste (boîtes, zones de texte, icônes) accompagné d'un contexte texte/audio explicatif. Le modèle comprend la disposition spatiale et implémente la structure CSS/React correspondante beaucoup plus vite qu'avec du texte seul.
4. **Post-processing prompts pour la génération d'images :**
   * Si vous utilisez des croquis comme source de génération (ex. miniatures), ajoutez un prompt système de post-traitement pour ordonner à l'IA d'ignorer les formes brutes (cercles de repère, flèches) et de les remplacer par les vrais assets de style final.

---

### 4) Chiffres de revenus annoncés

* **10k MRR (Revenu Mensuel Récurrent) :** Affiché sur la biographie de son profil X pour ses projets SaaS (`thumbfa.st`, `theaffiches.fr`, `kasset.now`) – *affirmé par l'auteur*.
* **200 000 $+ :** Rémunération annuelle potentielle annoncée sur la page de présentation d'« AI Engineer » – *affirmé par l'auteur*.
* *Note :* Aucun autre chiffre de gain personnel direct ou chiffre d'affaires n'est mentionné oralement dans le reste de la vidéo.
