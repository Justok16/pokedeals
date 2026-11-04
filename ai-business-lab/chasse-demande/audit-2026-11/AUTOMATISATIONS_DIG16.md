# Automatisations DIG16 — état et améliorations

Vérifié le **04/11/2026**. Principe suivi : améliorer l'existant, ne pas ajouter une automatisation en double.

## 1. Ce qui tourne et a été vérifié (FAIT ET VÉRIFIÉ)

| Automatisation | Fréquence | Dernier résultat |
|---|---|---|
| Sentinelle dig16.fr (GitHub Actions) | toutes les 3 h | active ; ouvre une issue « Alerte DIG16 » en cas de problème |
| Contrôle global (point de Claude) | 2 fois par jour | 18/18 OK le 04/11 |
| Tests de la CI (`tests.yml`) | à chaque envoi | verts sur la PR #118 (04/11) |
| CodeQL | chaque semaine | actif |
| Courrier, publications, veille | quotidiens | exécutés le 04/11 |
| Veille fiscale | le 3 de chaque mois | 03/11 : valeurs inchangées |

## 2. Améliorations faites pendant l'audit

| Changement | Pourquoi | Vérification | Retour arrière |
|---|---|---|---|
| **13 tâches PokéDeals arrêtées** (PR #172, fusionnée le 04/11) | Application abandonnée : un échec quotidien (SendGrid), des minutes de CI et du bruit dans les courriels | `git show origin/main` : seuls `sentinelle_dig16.yml` et `codeql.yml` restent programmés | Remettre les blocs `schedule` (historique de la PR #172) |
| **Nouveau job `outils_dig16`** dans `tests.yml` | Les outils de gestion DIG16 n'avaient pas de tests en CI | 9 tests réussis en local ; YAML relu (`yaml.safe_load`) | Retirer le job |
| **Livre des recettes + préparation du e-reporting** (`outils/compta/`) | Obligation légale non couverte par l'offre gratuite d'Indy ; préparation de septembre 2027 | 9 tests | Supprimer le dossier (aucune autre dépendance) |
| **Rappel du 04/05/2027** (facturation électronique) | L'échéance du 01/09/2027 ne doit pas être oubliée | Tâche `trig_01NtmbRzdCZSdDdsMK21ikx1` créée | La supprimer |
| **CSP resserrée** (`_headers`) | Domaine Cloudflare Web Analytics inutile | `test_pages.py` propre, formulaire OK | Remettre les deux domaines |

## 3. Pistes examinées et non retenues

- **Nouvel outil de détection des secrets** : non retenu. `detect-secrets` est déjà dans le crochet d'avant commit, et
  un scan complet a été fait le 04/11.
- **Tableau de bord des clients** : non retenu, car il n'y a pas encore de client (règle « pas de construction sans
  demande », `39` § 6.4). À faire au premier client.
- **Import automatique depuis Indy** : bloqué, faute d'API publique. Il faudrait se connecter au compte de l'utilisateur,
  ce qui est interdit. Voir FACTURATION § 5.

## 4. Recommandations

1. **Sauvegarde durable des données privées** (priorité haute). Le point du soir copierait chaque jour `ETAT.md` et les
   nouveaux lots dans le Drive « Dig ». Le Drive est déjà utilisé et gratuit. À brancher dans la consigne du point de
   19:34 (A2 du plan d'action).
2. **Rapport mensuel automatique du livre des recettes**, à faire au premier encaissement : la veille fiscale du 3 lance
   `livre_recettes.py` et signale une alerte de seuil.
3. **Quota Zapier épuisé chaque mois** (stories Buffer) : la solution manuelle prévue suffit. Pas d'abonnement payant
   (budget 0 €).
