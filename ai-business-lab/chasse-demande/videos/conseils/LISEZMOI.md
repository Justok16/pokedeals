# Série « Le conseil DIG16 » (18/10/2026)

Choix B de l'utilisateur (18/10) : vidéos courtes animées avec voix de synthèse, sans se filmer, pour nourrir les
réseaux (idée « clipping » du reel Dej1p_IgkuM, faite gratuitement et sans filigrane).

- 5 vidéos verticales 1080 × 1920 de 15 à 25 s : `conseil-1.mp4` … `conseil-5.mp4`. Reels Instagram et Facebook,
  Shorts YouTube, TikTok, X, statut WhatsApp.
- Contenu : uniquement le guide https://dig16.fr/site-internet-artisan/ (sources citées dans le guide). Aucun chiffre,
  aucun nom réel, aucun avis.
- Voix « Algieba » (`gemini-3.8-flash-tts`, choisie par l'utilisateur le 08/10) via `/api/voix` du relais, une phrase
  par scène ; **chaque phrase est transcrite (faster-whisper) et comparée au texte voulu** avant le montage (leçon du
  18/10 : une consigne de style était lue à voix haute). Musique originale DIG16 (`../dig16-presentation/musique.py`).
  Étiquette « contenu généré par IA » à cocher sur TikTok et Instagram (voix de synthèse), comme pour la présentation.
- Refaire : `python3 fabriquer.py [numéros]` (voix en cache dans `voix/`, non versionnées). Contrôles bloquants :
  polices chargées, textes dans la marge, durée 12-35 s, voix conforme, barre de progression à 50 % à mi-vidéo, 1re image avec le titre (vignette des réseaux). Images de contrôle dans `controle/`.
- Textes des publications : `legendes.md`.

- Contrôle du 18/10 (conseils 1 et 2) : 7 images par vidéo (0 à 100 %), transitions sans chevauchement, son final
  transcrit (phrases exactes), −14,8 et −14,5 LUFS, H.264 + AAC 1080 × 1920. Défauts trouvés et corrigés : barre de
  progression trop rapide, 1re image vide, titre final trop proche du bandeau, « : » et « ? » en début de ligne,
  apostrophes droites, « devis en deux clics » (non écrit dans le guide) remplacé par « simple à demander ».
