# Inventaire des ressources DIG16

Relevé le **04/11/2026** par commandes sur le dépôt (`git`, `find`, `du`) et par les outils connectés (tâches
programmées, GitHub, Drive). La carte fichier par fichier existe déjà et reste la référence : `CARTE.md`, régénérée par
`outils/carte.py`. Le contrôle global du 04/11 la dit « à jour ».

## 1. Dépôt et sauvegardes

| Élément | État | Constat |
|---|---|---|
| Dépôt `Justok16/pokedeals` (GitHub) | Opérationnel | **Public**. 8 249 commits depuis le 05/07/2026 ; dossier `.git` de 644 Mo. Branche de travail DIG16 : `claude/ai-business-portfolio-strategy-96yf4g` (PR #118 ouverte, CI verte le 04/11). |
| Sauvegarde du code | Opérationnelle | GitHub (chaque commit est poussé). Jamais de réécriture d'historique. |
| Données privées (prospects, clients, identité) | **À risque** | Dans le scratchpad du conteneur, **effacé quand le conteneur est recyclé**. Copies partielles dans le Drive « Dig » (lots d'appels). Archive locale faite le 04/11 : `scratchpad/audit/sauvegarde-prive-2026-11-04.tgz`, 49 Mo, SHA-256 `d4480cf3…0dcb1450`. Elle reste dans le conteneur : **ce n'est pas une sauvegarde durable**. Voir le plan d'action, A2. |
| Drive « Dig » | Opérationnel | Documents privés : fiches d'appels, lots, kits. |

## 2. Projets dans le dépôt

| Projet | Dossier | État | Lien avec DIG16 |
|---|---|---|---|
| **DIG16** (sites pour artisans) | `ai-business-lab/chasse-demande/` | **Actif** | C'est l'entreprise |
| Site dig16.fr | `chasse-demande/site-dig/` (164 Mo) | **En ligne** (Cloudflare Pages, projet « digsite ») | Vitrine |
| Démos de sites | `site-dig/demos/`, `site-dig/m/` (maquettes chiffrées) | Actif, hors diffusion sans accord | Prospection |
| Stratégie et portefeuille | `ai-business-lab/*.md`, `ai-business-lab/outils/scorer.py` | Historique (septembre) ; tests en CI | Contexte |
| **PokéDeals / PokéPrécoms** | `scraper/`, 13 workflows | **Abandonné** (l'utilisateur, 04/11) | Aucun. Tâches programmées arrêtées le 04/11 (PR #172 fusionnée) ; le code est gardé |
| Carte « voyage Japon » | autre dépôt `voyage-japon-2030-outils` + tâches 2029 | Personnel, en sommeil | Aucun (hors périmètre de cette conversation) |

## 3. Outils DIG16 (`chasse-demande/outils/`)

- **109 scripts Python**, plus des modèles (`modeles/`), le relais Vercel (`relais-vercel/`) et Unlighthouse.
- Inventaire des outils et services : `connaissances/inventaire-outils.json`, 77 outils, avec version, licence et veille
  quotidienne.

Familles et outils principaux, tous opérationnels au 04/11 sauf mention :

| Famille | Outils | Vérification du 04/11 |
|---|---|---|
| Santé et sécurité du site | `controle_global.py`, `sentinelle_dig16.py` (GitHub Actions, toutes les 3 h), `audit_securite.py`, `test_pages.py`, `test_formulaire.py`, `audit_acces.py`, `qa_site.py` | 18/18 OK ; 100/100 ; pages propres ; formulaire OK |
| Documents clients | `kit_client.py`, `documents_client.py`, `accord_gracieux.py`, `pdf_remplissable.py`, `charte_client_pdf.py`, `contrat_mandat_pdf.py`, `modeles_docuseal.py` | Non relancés (aucun client) |
| Prospection | `outils/prospects/` (fiche d'appel, comparatif de site), `verif_entreprises.py`, `suivi_siren.py`, `trouver_contact.py` | Utilisés les 03 et 04/11 |
| Fiscalité et comptabilité | `fiscal/simulateur.py`, **`compta/livre_recettes.py` (nouveau)** | 9 tests réussis (nouveau) |
| Référencement | `indexnow.py`, `pages_markdown.py`, `seo_client.py` | — |
| Réseaux et vidéos | `marque/publications_v2.py`, `controle_voix_videos.py`, résumés de vidéos | Utilisés le 04/11 |
| Veille | `veille_sources.py`, `veille_outils.py`, `veille_presse.py`, `radar_fermetures.py` | Quotidienne |
| Qualité des textes | `orthographe.py`, `typo_fr.py`, `lisibilite.py`, `anti_generique.py` | — |
| Héritage de septembre (catalogues d'applications) | `bigcommerce_apps.py`, `hubspot_apps.py`, `wix_apps.py`, `zoom_apps.py`… | **Plus utilisés** (étude de marché close). Gardés, à ne pas supprimer (consigne) |

## 4. Automatisations

| Type | Nombre | Détail |
|---|---|---|
| Workflows GitHub actifs (programmés) | 2 | `sentinelle_dig16.yml` (toutes les 3 h), `codeql.yml` (hebdomadaire) ; `tests.yml` à chaque envoi |
| Workflows PokéDeals | 13 | Programmation retirée le 04/11 (lancement manuel encore possible) |
| Tâches programmées Claude | plus de 15 actives | Courrier (2 par jour), points 07:34 et 19:34, contrôle du soir des publications, publications manuelles, Charente Libre, veille des outils (09:41), veille fiscale (le 3), appels du mardi et du jeudi, relances datées (CCI, maçon, Athanas), échéances (CFE, ACRE, impôts 2027), **facturation électronique 2027 (créée le 04/11)** |
| Crochets Claude Code | 8 | Secrets avant commit, syntaxe Python, quotas de publication, « vérifier avant d'agir », réserve à proposer… (`.claude/hooks/`) |
| Services externes | — | Metricool (marque 7154026), Buffer par Zapier (quota de novembre épuisé), Gmail, Drive, Agenda, DocuSeal, Vercel (relais), Cloudflare Pages, Indy, GoCardless (inscription à faire), vidIQ |

## 5. Dépendances entre projets

```
dig16.fr (Cloudflare Pages) ← site-dig/ ← test_pages.py, test_formulaire.py, indexnow.py
        ↑ surveillé par : sentinelle_dig16.yml (GitHub, branche principale) + controle_global.py (points Claude)
        → FormSubmit (formulaire) → contact@dig16.fr
        → Metricool (compteur de visites)
outils/prospects → registre officiel (relais Vercel /api/cc, cookie de 22 h) + BODACC → lots privés (scratchpad, Drive)
kit_client / documents_client → données JSON privées → PDF hors dépôt → DocuSeal (signature) → Drive « Dig »
Indy (factures, plateforme agréée, compte pro) → livre_recettes.py (CSV privé) → contrôles franchise + e-reporting 2027
fiscal-valeurs.json → simulateur.py, livre_recettes.py ← veille fiscale du 3 de chaque mois
PokéDeals (scraper/) : aucune dépendance avec DIG16 (vérifié : sentinelle et outils DIG16 n'importent rien de scraper/)
```

## 6. Secrets et données personnelles (contrôle du 04/11)

- `detect-secrets` sur `ai-business-lab/`, `.claude/` et `.github/` : 9 fichiers signalés. Tous sont des **faux
  positifs** : empreintes de polices, identifiants publics de vidéos, exemples d'un skill, script inline du site. Aucune
  clé réelle.
- Courriels personnels (gmail, orange, free…) dans le dépôt : **aucun**.
- Numéros de mobile : seulement le numéro professionnel publié sur le site ; les autres correspondances sont des
  identifiants de publications X.
- Crochet `secrets_avant_commit.sh` actif sur chaque commit.

## 7. Audit 0.4.5 (BLOQUÉ)

Aucune trace de « Audit 0.4.5 » :
- ni dans le dépôt (`git grep`) ;
- ni dans le Drive (recherche par titre et contenu) ;
- ni dans Gmail.

Son intégration ne peut donc pas être vérifiée. Il faut à l'utilisateur dire où se trouve l'archive (lien ou dépôt). Rien n'a
été modifié.
