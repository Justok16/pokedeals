# Paperclip : faire travailler plusieurs agents IA comme une entreprise

Vidéo : https://youtu.be/7RVf25Rg0Mc · envoyée par l'utilisateur le 28/09/2026 · résumé Gemini (gemini-3.6-flash) du 2026-09-28
(chiffres de revenus : affirmés par les auteurs, non vérifiés)

### 1) Idée principale
La vidéo présente **Paperclip**, un « meta-harness » (orchestrateur d'orchestrateurs d'IA) conçu pour structurer et faire collaborer plusieurs agents IA (Claude Code, OpenAI Codex, Hermes, modèles locaux, etc.) sous la forme d'une **entreprise virtuelle / département IT complet**. L'auteur montre comment installer Paperclip, créer une hiérarchie d'agents IA spécialisés, leur attribuer des rôles précisiés (CEO, CTO, Ingénieur Réseau, Ingénieur Sécurité), organiser des réunions quotidiennes (*standups*) autonomes et leur faire résoudre un problème complexe d'infrastructure réseau réelle.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Paperclip** (`paperclipai`)
    *   **Statut :** Gratuit (open-source en auto-hébergement local) / Version Cloud en liste d'attente (*waitlist*, prix non précisé).
    *   **À quoi il sert :** Meta-harness d'orchestration qui transforme les agents IA en « employés ». Il gère la hiérarchie d'entreprise (*organigramme*), la création de projets/tâches, l'attribution de compétences (*skills*), les secrets/clés API, les réunions récurrentes (*routines*) et le suivi des décisions.
*   **Dépôt GitHub / Scripts d'installation Paperclip** (`raw.githubusercontent.com/paperclipai/...`)
    *   **Statut :** Gratuit.
    *   **À quoi il sert :** Permet de télécharger et d'installer Paperclip sur Linux/Mac/WSL2 via une commande `curl` et un script bash (`install.sh`).
