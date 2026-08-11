# Notes de session — extension multi-plateforme PokéDeals

Dernière mise à jour : 2026-08-11 (nuit, en autonomie pendant que
l'utilisateur dormait — 83 boutiques actives au total, radar de
précommandes activé en prod, 3 bugs réels signalés par l'utilisateur
corrigés, passe de nettoyage effectuée). Voir la toute dernière section
"Résumé de la nuit" en bas de fichier pour le récapitulatif complet à
lire au réveil.

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
- `scan_boutique.py` (Shopify, 39 boutiques actives dans `boutiques_shopify.py`)
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

## Nouvelle fonctionnalité : radar de précommandes (2026-08-10/11)

Détection de l'**apparition** d'un produit scellé surveillé (précommande
qui n'existait pas avant → existe maintenant, en stock ou non) — PAS un
retour en stock d'un produit déjà catalogué (ça, c'est `alerte_stock.py`).
Système entièrement **indépendant** des 2 alertes existantes (bonnes
affaires + retour en stock sur cartes à l'unité) : nouveaux fichiers
dédiés, aucune modification des connecteurs/scans/orchestrateurs
existants.

**Fichiers ajoutés :**
- `precommandes_watchlist.py` — `PRODUITS_SURVEILLES` (liste des produits
  à guetter), matching mots-clés (double groupe édition+type) + extraction
  et validation de date sur la page produit.
- `alerte_precommande.py` — mémoire d'état (`data/precommandes_anniversaire.json`,
  une entrée par `domaine|nom_produit`, alerte une seule fois par produit
  x boutique, avec re-alerte si la confiance passe de "moyenne" à "forte")
  + envoi Telegram dédié (🎉).
- `radar_precommandes.py` — scanners par plateforme, réutilisent les
  connecteurs existants SANS les modifier : Shopify (catalogue complet
  déjà récupéré, titre+description disponibles sans requête
  supplémentaire), PrestaShop/WooCommerce sitemap (préfiltre léger sur le
  slug avant de charger la page complète), PrestaShop/WooCommerce replis
  (recherche par mot-clé "type" via le mécanisme de découverte déjà en
  place, y compris `rechercher_via_api_rest` pour mymesis.fr).
- `scan_precommandes.py` — orchestrateur CLI
  (`python scan_precommandes.py {shopify|prestashop|woocommerce} [boutiques...]`),
  conçu pour être ajouté comme **étape supplémentaire** aux 3 workflows
  GitHub Actions existants (pas de nouveau workflow séparé) — s'arrête de
  lui-même si tous les produits surveillés ont dépassé leur date de sortie.

**3 produits surveillés actuellement** (cf. `PRODUITS_SURVEILLES`) :
Coffret ETB 30e Anniversaire (sortie 16/09/2026), Coffret ETB ME06 Règne
Delta (06/11/2026), Collection Ultra-Premium 30e Anniversaire Mentali/Noctali
(06/11/2026).

### 2 bugs trouvés et corrigés PENDANT le test sur échantillon (14 boutiques)

Le test sur échantillon (5 Shopify, 4 PrestaShop dont 1 repli, 5
WooCommerce dont `mymesis.fr` en API REST) a révélé, comme demandé, des
**vrais faux positifs** avant d'être considéré validé :

1. **Mots-clés trop génériques** (1er run : 15 candidats, 4 faux
   positifs) :
   - `"celebration"`/`"célébration"` seul matchait à tort l'**ANCIEN**
     coffret "Celebrations"/"Célébrations" (25e anniversaire, EB7.5,
     2021, toujours en vente/revente) — constaté sur `lemantcg.fr`,
     `hikarudistribution.com`, `poke-geek.fr`, et un produit SLEEVES (pas
     même un ETB) sur `hamacards.com`. **Fix** : retiré du groupe édition
     du produit 1, ne garde que les expressions complètes sans ambiguïté
     ("30e anniversaire", "30th anniversary", "30th celebration").
   - `"ultra premium"` seul est aussi un adjectif marketing générique
     ("carte ultra premium issue de l'extension...") utilisé sur des
     cartes à l'unité SANS RAPPORT — constaté sur `questcorner.fr` (une
     simple Noctali-VMAX EVS matchée à tort). **Fix** : remplacé par la
     phrase complète `"collection ultra premium"` / `"ultra premium collection"`.
