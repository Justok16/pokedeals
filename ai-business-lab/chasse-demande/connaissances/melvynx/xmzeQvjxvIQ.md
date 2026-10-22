# Codex : de Débutant à PRO avec Les Skills (formation complète)

Vidéo : https://youtu.be/xmzeQvjxvIQ · durée 21:42 · résumé Gemini (gemini-3.6-flash) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
La vidéo est une masterclass expliquant comment maîtriser les **« Skills » (compétences)** au sein de l'environnement **Codex** (et des outils compatibles comme Claude Code ou Cursor). Les Skills permettent d'automatiser des workflows, de connecter l'IA à des outils CLI externes, et d'optimiser l'utilisation du contexte (économie de tokens) pour automatiser la création de logiciels, la gestion de campagnes ou le montage vidéo.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Codex / ChatGPT (mode Codex)** :
    *   *Statut* : Payant (Abonnement / usage API).
    *   *Rôle* : Environnement et assistant IA pour le développement logiciel.
*   **Claude Code** :
    *   *Statut* : Payant (Usage API Anthropic).
    *   *Rôle* : Agent CLI de codage compatible avec la même structure de Skills/Plugins.
*   **mlv.sh/fc (Agents Config PRO)** :
    *   *Statut* : Inscription gratuite (détails d'offres non précisés).
    *   *Rôle* : Site de l'auteur proposant sa configuration, ses agents spécialisés et plus de 20 skills préconfigurés.
*   **Zed** :
    *   *Statut* : Gratuit (Open source).
    *   *Rôle* : Éditeur de code léger utilisé dans la démonstration pour visualiser les dossiers et fichiers `.md`.
*   **dev-browser** (`SawyerHood/dev-browser` sur GitHub) :
    *   *Statut* : Gratuit (Open source).
    *   *Rôle* : Skill permettant à l'IA de contrôler un navigateur web headless, d'interagir avec les pages et de prendre des captures d'écran.
*   **Saveit.now** (`saveit.now`) :
    *   *Statut* : Non précisé.
    *   *Rôle* : Application de gestion de favoris par IA créée par l'auteur.
*   **jakub.kr/skills** :
    *   *Statut* : Gratuit (Open source).
    *   *Rôle* : Collection de skills créés par Jakub (`better-ui`, `better-typography`, etc.) pour améliorer les interfaces web.
*   **Lumail.io** (`lumail.io`) :
    *   *Statut* : Freemium (3 000 emails/mois gratuits sans carte bancaire, puis payant).
    *   *Rôle* : SaaS d'email marketing créé par l'auteur, pilotable via un skill et un CLI (`lumail CLI`).
*   **Tella** (`tella.tv`) :
    *   *Statut* : Freemium / Payant.
    *   *Rôle* : Plateforme d'enregistrement et de montage vidéo dotée d'une CLI (`tella CLI`) permettant à l'IA d'automatiser le montage vidéo.
*   **skills.sh** (`skills.sh`) :
    *   *Statut* : Gratuit (Open source).
    *   *Rôle* : Registre/Écosystème ouvert pour trouver et installer des skills d'agents IA via une ligne de commande (`npx skills add <owner/repo>`).

---

### 3) Astuces concrètes et réutilisables

1.  **Qu'est-ce qu'un Skill ?** : C'est simplement un dossier contenant un fichier `SKILL.md` (format Markdown) comprenant des métadonnées (`name`, `description`, `argument-hint`) et des instructions procédurales détaillées pour réaliser une tâche précise.
2.  **Optimisation de contexte (économie de tokens)** : Au lieu d'injecter toute la documentation ou toutes les consignes dans le prompt principal (ce qui consomme des tokens et perd l'IA), organisez vos consignes dans un dossier Skill. L'IA n'ira lire le fichier spécifique que lorsqu'elle aura besoin d'exécuter la tâche.
3.  **Ne rédigez pas les Skills à la main** : Utilisez un Skill méta comme `Skill Manager` (`$skill-manager`) ou demandez directement à l'agent IA de créer le skill pour vous à partir de vos consignes textuelles.
4.  **Différencier la portée des Skills** :
    *   *Skills globaux* (stockés dans `~/.agents/skills`) : Accessibles depuis tous vos projets.
    *   *Skills de projet* (stockés dans `.agents/skills` du projet en cours) : Dédiés uniquement à la logique de ce projet pour ne pas polluer l'espace global.
5.  **Contrôler qui invoque le Skill** :
    *   Certains skills doivent être déclenchés par l'IA elle-même (*Self-aware / Agent-invokable*).
    *   D'autres (comme la création de variantes UI lourdes) doivent être réservés à l'utilisateur humain (*User-invokable only*). Pour empêcher l'IA d'invoquer implicitement un skill, configurez l'option `allow_implicit_invocation: false` dans la configuration du skill (ex: `openai.yaml`).
6.  **Forcer la prise en compte immédiate (Mode "Orienter")** : Dans l'interface de chat Codex, utilisez la combinaison `Cmd + Entrée` ou cliquez sur « Orienter » pour injecter immédiatement une consigne dans le contexte actif sans attendre que l'IA termine sa file d'attente.

---

### 4) Chiffres de revenus annoncés

*   **Dépenses API / Recherche** : Plus de **40 000 $** dépensés par l'auteur sur Codex pour tester, optimiser et maîtriser l'outil *(affirmé par l'auteur)*.
*   **Revenus générés** : Non précisé dans la vidéo (pas de chiffre d'affaires spécifique mentionné).
