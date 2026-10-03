# J'ai créé un outil pour détecter les vidéos IA (vous pouvez l'utiliser)

Vidéo : https://youtu.be/-KcHn0QcSb0 · durée 20:11 · résumé Gemini (gemini-3.6-flash) du 2026-10-01
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo structuré selon vos critères :

---

### 1) Idée principale
L'auteur cherche à développer une application web (« AI Slop Detector ») permettant de coller le lien d'une vidéo courte (Instagram, TikTok, YouTube, X) afin de déterminer automatiquement si elle a été créée par une IA. En tentant de la développer avec des agents de code IA et divers modèles multimodaux, il réalise que les LLM actuels sont très mauvais pour détecter les vidéos IA. Il doit recourir à une API tierce spécialisée (SightEngine). Finalement, le projet s'avère **financièrement inviable en tant que service gratuit en ligne** en raison du coût très élevé des requêtes API par vidéo. Il choisit donc de partager le code gratuitement sur GitHub pour un usage local.

---

### 2) Outils, sites et dépôts GitHub cités

*   **ChatGPT / Codex (OpenAI)**
    *   *Statut :* Payant (via abonnement / API)
    *   *Rôle :* Brainstorming sur la faisabilité, génération du code complet de l'application (Next.js/React) et exécution de tests automatisés autonomes.
*   **Google Gemini (DeepMind)**
    *   *Statut :* Gratuit / Payant selon l'usage API
    *   *Rôle :* Modèle multimodal utilisé pour analyser le flux vidéo et identifier visuellement les artefacts/anomalies d'IA (s'est révélé peu efficace lors des tests).
*   **Google SynthID**
    *   *Statut :* Gratuit (intégré aux écosystèmes Google)
    *   *Rôle :* Outil de tatouage numérique et de détection d'images/vidéos générées par les IA de Google.
*   **SightEngine API**
    *   *Statut :* Freemium (Gratuit pour 2 000 ops/mois sans analyse vidéo ; Payant de 29 $/mois à 99 $/mois pour l'analyse vidéo)
    *   *Rôle :* API spécialisée dans la modération de contenu et la détection visuelle de médias générés par IA. Utilisée comme moteur principal d'analyse.
*   **GitHub (Dépôt du projet "AI Slop Detector")**
    *   *Statut :* Gratuit
    *   *Rôle :* Hébergement du code source ouvert du projet afin que les utilisateurs puissent le cloner et l'exécuter localement.

---

### 3) Astuces concrètes et réutilisables

*   **Prompting contextuel par lien partagé :** Pour transmettre un cahier des charges complet à un agent de code (Codex), copiez-collez le lien de partage d'une conversation ChatGPT préalable contenant déjà la réflexion d'architecture.
*   **Gestion des désaccords entre IA (Fallback & Priorités) :** Si deux IA donnent des résultats contradictoires (ex: Gemini dit « vidéo réelle » et SightEngine dit « vidéo IA »), intégrez une logique de priorité dans votre code (ex: donner la priorité à l'outil le plus sensible/spécialisé).
*   **Banc de test automatisé (`/goal`) :** Laissez l'agent de code tourner en boucle pendant plusieurs heures avec un jeu de données de test (vidéos réelles vs vidéos IA) pour qu'il ajuste de lui-même la précision de détection.
*   **Calcul de viabilité économique d'un SaaS IA :** Avant de lancer un outil IA gratuit, calculez le coût par requête. L'analyse vidéo découpe le fichier en dizaines d'images (échantillonnage) : une seule vidéo de 45 secondes peut consommer 400 à 800+ opérations d'API, ce qui rend l'accès public gratuit ruineux.
*   **Modèle "Bring Your Own Key" (BYOK) :** Si le coût des API empêche la commercialisation ou la gratuité d'un SaaS, publiez le projet en Open Source sur GitHub en demandant aux utilisateurs d'insérer leurs propres clés d'API dans un fichier `.env.local`.

---

### 4) Chiffres de revenus annoncés

*   **Revenus générés par l'auteur sur ce projet :** Non précisé *(l'auteur n'a pas commercialisé l'application ni cherché à générer de revenus directs avec ce projet)*.
*   **Coûts et métriques consommées (affirmé par l'auteur) :**
    *   Abonnement API SightEngine souscrit : **99 $/mois** (plan Pro incluant 40 000 opérations).
    *   Consommation d'API durant la phase de test : **12 150 opérations** brûlées en scannant seulement une sixaine de vidéos (soit environ 440 à 790 opérations d'API consommées par vidéo analysée).
