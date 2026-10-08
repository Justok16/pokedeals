# Les modèles NOUS MENTENT TOUS : La vérité sur les benchmarks SWE-Bench

Vidéo : https://youtu.be/wW9Y7zQi_j4 · durée 18:32 · résumé Gemini (gemini-3.5-flash-lite, lot de 6) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** L’analyse du benchmark SWE-bench et de ses variantes (Verified, Rebench) montre que de nombreux modèles de langage (notamment chinois ou américains) progressent rapidement en apparence, mais que ce succès est souvent biaisé par la contamination des données, l'entraînement sur les questions de test et l'obsolescence rapide des benchmarks, ce qui pose question sur la réelle supériorité de l'IA.

2) **Outils, sites ou dépôts GitHub cités :**
- **Minimax (M Series) / modèles M1, M2, M2.5 :** Modèles (gratuit ou payant selon les versions), évalués sur le codage et les benchmarks.
- **OpenAI (GPT-4, GPT-4.5, GPT-5.2) :** Modèles d'IA (payants/API), utilisés comme référence sur SWE-bench.
- **Anthropic (Claude 3.5, Claude 4, Claude Opus, Claude Code) :** Modèles et outils de codage (payants), positionnés sur les classements de programmation.
- **Google (Gemini 2.5 Pro, Gemini 3 Pro) :** Modèles d'IA (payant/API), comparés sur les benchmarks.
- **GLM-4 / GLM-5 :** Modèles (notamment chinois), testés sur les benchmarks de code.
- **SWE-bench / SWE-bench Verified / SWE-Rebench :** Sites et benchmarks (gratuits/open-source sur Hugging Face / GitHub, ex. *princeton-nlp/SWE-bench_Verified*), servant à évaluer la résolution de problèmes réels sur le code GitHub.
- **Hugging Face :** Site web (gratuit), plateforme d'hébergement de datasets dont SWE-bench Verified.
- **Escalidraw :** Outil de schématisation (gratuit/freemium), utilisé pour expliquer le fonctionnement des tests.
- **Kimi / Kimi K2 / Kimi K2.5 :** Modèles d'IA (gratuits/payants), classés sur les leaderboards.
- **OpenRouter :** Site web / plateforme d'API (payante à l'usage), permettant de comparer les performances, coûts et tokens des modèles.
- **Formation Claude Code / Setup Claude Code (mlv.sh/fa) :** Site de formation (gratuit selon la vidéo), permettant d'accéder à des tutoriels sur l'utilisation de Claude Code et l'IA.

3) **Astuces concrètes et réutilisables :**
- Comprendre le fonctionnement d'un benchmark de code : un test standardisé utilise des issues GitHub réelles (code avant, pull request, code fixé) pour vérifier si un modèle IA parvient à générer un correctif qui passe les tests unitaires.
- Se méfier des scores élevés sur les benchmarks publics : si les questions et les tests sont publics, les créateurs de laboratoires d'IA peuvent involontairement (ou volontairement) entraîner leurs modèles directement sur ces données de test, faussant ainsi les résultats de performance (phénomène de mémorisation).
- Préférer des benchmarks évolutifs et decontaminés (comme *SWE-Rebench*, qui prend des plages de dates "From -> To" dynamiques) pour évaluer la vraie progression des modèles sans fuite de données d'entraînement.
- Analyser le ratio coût/tokens/performance sur des plateformes comme OpenRouter avant de choisir un modèle pour automatiser des tâches de développement.

4) **Chiffres de revenus annoncés :**
- Non précisé (la vidéo traite de performances techniques, de scores en pourcentage sur des benchmarks et de coûts par million de tokens d'API, mais aucun chiffre de gain financier ou de revenus personnels n'est affirmé).

---
