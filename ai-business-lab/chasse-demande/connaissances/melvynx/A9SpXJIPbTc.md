# Claude Code prend le contrôle de ton ordinateur (application, simulateur, etc...)

Vidéo : https://youtu.be/A9SpXJIPbTc · durée 14:29 · résumé Gemini (gemini-3.7-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
Anthropic a intégré la fonctionnalité **Computer Use** nativement dans **Claude Code** sous forme de serveur MCP (Model Context Protocol). Cela permet à Claude de prendre le contrôle direct de l'ordinateur (déplacement et clics de souris, saisie clavier, captures d'écran, glisser-déposer) afin d'exécuter des tests end-to-end d'applications, d'interagir avec des interfaces graphiques (GUI) ou d'effectuer des réglages système. Bien que puissant pour de l'automatisation ou des tests sur un serveur distant (VPS), l'outil monopolise l'écran et la souris en local.

---

### 2) Outils, sites et dépôts GitHub cités

* **Claude Code (Anthropic)**
  * *Statut :* Payant (consommation de crédits API / tokens Anthropic, plans Pro/Max).
  * *Usage :* Outil d'assistance au développement en ligne de commande.
* **Serveur MCP `computer-use`**
  * *Statut :* Intégré nativement dans Claude Code (consomme des tokens API).
  * *Usage :* Permet à l'IA d'interagir avec l'interface graphique (cliquer, taper, capturer l'écran, glisser-déposer).
* **Modèles Claude (Opus 4.6, Haiku 4.5)**
  * *Statut :* Payant (via API Anthropic).
  * *Usage :* Moteurs d'intelligence artificielle exécutant les instructions de raisonnement et de contrôle d'interface.
* **mlv.sh/fc (Codeline.app)**
  * *Statut :* Gratuit (sur inscription).
  * *Usage :* Plateforme de l'auteur partageant sa configuration complète pour Claude Code (agents, skills, statusline, configuration des permissions).
* **Ghostty**
  * *Statut :* Gratuit / Open source.
  * *Usage :* Émulateur de terminal utilisé pour faire tourner Claude Code et permettre le zoom vidéo.
* **Cmux**
  * *Statut :* Gratuit / Open source.
  * *Usage :* Multiplexeur / terminal mentionné par l'auteur comme son outil quotidien.
* **Parler (Dépôt local/open source)**
  * *Statut :* Gratuit / Open source.
  * *Usage :* Application native de transcription audio utilisée dans la vidéo pour tester la navigation et la modification de raccourcis par Claude.
* **Pixelmator Pro**
  * *Statut :* Payant.
  * *Usage :* Logiciel d'édition graphique sur macOS utilisé pour tester si Claude peut modifier des réglages de pinceaux et dessiner une image.
* **Claude in Chrome**
  * *Statut :* Non précisé (intégration / extension Anthropic).
  * *Usage :* Permet à Claude d'interagir spécifiquement avec les pages Web dans le navigateur.
* **X (Twitter)**
  * *Statut :* Gratuit / Option payante.
  * *Usage :* Consultation des annonces officielles (Auto mode) et des retours de la communauté.
* **OBS Studio**
  * *Statut :* Gratuit / Open source.
  * *Usage :* Logiciel de capture vidéo et de streaming visible lors des tests.

---

### 3) Astuces concrètes et réutilisables

1. **Activer `computer-use` dans Claude Code :**
   * Ouvrir Claude Code dans le terminal et taper la commande `/mcp`.
   * Sélectionner `computer-use` dans la liste des serveurs MCP intégrés et choisir `Enable`.
2. **Configurer les permissions système (macOS) :**
   * Donner au terminal (ex: Ghostty) les autorisations dans *Réglages Système > Confidentialité et sécurité* pour l'**Accessibilité** et l'**Enregistrement de l'écran**.
3. **Automatisation de tests E2E sans framework lourd :**
   * Lancer une application en mode développement directement via Claude Code.
   * Demander à Claude de tester les parcours utilisateurs (navigation entre onglets, vérification visuelle par capture d'écran, assignation de raccourcis clavier, boutons de réinitialisation).
4. **Utilisation sur machine virtuelle ou VPS :**
   * Étant donné que `computer-use` monopolise le curseur physique et l'écran en local, déployer ces agents sur un VPS ou une machine distante dédiée pour exécuter des tâches en arrière-plan sans bloquer sa propre station de travail.
5. **Prestations de services et création de valeur :**
   * Proposer des prestations d'automatisation de QA (assurance qualité logicielle) ou de manipulation de logiciels tiers sans API (ex: Figma, outils internes, simulateurs mobiles) grâce à des agents basés sur Claude Code.

---

### 4) Chiffres de revenus annoncés

* **Non précisé** (aucun chiffre de revenus n'est mentionné dans la vidéo).
