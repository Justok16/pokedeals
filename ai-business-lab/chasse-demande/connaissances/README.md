# Base de connaissances vidéo

Résumés de vidéos YouTube demandés par l'utilisateur, produits par Gemini
(offre gratuite, clé de l'utilisateur stockée dans Vercel) via le relais
`outils/relais-vercel` (`/api/chaine` pour lister une chaîne, `/api/video`
avec `mode=finance` pour une fiche de connaissances).

- `finary/` : chaîne YouTube Finary (finances personnelles, patrimoine,
  fiscalité) — 965 vidéos au 26/09/2026 (378 longues, 185 h ; 587 courtes).
  Limite gratuite constatée le 27/09 : ~20 vidéos par jour et par modèle ; l'outil
  alterne 7 modèles (≈ 140 vidéos/jour, soit environ une semaine pour tout) :
  `python3 outils/resumer_chaine.py connaissances/finary/liste-videos.json connaissances/finary cookies.txt 3000 finance`
- `fintales/` : chaîne YouTube Fintales (@fintales_media, finance et marchés),
  demandée le 28/09/2026 — 152 vidéos au 28/09/2026. À traiter **après** Finary,
  avec la même commande (dossier `connaissances/fintales`).

Règles : ce sont des connaissances générales **non vérifiées** ; toute règle
fiscale, tout plafond ou tout taux est revérifié sur la source officielle
(impots.gouv.fr, service-public.fr, Légifrance, AMF) avant d'être affirmé.
Finary vend une application et des services : les passages promotionnels sont
signalés comme tels dans les fiches.
