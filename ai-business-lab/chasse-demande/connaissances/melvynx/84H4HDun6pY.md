# DeepSWE détruit les modèles chinois (et Claude... désolé les fans)

Vidéo : https://youtu.be/84H4HDun6pY · durée 19:10 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur analyse les limites des benchmarks actuels d'IA pour le code (notamment SWE-bench Pro) qu'il juge biaisés ou déconnectés de la réalité du terrain. Il présente le nouveau benchmark **DeepSWE** (conçu par Datacurve), qui évalue les agents IA sur des tâches d'ingénierie logicielle longues, complexes, multi-fichiers et sans contamination préalable. Les résultats confirment l'expérience réelle des développeurs : les modèles de pointe propriétaires dominent nettement en efficacité et en coût par rapport aux modèles chinois ou aux versions allégées, à condition d'adopter les bons outils d'orchestration et les bonnes méthodes d'instruction.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit ou Payant | À quoi il sert |
| :--- | :--- | :--- |
| **DeepSWE** (`deepswe.datacurve.ai`) | **Gratuit** (consultation publique) | Benchmark et article de recherche évaluant les capacités réelles d'agents de code sur des tâches logicielles complexes. |
| **SWE-bench / SWE-bench Pro** (`swebench.com`) | **Gratuit** (open source) | Benchmark de référence historique pour évaluer la résolution de tickets GitHub par des LLMs. |
| **Codex** (OpenAI / Codex Desktop / Codex CLI) | **Payant** (l'auteur indique payer un abonnement à 200 $/mois) | Environnement et agent d'exécution pour coder et refactorer des bases de code entières. |
| **Claude Code / Claude Code CLI** (Anthropic) | **Payant** (via API / abonnements Anthropic - *détail précis non précisé*) | Agent en ligne de commande d'Anthropic pour interagir directement avec un dépôt de code. |
| **Gemini CLI** (Google) | *Non précisé* (accès API Google) | Outil CLI pour faire agir les modèles Gemini sur du code. |
| **mini-swe-agent** | **Gratuit** (open source) | Harnais d'orchestration minimaliste pour exécuter des agents de code de manière standardisée. |
| **Code Arena / LMSYS Arena** (`arena.ai`) | **Gratuit** | Classement comparatif de modèles de code basé sur des votes/tests. |
| **X (Twitter)** | **Gratuit** (avec options payantes) | Plateforme de veille technologique où développeurs et chercheurs partagent leurs retours d'expérience. |
| **FastAPI**, **LangChain** | **Gratuit** (open source) | Bibliothèques logicielles open-source utilisées parmi les 91 dépôts de test du benchmark DeepSWE. |
| **Codelynx / AI Blueprint** (`codelynx.dev`, `mlv.sh/fa`) | **Payant** | Plateforme et formation de l'auteur pour apprendre le métier d'AI Engineer et coder plus vite avec les agents. |

---

### 3) Astuces concrètes et réutilisables (notamment avec Claude Code / agents de code)

* **Décomposer les instructions complexes avec Claude :** L'analyse DeepSWE démontre que Claude a tendance à oublier des exigences lorsqu'on lui fournit des prompts en plusieurs volets simultanés (*"forgetful with multi-part prompts"*). Découpez vos consignes de façon séquentielle plutôt que de tout regrouper dans un seul prompt massif.
* **Privilégier un harnais d'orchestration simple :** Les résultats montrent qu'un orchestrateur minimaliste (comme `mini-swe-agent`) surpasse régulièrement les harnais natifs (Claude Code CLI ou Gemini CLI) en taux de succès tout en consommant moins de tokens.
* **Laisser l'agent écrire et exécuter ses propres tests :** Les modèles les plus performants testent systématiquement leur propre code dans l'environnement du projet avant de soumettre leur travail. Incitez ou configurez vos agents pour exécuter la suite de tests existante afin de valider chaque patch.
* **Surveiller la consommation de tokens :** Certains modèles nécessitent 2 à 3 fois plus de tokens pour accomplir la même tâche tout en obtenant un moins bon score. Utiliser un modèle plus précis dès le départ réduit directement vos coûts d'API.
* **Pratiquer le "one-shot" d'architecture :** En structurant précisément le contexte et les règles dès le départ, il est possible de faire migrer ou créer des briques applicatives entières sans intervention manuelle répétée.

---

### 4) Chiffres de revenus annoncés

* **200 000 $+ par an :** Rémunération mentionnée sur le site de formation de l'auteur pour les postes d'AI Engineer (« affirmé par l'auteur »).
* **50 000 $/mois et ~420 000 $/mois :** Revenus générés par le développement d'applications sans code manuel affichés dans un tweet d'Alejandro à l'écran (« affirmé par l'auteur » du tweet).
* **100 000 $ :** Offre de rachat d'une application (PostPlanify) affichée dans un tweet de TrustMRR (« affirmé par l'auteur » du tweet).
