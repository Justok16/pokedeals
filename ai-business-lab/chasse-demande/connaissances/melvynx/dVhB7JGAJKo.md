# CODEX DEVIENT LIBRE : utilise n'importe quel modèle dans l'application

Vidéo : https://youtu.be/dVhB7JGAJKo · durée 16:33 · résumé Gemini (gemini-3.8-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur explique comment intégrer n'importe quel grand modèle d'IA (Anthropic Claude/Fable, Cursor Composer, Kimi, etc.) directement dans l'interface et le système d'orchestration de **Codex** (l'agent de développement d'OpenAI/ChatGPT) en utilisant un proxy local open source appelé **`opencodex`**. 

L'objectif est d'exploiter les fonctionnalités avancées d'interface de Codex (gestion multi-chats, sous-agents, vue diff des commits, pilotage de Chrome) tout en utilisant les modèles et abonnements d'autres fournisseurs (sans repayer au token via des API tierces), et en démontrant pourquoi il préfère cette configuration à l'environnement natif de **Claude Code**.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit ou Payant | Utilité |
| :--- | :--- | :--- |
| **Codex** (ChatGPT App / OpenAI Codex) | Payant *(inclus dans les abonnements ChatGPT Plus/Team/Pro)* | Environnement d'agent de développement autonome, exécution de terminal, gestion de code et intégration GitHub. |
| **`opencodex`** (dépôt GitHub : `miki734/opencodex` ou `github.com/opencodex/opencodex`) | Gratuit *(Open Source)* | Proxy local universel qui intercepte les requêtes de Codex pour les rediriger vers différents fournisseurs d'IA (Anthropic, Cursor, Kimi, xAI, etc.). |
| **Claude Code** (Anthropic) | Payant *(via abonnement Claude Pro/Max ou API Anthropic)* | Outil CLI/agent de dev d'Anthropic, critiqué dans la vidéo pour sa lourdeur d'interface et sa consommation de RAM. |
| **Modèles Anthropic** (Claude 3.5 Sonnet, Opus, Fable) | Payant *(abonnement Anthropic ou API)* | Modèles de raisonnement et de programmation connectés via le proxy. |
| **Cursor** (Cursor Composer, Grok, etc.) | Payant *(abonnement Cursor)* | Modèles de génération de code de Cursor routés dans Codex. |
| **Kimi** (Kimi k1.6, k2) de Moonshot AI | Gratuit / Payant selon usage *(non précisé dans la vidéo)* | Modèle IA à longue fenêtre de contexte (1M de tokens) utilisé pour exécuter des tâches d'orchestration. |
| **xAI** / **Grok** / **X Premium** | Payant *(abonnement X Premium)* | Fournisseur mentionné dans le dashboard `opencodex` pour utiliser Grok. |
| **GitHub Copilot** | Payant *(abonnement GitHub)* | Fournisseur d'IA listé dans le dashboard de configuration du proxy. |
| **Extension Chrome ChatGPT / Codex** | Gratuit *(nécessite le compte ChatGPT)* | Permet à l'agent Codex de piloter Chrome, naviguer sur le web local/externe et prendre des captures d'écran de vérification. |
| **`mlv.sh/fc`** (Formation "AI Agents" de l'auteur) | Payant | Page de vente de la formation de l'auteur pour configurer des agents IA "senior développeur" et ajouter des compétences personnalisées (ex. *Use Artifacts*). |
| **Excalidraw** (`app.excalidraw.com`) | Gratuit / Freemium | Tableau blanc en ligne utilisé par l'auteur pour schématiser l'architecture du proxy. |

---

### 3) Astuces concrètes et réutilisables

1. **Déléguer l'installation à l'agent** : Ne pas installer manuellement le proxy. Ouvrez une conversation dans Codex, fournissez l'URL GitHub d'**opencodex** et demandez-lui d'installer et configurer automatiquement le serveur proxy avec vos comptes.
2. **Optimiser la consommation des quotas grâce aux sous-agents** : Dans le tableau de bord local d'`opencodex` (`127.0.0.1:10100`), affecter les sous-agents (sub-agents) à des modèles illimités ou moins chers (comme Cursor Composer) pour préserver les quotas des modèles principaux (comme Claude 3.5 Sonnet).
3. **Nettoyer le catalogue de modèles** : Désactiver tous les modèles superflus dans l'onglet *Models* d'`opencodex` pour garder un sélecteur épuré dans l'interface Codex.
4. **Validation automatique dans le navigateur** : Connecter l'extension Chrome pour que l'agent teste visuellement les modifications front-end (CSS, responsive, emailing) et prenne des captures d'écran de preuve avant de générer le commit.
5. **Parallélisation massive (Multi-chat / Forks)** : Lancer 5 à 8 tâches simultanées dans la barre latérale de Codex ou forker des conversations pour explorer des implémentations en parallèle sans bloquer votre flux de travail.
6. **Sauvegarde et réversibilité totale** : En cas de mise à jour ou de bug de ChatGPT/Codex, utiliser les scripts de rollback générés (`restore`, `stop`, `uninstall`) pour restaurer la configuration d'origine sans risque pour le système.

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de revenus n'est mentionné** dans la vidéo : **non précisé**. 
*(L'auteur traite uniquement de l'optimisation technique, de la productivité de développement et de l'interconnexion d'outils d'IA).*
