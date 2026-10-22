# Formation Codex CLI : Prendre en main codex en moins de 10 minutes

Vidéo : https://youtu.be/fRerO1UFupg · durée 19:51 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** :
Une présentation détaillée de **Codex CLI**, l'agent de code propulsé par OpenAI, son installation, son intégration avec les abonnements ChatGPT Plus/Pro, ses différents niveaux de raisonnement (modèles `gpt-5-codex`), l'utilisation du fichier `agents.md` pour le contexte, et un comparatif de ses fonctionnalités face à Claude Code et Cursor CLI.

2) **Outils, sites ou dépôts GitHub cités** :
* **Codex CLI (`@openai/codex`)** : Agent de code en ligne de commande d'OpenAI. Gratuit à l'installation, mais l'utilisation nécessite un abonnement ChatGPT Plus/Pro ou une clé API payante.
* **ChatGPT Plus / Pro** : Abonnements OpenAI permettant d'accéder à Codex gratuitement ou via quotas. Payant (20$ ou 200$/mois selon les plans mentionnés dans la vidéo).
* **VS Code / Cursor** : Éditeurs de code compatibles avec l'extension Codex. Gratuits (avec options payantes pour Cursor).
* **GitHub** : Plateforme de code (mentionnée pour les dépôts). Gratuit / Payant.
* **Aibluprint.dev / ai** : Site de formation mentionné à la fin. Payant (formation).

3) **Astuces concrètes et réutilisables** :
* Installer Codex CLI globalement via la commande `npm install -g @openai/codex` et se connecter avec son compte ChatGPT ou sa clé API OpenAI.
* Utiliser la commande `/init` pour générer un fichier `agents.md` (le fichier de configuration et de prompt système) qui sert de guide contextuel à l'IA pour tout le projet.
* Choisir le modèle et le niveau de raisonnement adapté (`low`, `medium`, `high`) via `/model` pour équilibrer la précision du code et la consommation de tokens.
* Configurer les modes d'approbation (`Read Only`, `Auto`, `Full Access`) pour autoriser ou restreindre l'autonomie de l'agent dans l'exécution de commandes et la modification de fichiers.

4) **Chiffres de revenus annoncés** :
* « **$29** » ou « **$10** » / mois (Abonnement ChatGPT Plus mentionné).
* « **$200** » / mois (Abonnement ChatGPT Pro mentionné).
*(Ces chiffres concernent les tarifs des abonnements OpenAI requis pour utiliser l'outil, et non un revenu généré).*

---
