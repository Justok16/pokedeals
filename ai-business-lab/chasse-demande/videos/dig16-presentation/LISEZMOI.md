# Vidéo de présentation DIG16 (08/10/2026)

- `dig16-presentation.mp4` : 38,5 s, format vertical 1080 × 1920 (téléphone), H.264 + AAC, volume -16 LUFS.
- Demandée par l'utilisateur le 08/10 (« Oui vidéo avec une présentation attractive et convaincante », voix et musique).
- Usage : à montrer en rendez-vous ou en entretien. **Pas de prix dans la vidéo**, pour qu'elle reste utilisable
  pendant les entretiens d'étude de marché, où l'on ne vend rien (`57-entretiens-etude-de-marche.md`).
- Affirmations reprises telles quelles du site dig16.fr : 0 € de création, en ligne en 7 jours, site à votre nom,
  page d'accueil refaite gratuitement avant toute décision.

## Fabrication (0 €, tout est rejouable)

1. Voix : `texte.txt`, lue par Piper (logiciel libre) avec la voix française « siwis » (licence du jeu de données :
   CC BY 4.0, lue sur la fiche officielle du modèle le 08/10). Crédit affiché à la fin de la vidéo.
   La marque est écrite « Dig seize » dans le texte pour être bien prononcée.
2. Musique : `musique.py`, composition originale générée par programme (aucun droit de tiers).
3. Images : `video.html` (animation pilotée par `seek(t)`), capturée image par image avec Playwright (30 i/s),
   assemblée avec FFmpeg ; musique baissée automatiquement sous la voix.
   Captures des démos : `site-dig/img/vitrine-*-tel.webp`.
