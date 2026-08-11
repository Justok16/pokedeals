# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Comments, log messages, config, and the README are in French (the user's language); code identifiers mix French and English. Keep new code/comments in French to match the existing style. **L'utilisateur est débutant en programmation** : explique en français, sans jargon technique non expliqué.

## Vue d'ensemble

PokéDeals est un bot d'alerte Pokémon TCG entièrement automatisé, sans serveur ni base de données : il tourne uniquement via des cron GitHub Actions, et persiste son état dans `data/*.json`/`.csv` que le bot commit lui-même dans le repo. Trois fonctions actives aujourd'hui, indépendantes les unes des autres :

1. **Radar de bonnes affaires historique** (`main.py`) — scanne eBay France, Vinted et Leboncoin (via alertes email) pour des cartes sous-évaluées par rapport à une cote calculée automatiquement, plus une intégration Cardtrader/Cardmarket pour affiner cette cote.
2. **Radar de stock/bonnes affaires boutiques TCG** — surveille **83 boutiques françaises et japonaises spécialisées** (Shopify, PrestaShop, WooCommerce) pour deux choses : une carte de la watchlist en-dessous du seuil de prix (🔥), ou un retour en stock d'une carte suivie (📦).
3. **Radar de précommandes anniversaire** — détecte l'apparition de produits scellés précis pas encore catalogués (🎉), actuellement le Coffret ETB 30e Anniversaire et le Coffret ETB ME06 Règne Delta (cf. `PRODUITS_SURVEILLES` dans `precommandes_watchlist.py` pour la liste à jour).

Les fonctions 2 et 3 partagent les mêmes connecteurs de scraping mais des logiques d'alerte et des fichiers mémoire séparés. Elles ne modifient jamais `main.py` ni ses fichiers de mémoire (`data/seen.json`, `data/cotes.json`, etc.).

## Architecture réelle

### Système historique (`main.py`)

Fichier unique (~3500 lignes), pas de module. Reste organisé en sections délimitées par des banners `# ====` : utilitaires HTTP/texte, filtres de pertinence d'annonce (`annonce_pertinente`), chargement config, état "vues" (dédup), connecteurs eBay/Cardtrader/Cardmarket/Vinted/Leboncoin, moteur de cote (`obtenir_cote`), évaluation de deal (`evaluate`), notifications Telegram/email, stats/CSV, orchestration (`collecter`/`main`). Chaque changement de règle non-trivial porte un commentaire `VNN:` expliquant le cas concret qui l'a motivé — c'est le changelog du fichier, à respecter pour tout nouveau changement.

`config.yaml` reste l'interface principale : `watchlist`, `regles`, `api_cotes`, `mes_achats`, `notifications`, `plateformes`. Il est partagé avec le système boutiques TCG (même `watchlist` de cartes, réutilisée par `watchlist_shopify.py`).

### Système boutiques TCG (connecteurs Shopify/PrestaShop/WooCommerce)

Architecture commune aux 3 plateformes : un connecteur découvre les URLs produit (sitemap XML en priorité), les résultats sont normalisés dans une structure `ResultatRecherche` partagée, puis passés à deux logiques d'alerte génériques qui ne dépendent d'aucun connecteur spécifique.

**Connecteurs :**
- `connecteur_shopify.py` — API publique `/products.json`. Héberge aussi les fonctions **partagées par les 3 connecteurs** : `_titre_correspond`, `_slug_correspond`, `_normaliser_texte`, `_regex_numero_sans_denominateur`, `_retirer_fractions`, `_est_xml_valide`, `detecter_langue`, ainsi que `HEADERS` (API JSON Shopify) et `HEADERS_HTML` (toutes les requêtes HTML des deux autres connecteurs — **ne jamais réutiliser `HEADERS` pour du HTML**, cf. section pièges ci-dessous).
- `connecteur_prestashop_sitemap.py` — sitemap XML + JSON-LD + repli microdata + repli recherche HTML (`?controller=search&s=`) pour les boutiques sans sitemap, + fix de désync stock DOM (`_stock_indisponible_selon_dom`).
- `connecteur_woocommerce.py` — sitemap XML (Yoast/AIOSEO/natif) + JSON-LD + repli recherche HTML (`?s=`) + repli API REST WooCommerce Store API (`rechercher_via_api_rest`, utilisé par `mymesis.fr`) + détection de produit variable (attribut "état").

