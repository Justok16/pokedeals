# Créer ta première application avec Codex - Tuto débutant

Vidéo : https://youtu.be/_sXQ7UP6eSM · durée 17:43 · résumé Gemini (gemini-3.7-flash) du 2026-10-03
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici le résumé complet et structuré de la vidéo :

---

### 1) Idée principale
L'auteur montre comment utiliser l'application de bureau **Codex** (l'agent autonome de codage développé par OpenAI) pour concevoir et faire coder entièrement une application locale sans savoir programmer. 

À titre d'exemple, il crée un outil nommé **« B-roll Cutter »** :
* L'application tourne en local dans le navigateur web.
* L'utilisateur y glisse-dépose des vidéos brutes (B-roll).
* L'application utilise des API d'IA (Gemini / ElevenLabs) pour analyser les scènes, découper automatiquement les meilleurs passages (durée maximale de 10 secondes), les renommer intelligemment en français selon l'action filmée, et enregistrer les clips découpés dans un dossier de sortie.
* L'objectif est d'automatiser des flux de travail chronophages (montage vidéo, tri d'actifs multimédias) ou de créer des micro-outils internes et des SaaS.

---

### 2) Outils, sites et extensions cités

| Nom exact | Gratuit / Payant | Utilité |
| :--- | :--- | :--- |
| **Codex App** (`openai.com/codex`) | Payant (nécessite un abonnement ChatGPT) | Application de bureau d'OpenAI permettant à un agent IA de développer, tester et exécuter du code directement sur la machine. |
| **ChatGPT** (`chatgpt.com`) | Gratuit / Payant (Formules **Plus** à 20 $/mois, **Pro** à 120 $/mois ou 200 $/mois recommandées) | Plateforme IA sous-jacente donnant accès aux modèles et fonctionnalités de Codex. |
| **Google AI Studio / Gemini API** (`aistudio.google.com` / `gemini.google.com`) | Gratuit (dans les limites de quota de base) / Payant | Fournit une clé API pour les modèles multimodaux de Google (ex. *Gemini 1.5 Flash* / *Flash Lite*) afin d'analyser le contenu visuel des vidéos. |
| **ElevenLabs** (`elevenlabs.io`) | Freemium (gratuit avec crédits / payant au-delà) | Plateforme d'IA audio utilisée ici pour ses capacités d'analyse/traitement audio (*Speech-to-Text*). |
| **OpenAI API / OpenRouter** | Payant (à l'usage) | Cités brièvement comme solutions alternatives pour connecter des clés API de modèles d'IA. |
| **Plugin Computer Use** (dans Codex) | Inclus dans Codex | Extension interne permettant à l'agent IA de contrôler des actions sur l'ordinateur. |
| **Plugin Chrome / ChatGPT Chrome Extension** | Gratuit | Extension permettant à Codex d'interagir directement avec le navigateur Google Chrome. |
| **Formation Codelynx / AI Builder** (`mlv.sh/fcs` / `codelynx.dev`) | Payant | Formation de l'auteur axée sur la création de SaaS et l'utilisation d'outils d'IA comme Claude Code, Cursor et Codex. |

---

### 3) Astuces concrètes et réutilisables

1. **Forcer la phase de cadrage (« Pose-moi des questions »)** :
   Avant de laisser l'IA coder, donnez-lui l'instruction explicite de vous poser une série de questions pour préciser tous les détails techniques et fonctionnels (format des fichiers, durée des clips, conventions de nommage, API à utiliser). Cela évite les erreurs de conception et le code inutile.
2. **Adapter l'effort du modèle à son budget** :
   * Avec un forfait ChatGPT à 20 $/mois : choisir le modèle avec un niveau d'effort *Light* ou *Medium*.
   * Avec un forfait Pro (120 $ ou 200 $/mois) : activer l'effort *High* ou *Extra High* ainsi que le mode *Fast*.
3. **Accorder le « Full Access »** :
   Activer l'option *Full access* dans Codex afin qu'il puisse créer les fichiers, installer les dépendances locales et lancer les serveurs sans demander de permission à chaque ligne.
4. **Piloter via la file d'attente (*Queue / Steer*)** :
   Pendant que l'agent code, vous pouvez saisir des instructions complémentaires dans la boîte de saisie ; elles sont mises en attente et s'exécuteront dès que l'étape courante est terminée.
5. **Utiliser les annotations visuelles pour l'UI** :
   Ouvrez la prévisualisation web intégrée dans Codex, utilisez l'outil de capture/annotation pour pointer un bouton ou une zone spécifique et dictez directement la consigne de refonte (ex. « passer les textes en anglais », « rendre l'interface plus minimaliste »).
6. **Demander le traitement parallèle (Batch processing)** :
   Préciser à l'agent de traiter les fichiers en parallèle plutôt que de manière séquentielle pour accélérer le traitement lors de l'import de nombreuses vidéos.

---

### 4) Chiffres de revenus annoncés

* **Chiffres de gains financiers personnels / revenus générés :** **Non précisé** (l'auteur évoque une économie de coûts par rapport au salaire d'un monteur/assistant et mentionne que plus de 4 000 personnes ont rejoint sa formation, mais ne donne aucun chiffre de chiffre d'affaires ou de bénéfice chiffré — *affirmé par l'auteur : non mentionné*).
