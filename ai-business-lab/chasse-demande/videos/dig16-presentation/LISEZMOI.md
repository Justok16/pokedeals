# Vidéo de présentation DIG16 (08/10/2026)

- `dig16-presentation.mp4` : 38,5 s (version voix naturelle du 08/10), format vertical 1080 × 1920 (téléphone), H.264 + AAC, volume -16 LUFS.
- Demandée par l'utilisateur le 08/10 (« Oui vidéo avec une présentation attractive et convaincante », voix et musique).
- Usage : à montrer en rendez-vous ou en entretien. **Pas de prix dans la vidéo**, pour qu'elle reste utilisable
  pendant les entretiens d'étude de marché, où l'on ne vend rien (`57-entretiens-etude-de-marche.md`).
- Affirmations reprises telles quelles du site dig16.fr : 0 € de création, en ligne en 7 jours, site à votre nom,
  page d'accueil refaite gratuitement avant toute décision.

## Fabrication (0 €, tout est rejouable)

1. Voix (refaite le 08/10, l'utilisateur trouvait la première « robotique ») : `texte.txt`, lu par la synthèse
   vocale **Gemini** (modèle `gemini-2.5-flash-preview-tts`, voix « Despina », consigne « chaleureuse, posée et
   souriante »), via la fonction `api/voix.js` du relais Vercel et la clé Gemini gratuite. Un seul modèle pour toutes
   les phrases (timbre identique). **Contrôle automatique** : la bande-son finale est retranscrite par Vosk
   (reconnaissance vocale libre, modèle français) pour vérifier chaque mot et son horaire.
   La marque est écrite « Dig seize » dans le texte pour être bien prononcée.
   Première version (abandonnée) : Piper, voix « siwis » (CC BY 4.0).
2. Musique : `musique.py`, composition originale générée par programme (aucun droit de tiers).
3. Images : `video.html` (animation pilotée par `seek(t)`), capturée image par image avec Playwright (30 i/s),
   assemblée avec FFmpeg ; musique baissée automatiquement sous la voix.
   Captures des démos : `site-dig/img/vitrine-*-tel.webp`.

## Sur dig16.fr

Au centre de l'éventail du haut de l'accueil (`site-dig/video/`, 720 × 1280, MP4 2,4 Mo + WebM 2 Mo) : aperçu muet
en boucle à l'arrivée (désactivé si « mouvement réduit » ou « économie de données »), bouton « Regarder avec le son »
qui relance la vidéo depuis le début avec le son ; la barre d'appel du bas se cache tant que la vidéo est visible.

## Version 3 (08/10, après-midi) : voix d'homme « conteur »

- L'utilisateur trouvait encore la voix « robotique » et a cité comme modèle la voix de la chaîne YouTube
  @laquetedusavoiryt. Analyse par Gemini (mode `voix` du relais) : **voix de synthèse** (probablement ElevenLabs,
  payant, offre gratuite non commerciale), homme 30-40 ans, médium-grave, ronde et chaleureuse, ton de conteur
  mi-sérieux mi-ironique, ~160 mots/min, voix sèche et proche. On **s'inspire du style sans copier la voix**.
- Texte lu **d'une seule traite** (prosodie naturelle) par `gemini-3.8-flash-tts`, sans consigne (ce modèle lit
  la consigne à voix haute), voix « Algieba » par défaut ; essais « Sadaltager » et « Charon » envoyés à
  l'utilisateur pour choix. Texte : ajout « Basé en Charente » (demande du 08/10).
- Traitement : passe-haut 75 Hz, +2,5 dB à 160 Hz (chaleur), +1,5 dB à 3,2 kHz (présence), compression 3,5:1,
  dé-essage, -15 LUFS. Musique ajustée à la durée (`DUREE`).
- `fabriquer.py <voix>` : repère le début de chaque phrase dans la voix (mots horodatés par Vosk), déforme le temps
  de l'animation pour suivre la voix, mixe, rend la vidéo. Sur le site : `site-dig/video/presentation-v3.*`
  (nouveau nom à chaque version, pour éviter l'ancienne vidéo gardée en cache).
- **Choix validé par l'utilisateur le 08/10 : voix « Algieba »** (« Algieba c'est très bien »). À réutiliser pour toute future vidéo DIG16.

## v5 (08/10/2026)

- « pour les artisans et commerçants de Charente » coupé à droite (signalé par l'utilisateur) : passé sur
  deux lignes (« … commerçants » / « de Charente »), largeur contrôlée (888 px sur 888 px disponibles).
- Nouveau logo DIG16 (emblème D16 et signature) en haut de la vidéo et sur l'écran de fin.
- Même voix Algieba, même musique, même durée (33,8 s), −15,7 LUFS. Fichiers web : `presentation-v5.*`.

## v6 (08/10/2026) — demande de l'utilisateur : dire « DIG16.fr » pour que le visiteur retienne l'adresse

- Texte : « Basé en Charente, Dig seize point F R crée… » et fin « Vous jugez sur pièce. Dig seize point F R. »
  (écrit « point F R » pour que la voix épelle l'extension ; vérifié par Vosk : « points et faire »).
- Écran : « Avec DIG16.fr ». Nouvelle prise Algieba (gemini-3.8-flash-tts), 33,2 s, −15,5 LUFS.
  Fichiers web `presentation-v6.*`, affiche `affiche-v6.webp` ; boutons du site passés à « 33 s ».
- La v5 (voix « Dig seize, sites internet ») est gardée dans le brouillon de travail, pas sur le site.
- **08/10 : v6 validée par l'utilisateur** (prononciation « Dig seize point F R » : « parfait »).