**Watchlist et structures partagées :**
- `watchlist_shopify.py` — `CarteWatchlist`, parsing de `config.yaml` (`charger_watchlist_config`), extraction/détection du qualificatif ("ex"/"gx"/"v"/"vmax"/"vstar"), `NOMS_SET_QUALIFICATIF_AMBIGU` (liste curée à la main, voir pièges ci-dessous).

**Logiques d'alerte (génériques, agnostiques du connecteur) :**
- `bonne_affaire_shopify.py` — alerte 🔥, garde-fous stock → langue → qualificatif symétrique → décote ≥30%.
- `alerte_stock.py` — alerte 📦 retour en stock, **mêmes garde-fous dans le même ordre** que `bonne_affaire_shopify.py` (alignement fait le 2026-08-11, à préserver sur tout nouveau garde-fou).

**Orchestrateurs (un par plateforme, appelés par les workflows) :**
- `scan_boutique.py` — Shopify, boutiques actives dans `boutiques_shopify.py` (`BOUTIQUES_SHOPIFY`).
- `scan_boutique_prestashop.py` — PrestaShop, boutiques actives dans `boutiques_prestashop.py` (`BOUTIQUES_PRESTASHOP_SITEMAP` + `BOUTIQUES_PRESTASHOP_REPLI_HTML`).
- `scan_boutique_woocommerce.py` — WooCommerce, boutiques actives dans `boutiques_woocommerce.py` (`LOT_A`/`LOT_B` pour le sitemap, `BOUTIQUES_WOOCOMMERCE_REPLI_API_REST` pour `mymesis.fr`) ; scindé en 2 lots équilibrés par volume d'URLs (pas par nombre de boutiques) pour tenir dans le timeout du workflow.

Chaque fichier `boutiques_*.py` documente aussi, en commentaires, les boutiques diagnostiquées mais **volontairement non intégrées** (catalogue non pertinent, sitemap cassé côté site, rate-limit trop agressif, etc.) — vérifier là avant de ré-investiguer une boutique qui semble manquante.

### Radar de précommandes

Système **indépendant** des scans cartes ci-dessus (nouveaux fichiers, aucune modification des connecteurs/orchestrateurs existants) :
- `precommandes_watchlist.py` — `PRODUITS_SURVEILLES`, matching par mots-clés (deux groupes obligatoires : édition + type) + extraction/validation de date sur la page produit.
- `alerte_precommande.py` — mémoire d'état + alerte Telegram 🎉 (une seule fois par produit × boutique, avec re-alerte si la confiance passe de "moyenne" à "forte"). La toute première détection d'un couple (domaine, produit) établit une base de référence silencieuse, sans alerte — même principe qu'`alerte_stock.py`, pour éviter le spam au premier lancement.
- `radar_precommandes.py` — scanners par plateforme, réutilisent les connecteurs existants sans les modifier. Le préfiltre de slug (`_slug_est_candidat`) exige les deux groupes de mots-clés (édition ET type) avant de charger une page complète — voir pièges ci-dessous pour l'historique de ce choix.
- `scan_precommandes.py` — orchestrateur CLI (`python scan_precommandes.py {shopify|prestashop|woocommerce} [boutiques...]`), branché comme étape supplémentaire dans les 3 workflows de scan boutiques (pas de workflow séparé). S'arrête de lui-même une fois tous les produits surveillés passés leur date de sortie.

### Modules transverses

- `telegram_utils.py` — `echapper_html`/`echapper_url_html`, partagés par les 3 modules d'alerte boutiques TCG.
- `memoire_json.py` — `charger_memoire`/`sauvegarder_memoire` génériques pour un fichier JSON, partagés par `alerte_stock.py` et `alerte_precommande.py`.

## CI/déploiement — 4 workflows GitHub Actions

Tournent en parallèle sur le même repo, chacun avec son propre groupe de concurrence (`concurrency.group`) pour ne jamais se bloquer mutuellement, et une étape de sauvegarde mémoire avec dance stash/pull-rebase/push pour éviter les collisions Git entre crons qui se chevauchent.

