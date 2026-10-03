# Gemini 3.8 Flash : mieux que Fable et GPT Sol, c'est quoi ce bordel ?

Vidéo : https://youtu.be/1i03jnNGpyQ · durée 18:19 · résumé Gemini (gemini-3.5-flash-lite) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo, structuré selon tes demandes :

### 1) Idée principale
L’auteur teste et compare le nouveau modèle **Gemini 3.8 Flash** d’OpenAI/Google avec d’autres agents de codage (Claude Fable, Grok). Il met en avant son excellent rapport qualité-prix (environ 5 fois moins cher que Fable Opus pour des performances très proches, voire supérieures sur certains benchmarks de cybersécurité), malgré une consommation de tokens parfois élevée et quelques bizzareries de comportement.

---

### 2) Outils, sites et dépôts GitHub cités
* **Artificial Analysis** (`artificialanalysis.ai`) — *Gratuit* — Site d'analyse comparative des modèles d'IA (intelligence, vitesse, coût).
* **Cursor** (`cursor.com`) — *Payant (modèle freemium/abonnement)* — IDE (environnement de développement) intégrant des agents d’IA pour coder (utilisé pour les tests CursorBench).
* **OpenRouter** (`openrouter.ai`) — *Payant (à l'utilisation)* — Agrégateur d'API permettant d'accéder à différents modèles (Gemini, Grok, Claude) à des tarifs compétitifs (via Google AI Studio Flex/Priority).
* **GitHub (Divers repos de test)** — *Gratuit* — Dépôts utilisés pour exécuter des benchmarks d'agents de codage (ex: `car-crash`, `simulation-life`, `gmail-clone`).

---

### 3) Astuces concrètes et réutilisables
* **Optimiser les coûts d'API :** Utiliser des modèles plus récents et économiques comme Gemini 3.8 Flash via OpenRouter pour réduire drastiquement le coût des tâches de développement (divisé par 3 à 5 par rapport à Claude Opus), tout en gardant un haut niveau de performance.
* **Gérer les agents de codage :** Si un agent de codage (comme Gemini) commence à boucler ou consomme trop de tokens sur une tâche, il est conseillé de l'interrompre et de basculer vers un autre modèle plus efficace (comme Grok ou Claude Fable) selon la complexité du prompt.
* **Surveiller les performances (TPS) :** Utiliser des options comme *Google AI Studio Flex* ou *Priority* pour ajuster la vitesse (tokens par seconde) en fonction de vos besoins de réactivité.

---

### 4) Chiffres de revenus annoncés
* **Non précisé** (La vidéo parle de coûts d'API en dollars et de performances sur des benchmarks de code, mais ne mentionne **aucun chiffre de revenus en euros/dollars gagnés** par l'utilisation de ces outils).
