# Journal des changements de l'audit (04/11/2026)

Chaque ligne indique le changement, le fichier, la vérification et le retour arrière.

| # | Changement | Fichier(s) | Vérification | Retour arrière |
|---|---|---|---|---|
| 1 | Arrêt des 13 tâches programmées PokéDeals (demande de l'utilisateur) | `.github/workflows/*.yml` sur la branche principale (PR #172, fusionnée) | YAML relu ; `cron` restants : `sentinelle_dig16.yml` et `codeql.yml` seulement | Rétablir les blocs `schedule` depuis la PR #172 |
| 2 | CSP : retrait de Cloudflare Web Analytics, non utilisé | `site-dig/_headers` | `test_pages.py` : pages propres ; `test_formulaire.py` : OK | Historique git (commit 65b3b6dba) |
| 3 | Nouvel outil livre des recettes + préparation du e-reporting | `outils/compta/livre_recettes.py`, `outils/compta/test_livre_recettes.py` | 13 tests réussis ; `ruff` sans erreur | Supprimer `outils/compta/` |
| 4 | Tests DIG16 en CI | `.github/workflows/tests.yml` (job `outils_dig16`) | `yaml.safe_load` : 3 jobs ; vert sur GitHub le 04/11 | Retirer le job |
| 5 | Rappel « facturation électronique 2027 » | tâche programmée `trig_01NtmbRzdCZSdDdsMK21ikx1` (04/05/2027) | Création confirmée par l'outil | Supprimer la tâche |
| 7 | Audit Migration 0.4.5 intégré **sans modification** (version 0.4.5 conservée) + étape CI (intégrité + 50 tests) + point 12 de `65` | `outils/migration_audit/`, `.github/workflows/tests.yml`, `65-seo-sites-clients.md` | SHA-256 de l'archive = ab8c6660…eebe7 ; 50/50 tests (Python 3.11 et 3.13) ; reconstruction identique | Supprimer le dossier, l'étape et le point 12 |
| 6 | Sept documents d'audit | `audit-2026-11/*.md` | Relus | Supprimer le dossier |

Aucun fichier existant n'a été écrasé, à part les trois modifications ciblées ci-dessus (lignes 1, 2 et 4). Rien n'a été
supprimé. Aucun compte créé, aucun mandat signé, aucune donnée envoyée à un tiers.
