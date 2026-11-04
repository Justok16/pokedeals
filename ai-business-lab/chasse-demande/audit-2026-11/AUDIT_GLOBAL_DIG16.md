# Audit global DIG16 — synthèse

**Date de vérification : 04/11/2026** (entre 21 h 30 et minuit, heure de Paris).

Documents de l'audit, dans ce dossier :
- inventaire : `INVENTAIRE_RESSOURCES_DIG16.md` ;
- facturation électronique : `FACTURATION_ELECTRONIQUE_DIG16.md` ;
- protection des données : `CONFORMITE_RGPD_DIG16.md` ;
- automatisations : `AUTOMATISATIONS_DIG16.md` ;
- plan d'action : `PLAN_ACTION_DIG16.md` ;
- journal des changements : `CHANGELOG_AUDIT.md`.

## Sources principales (toutes lues le 04/11/2026)

- impots.gouv.fr :
  - « Je consulte la liste des plateformes agréées », modifiée le 03/11/2026, et ses fichiers XLSX ;
  - « Fréquences et délais de transmission (e-reporting) » ;
  - FAQ « J'approfondis la facturation électronique », version du 01/09/2026.
- entreprendre.service-public.gouv.fr/vosdroits/F23266 : obligations comptables du micro-entrepreneur, vérifié le
  07/09/2026.
- CNIL, « Cookies : solutions pour les outils de mesure d'audience », page du 04/07/2025.
- Aide Indy (wikicompta) :
  - article 16596548, daté du 31/08/2026 ;
  - article 17058407, daté du 22/09/2026 ;
  - page tarifs d'Indy.
- Pages tarifs de Tiime et d'Abby.
- Mesures locales : `controle_global.py`, `audit_securite.py`, `test_pages.py`, `test_formulaire.py`, `detect-secrets`,
  `git grep`.

## Résultat par domaine

| Domaine | Niveau | Résumé |
|---|---|---|
| Administratif et réglementaire | Bon | Les démarches sont suivies dans 64 avec des rappels datés. La CFE est à déposer avant le 31/12 (rappel du 10/12). |
| Facturation électronique, réception | **Conforme** | Indy est désigné plateforme agréée depuis le 16/10/2026. **La mission le croyait à faire : c'est déjà fait.** |
| Facturation électronique, émission et e-reporting | Préparé | Obligatoires au 01/09/2027. Pas encore ouverts chez Indy. Outil de préparation livré et testé. Rappel le 04/05/2027. Un point est à lever : données de paiement pour un franchisé (la DGFiP dit oui). |
| Factures clients et fournisseurs | Prêt, non utilisé | Aucun client ni fournisseur facturé à ce jour. Le livre des recettes, obligatoire, est maintenant outillé. |
| Protection des données | Correct, 2 points à vérifier | Pas de cookie, polices sur le site, formulaire chiffré et protégé du spam. À vérifier : exemption CNIL du compteur Metricool, encadrement des transferts vers les États-Unis (FormSubmit, Cloudflare). |
| Sécurité informatique | Très bon | Note de 100/100 à l'audit passif, DNSSEC, SPF, DMARC, HSTS. Aucun secret dans le dépôt. CSP resserrée. |
| Automatisations | Bon, allégé | 13 tâches PokéDeals inutiles arrêtées ; tests DIG16 ajoutés à la CI. |
| Qualité des sites | Bon | Toutes les pages et les démos sont propres sur 7 largeurs d'écran (`test_pages.py`). |
| Documentation et maintenance | Bon | `CARTE.md` est à jour, ainsi que les leçons et l'inventaire des outils. Point faible : les données privées vivent dans un conteneur éphémère (A2). |

## Synthèse des actions de l'audit

**FAIT ET VÉRIFIÉ**
1. Inventaire du dépôt, des outils, des automatisations, des secrets et des données personnelles.
2. Statut officiel des 4 plateformes : toutes dans la liste définitive du 03/11/2026.
3. Arrêt des tâches PokéDeals (PR #172).
4. CSP resserrée, avec tests du site et du formulaire.
5. Livre des recettes et préparation du e-reporting (9 tests), ajoutés à la CI.
6. Rappel du 04/05/2027.
7. Ces sept documents.

**FAIT MAIS NON TESTÉ**
- Le job CI `outils_dig16` ne sera exécuté par GitHub qu'au prochain envoi. Il a été testé en local.

**À FAIRE** : A4 (transferts hors UE), B1 à B4 (au premier client).

**BLOQUÉ**
- A1 : « Audit 0.4.5 » introuvable.
- Import automatique depuis Indy : pas d'API publique, connexion au compte interdite.

**À DÉCIDER par l'utilisateur**
- A2 : sauvegarde hebdomadaire au Drive.
- A3 : compteur de visites.

**HYPOTHÈSE**
- Les données de paiement sont dues par un franchisé en base. C'est la lecture de la DGFiP, différente de celle d'Indy ;
  la question sera tranchée en mai 2027.

## Tests exécutés le 04/11/2026

| Test | Résultat |
|---|---|
| `outils/controle_global.py` | 18/18 OK |
| `outils/audit_securite.py https://dig16.fr` | 100/100 |
| `outils/test_pages.py` (après la modification de la CSP) | « Toutes les pages sont propres » |
| `outils/test_formulaire.py site-dig` | OK, aucun refus CSP |
| `python3 -m unittest discover -s outils/compta` | 9 tests OK |
| `ruff check outils/compta` | 0 erreur |
| `detect-secrets scan` | 9 signalements, tous faux positifs |
| CI de la PR #118 (avant ces changements) | Cloudflare Pages, pytest et scoring : verts |
