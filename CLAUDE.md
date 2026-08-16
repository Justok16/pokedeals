# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Comments, log messages, config, and the README are in French (the user's language); code identifiers mix French and English. Keep new code/comments in French to match the existing style. **L'utilisateur est débutant en programmation** : explique en français, sans jargon technique non expliqué.

## Vue d'ensemble

PokéDeals est un bot d'alerte Pokémon TCG entièrement automatisé, sans serveur ni base de données : il tourne uniquement via des cron GitHub Actions, et persiste son état dans `data/*.json`/`.csv` que le bot commit lui-même dans le repo. Trois fonctions actives aujourd'hui, indépendantes les unes des autres :

1. **Radar de bonnes affaires historique** (`main.py`) — scanne eBay France, Vinted et Leboncoin (via alertes email) pour des cartes sous-évaluées par rapport à une cote calculée automatiquement, plus une intégration Cardtrader/Cardmarket pour affiner cette cote.
2. **Radar de stock/bonnes affaires boutiques TCG** — surveille **83 boutiques françaises et japonaises spécialisées** (Shopify, PrestaShop, WooCommerce) pour deux choses : une carte de la watchlist en-dessous du seuil de prix (🔥), ou un retour en stock d'une carte suivie (📦).
3. **Radar de précommandes anniversaire** — détecte l'apparition de produits scellés précis pas encore catalogués (🎉), actuellement le Coffret ETB 30e Anniversaire et le Coffret ETB ME06 Règne Delta (cf. `PRODUITS_SURVEILLES` dans `precommandes_watchlist.py` pour la liste à jour).

Les fonctions 2 et 3 partagent les mêmes connecteurs de scraping mais des logiques d'alerte et des fichiers mémoire séparés. Elles ne modifient jamais `main.py` ni ses fichiers de mémoire (`data/seen.json`, `data/cotes.json`, etc.).

En plus de ces 3 fonctions du bot, le dépôt héberge aussi `mcp_pokedeals/`, un outil **développeur** (serveur MCP pour Claude Code, cf. section dédiée plus bas) — jamais exécuté en cron, sans lien avec les alertes Telegram.

## Architecture réelle

### Système historique (`main.py`)

Fichier unique (~3500 lignes), pas de module. Reste organisé en sections délimitées par des banners `# ====` : utilitaires HTTP/texte, filtres de pertinence d'annonce (`annonce_pertinente`), chargement config, état "vues" (dédup), connecteurs eBay/Cardtrader/Cardmarket/Vinted/Leboncoin, moteur de cote (`obtenir_cote`), évaluation de deal (`evaluate`), notifications Telegram/email, stats/CSV, orchestration (`collecter`/`main`). Chaque changement de règle non-trivial porte un commentaire `VNN:` expliquant le cas concret qui l'a motivé — c'est le changelog du fichier, à respecter pour tout nouveau changement.

`config.yaml` reste l'interface principale : `watchlist`, `regles`, `api_cotes`, `mes_achats`, `notifications`, `plateformes`. Il est partagé avec le système boutiques TCG (même `watchlist` de cartes, réutilisée par `watchlist_shopify.py`).

### Système boutiques TCG (connecteurs Shopify/PrestaShop/WooCommerce)

Architecture commune aux 3 plateformes : un connecteur découvre les URLs produit (sitemap XML en priorité), les résultats sont normalisés dans une structure `ResultatRecherche` partagée, puis passés à deux logiques d'alerte génériques qui ne dépendent d'aucun connecteur spécifique.