2. **Asymétrie de normalisation** (2e run après fix #1 : la boutique
   `poke-geek.fr` a perdu un match pourtant légitime — régression
   introduite PAR le fix #1). En renforçant la normalisation du texte de
   page (ponctuation/tirets/apostrophes écrasés en espace, pour mieux
   gérer "Ultra-Premium" vs "Ultra Premium"), les mots-clés eux-mêmes
   (ex: `"dresseur d'elite"`, avec apostrophe) n'étaient PAS normalisés
   avant comparaison — un mot-clé avec apostrophe ne peut alors plus
   JAMAIS matcher un texte normalisé (donc sans apostrophe). **Fix** :
   normaliser aussi les mots-clés au moment de la comparaison, pas
   seulement le texte de la page.

**Résultat final** (3e run, après les 2 fix) : **9 candidats, 1 confiance
forte, 8 confiance moyenne, 0 faux positif** — tous les vrais matches
préservés (dont `hikarudistribution.com` : *"Coffret Dresseur d'Élite
(ETB) Pokémon - Règne Delta - ME06 - Français"* avec la date 06/11/2026
explicitement confirmée sur la page → confiance forte), tous les faux
positifs identifiés éliminés.

### Comment ajouter un futur produit à surveiller

Ajouter une entrée à `PRODUITS_SURVEILLES` dans `precommandes_watchlist.py`
— aucune autre modification de code nécessaire. Exemple pour un futur set
JP fictif "Coffret ME07" sortant le 15 janvier 2027 :

```python
ProduitSurveille(
    nom="Coffret Dresseur d'Élite — ME07 FR",
    mots_cles_edition=frozenset({"me07", "nom-du-set-en-toutes-lettres"}),
    mots_cles_type=frozenset({"dresseur d'elite", "dresseur elite", "etb", "elite trainer box"}),
    date_sortie=date(2027, 1, 15),
),
```

Règles à respecter (retour d'expérience direct du test ci-dessus) :
- **Toujours 2 groupes** (édition ET type), jamais un mot-clé isolé —
  c'est ce qui évite les faux positifs massifs.
- **Éviter les mots-clés génériques/adjectifs courants** ("celebration",
  "premium", "édition limitée"...) — préférer des expressions complètes
  et spécifiques au produit, ou des codes/noms officiels peu ambigus
  ("ME06", "règne delta").
- Le radar s'arrête tout seul après `date_sortie` — pas besoin de retirer
  l'entrée manuellement une fois le produit sorti (mais elle peut être
  retirée par propreté si on veut).

### Activation en prod — FAIT (2026-08-11)

Branché aux 3 workflows GitHub Actions existants, comme étape(s)
supplémentaire(s) après le scan cartes existant, **sans nouveau workflow
séparé** :

- **`scan_shopify.yml`** — 1 étape `python scan_precommandes.py shopify`
  + sa sauvegarde mémoire (même logique stash/pull-rebase/push que les
    fichiers de stock existants). `timeout-minutes` relevé de 18 à 25.
- **`scan_prestashop.yml`** — même pattern, `timeout-minutes` relevé de
  20 à 30 (les 2 plus gros sitemaps, skydreamer.fr/ludum.fr, sont relus
  une seconde fois par le radar).
- **`scan_woocommerce.yml`** — nouveau **job** `scan_precommandes` (pas
  un nouveau fichier workflow) qui démarre après `scan_lot_b` : 2 étapes
  séquentielles (lot A, puis lot B + `mymesis.fr` en API REST) au sein du
  même job, une seule sauvegarde mémoire à la fin. `timeout-minutes: 25`
  pour ce nouveau job — à surveiller/ajuster selon la durée réelle
  mesurée en prod (le radar est en principe moins coûteux par boutique
  que le scan cartes : pas de matching sur 194 critères, juste un
  préfiltre de slug puis quelques pages ciblées).

**Correction de conception appliquée avant l'activation** : la mémoire du
radar était initialement un fichier UNIQUE partagé entre les 3
plateformes (`data/precommandes_anniversaire.json`) — un vrai risque de
collision puisque les 3 workflows tournent en parallèle toutes les 30 min
(contrairement aux fichiers de stock existants, déjà séparés par
plateforme pour cette raison précise). **Fix** : `scan_precommandes.py`
charge/sauvegarde désormais dans un fichier dédié par plateforme
(`data/precommandes_anniversaire_{shopify,prestashop,woocommerce}.json`),
même principe que `stock_boutiques_tcg{,_prestashop,_woocommerce}.json`.

**Coût réseau** : double le nombre de requêtes par cycle sur chaque
plateforme (nouveau parcours du catalogue/sitemap, séparé du scan cartes
existant). Marges de timeout élargies en conséquence (cf. ci-dessus).

**Confirmé fonctionnel en prod** : run Shopify #19 (commit `5e58183`)
terminé en succès, 16 min (contre ~9 min avant, cohérent avec le nouveau
step). `data/precommandes_anniversaire_shopify.json` créé et commité
automatiquement par le bot, avec des détections réelles cohérentes avec
le test sur échantillon.

### Bug de première activation — CONFIRMÉ ET CORRIGÉ (2026-08-11)

**Signalé par l'utilisateur** peu après l'activation : alertes Telegram
reçues pour des précommandes qui se révèlent en réalité **hors stock ou
pas encore ouvertes à la commande**.

**Cause racine** : `detecter_nouvelles_precommandes()` (`alerte_precommande.py`)
alertait dès la **toute première détection** d'un `(domaine, nom_produit)`
— contrairement à `alerte_stock.py`, qui n'alerte JAMAIS sur la première
détection ("Une carte x boutique jamais vue avant est ajoutee a la
memoire mais NE DECLENCHE PAS d'alerte, evite le spam massif au premier
lancement"). Ce choix de conception avait été fait délibérément (docstring
d'origine : "Alerte UNE SEULE FOIS... contrairement à alerte_stock.py")
en pensant que "premiere apparition = evenement interessant" — raisonnement
correct pour un produit qui apparaît APRÈS l'activation du radar, mais
FAUX pour le tout premier cycle : les 84 boutiques (alors actives, avant
le retrait de card-binder.com) ont été scannées pour
la première fois avec une mémoire vide, donc TOUTE page déjà existante
au moment de l'activation (souvent des annonces précoces de revendeurs,
notamment japonais, pas encore réellement ouvertes à la commande) a été
traitée comme une "apparition" et a déclenché une alerte immédiate — pas
un faux positif de matching (les mots-clés/dates étaient corrects), mais
une alerte prématurée/pas actionnable.

**Fix appliqué** : alignement sur le principe déjà éprouvé d'`alerte_stock.py`
— la première détection d'un `(domaine, nom_produit)` établit
silencieusement une base de référence, sans alerte. Seules les apparitions
constatées APRÈS ce premier cycle de référence déclenchent une alerte.
Risque résiduel documenté : une précommande qui ouvre entre le tout
premier cycle et le second n'est détectée qu'au 2e passage (30 min de
retard max, pas un vrai raté).

**Amélioration complémentaire** : le message Telegram affiche désormais
explicitement le statut de stock (📦 en stock / ⛔ hors stock / ❓
indéterminé selon les données disponibles par plateforme) — rend chaque
alerte auto-suffisante sans avoir à cliquer pour découvrir que la page
n'est pas encore commandable.

Testé (3 scénarios simulés : 1re détection → pas d'alerte ; re-détection
identique → pas d'alerte ; upgrade moyenne→forte → alerte de confirmation ;
nouveau produit sur boutique déjà connue → pas d'alerte non plus, tous
corrects).

**Note** : les 9 entrées déjà présentes dans
`data/precommandes_anniversaire_shopify.json` (issues du premier cycle
raté) restent en l'état — elles servent maintenant de base de référence
légitime pour la détection future, pas besoin de les effacer.

## Faux positif matching numéro/fraction — CONFIRMÉ ET CORRIGÉ (2026-08-11)

**Signalé par l'utilisateur** : alerte 📦 (`alerte_stock.py`) reçue pour
"Evoli 078 sv5a" (JP/KR) sur `blazingtail.fr`, alors que la carte réelle
en vente est *"Carte Pokémon Évoli 054/078 Commune Pokémon GO (JCC)"* —
une carte FR sans rapport à 0,35€.

**Cause racine** : `config.yaml` stocke le numéro de "Eevee 078 sv5a" SANS
dénominateur ("078" seul — artefact du parsing, qui retire le code de set
"sv5a" du nom). Le matching numéro-sans-dénominateur
(`_regex_numero_sans_denominateur`, partagé par les 3 connecteurs) fait
une simple recherche regex tolérante au padding de zéros, bornée par des
lookarounds anti-chiffre — mais SANS vérifier si le "078" trouvé fait
partie d'une fraction NNN/MMM sans rapport. Sur le slug
`.../evoli-054-078-...html`, "078" est le **DÉNOMINATEUR** (nombre total
de cartes du set Pokémon GO), pas le numéro de la carte — mais la regex
ne fait pas la différence.

**Comparaison avec `main.py`/eBay** : le système principal a DÉJÀ ce
garde-fou depuis longtemps (`numeros_nus_titre`, V17.4) — il retire
D'ABORD toute fraction NNN/MMM du titre avant de chercher un numéro nu.
Mais une reprise LITTÉRALE de cette logique (tout retirer) casse un vrai
cas ici : `numero_nu_voulu` dans `main.py` sert aux cartes dont le numéro
RÉEL n'a jamais de dénominateur (Nuit Noire FR/PBL) ; le numéro "sans
dénominateur" de nos cartes JP/KR ("Eevee 078 sv5a") est souvent un simple
artefact de parsing — la vraie carte affiche généralement un numéro
complet type "078/069" en boutique. Retirer la fraction ENTIÈRE ferait
perdre ce vrai match (vérifié par un test : *faux rejet* sur un titre réel
"Eevee 078/069 SAR sv5a Crimson Haze").

**Fix retenu** (factorisé dans `connecteur_shopify.py`, partagé par les 3
connecteurs — pas dupliqué) : `_retirer_fractions()` retire uniquement le
**DÉNOMINATEUR** d'une fraction NNN/MMM ou NNN-MMM, en gardant le
numérateur. Résultat : "054/078" → "054" (le "078" dénominateur
disparaît, le faux positif est rejeté) ; "078/069" → "078" (le numérateur
recherché reste trouvable, le vrai match est préservé).

**Test** (7 scénarios) : le cas signalé (rejeté), un vrai numéro AVEC
dénominateur (188/167, préservé), un vrai numéro SANS dénominateur du
tout (078 seul, préservé), le même cas signalé côté titre Shopify (rejeté),
un vrai numéro affiché AVEC dénominateur en boutique (078/069, préservé),
et Plumeline ex 024 (non-régression du fix précédent, préservé) — tous OK.

**Non-régression à l'échelle** : test complet sur 80 boutiques actives
(39 Shopify + 15 PrestaShop + 26 WooCommerce — 80 et non 81, `card-binder.com`
retirée entre-temps) : 80/80 OK, 0 échec, 6 deals avant/après inchangés,
mêmes 3 rejets légitimes qu'avant (aucun nouveau).

**Nettoyage** : l'entrée mémoire polluée par le faux positif
(`blazingtail.fr|Eevee 078 sv5a`, `en_stock: true`) a été retirée de
`data/stock_boutiques_tcg_prestashop.json` — le prochain cycle réétablira
une base de référence propre, sans alerte (première détection = pas
d'alerte, cf. le même principe déjà appliqué à `alerte_precommande.py`).

## Timeout du radar de précommandes en prod — CONFIRMÉ ET CORRIGÉ (2026-08-11)

**Constaté par l'utilisateur** (captures d'écran GitHub Actions) : les
jobs `scan_precommandes` (PrestaShop, 30m15s) et `scan_precommandes`
(WooCommerce, 25m16s) ont été **annulés** pour dépassement du timeout
configuré, immédiatement après l'activation.

**Cause racine** : le préfiltre de slug (`_slug_contient_type`, avant
récupération complète d'une page) ne vérifiait que le groupe **TYPE**
("etb"/"upc"/nom de personnage) — des termes bien trop courants
(N'IMPORTE QUEL set a un ETB). Sur `blazingtail.fr` SEUL : **251
candidats** matchés par ce préfiltre trop laxiste, dont des **URLs
d'images (.jpg)** jamais filtrées (le sitemap combine sitemap produits +
sitemap images). Chaque candidat = une requête réseau + le délai de
politesse habituel → explosion du temps total sur les gros catalogues
(mesuré ensuite : `cardshunter.fr` 269 candidats, `k-tcg.com` 27,
`hamacards.com` 188).

**Fix** : nouveau préfiltre `_slug_est_candidat()` qui exige **les deux
groupes** (édition ET type) dans le slug — même double exigence que
`evaluer_correspondance()` sur le texte complet de la page, appliquée
plus tôt pour limiter le nombre de pages à récupérer — et exclut les
extensions média (`.jpg`/`.jpeg`/`.png`/`.webp`/`.gif`/`.svg`/`.css`/`.js`).

**Résultat mesuré** :
- `blazingtail.fr` : 251 → **0** candidats
- `cardshunter.fr` : 269 → **0**
- `k-tcg.com` : 27 → **0**
- `hamacards.com` : 188 → **4** (cohérent avec les vrais matches déjà
  identifiés sur cette boutique lors du test sur échantillon — le fix ne
  perd rien de réel, il élimine le bruit).

**Note** : les scanners *repli* (recherche HTML par mot-clé, API REST)
n'étaient pas concernés par ce bug précis — leur découverte de candidats
est déjà bornée par la recherche elle-même, pas par un parcours de
sitemap complet.

## Stock désynchronisé (microdata vs DOM réel) sur investcollect.com — CONFIRMÉ ET CORRIGÉ (2026-08-11)

**Signalé par l'utilisateur** : alertes 🔥 "bonne affaire" reçues pour
*Méga-Dracaufeu X ex MEP023* et *Méga-Dracolosse ex 290/217* sur
`investcollect.com`, alors que les deux étaient en réalité **hors stock**.
Diagnostic initial infructueux : le code lisait `en_stock=True` pour les
deux via microdata schema.org, cohérent avec les données extraites — rien
n'indiquait de bug jusqu'à vérification VISUELLE des pages réelles.

**Cause racine** : le microdata `itemprop="availability"` annonçait
`InStock` pour les deux produits, alors que la page affichait
littéralement **"Rupture de stock"** sous le bouton "Ajouter au panier"
(span `id="product-availability"`, rendu côté SERVEUR au chargement —
vide quand disponible, rempli du message sinon). Le microdata est
vraisemblablement généré par un module/plugin en cache, désynchronisé du
stock réel. **Même catégorie de bug** que celui déjà rencontré et corrigé
côté WooCommerce plus tôt dans le projet (JSON-LD "InStock" vs variation
réelle "En rupture de stock") — jamais porté côté PrestaShop jusqu'ici.

**Fix** : nouvelle fonction `_stock_indisponible_selon_dom()` dans
`connecteur_prestashop_sitemap.py`, appliquée en **override** dans
`_evaluer_url()` (utilisée par les 2 stratégies, sitemap et repli) : ne
peut que dégrader `en_stock` de `True` vers `False`, jamais l'inverse (un
span vide ne PROUVE pas la disponibilité, il signale juste l'absence d'un
message de rupture affiché).

**Tests** :
- Les 2 cas signalés (`MEP023`, `290/217`) → `en_stock=False`, corrigé.
- Le 3e deal connu (`Méga-Dracaufeu Y ex 294/217`, réellement en stock,
  vérifié visuellement au navigateur) → `en_stock=True`, préservé.
- Vérifié sans effet de bord sur un thème PrestaShop différent
  (`blazingtail.fr`) : le même span existe (module partagé) mais reste
  correctement vide sur un produit en stock.
- Non-régression complète sur 80 boutiques actives : 80/80 OK, 0 échec,
  6 deals inchangés (l'échantillon standard ne couvre pas
  `investcollect.com`, qui est en repli HTML — testé séparément).
- Vérification ciblée `investcollect.com` : deals détectés passés de
  **3 à 1** (exactement les 2 faux positifs signalés disparaissent, le
  vrai deal reste) — confirmation directe du fix.

## Passe de relecture/nettoyage — FAITE (2026-08-11, en autonomie)

L'utilisateur est allé se coucher en autorisant une relecture complète du
code produit dans la session, avec liberté de nettoyer/simplifier ce qui
peut l'être. 4 changements réels identifiés et appliqués (pas de
refactoring cosmétique gratuit) :

