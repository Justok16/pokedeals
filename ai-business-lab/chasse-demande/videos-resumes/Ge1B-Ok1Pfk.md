# Vidéo YouTube Ge1B-Ok1Pfk (envoyée le 20/10/2026)

Lien : https://youtu.be/Ge1B-Ok1Pfk · résumé Gemini (gemini-3.5-flash-lite) du 20/10/2026, affirmations non vérifiées.

## Contenu
Vidéos animées (motion design) codées par Claude en JavaScript, sans générateur de vidéo par IA. Base gratuite « The Style Atlas » (Futurepedia, 86 styles avec leurs prompts). Voix de synthèse Gemini TTS (Google AI Studio) ou ElevenLabs ; minutage mot à mot (fichier SRT) pour caler l'animation sur la voix ; storyboard en images avant le rendu ; un style réussi est transformé en skill réutilisable. Remotion et HyperFrames cités comme alternatives.

## Comparaison avec notre méthode (`videos/conseils/fabriquer.py`, validée par l'utilisateur le 18/10)
| Astuce de la vidéo | Chez DIG16 |
|---|---|
| Animation codée plutôt que générée par IA | ✅ Déjà le cas (Python + FFmpeg, charte du site) |
| Voix Gemini TTS | ✅ Déjà le cas (voix « Algieba », choisie le 08/10) |
| Caler l'animation sur la voix | ✅ Déjà le cas : une phrase par scène, chaque phrase transcrite (faster-whisper) et comparée au texte |
| Storyboard avant le rendu | ✅ Images de contrôle `controle/` (7 par vidéo) |
| Style transformé en skill | 📦 À faire seulement si une 2e série de vidéos démarre (le format actuel est validé, on n'y touche pas) |
| The Style Atlas | 📦 En réserve pour une future série. L'adresse futurepedia.io/style-atlas renvoie « 404 » le 20/10 : lien exact à reprendre dans la description de la vidéo avant usage |

## Tri
✅ Rien à changer : notre chaîne de fabrication fait déjà l'essentiel, gratuitement. Rien installé.
