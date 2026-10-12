# 5 OUTILS Claude Code que tu DOIS connaître.

Vidéo : https://youtu.be/oLG0hh_xeWU · durée 16:26 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-11
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Présentation de 5 outils indispensables et utiles pour les développeurs utilisant **Claude Code**, afin de surveiller l'utilisation, d'automatiser des tâches via des agents et d'optimiser l'écosystème.

2) **Outils, sites et dépôts GitHub cités :**
*   **Claude Code :** L'agent de code CLI (statut non précisé).
*   **`ccusage` (`ryanzur/ccusage` sur GitHub) :** Outil CLI open-source/gratuit pour analyser l'utilisation des tokens Claude Code et obtenir un rapport des coûts (par jour, par mois, par session, ou en temps réel avec `ccusage blocks --live`).
*   **VS Code :** Éditeur de code (gratuit).
*   **`CCNotify` (`dazubee/CCNotify` sur GitHub) :** Outil/script Python open-source/gratuit pour envoyer des notifications système (macOS) lorsque Claude Code requiert une saisie ou termine une tâche, grâce aux "Hooks" (UserPromptSubmit, Stop, Notification).
*   **SuperClaude (`SuperClaude_Framework` sur GitHub) :** Framework de configuration open-source/gratuit proposant des commandes spécialisées, des "Smart Personas" (rôles d'architecte, back-end, testeur, etc.) et une intégration MCP (Model Context Protocol).
*   **Claude Code Templates (`claudecode.com/templates` ou similaire) :** Dépôt/site de templates prêts à l'emploi (Agents, Commandes, MCP, Templates pour React, Vue, iOS, Playwright, etc., gratuits).
*   **Claude Code Web UI (`claudia.gui`, `open-code`, etc.) :** Interfaces web alternatives pour interagir avec Claude Code sans passer uniquement par le terminal (statut non précisé).

3) **Astuces concrètes et réutilisables :**
*   Utiliser la commande terminal `npx ccusage` (ou `ccusage daily`, `ccusage monthly`) pour suivre précisément sa consommation d'API et éviter les surprises de facturation.
*   Configurer les **Hooks** de Claude Code dans `~/.claude/settings.json` en y ajoutant des scripts pour automatiser des notifications de bureau (`terminal-notifier`) lors des prompts ou de la fin des tâches longues.
*   Employer les **Smart Personas** et les commandes de **SuperClaude** (` /sc analyze`, etc.) pour structurer les analyses de code, les refactorisations et les vérifications de bugs de manière automatisée.
*   Installer des templates spécifiques (ex: `ios-developer` ou des templates de composants) via les commandes de packages pour initialiser rapidement des configurations complexes dans ses projets.

4) **Chiffres de revenus annoncés (« affirmé par l'auteur ») :**
*   Coûts d'utilisation de Claude Code mentionnés à titre d'exemple d'utilisation personnelle (ex: sessions à 1,01 $, 6 $ par jour, 110 $, 166 $ ou 118 $ selon les périodes et les modèles comme *sonnet* ou *opus*).

---
