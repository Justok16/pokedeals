# L'effort est plus important que ce que tu penses : lequel choisir ?

Vidéo : https://youtu.be/4VZPCEtg6uU · durée 15:10 · résumé Gemini (gemini-3.7-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1. L’idée principale
Le paramètre de **« Thinking / Effort »** (budget de réflexion) dans les agents de code IA ne garantit pas une meilleure intelligence : augmenter l'effort au niveau maximum (**MAX**) augmente systématiquement le coût en tokens (+49 %) et le temps d'exécution (+74 %), mais conduit souvent à du « sur-raisonnement » (*overthinking*) ou à des modifications hors-sujet. La réussite d'une tâche dépend avant tout du système global (précision du prompt, contexte fourni, outils et tests automatisés) et non du seul modèle ou du niveau d'effort maximal.

---

### 2. Outils, sites et plateformes cités

| Nom exact | Gratuit / Payant | Utilité |
| :--- | :--- | :--- |
| **Claude / Claude Code** (Anthropic) | Payant (via API / abonnement) | Modèle de langage et agent de programmation utilisé pour exécuter des tâches de développement. |
| **ChatGPT** (OpenAI) | Gratuit / Payant | Modèle IA mentionné pour ses réglages de niveau de réflexion recommandés. |
| **Codex** *(interface d'agent montrée dans la vidéo)* | Payant (consommation de tokens) | Interface agentique de développement permettant d'ajuster le curseur d'effort/modèle (*Sol*, *Terra*, *Light*). |
| **Excalidraw** (`app.excalidraw.com`) | Gratuit (version en ligne) | Outil de schéma/tableau blanc utilisé par l'auteur pour modéliser les matrices et flux de décision. |
| **Lumail / Lumail.io** | Projet de démonstration | Application web montrée en exemple pour tester les reviews d'interfaces par l'agent. |
| **CodeSynx / AI Blueprint** (`mlv.sh/fa` / `codesynx.dev`) | Gratuit / Payant selon la formule (*non précisé en détail*) | Formation et configuration clé en main pour devenir « AI Engineer ». |

---

### 3. Astuces concrètes et réutilisables

1. **Règle du minimum suffisant :** Ne commencez jamais au niveau MAX par défaut.
   - **Claude :** Démarrez en **Medium / High**.
   - **ChatGPT :** Démarrez en **Medium**.
2. **Adapter l'effort selon la nature de la tâche :**
   - **LOW :** Tâches courtes, très cadrées, sous-agents, classification, mise à jour de texte simple.
   - **MEDIUM :** Routine quotidienne du dev, bon compromis coût/qualité sans surcoût.
   - **HIGH :** Code complexe, raisonnement multi-fichiers, architecture agentique standard.
   - **XHIGH / MAX :** Uniquement pour les explorations très créatives, les demandes abstraites/vagues, ou la refonte lourde d'architecture (*problèmes dits « frontière »*).
3. **Privilégier la vérifiabilité par des tests :** Écrivez un script ou des tests automatisés pour valider le résultat. L'agent itérera efficacement jusqu'à réussir, même avec un niveau d'effort modéré.
4. **Clarifier la demande plutôt que monter l'effort :** Si une tâche échoue, précisez le contexte, découpez la tâche ou ajoutez des règles précises avant d'augmenter le slider d'effort.

---

### 4. Chiffres de revenus annoncés

* **200 000 $+/an** : Salaire mentionné pour le rôle de *« AI Engineer »* sur la page de destination de sa formation (à 07:01) — *affirmé par l'auteur*.
