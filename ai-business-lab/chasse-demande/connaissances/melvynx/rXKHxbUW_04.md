# MIGRATION de Claude à Codex : 1 seul ligne à faire (TUTO SIMPLE)

Vidéo : https://youtu.be/rXKHxbUW_04 · durée 10:31 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'objectif de la vidéo est de montrer comment **centraliser, unifier et synchroniser automatiquement la configuration de ses agents IA et compétences (*skills*)** entre différents outils de code assisté par IA (principalement **Claude Code**, **Codex** et **Cursor**). Grâce à une seule commande CLI, l'utilisateur évite de devoir reconfigurer ses agents manuellement à chaque changement d'outil, et sécurise ses configurations grâce à un système de sauvegardes.

---

### 2) Outils, sites et dépôts cités

1. **Codex (OpenAI Codex)**
   * **Modèle économique :** Inclus avec les forfaits ChatGPT / API OpenAI (*freemium / payant selon usage*).
   * **Utilité :** Environnement / assistant de développement agentique pour exécuter des tâches de code et lancer des agents spécialisés.

2. **Claude Code**
   * **Modèle économique :** Payant via l'API Anthropic (ou abonnement Claude Max/Pro).
   * **Utilité :** Outil CLI d'Anthropic pour générer, auditer et exécuter du code assisté par IA avec des commandes et sous-agents personnalisés.

3. **Cursor**
   * **Modèle économique :** Freemium / Payant (abonnement).
   * **Utilité :** Éditeur de code assisté par IA compatible avec les agents et compétences unifiés.

4. **LALAL.AI (`lalal.ai`)** *(Sponsor)*
   * **Modèle économique :** Freemium (10 minutes gratuites offertes, puis plans Lite à 7,50 $/mois, Pro à 15 $/mois, et options API).
   * **Utilité :** Séparation de pistes audio par IA (retrait du bruit de fond, isolation de voix, suppression d'instruments, clonage de voix) accessible via interface web ou API pour créer des applications/SaaS.

5. **AI Blueprint CLI (`aiblueprint-cli` / `cli.codelynx.dev`)**
   * **Modèle économique :** Gratuit / Open source pour les commandes de base (avec une version pro payante).
   * **Utilité :** Outil en ligne de commande pour regrouper les dossiers de compétences et agents (`.claude`, `.codex`, etc.) dans un dossier centralisé via des liens symboliques (*symlinks*), avec gestion de sauvegardes et restauration (*snapshots*).

6. **`mlv.sh/fc` (CodeLynx Config Pro)**
   * **Modèle économique :** Payant.
   * **Utilité :** Configuration avancée prête à l'emploi (agents spécialisés, statusline, règles de sécurité de suppression de fichiers) pour Claude Code, Codex et Cursor.

7. **`mlv.sh/fa` / `codeline.app`**
   * **Modèle économique :** Gratuit (sur inscription).
   * **Utilité :** Plateforme de formation pour apprendre à configurer et utiliser Claude Code et les agents IA.

---

### 3) Astuces concrètes et réutilisables

* **Unification en une ligne :** Exécuter la commande `npx aiblueprint-cli@latest agents unify` pour scanner vos configurations Claude Code / Codex, les centraliser dans un dossier commun `~/.agents`, et créer automatiquement les liens symboliques (*symlinks*) vers les différents environnements.
* **Sécuriser ses suppressions :** Mettre en place un hook de sécurité qui remplace les commandes destructrices (type `rm -rf`) par un utilitaire de corbeille (`trash`) pour éviter toute perte accidentelle de fichiers lors de l'exécution automatique par un agent.
* **Gestion de versions de config (Snapshots) :**
  * Lister les sauvegardes : `npx aiblueprint-cli@latest configs list`
  * Restaurer une version précédente après modification ou bug : `npx aiblueprint-cli@latest configs load <nom_de_la_sauvegarde>`
* **Opportunité business (Monétisation IA) :** Utiliser l'API d'outils de traitement audio comme LALAL.AI pour packager des fonctionnalités de nettoyage de son ou d'isolation de voix au sein d'une application mobile ou d'un SaaS.

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de revenus n'est mentionné dans la vidéo.**