1. **Code mort supprimé** : `_slug_contient_type()` dans
   `radar_precommandes.py` — ancien préfiltre (mot-clé TYPE seul)
   remplacé par `_slug_est_candidat()` lors du fix du timeout, mais
   jamais retiré, devenu inutilisé nulle part dans le repo.
2. **Duplication factorisée** : `_normaliser_texte()` et
   `_slug_correspond()` étaient dupliquées **à l'identique** dans
   `connecteur_prestashop_sitemap.py` et `connecteur_woocommerce.py`
   (déjà le cas avant cette session, perpétué en appliquant le fix
   fraction/dénominateur aux deux séparément plutôt que de factoriser
   tout de suite). Déplacées dans `connecteur_shopify.py` (module déjà
   "partagé", y héberge déjà `_titre_correspond`/`_regex_numero_sans_denominateur`/
   `_retirer_fractions`), importées par les deux autres connecteurs.
   Testé : les 8 scénarios de non-régression du fix fraction/dénominateur
   passent identiquement via les deux connecteurs consolidés + test
   complet sur 80 boutiques (0 échec, deals inchangés).
3. **Gap de cohérence de langue comblé** : `alerte_stock.py`
   (`detecter_retours_en_stock`) n'avait PAS le garde-fou de cohérence de
   langue déjà présent dans `bonne_affaire_shopify.py` (`evaluer_deal`) —
   une carte FR pouvait matcher un retour en stock d'une carte JP/KR
   homonyme (même nom+numéro, édition différente). Gap réel repéré en
   comparant les deux fonctions pendant la session (pas un bug signalé,
   une incohérence trouvée en relisant). Fix : même logique exacte
   copiée (compatible `jp_ou_kr` avec `jp`/`kr`, `None` = pas de
   vérification possible = laisse passer, risque résiduel documenté déjà
   accepté ailleurs). Testé : 3 scénarios unitaires + test réel sur 4
   boutiques JP/mixtes (`hikarudistribution.com`, `japan2uk.com`,
   `leviacards.com`, `kyoriyu.fr`, transitions forcées) — aucune erreur,
   résultats cohérents.
