# J'AI CRÉÉ L'APP PARFAITE "Speech to Text" en 1 HEURE avec Claude Code (et tu peux aussi le faire)

Vidéo : https://youtu.be/NTsVyYNehEY · durée 22:04 · résumé Gemini (gemini-3.5-flash-lite, lot de 6) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale** : Présentation d'outils de « speech-to-text » (parole vers texte) et d'une méthode pour forker et modifier des projets Open Source existants (en particulier un outil nommé *Parler*) afin d'ajouter des fonctionnalités personnalisées comme le « post-processing » avec l'IA.

2) **Outils, sites et dépôts cités** :
- **Handy** : Application gratuite et Open Source pour Mac (speech to text).
- **SuperWhisper** : Outil payant (prix non précisé clairement au début, mention d'un plan gratuit limité à 2000 mots/semaine, et version Pro ou outils basés sur des modèles open source).
- **WhisperFlow** : Outil payant ($15/user/mo pour Flow Pro, version gratuite limitée à 2000 mots/semaine).
- **Modèles Open Source mentionnés** : Whisper, Paraket V3, Moonshine.
- **Claude Code** : Utilisé en terminal pour télécharger, modifier et interagir avec les projets.
- **Excalidraw** : Utilisé pour faire des schémas explicatifs des tarifs.
- **VoiceInk** : Outil jugé overkill / non retenu ($39 à vie ou $25 à vie selon les offres).
- **Parler** : Projet Open Source (forké par l'auteur à partir d'un dépôt GitHub nommé `mpainter/handy`), avec licence MIT (permissive pour usage commercial).
- **Gemini Flash / API Google** : Utilisé pour le post-processing (corrections grammaire, etc.).

3) **Astuces concrètes et réutilisables** :
- Utiliser Claude Code en terminal pour cloner des dépôts GitHub open source (`git clone ...`), créer un fork sous un nouveau nom, et modifier le code source pour y intégrer ses propres préférences (changer les couleurs, ajouter des modèles LLM comme Gemini, configurer des raccourcis clavier ou des modes de post-traitement).
- Configurer des actions de « post-processing » dans l'application pour appliquer automatiquement des règles de correction textuelle (ponctuation, majuscules, suppression des tics de langage) via des prompts envoyés à une IA.
- Configurer le basculement automatique de modèle (par exemple passer de Paraket V3 à Whisper Turbo si la durée d'enregistrement dépasse un certain seuil).

4) **Chiffres de revenus annoncés** :
- Non précisé (la vidéo parle de coûts d'abonnement pour les logiciels concurrents comme Flow Pro à $15/mois ou WhisperFlow, et de la licence MIT gratuite, mais aucun chiffre de gain d'argent n'est annoncé).
