# Registre des leçons — à relire au début de chaque session et avant toute tâche du même type

Demande de l'utilisateur (18/10/2026) : « apprendre de tes erreurs POUR TOUJOURS et continuer à apprendre de façon
exponentielle ». Règle : **chaque erreur constatée (par l'utilisateur, par un contrôle ou par Claude) devient aussitôt
une ligne ici**, avec la règle qui l'empêche de revenir et, si possible, un contrôle automatique. Rien de personnel ici
(dépôt public).

## Comment s'en servir

1. Début de session : lire ce fichier en entier (il est cité dans `.claude/CLAUDE.md`).
2. Avant une tâche : relire la section correspondante (documents, site, vidéo, chiffres, rappels, outils).
3. Après une erreur : ajouter la ligne **avant** de répondre à l'utilisateur ; transformer la règle en contrôle
   automatique dès que c'est possible (colonne « Garde-fou »).
4. Auto-analyse du mardi et du vendredi (21 h 22) : relire les corrections de la semaine, compléter ce fichier.

## Rappels programmés et autonomie

| Date | Erreur | Règle | Garde-fou |
|---|---|---|---|
| 16/10, 17/10 (×3) | Réponse « No response requested » à un rappel programmé au lieu de faire les étapes (cookie du relais, Indy/GoCardless) | **Un rappel programmé est une tâche** : lire la notification, faire chaque étape avec les outils, puis reprogrammer. Jamais de réponse vide | Phrase « ne jamais répondre No response requested » dans chaque consigne de rappel |
| 19/10 | Demandé à l'utilisateur d'appeler le Point-Justice et de « lire le projet », puis de valider un mail à un organisme que Claude pouvait envoyer seul (règle « organismes » de `CLAUDE.md`) | **Avant toute demande à l'utilisateur : « puis-je le faire moi-même ? »** Si oui, le faire ; au pire, demander une validation d'un mot, jamais une tâche (règle permanente du 19/10) | Relire chaque « À TOI » avant envoi : chaque ligne doit être impossible pour Claude (présence physique, identité, argent, signature) |
| 18/10 (23 h) | Page guide ajoutée au plan du site le 18/10 **à l'intérieur** de l'entrée « Le projet » (balise `</url>` oubliée) : XML bien formé, mais la Search Console affichait « Aucun sitemap référent détecté » pour la page guide | Après toute modification de `sitemap.xml`, vérifier que chaque `<url>` est au premier niveau | `test_pages.py` → `plan_du_site()` : alerte si une entrée est imbriquée ou si une page publique testée manque au plan |
| 18/10 (22 h 20) | Captures des profils validées (« flyer épinglé 👍 ») sans zoomer : l'épingle Instagram était une version du flyer **avec champs vides** (« [Téléphone] », « [Prénom Nom] », « SIREN [à compléter] ») et l'épingle TikTok la **version papier A5** (nom complet, adresse, « Ne pas jeter sur la voie publique ») ; vu seulement en recadrant les captures | **Toute capture d'un visuel publié est agrandie (recadrage) et lue en entier** avant de dire « c'est bon » : coordonnées, mentions légales, champs entre crochets | Script de recadrage (PIL) sur chaque capture de publication ; recherche de « [ » et de l'adresse dans le texte lu |
| 18/10 (19 h 45) | Encore « No response requested », cette fois au milieu du point de 19:34 UTC, après une reprise (« Continue from where you left off ») : le point est resté à moitié fait | **Une reprise continue la tâche en cours** : relire la dernière consigne non terminée et finir chaque étape (ETAT.md compris) avant toute réponse | Avant de répondre, se demander : « quelle étape de la consigne reste à faire ? » |
| 18/10 | Cookie du relais reposé sans `-L` : la redirection du lien de partage n'était pas suivie, fichier de cookies vide, relais refusé (302) | Reposer le cookie avec `curl -s -L -c /tmp/cj.txt -b /tmp/cj.txt` puis tester `/api/video` | Test « identifiant vidéo invalide » obligatoire après chaque renouvellement |
| 16/10 | Mail d'Atout Ruffec arrivé à 11 h, vu le soir | Courrier relevé 3 fois par jour en semaine | Rappel lun-sam 10 h 13, 13 h 13, 16 h 13 |
| 13/10 | Tâche classée « facultative » sans vérifier les données (compteur de visites à 0) | Vérifier les données réelles avant de classer une tâche | Liste unique `64` § 0 relue en entier |
| 11/10 | Récapitulatif oubliant YouTube, Threads, Bluesky | Une seule liste fait foi : `64` § 0 | Idem |

## Chiffres, faits et textes publiés

| Date | Erreur | Règle | Garde-fou |
|---|---|---|---|
| 25/09 | Aide annoncée à 6 300 € (article de 2022) au lieu de 3 000 € ; taux oublié | Chiffre = page officielle datée, lue directement, citée | Règle « Chiffres » de `CLAUDE.md` |
| 18/10 | Formule « devis en deux clics » écrite dans une vidéo sans être dans le guide | **Tout texte publié reprend une source** (guide, page officielle) ; pas de promesse ajoutée par style | Relecture « chaque phrase a une source » avant rendu |
| 18/10 | Tarif N26 : le communiqué de 2025 (« trading gratuit ») contredisait la page actuelle (0,90 €) | La page actuelle prime sur un communiqué ancien ; dater chaque fait | Citer la page et la date |
| 05/10 | État d'un site prospect affirmé sans revérification | Revérifier en ligne le jour même | `44` |

## Documents, visuels, vidéos

| Date | Erreur | Règle | Garde-fou |
|---|---|---|---|
| 28/09 | PDF à effets mal affiché sur le téléphone de l'utilisateur | PDF à effets = image 300 ppp, contrôle sur 2 moteurs | `44` |
| 18/10 | Voix de synthèse : la consigne de style était **lue à voix haute** | Ne jamais envoyer de consigne au modèle de voix ; texte seul | Transcription automatique de chaque phrase (`videos/conseils/fabriquer.py`) |
| 18/10 | Barre de progression d'une vidéo pleine en 1 s (variable jamais transmise) ; 1re image vide (vignette) ; titre final sur le bandeau | Contrôler une vidéo à 0, 25, 50, 75 et 100 % et ses transitions **avant** de l'envoyer | Contrôles bloquants dans `fabriquer.py` (barre à 50 %, 1re image) |
| 18/10 | « : » et « ? » en début de ligne, apostrophes droites | Typographie française : insécable avant « : ; ? ! », apostrophe ’ | Fonction `insecables()` |
| 18/10 | Carte « avis » rendue avec une police de secours (chemins `/moteur/polices/` hors du site) | Hors du site, incorporer les polices (data URI) et vérifier `document.fonts` | `kit_avis.py`, `fabriquer.py` |
| 18/10 | Légendes Instagram avec une adresse écrite (non cliquable sur Instagram), contraire à la règle notée en tête du même fichier | Une légende se contrôle **par réseau** : lien cliquable sur Facebook et X seulement ; Instagram et TikTok → « lien dans la bio », et seulement si la bio a bien un lien | `caption.py` (`.claude/skills/ig-caption/`) sur chaque légende avant publication |
| 18/10 | Envoi de 2 vidéos **avant** le contrôle complet (défauts trouvés ensuite) | **Rien n'est envoyé avant le contrôle complet de `44`**, même une « première version » | Ce registre, relu avant chaque envoi |

## Site et référencement

| Date | Erreur | Règle | Garde-fou |
|---|---|---|---|
| 18/10 | Post « flyer » sur la fiche Google avec **téléphone et email dans le texte et sur l'image** : Google a supprimé le post et **désactivé les publications de la fiche** | **Fiche Google : jamais de téléphone, d'email ni de compte de réseau social dans un post (texte ni image)** ; utiliser le bouton « Appeler » ; lire le règlement des posts (support.google.com/business/answer/7213077) avant tout nouveau type de contenu sur une plateforme | Avant toute publication « gmb » : chercher numéro (`0[1-9]( ?\d\d){4}`), « @ » et réseaux dans le texte, et ne jamais réutiliser un visuel portant des coordonnées |
| 15/10 | Ancien CSS servi par le cache, correctif aléatoire en ligne | Changer le `?v=` des liens à chaque modification d'un CSS mis en cache | `CLAUDE.md` (polices) |
| 18/10 | `www.dig16.fr` répondait en 200 (site en double pour Google) | Une seule adresse ; vérifier les deux variantes avec `curl` | `functions/_middleware.js` |
| 18/10 | 6 images sans texte alternatif sur l'accueil | Toute image publique a un `alt` | `audit_acces.py`, OpenRush `audit_site` |

## Outils, relais, quotas

| Date | Erreur | Règle | Garde-fou |
|---|---|---|---|
| 30/09, 17/10 | Cookie du relais posé sur l'adresse du déploiement au lieu de l'alias utilisé par les outils | Lien de partage demandé sur `relais-dig-justok1.vercel.app` (l'alias), puis test `/api/video` | Consigne du rappel « cookie » |
| 18/10 | Quota gratuit de la voix épuisé en pleine série (essais ratés comptés) | Tester sur 1 phrase avant une série ; garder le cache ; prévoir la reprise | Cache `voix/` + rappel de reprise |
| 18/10 | `flyer_reseaux.py` écrivait un HTML temporaire contenant le téléphone de `identite.json` : CodeQL l'a bloqué (donnée privée stockée en clair) | Aucune donnée de l'identité n'est écrite sur disque par un outil du dépôt : la poser dans la page (Playwright `evaluate`) ou dans le fichier final privé seulement | Analyse CodeQL à chaque push |
| 24/09 | 56 validations manuelles demandées à l'utilisateur | Anticiper les permissions avant toute action en série | `CLAUDE.md` |

## Apprendre en continu (au-delà des erreurs)

- Chaque lien envoyé : résumé, trié, appliqué ou mis en réserve prête (`reserve-prete.md`), registre `46`.
- Veille quotidienne des sources (`veille_sources.py`), skills installés après lecture complète.
- Auto-analyse 2 fois par semaine (`ameliorer_systeme.py`) : corrections de l'utilisateur → règles et contrôles ici.
- Chaque bonne pratique qui a marché (ex. transcription de contrôle, contrôles bloquants dans les outils) est
  réutilisée sur les autres outils du même type.
