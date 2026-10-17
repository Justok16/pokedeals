# MA NOUVELLE APP macOS pour tracker ton usage IA (Agent Burn)

Vidéo : https://youtu.be/qQxHp2pe8YE · durée 15:41 · résumé Gemini (gemini-3.5-flash-lite) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo, structuré selon tes demandes :

### 1) Idée principale
L'auteur présente une application gratuite, **Agent Burn**, conçue pour suivre l'utilisation et les coûts (en dollars, tokens et limites de quotas) des agents d'IA utilisés dans les outils de développement (comme Codex, Claude Code, Cursor, etc.). L'objectif est d'aider les développeurs à optimiser leur consommation et à éviter de dépasser leurs limites, tout en démontrant l'utilisation conjointe de plusieurs modèles d'IA pour réduire les coûts.

---

### 2) Outils, sites et dépôts GitHub cités

* **Portly** (`portly.melvynx.dev`)
  * **Prix :** Gratuit (mentionné par l'auteur).
  * **Rôle :** App de tracking d'usage (existante également en version Linux) qui a précédé Agent Burn.

* **Agent Burn** (`agent-burn.melvynx.dev` / dépôt GitHub `Melvynx/agent-burn`)
  * **Prix :** Gratuit, open source (mentionné par l'auteur).
  * **Rôle :** Application et CLI pour suivre les quotas, dépenses en dollars, et l'usage des tokens de différents agents et modèles d'IA (Codex, Claude Code, Cursor, etc.), avec des graphiques de prévision et un système de cache pour ne pas perdre les données.

* **Codex**
  * **Rôle :** Outil ou fournisseur d'agent d'IA (mentionné pour le tracking).

* **Claude Code**
  * **Rôle :** Outil de développement d'IA (les données d'usage sont analysées dans Agent Burn).

* **Cursor** (et **Cursor Ultra**)
  * **Prix :** Abonnement payant (mentionné par l'auteur via des crédits promotionnels, par exemple 200 $/mois).
  * **Rôle :** Éditeur de code assisté par IA.

* **D’autres outils/modèles cités (dans les menus ou graphiques de DeepSWE) :**
  * **Droid, Gemini, Kimi, OpenClaw, Qwen, Pi, Fable, Astra, Terra, Grok (4.6 High, etc.)**
  * **Rôle :** Modèles ou agents d'IA utilisés pour le codage, la planification ou la relecture de code.

* **Site de formation / skills :** `mlv.sh/fc` (Agents Config PRO)
  * **Prix :** Configuration gratuite (mentionnée à l'écran).
  * **Rôle :** Regroupe des skills validés pour transformer les agents IA en « senior développeur ».

---

### 3) Astuces concrètes et réutilisables

* **Suivi des quotas en temps réel :** Utiliser des outils de tracking (comme Agent Burn) pour surveiller sa ligne de consommation par rapport aux prévisions (forecast) et éviter d'épuiser ses limites trop rapidement.
* **Mise en cache des données :** Sauvegarder localement les résumés quotidiens d’usage pour éviter de recharger de lourds volumes de données à chaque exécution dans le terminal.
* **Combinaison de modèles pour réduire les coûts :**
  * Utiliser un modèle intelligent mais plus lourd (ex. **Astra**) uniquement pour la planification ou la supervision/relecture de code (via des prompts de type « superviseur » ou avec l'option *Use Goal*).
  * Utiliser un modèle plus économique (ex. **Terra** ou **Grok**) pour l'implémentation brute des fonctionnalités.
  * *Règle générale de l'auteur :* Ne pas utiliser systématiquement les modèles les plus chers pour toutes les tâches, car beaucoup de tâches simples n'en ont pas besoin.

---

### 4) Chiffres de revenus annoncés (affirmés par l'auteur)

* *Note :* Aucun **revenu personnel** n'est annoncé dans cette vidéo (il est question de coûts/dépenses en tokens et en crédits d'abonnements, et non de gains). Les chiffres mentionnés correspondent à des dépenses ou à des valeurs d'équivalence API :
  * **Dépenses/crédits d'utilisation d'IA (affirmés par l'auteur) :**
    * Dépenses globales affichées sur le dashboard de l'auteur : ~30 758 $ / ~15 092 $ / ~6 327 $ (selon les vues).
    * Crédits promotionnels Cursor : 5 000 $ (abonnement à 200 $/mois).
    * Crédit d'abonnement Codex Pro : 200 $/mois.
