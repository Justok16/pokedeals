# JE FIX TES AGENTS IA : ma première application MacOS qui change tout

Vidéo : https://youtu.be/2M0i2BMhWMI · durée 12:02 · résumé Gemini (gemini-flash-lite-latest) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo avec toutes les informations demandées.

---

### 1. Idée principale
L'auteur présente **Portly**, une application open source et gratuite qui résout un problème majeur lors de l'utilisation d'agents IA (comme ChatGPT et Claude Code) : la gestion chaotique des processus en arrière-plan. Portly agit comme un **superviseur** centralisé pour les serveurs de développement (par exemple, Next.js), évitant la surconsommation de RAM (« processus fantômes » ou « orphelins ») et permettant de superviser, tracer et redémarrer proprement les applications. Cela permet de travailler de manière plus productive et multitâche avec les agents IA sans risquer de faire surchauffer ou planter son ordinateur.

---

### 2. Outils, sites et dépôts GitHub cités

*   **Portly**
    *   **Statut :** Gratuit et Open Source.
    *   **Rôle :** Application et gestionnaire de ports/processus qui fait office de superviseur pour les agents IA et les serveurs de développement (suivi des logs, de l'uptime, des performances, arrêt automatique en cas de dépassement de RAM).
*   **Claude Code**
    *   **Statut :** Non précisé (généralement payant/abonnement selon les offres d'Anthropic).
    *   **Rôle :** Agent IA utilisé pour le développement, capable de lancer des tâches et des processus en arrière-plan.
*   **ChatGPT**
    *   **Statut :** Version gratuite disponible / Versions payantes (ChatGPT Plus/Team).
    *   **Rôle :** Assistant IA, également gourmand en ressources lorsqu'il est utilisé en développement.
*   **Raycast Beta**
    *   **Statut :** Gratuit/Freemium (version bêta).
    *   **Rôle :** Lanceur d'applications et utilitaires pour macOS, également mentionné comme gros consommateur de ressources CPU/RAM.
*   **Helium**
    *   **Statut :** Non précisé.
    *   **Rôle :** Application mentionnée dans le suivi des processus.
*   **Site de formation No-Code / Stack de l'auteur (`mlv.sh/fn`)**
    *   **Statut :** Non précisé (mentionné pour voir la stack et les méthodes de l'auteur).
    *   **Rôle :** Lien vers la formation de l'auteur pour voir la stack et les processus utilisés pour lancer des applications rapidement.

---

### 3. Astuces concrètes et réutilisables

*   **Définir des limites de RAM par projet :** Configurer une limite personnalisée (ex. 6 Go ou 10 Go) dans Portly pour qu'un processus se redémarre automatiquement (`restart`) dès qu'il dépasse le seuil, évitant ainsi la saturation de la mémoire vive.
*   **Utiliser le CLI de Portly :** Centraliser le lancement des serveurs de développement via le CLI de Portly (`portly add-server ...`) pour que tous les agents IA passent par ce superviseur unique, garantissant une source de vérité unique (`config.json`) et un accès facile aux logs (jusqu'à 5000 lignes par fichier).
*   **Surveillance TCP automatisée :** Laisser Portly effectuer des health checks TCP toutes les 10 secondes pour s'assurer que les serveurs sont actifs et les redémarrer automatiquement en cas de crash.
*   **Migration des ports :** Utiliser l'interface de Portly pour migrer ou fermer instantanément les ports ouverts par d'autres agents en dehors de Portly.
*   **Vitesse d'exécution :** Avoir une idée, développer, utiliser l'IA pour automatiser le code et publier rapidement, sans passer trop de temps sur des configurations complexes.

---

### 4. Chiffres de revenus annoncés
*   **Revenus :** Non précisés. *(L'auteur ne donne aucun chiffre de gain financier ou de chiffre d'affaires dans cette vidéo, il se concentre uniquement sur la productivité et la gestion technique des ressources informatiques).*
