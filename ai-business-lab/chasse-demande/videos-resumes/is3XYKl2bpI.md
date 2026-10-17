# 8 conseils officiels pour bien utiliser Claude Opus 5.5

Vidéo : https://youtu.be/is3XYKl2bpI · envoyée par l'utilisateur le 28/09/2026 · résumé Gemini (gemini-3.6-flash) du 2026-09-28
(chiffres et affirmations des auteurs : non vérifiés)

### 1) Idée principale
La vidéo présente et explique **8 conseils pratiques** issus du guide officiel d'Anthropic pour bien utiliser et prompter le modèle **Claude Opus 5.5**. L'objectif est d'aider les utilisateurs et développeurs à obtenir de meilleurs résultats, à automatiser des tâches efficacement et à réduire la consommation de jetons (*tokens*) pour faire des économies financières lors de l'utilisation de l'API.

---

### 2) Outils, sites ou dépôts GitHub cités

1. **Claude Opus 5.5** (par Anthropic)
   * **Gratuit ou payant :** Non précisé dans la vidéo (modèle accessible via l'API/interface d'Anthropic).
   * **À quoi il sert :** Modèle de langage avancé utilisé pour la rédaction, l'analyse de documents, la programmation, l'exécution d'agents autonomes et l'analyse d'images.
2. **Claude Opus 5** (par Anthropic)
   * **Gratuit ou payant :** Non précisé.
   * **À quoi il sert :** Version antérieure du modèle, citée pour comparer les réglages par défaut de réflexion et la précision visuelle.
3. **PIL / OpenCV** (mentionnés dans la documentation affichée à l'écran)
   * **Gratuit ou payant :** Non précisé.
   * **À quoi ils servent :** Outils/outils de traitement d'images permettant à l'agent IA d'effectuer des opérations comme le recadrage (*crop*) pour mieux lire les détails.
4. **Dépôts GitHub :** Aucun dépôt GitHub n'est cité dans la vidéo.

---

### 3) Astuces concrètes et réutilisables

* **1. Ajuster le niveau d'effort (*Effort Setting*) :**
  * Opus 5.5 utilise désormais le niveau d'effort « Medium » par défaut (alors qu'Opus 5 était sur « High »). 
  * *Astuce :* N'appliquez pas automatiquement vos anciens réglages élevés. Commencez toujours par tester votre tâche avec le niveau d'effort moyen avant de l'augmenter, afin d'économiser des jetons.

* **2. Nettoyer les instructions de réflexion (*Thinking Instructions*) :**
  * Supprimez les consignes vagues du type « réfléchis attentivement ». Le modèle gère lui-même la quantité de réflexion nécessaire.
  * Dans les conversations à plusieurs tours, indiquez à Claude de considérer ses réponses précédentes comme acquises et de ne pas les réanalyser à chaque nouveau message, sauf si vous lui demandez explicitement d'en corriger une.

* **3. Demander de vérifier tout le contexte avant d'agir :**
  * Opus 5.5 a tendance à travailler très vite. Dans des flux de travail multi-applications, demandez-lui d'explorer toutes les sources (emails, documents, onglets de tableur) avant de rédiger ou de mettre à jour un travail, car une information essentielle (comme un changement de date limite) peut se trouver dans un autre fichier.

* **4. Séparer vos consignes du texte copié-collé :**
  * Distinguez clairement vos instructions du contenu externe fourni (ex. le texte d'un email). Indiquez explicitement à Claude quel texte constitue la consigne et quel texte est uniquement du matériau source à analyser, pour éviter qu'il n'exécute des consignes situées dans le texte source (*prompt injection*).

* **5. Définir des étapes clés pour les mises à jour (*Checkpoints*) :**
  * Au lieu de laisser le timing ouvert ou de demander à l'IA de « parler plus », définissez des jalons précis où l'IA doit vous donner un court rapport (ex. *« Donne-moi un bref résumé après avoir vérifié les fichiers, puis un autre quand le brouillon est prêt »*).

* **6. Faire avancer l'agent jusqu'à un blocage réel :**
  * Une réponse générée ne veut pas dire que la tâche globale est finie. Définissez ce que contient le travail terminé (ex. rapport + liste de sources + résumé).
  * Pour les agents automatisés, ordonnez-lui de continuer d'exécuter l'étape suivante de lui-même sans attendre votre validation, sauf en cas de blocage réel ou de besoin d'approbation obligatoire.

* **7. Donner des consignes de design spécifiques :**
  * Évitez les requêtes vagues comme *« Rends ce site moins générique »* (l'IA va juste remplacer un style par défaut par un autre style par défaut).
  * Précisez des détails visuels concrets : couleur de fond, style des titres, forme des boutons, espacements, ou fournissez une image de référence.

* **8. Faciliter la lecture des détails visuels complexes :**
  * Pour que l'IA lise de petites étiquettes ou des graphiques denses, fournissez une image en haute résolution, donnez-lui accès à un outil de recadrage (*crop tool*) pour qu'elle zoome elle-même, ou joignez vous-même un gros plan. Dites-lui aussi d'indiquer si un texte est illisible plutôt que de deviner.

---

### 4) Chiffres de revenus annoncés
* **Aucun chiffre de revenu n'est annoncé ou mentionné dans la vidéo** (*affirmé par l'auteur / non précisé*).
