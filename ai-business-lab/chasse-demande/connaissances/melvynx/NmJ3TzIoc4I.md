# C'est la fin de Claude : pourquoi tout le monde utilise Codex ?

Vidéo : https://youtu.be/NmJ3TzIoc4I · durée 21:31 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur explique pourquoi il a abandonné l'écosystème d'Anthropic (**Claude / Claude Code / Fable 5**) au profit de celui d'OpenAI (**Codex / GPT-5.6 Sol**). Selon lui, la stratégie de communication, les restrictions de sécurité excessives (*safeguards*) et la gestion frustrante des limites de requêtes chez Anthropic pénalisent la productivité des développeurs. À l'inverse, l'environnement Codex combiné aux modèles comme GPT-5.6 Sol offre de meilleures performances de génération d'applications, un coût par tâche inférieur et une gestion plus généreuse des quotas (via des systèmes de *reset* de limites).

---

### 2) Outils, sites et dépôts cités

*   **Claude / Claude Code / Claude App (Anthropic)**
    *   **Statut :** Payant (abonnements / crédits d'API).
    *   **Utilité :** Assistant d'ingénierie et de génération de code IA.
*   **OpenAI Codex / Codex Desktop / Codex CLI**
    *   **Statut :** Payant (plans d'abonnements / crédits).
    *   **Utilité :** Environnement et agent d'exécution pour piloter le développement, exécuter des tâches et générer des applications de bout en bout.
*   **Modèles IA cités (GPT-5.6 Sol, Terra, Luna / Claude Fable 5, Mythos 5, Opus 4.8)**
    *   **Statut :** Payants via API / abonnements respectifs.
    *   **Utilité :** Modèles de langage et de raisonnement pour le codage et les benchmarks logiciels.
*   **DeepSWE (`deepswe.dataserve.ai`)**
    *   **Statut :** Gratuit (consultation publique).
    *   **Utilité :** Tableau de bord de *benchmarks* mesurant l'efficacité, le score de réussite et le coût par tâche des différents modèles de code.
*   **Excalidraw (`excalidraw.com`)**
    *   **Statut :** Gratuit / Freemium.
    *   **Utilité :** Outil de schéma et tableau blanc virtuel utilisé dans la vidéo pour illustrer le fonctionnement des filtres de sécurité.
*   **Site / Configuration Melvyn (`mlv.sh/fc`)**
    *   **Statut :** Gratuit (version de démarrage / configuration gratuite mentionnée).
    *   **Utilité :** Tutoriels de configuration du terminal (WSL, Mac, Linux) et commandes/fichiers de configuration pour agents IA (Claude Code, Codex, Cursor).

---

### 3) Astuces concrètes et réutilisables

1.  **Vérifier le coût réel par tâche (Benchmark ROI) :** Ne pas se fier uniquement au marketing ; comparer les coûts et le temps d'exécution (dans la vidéo, un modèle plus rapide et moins cher divise par 2 à 4 le coût d'une tâche complète tout en obtenant un résultat UI/UX équivalent ou supérieur).
2.  **Exploiter les resets de limites de tokens :** Sur l'interface Codex, surveiller l'onglet *Usage Remaining* pour activer les *limit resets* disponibles dès que le quota hebdomadaire s'épuise, afin de maximiser le volume de code généré sans interruption.
3.  **Forcer une période d'adaptation :** Lors d'un changement d'outil/modèle d'IA, s'imposer 1 semaine complète d'utilisation exclusive pour adapter ses prompts au style et à la logique du nouveau moteur.
4.  **Harmoniser sa configuration d'agents :** Utiliser des configurations unifiées et compatibles cross-plateformes (fichiers de configuration partagés) pour pouvoir basculer rapidement d'un agent IA à un autre sans perdre son workflow.

---

### 4) Chiffres de revenus annoncés

*   **Revenus générés avec Claude Code / IA :** *Non précisé* (aucun chiffre de gain financier direct ni de méthode de monétisation n'est présenté par l'auteur dans la vidéo).
*   *Note contextuelle :* Le profil Twitter de *Rob Hallam* affiché brièvement à l'écran indique dans sa biographie « $10,000/month SaaS » *(affirmé par l'auteur du tweet affiché)*, mais cela ne constitue pas une méthode détaillée dans la vidéo.