**Connecteurs :**
- `connecteur_shopify.py` — API publique `/products.json`. Héberge aussi les fonctions **partagées par les 3 connecteurs** : `_titre_correspond`, `_slug_correspond`, `_normaliser_texte`, `_regex_numero_sans_denominateur`, `_retirer_fractions`, `_est_xml_valide`, `detecter_langue`, `detecter_etat` (extraction brute d'un champ "Etat :"/"Condition :" dans une fiche produit, cf. `ResultatRecherche.etat_detecte` et pièges ci-dessous), ainsi que `HEADERS` (API JSON Shopify) et `HEADERS_HTML` (toutes les requêtes HTML des deux autres connecteurs — **ne jamais réutiliser `HEADERS` pour du HTML**, cf. section pièges ci-dessous).
- `connecteur_prestashop_sitemap.py` — sitemap XML + JSON-LD + repli microdata + repli recherche HTML (`?controller=search&s=`) pour les boutiques sans sitemap, + fix de désync stock DOM (`_stock_indisponible_selon_dom`).
- `connecteur_woocommerce.py` — sitemap XML (Yoast/AIOSEO/natif) + JSON-LD + repli recherche HTML (`?s=`) + repli API REST WooCommerce Store API (`rechercher_via_api_rest`, utilisé par `mymesis.fr`) + détection de produit variable (attribut "état").

**Watchlist et structures partagées :**
- `watchlist_shopify.py` — `CarteWatchlist`, parsing de `config.yaml` (`charger_watchlist_config`), extraction/détection du qualificatif ("ex"/"gx"/"v"/"vmax"/"vstar"), `NOMS_SET_QUALIFICATIF_AMBIGU` (liste curée à la main, voir pièges ci-dessous).

**Logiques d'alerte (génériques, agnostiques du connecteur) :**
- `bonne_affaire_shopify.py` — alerte 🔥, garde-fous gradée → état (Neuf/NM uniquement) → stock → langue → qualificatif symétrique → décote ≥30%.
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

### Radar de découverte automatique de boutiques

Système **indépendant** ajouté le 12/08/2026, ne modifie jamais les listes annotées à la main :
- `decouverte_boutiques.py` — télécharge les 7 derniers jours de listes AFNIC (nouveaux domaines `.fr` créés, gratuit, sans clé, cf. `https://www.afnic.fr/wp-media/ftp/domaineTLD_Afnic/YYYYMMDD_CREA_fr.txt`), filtre par mots-clés sur le nom de domaine, puis vérifie techniquement chaque candidat (Shopify `/products.json` ou WooCommerce `product-sitemap.xml`) avec les mêmes critères objectifs que la vérification manuelle (motif de numéro de collection NNN/MMM + mention Pokémon explicite). N'ajoute automatiquement que si le signal est net (`SEUIL_*`) ; sinon rapporte sans ajouter. Une boutique au catalogue encore vide n'est **pas** mémorisée définitivement (reste re-vérifiée chaque semaine), seule une absence totale de boutique l'est.
- `boutiques_decouvertes.py` — fichier **auto-généré**, réécrit en entier à chaque cycle (`BOUTIQUES_SHOPIFY_AUTO`, `BOUTIQUES_SHOPIFY_AUTO_PRECOMMANDE_SEULEMENT`, `BOUTIQUES_WOOCOMMERCE_AUTO`, `BOUTIQUES_WOOCOMMERCE_AUTO_PRECOMMANDE_SEULEMENT`) — ne jamais éditer à la main, une boutique trouvée manuellement va dans `boutiques_shopify.py`/`boutiques_woocommerce.py` à la place.
- Câblé dans `scan_boutique.py`, `scan_boutique_woocommerce.py` et `scan_precommandes.py` (les listes `*_AUTO*` s'ajoutent aux listes curées à la main) — voir pièges ci-dessous pour la limite connue de cette approche.

**Fichiers `*_PRECOMMANDE_SEULEMENT`** (dans `boutiques_shopify.py`/`boutiques_woocommerce.py`, et leurs équivalents `*_AUTO_*`) : boutiques actives mais 100% scellé (0 carte à l'unité) — volontairement exclues des listes actives de scan cartes pour ne pas les polluer de candidats voués à 0 résultat, mais incluses dans le radar précommandes. Toute boutique qui vend À LA FOIS des cartes à l'unité ET du scellé n'a besoin que d'être dans la liste principale : `scan_precommandes.py` inclut déjà l'intégralité des listes de cartes dans son propre périmètre (cf. `_boutiques_et_replis`).

### Tendance de prix long terme (aide à la décision d'achat)

Système **indépendant** ajouté le 12/08/2026, pour répondre à "est-ce le bon moment pour acheter CETTE carte précise ?" sur un petit nombre de cartes JP/KR/CN explicitement choisies (pas la watchlist complète) :
- `watchlist_tendance.py` — `CARTES_TENDANCE`, liste explicite et réduite (ajout manuel délibéré, pas automatique).
- `historique_prix.py` — accumulateur quotidien **indépendant** de `data/cotes.json` (qui est plafonné à 5 points/carte et purgé à chaque `PURGE_VERSION`, donc inutilisable pour du long terme). Combine deux sources : l'API tierce gratuite [PokemonPriceTracker](https://www.pokemonpricetracker.com) (couvre les cartes JP/KR, secret `POKEMONPRICETRACKER_API_KEY`, prix en **USD** confirmé en conditions réelles le 12/08/2026 — rechercher via `search` texte libre + `set`, avec repli sans `set` si le premier essai échoue, cf. `_requete_pokemonpricetracker`) et, en repli, la dernière cote locale de `data/cotes.json` si elle existe. Signal de tendance (`analyser_tendance`) calculé seulement au-delà de `MIN_POINTS_POUR_SIGNAL` (14) points accumulés — jamais de conclusion prématurée sur un historique trop court, même logique que `alerte_stock.py`.
- **Conversion de devise** (`taux_change_vers_eur`) : sources gratuites sans clé (frankfurter.dev, repli open.er-api.com), appliquée **uniquement à l'affichage Telegram**, jamais aux données stockées ni au calcul de tendance (un écart en % entre 2 valeurs USD est déjà correct sans conversion). Montant converti affiché en gras, montant d'origine toujours montré entre parenthèses — jamais un chiffre EUR sans indiquer sa source.
- **Limite assumée et documentée** : aucun "nombre d'achats" (volume de ventes réelles) n'existe gratuitement pour la plupart des cartes — l'API eBay correspondante (Marketplace Insights) est fermée aux nouveaux comptes (déjà vérifié). PokemonPriceTracker ne fournit un historique de ventes eBay réelles que pour les copies **gradées** (PSA/CGC), jamais pour les cartes brutes. Le signal de tendance repose donc sur un **prix de marché**, pas un volume — à ne jamais présenter comme plus fiable que ça.
- Workflow dédié `tendance_prix.yml`, cron quotidien (pas besoin de plus fréquent pour un signal à l'échelle de semaines/mois). Alerte Telegram uniquement au **changement** de signal (`bon_moment_achat` / `prix_eleve` / `stable`), jamais de répétition quotidienne du même signal.

### Prix bas quotidien (état des lieux, pas une alerte de deal)

Système **indépendant** ajouté le 13/08/2026, pour 4 cartes explicitement choisies par Justok (`watchlist_prix_bas.py` : Plumeline ex, Carapuce, Psykokwak, Tiplouf), suivies dans les 4 langues qui l'intéressent (FR/JP/KR/CN, chacune ajoutée à `config.yaml` — y compris le chinois **traditionnel** uniquement (Chinois-T sur Cardmarket ; le simplifié a des références différentes et n'est pas suivi), langue absente jusqu'ici, avec cote **manuelle** obligatoire faute de source automatisée pour cette langue — mais mêmes numéros de carte/série que JP/KR, cf. pièges connus ci-dessous). Répond à "quel est le prix le plus bas disponible aujourd'hui, tous sites/langues confondus ?" — envoyé sur Telegram **chaque jour à 11h (Paris)** même sans bonne affaire détectée, contrairement à `bonne_affaire_shopify.py`/`main.py` qui n'alertent QUE sous la cote.

- `watchlist_prix_bas.py` — regroupe les 4 cartes × 4 langues par "famille", en pointant vers les entrées `config.yaml` existantes (aucune duplication de nom/numéro/qualificatif).
- `radar_prix_bas.py` — orchestrateur : réutilise `ebay_rechercher`/`vinted_rechercher`/`annonce_pertinente` de `main.py`, et les connecteurs Shopify/PrestaShop/WooCommerce existants (même esprit que `radar_precommandes.py` : connecteurs réutilisés tels quels, watchlist ciblée à part) — mais retourne les résultats **bruts** (prix/stock/url), pas filtrés par cote, puisque l'objectif est le prix le plus bas du jour, pas la détection de deal. Les alertes immédiates "sous la cote" pour ces mêmes cartes restent gérées par les systèmes existants (aucune logique dupliquée).
- Volontairement **hors périmètre** : Leboncoin (bloqué par anti-bot, alertes email pré-configurées seulement, pas de recherche à la demande), Cardmarket (API fermée + scraping quotidien interdit par leurs CGU), TCGplayer (marché quasi exclusivement américain, peu pertinent pour un filtre "vendeur en France").
- Workflow dédié `prix_bas_quotidien.yml`, cron quotidien 9h UTC (= 11h Paris en été, dérive à 12h en hiver — même limite déjà acceptée pour `tendance_prix.yml`, pas d'ajustement DST).

### Modules transverses

- `telegram_utils.py` — `echapper_html`/`echapper_url_html`, partagés par les 3 modules d'alerte boutiques TCG.
- `memoire_json.py` — `charger_memoire`/`sauvegarder_memoire` génériques pour un fichier JSON, partagés par `alerte_stock.py`, `alerte_precommande.py`, `decouverte_boutiques.py` **et** `mcp_pokedeals/cache.py`.

## Serveur MCP (`mcp_pokedeals/`) — outil développeur, PAS une fonction du bot

Ajouté le 14/08/2026, système **totalement indépendant** des 3 fonctions ci-dessus : ne tourne jamais en CI/cron, ne modifie et ne lit aucun fichier `data/*.json` de PokéDeals (son propre cache vit dans `mcp_pokedeals/.cache/`, exclu de git). Expose des données Pokémon TCG (cartes, sets, prix) à une IA comme Claude Code via le protocole MCP (transport stdio, lancé en local par l'utilisateur — `python -m mcp_pokedeals.server`).

- **Fournisseurs** : TCGdex (`providers/tcgdex.py`, API publique gratuite, appels REST directs — champs JSON vérifiés via le code déjà en prod dans `main.py`, pas via le SDK officiel `tcgdex-sdk` non vérifié à l'écriture) ; CardDex (`providers/carddex.py`, gratuit avec clé optionnelle, URL de base **à vérifier par l'utilisateur** avant premier usage, cf. son README) ; Cardmarket (`providers/cardmarket.py`, guide de prix officiel gratuit actif par défaut — même technique que `cardmarket_prix()` dans `main.py` — API Marketplace OAuth volontairement **non implémentée**, nécessite un compte vendeur).
- **Outils exposés** : `search_cards`, `get_card`, `search_set`, `get_set_cards`, `get_card_prices`, `analyze_card` (synthèse informative, jamais une prédiction de valeur).
- **Dépendances séparées** (`mcp_pokedeals/requirements.txt` : `mcp`, `requests`, `python-dotenv`) — jamais dans `requirements.txt` racine, jamais installées par les workflows CI.
- Voir `mcp_pokedeals/README.md` pour l'installation, la config Claude Code (`.mcp.json` à la racine) et le statut détaillé de chaque source.
- Piège déjà rencontré : le SDK officiel `mcp` (PyPI) a renommé `mcp.server.fastmcp.FastMCP` en `mcp.server.mcpserver.MCPServer` dans sa v2 — un `pip install mcp` sans version fixée casse tout code écrit pour l'ancienne API (`ModuleNotFoundError`).

## CI/déploiement — 8 workflows GitHub Actions

Tournent en parallèle sur le même repo, chacun avec son propre groupe de concurrence (`concurrency.group`) pour ne jamais se bloquer mutuellement, et une étape de sauvegarde mémoire avec dance stash/pull-rebase/push pour éviter les collisions Git entre crons qui se chevauchent (sauf les workflows sans fichier mémoire, ex. `prix_bas_quotidien.yml`, `permissions: contents: read` seulement).

| Workflow | Cadence | Timeout | Contenu |
|---|---|---|---|
| `pokedeals.yml` | 15 min | 15 min | `main.py` (système historique) |
| `scan_shopify.yml` | 30 min | 25 min | scan cartes Shopify + radar précommandes Shopify |
| `scan_prestashop.yml` | 30 min | 30 min | scan cartes PrestaShop + radar précommandes PrestaShop |
| `scan_woocommerce.yml` | 30 min | 22 min (lot A) + 18 min (lot B) + 25 min (précommandes) | 3 jobs séquentiels (`needs:`) : scan cartes lot A, lot B, puis radar précommandes (lot A + lot B) |
| `decouverte_boutiques.yml` | hebdomadaire (lundi 06h UTC) | 20 min | radar de découverte automatique de nouvelles boutiques (AFNIC) |
| `tendance_prix.yml` | quotidien 8h30 UTC | 10 min | suivi de tendance de prix long terme (3 cartes JP) |
| `prix_bas_quotidien.yml` | quotidien 9h UTC (~11h Paris) | 35 min | radar de prix bas quotidien (4 cartes × 4 langues, tous sites confondus) |
| `tests.yml` | à chaque push/PR | — | suite pytest (cf. section Commandes) |

`scan_woocommerce.yml` est le seul à jobs multiples (nécessaire car son plus gros catalogue à lui seul dépasse le budget d'un run simple) ; les jobs sont **séquentiels**, jamais en parallèle entre eux au sein d'un même run, pour éviter une course d'écriture sur le même fichier mémoire.

Avant de changer un timeout ou une composition de lot, vérifier `SESSION_NOTES.md` (section diagnostic du flake `scan_lot_a`) — les marges mesurées en prod y sont documentées, ne pas ajuster à l'aveugle.

## Fichiers de mémoire (`data/*.json`)

Deux familles de schéma, une par fonctionnalité, jamais mélangées :
- **Stock/bonnes affaires** (`seen.json`, `cotes.json`, `anciennete_annonces.json` pour `main.py` ; `stock_boutiques_tcg.json`/`stock_boutiques_tcg_prestashop.json`/`stock_boutiques_tcg_woocommerce.json` — un fichier **par plateforme**, séparés justement pour éviter les collisions entre workflows parallèles).
- **Précommandes** (`precommandes_anniversaire_{shopify,prestashop,woocommerce}.json` — un fichier par plateforme, clé `{domaine}|{nom_produit}`, valeurs `{confiance, raison, titre_produit, url_produit, derniere_verification}`).
- **Découverte** (`decouverte_boutiques_memoire.json` — clé `{domaine}`, valeurs `{derniere_verification, verdict}` ; contient uniquement les domaines définitivement écartés ou déjà ajoutés, jamais les candidats "insuffisants" qui restent re-vérifiés chaque semaine).

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
- **Identification de carte donnée par Justok (numéro, langue, série/set) : faire confiance à 100%, sans la recontester.** Justok vérifie ces informations de son côté avant de les donner — ne pas chercher à les re-vérifier ou à les remettre en question. Ça n'empêche pas de vérifier la cohérence technique (format attendu par `config.yaml`, présence d'un dénominateur, etc.) ni de creuser une anomalie de comportement (ex. un mauvais matching) : ce qui ne doit plus être remis en cause, c'est l'identification elle-même de la carte (quelle carte physique elle est).

## Pièges connus à ne pas réintroduire

- **Noms de coffret/set contenant eux-mêmes un mot de qualificatif** ("MEGA Dream ex", "VMAX Climax") : un filtre purement positionnel (distance au numéro) ne suffit pas à les distinguer d'un vrai qualificatif de carte — un faux positif et un vrai rejet légitime peuvent se trouver à la même distance. La seule parade fiable trouvée est `NOMS_SET_QUALIFICATIF_AMBIGU` dans `watchlist_shopify.py`, une liste **curée à la main et volontairement incomplète** — à enrichir au fil des faux positifs constatés, pas de détection automatique possible.
- **Garde-fou de cohérence de langue** : `bonne_affaire_shopify.py` l'avait dès le départ, `alerte_stock.py` ne l'a eu qu'après coup (gap trouvé en relisant le code, pas signalé par un bug). Tout nouveau point d'alerte sur les résultats des connecteurs boutiques TCG doit appliquer les mêmes garde-fous, dans le même ordre : gradée → état → stock → langue → qualificatif.
- **État de conservation (Neuf/NM uniquement) non filtré côté boutiques TCG** : jusqu'au 14/08/2026, `bonne_affaire_shopify.py`/`alerte_stock.py` n'avaient AUCUN filtre sur l'état de la carte (contrairement à `main.py`, qui a `etats_acceptes`/`etats_refuses` depuis longtemps, mais UNIQUEMENT pour le système eBay/Vinted/Leboncoin — jamais lu par les modules boutiques TCG). Cas réel : kairyu.fr, Eevee ex 223 sv8a, fiche produit "Etat : Exc" (Excellent, pas Near Mint) alertée à tort comme bonne affaire à -32,2%. Corrigé via `detecter_etat()` (`connecteur_shopify.py`, extraction ANCRÉE sur un label "Etat :"/"Condition :"/"Qualité :" suivi d'un vrai séparateur `:`/`-` — jamais une recherche libre dans tout le texte, pour ne jamais confondre "ex" — présent dans la quasi-totalité des titres de la watchlist — avec l'abréviation anglaise d'"Excellent") + `bonne_affaire_shopify._etat_refuse()` (liste `MOTS_ETAT_REFUSE`, volontairement incomplète comme `NOMS_SET_QUALIFICATIF_AMBIGU`/`MOTS_CARTE_GRADEE`). Aucun label d'état trouvé = **accepté** (beaucoup de boutiques n'indiquent pas l'état sur toutes leurs fiches), seul un état explicitement inférieur à Near Mint/Neuf bloque l'alerte — même philosophie que `etats_acceptes`/`etats_refuses` dans `main.py`.
- **Cartes gradées (PSA/CGC/BGS/CCC...) non exclues du système boutiques TCG** : `main.py` (système eBay historique) exclut ces annonces depuis longtemps (`EXCLUSIONS`, avec négation "non gradée"), mais `bonne_affaire_shopify.py`/`alerte_stock.py` n'avaient AUCUN filtre équivalent jusqu'au 13/08/2026 — une carte gradée comparée à la cote d'une carte brute produit une "décote" biaisée, pas une vraie affaire (cas réel : Evoli ex 167/131 PSA 8/CCC 9.5 alerté à -53.9%/-32.4%). `_est_carte_gradee()` dans `bonne_affaire_shopify.py` fait référence pour les deux modules. Liste de mots-clés **volontairement incomplète** (même limite que `NOMS_SET_QUALIFICATIF_AMBIGU`) — "ccc" manquait même dans la liste d'origine de `main.py`, découvert via ce cas réel ; à enrichir au fil des nouvelles notations de gradation rencontrées.
- **Headers HTTP partagés entre connecteurs de plateformes différentes** : `HEADERS` (`Accept: application/json`) n'est pertinent QUE pour l'API JSON Shopify — réutilisé par erreur sur des requêtes HTML PrestaShop/WooCommerce, il a fait renvoyer un corps de réponse vide (200 OK, 0 octet) sans aucune erreur levée, facilement confondu avec un vrai blocage anti-bot. Toute requête HTML doit utiliser `HEADERS_HTML`.
- **Fractions numéro/dénominateur** (`NNN/MMM`) dans un slug ou un titre : ne jamais chercher un numéro nu sans d'abord neutraliser le **dénominateur** d'une fraction sans rapport (`_retirer_fractions` retire uniquement le dénominateur, pas la fraction entière — retirer la fraction entière casse les vrais numéros qui n'ont jamais de dénominateur affiché ailleurs).
- **Microdata/JSON-LD de disponibilité en cache, désynchronisé du DOM réel** : rencontré deux fois indépendamment (WooCommerce sur une variation produit, PrestaShop sur `investcollect.com`) — le microdata/JSON-LD peut annoncer `InStock` alors que la page affiche littéralement une mention de rupture. Un nouveau connecteur de plateforme doit prévoir une vérification DOM en override qui ne peut que dégrader `en_stock` de `True` vers `False`, jamais l'inverse.
- **Préfiltre de découverte de candidats trop laxiste** : le radar de précommandes a explosé en timeout parce que son préfiltre de slug ne vérifiait qu'un seul groupe de mots-clés (type) au lieu des deux (édition + type) — tout connecteur qui parcourt un sitemap complet doit filtrer sur les DEUX groupes avant de charger une page, et exclure les extensions média (le sitemap combine souvent sitemap produits + sitemap images).
- **Nom de domaine trompeur ou évocateur mais non pertinent** : un nom qui semble Pokémon (ex. un domaine contenant "poke") peut être une tout autre franchise (une boutique trouvée le 12/08/2026 vendait exclusivement du Disney Lorcana malgré un nom à consonance Pokémon). Le radar de découverte (`decouverte_boutiques.py`) ne se fie donc JAMAIS au nom de domaine pour la décision finale — uniquement pour générer des candidats à vérifier ; la décision d'ajout se fait sur le contenu réel du catalogue (mention Pokémon explicite + numéro de collection). Ne pas simplifier cette étape même si ça semble redondant.
- **Boutique fraîchement enregistrée avec un catalogue encore vide** : ne pas mémoriser un verdict "pas assez de signal" comme définitif, sous peine de ne plus jamais revérifier une boutique légitime qui n'a simplement pas encore eu le temps de s'approvisionner (cas réel : `nemee-tcg.fr`, 1 seul produit au premier passage). Seule l'absence totale de site (aucune plateforme détectée) justifie une mémorisation permanente.
- **`git stash pop` en conflit dans une étape "Sauvegarder..." de workflow** : ne supprime JAMAIS l'entrée du stash ("kept in case you need it again"), même quand le `cp`/`add`/`commit` de rattrapage qui suit répare bien le fichier visé. Si un même job enchaîne 2 étapes de sauvegarde (`scan_prestashop.yml`, `scan_shopify.yml`), le stash orphelin de la première pollue le `git stash pop` de la seconde et peut faire échouer tout le job (`Committing is not possible because you have unmerged files`, cas réel du 15/08/2026 soir). Toujours faire suivre `git stash pop || true` d'un `git stash drop || true` dans ce genre d'étape.
- **Sortie Python bufferisée dans les workflows** : un `run: python ...` sans `PYTHONUNBUFFERED: "1"` peut laisser un log GitHub Actions totalement vide si le process est tué (timeout) avant que le buffer ne se vide — même si le script affiche bien une progression ligne par ligne. Réflexe systématique sur toute nouvelle étape `run: python ...`.
- **Entrée `config.yaml` sans numéro pour une carte homonyme fréquente** : "nom seul" (sans `X/Y` ni numéro nu) fait matcher N'IMPORTE QUELLE carte de ce nom, toutes éditions confondues — pas seulement l'édition suivie. Cas réel (16/08/2026) : les 4 entrées `langue: cn` de `watchlist_prix_bas`/`config.yaml` (Squirtle/Psyduck/Piplup/Oricorio, posées sans numéro faute de référence connue au départ) ont fait remonter un Squirtle chinois quelconque sur Vinted au lieu du sv2a 170/165 suivi. Le chinois **traditionnel** (Chinois-T sur Cardmarket — le seul suivi ici, le simplifié a des références différentes) partage les mêmes numéros que JP/KR : toujours réutiliser le `nom` JP/KR tel quel plutôt que d'improviser un nom générique. Corollaire dans le code : `cartes_boutiques_par_nom_config` (radar_prix_bas.py) est indexé par `nom_config`, donc partagé entre langues qui partagent ce nom (JP/KR/CN-T) — tout code qui itère dessus doit filtrer explicitement sur `carte.langue`, sinon un résultat d'une langue peut s'étiqueter avec celle d'une autre (bug réel corrigé le 16/08/2026).

## Journal détaillé

`SESSION_NOTES.md` est le journal chronologique complet du projet (bugs trouvés, diagnostics, tests de non-régression, décisions prises) — la source à consulter pour le détail d'un bug précis ou l'historique d'une décision. Ce fichier (`CLAUDE.md`) reste volontairement une référence de contexte stable et concise ; ne pas y dupliquer l'historique, seulement les faits et pièges qui restent vrais dans la durée.
