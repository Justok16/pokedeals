# Sonnet est un ÉCHEC ? Nouveau modèle "Agentic" de Claude

Vidéo : https://youtu.be/2rRK7W1vYXA · durée 24:43 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
La vidéo analyse les performances, l'ergonomie et le rapport coût/efficacité de nouveaux modèles d'IA (dans un scénario prospectif/benchmark comparant notamment *Claude Sonnet 5*, *Claude Opus 4.8*, *GLM-5.2* et *GPT 5.5* via des outils de développement agentique comme Claude Code et Codex). L'auteur démontre, tests concrets de code à l'appui (génération d'un vérificateur de fuseaux horaires, simulation de collision 2D, éditeur de miniatures), que l'efficacité et la rentabilité pour un développeur ne dépendent pas uniquement du modèle le plus récent, mais de l'architecture agentique, du coût au token et de la rapidité d'exécution en un seul essai (*one-shot*).

---

### 2) Outils, sites et dépôts cités

1. **Claude / Claude Code CLI (Anthropic)**
   - **Type / Statut :** Modèles et agent CLI d'IA – **Payant** (abonnements Pro/Max/Team/Enterprise ou crédits d'usage API ; tarifs d'introduction affichés pour Sonnet 5 à 2 $/M tokens d'entrée et 10 $/M tokens de sortie, passant ensuite à 3 $/15 $).
   - **Utilité :** Assistant de programmation agentique en ligne de commande pour explorer, lire, modifier des bases de code et exécuter des tâches.

2. **Codex / Codex App & CLI (OpenAI)**
   - **Type / Statut :** Agent de développement d'OpenAI – **Payant** (via compte/crédits OpenAI).
   - **Utilité :** Génération et modification de code pilotées par les modèles de la gamme OpenAI (ex. GPT 5.5).

3. **Cursor**
   - **Type / Statut :** Éditeur de code assisté par IA – **Gratuit / Payant (Freemium)** selon l'abonnement.
   - **Utilité :** Environnement de développement intégré (IDE) exploitant des agents pour coder.

4. **Artificial Analysis (`artificialanalysis.ai`)**
   - **Type / Statut :** Site web d'analyse et d'indexation – **Gratuit** pour la consultation publique des comparatifs.
   - **Utilité :** Comparer le coût par tâche (*Cost per task*), l'intelligence et la vitesse des différents LLM et agents de code.

5. **X / Twitter (`x.com`)**
   - **Type / Statut :** Réseau social – **Gratuit / Payant** (formule Premium).
   - **Utilité :** Veille technique et discussions autour des déploiements de modèles d'IA et de workflows agentiques.

6. **Site de prompts de test (`code.melvynx.dev`)**
   - **Type / Statut :** Site web de ressources – **Gratuit**.
   - **Utilité :** Répertoire de prompts de benchmark standardisés (*Testing Prompts*) pour tester la cohérence, l'architecture et les choix techniques des modèles IA (ex. *timezone-checker*, *car-brick-wall-crash*, *draw-to-inspiration*).

7. **AI Blueprint (`mlv.sh/fa` / `codelynx.app`)**
   - **Type / Statut :** Formation en ligne / plateforme – **Payant** (avec modules de découverte / mini-formation).
   - **Utilité :** Formation pour apprendre à utiliser les agents IA (Claude Code, Codex, Cursor), configurer des compétences/MCP et accélérer sa vitesse de développement.

8. **GLM-5.2 (Zhipu AI)**
   - **Type / Statut :** Modèle open-source / API – **Accès open-source / API payante** selon l'hébergement.
   - **Utilité :** Modèle alternatif évalué pour la génération d'interfaces et de logique de code à bas coût.

---

### 3) Astuces concrètes et réutilisables

- **Éviter de tout déléguer à un seul gros modèle monolithique :** Pour réduire la consommation de tokens et les boucles d'erreurs coûteuses, il est recommandé de découper les rôles (ex. utiliser un modèle plus léger/rapide pour l'exploration et les sous-tâches, et réserver le modèle supérieur pour la planification stratégique et les décisions clés).
- **Surveiller l'impact du *tokeniseur* et de la consommation en boucle :** Un modèle théoriquement moins cher à la grille tarifaire peut revenir plus cher s'il nécessite plusieurs passes de correction ou si son encodage génère plus de tokens par requête.
- **Stopper manuellement les boucles de tests superflues de l'agent :** Lorsque l'agent IA lance de manière autonome un navigateur ou des tests lourds non nécessaires, l'interrompre immédiatement permet d'économiser du temps et des crédits d'API.
- **Utiliser des prompts de benchmark standardisés :** Avant d'intégrer un modèle dans un pipeline de production rémunéré, testez-le avec un prompt d'application complet pour évaluer sa capacité à produire une architecture propre, du code modulaire et une interface fonctionnelle sans régression.

---

### 4) Chiffres de revenus annoncés

- **200 000 $+ par an** : Rémunération potentielle pour le rôle d'*AI Engineer* affichée sur la page de présentation de la formation *AI Blueprint* (*« affirmé par l'auteur »*).
- *Autres revenus personnels / gains directs :* **Non précisé**.
