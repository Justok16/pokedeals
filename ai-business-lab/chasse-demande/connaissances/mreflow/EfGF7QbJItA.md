# Actu IA : OpenAI vient de mettre le frein sur l'IA

Vidéo : https://youtu.be/EfGF7QbJItA · durée 32:41 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé complet et structuré de la vidéo, en français :

---

### 1) Idée principale
La vidéo propose un tour d'horizon de l'actualité de l'intelligence artificielle : les avancées de la modélisation 3D par IA (création d'assets pour jeux vidéo), les applications médicales de l'IA (vaccins contre le cancer), la montée en puissance des modèles de langage libres et puissants exécutables localement (comme la série Qwen), ainsi que les nouveaux outils d'automatisation agentique et d'intégration en entreprise (Hyperagent, Slack Code, Cursor, extensions ChatGPT).

---

### 2) Outils, sites et dépôts cités

1. **Tripo AI (Tripo P2.0 Preview)**
   * **Modèle économique :** Gratuit (2 générations offertes) avec offres payantes.
   * **Utilité :** Génère des modèles 3D complets (mesh et textures) à partir d'une image ou d'un prompt texte, exportables vers Blender, Unreal Engine ou pour l'impression 3D.

2. **Hyperagent** *(Sponsor de la vidéo)*
   * **Modèle économique :** Payant (offre de 100 $ de crédits bonus via le lien du créateur).
   * **Utilité :** Plateforme de gestion d'équipes d'agents IA collaboratifs (multi-agents et multi-humains) pour automatiser des flux de travail (ex. génération de B-roll vidéo, prospection).

3. **Qwen 2.5 (Alibaba)** *(mentionné dans la vidéo comme Qwen 27B / Qwen open-weights)*
   * **Modèle économique :** Gratuit (Open-source / Open-weight).
   * **Utilité :** Modèle de langage puissant capable de coder et raisonner, téléchargeable et exécutable hors-ligne sur du matériel grand public (24–32 Go de VRAM/RAM unifiée).

4. **LM Studio**
   * **Modèle économique :** Gratuit.
   * **Utilité :** Application pour ordinateur permettant de télécharger, quantifier et exécuter localement des LLMs avec interface de discussion et serveur API local compatible OpenAI.

5. **Hugging Face**
   * **Modèle économique :** Gratuit (avec options payantes d'hébergement).
   * **Utilité :** Dépôt communautaire pour télécharger les versions quantifiées (GGUF, MLX) de modèles ouverts comme Qwen.

6. **OpenRouter**
   * **Modèle économique :** Payant à l'usage (par jeton).
   * **Utilité :** Routeur d'API pour exécuter divers LLMs dans le cloud.

7. **BuseyBench**
   * **Modèle économique :** Gratuit / En ligne.
   * **Utilité :** Outil de benchmark mesurant la capacité des LLMs à générer des illustrations vectorielles en SVG.

8. **Hermes (Nous Research)**
   * **Modèle économique :** Gratuit / Open-source.
   * **Utilité :** Harnais / interface agentique capable de piloter des modèles locaux (via LM Studio) pour concevoir des plans d'action, écrire et exécuter du code étape par étape de manière similaire à Codex ou Claude Code.

9. **ChatGPT pour Mac (OpenAI)**
   * **Modèle économique :** Gratuit avec options payantes (Plus/Team/Pro).
   * **Utilité :** Intègre les nouvelles fonctionnalités *Computer History* (suivi d'activité pour mémoriser et automatiser les tâches) et le plugin *Apple Messages* (lecture, rédaction et envoi de SMS/iMessages).

10. **Meta AI App (macOS)**
    * **Modèle économique :** Gratuit.
    * **Utilité :** Application de bureau dédiée pour interagir avec les modèles Llama, générer des images et planifier des tâches.

11. **Perplexity Brain**
    * **Modèle économique :** Inclus dans Perplexity (Gratuit / Pro payant).
    * **Utilité :** Système de mémoire agentique et wiki de connaissances sous forme de graphe relationnel pour organiser le travail et les recherches.

12. **Google Gemini**
    * **Modèle économique :** Gratuit / 1 an offert pour les étudiants éligibles.
    * **Utilité :** LLM et génération multimédia ; propose désormais une option pour désactiver le filigrane visible sur les médias générés.

13. **HappyShrimp 1.0 (Alibaba Cloud)**
    * **Modèle économique :** Bêta (Gratuit / Non précisé pour la suite).
    * **Utilité :** Modèle d'IA de génération de musique complète à partir de prompts textuels (concurrent de Suno).

14. **Origin (par Cursor)**
    * **Modèle économique :** Inclus dans les forfaits Cursor payants (en accès anticipé).
    * **Utilité :** Hébergement de dépôts de code concurrent de GitHub, conçu pour faciliter l'interaction des agents de développement.

15. **Slack Code (Salesforce)**
    * **Modèle économique :** Non précisé (fonctionnalité intégrée à Slack).
    * **Utilité :** Intégration d'agents de développement (Claude, Codex, etc.) directement dans les canaux Slack pour coder de manière collaborative avec les équipes humaines.

---

### 3) Astuces concrètes et réutilisables (notamment pour du travail avec le code et l'IA)

* **Exécuter un agent de code localement sans coût d'API :** Associez **LM Studio** (faisant tourner un modèle de code ouvert comme *Qwen 27B*) à un harnais agentique comme **Hermes**. Cela permet d'avoir un agent autonome qui planifie, rédige et corrige du code directement sur votre machine sans payer d'abonnements API.
* **Génération rapide d'assets 3D pour jeux vidéo / impression 3D :** Utilisez des générateurs d'images IA pour créer un concept art (idéalement en pose neutre / T-pose avec vêtements distincts), puis importez-le dans **Tripo AI** pour obtenir un maillage 3D texturé prêt à l'emploi.
* **Automatisation des tâches répétitives sur macOS :** Si vous utilisez l'application bureau de ChatGPT, activez l'option *Computer History* pour analyser vos workflows récurrents (documents ouverts, navigateurs, projets) et demander à l'IA de générer des scripts ou compétences d'automatisation sur mesure.
* **Collaboration d'agents dans la communication d'équipe :** L'intégration de canaux de code IA (comme dans Slack ou Hyperagent) permet de déléguer des tâches de maintenance, tests ou revue de code sans sortir de votre environnement de travail habituel.

---

### 4) Chiffres de revenus annoncés

* **Revenus :** Non précisé (la vidéo est un résumé d'actualités technologiques et ne présente aucune méthode ni aucun chiffre de revenus ou de gains financiers personnels).
