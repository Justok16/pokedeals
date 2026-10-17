# pnD1PafeXic — « Comment AVOIR Claude en illimité et arrêter de cramer tes limites »

- Auteur : Melvynx ; lien : https://youtu.be/pnD1PafeXic
- Envoyée par l'utilisateur le 15/10/2026 ; résumée le 15/10 par Gemini (modèles gratuits, via le relais)

---

### 1. Idée principale
L'utilisation intensive et non maîtrisée des modèles d'IA les plus puissants (comme Claude Opus 5.5 au niveau « Max ») peut rapidement détruire vos limites d'utilisation (quotas) et exploser les coûts (via les *tokens* et le « *thinking* »), bloquant votre travail pendant plusieurs jours. Pour maximiser la rentabilité et l'efficacité sans se ruiner ni se faire bloquer, il faut apprendre à **surveiller sa consommation**, **adapter le niveau d'effort** (privilégier « Low » ou « Medium » pour l'exécution), et **bien structurer ses requêtes** (en combinant par exemple un agent principal avec des sous-agents moins chers pour la collecte de contexte).

---

### 2. Outils, sites et dépôts GitHub cités

*   **Claude Opus 5.5 (et la suite Claude 5.5 / Fable / Sonnet / Haiku)**
    *   *Type :* Payant (Abonnement Claude Max à 200 $ / mois, ou tarification à l'usage via l'API).
    *   *Utilité :* Modèles de langage avancés pour le code, l'écriture, le montage vidéo, etc.
*   **Agent Burn (agent-burn.melvynx.dev)**
    *   *Type :* Gratuit.
    *   *Utilité :* Application permettant de surveiller en temps réel son usage et ses limites (notamment la session et la limite hebdomadaire).
*   **Artificial Analysis (artificialanalysis.ai)**
    *   *Type :* Gratuit (avec options premium).
    *   *Utilité :* Site de benchmarks indépendants comparant l'intelligence, la vitesse et le coût par tâche des différents modèles d'IA.
*   **Hermes (hermes.melvynx.dev / application de schedule / automatisation)**
    *   *Type :* Non précisé (mentionné comme un outil personnel ou un projet/site de l'auteur).
    *   *Utilité :* Gestion, planification de posts sur les réseaux sociaux et automatisation (commentaires Instagram, etc.).
*   **Tella / Tella MCP (tella.com)**
    *   *Type :* Payant / Freemium (non détaillé précisément dans la vidéo, mais propose un protocole MCP).
    *   *Utilité :* Outil et MCP pour éditer des vidéos avec des agents IA, automatiser des démos, etc.
*   **1Password**
    *   *Type :* Payant.
    *   *Utilité :* Gestionnaire de mots de passe (connecteur/plugin mentionné dans l'écosystème).
*   **Claude in Chrome**
    *   *Type :* Gratuit / Intégré.
    *   *Utilité :* Connecteur pour interagir avec le navigateur.
*   **Clipatra**
    *   *Type :* Non précisé (supprimé par l'auteur dans la vidéo car jugé inutile pour son usage).
    *   *Utilité :* Outil/plugin/MCP tiers montré dans l'interface de Claude Code.

---

### 3. Astuces concrètes et réutilisables

1.  **Surveiller ses limites (*Session limit* vs *Weekly limit*) :** Suivez votre consommation avec des outils comme *Agent Burn*. La limite hebdomadaire (*Weekly*) est la plus critique car elle peut vous bloquer plusieurs jours d'affilée.
2.  **Ne jamais utiliser le mode « Max » d'effort par défaut :** Le mode *Max* active un niveau de réflexion (*thinking*) extrêmement coûteux en tokens de sortie. Réservez-le uniquement à des tâches de pure créativité/innovation très complexes. Pour les tâches d'exécution, de code simple ou de routine, utilisez le mode **Low** ou **Medium** (qui consomment beaucoup moins de tokens tout en restant très efficaces).
3.  **Croiser l'intelligence et le coût par tâche :** Ne choisissez pas systématiquement le modèle le plus cher (comme Opus en Max). Des modèles comme Sonnet ou Opus configurés en mode *Medium* ou *Low* offrent souvent un excellent compromis entre une intelligence suffisante et un coût divisé par 3 ou 4.
4.  **Optimiser le contexte (*Context Window*) :**
    *   Évitez de surcharger votre contexte avec des outils, scripts ou MCPs inutiles (*MCP tools*, plugins superflus, dossiers d'instructions non utilisés) qui consomment des tokens pour rien.
    *   Nettoyez régulièrement vos compétences (*skills*) et connecteurs non pertinents.
    *   Utilisez la compression de session (*compact session*) lorsque le contexte devient trop lourd.
5.  **Utiliser des sous-agents (*Sub-agents*) pour la collecte de contexte (*Context gathering*) :** Au lieu de faire tout faire par un agent principal très coûteux (ex. Opus), déléguez les tâches de recherche et de lecture de fichiers à des modèles plus rapides et moins chers (ex. Haiku) pour récupérer l'information avant de l'injecter dans l'agent principal.
6.  **Être précis dans ses prompts :** Donner des instructions claires et précises évite à l'IA de passer par de longues phases de recherche/réflexion (*thinking*) qui font exploser la facture de tokens.

---

### 4. Chiffres de revenus annoncés (*affirmés par l'auteur*)
*   **Dépenses personnelles en IA :** L'auteur affirme avoir dépensé près de **98 106,65 $** (ou environ **14 292,70 $** selon les vues du dashboard présentées) en abonnements et usage d'IA, se qualifiant de « l'un des plus gros *users* francophones de l'écosystème d'agents IA ».
*   **Statistiques de reach / audience (mentionnées à la fin pour la formation) :** Plus de **10 000 personnes aidées** et des **millions de vues sur YouTube**.

## Tri DIG16 (15/10/2026)

**Appliqué le 15/10** : économie de quota (consigne de CLAUDE.md) : réserver les efforts de réflexion élevés aux tâches complexes, déléguer les recherches simples à des sous-agents moins coûteux, garder peu d'outils et de skills actifs (règle du 15/10). Le choix du modèle et de l'effort reste à l'utilisateur (/model). **Écarté** : Agent Burn, Hermes, Tella (outils de l'auteur ou payants, non vérifiés). Dépenses de l'auteur : affirmées par lui.
