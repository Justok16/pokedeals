# Base de connaissances vidéo

Résumés de vidéos YouTube demandés par l'utilisateur, produits par Gemini
(offre gratuite, clé de l'utilisateur stockée dans Vercel) via le relais
`outils/relais-vercel` (`/api/chaine` pour lister une chaîne, `/api/video`
avec `mode=finance` pour une fiche de connaissances).

- `finary/` : chaîne YouTube Finary (finances personnelles, patrimoine,
  fiscalité) — 965 vidéos au 26/09/2026 (378 longues, 185 h ; 587 courtes).
  Lots quotidiens (limite gratuite : 8 h de vidéo par jour) :
  `python3 outils/resumer_chaine.py connaissances/finary/liste-videos.json connaissances/finary cookies.txt 60 finance`

Règles : ce sont des connaissances générales **non vérifiées** ; toute règle
fiscale, tout plafond ou tout taux est revérifié sur la source officielle
(impots.gouv.fr, service-public.fr, Légifrance, AMF) avant d'être affirmé.
Finary vend une application et des services : les passages promotionnels sont
signalés comme tels dans les fiches.
