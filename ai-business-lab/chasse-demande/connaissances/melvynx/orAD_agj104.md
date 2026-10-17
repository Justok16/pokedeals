# Grok et SpaceX pourraient devenir les meilleurs modèles au monde (mieux que Fable et GPT ?)

Vidéo : https://youtu.be/orAD_agj104 · durée 15:41 · résumé Gemini (gemini-3.7-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur met en avant les performances sous-estimées et le **rapport qualité/prix exceptionnel du modèle Grok 4.5** (développé par xAI / accessible notamment via Cursor) pour le développement et l'automatisation de tâches de programmation (UI/UX, correction de bugs, intégration de fonctionnalités). Il démontre, benchmarks et cas réels à l'appui, que Grok 4.5 produit des résultats comparables aux modèles les plus chers (Claude, GPT) pour une fraction minime de leur coût API.

---

### 2) Outils, sites et dépôts cités

* **Grok 4.5 (xAI)**  
  * **Statut :** Payant (via API xAI ou inclus via un abonnement Cursor).  
  * **Usage :** Modèle d'intelligence artificielle utilisé pour la génération de code, le raisonnement et la création d'interfaces.
* **Cursor**  
  * **Statut :** Freemium / Payant (abonnement payant requis pour l'accès aux quotas de modèles avancés comme Grok 4.5).  
  * **Usage :** Éditeur de code assisté par IA intégrant divers modèles de langage.
* **OpenCodex / Codex**  
  * **Statut :** Non précisé (outil d'interface et agent de code local/proxy montré à l'écran).  
  * **Usage :** Plateforme / interface d'exécution d'agents IA, gestion multi-fournisseurs (xAI, Anthropic, Kimi, Cursor) et suivi des benchmarks.
* **Artificial Analysis (`artificialanalysis.ai`)**  
  * **Statut :** Gratuit / Accès public (avec version Premium optionnelle).  
  * **Usage :** Site de benchmark indépendant comparant les modèles d'IA selon leur intelligence, rapidité et coût par tâche.
* **SaveIt.now (`saveit.now`)**  
  * **Statut :** Freemium / 5 $/mois (Pro).  
  * **Usage :** Application SaaS de gestion de signets/bookmarks basée sur des agents IA (utilisée ici comme cas d'usage pour tester la refonte de landing pages par l'IA).
* **Lumail (`lumail.io`) / Vercel**  
  * **Statut :** Freemium / Payant.  
  * **Usage :** Application web SaaS de newsletter/emailing hébergée sur Vercel, sur laquelle l'auteur teste des modifications de code directes avec Grok 4.5.
* **X (ex-Twitter)**  
  * **Statut :** Gratuit / Freemium (X Premium).  
  * **Usage :** Veille technique et partages de la communauté de développeurs IA.

---

### 3) Astuces concrètes et réutilisables

* **Réduire drastiquement les coûts API de dev :** Pour des modifications précises, des ajustements d'interfaces (CSS/hauteur d'éléments) ou des ajouts de fonctionnalités frontend, basculez sur **Grok 4.5** au lieu d'utiliser systématiquement les modèles les plus onéreux (Claude Opus/Sonnet ou GPT-5/équivalents).
* **Exploiter l'abonnement Cursor :** Utiliser Grok 4.5 directement via l'intégration Cursor permet d'économiser sur les coûts de tokens tout en conservant une bonne vitesse d'exécution.
* **Gestion du niveau de raisonnement (*Effort*) :** Laisser le niveau d'effort sur *Medium* avec Grok 4.5 suffit pour la majorité des tâches courantes de dev sans consommer inutilement de ressources.
* **Workflow d'itération visuelle :** Fournir des captures d'écran et des consignes d'interaction claires à l'agent IA pour qu'il produise le code, vérifie l'UI et valide lui-même le bon fonctionnement (*runtime checks*).

---

### 4) Chiffres de revenus annoncés
* **Revenus personnels / gains :** Aucun chiffre de revenus personnels n'a été annoncé dans la vidéo (*non précisé*).  
* **Tarifs et coûts cités (affirmé par l'auteur) :**
  * Coût de refonte de la landing page par Grok 4.5 : **1,14 $** (contre **~8,59 $ à 8,80 $** pour Claude Fable / GPT).
  * Prix affiché du SaaS SaveIt.now : **5 $/mois**.
