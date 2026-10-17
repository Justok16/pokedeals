# 27 choses gratuites que vous pouvez faire avec Gemini

Vidéo : https://youtu.be/sXamQXKgSeU · durée 27:52 · résumé Gemini (gemini-3.8-flash) du 2026-09-30
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé détaillé et fidèle de la vidéo, structuré selon vos consignes :

---

### 1) Idée principale
La vidéo montre comment exploiter les fonctionnalités avancées de l'écosystème d'intelligence artificielle de **Google (Google AI Studio, Gemini, NotebookLM)**, qui sont pour la plupart accessibles **gratuitement**, alors que des concurrents comme OpenAI (ChatGPT) et Anthropic (Claude) imposent des abonnements payants de plus en plus onéreux. L'auteur illustre concrètement la création d'applications, le tutorat vidéo en direct avec partage d'écran, l'analyse multimodale de vidéos, la génération audio/voix, la création de visualisations de données et la recherche approfondie.

*(Note : Claude Code n'est pas abordé dans cette vidéo ; seul le nom Claude est mentionné au tout début pour souligner l'augmentation du coût de ses offres).*

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit ou payant | À quoi il sert |
| :--- | :--- | :--- |
| **Google AI Studio** (`aistudio.google.com`) | **Gratuit** | Environnement de développement et prototypage des modèles Gemini : génération de code d'applications/jeux en un prompt, analyse multimodale, streaming d'écran/webcam en direct, génération de voix/images. |
| **Google Gemini** (`gemini.google.com`) | **Gratuit** *(propose aussi un abonnement payant Google AI Pro)* | Interface de chat IA de Google permettant l'analyse, le brainstorming, la génération d'images, la recherche documentaire poussée (« Deep Research ») et la création d'applications/graphiques interactifs via « Canvas ». |
| **NotebookLM** | **Gratuit** | Outil Google de gestion de connaissances permettant d'importer des documents/liens/vidéos et de générer des résumés, mind maps ou un podcast audio animé par deux voix IA (« Deep Dive conversation »). |
| **Veo 3** | **Payant** *(20 $/mois pour Google AI Pro, ou 250 $/mois pour l'offre Ultra)* | Modèle de génération de vidéos par IA développé par Google, capable de générer la vidéo et les effets sonores natifs. |
| **Perplexity / @AskPerplexity** | **Gratuit** *(sur X.com lors de l'enregistrement)* | Bot IA sur la plateforme X permettant de générer gratuitement des vidéos avec Veo 3 via un simple tweet. |
| **Imagen** | **Gratuit** *(intégré dans Google AI Studio)* | Modèle de génération et d'édition d'images par prompt textuel. |
| **ElevenLabs** | Payant / Freemium (*non précisé dans la vidéo*) | Modèle externe cité en comparaison pour la synthèse vocale (text-to-speech). |
| **ChatGPT** | Freemium / Payant | Modèle d'OpenAI cité pour comparaison de coûts et de fonctionnalités. |
| **Claude** | Freemium / Payant | Modèle d'Anthropic cité pour comparaison de coûts (*Claude Code non mentionné*). |
| **Feedly** | *Non précisé* | Agrégateur de flux RSS utilisé comme modèle d'application à cloner. |
| **DaVinci Resolve** | *Non précisé* | Logiciel de montage vidéo utilisé pour la démonstration de l'assistance en direct par partage d'écran. |
| **YouTube** (`youtube.com`) | **Gratuit** | Hébergeur vidéo dont les URLs sont importées dans AI Studio pour analyse visuelle ou transcription. |
| **X** (`x.com`) | **Gratuit** | Réseau social utilisé pour appeler le bot `@AskPerplexity`. |
| **FutureTools.io** | **Gratuit** (*non précisé pour options payantes*) | Répertoire d'outils IA administré par l'auteur (Matt Wolfe). |

*(Aucun dépôt GitHub n'est cité).*

---

### 3) Astuces concrètes et réutilisables

1. **Créer une application ou un jeu en un seul prompt :**
   * Rendez-vous sur `aistudio.google.com` > onglet **Build** (icône de pièce de puzzle).
   * Décrivez une mécanique de jeu ou téléchargez la capture d’écran d’un logiciel existant (ex. : Feedly) : l'outil génère l'architecture, écrit le code React/TypeScript et corrige automatiquement ses propres bugs.
2. **Obtenir une assistance pas-à-pas en direct avec partage d'écran :**
   * Dans Google AI Studio, onglet **Stream Realtime** > cliquez sur **Share Screen** ou **Webcam**.
   * L'IA voit votre écran ou vos objets en temps réel et peut vous guider vocalement pour réaliser des manipulations complexes dans des logiciels comme DaVinci Resolve.
3. **Analyse visuelle pure de vidéos YouTube :**
   * Collez l'URL d'une vidéo YouTube directement dans l'invite d'AI Studio : l'IA regarde les images de la vidéo (multimodalité réelle) sans se limiter à la transcription audio (utile pour détecter des mèmes, objets, éléments graphiques à des timestamps précis).
4. **Contourner la limite de tokens sur les longues vidéos :**
   * Pour une vidéo trop longue (> 1h20 / > 1 million de tokens), extrayez et collez la transcription brute dans AI Studio : cela fait chuter la consommation à environ 22 000 tokens et permet d'extraire des synthèses complètes et des listes à puces en quelques secondes.
5. **Génération de dialogues multi-intervenants gratuite :**
   * Dans AI Studio > **Create Generative Media** > **Gemini speech generation**, configurez des scripts à plusieurs voix en attribuant des timbres et des tons spécifiques (joyeux, colérique, etc.) pour créer des voix off de haute qualité sans payer ElevenLabs.
6. **Création de visualisations et cartes interactives :**
   * Dans `gemini.google.com`, activez l'option **Canvas** et demandez une carte ou un graphique interactif (ex. : carte de la population mondiale). L'outil génère une interface dynamique manipulable à la souris.
7. **Production de podcasts automatisés avec NotebookLM :**
   * Importez vos documents, pages web ou vidéos dans `notebooklm.google.com`, puis lancez l'**Audio Overview** pour obtenir un podcast naturel à deux voix récapitulant le sujet (idéal pour tester des formats de contenu sans enregistrement studio).
8. **Accéder gratuitement au générateur vidéo Veo 3 :**
   * Sur X (Twitter), créez un post taguant `@AskPerplexity` suivi de votre prompt vidéo (ex. : « *Make me a video of...* ») pour générer une vidéo gratuitement sans souscrire aux forfaits payants de Google.

---

### 4) Chiffres de revenus annoncés

* **Chiffres de revenus annoncés :** **non précisé**. L'auteur ne divulgue ni ne revendique aucun chiffre de revenus personnels ou de gains financiers dans cette vidéo.
