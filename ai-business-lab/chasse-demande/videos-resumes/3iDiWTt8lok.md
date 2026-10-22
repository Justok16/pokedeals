# Vidéo du 05/10/2026 : Jev + Claude (https://youtu.be/3iDiWTt8lok)

Résumé Gemini (gemini-3.7-flash), non vérifié : les chiffres sont ceux affirmés par l'auteur.

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’auteur présente **Jev** (développé par TypeSafe), un modèle d’IA ultra-léger et spécialisé dans la prise de décision rapide (sélection de choix prédéfinis, scores, vrai/faux) plutôt que dans la génération de texte. Il est présenté comme étant jusqu'à 200 fois plus rapide et 400 fois moins cher que les LLM traditionnels. L'objectif est d'utiliser Jev en combinaison avec des outils comme **Claude** et **Claude Code** pour réduire drastiquement les coûts de tokens, accélérer les flux de travail et créer des produits ou services d'agents IA rentables à vendre à des entreprises.

---

### 2) Outils, sites et dépôts cités

*   **Jev (TypeSafe)** : Modèle de décision/classification ultra-rapide (choix multiples, scores, booléens).  
    *Statut :* Payant à l'usage via API (coût minime : fractions de centime par appel).
*   **OpenRouter.ai** : Plateforme d'agrégation d'API utilisée pour se connecter à Jev.  
    *Statut :* Payant à l'usage.
*   **Claude / Claude Code (Anthropic)** : Modèles de langage et environnement agentique/CLI servant à coder les scripts, extensions et agents.  
    *Statut :* Payant (abonnement / crédits API).
*   **Google Sheets** : Tableur utilisé pour catégoriser des données (ex. dépenses bancaires) via un plugin généré par Claude.  
    *Statut :* Gratuit (avec options payantes Workspace).
*   **Meta Ad Library** : Répertoire publicitaire de Meta servant à espionner et analyser les publicités des concurrents.  
    *Statut :* Gratuit.
*   **Apify** : Plateforme de web scraping utilisée pour extraire les commentaires de vidéos (ex. TikTok).  
    *Statut :* Freemium / Payant.
*   **Obsidian** : Outil de prise de notes ("second brain") pour créer des liens automatiques entre pages.  
    *Statut :* Gratuit (options de synchronisation payantes).
*   **Shopify** : Plateforme e-commerce (cas d'usage : maillage interne d'articles de blog).  
    *Statut :* Payant.
*   **Unclutter** : Extension Chrome open-source pour masquer les bannières et publicités gênantes.  
    *Statut :* Gratuit / Open source (*« BYOK, open source + free »*).
*   **Gemini Flash-Lite (Google)** : Modèle d'IA très économique pour générer des légendes d'images avant indexation.  
    *Statut :* Payant à l'usage (quelques centimes pour 1 000 images).
*   **ShipWithJev.com** : Répertoire listant plus de 600 cas d'usage et projets créés avec Jev.  
    *Statut :* Gratuit d'accès.
*   **Decisions API / Luna (OpenAI)** : API de décision concurrente lancée lors du DevDay d'OpenAI.  
    *Statut :* *Non précisé* (l'auteur indique : *« Pricing is still unknown »*).
*   **The RoboNuggets Community (hébergée sur Skool)** : Communauté privée de l'auteur Jay Enriquez dédiée à la vente de services d'agents IA (*Agents-as-a-Service*).  
    *Statut :* Payant (*non précisé dans la vidéo pour le tarif exact*).

---

### 3) Astuces concrètes et réutilisables

1. **Filtrage en amont (*Pre-filtering*) :** Placer Jev devant une boîte de réception e-mail ou un service client. Jev trie les requêtes (spam, facturation, questions) en quelques millisecondes ; seuls les messages nécessitant une vraie réponse sont envoyés à un LLM coûteux (Claude Sonnet/Opus), économisant plus de 90 % des coûts d'API.
2. **Routage de modèles (*Model Routing*) :** Créer une commande de routage (ex. `/jev on`) pour évaluer la difficulté d'une invite utilisateur et l'adresser automatiquement au bon modèle (Haiku pour une recherche simple, Opus pour une tâche d'architecture de données).
3. **Sélection d'outils dans Claude Code (*Skill Picker*) :** Quand un agent dispose de plus de 100 compétences/fonctions, utiliser Jev pour déterminer l'outil à charger en quelques millisecondes au lieu de forcer le LLM principal à relire l'ensemble des descriptions.
4. **Détection d'intention d'achat sur les réseaux :** Extraire les commentaires de posts sociaux de concurrents avec Apify, puis utiliser Jev pour isoler les prospects indiquant une intention d'achat (*« Ready to buy »*) afin de générer des leads qualifiés.
5. **Seuils de confiance et arbitrage humain :** Configurer Jev pour retourner un score de confiance (ex. renvoyer à un agent humain ou à un LLM plus puissant dès que le score passe sous les 60 %).
6. **Calibration par set de validation :** Valider les prompts de classification sur un échantillon de 100 à 200 exemples étiquetés à la main pour mesurer la précision avant de déployer en production.
7. **Création d'extensions Chrome personnalisées :** Demander à Claude de coder des extensions de navigateur (filtrage du contenu indésirable sur X/LinkedIn, analyse de pubs Meta, surlignage sémantique à la place de *Ctrl+F*).

---

### 4) Chiffres de revenus annoncés

*(Chiffres issus des témoignages de membres de la communauté montrés à l'écran, **affirmé par l'auteur**)* :
*   **30 000 $** : Montant d'un contrat de création d'application signé par un membre (*Martin*).
*   **2 000 $ de mise en place + 500 $/mois d'abonnement récurrent** : Montant obtenu auprès d'un premier client par un membre (*Ryan*) pour des agents IA.
*   **40 000 $** : Montant d'un projet délivré à un client par un membre (*Mark*).
