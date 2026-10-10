# Kimi 3 : Aussi bon que FABLE mais OpenSource ?

Vidéo : https://youtu.be/VjbCEla2mlw · durée 24:30 · résumé Gemini (gemini-3.7-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
La vidéo présente et teste en conditions réelles le modèle open-weight / open-source **Kimi K3** (développé par Moonshot AI). L'auteur l'intègre directement dans le terminal via l'outil d'agent **Claude Code** pour évaluer ses capacités sur la création d'interfaces complexes, la simulation web et le développement backend sur un SaaS réel. Bien que Kimi K3 fournisse des interfaces soignées et un code de très haute qualité grâce à des cycles intenses d'auto-vérification, il reste ralenti par une vitesse de génération (tokens/s) faible et une forte consommation de tokens de raisonnement.

---

### 2) Outils, sites et dépôts cités

* **Kimi K3 / Kimi AI (Moonshot AI)** : Modèle open-source de 2,8 trillions de paramètres avec raisonnement poussé et multimodal. Accessible via abonnement web (Vivace) ou par API payante au token.
* **Claude Code** : Outil CLI en ligne de commande développé par Anthropic servant d'agent de développement logiciel autonome (payant à l'usage via crédits/API).
* **Next.js AI Agent Evaluations (`nextjs.org/eval`)** : Site officiel d'évaluation comparative des agents IA sur les tâches et migrations Next.js (gratuit à la consultation).
* **Artificial Analysis (`artificialanalysis.ai`)** : Plateforme d'analyse et de benchmark indépendant mesurant l'intelligence, la vitesse et le coût des modèles IA (accès gratuit / options pro).
* **OpenRouter (`openrouter.ai`)** : Plateforme d'agrégation d'API de modèles IA pour comparer les prix, latences et débits (payant à l'usage).
* **HTTPie** : Outil / client d'envoi et de test de requêtes HTTP et API REST (gratuit / freemium).
* **Site de l'auteur (`code.melvynx.dev`)** : Site mentionné pour retrouver les prompts et benchmarks de test (accès gratuit / non précisé).
* **APEX** : Workflow/système d'agent et de sous-agents utilisé dans le terminal pour planifier, exécuter et auditer des modifications de code (statut de distribution : non précisé).
* **Lumail / Luma Mail** : Application SaaS de messagerie développée par l'auteur, utilisée comme projet de test (propriétaire / non précisé).

---

### 3) Astuces concrètes et réutilisables

* **Connecter des modèles tiers à Claude Code** : Vous pouvez configurer des alias de terminal (ex. `cckimi`) en pointant les variables d'environnement (`ANTHROPIC_BASE_URL`, clé API personnalisée) vers une passerelle compatible afin d'utiliser la puissance ergonomique de Claude Code avec des modèles open-source plus abordables.
* **Verrouiller le périmètre de travail de l'agent** : Toujours spécifier dans les prompts une règle stricte d'isolation (ex. *« Work only inside the current directory »*) pour empêcher l'agent d'explorer l'arborescence globale, ce qui évite la triche sur les benchmarks et réduit drastiquement le gaspillage de tokens de contexte.
* **Exploiter l'auto-vérification pour les tâches UI/Design** : Les modèles à long temps de réflexion comme Kimi K3 relisent et corrigent spontanément leur CSS/Tailwind et la réactivité mobile (jusqu'à 50 % du temps passé en vérification), ce qui produit des interfaces plus abouties du premier coup sans intervention manuelle.
* **Arbitrage coût / temps d'inférence** : Un modèle dont le tarif facial au million de tokens est bas peut coûter autant qu'un grand modèle propriétaire s'il consomme 2 à 3 fois plus de tokens de réflexion et prend plus de temps d'exécution. Il convient d'évaluer le coût total par tâche plutôt que le simple prix du token.

---

### 4) Chiffres de revenus annoncés

* Aucun chiffre de gain, de chiffre d'affaires ou de revenu financier n'a été annoncé dans cette vidéo *(affirmé par l'auteur : non précisé / aucun montant mentionné)*. 
*(Note : les seuls montants financiers évoqués concernent les coûts d'appels API des modèles, oscillant entre ~1 $ et 11 $ par tâche).*
