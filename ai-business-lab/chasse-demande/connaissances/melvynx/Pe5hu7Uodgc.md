# Mes 5 MEILLEURES skills pour Claude Code et Codex (c'est cheaté)

Vidéo : https://youtu.be/Pe5hu7Uodgc · durée 16:59 · résumé Gemini (gemini-3.8-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo, adapté à une démarche de développement de projets rentables avec l’IA et Claude Code :

---

### 1) Idée principale
L’auteur présente **5 « skills » (compétences/modules de consignes sous forme de fichiers `SKILL.md`)** pour agents de codage IA (comme Claude Code ou Cursor). L'objectif est d'éliminer le code et le design de mauvaise qualité (« slop » généré par l'IA), de forcer l'agent à clarifier les besoins en amont et à tester/vérifier son travail de façon autonome avec des sous-agents et des captures d'écran, permettant ainsi de créer des applications (web et mobiles) prêtes pour la production du premier coup (« one shot »).

---

### 2) Outils, sites et dépôts GitHub cités

1. **Impeccable (`impeccable.style`)**
   * **Modèle économique :** Gratuit (outil CLI open-source / expérimental mentionné via `npx impeccable`).
   * **À quoi il sert :** Génère un document de design system (`design.json` / `DESIGN.md`) sur mesure pour l'application afin d'éviter le « design slop » (polices inadaptées, styles génériques). Il comprend une collection de sous-commandes de design et une CLI (`npx impeccable detect`) pour détecter les anti-patterns dans le code.

2. **Frontend-design (Anthropic)**
   * **Dépôt / Référence :** `anthropics/skills/tree/main/skills/frontend-design`
   * **Modèle économique :** Gratuit (open-source).
   * **À quoi il sert :** Le skill historique de design d'Anthropic pour guider l'IA sur l'esthétique et la typographie (l'auteur note qu'il est désormais un peu trop lourd et a tendance à reproduire de nouveaux clichés visuels).

3. **Grilling (ou Grill-me de Matt Pocock)**
   * **Dépôt / Référence :** `mattpocock/skills/tree/main/skills/productivity/grilling` (auparavant `grill-me`).
   * **Modèle économique :** Gratuit (open-source).
   * **À quoi il sert :** Force l'agent IA à poser une série de questions ciblées et insistantes (« griller » le développeur) sur les détails d'un plan ou d'une fonctionnalité avant d'écrire la moindre ligne de code, évitant les malentendus.

4. **APEX (AIBlueprint CLI)**
   * **Site / Documentation :** `docs.aiblueprint.dev/concepts/apex`
   * **Modèle économique :** Décrit comme « Premium skill » sur la documentation affichée (payant / freemium selon accès).
   * **À quoi il sert :** Automatise un workflow complet en plusieurs phases : Analyse, Planification, Exécution, Validation (typecheck, tests), Examen contradictoire via des sous-agents parallèles, et Vérification (lancement de l'appli et prise de captures d'écran automatiques) pour valider visuellement les résultats.

5. **Make Interfaces Feel Better (Jakub Krikal)**
   * **Site / Dépôt :** `jakub.krikal/make-interfaces-feel-better` / `skills.sh`
   * **Modèle économique :** Gratuit (open-source).
   * **À quoi il sert :** Améliore les micro-détails d'interface utilisateur (alignements optiques, lissage de sous-pixels, animations de compteurs, bordures de contraste, etc.).

6. **Thermo-Nuclear Code Quality Review (Cursor Team Kit)**
   * **Dépôt GitHub :** `cursor/plugins` (dossier `cursor-team-kit/skills/thermo-nuclear-code-quality-review`).
   * **Modèle économique :** Gratuit (open-source).
   * **À quoi il sert :** Revue de code extrêmement stricte pour éliminer le « code spaghetti », simplifier l'architecture, auditer la sécurité, la maintenabilité et supprimer le code mort.

7. **Sites et ressources de l'auteur (Melvynx / Codelynx)**
   * **`mlv.sh/fm`** : Page d'accès à une mini-formation gratuite (comprenant 3 skills pour automatiser le développement mobile avec l'IA).
   * **`mlv.sh/fc`** : Formation payante de l'auteur (« 1 commande qui transforme tes agents IA en senior développeur »).
   * **`codelynx.dev`** : Blog technique de l'auteur récapitulant les commandes et liens de la vidéo.

---

### 3) Astuces concrètes et réutilisables

* **Faire « griller » son idée avant d'implémenter :** Utiliser une commande/skill comme `/grilling` pour que l'IA challenge chaque choix technique et fonctionnel avant d'écrire du code. Cela évite les itérations inutiles et permet un résultat propre dès la première tentative (« one shot »).
* **Installer les skills globalement :** Installer les skills de manière globale sur la machine avec le gestionnaire de skills (`npx skills add <nom_du_skill> -g`) pour pouvoir les invoquer depuis n'importe quel projet ou agent (Claude Code, Cursor, etc.).
* **Déléguer la revue de code à des sous-agents dédiés :** Ne pas demander au même agent qui vient d'écrire le code de faire sa propre relecture (il a tendance à valider ses propres erreurs). Il est plus efficace d'invoquer un sous-agent avec un contexte vierge et des consignes strictes (ex: *Thermo-Nuclear Quality Review* ou agent de sécurité).
* **Validation visuelle automatique :** Configurer l'agent pour qu'il prenne des captures d'écran de l'application en cours d'exécution dans le simulateur/navigateur et les inspecte lui-même afin de corriger les défauts d'affichage avant de rendre la main.
* **Créer un fichier de style persistant (`DESIGN.md`) :** Initialiser la charte avec un outil comme `impeccable init` pour que l'IA respecte des règles de design préétablies (palette, espacements, composants) au lieu d'inventer des styles au hasard à chaque prompt.

---

### 4) Chiffres de revenus annoncés
* **Non précisé** : L'auteur ne mentionne aucun chiffre d'affaires, gain financier personnel ou promesse de revenu chiffré dans la vidéo.
