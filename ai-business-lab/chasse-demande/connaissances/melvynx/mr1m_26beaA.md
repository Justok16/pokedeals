# Mistral Vibe: un vrai concurrent à Codex ou Claude Code (je suis un peu choqué).

Vidéo : https://youtu.be/mr1m_26beaA · durée 13:37 · résumé Gemini (gemini-3.5-flash, lot de 7) du 2026-10-09
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1. **Idée principale :**
Évaluer et comparer l'agent de développement open-source "Mistral Vibe CLI" (équipé de Devstral 2) et "Claude Code" (Claude Opus 4.5) pour le développement complet d'une application web génératrice de miniatures YouTube connectée à l'API de Google Gemini.

2. **Outils, sites ou dépôt GitHub cités :**
* **Mistral Vibe CLI** (ou *Mistral Vibe*) : Outil en ligne de commande et agent de codage open-source développé par Mistral AI. (Gratuit et disponible sur GitHub).
* **Claude Code / Claude CLI** : Agent d'Anthropic en ligne de commande. (Payant).
* **Devstral 2** (notamment *Devstral Small 2* et *Devstral Zizel 2*) : Modèles de codage de nouvelle génération de Mistral AI. (Gratuit sous licence open-source / Accès API payant).
* **Gemini 3 Pro Image-Preview** (ou Google GenAI SDK) : API d'IA de Google utilisée pour générer les images de miniatures. (Payant / Essai gratuit).
* **Shadcn UI** : Bibliothèque de composants React utilisée pour concevoir l'interface utilisateur. (Gratuit et open-source).
* **COSS UI** : Bibliothèque de composants utilisés pour créer l'interface de téléversement (Uploader). (Gratuit / Option payante).
* **Next.js** : Framework web React. (Gratuit).
* **OpenRouter** : Plateforme en ligne permettant de comparer les performances, la latence et le débit (TPS) des modèles d'IA. (Payant).
* **Zed** : Éditeur de code. (Gratuit et open-source).

3. **Astuces concrètes et réutilisables :**
* Pour créer un générateur d'images de miniatures performant, concevoir une interface permettant d'ajouter plusieurs photos de référence d'un visage (sous différents angles) et des images d'inspiration de style distinctes pour guider l'IA.
* En cas d'erreur de dépassement de taille de fichier lors du téléversement d'images (erreur de limite de corps de requête à 1 Mo sous Next.js), configurer explicitement l'option `experimental.serverActions.bodySizeLimit` à `10mb` (ou plus) dans le fichier `next.config.js`.
* Analyser le débit de tokens (TPS) lors du choix de vos agents : l'auteur montre que Devstral 2 tourne à environ 46 TPS sur OpenRouter, tandis que Claude Opus 4.5 atteint 98 TPS sur Anthropic.

4. **Chiffres de revenus annoncés :**
Non précisé (*affirmé par l'auteur*).