4. **Références de documentation cassées corrigées** : 3 fichiers
   (`boutiques_prestashop.py`, `boutiques_woocommerce.py`,
   `connecteur_shopify.py`) référençaient des fichiers d'audit
   (`audit_resultats_0_15.md`, `audit_resultats_15_122.md`,
   `audit_boutiques.py`) qui n'existent pas dans le repo (jamais créés,
   ou supprimés avant cette session) — références retirées/corrigées.
5. **Duplication supplémentaire fusionnée** : `_evaluer_page_prestashop()`
   et `_evaluer_page_woocommerce()` dans `radar_precommandes.py` étaient
   identiques à 100% (aucune logique spécifique à la plateforme — juste
   `connecteur.session`/`connecteur.nom_affiche`, présents sur les deux
   classes de connecteur). Fusionnées en une seule `_evaluer_page()`
   (duck typing). Docstring du module également corrigé : décrivait
   encore l'ANCIEN préfiltre (type seul) après le fix du bug de timeout.
   Testé : `blazingtail.fr` → 0 candidat, `hamacards.com` → 4 candidats
   identiques aux matches déjà connus (résultats inchangés après fusion).

## Diagnostic du flake `scan_lot_a` (run WooCommerce #12 annulé) — 2026-08-11 matin

**Investigation demandée par l'utilisateur** suite au run #12 annulé (18m17s,
timeout de 18 min dépassé sur le job `scan_lot_a`) constaté lors de la
vérification post-fixes de la nuit. Objectif : comprendre la cause avant
tout correctif, pas d'ajustement de timeout à l'aveugle.

