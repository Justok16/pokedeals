# Atlassian Data Center : fin de vie le 28/03/2029 — mesure (24/09, soir)

## Faits (source primaire : atlassian.com/licensing/data-center-end-of-life)

- 30/03/2026 : plus de nouveaux abonnements Data Center (DC) ni de nouvelles
  apps DC pour les **nouveaux** clients.
- 30/03/2028 : fin des achats et extensions pour les clients existants.
- **28/03/2029 : fin de vie ; produits DC et apps associées en lecture
  seule.**
- Atlassian montre aux clients qui migrent des **alternatives cloud** aux
  apps qui ne seront pas portées (support.atlassian.com, « Cloud alternatives
  to your Atlassian Marketplace Data Center & Server apps », 25/09/2025),
  choisies notamment d'après ce que les autres clients ont pris.
- Non vérifié à la source primaire (source secondaire seulement) :
  Bitbucket DC recevrait une licence hybride et ne serait pas concerné de la
  même façon. Les apps Bitbucket sont donc laissées de côté.

## Mesure (API publique de la boutique ; outils `atlassian_dc.py`,
## `atlassian_dc_alternatives.py`)

| | Nombre |
|---|---|
| Apps DC listées | 1 598 |
| Sans version cloud sous la même clé | 755 |
| … dont payantes | 573 |
| … dont l'éditeur a une app cloud au nom proche | 73 |
| … sans aucune alternative cloud bien notée trouvée (≥ 4★, ≥ 10 avis) | 42 (5 766 installations au total) |

Lecture des plus grosses apps DC sans version cloud (vérification manuelle) :
- **Impossibles en cloud** (accès serveur, base de données, fichiers,
  changement d'utilisateur) : Integrity Check, Power Admin, User Switcher,
  Home Directory Browser, Switch User… → pas de marché cloud.
- **Couvertes nativement par le cloud** (point 14 : absorption) : SSO/SAML
  et 2FA (Atlassian Guard), **bannière d'annonce Confluence** (native en
  cloud depuis 2024, vérifié : support.atlassian.com, « Post Confluence-wide
  announcements in a banner »), dernières connexions (administration).
- **Déjà remplacées** par des apps cloud installées : configuration de
  projets (CMJ), formulaires (ProForma est devenu natif à JSM), graphiques,
  notifications email, LaTeX, versions de documentation.
- Les 42 « trous » restants sont petits (le plus gros : Last Log for Jira,
  1 473 installations, une fonction d'administration que le cloud fournit
  en partie).

## Conclusion

**Écarté.** La fin de vie Data Center est massive, mais le trou côté apps
est presque entièrement bouché : ce qui n'a pas été porté est soit
impossible en cloud, soit déjà natif, soit déjà remplacé — et Atlassian
oriente lui-même les clients vers les remplaçants existants. Contrairement
à la fin de Connect (apps cloud figées, clients qui paient déjà dans le
cloud), il n'y a pas ici de base payante orpheline à reprendre.

Données brutes : `outils/dc.csv`, `outils/dc_alternatives.csv` (relevé du
24/09/2026).
