# Hermes Agent : le meilleur remplaçant à OpenClaw (c'est beaucoup mieux)

Vidéo : https://youtu.be/XQ8hKjjYsJc · durée 24:08 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé détaillé de la vidéo :

---

### 1) Idée principale

La vidéo compare deux agents IA autonomes open source : **OpenClaw** et **Hermes Agent** (de *Nous Research*). L'auteur explique pourquoi il a abandonné OpenClaw (instable, lent, bloqué par les restrictions/bannissements de Claude et posant des problèmes avec Codex) au profit de **Hermes Agent**. 

Hermes Agent est présenté comme une solution nettement plus puissante et fiable pour automatiser des tâches complexes (codage, gestion d'e-mails, exécution de scripts Python, navigation web, délégation à **Claude Code**). Grâce à son système de mémoire persistante, sa capacité à créer ses propres compétences (*skills*) et son tableau de bord visuel (*Hermes HUD*), Hermes s'impose comme une infrastructure idéale pour automatiser des flux de travail de développement logiciel et de gestion de projets.

---

### 2) Outils, sites et dépôts GitHub cités

1. **Hermes Agent** (*Nous Research* / GitHub / `agent.nousresearch.com`)
   * **Statut :** Gratuit / Open source.
   * **Rôle :** Agent IA autonome auto-améliorant écrit en Python. Il exécute des scripts, retient le contexte d'une session à l'autre et gère des tâches complexes de manière proactive.
2. **Nous Research / Nous Portal** (`nousresearch.com` / `portal.nousresearch.com`)
   * **Statut :** Gratuit (laboratoire open source) avec des fonctionnalités/API potentiellement payantes.
   * **Rôle :** Entreprise/laboratoire de recherche qui développe des modèles open source et héberge l'infrastructure d'Hermes.
3. **OpenClaw**
   * **Statut :** Gratuit / Open source.
   * **Rôle :** Ancien framework d'agent IA concurrençant Hermes, jugé lent, instable et difficile à maintenir avec Codex/Claude.
4. **Hermes HUD** (*joeynychmes-hud* / GitHub / `hermes-hud`)
   * **Statut :** Gratuit / Open source.
   * **Rôle :** Interface web / tableau de bord de suivi pour Hermes Agent. Il permet de visualiser la mémoire, les compétences, les projets actifs, les tâches planifiées (cron) et la consommation de jetons/coûts.
5. **Claude Code** (outil Anthropic / skill `claude-code`)
   * **Statut :** Payant (via clé API Anthropic ou abonnement).
   * **Rôle :** Outil de développement en ligne de commande délégué par Hermes Agent pour refactoriser du code, créer des commits et ouvrir automatiquement des Pull Requests (PR) sur GitHub.
6. **ChatGPT / OpenAI Codex / GPT-5.3-Codex-Spark** (`chatgpt.com/codex`)
   * **Statut :** Payant (plan Pro / abonnement à ~100 $/mois ou consommation d'API).
   * **Rôle :** Moteur LLM sous-jacent utilisé par Hermes pour exécuter du code Python et effectuer des raisonnements rapides.
7. **Telegram**
   * **Statut :** Gratuit.
   * **Rôle :** Interface de messagerie principale (passerelle) utilisée par l'auteur pour envoyer ses instructions directement à Hermes Agent sous forme de bot.
8. **Excalidraw** (`app.excalidraw.com`)
   * **Statut :** Gratuit (version de base).
   * **Rôle :** Application de dessin schématique. Hermes peut générer et lire des fichiers Excalidraw pour créer des schémas d'architecture ou de comparaison.
9. **GitHub**
   * **Statut :** Gratuit (compte standard).
   * **Rôle :** Plateforme de gestion de code source où l'agent inspecte les dépôts, gère les commits et crée des Pull Requests.
10. **Agent Skills** (`agentskills.io` / *Skills Hub*)
    * **Statut :** Gratuit / Open source.
    * **Rôle :** Registre et standard ouvert regroupant plus de 644 compétences réutilisables et téléchargeables par l'agent IA.
11. **Himalaya**
    * **Statut :** Gratuit / Open source.
    * **Rôle :** Outil CLI de gestion d'e-mails (IMAP/SMTP) intégré sous forme de compétence dans Hermes.
12. **Factory AI**
    * **Statut :** Payant (service tiers mentionné dans l'exemple d'e-mail de remboursement).
    * **Rôle :** Service client auquel l'agent a automatiquement envoyé une demande de remboursement sur consigne de l'utilisateur.

---

### 3) Astuces concrètes et réutilisables

* **Délégation croisée d'outils (Hermes + Claude Code) :** Donnez l'instruction à Hermes sur Telegram d'effectuer une modification dans un dépôt GitHub en utilisant la compétence `claude-code`. Hermes va appeler Claude Code en tâche de fond pour analyser le code, modifier les fichiers (ex. supprimer une bannière), commiter et ouvrir directement une Pull Request propre sur GitHub.
* **Auto-création de compétences (*Self-improving*) :** Quand Hermes résout une tâche ou fait une recherche (ex. configurer un bridge e-mail ou analyser la concurrence YouTube), il enregistre son processus sous forme d'un fichier `SKILL.md`. Cela lui évite de repartir de zéro la fois suivante.
* **Chaining Bash / Python au lieu de MCP :** Plutôt que de passer par des protocoles complexes (MCP), Hermes exécute directement du code Python en ligne de commande pour interroger des bases de données de logs, parser du JSON ou piloter des API.
* **Tableau de bord de surveillance (Hermes HUD) :** Installez Hermes HUD pour surveiller en temps réel l'utilisation de la mémoire de l'agent (`MEMORY.md` et `USER.md`), nettoyer le contexte saturé et suivre le coût exact de vos appels LLM par modèle.
* **Navigation Web autonome :** Utilisez les compétences de navigateur web intégrées à Hermes (`browser_navigate`, `browser_click`, `browser_snapshot`) pour faire des recherches approfondies (*Deep Search*) et interagir avec des interfaces web sans passer par des API fermées.
* **Nettoyage lors de la migration depuis OpenClaw :** Lors du passage d'OpenClaw à Hermes, dites explicitement à l'agent de "supprimer/tuer" (*kill*) les processus et configurations de l'ancien agent, sinon il aura tendance à ré-exécuter le code OpenClaw en boucle.

---

### 4) Chiffres de revenus annoncés

* **Revenus générés :** Non précisé (la vidéo est une démonstration technique d'automatisation et de développement, aucun chiffre de vente ou de chiffre d'affaires n'est mentionné par l'auteur).
* **Coûts de fonctionnement cités *(affirmé par l'auteur)* :** 
  * Abonnement ChatGPT / Codex : ~100 $/mois.
  * Consommation affichée sur le tableau de bord Hermes HUD : 339,95 $ enregistrés sur la journée de test d'API intensif/débogage.
