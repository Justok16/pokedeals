# Créer un jeu vraiment amusant (AUCUNE expérience de codage)

Vidéo : https://youtu.be/aa-Fu5Qw91M · durée 29:23 · résumé Gemini (gemini-3.5-flash, lot de 5) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) Idée principale**
Démonstration complète de la création d'un jeu vidéo web fonctionnel ("Library Survivors") en une journée en combinant ChatGPT pour la conception, Claude Code pour le développement automatisé, Leonardo.ai pour les graphismes 2D et Suno/ElevenLabs pour l'audio.

**2) Outils, sites et dépôts GitHub cités**
*   **ChatGPT (`o3-pro`, `o3`, `gpt-4o`)** : Payant / Gratuit. Utilisé pour concevoir le gameplay, rédigé la documentation et générer le brief technique au format Markdown (`.md`).
*   **Claude Code (`@anthropic-ai/claude-code`)** : Payant (via API Anthropic / abonnement). Agent IA en ligne de commande (CLI) s'exécutant directement dans le terminal pour lire, écrire et exécuter du code dans les dossiers locaux.
*   **Node.js / npm** : Gratuit. Environnement d'exécution nécessaire à l'installation de Claude Code et Vite.
*   **VS Code / Windsurf** : Gratuit / Payant. Éditeurs de code (IDE) utilisés pour exécuter l'extension Terminal de Claude Code.
*   **Vite** : Gratuit. Outil de création et serveur de développement pour applications web JavaScript.
*   **GitHub** : Gratuit / Payant. Service d'hébergement de dépôts Git pour la sauvegarde et le contrôle de version.
*   **Leonardo.ai** : Gratuit / Payant. Générateur d'images IA utilisé avec les modèles `Phoenix 1.0` et `Lucid Realism` ainsi que l'option *Tiling* pour les sprites et textures.
*   **Adobe Photoshop** : Payant. Utilisé pour harmoniser la couleur des vestes des sprites de personnages.
*   **Suno.ai** : Gratuit / Payant. Générateur de musique IA pour créer les bandes-son rétro Lo-Fi.
*   **ElevenLabs** : Gratuit / Payant. Moteur IA utilisé pour générer les effets sonores (bruits de menus, chutes de livres).
*   **Delphi.ai** : Gratuit / Payant (mention personnelle). Outil de création de clones numériques interactifs (texte et voix).

**3) Astuces concrètes et réutilisables**
*   **Workflow de développement par IA** :
    1. Demandez à ChatGPT `o3-pro` de rédiger un cahier des charges complet (`design.md`).
    2. Dans Claude Code, utilisez `Shift + Tab` pour passer en mode "Plan" afin qu'il établisse une feuille de route d'implémentation détaillée (`development_plan.md`).
    3. Passez en mode "Auto-accept edits" et ordonnez à Claude Code de créer la structure du projet avec Vite et de coder le jeu étape par étape.
*   **Résolution automatique de bugs** : En cas de dysfonctionnement dans le navigateur, ouvrez la console développeur (F12), copiez l'intégralité des erreurs/logs et collez-les directement dans Claude Code pour qu'il corrige automatiquement le code source.
*   **Textures de jeu 2D sans raccord** : Dans Leonardo.ai, cochez l'option `Tiling` lors de la génération de parquets ou murs pour obtenir des images parfaitement répétables sans couture visible.
*   **Sécurisation du code** : Effectuez des *commits* et *pushs* réguliers vers GitHub (via l'agent Windsurf Cascade ou Git) avant chaque phase de modification graphique/audio majeure afin de créer des points de restauration.

**4) Chiffres de revenus annoncés**
*   Non précisé.

---
