# LE TUEUR DE FABLE EST SORTI : les Japonais bombardent tout

Vidéo : https://youtu.be/K1ej_A7NTaY · durée 15:35 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) L'idée principale
L'auteur teste et évalue un nouveau système multi-agents japonais, **Sakana Fugu (Fugu Ultra)**, qui orchestre plusieurs grands modèles de langage (LLM) sous une seule API compatible OpenAI. Il compare ses capacités de génération de code et d'interfaces web à celles d'autres modèles (notamment GPT et Fable). Bien que le modèle montre des résultats corrects sur certaines retouches de code, l'auteur conclut que l'abonnement actuel ($20/mois) impose des quotas de requêtes beaucoup trop restrictifs et coûteux par rapport aux offres directes de Claude ou OpenAI, rendant son utilisation peu rentable pour l'instant. En parallèle, il montre comment automatiser la création de présentations marketing à partir d'un simple lien grâce à un connecteur IA.

---

### 2) Outils, sites ou dépôts GitHub cités

* **Sakana Fugu / Sakana Fugu Ultra (sakana.ai)**
  * *Modèle économique :* Payant (formule Standard testée à 20 $ / mois ; accès API payant).
  * *Utilité :* Orchestrateur multi-agents agissant via une API unique compatible OpenAI, qui répartit dynamiquement les tâches complexes (code, raisonnement, finance, etc.) vers un pool de modèles (GPT, Claude Opus, Gemini et modèles internes). Nécessite un VPN hors d'Europe pour s'inscrire (bloqué en UE/Suisse pour raisons de conformité/GDPR).
* **Gamma (gamma.app)**
  * *Modèle économique :* Freemium (offre gratuite avec solde de crédits de départ, ex. 246 crédits montrés ; formules payantes pour recharger ou lever les limites).
  * *Utilité :* Générateur de présentations, documents et pages web assisté par IA. Dans la vidéo, il est connecté directement comme outil/connecteur à Claude pour générer un jeu de diapositives complet à partir de la simple URL d'une page de vente.
* **Claude / Claude Code (Anthropic)**
  * *Modèle économique :* Freemium / Payant (abonnement mensuel).
  * *Utilité :* Assistant de développement IA et environnement dans lequel l'auteur configure des connecteurs externes (via les paramètres de fonctionnalités / connectors).
* **CodeLynx / code.melvyn.dev**
  * *Modèle économique :* Formations payantes (AI Builder) ; bibliothèque de prompts de test en ligne (gratuité/tarification exacte de la section prompt non précisée).
  * *Utilité :* Plateforme de l'auteur servant de base de test SaaS, ainsi que de bibliothèque publique de prompts de référence de développement (ex. prompt de benchmark `timezone-checker`).
* **Vite**
  * *Modèle économique :* Gratuit et open source.
  * *Utilité :* Outil de build et serveur de développement local rapide pour lancer des projets web (ex. application de test du fuseau horaire).
* **Next.js**
  * *Modèle économique :* Gratuit et open source.
  * *Utilité :* Framework web React utilisé pour la plateforme SaaS de l'auteur.
* **OpenRouter (openrouter.ai)**
  * *Modèle économique :* Payant à l'usage des API.
  * *Utilité :* Agrégateur d'API LLM montré brièvement lors de la recherche des tarifs de Sakana Fugu.
* **Excalidraw (excalidraw.com)**
  * *Modèle économique :* Gratuit en version web de base (options payantes d'équipe non précisées).
  * *Utilité :* Tableau blanc virtuel utilisé à la fin de la vidéo pour schématiser la progression des modèles sur un graphique.
* **Ghostty**
  * *Modèle économique :* Gratuit et open source.
  * *Utilité :* Émulateur de terminal utilisé par l'auteur pour exécuter ses lignes de commande et serveurs locaux.

---

### 3) Astuces concrètes et réutilisables

* **Intégration d'outils tiers dans Claude via les connecteurs :** Dans les réglages de Claude (`Capabilities > Connectors > Add > Browse connectors`), connectez des outils comme **Gamma**. Vous pouvez ensuite lui fournir une simple URL et lui demander : *« Crée une nouvelle présentation Gamma super stylé sur [URL] et fais une présentation complète de [projet] »* pour obtenir un diaporama complet structuré avec images et textes sans effort manuel.
* **Méthode de prompt avec spécifications techniques complètes pour le code :** Plutôt que de donner des instructions vagues, utilisez un prompt de référence structuré (comme le prompt `timezone-checker`) qui définit clairement les objectifs, les modes d'affichage, la compatibilité responsive, la persistance locale (`localStorage`) et le formatage des données.
* **Ajustement d'interface par injection d'images :** Lorsque le modèle IA échoue à reproduire un élément complexe d'interface (comme un sélecteur multiple de produits avec logos), envoyez directement une capture d'écran de l'interface souhaitée ou similaire en accompagnement du prompt pour guider visuellement la génération du composant.
* **Attention aux quotas des modèles tiers :** Vérifiez systématiquement les limites d'utilisation (limites sur 5 heures et limites hebdomadaires) avant de baser un flux de travail de production sur des API tierces/orchestrateurs émergents, car le coût en tokens (notamment via le caching et les sous-appels d'agents) peut épuiser un forfait mensuel en quelques tests.

---

### 4) Chiffres de revenus annoncés

*(Tous les chiffres ci-dessous sont marqués **affirmé par l'auteur** / visibles sur ses supports)* :

* **Tableau de bord de l'auteur (CodeLynx) :**
  * Chiffre d'affaires total affiché : **740 116,99 €** *(affirmé par l'auteur)*.
  * Revenu du mois de juin affiché : **2 929,50 €** *(affirmé par l'auteur)*.
* **Exemple d'étudiant sur la diapositive de formation (Yannis) :**
  * **50 000 € générés** et **5 000 € de MRR** (revenu récurrent mensuel) atteint *(affirmé par l'auteur)*.
