# J'arrête d'utiliser mon Mac pour coder : je passe sous Linux (enfin presque)

Vidéo : https://youtu.be/4rvzsxkNw78 · durée 19:35 · résumé Gemini (gemini-3-flash-preview) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo pour exploiter l'IA et **Claude Code** (ou des outils similaires comme Cursor) de manière professionnelle et lucrative :

### 1) L'idée principale
Déléguer 100 % des tâches de développement, d'exécution d'agents IA et de tests à un **serveur distant (VPS)** ultra-performant au lieu de les faire tourner sur son propre ordinateur. Cela permet de faire travailler plusieurs agents IA en simultané sans faire ramer son Mac/PC, d'optimiser les performances de Docker (plus fluide sur Linux que sur Mac) et de garder une machine locale disponible pour d'autres tâches productives.

### 2) Outils, sites et dépôts GitHub cités

*   **Cursor** (Payant/Gratuit) : Éditeur de code basé sur VS Code, utilisé ici pour se connecter en SSH au VPS et coder directement sur le serveur avec l'aide de l'IA.
*   **Claude Code / Claude 3.5 Sonnet** (Payant via API/Abonnement) : Modèles d'IA utilisés par les agents pour coder et résoudre des issues.
*   **Netcup** (Payant) : Hébergeur de serveurs (VPS/Root-Server) recommandé par l'auteur pour son rapport performance/prix.
*   **Hetzner** (Payant) : Autre hébergeur de VPS cité.
*   **Bezel** (Gratuit/Open-source) : Outil de monitoring (bezel.molvynx.com) utilisé dans la vidéo pour surveiller l'utilisation CPU/RAM des serveurs en temps réel.
*   **Docker Engine** (Gratuit) : Utilisé sur le VPS pour faire tourner les applications et les bases de données (Redis, Postgres) avec moins de "couches" logicielles que sur Mac.
*   **Cloudflare Tunnel** (Gratuit) : Utilisé pour exposer localement des dossiers du VPS (comme des captures d'écran de tests) sur un domaine web (ex: `melvynx.dev`) afin que l'utilisateur ou l'IA puisse vérifier le rendu visuel.
*   **Agent Config PRO / mlv.sh/fc** (Payant) : Configuration spécifique créée par l'auteur pour transformer des agents IA en "développeurs seniors".
*   **CleanMyMac** (Payant) : Utilitaire Mac utilisé pour démontrer la saturation du CPU local avant la migration sur VPS.
*   **Excalidraw** (Gratuit/Payant) : Outil de schéma utilisé pour expliquer l'architecture technique.
*   **OpenClaw / Hermes Agent** : Noms donnés aux agents/systèmes internes de l'auteur (non précisé s'ils sont publics).

### 3) Astuces concrètes et réutilisables

*   **Le "Remote Development" via SSH :** Ne plus faire tourner l'IA localement. En configurant Cursor pour travailler sur un "Remote Machine", c'est le serveur qui encaisse la charge de calcul, pas votre ventilateur.
*   **Optimisation Docker :** Utiliser Linux (VPS) pour Docker. Sur Mac, Docker nécessite une machine virtuelle et un partage de fichiers qui ralentissent tout. Sur Linux, c'est natif et beaucoup plus rapide.
*   **Vérification visuelle automatisée :** Créer un dossier `skills-verify` sur le VPS. Faire en sorte que l'agent IA prenne une capture d'écran après avoir codé une interface, l'enregistre dans ce dossier, et vous donne l'URL (via Cloudflare Tunnel) pour valider le travail sans même ouvrir un navigateur local.
*   **Scalabilité horizontale :** Si vous avez besoin de plus de puissance pour faire tourner 10 agents en même temps, il suffit d'augmenter les ressources du VPS (ex: passer de 16 Go à 32 Go de RAM) plutôt que de racheter un ordinateur.

### 4) Chiffres de revenus et coûts

*   **Revenus :** Non précisé (l'auteur se concentre sur l'efficacité technique et le gain de temps).
*   **Coûts des serveurs (Affirmé par l'auteur) :**
    *   **RS 1000 G12 :** ~10,74 € / mois (4 cœurs, 8 Go RAM).
    *   **RS 2000 G12 :** ~18,00 € / mois (8 cœurs, 16 Go RAM).
    *   **RS 4000 G12 :** ~33,54 € / mois (12 cœurs, 32 Go RAM).
    *   **RS 8000 G12 :** ~59,90 € / mois (16 cœurs, 64 Go RAM).
*   **Configuration citée :** Le serveur "Steveclaw" utilise un processeur AMD EPYC Genoa avec 8 vCPU, 16 Go de RAM et 305 Go de disque.
