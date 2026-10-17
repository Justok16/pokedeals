# BREAKING : OpenAI lance un modèle hors ligne ouvert GRATUIT !

Vidéo : https://youtu.be/LEd_b2vTbAM · durée 16:06 · résumé Gemini (gemini-3.5-flash, lot de 5) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) Idée principale**
OpenAI a publié deux modèles de raisonnement open-weight (poids ouverts) nommés `gpt-oss-120b` et `gpt-oss-20b` sous licence Apache 2.0. Ils s'exécutent entièrement en local sans connexion Internet, tout en offrant des performances comparables aux modèles fermés récents comme `o4-mini`.

**2) Outils, sites et dépôts GitHub cités**
*   **gpt-oss-120b & gpt-oss-20b (OpenAI)** : Gratuit / Open-weight (Licence Apache 2.0). Modèles de langage à poids ouverts axés sur le raisonnement et le code, utilisables en local.
*   **LM Studio** : Gratuit. Application permettant de télécharger, configurer et exécuter des modèles LLM locaux sur Mac, Windows et Linux.
*   **Hugging Face** : Gratuit. Plateforme d'hébergement et de téléchargement des modèles d'IA.
*   **Recraft** : Gratuit (avec options payantes / sponsor). Outil de génération d'images et de graphiques vectoriels IA créant de vrais fichiers SVG exploitables pour le design.
*   **Perplexity** : Gratuit / Payant. Moteur de recherche IA utilisé pour vérifier la compatibilité des cartes graphiques (VRAM).
*   **Ollama, vLLM, llama.cpp, Fireworks, Together AI, Baseten, Databricks, Vercel, Cloudflare, OpenRouter** : Gratuit / Payant. Plateformes et frameworks d'inférence et de déploiement local ou cloud cités.
*   **Microsoft / ONNX Runtime / Foundry Local** : Gratuit. Outils d'optimisation GPU pour exécuter `gpt-oss-20b` sur les appareils Windows.

**3) Astuces concrètes et réutilisables**
*   **Éliminer les coûts d'API** : En faisant tourner `gpt-oss` en local via LM Studio, vous n'avez aucun frais d'utilisation par jeton et vos données ne quittent pas votre ordinateur.
*   **Choix du matériel** : 
    *   `gpt-oss-20b` nécessite environ 16 Go de VRAM (compatible avec la majorité des GPU modernes comme RTX 3090, 4080, 5080, RX 7800 XT ou les Mac Apple Silicon).
    *   `gpt-oss-120b` nécessite une configuration lourde avec ~80 Go de RAM/VRAM (type Mac Studio haut de gamme).
*   **Paramétrage dans LM Studio** : Réglez la fenêtre de contexte (*Context Length*) et activez le niveau d'effort de raisonnement (*Reasoning Effort* : Low, Medium, High) selon la complexité du code à générer.
*   **Environnement de bac à sable** : Activez l'intégration `js-code-sandbox` dans LM Studio pour tester et exécuter le code JavaScript généré directement par le modèle local.

**4) Chiffres de revenus annoncés**
*   Non précisé.

---
