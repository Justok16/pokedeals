# 1000h de Claude Code résumées en 1h30 (formation gratuite 2026)

Vidéo : https://youtu.be/QB2XG-v4IPk · durée 1:36:12 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, orienté pour quelqu'un qui cherche à gagner de l'argent légalement grâce à l'IA et **Claude Code**.

---

### 1) Idée principale
La vidéo présente **Claude Code**, un outil de développement ultra-puissant propulsé par l'IA (modèles de type Claude / Anthropic). L'idée centrale est qu'avec cet outil (utilisé depuis le terminal ou un IDE), même une personne non-développeuse peut **créer, modifier, et déployer des applications, des SaaS ou des bots complets**, parfois **sans écrire une seule ligne de code manuellement**, en pilotant l'IA via le langage naturel et des mécanismes d'agents, de commandes et de fichiers de configuration (`CLAUDE.md`, skills, hooks, MCP). Cela permet de multiplier sa productivité par plusieurs, de créer des applications monétisables et de lancer des projets sur le web (par exemple sur Netlify) très rapidement.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Code** (et Claude AI / Claude Chat / Claude API)
    *   *Tarif :* Payant (modèle d'abonnement mensuel ou facturation à l'usage via l'API Anthropic).
    *   *Utilité :* Outil CLI/terminal (et compatible VS Code) permettant à une IA d'agir comme un agent de développement complet (lire, écrire, modifier des fichiers, exécuter des commandes, gérer des projets entiers).
*   **Lumail.io** (mentionné comme exemple de projet créé par l'auteur)
    *   *Utilité :* Application pour envoyer des newsletters comme Mailchimp.
*   **Saveit.now** (mentionné comme exemple)
    *   *Utilité :* SaaS de signets pour sauvegarder des liens YouTube, pages web, etc. (utilise l'IA pour analyser les screenshots).
*   **Thumbfa.st** (mentionné comme exemple)
    *   *Utilité :* Application pour générer des miniatures YouTube avec l'IA.
*   **Tchao.app** (mentionné comme exemple de chatbot créé sans coder)
    *   *Utilité :* Petit chatbot conversationnel fonctionnant en temps réel.
*   **PadelTally.com** (mentionné comme exemple d'app iOS/Watch)
    *   *Utilité :* Application de score tracking pour Apple Watch.
*   **shadcn/ui** (mentionné pour le design des applications)
    *   *Utilité :* Bibliothèque de composants UI pour des interfaces modernes.
*   **Visual Studio Code (VS Code)**
    *   *Tarif :* Gratuit.
    *   *Utilité :* Éditeur de code source populaire.
*   **Node.js**
    *   *Tarif :* Gratuit.
    *   *Utilité :* Environnement d'exécution JavaScript requis pour certaines installations/dépendances.
*   **GitHub** (mentionné pour l'initialisation de dépôts via les compétences Claude)
    *   *Tarif :* Gratuit / Freemium.
    *   *Utilité :* Hébergement de code source et gestion de versions.
*   **Context7** (`context7.com`) (mentionné comme MCP)
    *   *Utilité :* Outil / serveur MCP permettant de donner à Claude l'accès à de la documentation actualisée (ex: bibliothèques React).
*   **Exa** (`exa.ai`) (mentionné comme MCP payant/outil)
    *   *Utilité :* API de recherche web ultra-optimisée pour les IA (web search).
*   **Netlify** / **Netlify Drop** (`netlify.com`)
    *   *Tarif :* Gratuit / Freemium.
    *   *Utilité :* Hébergement et déploiement ultra-rapide de sites web statiques ou d'applications en « *drag and drop* ».
*   **Dépôt/Ressource spécifique de l'auteur** : `mlv.sh/fc` (mentionné pour récupérer sa configuration Claude Code complète, ses scripts, ses agents, ses commandes, ses statuslines et ses safe scripts).
    *   *Tarif :* Non précisé dans la vidéo (probablement payant ou lié à une formation/offre de l'auteur).

---

### 3) Astuces concrètes et réutilisables

*   **Le fichier `CLAUDE.md` (Mémoire contextuelle) :** Placer un fichier `CLAUDE.md` à la racine d'un projet ou dans les sous-dossiers permet d'injecter des instructions permanentes et super-spécifiques à l'IA (commandes à lancer, règles de code, architecture, informations personnelles, ton, etc.) pour qu'elle sache toujours quoi faire sans tout réexpliquer à chaque session.
*   **Utiliser le mode « Bypass Permissions » :** Configurer les paramètres (`settings.json`) en mode `bypassPermissions` (ou définir des règles de refus `deny` pour les commandes dangereuses comme `rm -rf`) pour éviter que Claude Code ne demande une validation humaine à chaque micro-action, accélérant ainsi drastiquement l'automatisation.
*   **Les Skills (Compétences) :** Créer ou installer des « *skills* » (comme le *skill-creator* ou des kits graphiques comme *frontend-design*) pour doter l'IA de méthodologies pas-à-pas, de templates et de workflows de cuisine/code réutilisables.
*   **Les Hooks (Avant/Après actions) :** Programmer des *hooks* (par ex. `post-tool-use` avec Prettier) pour formater et corriger automatiquement le code généré par l'IA dès qu'un fichier est modifié.
*   **L'utilisation de sous-agents (Sub-agents) :** Lancer des agents spécialisés (comme un agent de recherche ou de correction de grammaire/code) en parallèle pour économiser les tokens de contexte et décharger la charge de travail de l'agent principal.
*   **L'optimisation des MCP (Model Context Protocol) :** Connecter des serveurs MCP externes (comme Context7 pour la doc technique ou Exa pour la recherche web) pour que Claude cesse d'inventer du code obsolète et récupère les données exactes et à jour.
*   **Le déploiement par glisser-déposer (Drag & Drop) :** Utiliser Netlify Drop pour mettre en ligne une application web en quelques secondes simplement en glissant le dossier de build (`dist`).

---

### 4) Chiffres de revenus annoncés (affirmés par l'auteur)

*   **Revenus générés par l'auteur avec ses applications (Lumail, etc.) :** *Non précisé*.
*   **Coûts d'utilisation de l'API Claude (exemples donnés par l'auteur) :**
    *   Modèle de tarification par défaut à l'API (Opus) : **25 $ par million de tokens** (affirmé par l'auteur).
    *   Dépense personnelle de l'auteur sur une journée en API : **171 $** (affirmé par l'auteur).
*   **Tarifs des abonnements Claude (pour situer les formules Pro/Max) :**
    *   Abonnement Pro : **17 $ ou 20 $ par mois** (selon engagement/formule mentionnés à l'écran).
    *   Abonnements Max (Max 5x / Max 20x) : **100 $ à 200 $ par mois** (affirmé par l'auteur).
    *   Estimation de consommation en équivalent API pour un gros utilisateur (comparaison de l'auteur) : de **160 $ à 3 200 $ par mois** en valeur d'usage API selon les paliers (affirmé par l'auteur).
