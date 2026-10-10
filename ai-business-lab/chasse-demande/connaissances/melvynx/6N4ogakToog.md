# Prompt Caching : Tout savoir sur l'optimisation des coûts IA via le cache

Vidéo : https://youtu.be/6N4ogakToog · durée 14:41 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
La vidéo explique le fonctionnement technique et économique du **Prompt Caching** (mise en cache des prompts) appliqué aux modèles de langage d'Anthropic (Claude, Claude Code). En évitant de re-calculer les mêmes tokens de contexte (instructions système, outils, historique) à chaque tour de conversation (*round*), le caching permet de réduire la latence et de **diminuer les coûts d'API de l'IA jusqu'à 90 %**, ce qui est essentiel pour rentabiliser le développement d'agents IA et d'applications automatisées.

---

### 2) Outils, sites et dépôts cités

*   **Claude API / Anthropic Console (`platform.claude.com`)**
    *   *Statut :* Payant (facturation à l'usage au million de tokens, tarif préférentiel sur les *cache hits*).
    *   *Rôle :* Interface API fournissant l'accès aux modèles Claude (Opus, Sonnet, Haiku) et au système de *Prompt Caching*.
*   **Claude Code**
    *   *Statut :* Non précisé (intégré à l'écosystème Anthropic/API).
    *   *Rôle :* Agent IA de code servant d'exemple pratique d'architecture mettant en cache globale les instructions système, les outils (*Tools*) et la mémoire projet.
*   **Excalidraw (`app.excalidraw.com`)**
    *   *Statut :* Gratuit.
    *   *Rôle :* Outil de tableau blanc virtuel utilisé par le créateur pour schématiser la différence entre la phase de *prefill* (mise en cache) et de *decode*.
*   **X / Twitter (`x.com`)**
    *   *Statut :* Gratuit.
    *   *Rôle :* Présentation d'annonces officielles sur le *Prompt Caching Dashboard* de Claude et d'articles explicatifs (ex. de Lance Martin).
*   **AI Blueprint (`mlv.sh/ai`)**
    *   *Statut :* Gratuit (*affirmé par l'auteur*).
    *   *Rôle :* Contenu / formation de l'auteur sur la création d'agents IA et l'architecture multi-niveaux.
*   **Jomo**
    *   *Statut :* Non précisé.
    *   *Rôle :* Application Mac de productivité/blocage de sites aperçue brièvement à l'écran.

---

### 3) Astuces concrètes et réutilisables

*   **Activer le Prompt Caching dans vos appels API :**
    Ajoutez le paramètre `"cache_control": {"type": "ephemeral"}` dans le corps JSON de la requête sur vos blocs de texte stables (instructions système, définitions d'outils/tools, contexte du projet).
*   **Éviter d'invalider ("casser") le cache :**
    *   **Ne modifiez pas la liste ou l'ordre des outils (*Tools*)** d'un tour de conversation à l'autre. Fournissez tous les outils dès le début au lieu de les ajouter/retirer dynamiquement selon le mode.
    *   **Ne changez pas de modèle** au milieu d'une session (passer de Claude Opus à Sonnet invalide le cache existant).
    *   **Conservez un System Prompt strictement identiquement formaté**.
*   **Comprendre la différence de coût (*Prefill* vs *Cache Hit*) :**
    *   La phase d'écriture initiale dans le cache (*Cache Write*) coûte un peu plus cher la première fois, mais l'utilisation ultérieure du cache (*Cache Hit*) ne coûte qu'environ 10 % du prix de base des *input tokens* (soit 90 % d'économie par tour de conversation supplémentaire).
*   **Gérer la durée de vie (TTL) :**
    Le cache reste actif par défaut pendant 5 minutes (ou 1 heure selon la configuration). Si vos requêtes sont espacées de plus d'une heure, le cache est supprimé et doit être réécrit.

---

### 4) Chiffres de revenus annoncés

*   **Affirmé par l'auteur :** Non précisé (l'auteur n'aborde pas de chiffre d'affaires ou de revenus personnels dans cette vidéo).
