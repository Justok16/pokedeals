# Tri des 30 vidéos prioritaires Melvynx + Matt Wolfe (01/10/2026)

Synthèse Gemini (gemini-flash-lite-latest, via `/api/avis`) des 30 fiches `connaissances/melvynx/` et
`connaissances/mreflow/` (15 + 15), puis **contrôle à la main** : chaque affirmation reprise ici a été
relue dans la fiche source, et chaque offre gratuite vérifiée sur la page officielle le 01/10/2026.
Les affirmations des créateurs restent des affirmations (non vérifiées sauf mention).

## Ce qui est retenu et appliqué

| Enseignement | Source | Vérification | Décision pour Dig |
|---|---|---|---|
| Skills de design anti « site IA générique » | melvynx RkzkLpLuY1E, mreflow STH929HARLo | — | **Déjà en place** : `taste-design`, `taste-redesign`, `impeccable`, `ui-ux-pro-max` ; **ajouté le 01/10** : `frontend-design`, skill officiel d'Anthropic cité par la vidéo (texte seul, licence Apache 2.0, lu en entier avant installation) |
| Maquette par « inspiration croisée » : prendre le meilleur de 4 sites différents, ne jamais en copier un seul | melvynx RkzkLpLuY1E | relu dans la fiche | **Appliqué** aux prochaines démos (règle ajoutée ci-dessous) |
| Hébergement gratuit relié à GitHub | melvynx Swp29OiGs80 (Netlify) | — | **Déjà en place** avec Cloudflare Pages (site Dig) ; pas besoin de Netlify |
| Skills courts ; `disable-model-invocation: true` pour un skill qu'on veut lancer seulement à la main | melvynx GUvJsd964fA | **Confirmé** par la doc officielle Claude Code (code.claude.com/docs/en/skills, lue le 01/10) | Noté. Non appliqué à nos skills : la routine automatique doit pouvoir les utiliser seule |
| Mini-outils gratuits sans inscription pour attirer des visiteurs (« engineering as marketing ») | melvynx HLCurWw88bM | relu dans la fiche | Confirme la ligne « À faire » n° 11 (outil gratuit sur le site Dig, grille anti-DigCost d'abord) |
| Dictée vocale Wispr Flow | mreflow p7SRuKWZMvQ | **Offre gratuite confirmée** (wisprflow.ai/pricing, lu le 01/10) : Mac, Windows, iOS et Android ; 2 000 mots/semaine sur ordinateur, 1 000 sur téléphone | **Proposé à l'utilisateur** (il travaille surtout au téléphone) ; installation de son côté |
| NotebookLM pour transformer les documents d'un artisan en textes de site | mreflow p7SRuKWZMvQ | gratuit selon la vidéo, à vérifier avant usage | À tester au premier client (documents du client, avec son accord) |

## Ce qui est écarté (et pourquoi)

| Proposition | Raison |
|---|---|
| Relume (« gratuit ») pour les maquettes | Page officielle lue le 01/10 : l'offre gratuite se limite à 30 composants, puis abonnement ; Claude Code + nos skills font déjà le travail |
| Images générées par IA (Bing Image Creator) pour illustrer les sites d'artisans | Jamais pour montrer des « réalisations » : ce serait trompeur pour les clients de l'artisan (pratique commerciale trompeuse). Seulement pour des décors neutres, avec la mention « image générée par IA » |
| « Ne pas faire de SEO au début » | Erreur de la synthèse automatique : le conseil de Melvynx concerne le lancement de **son** logiciel, pas le référencement local d'un artisan. Pour Dig, la fiche Google et le référencement local restent au cœur de l'offre |
| Lovable, Dub et autres abonnements | Payants ; budget 0 € |

## Règle ajoutée aux démos

Avant chaque démo : relever 3 ou 4 sites de référence du métier (pas seulement des concurrents
locaux), noter pour chacun l'élément à reprendre (en-tête, galerie, bloc contact, avis), puis
composer une maquette originale. Ne jamais reproduire la mise en page complète d'un site existant.
