# Claude Code veut remplacer OpenClaw : LEUR NOUVEAU TOOLS

Vidéo : https://youtu.be/h4xp2BthaFo · durée 18:44 · résumé Gemini (gemini-3.6-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé de la vidéo structuré selon vos critères :

---

### 1) Idée principale
La vidéo compare **Claude Code Dispatch / Cowork** (l'assistant d'Anthropic contrôlant votre ordinateur local sous votre supervision stricte) à un agent autonome comme **OpenClaw** hébergé sur un serveur VPS à distance. L'auteur explique que pour automatiser efficacement des tâches complexes 24h/24 (ex. télécharger des vidéos, transcrire de l'audio, gérer des fichiers, exécuter des tâches planifiées), utiliser un agent en cloud autonome sur VPS via Telegram est bien plus puissant et flexible que la solution locale d'Anthropic limitée par des demandes de permissions constantes.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Code / Dispatch / Cowork (Anthropic)**
    *   **Statut :** Payant (Abonnement Claude Pro / Team ou consommation API).
    *   **À quoi il sert :** Assistant IA sur Mac/PC capable d'interagir avec les applications et le navigateur web localement, mais restreint par un bac à sable et des demandes de validation répétées.
*   **OpenClaw (OpenClawPro / SteveClaw / ClawBot)**
    *   **Statut :** Gratuit / Open-source (nécessite un serveur VPS payant pour tourner).
    *   **À quoi il sert :** Agent IA autonome installé sur un serveur cloud, contrôlable par Telegram, exécutant des commandes terminal, des scripts bash, et gérant des fichiers sans restrictions d'environnement local.
*   **Hetzner**
    *   **Statut :** Payant (environ 20 $/mois pour la configuration VPS présentée : 8 vCPU, 16 Go RAM, 300 Go SSD).
    *   **À quoi il sert :** Hébergeur cloud économique utilisé pour faire tourner le VPS et exécuter l'agent IA en continu.
*   **Telegram**
    *   **Statut :** Gratuit.
    *   **À quoi il sert :** Interface de messagerie sur smartphone/ordinateur pour piloter l'agent OpenClaw à distance à n'importe quel moment.
*   **Dépôts GitHub (`openclaw-config` / `openclawpro`)**
    *   **Statut :** Gratuit / Open-source.
    *   **À quoi il sert :** Dépôt de configuration et de sauvegarde où l'agent OpenClaw enregistre sa mémoire continue, ses règles (`AGENTS.md`), ses compétences (`skills`) et commite automatiquement ses changements d'organisation du workspace.
*   **`yt-dlp` / `ffmpeg` / `fx-twitter`**
    *   **Statut :** Gratuit (outils CLI open-source).
    *   **À quoi il sert :** Outils en ligne de commande installés sur le VPS permettant à l'agent d'extraire les vidéos X/Twitter, d'en découper l'audio et de générer des images/frames.
*   **OpenAI Whisper API**
    *   **Statut :** Payant (à la consommation API par minute).
    *   **À quoi il sert :** Service de transcription utilisé par l'agent pour convertir la bande audio des vidéos extraites en texte brut.
*   **Site `mlv.sh` / `codelyne.dev` (`mlv.sh/fo`)**
    *   **Statut :** Gratuit (formation / script d'installation promotionnel).
    *   **À quoi il sert :** Page de l'auteur proposant un script d'installation en une ligne ("one-shot") et un guide vidéo pour configurer OpenClaw sur un VPS Hetzner avec Telegram.

---

### 3) Astuces concrètes et réutilisables

*   **Découpler l'agent IA de votre machine personnelle :** Faire tourner votre agent IA sur un VPS externe plutôt que sur votre ordinateur portable permet au bot de continuer à travailler (téléchargements, scraping, rendus, crons) même si votre ordinateur est fermé ou sans connexion Wi-Fi.
*   **Conserver une mémoire persistante par versioning Git :** Liez votre agent IA à un dépôt GitHub (`AGENTS.md`, `MEMORY.md`). À chaque fois que vous donnez une consigne d'organisation (ex. *"range toujours les fichiers PDF et vidéos dans le dossier Documents/ et garde la racine propre"*), demandez-lui d'enregistrer cette règle dans son fichier de mémoire.
*   **Créer des compétences ("Skills") réutilisables :** Quand l'IA trouve la solution à un problème complexe (ex. contourner un blocage pour télécharger une vidéo Twitter), faites-lui écrire un script/template réutilisable (ex. `get-tweet-skill`) pour qu'elle réutilise la même méthode automatique les fois suivantes.
*   **Pipeline média automatisé :** Pour résumer une vidéo web :
    1. Télécharger la vidéo via `fx-twitter` / `yt-dlp`.
    2. Découper la piste audio avec `ffmpeg`.
    3. Envoyer l'audio à l'API Whisper pour transcription texte.
    4. Extraire des images/frames clés avec `ffmpeg` et les transmettre au modèle de vision pour obtenir une description visuelle complète.

---

### 4) Chiffres de revenus annoncés

*   **Chiffres de revenus :** Non précisé (aucun chiffre d'affaires ou revenu financier personnel n'est mentionné ou affirmé dans la vidéo ; l'auteur cite uniquement un coût de serveur VPS de 20 $/mois).
