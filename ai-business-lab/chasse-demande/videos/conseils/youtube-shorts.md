# Shorts YouTube « Le conseil DIG16 » (calendrier, 20/10/2026)

Demande de l'utilisateur du 20/10 : « faire régulièrement des shorts sur ma chaîne ».

## Pourquoi YouTube était en retard
- Metricool (seul outil qui publiait sur YouTube) : quota gratuit de 20 publications par mois atteint pour octobre.
- Buffer gratuit : 3 réseaux maximum, déjà pris par Facebook, Instagram et TikTok.
- Résultat : après le conseil n° 1 (20/10, Metricool), plus rien de prévu sur YouTube.

## Solution (gratuite)
- **Zapier, action YouTube « Upload Video »** (connexion YouTube à faire une fois par l'utilisateur dans Zapier).
  Publication immédiate seulement (la programmation « Publish At » est réservée aux comptes Partenaires YouTube) :
  Claude publie donc à l'heure prévue, grâce à deux rappels automatiques (mardi 12 h 13 et jeudi 10 h 13, heure de Paris).
- Coût : 2 tâches Zapier par Short (offre gratuite : 100 tâches par mois, arrêt de sécurité à 90 ; compteur `.claude/hooks/quotas.json`).
- Vidéo envoyée depuis `https://dig16.fr/video/conseils/conseil-N.mp4` (conseils 6 à 10 : **`conseil-N-3d.mp4`**, version 3D validée par l'utilisateur le 21/10) (verticale, < 3 min : YouTube en fait un Short).
- Étiquette IA : l'aide YouTube (support.google.com/youtube/answer/14328491, lue le 20/10) ne demande de signaler que les contenus **réalistes** ; nos vidéos sont des animations de texte, non réalistes. Par transparence, la description dit « Voix de synthèse ».

**Connexion vérifiée le 20/10 à 4 h 10** : l'utilisateur a relié YouTube dans Zapier ; appel de contrôle « channels?mine=true » → chaîne **DIG16** (@dig16fr, UCdjVtP-NyaCQm4e0IJCYm1w), connexion par défaut 02bdf08a. Compteur Zapier d'octobre : 66/100 après les essais (marge 90).

## Calendrier (une ligne = un Short ; colonne « État » mise à jour après chaque publication)
| Date (Paris) | Heure | Vidéo | Titre YouTube | État |
|---|---|---|---|---|
| mar. 20/10 | 12 h 15 | conseil-1 | Le conseil DIG16 : Votre site est-il vraiment à vous ? | **Publié** par Metricool : https://www.youtube.com/shorts/RIUMc2ZnhmI (vérifié le 20/10 à 12 h 35) |
| mar. 20/10 | 13 h 36 | lancement-dig16 (voix off) | DIG16 : votre page d'accueil refaite gratuitement | **Publié** : https://www.youtube.com/shorts/ylisB7SW5Ms |
| jeu. 22/10 | 10 h 15 | conseil-6-3d | Le conseil DIG16 : Pensé pour le téléphone | **Publié** par Zapier à 11 h 24 (1 h 09 de retard : le garde-fou de quota bloquait à 90 tâches, l'exception « Shorts du calendrier » n'y était pas codée ; corrigé le 22/10) : https://www.youtube.com/shorts/sqUv83Gzqh4 ; compteur Zapier 92/100. **Voix « Di seize » à la fin (signalé par l'utilisateur à 14 h 30)** : conseils 6 et 10 refaits (contrôle strict de la marque + resynthèse automatique dans `fabriquer.py`), mis en ligne, **republié à 15 h 02** : https://www.youtube.com/shorts/_lGpEp6ohR0 (abonnés non prévenus une 2e fois) ; l'ancien Short est à supprimer par l'utilisateur ; compteur Zapier 94/100 |
| ~~mar. 27/10~~ **lun. 02/11** | 10 h 15 | conseil-2 | Le conseil DIG16 : Les 5 pages qui comptent | **reporté au 02/11** (22/10 : Zapier 100/100 et Metricool 20/20 en octobre) ; rappel du 02/11 |
| ~~jeu. 29/10~~ **mer. 04/11** | 10 h 15 | conseil-7-3d | Le conseil DIG16 : La fiche Google | **reporté au 04/11** (22/10 : quota Zapier d'octobre à 98/100 après la correction du conseil 6 ; il reste juste le Short du 27/10) — rappel programmé le 04/11 à 10 h 13 |
| mar. 03/11 | 12 h 15 | conseil-3 | Le conseil DIG16 : Les avis Google, sans tricher | **par Metricool** (programmé, YouTube seul, description et 11 mots-clés à jour le 21/10) : ne pas envoyer par Zapier, seulement vérifier |
| jeu. 05/11 | 10 h 15 | conseil-8-3d | Le conseil DIG16 : Un site gratuit suffit-il ? | **par Metricool** (programmé, YouTube seul, description et 11 mots-clés à jour le 21/10) : ne pas envoyer par Zapier, seulement vérifier |
| mar. 10/11 | 12 h 15 | conseil-4 | Le conseil DIG16 : 3 questions avant de signer | **par Metricool** (programmé, YouTube seul, description et 11 mots-clés à jour le 21/10) : ne pas envoyer par Zapier, seulement vérifier |
| jeu. 12/11 | 10 h 15 | conseil-9-3d | Le conseil DIG16 : Location ou achat ? | **par Metricool** (programmé, YouTube seul, description et 11 mots-clés à jour le 21/10) : ne pas envoyer par Zapier, seulement vérifier |
| mar. 17/11 | 12 h 15 | conseil-5 | Le conseil DIG16 : Une page Facebook suffit ? | **par Metricool** (programmé, YouTube seul, description et 11 mots-clés à jour le 21/10) : ne pas envoyer par Zapier, seulement vérifier |
| jeu. 19/11 | 10 h 15 | conseil-10-3d | Le conseil DIG16 : Besoin d'un site ? | à publier |
| Note du 21/10 | | | Novembre réorganisé : les Shorts des 03, 05, 10, 12 et 17/11 partent par Metricool (YouTube seul) ; Zapier ne publie que le 19/11 (conseil 10) et ceux d'octobre | tranché le 21/10 |
| à partir du 24/11 | | conseils 11 à 15 | (nouveaux sujets tirés du guide, même format validé ; à montrer à l'utilisateur avant publication) | à fabriquer début novembre |

## Description de chaque Short
Texte de la vidéo dans `legendes.md`, avec « (lien dans la bio) » remplacé par le lien complet
`https://dig16.fr/site-internet-artisan/`, puis la ligne « Voix de synthèse. DIG16, sites internet pour artisans et commerçants en Charente. »
Catégorie « Howto & Style », pas pour les enfants, public, abonnés prévenus.

## Contrôle du son après chaque publication (ajouté le 22/10)
L'utilisateur a cru le Short n° 6 muet. Contrôle en 3 temps, désormais à chaque Short : 1) `ffprobe` sur le fichier en ligne (piste aac) et `ffmpeg -af volumedetect` (niveau moyen autour de −18 dB, comme le conseil n° 1) ; 2) après publication, demander au relais Vercel `…/api/video?id=<id>&mode=voix&modeles=gemini-3.8-flash` : Gemini décrit la voix off telle que YouTube la sert (le 22/10 : voix d'homme, baryton, voix de synthèse ; donc le son est bien sur YouTube) ; 3) si l'utilisateur n'entend rien : vérifier d'abord le volume multimédia du téléphone et la petite icône de haut-parleur barré en haut du Short (les Shorts s'ouvrent parfois en sourdine), puis attendre quelques minutes (YouTube finit de traiter le son après l'envoi).

