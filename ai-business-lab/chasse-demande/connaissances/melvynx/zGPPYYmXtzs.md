# Mon application CHEATÉE pour tester les modèles

Vidéo : https://youtu.be/zGPPYYmXtzs · durée 12:09 · résumé Gemini (gemini-3.7-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
La vidéo présente un outil et dépôt open-source créé par l'auteur (**Benchmarks** / **Benchmark Compare**) qui automatise l'exécution, le suivi et la comparaison visuelle d'applications web générées par différents modèles d'IA (Claude, GPT, Kimi, etc.) via des agents de code comme Codex ou Claude Code. Cela permet d'évaluer précisément la qualité visuelle, la logique, le temps d'exécution, la consommation de tokens et le coût financier de chaque modèle.

---

### 2) Outils, sites et dépôts cités

* **GitHub Repository : `melvynx/benchmarks`**
  * **Statut :** Gratuit / Open-source.
  * **Utilité :** Contient l'infrastructure de benchmark, la suite de prompts de test, les scripts de lancement automatique (`run-benchmark`) et l'application web de comparaison (`benchmark-compare`).
* **Codex (CLI / Assistant)**
  * **Statut :** Non précisé dans la vidéo (généralement payant / consommation API).
  * **Utilité :** Environnement d'agent de développement utilisé par l'auteur pour orchestrer, exécuter et superviser les sessions de test en arrière-plan.
* **Claude Code (CLI)**
  * **Statut :** Non précisé dans la vidéo (accès via API Anthropic payante).
  * **Utilité :** Agent en ligne de commande développé par Anthropic permettant d'éditer des fichiers et exécuter des tâches de programmation de manière autonome.
* **Modèles d'IA mentionnés (pour les tests) :**
  * *Claude (Sonnet 3.5, 3.7, Opus 4, 4.5, 4.7, Fable 5)*
  * *GPT (5.5, 5.6 Sol/Terra/Luna, Codex)*
  * *Kimi k3*
  * **Statut :** Payants à l'usage (APIs des fournisseurs respectifs).

---

### 3) Astuces concrètes et réutilisables

* **Automatisation de bout en bout :** Configurer un agent IA (ex: Codex ou Claude Code) pour exécuter des scripts de benchmark en tâche de fond, monitorer l'avancement et analyser les logs d'erreurs sans intervention manuelle.
* **Analyse multicritère :** Ne pas se fier uniquement au rendu final, mais analyser :
  * Le **temps d'exécution** et la vitesse.
  * Le **coût API réel** et le volume de tokens consommés (cache read/write, input, output, tokens de réflexion/reasoning).
  * La répartition de l'activité du modèle (*Transcript Activity* : contexte, planification, implémentation, vérification).
* **Conception de prompts de test équilibrés :** 
  * Éviter les prompts trop directifs (qui rendent la réponse prédictive et identique d'un modèle à l'autre).
  * Éviter les prompts trop vagues (qui génèrent des incohérences).
  * Trouver l'équilibre pour tester la capacité d'initiative, de design et de rigueur algorithmique de chaque modèle.
* **Comparaison visuelle synchronisée :** Utiliser des vues en grille ou en colonnes avec option d'*auto-scroll* synchronisé pour comparer côte à côte les interfaces créées par les différentes IA.

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de revenus n'est mentionné** dans la vidéo (marqué : *affirmé par l'auteur / non précisé*).
