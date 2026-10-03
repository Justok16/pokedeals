# Pourquoi personne ne parle de ce modèle Google ?

Vidéo : https://youtu.be/Po_Dh7WLgmM · durée 26:29 · résumé Gemini (gemini-3.8-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
L'auteur dénonce l'emballement (« hype ») constant autour des sorties répétées de nouveaux modèles d'IA, dont les gains marginaux ne changent pas le quotidien de la majorité des utilisateurs mais impactent surtout les développeurs. En comparant les derniers modèles présentés (notamment Claude Fable 5.1 d'Anthropic et Gemini 3.8 Flash de Google), il démontre que le modèle le plus intelligent sur le papier n'est pas forcément le plus viable : **Claude Fable 5.1 offre d'excellentes capacités de programmation mais à des coûts prohibitifs** (plus de 100 $ pour coder un prototype de jeu via Claude Code), alors qu'un modèle rapide et moins coûteux comme **Gemini 3.8 Flash atteint un niveau de code presque équivalent pour une fraction du prix et du temps**.

---

### 2) Outils, sites et logiciels cités

* **Claude Code (avec mode « Ultra Code »)**
  * *Statut :* Payant (l'auteur utilise le forfait à 200 $/mois, plus des crédits d'utilisation supplémentaires).
  * *Utilité :* Agent de développement en ligne de commande pour concevoir, coder et tester des applications logicielles complètes de manière autonome.
* **Claude Fable 5.1 & Claude Mythos 5.1 (Anthropic)**
  * *Statut :* Payant (tarification API : 10 $ / million de tokens en entrée, 50 $ / million en sortie). Mythos est restreint à un groupe fermé de partenaires en cybersécurité.
  * *Utilité :* Modèles de langage avancés pour le raisonnement complexe, le codage agentique et l'analyse de vulnérabilités.
* **Gemini 3.8 Flash & Gemini 3.8 Flash Cyber (Google DeepMind)**
  * *Statut :* Payant à l'usage via API (0,75 $ / million de tokens en entrée, 3,75 $ / million en sortie).
  * *Utilité :* Modèles optimisés pour la rapidité, le codage et les tâches agentiques/cybersécurité à bas coût.
* **DeepSWE (deepswe.com)**
  * *Statut :* Gratuit à la consultation.
  * *Utilité :* Benchmark mesurant l'efficacité et le coût par tâche d'agents d'ingénierie logicielle sur des problèmes de code réels.
* **Artificial Analysis (artificialanalysis.ai)**
  * *Statut :* Gratuit à la consultation (propose également une offre Premium payante).
  * *Utilité :* Plateforme d'évaluation comparant l'intelligence globale, le coût réel par tâche (« Cost per task »), le temps d'exécution et la consommation de tokens des modèles IA.
* **BuseyBench (buseybench.com)**
  * *Statut :* Gratuit à la consultation.
  * *Utilité :* Benchmark satirique mesurant la capacité des modèles à générer une illustration SVG précise (visage de Gary Busey), notée par un juge IA avec mesure du coût et du temps de calcul.
* **The Information (theinformation.com)**
  * *Statut :* Payant (site d'actualités sur abonnement).
  * *Utilité :* Cité pour un article révélant la méthode d'entraînement dite de « profondeur récurrente » (*recurrent depth / looped transformer*) testée par OpenAI sur son projet Astra.
* **Megabonk**
  * *Statut :* Gratuit ou payant : non précisé.
  * *Utilité :* Jeu vidéo de type arène/survie pris comme référence pour tester la génération de jeux complets.
* **Ultrabonk**
  * *Statut :* Prototype créé par l'auteur (non commercialisé).
  * *Utilité :* Clone de *Megabonk* généré en un seul prompt pour évaluer les capacités de développement de l'IA.

---

### 3) Astuces concrètes et réutilisables pour le développement et la rentabilité

1. **Calculer la rentabilité au « coût par tâche » plutôt qu'au token brut :**
   Un modèle performant qui boucle longuement sur un problème de code peut consommer un volume massif de tokens de raisonnement. Il faut regarder la dépense totale nécessaire pour finaliser une fonction ou un script.
2. **Se méfier des sessions de codage autonome prolongées dans Claude Code :**
   Lancer une tâche en mode approfondi (« Ultra Code ») peut vider 100 % d'une session d'abonnement et basculer automatiquement sur des crédits d'utilisation payants (114 $ dépensés en une seule session d'environ 1 h 30 pour un seul prototype).
3. **Privilégier les modèles légers/Flash pour le prototypage rapide :**
   Gemini Flash génère un jeu 3D fonctionnel en un seul prompt pour une dépense minime et en 2,5 minutes par tâche (contre plus de 7 minutes pour les modèles haut de gamme), ce qui permet d'itérer à très faible coût avant de recourir à un modèle plus cher pour des bugs complexes.
4. **Exploiter la mise en cache des invites (*Prompt Caching / Cache Reads*) :**
   Sur les modèles qui le supportent, cela permet de réduire jusqu'à 25 % la facture API sur les flux de travail itératifs contenant de longues bases de code répétées.
5. **Préserver l'auditabilité du code :**
   Les techniques d'IA qui masquent la chaîne de pensée (*Chain of Thought*) rendent le débogage et l'analyse de sécurité beaucoup plus difficiles à vérifier par un développeur humain.

---

### 4) Chiffres de revenus annoncés

* **Aucun chiffre de revenus n'est annoncé dans la vidéo** (affirmé par l'auteur : non applicable / non précisé). L'auteur se concentre exclusivement sur les coûts de développement, les tarifs d'API et les performances des modèles, sans aborder de monétisation ou de gains financiers personnels.