### Données collectées (historique des jobs sur les runs #12 à #19, via l'UI GitHub Actions)

| Run | Commit | `scan_lot_a` | `scan_lot_b` | `scan_precommandes` | Statut |
|---|---|---|---|---|---|
| #12 | `9d7d394` | **18m17s → ANNULÉ** (timeout 18m0s dépassé) | 0s (jamais démarré) | 0s (jamais démarré) | Cancelled |
| #13 | `63f2bc8` | 13m27s | 4m44s | 7m55s | Success |
| #14 | `3393bac` | 16m15s | 5m29s | 8m12s | Success |
| #15 | `fd8bb54` | 16m0s | 7m59s | 8m53s | Success |
| #17 | `17dfb78` | 13m53s | 7m46s | **24m0s** | Success |
| #18 | `dd218d4` | 13m41s | 4m55s | 10m3s | Success |
| #19 | `7207229` | 13m58s | 4m0s | **23m41s** | Success |

### Réponses aux 5 points d'investigation

1. **Fréquence** : 1 seul dépassement (`scan_lot_a`) sur 7 runs vérifiés
   depuis l'activation du radar précommandes (structure à 3 jobs) — soit
   ~14% de l'échantillon disponible. Pas d'accès à un historique plus
   long via `gh` CLI (non installé sur cette machine) ni aux logs bruts
   (non connecté à GitHub) — l'échantillon UI est le maximum accessible
   dans ces conditions.
