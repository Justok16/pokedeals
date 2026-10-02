# Actu IA : OpenAI porte un coup majeur à NVIDIA

Vidéo : https://youtu.be/TInwQglNkzo · durée 29:31 · résumé Gemini (gemini-3.7-flash) du 2026-10-02
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo, orienté pour un usage pratique et technique de l’IA :

---

### 1) Idée principale
Cette vidéo est une revue d'actualité hebdomadaire sur l'écosystème de l'intelligence artificielle. Elle met en lumière :
- La montée en puissance spectaculaire des modèles « open-weights » (poids ouverts comme GLM et Qwen) qui rivalisent désormais avec les grands modèles propriétaires fermés à des coûts d'inférence dérisoires.
- L'émergence des agents de code et d'exécution automatisée capables de contrôler des navigateurs ou d'être pilotés à distance (Codex, Claude Cowork/Claude Code, Antigravity).
- L'évolution du matériel permettant de faire tourner de l'IA lourde en local (Apple M5 Ultra, architecture Perplexity Portable Computer).

---

### 2) Outils, sites et dépôts cités

| Nom exact de l'outil / site | Gratuit ou Payant | À quoi il sert |
| :--- | :--- | :--- |
| **OpenAI Jalapeño** | Non commercialisé (*puce interne*) | Puce d'inférence conçue par OpenAI pour réduire sa dépendance envers Nvidia. |
| **Hugging Face** | Gratuit / Options & GPU payants | Plateforme d'hébergement de modèles open-source et location de puissance de calcul GPU. |
| **Vercel AI Gateway** | Gratuit / Payant selon usage | Passerelle de routage et d'analyse du trafic vers différents modèles d'IA. |
| **Artificial Analysis** | Gratuit | Benchmark indépendant comparant l'intelligence et le coût par tâche des modèles d'IA. |
| **BuseyBench** | Gratuit | Benchmark créé par l'auteur évaluant la génération de code SVG par les LLM. |
| **LMSYS Arena (arena.ai)** | Gratuit | Plateforme de test à l'aveugle où les utilisateurs votent pour les meilleurs modèles (texte, vidéo). |
| **GLM-5.3-Flash (Zhipu AI / ZAI)** | Open-weight (Gratuit) / API payante ultra-low cost | Modèle ultra-rapide et économique surpassant des modèles comme Claude Opus 4.8 sur les benchmarks de code (DeepSWE). |
| **Qwen3.8-Flash & Qwen3.8 27B (Alibaba)** | Open-weight (Gratuit) / API payante | Modèles légers et performants pour le code et l'analyse, optimisés pour le cloud ou le local haut de gamme. |
| **Codex** | *Non précisé* (lié aux abonnements OpenAI) | Environnement de développement et d'agents IA pour coder et déployer des applications. |
| **ChatGPT Sites (OpenAI)** | Payant (*plans ChatGPT Plus/Pro/Team*) | Outil intégré créant et hébergeant automatiquement des sites/tableaux de bord interactifs connectés à des données (ex. Google Sheets). |
| **Google AI Studio** | Gratuit (quotas) / Payant à l'usage | Interface développeur pour prototyper et appeler les API des modèles Google. |
| **Google Flow** | Payant (*abonnements Google One AI / Ultra*) | Interface créative pour générer du contenu multimodal chez Google. |
| **Gemini Omni 1.1 Flash** | Payant via API (*ex. 0,10 $ / vidéo 720p*) | Modèle de génération vidéo avec contrôle d'images de début/fin et cohérence temporelle. |
| **Gemini 3.5 Transcribe** | Gratuit sur app / API payante | Modèle de transcription audio (Speech-to-Text) ultra-précis. |
| **Gemini Notebook (ex-NotebookLM)** | Gratuit | Outil d'analyse documentaire permettant désormais d'importer directement des livres achetés sur Google Play Books. |
| **Google Play Books** | Payant (achat au livre) | Librairie d'e-books connectable à Gemini Notebook. |
| **Antigravity** | *Non précisé* | IDE / environnement de code IA proposant une fonction de contrôle à distance via navigateur. |
| **Claude Code & Claude Cowork (Anthropic)** | Payant (*Claude Pro / Max / Team / API*) | Outils d'Anthropic intégrant désormais un navigateur autonome et une mémoire contextuelle persistante. |
| **Claude in Chrome** | Payant (*inclus dans les abonnements Claude*) | Extension Chrome permettant à Claude de lire, résumer et interagir avec les pages web. |
| **Perplexity Portable Computer** | *Non précisé* (Recherche / Open source) | Architecture d'agent local exécutant des petits modèles sur la machine de l'utilisateur avec escalade vers le cloud si nécessaire. |
| **Suno** | Freemium (Gratuit avec crédits / Payant) | Générateur de musique IA à partir de prompts ou d'enregistrements audio importés. |
| **Skild AI (Modèle S1)** | *Non précisé* | Modèle de fondation pour robots apprenant des tâches complexes de 10 min à partir d'une seule vidéo de démonstration. |

---

### 3) Astuces concrètes et réutilisables

1. **Création rapide de micro-SaaS / Tableaux de bord :** Utilisez un outil comme *ChatGPT Sites* dans Codex pour transformer une simple feuille *Google Sheets* en une application web hébergée, stylisée et partageable avec authentification sans coder l'infrastructure.
2. **Réduction drastique des coûts d'inférence en dev :** Privilégiez des modèles compacts open-weight récents comme **GLM-5.3-Flash** pour les tâches d'agent de code : ils offrent des performances quasi identiques aux modèles de pointe fermés pour une fraction du coût.
3. **Pilotage d'agents IA à distance (*Remote Control*) :** Configurez les fonctionnalités d'accès distant (sur Antigravity, Claude Code, Cursor ou Codex) pour faire tourner de longues sessions de code sur un serveur ou un ordinateur fixe et les monitorer/valider depuis un navigateur mobile.
4. **Flux de travail hybride sur Claude :** Élaborez la stratégie et le prompt d'un projet dans l'interface de chat standard de Claude, puis basculez directement sur *Claude Cowork* pour l'exécution technique grâce au système de **mémoire unifiée**.
5. **Création de contenu musical assisté (légal/éthique) :** Au lieu de générer des morceaux 100 % automatisés par prompt, enregistrez vos propres instruments (guitare, clavier) et utilisez Suno pour générer l'accompagnement (batterie/basse) afin de garder un contrôle créatif.

---

### 4) Chiffres de revenus annoncés
- **Revenus personnels / Méthodes de gains :** Aucun chiffre de gains financiers directs n'est mentionné pour l'utilisateur (*Non précisé / La vidéo est un récapitulatif d'actualités technologiques*).

*Données financières et tarifs mentionnés dans les actualités (affirmé par l'auteur) :*
- Rachat potentiel de Hugging Face par Nvidia : **12,9 milliards de dollars** (*affirmé par l'auteur, citant The Information*).
- Financement total de Stability AI : **232 millions de dollars** (*affirmé par l'auteur*).
- Prix du Mac Studio M5 Ultra (256 Go RAM) pour le calcul local : **~10 799 $** (*affirmé par l'auteur*).
- Coût de génération vidéo Gemini Omni 1.1 Flash : **0,10 $** par sortie 720p (*affirmé par l'auteur*).
- Réduction tarifaire de l'API OpenAI GPT-5.6 Sol : **-20 %** pendant 3 mois (*affirmé par l'auteur*).
