# _Up4YpZe5H8 — « J’ai testé l’outil IA viral qui clone n’importe quel logiciel (reverse engineering) »

- Auteur : Simon De Lima (https://www.youtube.com/@Simon_de_lima) ; lien : https://youtu.be/_Up4YpZe5H8
- Envoyée par l'utilisateur le 15/10/2026 ; résumée le 15/10 par Gemini (modèle gemini-3.5-flash-lite, via le relais)

### 1) Idée principale
L'outil REA (Reverse Engineer Anything) est un skill gratuit pour les agents IA (comme Claude Code) qui décompile et analyse des applications existantes pour aider à les recréer. Pour quelqu'un qui veut gagner de l'argent avec l'IA, l'idée n'est pas de copier illégalement du code protégé, mais d'utiliser ces outils pour comprendre rapidement comment fonctionnent les meilleures applications (comme Trello), s'en inspirer, et reconstruire rapidement des solutions concurrentes (en respectant les aspects légaux, notamment l'interopérabilité).

---

### 2) Outils, sites et dépôts GitHub cités

*   **REA (Reverse Engineer Anything)**
    *   **Nom exact :** REA
    *   **Prix :** Gratuit (open-source)
    *   **Rôle :** Skill pour agents IA (branché sur Claude Code) permettant de décompiler, analyser et reconstruire des logiciels, applications et sites web.
    *   **Lien / Dépôt :** `github.com/morluto/rea` (adresse corrigée le 15/10 : la vidéo est mal transcrite, dépôt vérifié par recherche web)

*   **Claude Code**
    *   **Nom exact :** Claude Code
    *   **Prix :** Non précisé (lié à l'écosystème Anthropic)
    *   **Rôle :** Agent IA utilisé dans un terminal/éditeur pour exécuter des requêtes de développement, installer REA et piloter la reconstruction d'applications.

*   **VS Code**
    *   **Nom exact :** VS Code (Visual Studio Code)
    *   **Prix :** Gratuit
    *   **Rôle :** Éditeur de code utilisé dans la vidéo pour utiliser Claude Code.

*   **Ghidra**
    *   **Nom exact :** Ghidra
    *   **Prix :** Gratuit (public depuis 2019, créé par la NSA)
    *   **Rôle :** Outil de reverse engineering pour analyser des binaires et logiciels.

*   **Hopper**
    *   **Nom exact :** Hopper
    *   **Prix :** Payant (logiciel existant depuis plus de 15 ans)
    *   **Rôle :** Outil de reverse engineering et désassemblage.

*   **IDA (IDA Pro)**
    *   **Nom exact :** IDA
    *   **Prix :** Payant (référence du secteur depuis les années 90)
    *   **Rôle :** Outil de décompilation et débogage pour le reverse engineering avancé.

*   **Google Chrome**
    *   **Nom exact :** Google Chrome
    *   **Prix :** Gratuit
    *   **Rôle :** Navigateur utilisé avec un profil dédié et le débogage à distance pour analyser des sites web et web apps.

*   **Trello**
    *   **Nom exact :** Trello
    *   **Prix :** Freemium / Payant (application prise comme exemple)
    *   **Rôle :** Application de productivité et de gestion de projet (kanban) utilisée pour le test de reverse engineering.

*   **Cairn** (ou Cairn / Cairn-trello)
    *   **Nom exact :** Cairn
    *   **Prix :** Gratuit (application recréée localement)
    *   **Rôle :** Nom donné par l'IA à l'application recréée à partir du reverse engineering de Trello.

*   **Newsletter IA de l'auteur**
    *   **Nom exact :** wolph (wolph.pro)
    *   **Prix :** Gratuit
    *   **Rôle :** Newsletter quotidienne (envoyée chaque midi) sur l'actualité, la monétisation et les outils activables en IA.

---

### 3) Astuces concrètes et réutilisables

*   **Brancher un skill à son agent IA :** Installer REA sur Claude Code via un dépôt GitHub pour donner à l'IA des capacités d'analyse de binaires, de sites web et de reverse engineering.
*   **Isoler la navigation :** Utiliser une instance dédiée de Google Chrome avec un profil séparé et le débogage à distance pour permettre à l'IA d'analyser des pages web sans compromettre sa session personnelle.
*   **La bonne méthode de reverse engineering :** Ne pas copier bêtement du code protégé, mais suivre la règle légale et éthique :
    1. **Comprendre** ce que fait l'outil (observer le comportement).
    2. **Lister** les fonctionnalités dont on a besoin.
    3. **Construire** sa propre version avec son propre nom, son propre design et sa propre identité visuelle.
*   **Utiliser l'IA comme accélérateur :** Permettre à l'IA de décompiler et d'analyser des workflows complexes en quelques minutes pour gagner un temps précieux sur la phase d'apprentissage technique.

---

### 4) Chiffres de revenus annoncés (marqués « affirmé par l'auteur »)

*   **Affirmé par l'auteur :** Plus de **9 000** abonnés lisent sa newsletter quotidienne gratuite.
*   **Affirmé par l'auteur :** Des projets de reverse engineering qui prenaient auparavant des **années** peuvent maintenant se faire en **quelques jours** grâce à ces outils d'IA.
*   **Affirmé par l'auteur :** Une application qui demandait des **années de travail** et des **centaines de milliers d'euros d'investissement** peut être en grande partie reconstruite en **quelques minutes** par une IA généraliste.

## Tri DIG16 (15/10/2026)

- **Écarté : installer REA.** C'est un programme en ligne de commande + serveur MCP + skill (`morluto/rea`) qui pilote des
  décompilateurs (Ghidra, Hopper, IDA) et un Chrome en débogage à distance. Aucun besoin pour DIG16 (sites vitrines simples,
  construits de zéro) ; programme tiers qui s'exécute et se met à jour seul (`rea update`) : même refus que pour Impeccable
  (`46` ligne 1). **Cadre légal** : en France, décompiler un logiciel n'est permis que pour l'interopérabilité (art. L122-6-1
  du Code de la propriété intellectuelle, à relire sur Légifrance avant toute affirmation chiffrée ou citée) ; reproduire
  le design ou les textes d'un site tiers reste interdit.
- **Déjà appliqué (la bonne méthode de la vidéo) : « comprendre, lister, construire sa propre version ».** C'est exactement
  la façon dont sont faites les démos DIG16 : on observe le site actuel du prospect, on liste ce qu'il fait, puis on
  construit une page neuve avec notre propre code et notre propre design (photos et logo du prospect seulement avec
  son accord, décision du 05/10).
- **Écarté** : newsletter de l'auteur (hors sujet), chiffres de l'auteur (non vérifiables).
