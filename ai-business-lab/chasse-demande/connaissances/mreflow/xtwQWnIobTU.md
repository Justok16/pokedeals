# Comment générer des images et des vidéos IA gratuitement sans Internet (tutoriel ComfyUI)

Vidéo : https://youtu.be/xtwQWnIobTU · durée 20:59 · résumé Gemini (gemini-3.5-flash, lot de 5) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) Idée principale**
Guide complet pour installer et utiliser ComfyUI en local sur son ordinateur (Mac ou PC) afin de générer des images photoréalistes (FLUX.1) et des vidéos (Wan 2.2) de façon 100 % gratuite, hors-ligne et sans censure.

**2) Chaque outil, site ou dépôt GitHub cité**
*   **ComfyUI (`comfy.org` et GitHub `comfyanonymous/ComfyUI`)** | Gratuit / Open-source | Interface basée sur des nœuds pour exécuter des modèles de génération d'images et vidéos en local.
*   **FLUX.1 Krea Dev (`black-forest-labs/FLUX.1-krea-dev` sur Hugging Face)** | Gratuit (Open-weight) | Modèle de génération d'images de très haute qualité et photoréaliste.
*   **Wan 2.2 (14B et 5B)** | Gratuit (Open-weight) | Modèles open-source performants pour la génération de vidéo (Text-to-Video et Image-to-Video).
*   **Hugging Face** | Gratuit | Plateforme permettant de télécharger les modèles et encodeurs textuels au format `.safetensors`.
*   **AITrepreneur & Olivio Sarikas** | Gratuit (Chaînes YouTube) | Chaînes recommandées pour apprendre à maîtriser les workflows nodaux complexes dans ComfyUI.

**3) Les astuces concrètes et réutilisables**
*   **Installation simplifiée :** Utiliser l'application Desktop de ComfyUI (`comfy.org`) plutôt que le dépôt GitHub manuel pour éviter la gestion complexe de Python et des bibliothèques.
*   **Résolution de bug Mac Apple Silicon :** Si la version FP8 du modèle FLUX plante (erreur MPS backend), télécharger le fichier safetensors complet de 23,8 Go depuis Hugging Face.
*   **Téléchargement automatique :** Utiliser le menu *Get Started with a Template* de ComfyUI pour charger des workflows préconfigurés qui téléchargent automatiquement les modèles manquants.
*   **Matériel recommandé pour la vidéo :** Utiliser un PC équipé d'une carte graphique Nvidia pour la génération vidéo avec Wan 2.2 (sur Mac, le rendu peut prendre de 20 à 60 minutes par vidéo).
*   **Accès aux fichiers :** Récupérer l'intégralité des visuels et vidéos générés dans le dossier local `ComfyUI/output/`.

**4) Les chiffres de revenus annoncés**
*   Non précisé.

---
