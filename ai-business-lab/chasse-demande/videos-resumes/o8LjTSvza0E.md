# o8LjTSvza0E — « This Viral Open Source Repo Lets Claude Clone ANYTHING »

- Auteur : Chase AI ; lien : https://youtu.be/o8LjTSvza0E
- Envoyée par l'utilisateur le 15/10/2026 ; résumée le 15/10 par Gemini (via le relais)

---

### 1) Idée principale
La vidéo explique comment utiliser **Claude Code** (via un outil de rétro-ingénierie open-source nommé REA) pour déconstruire le fonctionnement interne de logiciels, applications ou sites existants. L'objectif est d'analyser leur code jusqu'au niveau machine pour comprendre comment ils fonctionnent, puis de créer des versions personnalisées et adaptées à ses propres besoins ou projets commerciaux.

---

### 2) Outils, sites et dépôts GitHub cités

*   **REA (Reverse Engineer Anything)**
    *   **Lien / Dépôt GitHub :** `moroshko/rea` (ou `rea-agents`)
    *   **Gratuit ou payant :** Gratuit (Open Source)
    *   **À quoi il sert :** Un dépôt MCP (Model Context Protocol) qui permet à Claude d'analyser, décompiler et cartographier plus de 20 types de logiciels et binaires différents, du code source jusqu'au niveau de la machine.

*   **Ghidra**
    *   **Lien / Origine :** Développé par la NSA (disponible en open-source).
    *   **Gratuit ou payant :** Gratuit (Open Source)
    *   **À quoi il sert :** Un outil de rétro-ingénierie logiciel (utilisé par REA comme "les mains") pour analyser le code machine, le décompiler et le traduire en pseudo-code compréhensible.

*   **Claude Code Masterclass**
    *   **Lien / Site :** Chase AI+ (communauté de l'auteur)
    *   **Gratuit ou payant :** Payant (mentionné comme sponsor / formation de l'auteur)
    *   **À quoi il sert :** Une formation proposée par le créateur de la vidéo pour apprendre à utiliser Claude Code de zéro à expert en développement IA.

---

### 3) Astuces concrètes et réutilisables

*   **Approche en 4 étapes pour déconstruire une application :**
    1.  **Demander (You Ask) :** Poser une question précise à l'agent IA sur ce que fait l'application (ex: comprendre les raccourcis clavier ou l'enregistrement audio de *Wispr Flow*).
    2.  **Cartographier l'application (Map the App) :** Utiliser REA pour envoyer chaque partie du logiciel vers l'outil d'analyse adapté (Ghidra pour le code machine, analyseurs JS pour le web) afin d'obtenir une carte complète (fonctions, adresses web, liens).
    3.  **Enquêter (Investigate) :** Lancer une boucle de questions-réponses ciblées entre Claude et REA, où chaque affirmation de l'IA est étayée par des faits et des « reçus » (preuves dans le code).
    4.  **Construire (Build Your Own) :** Utiliser le plan détaillé et les preuves recueillies pour écrire un **nouveau code propre et personnalisé**, et non pour copier bêtement l'original.
*   **Utiliser les bons outils selon la cible :** Ne pas se contenter de demander à Claude Code d'analyser un binaire de manière autonome ; combiner Claude avec des moteurs spécialisés (comme Ghidra pour les binaires natifs ou des analyseurs JavaScript pour les applications Electron) pour obtenir des résultats précis.

---

### 4) Chiffres de revenus annoncés

*   **Revenus annoncés :** **Non précisé** (aucun chiffre de gain financier n'est mentionné dans la vidéo, l'accent étant mis sur la technique de rétro-ingénierie et le développement).

## Tri DIG16 (15/10/2026)

**Écarté** : même outil REA que `_Up4YpZe5H8.md` (dépôt réel : `morluto/rea`, le nom cité ici est mal transcrit). Méthode en 4 temps (demander, cartographier, enquêter avec preuves, reconstruire du code neuf) : **déjà appliquée** dans l'esprit pour les démos (observer le site du prospect, reconstruire du neuf). Formation payante de l'auteur : écartée (budget 0 €).
