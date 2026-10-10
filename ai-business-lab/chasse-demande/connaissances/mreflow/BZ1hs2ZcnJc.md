# Actualités IA : Anthropic Leak nous dévoile l'avenir de l'IA

Vidéo : https://youtu.be/BZ1hs2ZcnJc · durée 31:05 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé des informations utiles de la vidéo pour quelqu'un cherchant à monétiser l'IA, centré sur l'actualité de **Claude Code** et des nouveaux modèles :

---

### 1) Idée principale
La fuite du code source de **Claude Code** a révélé une architecture d’agent « toujours actif » appelée **KAIROS** (fonctionnant en arrière-plan sans intervention humaine pour consolider la mémoire, corriger du code, envoyer des notifications ou interagir avec GitHub). Cela préfigure une nouvelle ère de l’IA proactive (où les agents travaillent pour vous pendant que vous dormez ou travaillez). Par ailleurs, les géants (OpenAI, Google, Alibaba) multiplient les levées de fonds géantes et sortent de nouveaux modèles open source et multimodaux (Gemma 4, Qwen 3.5, etc.) pour automatiser des tâches complexes (code, design, transcription).

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Code** (Anthropic)
    *   *Tarif* : Inclus dans les abonnements Pro / Max (payants).
    *   *Utilité* : Assistant de code en ligne de commande, intègre désormais une fonction « computer use » et des plugins de code.
*   **Recraft V4 / V4 Pro** (Recraft)
    *   *Tarif* : Modèle payant/freemium (fonctionne avec des crédits).
    *   *Utilité* : Générateur d'images et de graphismes vectoriels (SVG) orienté professionnels, respectant le texte et le style artistique.
*   **MAI-Transcribe-1 / MAI-Voice-1 / MAI-Image-2** (Microsoft Foundry)
    *   *Tarif* : Payant (via Microsoft Foundry).
    *   *Utilité* : Modèles de transcription audio, synthèse vocale et génération d’images.
*   **Veo 3.1 Lite / Fast / 3.1** (Google / Gemini API)
    *   *Tarif* : Payant (basé sur la consommation par vidéo, 5 à 40 cents selon la résolution).
    *   *Utilité* : Modèles de génération de vidéo (jusqu'en 4K).
*   **Gmail AI Inbox** (Google)
    *   *Tarif* : Inclus dans le plan Google AI Ultra (environ 250 $ / mois).
    *   *Utilité* : Boîte mail intelligente avec priorisation et briefings personnalisés.
*   **Gemma 4** (Google)
    *   *Tarif* : Gratuit / Open-weight (licence Apache 2.0).
    *   *Utilité* : Grand modèle de langage ouvert, optimisé pour tourner sur appareils Android et GPU de PC portables, idéal pour faire tourner des agents localement.
*   **Qwen 3.5 Omni / Plus** (Alibaba)
    *   *Tarif* : Modèle accessible via API (tarifs variables, certains modèles Open Source à venir).
    *   *Utilité* : Modèle multimodal (texte, image, audio, vidéo) avec une fenêtre de contexte d'un million de tokens, idéal pour créer des applications ou sites web complets à partir d'une description vocale.
*   **Trinity-Large-Thinking** (Arcee)
    *   *Tarif* : Gratuit / Open-weight (licence Apache 2.0).
    *   *Utilité* : Modèle de raisonnement open source pour agents autonomes complexes.
*   **Codex Plugin for Claude Code** (OpenAI)
    *   *Tarif* : Nécessite une clé API OpenAI payante + Claude Code.
    *   *Utilité* : Permet d'intégrer les capacités de Codex (revue de code, délégation de tâches) directement dans l'interface de Claude Code.
*   **ChatGPT pour CarPlay** (OpenAI)
    *   *Tarif* : Inclus dans l'application ChatGPT (iOS 26.4+).
    *   *Utilité* : Permet d'interagir vocalement avec ChatGPT depuis son véhicule.
*   **TBPN (Tech Business Production Network)**
    *   *Statut* : Racheté par OpenAI.
    *   *Utilité* : Réseau de diffusion de podcasts/émissions sur la tech et le business.
*   **Computer for Taxes** (Perplexity)
    *   *Tarif* : Intégré aux services Perplexity (payant).
    *   *Utilité* : Module spécialisé dans l'aide à la déclaration fiscale fédérale américaine et la création de tableaux de bord financiers.
*   **Slackbot / Agentic Slack** (Salesforce / Slack)
    *   *Tarif* : Intégré aux forfaits Business Plus et Enterprise Plus (payant).
    *   *Utilité* : Transforme Slack en un assistant agentique capable de transcrire des réunions (Zoom, etc.), de gérer le CRM et de répondre automatiquement.

---

### 3) Astuces concrètes et réutilisables

*   **Automatisation proactive (Mode Daemon) :** Configurer un agent (type KAIROS ou équivalent en open source) pour qu'il tourne en arrière-plan (sur un serveur local ou dans le cloud) afin de surveiller vos services, de détecter des pannes (ex. : site web down, bugs de code, fautes de frappe sur Stripe) et de les résoudre automatiquement pendant que vous dormez.
*   **Utilisation des modèles Open-Weight (Gemma 4, Trinity) :** Pour les développeurs souhaitant créer des agents locaux sans dépendre d'une API cloud payante, utiliser ces modèles open source légers exécutables sur GPU local ou appareil mobile.
*   **Combinaison d'outils de code :** Utiliser le plugin Codex au sein de l'interface Claude Code pour bénéficier du meilleur des deux mondes (la simplicité d'UI de Claude et la puissance de revue de code de Codex).
*   **Génération d'actifs visuels de production :** Utiliser **Recraft V4 Vector** pour générer des logos, icônes ou illustrations directement exportables en **SVG modifiable** et vectoriel, éliminant le faux rendu vectoriel des autres générateurs d'images.

---

### 4) Chiffres de revenus annoncés (marqués « affirmé par l'auteur »)

*   **OpenAI :**
    *   Levée de fonds : **122 milliards de dollars** (à une valorisation de **852 milliards de dollars**), affirmé par l'auteur d'après le blog d'OpenAI.
    *   Revenus générés : **2 milliards de dollars par mois**, affirmé par l'auteur d'après le blog d'OpenAI.
*   **Sora (OpenAI) :**
    *   Coût de fonctionnement / pertes : **environ 1 million de dollars par jour** (soit plus d'un tiers de milliard par an), affirmé par l'auteur d'après un article du *Wall Street Journal*.
