# Les SHORTS vont TOUS être faits par Opus 5.5 (meilleur montage IA)

Vidéo : https://youtu.be/1MLzT47oas4 · durée 17:56 · résumé Gemini (gemini-3.8-flash) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L’auteur montre comment il a entièrement automatisé son processus de création et de publication de contenus courts (Shorts YouTube, Reels Instagram, TikTok) et de vidéos en motion design, sans toucher à un logiciel de montage traditionnel (Premiere, Final Cut, etc.). 

En s’appuyant sur des agents IA pilotés par **Claude Code** (modèle Claude Opus), l’IA se charge de tout en une seule commande : découpe d’un enregistrement brut ou d’un podcast, suppression automatique des silences, sous-titrage calé au mot près, détourage du visage sans fond vert, ajout d'animations et bruitages codés sur mesure, relecture/autocorrection visuelle, rendu haute vitesse, et publication/programmation directe sur les réseaux sociaux. L'objectif est de remplacer le travail d'un monteur vidéo ou des outils SaaS de sous-titrage par une chaîne de production 100 % automatisée et personnalisée par code.

---

### 2) Outils, sites et dépôts cités

| Nom exact | Gratuit / Payant | Utilité |
| :--- | :--- | :--- |
| **Claude (Anthropic) / Claude Code / Opus 3.5 (mentionné sous l'appellation "Opus 5.5")** | **Payant** (abonnement Claude Pro / crédits API) | Agent IA qui écrit le code, orchestre le flux de montage, génère les animations, audite le rendu et gère la publication. |
| **Tella** (`tella.tv`) | **Payant / Freemium** (*modèle exact non précisé*) | Outil de capture vidéo facecam/écran utilisé par l'auteur pour tourner en une seule prise brute sans coupure. |
| **ElevenLabs (TTS & Scribe)** | **Payant** | Génération de voix de synthèse (modèle `eleven_multilingual_v2`, voix *Corentin*) et retranscription audio horodatée au centième de seconde (*Scribe*). |
| **FFmpeg** | **Gratuit / Open source** | Découpe des silences et respirations, accélération de la vidéo (+15 %), extraction d’images, mixage et normalisation audio (LUFS). |
| **Apple Vision** (script `matte.swift`) | **Gratuit** (intégré à macOS) | Détourage automatique du corps et du visage image par image, sans fond vert. |
| **Canvas 2D** (Node.js) | **Gratuit / Open source** | Dessin et génération des scènes graphiques et animations vectorielles (motion design avec effet de ressorts). |
| **Chrome Headless / WebCodecs H.264** | **Gratuit / Open source** | Moteur de rendu vidéo ultra-rapide tournant directement dans le navigateur headless avec workers en parallèle (ex. vidéo de 92 s rendue en 18 s). |
| **DSP.js** | **Gratuit / Open source** | Synthèse procédurale de bruitages sonores directement par code. |
| **Submagic** | **Payant** | Outil SaaS concurrent de sous-titrage et montage automatique, cité comme référence dépassée par ce système. |
| **Zernio** | **Gratuit** (*précisé par l'auteur*) | Outil utilisé pour automatiser la publication des vidéos sur TikTok. |
| **Schedules** (`schedules.melvynx.dev` / Agent *Hermes*) | **Outil propriétaire / interne de l'auteur** | Interface web et agent VPS développés par l'auteur pour planifier et envoyer les vidéos automatiquement sur YouTube, Instagram et TikTok. |
| **YouTube Studio / Instagram / TikTok** | **Gratuit** | Plateformes cibles pour la publication automatique des formats courts. |
| **Site de l'auteur** (`mlv.sh/fv`) | **Non précisé** (présenté comme une mini-formation / masterclass de 10 min) | Lien partagé pour accéder aux explications détaillées de son système. |

---

### 3) Astuces concrètes et réutilisables

1. **Remplacer les logiciels de montage par du code déclaratif :** Au lieu de monter à la main dans une timeline, l’IA génère un fichier de spécifications (`spec.js` / `timeline.js`). Chaque carte visuelle, mot-clé, animation et bruitage est calé dynamiquement sur le timestamp exact des mots fournis par la transcription.
2. **Workflow automatisé en 7 étapes :**
   - **Prise brute unique :** Tournage sans interruption.
   - **Transcription ultra-précise :** Horodatage au centième de seconde via ElevenLabs Scribe.
   - **Nettoyage automatique du rush :** Découpe des silences et pauses via FFmpeg et accélération du débit (ex. rush de 1 min réduit à 40 s).
   - **Détourage natif :** Utilisation des API de vision système (ex. Apple Vision sur macOS) pour isoler le visage/corps.
   - **Génération visuelle & motion design :** Dessin d’animations et éléments graphiques via Canvas 2D.
   - **Boucle de relecture autonome (Self-correction loop) :** L'agent IA exporte des captures d'écran (planches-contact en JPEG) des moments clés, analyse visuellement si du texte déborde ou si un asset est mal positionné, corrige son propre code, puis relance le rendu.
   - **Rendu headless :** Export accéléré via Chrome Headless et WebCodecs plutôt que d'attendre le rendu lourd d'un logiciel vidéo.
3. **Création d’un Skill Claude Code personnalisé (ex. `/short-editing`) :** Encapsuler l’ensemble de ce pipeline dans une commande Claude Code. Il suffit ensuite de lui passer une URL (ex. un lien YouTube de podcast long) ou un fichier pour qu'il lance des agents en parallèle (ex. 10 agents pour extraire et monter 10 Shorts distincts simultanément).
4. **Automatisation de la distribution :** Lier les scripts de sortie à des API ou des outils de planification (APIs YouTube OAuth, agent VPS pour Instagram, Zernio pour TikTok) avec des créneaux horaires prédéfinis (ex. 9h00 et 18h00) pour automatiser la chaîne de A à Z.

---

### 4) Chiffres de revenus annoncés

- **Aucun chiffre de revenus générés n'est annoncé par l'auteur** (*les chiffres mentionnés à l'écran dans un extrait de podcast, tels que 11 600 $ ou 91 000 $, concernent des consommations/dépenses de tokens IA et non des revenus*).
- **Coût de fonctionnement :** L'auteur affirme qu'avec un abonnement d'environ **100 € par mois** (*affirmé par l'auteur*), il est possible de faire produire jusqu'à **10 000 vidéos par mois** par son agent IA Claude.
