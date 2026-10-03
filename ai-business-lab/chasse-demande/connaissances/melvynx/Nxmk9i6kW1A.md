# Apprendre Codex en 1 HEURE | TOUT Apprendre en 2026

Vidéo : https://youtu.be/Nxmk9i6kW1A · durée 1:21:59 · résumé Gemini (gemini-3.5-flash-lite) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré et fidèle de la vidéo, orienté sur les aspects pratiques, les outils, et les déclarations de l'auteur.

---

### 1) Idée principale
L'auteur présente une masterclass sur **Codex**, un nouvel outil d'intelligence artificielle (présenté comme le successeur surpuissant de Claude Code) conçu pour automatiser les tâches de développement, de marketing et de gestion d'entreprise. Pour exploiter pleinement Codex et maximiser sa productivité (dans une optique professionnelle et potentiellement lucrative), l'auteur explique comment configurer l'interface, structurer la mémoire de l'IA (via les fichiers de règles globales et spécifiques), utiliser les extensions/plugins, et maîtriser l'architecture des contextes et des modèles.

---

### 2) Outils, sites et dépôts GitHub cités
* **Codex** (Application de chat IA / agent de code) : Payant (abonnement similaire aux plans ChatGPT/Claude Code, par exemple 20$ à 200$/mois ou facturation à l'usage API). Sert d'orchestrateur (harnais) pour exécuter des tâches, gérer des fichiers, du code, des landing pages et automatiser l'ordinateur.
* **ChatGPT / OpenAI** : Gratuit / Payant (plans Free, Go, Plus à 20$/mois, Pro à 100$/mois, et API payante à l'usage). Sert de base pour les modèles et les services conversationnels.
* **Claude Code** : Payant (mentionné comme concurrent direct dont l'auteur s'est désabonné au profit de Codex).
* **Cursor** : Payant (éditeur de code mentionné comme ancien outil de l'auteur).
* **lumail.io** : Payant (SaaS d'e-mail marketing par l'IA de l'auteur).
* **Thumbif.ai** : Payant (SaaS de génération de miniatures YouTube de l'auteur).
* **saveit.now** : Payant (Outil de gestion de favoris de l'auteur).
* **Spylanding** : Payant (Outil d'analyse des pages de vente concurrentes de l'auteur).
* **chao.app** : Payant (Application de chat IA pour communiquer avec les clients de l'auteur).
* **Portly** : Gratuit / Open source (App de l'auteur pour gérer les serveurs et applications locales).
* **Agent Burn** : Gratuit / Open source (App de l'auteur pour suivre l'utilisation des tokens d'IA).
* **AIBlueprint CLI** : Gratuit / Open source (CLI de l'auteur accessible sur `mlv.sh/fc` ou `docs.aiblueprint.dev`) pour configurer l'environnement de développement et unifier les configurations des agents (`agents unify`).

---

### 3) Astuces concrètes et réutilisables
* **Activer l'accès complet** : Pour éviter que l'IA ne pose sans cesse des questions, activer le mode « Accès complet » dans les paramètres (permet à Codex de lire, écrire, modifier des fichiers et d'exécuter des commandes).
* **Structurer la mémoire de l'IA (Le système d'entonnoir)** :
  * **Mémoire globale (`.agents/AGENTS.md`)** : Fichier de configuration caché placé globalement pour définir les règles universelles (ex. : interdire l'utilisation de `rm -rf`, lister les projets).
  * **Mémoire spécifique (`projects/specific-folder/AGENTS.md`)** : Règles propres à chaque projet pour éviter de polluer le contexte global.
  * **Mémoire gérée par l'IA (`MEMORY.md`)** : Fichier mis à jour automatiquement par l'agent pour garder l'historique et le suivi des tâches.
* **Unifier les configurations** : Utiliser la commande CLI `agents unify` pour centraliser les configurations d'agents et éviter d'éparpiller les fichiers de configuration (comme `.claude` ou `.cursor`).
* **Utiliser les chats parallèles (Side chats)** : Ouvrir des sous-conversations en parallèle pour multitâcher sans perdre le fil principal.
* **Gérer habilement le contexte et le coût (Compactage)** :
  * Relancer régulièrement les conversations pour réduire la taille du contexte et limiter les coûts en tokens.
  * Privilégier les modèles légers (ex. : `GPT-5.6 Terra Léger` ou `Sol Léger`) pour les tâches simples (tri de fichiers, audits rapides) et réserver les modèles lourds (`Astra`) aux tâches d'ingénierie complexes ou de création créative.
* **Piloter le navigateur via Codex** : Utiliser les plugins de navigation (comme le contrôle du navigateur intégré ou l'extension Chrome/Arc) pour permettre à l'IA d'interagir directement avec des pages web, faire des captures d'écran et auditer des services en ligne.

---

### 4) Chiffres de revenus annoncés (Affirmés par l'auteur)
* **Dépenses en API Codex/OpenAI** : Plus de **30 000 $** dépensés en équivalent API sur une période de 5 mois.
* **Génération de tokens** : Plus de **46 milliards de tokens** générés (puis mis à jour à **63 milliards** plus loin dans la vidéo).
* **Dépenses en abonnements** : Environ **1 000 $** payés en abonnements sur la même période.
* **Statistiques personnelles de l'auteur** :
  * Plus de **70 000 abonnés** sur YouTube.
  * Plus de **2 000 personnes formées**.
  * Plus de **4,6 millions d'e-mails envoyés** via son SaaS `lumail.io`.
* **Prix de sa formation Codex** : **99 €** (formation autonome de 10 vidéos).
