# Notes de session — extension multi-plateforme PokéDeals

Dernière mise à jour : 2026-08-10 (fin de session — couverture des
boutiques sans sitemap terminée, 84 boutiques actives au total).

## Contexte du projet

Extension de PokéDeals pour surveiller **81+ boutiques TCG spécialisées**
(Shopify, PrestaShop, WooCommerce), en plus des sources historiques déjà en
place dans `main.py` (eBay, Vinted, Cardtrader, alertes email Leboncoin).

**4 workflows GitHub Actions tournent en parallèle** sur le même repo, chacun
avec son propre cron et son propre groupe de concurrence (pour ne jamais se
bloquer mutuellement) :

| Workflow | Cadence | Groupe de concurrence | Fichier mémoire stock |
|---|---|---|---|
| `pokedeals.yml` (main.py — eBay/Vinted/Cardtrader/Leboncoin) | 15 min | `pokedeals` | `data/seen.json`, `data/anciennete_annonces.json` |
| `scan_shopify.yml` | 30 min | `scan_shopify` | `data/stock_boutiques_tcg.json` |
| `scan_prestashop.yml` | 30 min | `scan_prestashop` | `data/stock_boutiques_tcg_prestashop.json` |
| `scan_woocommerce.yml` (2 jobs séquentiels, lot A + lot B) | 30 min | `scan_woocommerce` | `data/stock_boutiques_tcg_woocommerce.json` |

Chaque workflow de scan repose sur la même architecture : un connecteur par
plateforme découvre les URLs produits (sitemap XML en priorité), un seul
passage de matching nom+numéro par boutique, puis les résultats alimentent
DEUX logiques d'alerte indépendantes déjà génériques
(`bonne_affaire_shopify.py` pour le seuil de prix/cote, `alerte_stock.py`
pour les retours en stock) — ces deux modules ne dépendent d'aucun
connecteur spécifique, uniquement des structures `ResultatRecherche`/
`CarteWatchlist` partagées.

## Les 3 bugs de production corrigés aujourd'hui (commit `8ff3761`)

