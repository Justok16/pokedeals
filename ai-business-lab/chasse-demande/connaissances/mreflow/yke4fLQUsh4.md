# Créez une base de connaissances « second cerveau » avec l'IA (étape par étape)

Vidéo : https://youtu.be/yke4fLQUsh4 · durée 33:57 · résumé Gemini (gemini-3-flash-preview) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé de la vidéo pour vous aider à exploiter l'IA (notamment via Codex et l'architecture "LLM Wiki") afin d'optimiser votre productivité ou de créer des services automatisés.

### 1) L’idée principale
L’auteur explique comment construire un **"Second Cerveau" (Second Brain)** automatisé. Ce système centralise toutes vos sources d'informations (transcriptions YouTube, articles, notes de réunion), les fait traiter par une IA (Claude ou GPT-4 via Codex) pour les résumer, les lier entre elles et les organiser dans une base de connaissances interactive. Le but est de ne plus jamais "perdre" une information et de pouvoir "discuter" avec l'ensemble de ses connaissances accumulées.

---

### 2) Outils, sites et dépôts cités
*   **Obsidian (Obsidian.md)** : (Gratuit). Logiciel de prise de notes en Markdown qui sert d'interface visuelle au système.
*   **Obsidian Web Clipper** : (Gratuit). Extension Chrome pour capturer du contenu web et extraire automatiquement les transcriptions de vidéos YouTube.
*   **Codex (par OpenClaw)** : (Gratuit avec limites/Payant). Environnement de développement (IDE) pour l'IA qui permet de manipuler les fichiers et d'automatiser des tâches.
*   **Claude Code (Anthropic)** : (Payant/API). Cité comme l'un des moteurs IA possibles (avec GPT) pour faire fonctionner Codex.
*   **OpenClaw (openclaw.ai)** : (Open-source). Système d'agent IA personnel.
*   **Hostinger** : (Payant). Service d'hébergement proposant un déploiement en un clic de l'agent OpenClaw.
*   **Dépôt GitHub "llm-wiki" d'Andrej Karpathy** : (Gratuit). Modèle d'architecture de fichiers qui sert de base à la structure du système.
*   **Granola** : (Prix non précisé). Outil pour enregistrer et transcrire des notes de réunion.
*   **WisprFlow** : (Prix non précisé). Outil de dictée vocale utilisé pour donner des instructions à Codex.
*   **GitHub** : (Gratuit/Payant). Utilisé pour sauvegarder, historiser et synchroniser le "Second Cerveau".

---

### 3) Astuces concrètes et réutilisables
*   **L'architecture Karpathy** : Organisez vos dossiers en trois couches : `raw` (données brutes), `wiki` (pages générées par l'IA) et `assets` (fichiers joints).
*   **Automatisation du dossier "Raw"** : Programmez une routine (dans Codex) qui vérifie chaque heure si de nouveaux fichiers ont été ajoutés dans le dossier "Raw", les traite, puis les déplace dans un dossier "Processed".
*   **Lien CRM et Journal** : Ne vous contentez pas de stocker des articles. Ajoutez un dossier CRM pour vos contacts et un dossier Journal. Apprenez à l'IA à croiser ces données (ex: "Où ai-je rencontré cette personne ?" ou "Donne-moi des conseils basés sur mes anciennes notes").
*   **Le fichier `AGENTS.md`** : Utilisez ce fichier comme "manuel d'instruction" pour votre IA. C'est ici que vous définissez les règles (ex: "Ajoute toujours le nom de la chaîne YouTube en haut du fichier").
*   **Sauvegarde automatique** : Configurez Codex pour qu'il effectue un "commit" et un "push" sur un dépôt GitHub privé après chaque traitement de données pour garantir la sécurité de vos informations.

---

### 4) Chiffres de revenus annoncés
*   L'auteur affiche brièvement une vignette mentionnant **10 000 $/mois** pour une stratégie de contenu, mais cela n'est pas détaillé comme un revenu direct du système décrit.
*   L'auteur mentionne qu'une de ses vidéos YouTube a généré **40 000 $** (affirmé par l'auteur).
*   Il n'y a **aucun chiffre de revenu spécifique** annoncé pour la revente ou l'exploitation commerciale directe de ce système de "Second Cerveau" dans cette vidéo.
