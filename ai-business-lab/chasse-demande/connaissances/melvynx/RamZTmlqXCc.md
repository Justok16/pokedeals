# TUTO / COURS Skills : tout comprendre sur les skills avec Claude Code

Vidéo : https://youtu.be/RamZTmlqXCc · durée 31:20 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

---

### 1. Idée principale
La vidéo explique comment structurer et automatiser des flux de travail complexes avec **Claude Code** en utilisant des **« skills »** (compétences/dossiers de compétences). Plutôt que de surcharger la mémoire du modèle avec des instructions massives, les skills permettent de découper les connaissances et les outils en petits fichiers modulaires. Claude Code charge uniquement la table des matières (`SKILL.md`) au démarrage, puis pioche dynamiquement les fichiers nécessaires (scripts, références, templates) selon la tâche demandée, économisant les tokens et améliorant considérablement la qualité et la pertinence des résultats (code, scripts, diagrammes, gestion de SaaS, etc.).

---

### 2. Outils, sites et dépôts GitHub cités

*   **Claude Code** (par Anthropic)
    *   *Tarif :* Non précisé (nécessite un abonnement/accès à l'API Anthropic).
    *   *Rôle :* Éditeur de code et agent IA en ligne de commande.
*   **Excalidraw** (`app.excalidraw.com`)
    *   *Tarif :* Gratuit.
    *   *Rôle :* Outil de dessin et de création de diagrammes (utilisé via des scripts pour générer des schémas visuels).
*   **Context7** (`context7.com`)
    *   *Tarif :* Gratuit.
    *   *Rôle :* Site de documentation à jour pour les LLM et les éditeurs de code IA (propose un skill pour supprimer le besoin de MCP).
*   **Notion**
    *   *Tarif :* Gratuit/Payant selon l'usage.
    *   *Rôle :* Outil de gestion de bases de données et de pages, utilisé pour structurer et stocker les scripts et contenus de vidéos.
*   **GitHub / Dépôt personnel de l'auteur** (`github.com/melvynx/...` / `mlv.sh/fc`)
    *   *Tarif :* Gratuit (via inscription sur `mlv.sh/fc` pour accéder à la configuration privée, aux skills et à la formation).
    *   *Rôle :* Hébergement des configurations, des skills et des tutoriels de l'auteur (Claude Code Setup, Blueprints, etc.).
*   **Lumail** (CLI)
    *   *Tarif :* Non précisé.
    *   *Rôle :* Plateforme de marketing par e-mail via CLI (gestion des abonnés, campagnes, tags, etc.).
*   **Dev-Browser** (Skill / Outil)
    *   *Tarif :* Gratuit (Open source / Script).
    *   *Rôle :* Permet à l'agent IA de contrôler le navigateur (ouvrir des pages, tweeter, automatiser des actions web).

---

### 3. Astuces concrètes et réutilisables

*   **Structurer les compétences en dossiers (`.claude/skills/`) :** Ne surchargez pas le prompt système principal avec toutes vos instructions et recettes. Créez un dossier par skill contenant un fichier principal `SKILL.md` (qui sert de table des matières) et un sous-dossier `refs/` ou `scripts/` pour les détails.
*   **Éviter l'asphyxie du contexte (Token Efficiency) :** L'agent ne charge que le `SKILL.md` au départ, puis télécharge les fichiers de référence à la demande. Cela évite le « *context overload* » (plantage du modèle par excès d'informations).
*   **Empiler les skills :** Vous pouvez combiner plusieurs skills (ex. : `Notion CLI` + `Excalidraw CLI`) pour automatiser des workflows complexes de bout en bout (comme la création automatisée d'une vidéo YouTube : recherche, script, base de données Notion, schéma Excalidraw).
*   **Rédiger des descriptions précises :** La description dans le `SKILL.md` est cruciale. C'est elle qui permet à Claude Code de comprendre *quand* et *comment* déclencher le skill de manière autonome (ex. : *« Use this skill whenever working with email marketing... »*).
*   **Utiliser les 3 types de skills principaux :**
    1.  *Compétence d'outil* (apprendre à l'IA à utiliser une API ou un outil comme Git ou Canva).
    2.  *Compétence d'apprentissage* (transmettre des connaissances pointues à l'IA : Clean Code, Sécurité, React Best Practices).
    3.  *Compétence de workflow* (guider l'IA pas à pas dans une tâche multi-étapes complexe : debug, création de features, écriture de scripts).

---

### 4. Chiffres de revenus annoncés
*   *Non précisé.* (La vidéo est axée sur l'optimisation technique et l'automatisation avec l'IA, aucun chiffre de gain financier direct n'est mentionné).