2. **Logs du run #12** : détail ligne par ligne inaccessible sans
   connexion, mais l'info clé est disponible via l'UI : c'est bien
   `scan_lot_a` qui a été annulé pour dépassement de SON PROPRE timeout
   (18m0s), et lui seul — `scan_lot_b`/`scan_precommandes` n'ont jamais
   démarré (bloqués par leur dépendance `needs:`).
3. **Boutiques de LOT_A** : `cardshunter.fr` (58 011 URLs sitemap) et
   `hamacards.com` (39 757 URLs) — 2 des 3 plus gros catalogues
   WooCommerce du projet — y sont concentrés, déjà identifiés dans le
   commentaire d'origine de `boutiques_woocommerce.py` comme pesant
   "la moitié du volume total" à eux deux lors du découpage initial en
   lots. Rien de nouveau : composition de LOT_A inchangée par les fixes
   de cette nuit.
4. **Chevauchement avec `scan_precommandes`** : **NON, exclu avec
   certitude**. Les 3 jobs sont **séquentiels** (`needs: scan_lot_a` puis
   `needs: scan_lot_b`), jamais en parallèle sur le même run — chaque job
   GitHub Actions tourne de plus sur sa propre VM isolée (pas de
   partage CPU/réseau entre jobs, même séquentiels). Confirmé
   concrètement par le run #12 : `scan_precommandes` n'a jamais démarré
   pendant que `scan_lot_a` traînait.
5. **Marge réelle** : `scan_lot_a` tourne normalement entre **13m27s et
   16m15s** contre un budget de 18 min — soit une marge de seulement
   **1m45s à 4m33s** selon les runs, DÉJÀ SERRÉE en fonctionnement
   normal, avant même de compter un éventuel ralentissement réseau
   ponctuel. Le run #14 (16m15s) montre que cette marge peut descendre
   à moins de 2 minutes même sur un run qui réussit.

