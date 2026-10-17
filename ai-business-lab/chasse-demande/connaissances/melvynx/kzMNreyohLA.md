# DEV-BROWSER : Le CLI parfait pour que ton AGENT utilise Chrome (c'est mieux que tout le reste)

Vidéo : https://youtu.be/kzMNreyohLA · durée 17:05 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur présente l'outil open source **`dev-browser`**, une alternative en ligne de commande (CLI) aux serveurs MCP (Model Context Protocol) classiques pour automatiser et contrôler un navigateur Web avec des agents IA comme **Claude Code**. Contrairement aux outils MCP traditionnels qui consomment énormément de contexte de discussion et d'appels d'API successifs, `dev-browser` permet à l'agent IA d'exécuter des blocs de code Playwright complets dans un environnement bac à sable (sandbox QuickJS/WASM) ou directement sur une session Chrome existante (conservant ainsi cookies, connexions et état), réduisant ainsi drastiquement les coûts en tokens, le temps d'exécution et les erreurs de contexte.

---

### 2) Outils, sites et dépôts GitHub cités

| Nom exact | Statut (Gratuit / Payant) | À quoi il sert |
| :--- | :--- | :--- |
| **`dev-browser`** (SawyerHood / Do Browser) | **Gratuit** (Open source sous licence MIT) | Outil CLI / skill pour agents IA permettant de piloter Chromium/Chrome via des scripts Playwright/JavaScript sandboxés avec persistance de sessions. |
| **Claude Code** | **Payant** (Consommation de tokens / API Anthropic) | Outil d'assistance au développement en ligne de commande développé par Anthropic. |
| **Playwright** | **Gratuit** (Open source) | Bibliothèque d'automatisation de navigation Web utilisée par `dev-browser` pour simuler des clics, saisies, captures d'écran et interactions. |
| **Do Browser** (`dobrowser.io`) | **Non précisé** dans la vidéo (site présenté brièvement) | Plateforme / extension liée aux créateurs de `dev-browser` pour l'automatisation du navigateur. |
| **Lumail** (`lumail.io`) | **Non précisé** (projet SaaS de l'auteur utilisé en démonstration) | Application de marketing par e-mail native pour agents IA. |
| **OpenClaw** | **Non précisé** | Environnement / bot agentique utilisé dans la vidéo pour exécuter des compétences (skills) et automatisations. |
| **Formation Claude Code / Setup** (`mlv.sh/fc` ou `codeline.dev`) | **Gratuit** (offert contre inscription e-mail dans la vidéo) | Page de formation et ressources proposant la configuration Claude Code, les scripts de statut et les agents personnalisés de l'auteur. |
| **Chrome for Testing / Chromium** | **Gratuit** (Open source) | Navigateur utilisé pour le débogage distant et l'automatisation. |

---

### 3) Astuces concrètes et réutilisables

1. **Éviter le piège du dépassement de contexte des MCP :** 
   - Remplacer les listes d'outils MCP monolithiques (qui envoient des dizaines de définitions d'outils à chaque invite) par un outil CLI scriptable unique où l'IA génère et exécute directement un script entier en une seule étape.
2. **Conserver les sessions authentifiées (GitHub, SaaS, etc.) :**
   - Lancer Chrome avec le port de débogage distant (`chrome.exe --remote-debugging-port=9222`) puis connecter `dev-browser` via `dev-browser --connect`. Cela permet à l'IA d'interagir avec des pages déjà connectées sans avoir à gérer des flux d'authentification ou des captchas à chaque relance.
3. **Tester visuellement une application Web via IA :**
   - Demander à Claude Code de prendre des captures d'écran ciblées (`await browser.getPage('main')`, `screenshot: ...`), de changer de thème (Light/Dark mode) et de valider les composants UI avant et après modifications.
4. **Validation de parcours utilisateur complexes :**
   - Donner des instructions séquentielles claires dans le terminal (ex. : *« filtre par tag AI, sélectionne le premier tag, crée un segment et confirme »*), laissant l'IA naviguer, inspecter les sélecteurs DOM et valider le résultat final par capture d'écran.

---

### 4) Chiffres de revenus annoncés

* **Revenus financiers :** **Aucun chiffre de revenus n'est mentionné** dans la vidéo (*non précisé*).
* **Métriques de performance affichées dans les benchmarks (affirmé par l'auteur / documentation) :**
  - **Dev Browser :** Temps moyen de 3m 53s, coût de 0,88 $, 29 tours (turns), 100 % de succès.
  - **Playwright MCP :** 4m 31s, coût de 1,45 $, 51 tours, 100 % de succès.
  - **Claude Chrome Extension :** 12m 54s, coût de 2,81 $, 80 tours, 100 % de succès.
