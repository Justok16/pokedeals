# Slack : fin des « classic apps » le 16/11/2026 — mesure (24/09, soir)

## Faits (source primaire)

- docs.slack.dev, « Discontinuing support for legacy custom bots and classic
  apps » : « beginning November 16, 2026, classic apps will no longer
  function » (appels d'API rejetés, plus d'événements).
- docs.slack.dev, « Classic apps deprecation timeline adjustment »
  (29/07/2025) : date repoussée au 16/11/2026.
- Plus aucune nouvelle app classic acceptée depuis décembre 2020.

## Mesure (`outils/slack_classic.py`, sitemap public de la Slack Marketplace)

Une fiche est comptée « classic » si elle demande la permission générique
`bot` (et les permissions associées `rtm:stream`, `chat:write:bot`), qui
n'existent pas pour les apps à permissions granulaires.

| | Nombre |
|---|---|
| Apps de la Marketplace (en-us) | 2 743 (36 pages illisibles) |
| **Encore classic** | **106** (3,9 %) |
| … dont prix affiché payant ou mixte | 15 |
| … dont sans prix affiché (souvent abandonnées) | 79 |

Exemples notables : Dropbox, Dropbox Paper, Evernote, Olark, Zoho Survey,
Oracle CX Sales & Service, Teampay, Heymarket, Kipwise Wiki, et les apps
Atlassian « Jira Server », « Confluence Server », « Bitbucket Server ».

## Grille (points éliminatoires)

- Point 5 (preuve de paiement) : Slack ne facture pas les apps et ne publie
  aucun nombre d'installations → impossible de mesurer la base payante.
- Point 14 (absorption) : les grands éditeurs (Dropbox, Evernote, Oracle,
  Atlassian) migreront eux-mêmes ou remplaceront par une fonction native.
- Pas de procédure de transfert d'app entre éditeurs (contrairement à
  Atlassian) → pas de reprise possible.
- Point 18 (timing) : 7 semaines avant la date.

## Conclusion

**Écarté.** À revoir une fois, **après le 16/11/2026** : si une app classic
très utilisée disparaît sans remplaçant (plaintes publiques sur les
forums), la demande sera visible et mesurable. Données :
`outils/slack.csv`.