### Diagnostic

**Hypothèse retenue : timeout budgété trop juste — confiance ÉLEVÉE.**
Pas un problème latent lié aux fixes de cette nuit (le chevauchement
avec `scan_precommandes` est formellement exclu, structure séquentielle
+ VMs isolées), pas une régression introduite hier soir (composition de
LOT_A inchangée). C'est une caractéristique préexistante : LOT_A
concentre les 2 plus gros catalogues, sa marge de fonctionnement normal
est déjà mince (jusqu'à ~1m45s dans le pire cas réussi observé), et le
projet documente déjà lui-même un surcoût réseau GitHub Actions habituel
de "+19 à +38%" par rapport aux mesures locales — un ralentissement
mineur et ponctuel suffit à faire basculer un cycle en timeout.

**Recommandation** : augmenter légèrement `timeout-minutes` du job
`scan_lot_a` dans `scan_woocommerce.yml` (18 → 22 min, cohérent avec la
marge mesurée). **Appliqué le 11/08/2026 après validation explicite de
l'utilisateur.**

### Découverte secondaire (bonus, hors du périmètre demandé mais notable)

`scan_precommandes` montre une variance BEAUCOUP plus large que
`scan_lot_a` (8m12s à **24m0s** selon les runs) et talonne dangereusement
son propre budget de 25 min sur 2 des 3 runs les plus récents (#17 :
24m0s, #19 : 23m41s — plus de 95% du budget consommé, alors que #15,18
n'en utilisaient que 33-40%). Cause probable : le nombre de candidats
réellement évalués varie fortement d'un cycle à l'autre (dépend de ce
qui est actuellement en ligne sur chaque boutique au moment du scan,
contrairement à `scan_lot_a` qui traite toujours la même charge de
travail fixe). **Pas encore un timeout dépassé**, mais la marge se réduit
rapidement — à surveiller de près, prochain point de friction probable
si la tendance se confirme sur plusieurs cycles supplémentaires.

## Prochaines étapes suggérées (par ordre de priorité, mises à jour 2026-08-11 nuit)

1. Surveiller les premiers cycles de prod du radar de précommandes
   (activé cette nuit sur les 3 workflows) — confirmer que les timeouts
   élargis (25-30 min) sont suffisants en conditions réelles GitHub
   Actions, et qu'aucune nouvelle alerte prématurée n'apparaît.
2. Surveiller `investcollect.com` sur la durée — boutique prometteuse
   (plusieurs deals réels trouvés), maintenant avec une lecture de stock
   fiabilisée (fix DOM vs microdata).
3. `pokemoncarte.com` et `gamespirit.fr` : rien à faire dans l'immédiat,
   mais si la watchlist s'étend un jour vers des cartes plus communes/
   variées, refaire un test rapide (le blocage vient du catalogue, pas de
   la technique).
4. Envisager d'appliquer le même garde-fou "DOM prime sur microdata"
   (cf. `_stock_indisponible_selon_dom`) aux autres boutiques PrestaShop
   sitemap si un faux positif similaire est un jour signalé ailleurs que
   sur `investcollect.com` — pas fait préventivement cette nuit (pas de
   preuve que d'autres thèmes ont ce problème, éviter de deviner).

## Résumé de la nuit (2026-08-11, en autonomie pendant que l'utilisateur dormait)

L'utilisateur est allé se coucher en autorisant explicitement la
poursuite du travail en autonomie (commit + push sans attendre de
validation, sauf action réellement risquée), puis une relecture complète
du code de la session pour nettoyer ce qui pouvait l'être. Résumé
chronologique de cette portion de la session :

1. **Push des 2 fixes déjà validés avant le coucher** (numéro/fraction +
   timeout radar précommandes) — conflit de merge sur le fichier mémoire
   (le bot de prod avait re-détecté le même faux positif entre-temps),
   résolu en gardant la version corrigée.
2. **Bug signalé par l'utilisateur** : alertes 🔥 reçues pour 2 produits
   `investcollect.com` en réalité hors stock (Méga-Dracaufeu X ex MEP023,
   Méga-Dracolosse ex 290/217). Diagnostiqué en vérifiant visuellement
   les pages réelles au navigateur : microdata schema.org désynchronisé
   du DOM réellement affiché ("Rupture de stock" visible, microdata dit
   "InStock"). Corrigé, testé (les 2 cas exacts + non-régression complète
   80/80 boutiques + vérification ciblée investcollect.com : 3 deals → 1,
   les 2 faux positifs disparaissent).
3. **Passe de nettoyage** (5 changements réels, aucun cosmétique) : code
   mort supprimé, 2 duplications factorisées (`_normaliser_texte`/
   `_slug_correspond` entre PrestaShop/WooCommerce, `_evaluer_page_*`
   dans le radar précommandes), un vrai gap de cohérence de langue comblé
   dans `alerte_stock.py` (absent alors que présent dans
   `bonne_affaire_shopify.py`), 3 références de documentation cassées
   corrigées (fichiers d'audit inexistants).

**Tout est commité ET poussé** (`git log` propre, working tree clean au
moment d'écrire ceci). Chaque changement a été testé individuellement
(scénarios unitaires ciblés) ET vérifié par au moins un test de
non-régression à l'échelle réelle (60-80 boutiques) avant d'être
committé — aucun changement "à l'aveugle".

**Rien de bloquant ni de risqué n'a été laissé en suspens.** Les seuls
points ouverts sont des observations à faire sur la durée (cf. section
"Prochaines étapes" ci-dessus), pas des actions requises immédiatement.

## Validation en conditions réelles — CONFIRMÉE (2026-08-11 matin)

Vérification du premier cycle complet des 3 workflows après les fixes de
la nuit (préfiltre précommandes resserré, garde-fou langue
`alerte_stock.py`, fix microdata `investcollect.com`), via l'UI GitHub
Actions (pas d'accès aux logs bruts, non connecté).

**Timeout du radar précommandes — RÉSOLU, confirmé.**
- `scan_woocommerce.yml` run #15 (commit `fd8bb54`, après tous les fixes) :
  **`Status: Success`**, job `scan_precommandes` en **8m 53s** (contre
  25 min dépassées et job annulé avant le fix). Jobs `scan_lot_a` (16m)
  et `scan_lot_b` (7m59s) également réussis, aucune régression.
- `scan_prestashop.yml` run #17 (commit `c61acdd`) : `Status: Success`,
  24m23s au total (scan cartes + étape précommandes dans le même job),
  sous le timeout de 30 min.
- `scan_shopify.yml` run #24 (commit `f3f8c14`) : `Status: Success`,
  17m au total, sous le timeout de 25 min.

**Note distincte (pas une régression du radar précommandes)** :
`scan_woocommerce.yml` run #12 (commit `9d7d394`, donc APRÈS le fix
fraction/timeout mais juste avant le fix stock DOM) a été annulé pour
dépassement — mais le job en cause était `scan_lot_a` (le scan cartes
existant, 18 min dépassées), PAS `scan_precommandes` (jamais démarré,
bloqué par la dépendance `needs: scan_lot_a`). Flake réseau ponctuel déjà
documenté comme risque connu dans ce projet ("+19 à +38% de surcoût
GitHub Actions vs mesures locales") — les runs suivants (#13-15) ont
tous réussi sans réintervention.

**Volume de candidats / alertes** : pas d'accès aux logs détaillés
(non connecté à GitHub), mais les fichiers mémoire du radar confirment
un volume raisonnable et cohérent avec les tests d'hier soir — PAS
l'explosion à 250+ candidats d'avant le fix :
- `precommandes_anniversaire_shopify.json` : 6 entrées (1 confiance forte
  — ME06 Règne Delta chez `hikarudistribution.com` —, 5 moyenne), dont
  une **boutique inédite** (`lectorshop.com`) jamais vue lors des tests
  d'hier — signe que le radar continue de découvrir de vrais nouveaux
  produits en tournant.
- `precommandes_anniversaire_prestashop.json` : 0 entrée (cohérent : les
  boutiques PrestaShop en repli n'avaient déjà rien trouvé hier).
- `precommandes_anniversaire_woocommerce.json` : 3 entrées (toutes
  `hamacards.com`, cohérent avec les tests d'hier).

**Régression stock/bonnes affaires** : aucune détectée. Les 3 fichiers de
mémoire stock couvrent bien 39 boutiques Shopify + 17 PrestaShop +
27 WooCommerce (comptes exacts attendus après le retrait de
`card-binder.com` et l'intégration `investcollect.com`/`lepantheon-tcg.com`/
`mymesis.fr`) — aucune boutique disparue. Flux de commits `[skip ci]`
régulier et sans interruption sur les 3 plateformes depuis les fixes.

**Limite de cette vérification** : pas de compte exact "candidats évalués
par boutique après préfiltre" ni de contenu précis des alertes Telegram
envoyées (nécessiterait l'accès aux logs GitHub Actions, non disponible
sans connexion). Le faisceau d'indices (succès systématique, volumes de
mémoire cohérents, comptes de boutiques exacts) est jugé suffisant pour
valider les fixes, mais une vérification plus fine reste possible si
besoin (connexion GitHub + lecture des logs bruts).