Tous les trois ont été identifiés par leur **cause racine** avant correction
(pas de patch à l'aveugle), suite à des alertes Telegram réelles envoyées en
prod.

### 1. Bulbizarre 166/165 JP (hikarudistribution.com)

- **Cause racine** : le titre réel du produit était *"Bulbizarre AR 166/165
  - SV2A"*. `detecter_langue()` (dans `connecteur_shopify.py`) ne
  reconnaissait que des mots explicites ("japonais"/"japanese"), pas les
  codes de set courts comme "SV2A" qui identifient pourtant sans ambiguïté
  une carte japonaise (SV2A = set exclusivement japonais "Pokémon Card
  151"). Résultat : `langue_detectee=None`, donc le garde-fou de cohérence
  de langue (qui existait déjà) n'avait rien à bloquer, et le prix d'une
  carte japonaise se comparait à tort à la cote FRANÇAISE de
  `config.yaml`.
- **Fichier corrigé** : `connecteur_shopify.py` (ajout de
  `CODES_SET_ASIATIQUES` et de la valeur de retour `"jp_ou_kr"` dans
  `detecter_langue()`) + `bonne_affaire_shopify.py` (`evaluer_deal` traite
  `"jp_ou_kr"` comme compatible avec une carte configurée `jp` OU `kr`,
  incompatible avec `fr`).

### 2. Evoli 188/167 (fuji-store.fr)

- **Cause racine** : produit WooCommerce **variable** (attribut "état" —
  quasi tous les listings de cartes à l'unité sur WooCommerce en ont un,
  même avec une seule condition proposée). Le JSON-LD annonçait
  `"availability":"InStock"`, mais l'UNIQUE variation du produit portait
  elle-même `"En rupture de stock"` dans son propre `availability_html`
  (rendu côté serveur au chargement — donc plus fiable qu'un JSON-LD
  potentiellement en cache/périmé, généré par un plugin SEO).
- **Fichier corrigé** : `connecteur_woocommerce.py` (`_extraire_variations`
  + `_offre_depuis_variation` : avec une seule variation, on lui fait
  confiance et on écrase le stock JSON-LD si contradiction ; avec
  plusieurs variations, ambiguïté réelle → `confiance="faible"` +
  `necessite_verification_manuelle=True` plutôt que de deviner).

### 3. Plumeline ex 024 (kyoriyu.fr)

- **Cause racine** : collision entre deux cartes DISTINCTES partageant le
  même nom+numéro. `config.yaml` vise *"Plumeline ex 024"* (MEP Black Star
  Promos, ~28€), mais *"Plumeline 24 Sun & Moon REVERSE"* (carte plus
  ancienne, non-ex, 1,50€) existe aussi sur kyoriyu.fr avec le même
  numéro "024"/"24". Le parseur `watchlist_shopify._extraire_nom_et_numero`
  jetait silencieusement le qualificatif "ex" (mot considéré comme un
  simple terminateur de nom, jamais réutilisé). Le mauvais Plumeline
  (1,50€ ≤ seuil fixe 15€) matchait à la place du bon.
- **Fichier corrigé** : `watchlist_shopify.py` (nouveau champ
  `CarteWatchlist.qualificatif`, extraction de "ex"/"gx"/"v"/"vmax"/"vstar"
  depuis `config.yaml`) + `bonne_affaire_shopify.py` ET `alerte_stock.py`
  (rejet d'un match dont le titre ne contient pas ce qualificatif, via
  `\b...\b` — pas un simple `in`, sinon "v" matcherait "Evoli").
- **Bonus** : ce filtre a aussi attrapé une **2e collision réelle** trouvée
  pendant le test de régression (`Pikachu ex 234 m2a` vs un produit
  *"Pikachu – Promo SWSH – SWSH234"* sans "ex", sur fuji-store.fr).

## Asymétrie du filtre qualificatif — CONFIRMÉE ET CORRIGÉE (2026-08-10)

Le fix initial (`bonne_affaire_shopify.py` / `alerte_stock.py`) ne
vérifiait qu'un seul sens : *si `carte.qualificatif` est défini (ex: "ex")
ET absent du titre produit → rejeter.* Le `if carte.qualificatif` initial
sautait tout le bloc quand `carte.qualificatif` est `None`, donc le sens
inverse n'était pas couvert.

**Reproduit par un test synthétique** (carte config `"Bulbizarre 166/165"`
sans qualificatif vs titre produit `"Bulbizarre ex 166/165 - Edition
Speciale"`) : le mauvais match passait bien à travers (`DEAL (seuil
fixe)` déclenché à tort) avant correctif.

**Correctif appliqué :**
- `watchlist_shopify.py` : nouvelle fonction `detecter_qualificatif_titre(titre)`
  qui cherche "ex"/"gx"/"v"/"vmax"/"vstar" (mêmes `\b...\b`, pas de faux
  positif type "Evoli" contient "v") directement dans un titre de produit.
- `bonne_affaire_shopify.py` (`evaluer_deal`) et `alerte_stock.py` : quand
  `carte.qualificatif is None`, on rejette désormais tout résultat dont le
  titre contient un qualificatif détecté par `detecter_qualificatif_titre`.

**Test de non-régression** (script ad hoc, 7 cas, tous OK) :
1. Carte base vs titre "ex" homonyme → rejeté (nouveau comportement, avant : bug).
2. Carte base vs titre sans qualificatif → matche normalement (pas de régression).
3. Plumeline ex vs titre avec "ex" → matche (pas de régression sur le fix original).
4. Plumeline ex vs titre sans "ex" → rejeté (bug original toujours corrigé).
5. Evoli ex 174 promo → matche (deal déjà validé en prod, confirmé).
6. Mega Dracaufeu X ex 023 → matche (deal déjà validé en prod, confirmé).
7. Evoli base (nom contient "v") vs titre sans vrai qualificatif → matche
   (vérifie l'absence de faux positif du `\bv\b` sur "Evoli").

Script de test : non sauvegardé dans le repo (scratchpad temporaire), à
refaire si besoin de re-vérifier.

## Test de non-régression COMPLET sur 81 boutiques — FAIT, deal count inchangé (2026-08-10)

Script ad hoc (lecture seule, aucune écriture mémoire prod, aucun envoi
Telegram) scannant les listes actives réelles des 3 plateformes
(`BOUTIQUES_SHOPIFY` 40, `BOUTIQUES_PRESTASHOP_SITEMAP` 15,
`BOUTIQUES_WOOCOMMERCE_SITEMAP` 26 — 81 boutiques, 0 échec) avec la
watchlist complète (194 critères de recherche chargés, alias inclus).

Pour chaque résultat à confiance forte (758-759 selon le run, léger bruit
de stock/catalogue entre deux scans à 30 min d'écart), comparaison de
l'ANCIEN comportement (asymétrique, ré-implémenté localement dans le
script pour diff) contre le NOUVEAU (code actuel) :

- **Deals détectés AVANT le fix (simulé) : 6 = Deals détectés APRÈS le fix : 6**
  → aucune bonne affaire perdue, sur les deux runs (avant et après le fix
  du faux positif décrit ci-dessous).
- **1er run** (avant le fix du faux positif) : 11 rejets introduits par le
  filtre symétrique — analysés un par un, **8 étaient des faux positifs**
  (voir section suivante) et 3 des vrais rejets légitimes.
- **2e run** (après le fix du faux positif) : **3 rejets introduits**,
  exactement les 3 vrais rejets légitimes attendus (aucun faux positif
  restant).

## Faux positif dans `detecter_qualificatif_titre()` — CONFIRMÉ ET CORRIGÉ (2026-08-10)

**Cause racine** : la fonction cherchait un qualificatif ("ex"/"gx"/"v"/
"vmax"/"vstar") n'importe où dans le titre du produit. Or certains
coffrets/sets portent EUX-MÊMES ce mot dans leur propre nom (branding
marketing du coffret, pas rareté de la carte) : "MEGA Dream ex" (coffret
JP) et "VMAX Climax" (set S8b FR/JP). Résultat : des cartes de BASE
(non-ex) matchant un produit de ces coffrets étaient rejetées à tort —
8 cas réels trouvés lors du 1er scan complet (`Psyduck/Psykokwak 199`
chez `lemantcg.fr`, `japantradingcardstore.com`, `cartespokemon.com`,
`japan2uk.com` ; `Evoli/Eevee 210` chez `cardshunter.fr` et
`japantradingcardstore.com`).

**Approche testée et rejetée** : une simple fenêtre de caractères autour
du numéro matché (comme suggéré initialement) ne suffit PAS — mesure
précise des distances réelles : le faux positif le plus proche ("ex" dans
"MEGA Dream ex" collé au nom de carte "Psykokwak ex") est à seulement 5
caractères du numéro, alors qu'un vrai rejet légitime ("Voltali V" pour
une carte `Eevee`) est aussi à 1 caractère du numéro — aucune taille de
fenêtre ne sépare proprement les deux catégories, la distance seule ne
suffit pas à distinguer "la carte est une ex" de "le nom du coffret
contient ex".

**Fix appliqué** (`watchlist_shopify.py`) :
1. Nouvelle constante `NOMS_SET_QUALIFICATIF_AMBIGU = {"mega dream",
   "vmax climax"}` (même esprit que `CODES_SET_CONNUS` déjà existant) :
   si le titre contient un de ces noms de coffret connus, on renonce à y
   détecter un qualificatif (première ligne de défense — résout
   effectivement les 8 cas).
2. `FENETRE_QUALIFICATIF_TITRE = 40` caractères autour du numéro matché
   (défense en profondeur complémentaire, pas suffisante seule) — les 3
   vrais rejets légitimes se trouvent tous à ≤17 caractères du numéro.
3. `detecter_qualificatif_titre()` prend maintenant un 2e paramètre
   `numero: str | None` (réutilise `_regex_numero_sans_denominateur` de
   `connecteur_shopify.py`, déjà partagée par les 3 connecteurs) ; les
   deux points d'appel (`bonne_affaire_shopify.py`, `alerte_stock.py`)
   passent désormais `carte.numero`.

**Test ciblé** (script ad hoc, 15 cas, tous OK, cartes/cotes chargées
depuis les vrais `config.yaml`/`data/cotes.json`) :
- 6 titres distincts couvrant les 8 faux positifs → ne rejettent plus.
- 3 vrais rejets légitimes (Voltali V, Iron Crown ex, Iron Hands ex) →
  toujours rejetés.
- Non-régression : Plumeline ex (avec/sans "ex" dans le titre), Evoli ex
  174 promo, Mega Dracaufeu X ex 023 → comportement qualificatif inchangé.
- Cas symétrique original (Bulbizarre 166/165 sans qualificatif vs titre
  "Bulbizarre ex 166/165") → toujours rejeté correctement.

**Test complet 81 boutiques re-lancé après ce fix** : confirmé ci-dessus
(2e run, 3 rejets restants = exactement les 3 cas légitimes attendus).

**Risque résiduel documenté** : `NOMS_SET_QUALIFICATIF_AMBIGU` est une
liste curée, à compléter au fil des faux positifs constatés (comme
`CODES_SET_CONNUS`) — un futur coffret au nom ambigu non répertorié
pourrait reproduire le même faux positif jusqu'à être découvert et ajouté
à la liste.

## Fichiers concernés dans cette phase (pour s'orienter vite)

**Connecteurs (un par plateforme, structure `ResultatRecherche` commune) :**
- `connecteur_shopify.py` — Shopify, `/products.json`, détection de langue partagée par les 3 connecteurs
- `connecteur_prestashop_sitemap.py` — PrestaShop, sitemap XML + JSON-LD + repli microdata (`itemprop=`) + repli recherche HTML (`?controller=search&s=`) pour les boutiques sans sitemap
- `connecteur_woocommerce.py` — WooCommerce, sitemap XML (Yoast/AIOSEO/natif WP) + JSON-LD + repli classes CSS natives + repli recherche HTML (`?s=`) + détection produit variable

**Watchlist et structures partagées :**
- `watchlist_shopify.py` — `CarteWatchlist`, parsing de `config.yaml` (`charger_watchlist_config`), `ECHANTILLON_CONFIG` (10 cartes de test, jamais utilisé en prod)

**Logiques d'alerte (génériques, agnostiques du connecteur) :**
- `bonne_affaire_shopify.py` — seuil de prix/cote, garde-fous devise + langue + qualificatif + décote ≥30%
- `alerte_stock.py` — retours en stock (mémoire JSON par plateforme), même garde-fou qualificatif

**Orchestrateurs (un par plateforme, appelés par les workflows) :**
- `scan_boutique.py` (Shopify, 40 boutiques actives dans `boutiques_shopify.py`)
- `scan_boutique_prestashop.py` (PrestaShop, 17 boutiques actives dans `boutiques_prestashop.py` — 15 couvertes par sitemap + 2 via repli recherche HTML : `investcollect.com`, `lepantheon-tcg.com`, cf. section dédiée ci-dessous)
- `scan_boutique_woocommerce.py` (WooCommerce, 26 boutiques actives dans `boutiques_woocommerce.py`, scindées en 2 lots équilibrés par volume d'URLs pour le workflow)

**Workflows GitHub Actions :** `.github/workflows/{pokedeals,scan_shopify,scan_prestashop,scan_woocommerce}.yml`

## Couverture des boutiques sans sitemap — TERMINÉE (2026-08-10)

Reprise du travail interrompu ("compléter avec les cas restants les plus
rentables"). Diagnostic poussé au maximum sur chaque boutique bloquée,
dans les limites raisonnables (pas de navigateur headless, pas de
contournement anti-bot lourd, respect des rate-limits).

### 2 bugs réels trouvés et corrigés (impact potentiellement large)

En creusant pourquoi `investcollect.com` semblait "bloqué en 403" (a priori
faux, l'audit initial l'avait mal diagnostiqué) :

1. **Header partagé `Accept: application/json`** (`connecteur_shopify.py`,
   `HEADERS`) — pensé générique, en réalité pertinent SEULEMENT pour l'API
   JSON Shopify (`/products.json`), mais réutilisé par erreur pour TOUTES
   les requêtes HTML des connecteurs PrestaShop/WooCommerce (robots.txt,
   sitemap, pages produit, pages de recherche). Sur `investcollect.com`,
   ce header fait renvoyer un corps de réponse **VIDE** (200 OK, 0 octet)
   sur les pages produit — aucune erreur levée, juste un `ResultatRecherche`
   silencieusement absent, facilement confondu avec un vrai blocage
   anti-bot. **Fix** : nouvelle constante `HEADERS_HTML` (Accept
   navigateur classique) dans `connecteur_shopify.py`, utilisée par les
   deux connecteurs sans sitemap pour TOUS leurs appels HTTP (pas
   seulement le point bloqué).
2. **Extraction du titre en microdata** (`_extraire_microdata_produit`,
   `connecteur_prestashop_sitemap.py`) — prenait la PREMIÈRE occurrence
   `itemprop="name"` du document, qui est souvent celle de la MARQUE
   ("The Pokémon Company", dans un `<meta>` auto-fermé sans texte interne)
   plutôt que celle du produit (dans le `<h1>`, plus bas). **Fix** : prend
   désormais la première occurrence NON VIDE.

**Test de non-régression complet sur les 81 boutiques actives** (requis
avant de toucher du code partagé) : 81/81 OK, 0 échec, 6 deals
avant/après inchangés, mêmes 3 rejets légitimes qu'avant (aucun nouveau) —
**aucune régression** du changement de header.

### Boutiques intégrées (3)

- **`investcollect.com`** (repli recherche HTML) — 55 résultats à
  confiance forte sur la watchlist complète (194 critères), **3 vraies
  bonnes affaires détectées** avec garde-fous (prix/décote/devise)
  vérifiés dans `evaluer_deal` : Méga-Dracaufeu Y ex 294/217 à 320€ (cote
  356€, -10.2%), Méga-Dracolosse ex 290/217 à 400€ (cote 583€,
  **-31.4%**), Méga-Dracaufeu X ex à 50€ (cote 65€, -23%). Vrai vendeur de
  cartes à l'unité (catégorie dédiée "cartes-a-l-unites", numéros de set
  dans les slugs produit).
- **`lepantheon-tcg.com`** (repli recherche HTML) — 2 résultats à
  confiance forte (1 produit unique, matché via nom + alias), 0 deal ce
  cycle précis — intégrée quand même (même principe que les boutiques
  déjà actives qui ont 0 match certains cycles ; recherche native
  confirmée fonctionnelle et pertinente).
- **`mymesis.fr`** (repli API REST — **demande explicite de l'utilisateur
  de pousser le diagnostic**, boutique qu'il affectionne) — le repli
  recherche HTML reste non viable (son moteur de recherche visible est un
  widget Elementor "Jet Search" piloté par AJAX côté client, une requête
  GET statique sur `?s=` renvoie une page quasi identique quelle que soit
  la requête). MAIS son
  **API REST WooCommerce "Store API" publique**
  (`wp-json/wc/store/v1/products?search=...`) répond parfaitement : ce
  n'est PAS un contournement, c'est le point d'entrée officiel documenté
  pour les vitrines headless, actif par défaut sur la plupart des
  installations WooCommerce, indépendant du widget de recherche du thème.
  Nouvelle methode `ConnecteurWooCommerce.rechercher_via_api_rest()` (JSON
  structuré : nom, prix en CENTIMES, devise, stock — pas besoin de
  récupérer chaque page produit individuellement). Testée sur la watchlist
  complète : **57 résultats à confiance forte**, vrai vendeur de cartes à
  l'unité (catégorie "cartes-pokemon-a-lunite"), 0 deal ce cycle précis
  mais garde-fous vérifiés sans faux positif. Intégrée dans
  `BOUTIQUES_WOOCOMMERCE_REPLI_API_REST` (LOT_A).

### Boutiques diagnostiquées, NON intégrées (raison précise pour chacune)

- **`gamespirit.fr`** — technique OK une fois le bon sous-domaine trouvé
  (son formulaire de recherche pointe vers `www2.gamespirit.fr`, pas
  `gamespirit.fr` — pas exploité en code, boutique jugée non prioritaire
  malgré la découverte). Catalogue vérifié : boutique généraliste
  rétro-gaming/figurines/goodies, AUCUNE carte à l'unité (recherche
  "pokemon carte" ne remonte que des accessoires — boîtes de protection,
  portfolios — et un jeu Game Boy), pas de catégorie "cartes à l'unité"
  (404). Pas un problème technique : désalignement de catalogue.
- **`pokemoncarte.com`** — bug de paramètre corrigé (son thème utilise
  `search_query`, pas le `s` standard PrestaShop ; `_decouvrir_candidats_recherche`
  envoie désormais les deux). Recherche fonctionnelle, mais 22 résultats
  sur la watchlist complète, TOUS à confiance FAIBLE (matching nom seul,
  jamais nom+numéro) — 0 alerte automatique possible en l'état. À
  réévaluer si son catalogue s'étoffe.
- **`kiokutcg.fr`** — repli recherche HTML fonctionnel (WooCommerce, pas
  de sitemap), mais 0 résultat sur la watchlist complète : boutique de
  PRODUITS SCELLÉS (coffrets, displays, tripacks, mini-tins), aucune carte
  à l'unité trouvée sur plusieurs recherches (Pikachu, Dracaufeu ex,
  Evoli).
- **`nexthobby.fr`** — identifié WooCommerce, sans sitemap, repli
  recherche HTML fonctionnel QUAND accessible (confirmé : 27 candidats
  réels pour "Dracaufeu", mais essentiellement des accessoires/sleeves,
  pas de carte à l'unité vue). **Rate-limit très agressif** : persiste
  même après 5 minutes sans requête (pas de header `Retry-After` fourni,
  au-delà d'un simple throttle par minute) — incompatible avec un cycle de
  scan automatique (~60-90 requêtes nécessaires sur la watchlist complète).
  Abandonné après plusieurs tentatives espacées (45s, 180s, 300s), suivant
  la consigne de ne pas insister indéfiniment sur un site qui répond 429
  en boucle.
- **`bcd-jeux.fr`** — sitemap toujours cassé côté site (re-testé,
  confirmé identique à l'audit initial : l'index sitemap répond 200 mais
  ses 3 sous-fichiers déclarés renvoient tous 404).
- **`loot-factory.com`** — certificat SSL/TLS invalide côté serveur
  ("unable to get local issuer certificate", chaîne de certificats
  incomplète) — bloque toute requête HTTPS avant même d'atteindre
  `/products.json`. Pas de contournement raisonnable sans désactiver la
  vérification TLS (hors de question).
- **`uturitrading.com`** — VRAI Shopify confirmé (signaux `cdn.shopify.com`
  présents, page d'accueil accessible), mais `/products.json` renvoie 404
  — l'endpoint JSON public semble désactivé volontairement côté marchand.
  Alternative sitemap.xml non investiguée (faible priorité).
- **Cardmarket** — explicitement hors scope (protection anti-bot
  volontairement dissuasive), non exploré par consigne.

## Prochaines étapes suggérées (par ordre de priorité)

1. ~~Committer le fix de symétrie du filtre qualificatif~~ — fait.
2. ~~Terminer le test de non-régression du fix qualificatif sur les listes
   actives complètes des 3 plateformes~~ — fait (81/81 boutiques, plusieurs
   runs, 0 régression).
3. ~~Reprendre le travail de couverture interrompu~~ — fait (cf. section
   dédiée ci-dessus). `investcollect.com` et `lepantheon-tcg.com` intégrées
   aux listes actives PrestaShop ; 8 boutiques diagnostiquées et
   documentées comme non-intégrables (raisons précises par boutique).
4. Surveiller les premiers cycles de prod sur `investcollect.com` — c'est
   la boutique la plus prometteuse trouvée cette session (3 deals réels
   détectés en un seul passage de test), à confirmer sur la durée.
5. `pokemoncarte.com` et `gamespirit.fr` : rien à faire dans l'immédiat,
   mais si la watchlist s'étend un jour vers des cartes plus communes/
   variées, refaire un test rapide (le blocage vient du catalogue, pas de
   la technique).