*   **Claude Code** (Anthropic)
    *   **Statut :** Payant (nécessite un abonnement Anthropic Pro/Max/Team/Enterprise ou une clé API facturée à l'usage).
    *   **À quoi il sert :** Agent CLI/Harness développé par Anthropic. Dans la vidéo, il est utilisé comme moteur principal pour l'agent CEO (« Dumbledore ») pour analyser, planifier et déléguer le travail.
*   **OpenAI Codex**
    *   **Statut :** Payant (accès API OpenAI / facturation à l'usage).
    *   **À quoi il sert :** Harness CLI d'OpenAI utilisé pour les agents de révision de code/sécurité (ex: « Mad-Eye Moody ») et d'outillage (ex: « Arthur Weasley »).
*   **Hermes Gateway / Hermes Agent** (Nous Research)
    *   **Statut :** Gratuit / Open-source (exécuté localement sur VM).
    *   **À quoi il sert :** Agent autonomisé et pré-entraîné doté d'outils système/réseau. Utilisé dans la vidéo pour les rôles de CTO (« Ron »), d'ingénieur réseau (« Fred ») et d'ingénieur stockage (« George »).
*   **Flare** (`flare.io`) — *Sponsor de la vidéo*
    *   **Statut :** Payant (essai gratuit / *free trial* disponible via le lien de l'auteur).
    *   **À quoi il sert :** Plateforme de Threat Intelligence axée sur l'identité. Elle surveille les fuites d'identifiants, de cookies de session et de données sensibles sur le Dark Web et Telegram, et automatise la neutralisation des accès (ex: via Microsoft Entra ID).
*   **Pi / Pi harness**
    *   **Statut :** Non précisé (gratuit/open-source en général).
    *   **À quoi il sert :** Harness d'agent IA léger optimisé pour faire tourner des modèles d'IA en local (ex: modèles Qwen exécutés sur Mac Studio ou Raspberry Pi pour le scanner réseau et le helpdesk).
*   **Proxmox**
    *   **Statut :** Gratuit / Open-source.
    *   **À quoi il sert :** Solution de virtualisation (hyperviseur) utilisée par l'auteur pour héberger les machines virtuelles (VM) exécutant Paperclip et les différents agents.
*   **Ubuntu**
    *   **Statut :** Gratuit / Open-source.
    *   **À quoi il sert :** Système d'exploitation Linux sur la VM servant d'environnement d'exécution principal pour Paperclip et Claude Code.
*   **Nginx Proxy Manager**
    *   **Statut :** Gratuit / Open-source.
    *   **À quoi il sert :** Outil d'administration de proxy inverse utilisé pour gérer les domaines locaux/port 3100 de Paperclip.
*   **Autres harnesses cités à l'écran (compatibles Paperclip) :**
    *   **Cursor Cloud / Cursor** : Statut non précisé (freemium/payant).
    *   **Gemini CLI** : Statut non précisé.
    *   **Grok Build** : Statut non précisé.
    *   **Kimi Code** : Statut non précisé.
    *   **OpenCode** : Statut non précisé.
*   **Mentionnés brièvement en introduction :**
    *   **OpenClaw** : Statut non précisé. Agent/harness IA.
    *   **Buzz** : Statut non précisé. Tentative précédente d'orchestration d'agents.

---

### 3) Astuces concrètes et réutilisables

1.  **Orchestration multi-harness (« Harness-Maxing ») :** Ne vous limitez pas à un seul modèle ou outil d'agent IA. Associez le meilleur outil à la tâche appropriée : un agent puissant comme Claude Code pour le rôle de direction/CEO, un modèle spécialisé en code comme Codex pour la révision de sécurité, et des modèles locaux légers (via Pi/Ollama/Qwen) pour les tâches répétitives ou le balayage réseau basique.
2.  **Organigramme d'entreprise pour agents IA :** Structurer vos agents IA avec des rôles précis (CEO, CTO, Ingénieur Réseau) et des liens de subordination (*« Reports to »*). Cela permet aux agents d'escalader leurs problèmes à leurs supérieurs virtuels avant de solliciter l'utilisateur humain.
3.  **Communication par tâches (*Task-driven*) plutôt que par chat général :** Évitez les groupes de discussion où les agents parlent sans but. Dans Paperclip, les agents interagissent exclusivement via le système de tickets/tâches en s'assignant des sous-tâches et en commentant le travail réalisé.
4.  **Réunions quotidiennes autonomes (*Daily Standups via Routines*) :** Programmez des tâches récurrentes automatiques. Chaque jour à heure fixe, les agents s'interrogent entre eux sur l'avancement des projets, vérifient la cohérence des sauvegardes et rédigent un compte-rendu synthétique (*digest*) pour l'administrateur humain.
5.  **Positionnement humain en « Conseil d'administration » (*Human-in-the-loop*) :** Laissez les agents travailler en autonomie complète sur l'exécution, mais conservez le contrôle sur les décisions critiques : approbation des embauches de nouveaux agents, arbitrage de choix techniques majeurs (*Decisions*), et validation des changements sur les infrastructures réelles.
6.  **Gestion centralisée et cloisonnée des secrets :** Stockez vos clés API sensibles (ex: clé API Flare) dans la section *Secrets* de Paperclip et attribuez les accès uniquement aux agents qui en ont explicitement besoin pour accomplir leurs fonctions.
7.  **Mesure de sécurité / Contrôle d'exécution :**
    *   Assignez des rôles d'agents en lecture seule (*Read-only*) pour les scanners et les tâches de diagnostic afin d'éviter qu'ils ne modifient l'infrastructure à votre insu.
    *   Incorporez un agent « Security Reviewer » (ex: *Mad-Eye Moody*) chargé de relire et d'approuver tout code ou script d'automatisation avant déploiement.
8.  **Portabilité d'entreprise (*Export/Import*) :** Exportez l'ensemble de la structure de votre équipe d'agents (configurations, compétences, routines, règles) sous forme de fichier package/repository pour la dupliquer facilement sur un autre serveur.

---

### 4) Chiffres de revenus annoncés

*   **Revenus personnels / directs de l'auteur :** Aucun chiffre de revenus personnels ou de gains financiers issus de l'utilisation de ces outils n'est annoncé dans la vidéo (*non précisé / non applicable*).
*   **Informations annexes citées dans la vidéo :**
    *   L'interface de Paperclip affiche un budget interne de `$0.00 Month Spend` / `Unlimited budget` *(affirmé par l'auteur via l'interface du logiciel)*.
    *   Pendant la séquence partenaire Flare, l'auteur mentionne que des fichiers de données/identifiants volés se revendent environ **10 $ par log** sur Telegram et sur les marchés noirs russes *(affirmé par l'auteur)*.