| Workflow | Cadence | Timeout | Contenu |
|---|---|---|---|
| `pokedeals.yml` | 15 min | 15 min | `main.py` (système historique) |
| `scan_shopify.yml` | 30 min | 25 min | scan cartes Shopify + radar précommandes Shopify |
| `scan_prestashop.yml` | 30 min | 30 min | scan cartes PrestaShop + radar précommandes PrestaShop |
| `scan_woocommerce.yml` | 30 min | 22 min (lot A) + 18 min (lot B) + 25 min (précommandes) | 3 jobs séquentiels (`needs:`) : scan cartes lot A, lot B, puis radar précommandes (lot A + lot B) |

`scan_woocommerce.yml` est le seul à jobs multiples (nécessaire car son plus gros catalogue à lui seul dépasse le budget d'un run simple) ; les jobs sont **séquentiels**, jamais en parallèle entre eux au sein d'un même run, pour éviter une course d'écriture sur le même fichier mémoire.

Avant de changer un timeout ou une composition de lot, vérifier `SESSION_NOTES.md` (section diagnostic du flake `scan_lot_a`) — les marges mesurées en prod y sont documentées, ne pas ajuster à l'aveugle.

## Fichiers de mémoire (`data/*.json`)

Deux familles de schéma, une par fonctionnalité, jamais mélangées :
- **Stock/bonnes affaires** (`seen.json`, `cotes.json`, `anciennete_annonces.json` pour `main.py` ; `stock_boutiques_tcg.json`/`stock_boutiques_tcg_prestashop.json`/`stock_boutiques_tcg_woocommerce.json` — un fichier **par plateforme**, séparés justement pour éviter les collisions entre workflows parallèles).
- **Précommandes** (`precommandes_anniversaire_{shopify,prestashop,woocommerce}.json` — un fichier par plateforme, clé `{domaine}|{nom_produit}`, valeurs `{confiance, raison, titre_produit, url_produit, derniere_verification}`).

## Commandes

```bash
pip install -r requirements.txt        # requests + PyYAML, seules dépendances de PROD
pip install -r requirements-dev.txt    # + pytest, pour lancer les tests (jamais installé en prod)
python -m pytest tests/ -v             # tests unitaires (~20 cas, sub-seconde) sur les fonctions les plus fragiles
python main.py                         # système historique : un scan complet
python scan_boutique.py [boutiques]    # scan cartes Shopify (vide = toutes les boutiques actives)
python scan_boutique_prestashop.py [boutiques]
python scan_boutique_woocommerce.py [boutiques]
python scan_precommandes.py {shopify|prestashop|woocommerce} [boutiques]
```

`tests/` couvre les fonctions de matching les plus sujettes à régression (`detecter_langue`, `_retirer_fractions`, `detecter_qualificatif_titre`, `evaluer_deal`) — un cas par bug réel déjà rencontré en prod (cf. pièges connus ci-dessous et `SESSION_NOTES.md`). Lancé automatiquement par `.github/workflows/tests.yml` sur chaque push/PR, workflow séparé des 4 workflows de scan (pas de secrets, pas d'écriture sur `data/`). Ce n'est pas une couverture exhaustive : pas de test sur les connecteurs eux-mêmes (nécessiterait des fixtures HTML/JSON par plateforme, pas fait à ce stade) ni sur `main.py`.

Pas de linter ni de `--dry-run` dans ce repo. Les orchestrateurs (`main.py`, `scan_boutique*.py`, `scan_precommandes.py`) effectuent de vraies requêtes HTTP et peuvent envoyer de vraies notifications Telegram/email, et modifient `data/*.json` en place — préférer les tests unitaires ou un script ad hoc pour itérer sur un détail plutôt que de relancer un orchestrateur complet. Les écritures dans `data/*.json` sont **atomiques** (fichier `.tmp` puis remplacement, via `_ecrire_json_atomique` dans `main.py` et `memoire_json.sauvegarder_memoire`) — un process tué en plein milieu (timeout GitHub Actions) ne peut plus laisser de fichier tronqué.

Secrets requis en variables d'env (secrets GitHub Actions en prod) : `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `TELEGRAM_BOT_TOKEN`, `CARDTRADER_TOKEN`, et optionnellement `GMAIL_APP_PASSWORD`.

## Conventions de travail

- Explications en français, sans jargon non expliqué — l'utilisateur apprend en même temps qu'il utilise le bot.
- Préférer montrer un fichier complet plutôt qu'un diff quand c'est pertinent pour la lecture.
- Autonomie sur `git commit` **et** `git push` sans demander confirmation à chaque fois (autorisation permanente donnée par l'utilisateur) — sauf action réellement risquée/irréversible (force-push, `git reset --hard`, suppression de données), qui reste à signaler avant d'agir.
- **Toujours tester avant de committer.** Pour tout changement touchant du code partagé entre connecteurs (`connecteur_shopify.py`, `watchlist_shopify.py`, `telegram_utils.py`, `memoire_json.py`), faire une non-régression sur l'ensemble des boutiques actives (pas juste un échantillon) avant de committer — c'est la pratique systématiquement suivie dans ce projet et elle a déjà attrapé plusieurs régressions réelles.
- Chaque changement de règle non-trivial dans `main.py` porte un commentaire `VNN:` ; pas de convention équivalente formalisée côté boutiques TCG, mais documenter la cause racine d'un bug corrigé (en commentaire ou dans `SESSION_NOTES.md`) plutôt que de patcher à l'aveugle.

## Pièges connus à ne pas réintroduire

- **Noms de coffret/set contenant eux-mêmes un mot de qualificatif** ("MEGA Dream ex", "VMAX Climax") : un filtre purement positionnel (distance au numéro) ne suffit pas à les distinguer d'un vrai qualificatif de carte — un faux positif et un vrai rejet légitime peuvent se trouver à la même distance. La seule parade fiable trouvée est `NOMS_SET_QUALIFICATIF_AMBIGU` dans `watchlist_shopify.py`, une liste **curée à la main et volontairement incomplète** — à enrichir au fil des faux positifs constatés, pas de détection automatique possible.
- **Garde-fou de cohérence de langue** : `bonne_affaire_shopify.py` l'avait dès le départ, `alerte_stock.py` ne l'a eu qu'après coup (gap trouvé en relisant le code, pas signalé par un bug). Tout nouveau point d'alerte sur les résultats des connecteurs boutiques TCG doit appliquer les mêmes garde-fous, dans le même ordre : stock → langue → qualificatif.
- **Headers HTTP partagés entre connecteurs de plateformes différentes** : `HEADERS` (`Accept: application/json`) n'est pertinent QUE pour l'API JSON Shopify — réutilisé par erreur sur des requêtes HTML PrestaShop/WooCommerce, il a fait renvoyer un corps de réponse vide (200 OK, 0 octet) sans aucune erreur levée, facilement confondu avec un vrai blocage anti-bot. Toute requête HTML doit utiliser `HEADERS_HTML`.
- **Fractions numéro/dénominateur** (`NNN/MMM`) dans un slug ou un titre : ne jamais chercher un numéro nu sans d'abord neutraliser le **dénominateur** d'une fraction sans rapport (`_retirer_fractions` retire uniquement le dénominateur, pas la fraction entière — retirer la fraction entière casse les vrais numéros qui n'ont jamais de dénominateur affiché ailleurs).
- **Microdata/JSON-LD de disponibilité en cache, désynchronisé du DOM réel** : rencontré deux fois indépendamment (WooCommerce sur une variation produit, PrestaShop sur `investcollect.com`) — le microdata/JSON-LD peut annoncer `InStock` alors que la page affiche littéralement une mention de rupture. Un nouveau connecteur de plateforme doit prévoir une vérification DOM en override qui ne peut que dégrader `en_stock` de `True` vers `False`, jamais l'inverse.
- **Préfiltre de découverte de candidats trop laxiste** : le radar de précommandes a explosé en timeout parce que son préfiltre de slug ne vérifiait qu'un seul groupe de mots-clés (type) au lieu des deux (édition + type) — tout connecteur qui parcourt un sitemap complet doit filtrer sur les DEUX groupes avant de charger une page, et exclure les extensions média (le sitemap combine souvent sitemap produits + sitemap images).

## Journal détaillé

`SESSION_NOTES.md` est le journal chronologique complet du projet (bugs trouvés, diagnostics, tests de non-régression, décisions prises) — la source à consulter pour le détail d'un bug précis ou l'historique d'une décision. Ce fichier (`CLAUDE.md`) reste volontairement une référence de contexte stable et concise ; ne pas y dupliquer l'historique, seulement les faits et pièges qui restent vrais dans la durée.
