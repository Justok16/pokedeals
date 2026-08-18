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

**⚠️ Section partiellement obsolète — voir "État du programme" en toute fin
de fichier pour l'inventaire à jour et faisant foi.** Conservée telle
quelle pour l'historique.

**Connecteurs (un par plateforme, structure `ResultatRecherche` commune) :**
- `connecteur_shopify.py` — Shopify, `/products.json`, détection de langue partagée par les 3 connecteurs
- `connecteur_prestashop_sitemap.py` — PrestaShop, sitemap XML + JSON-LD + repli microdata (`itemprop=`) + repli recherche HTML (`?controller=search&s=`) pour les boutiques sans sitemap
- `connecteur_woocommerce.py` — WooCommerce, sitemap XML (Yoast/AIOSEO/natif WP) + JSON-LD + repli classes CSS natives + repli recherche HTML (`?s=`) + détection produit variable

**Watchlist et structures partagées :**
- `watchlist_shopify.py` — `CarteWatchlist`, parsing de `config.yaml` (`charger_watchlist_config`), `ECHANTILLON_CONFIG` (10 cartes de test, jamais utilisé en prod)

**Logiques d'alerte (génériques, agnostiques du connecteur) :**
- `bonne_affaire_shopify.py` — seuil de prix/cote, garde-fous devise + langue + qualificatif + décote ≥30%
- `alerte_stock.py` — retours en stock (mémoire JSON par plateforme), mêmes garde-fous langue + qualificatif que `bonne_affaire_shopify.py`

**Orchestrateurs (un par plateforme, appelés par les workflows) :**
- `scan_boutique.py` (Shopify, 39 boutiques actives dans `boutiques_shopify.py`)
- `scan_boutique_prestashop.py` (PrestaShop, 17 boutiques actives dans `boutiques_prestashop.py` — 15 couvertes par sitemap + 2 via repli recherche HTML : `investcollect.com`, `lepantheon-tcg.com`, cf. section dédiée ci-dessous)
- `scan_boutique_woocommerce.py` (WooCommerce, 27 boutiques actives dans `boutiques_woocommerce.py` — 26 sitemap + `mymesis.fr` via repli API REST, scindées en 2 lots équilibrés par volume d'URLs pour le workflow)

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

## Audit de santé complet — 2026-08-11 après-midi

Passe méthodique demandée par l'utilisateur : points chauds connus,
recherche libre d'angles morts, nettoyage général, vérification de
sécurité (secrets), non-régression avant/après. Résumé structuré
ci-dessous — **c'est cette section, avec "État du programme" juste après,
qui fait foi pour une reprise rapide en début de prochaine session.**

### Trouvé et corrigé

- **4 duplications de code factorisées** (angles morts du même type que le
  gap de langue `alerte_stock.py` trouvé la veille) :
  - `_echapper_html`/`_echapper_url_html` (identiques dans 3 fichiers) →
    nouveau `telegram_utils.py`.
  - `charger_memoire`/`sauvegarder_memoire` (identiques dans 2 fichiers) →
    nouveau `memoire_json.py` (wrappers minces conservés dans chaque
    module pour préserver le défaut `FICHIER_MEMOIRE` existant).
  - `_est_xml_valide` (identique entre PrestaShop/WooCommerce) →
    factorisée dans `connecteur_shopify.py`.
- **Imports morts retirés** : 3 imports devenus inutiles suite à la
  consolidation de la veille (non nettoyés sur le coup), + `traceback`/
  `Path` jamais utilisés dans `scan_boutique.py` (pré-existant, trouvé au
  passage).
- **`NOMS_SET_QUALIFICATIF_AMBIGU`** : le besoin d'entretien manuel
  périodique était documenté uniquement dans `SESSION_NOTES.md`, pas
  découvrable depuis le code lui-même — ajouté un flag explicite
  "ENTRETIEN MANUEL REQUIS" directement en commentaire. Confirmé qu'il
  n'existe pas d'approche positionnelle plus robuste (déjà écartée lors
  du fix original : mesures de distance montrant un faux positif et un
  vrai rejet à la même distance du numéro, indiscernables).
- **Section "Fichiers concernés"** de `SESSION_NOTES.md` (écrite tôt dans
  la session, jamais mise à jour depuis) : comptes de boutiques et
  description des garde-fous `alerte_stock.py` corrigés, marquée comme
  partiellement obsolète au profit de la présente section.
- **Correction d'une hypothèse antérieure** : la "dérive de durée" de
  `scan_precommandes` (8m53s → 23-24min) n'est PAS une dérive continue —
  2 pics isolés (#17, #19) encadrés de cycles normaux (8-10 min), stable
  depuis sur 3 cycles consécutifs (#20-22 : 8m25s-8m47s). Reclassé de
  "à surveiller de près" à "sain, cause des 2 pics non identifiée avec
  les outils disponibles mais non récurrente".

**Aucun changement de comportement de matching, de seuil ou de logique
métier dans cette passe** — uniquement structurel (factorisation,
suppression de code mort, documentation). Confirmé par une non-régression
complète AVANT (80/80 boutiques, 6 deals, 3 rejets légitimes) et APRÈS
(identique) tous les changements.

### Vérifié et confirmé sain

- **Sécurité / secrets** : aucun token en clair dans le code actuel ni
  dans l'historique git complet (892 commits scannés, recherche par motif
  de token Telegram + recherche de fichiers `.env`/secrets jamais
  committés). Les 3 workflows référencent bien `${{ secrets.TELEGRAM_BOT_TOKEN }}`
  partout, jamais de valeur en dur.
- **`investcollect.com`** : les 2 faux positifs corrigés la veille
  (Méga-Dracaufeu X ex MEP023, Méga-Dracolosse ex 290/217) restent
  correctement détectés comme hors stock sur plusieurs cycles de
  production réels (dernière vérification : `12:45:33Z`). Spot-check en
  direct d'une carte supplémentaire (`Dracaufeu ex 199/165`, transition
  True→False) confirmé cohérent avec la page réelle.
  Fix stable, pas de régression.
- **Garde-fous entre connecteurs** : `bonne_affaire_shopify.py` et
  `alerte_stock.py` appliquent désormais les MÊMES garde-fous dans le
  MÊME ordre (en_stock → langue → qualificatif symétrique), vérifié ligne
  par ligne. Le radar de précommandes n'a pas d'équivalent direct
  (modèle de matching différent, mots-clés + date plutôt que nom+numéro)
  mais applique une rigueur structurellement comparable (double exigence
  édition+type + confirmation par date).
- **Format des fichiers mémoire (`data/*.json`)** : les 3 fichiers de
  stock (`stock_boutiques_tcg{,_prestashop,_woocommerce}.json`) partagent
  un schéma identique (`{domaine}|{nom_config}` → `{en_stock,
  derniere_verification}`), de même pour les 3 fichiers de précommandes
  (`{domaine}|{nom_produit}` → `{confiance, raison, titre_produit,
  url_produit, derniere_verification}`). Les deux familles ont des
  schémas différents entre elles, ce qui est attendu (objets suivis
  différents) — pas d'incohérence involontaire trouvée.
- **Encodage des fichiers mémoire précommandes** : fausse alerte
  initiale (caractères accentués affichés en `�` lors d'un diagnostic via
  la console Windows/Bash) — vérifié avec l'outil de lecture de fichier
  dédié que le contenu réel est du UTF-8 propre (`Élite`, `Pokémon`
  s'affichent correctement). Aucune corruption réelle, juste une
  limitation d'affichage de la console cp1252 utilisée pour le
  diagnostic.

### En observation (pas d'action requise, à surveiller sur la durée)

- Les 2 pics isolés de `scan_precommandes` (#17, #19) restent
  inexpliqués précisément (cause non identifiable sans accès aux logs
  bruts GitHub Actions) — si le motif se reproduit, creuser avec un accès
  aux logs.
- `investcollect.com` et le radar de précommandes sont les 2 ajouts les
  plus récents du projet — à revalider une fois de plus après quelques
  jours de recul pour confirmer la stabilité à plus long terme.

### Points nécessitant une décision utilisateur (non tranchés seul)

- **`CLAUDE.md` est significativement obsolète** : il décrit uniquement
  l'ancien système `main.py` (eBay/Vinted/Cardtrader/Leboncoin), sans
  mentionner DU TOUT l'extension multi-plateforme boutiques TCG
  (connecteurs Shopify/PrestaShop/WooCommerce, `bonne_affaire_shopify.py`,
  `alerte_stock.py`, le radar de précommandes, ni les 4 workflows GitHub
  Actions associés). Une future session Claude Code démarrant sur ce
  projet ne trouverait cette extension entière que via `SESSION_NOTES.md`
  (fichier de log chronologique, pas un guide de référence). Mise à jour
  substantielle non faite dans cette passe (hors périmètre "nettoyage",
  plutôt une vraie rédaction de documentation) — à décider si/quand la
  faire, potentiellement dans une session dédiée.

## Session du 2026-08-12 : CLAUDE.md réécrit, revue croisée, 12 boutiques ajoutées, radar de découverte AFNIC

### CLAUDE.md réécrit pour refléter le projet actuel

Décision en attente depuis la session précédente (cf. section "Points
nécessitant une décision utilisateur" ci-dessus) : réécriture complète
demandée par Justok et faite. Nouveau contenu basé sur le code réel et
`SESSION_NOTES.md` comme sources de vérité (pas de mémoire de conversation) :
vue d'ensemble des 3 fonctions actives, architecture réelle (connecteurs,
alertes, radar précommandes), 5 workflows, fichiers de mémoire, 5+ pièges
connus. Validé par Justok avant commit.

### Revue croisée DeepSeek/ChatGPT sur le repo public

Justok a demandé un avis à deux IA concurrentes (repo `alertes-btc` ET
`pokedeals` volontairement publics pour ça, cf. décision déjà actée).
Chaque retour vérifié point par point contre le code réel avant d'agir
(aucune IA n'avait accès au code, plusieurs suggestions étaient déjà
résolues ou fausses) :
- **Confirmé et corrigé** : écriture atomique des `data/*.json` (fichier
  `.tmp` + `os.replace`, dans `main.py` et `memoire_json.py`) — évite un
  fichier tronqué si le process est tué en plein écriture (timeout GH
  Actions). Seul point réel non traité, identifié indépendamment par les
  deux IA.
- **Ajouté** : suite de tests unitaires (`tests/`, pytest, 22 cas) sur les
  fonctions de matching les plus fragiles, un cas par bug réel déjà
  corrigé. Nouveau workflow `tests.yml` (push/PR, séparé des scans).
  `.gitignore` ajouté (absent jusque-là).
- **Écarté à raison** (vérifié faux ou déjà résolu) : "duplication entre
  connecteurs" (déjà factorisée), "URLs codées en dur" (déjà centralisées
  dans `boutiques_*.py`), "timeouts/sessions HTTP manquants" (déjà en
  place), "`cancel-in-progress: true` sur les workflows de scan" (aurait
  cassé le système, ils tournent volontairement en parallèle).

### Bot BTC (`alertes-btc`) : bug de robustesse corrigé

Sur demande de relecture complète : `send_telegram()` pouvait lever une
exception (échec Telegram) AVANT que `state.json` soit sauvegardé —
risque de re-tentative de la même alerte en boucle avec un signal
périmé. Fix : `try/except` autour de l'envoi, `save_state()` s'exécute
toujours, le job échoue quand même visiblement (`sys.exit(1)`) si l'envoi
a raté. Testé (état sauvegardé même avec un token Telegram invalide
simulé). Confirmé : token Telegram partagé entre `alertes-btc` et
`pokedeals` est un choix voulu de Justok, pas une erreur (cf. mémoire
`project_shared_telegram_bot.md`).

### 12 nouvelles boutiques ajoutées, vérifiées une à une

Justok a fourni des captures d'écran + des liens directs pour des
boutiques candidates. Chacune vérifiée techniquement (Shopify/WooCommerce
confirmé + ratio réel de cartes à l'unité avec numéro de collection, pas
juste présence du mot "pokemon") avant intégration — plusieurs faux
positifs trouvés en cours de route :
- **Ajoutées à `BOUTIQUES_SHOPIFY`** (singles) : `playshop.fr` (214/214
  singles tagués "pokemon-tcg"), `kairyu.fr` (74 singles Pokémon sur 190,
  2 vrais deals détectés dès le 1er scan), `kwilytcg.com` (39 singles
  FR/JP/CN), `upcfrance.shop` (singles + scellé), `wwcg.fr` (singles
  confirmés, type "carte pokémon" explicite).
- **Nouveau mécanisme `BOUTIQUES_*_PRECOMMANDE_SEULEMENT`** (Shopify ET
  WooCommerce) : boutiques actives mais 100% scellé (0 carte à l'unité) —
  inutiles pour le scan cartes mais utiles au radar précommandes,
  volontairement PAS dans les listes actives pour ne pas polluer le scan
  cartes de candidats voués à 0 résultat. `lepotoryko.fr`, `bgeek.be`
  (Belge), `cardsarena.fr` (Shopify) + `pokemagique.fr`, `pokeshop.cards`
  (WooCommerce). Câblé dans `scan_precommandes.py` (`_boutiques_et_replis`)
  et une étape dédiée dans `scan_woocommerce.yml`.
- **Rejetées avec raison documentée** (dans `boutiques_shopify.py`) :
  `lorenzone.fr` (boutique Disney LORCANA malgré un nom à consonance
  Pokémon — 243 "singles" trouvés, tous des cartes Lorcana), `europetcg.com`
  (catalogue trop généraliste), `poketropik.fr`/`pokemon-laboutique.fr`
  (certificat SSL invalide, même catégorie que `loot-factory.com`),
  `ton-pokemon.fr` (c'est un blog, pas une boutique), `cartepokemon.shop`/
  `redom.store` (domaine introuvable, DNS ne résout pas), `icekeeper.fr`
  (ne vend aucune carte, juste des boîtiers de protection).
- **Non intégrable en l'état** : `cmay-collections.com` — Shopify confirmé
  mais vitrine "headless" (frontend Next.js personnalisé), n'expose pas
  l'endpoint `/products.json` standard. Nécessiterait un connecteur
  différent (API GraphQL Storefront) — hors périmètre d'un ajout simple,
  documenté comme chantier à part si Justok le souhaite un jour.
- **En attente** : `osakard.com` — Shopify confirmé mais protégé par mot
  de passe (refonte en cours), retour annoncé par Justok pour septembre
  2026, à retester à partir de cette date.

Chaque ajout testé en conditions réelles avant commit (scan réel sur les
nouveaux domaines, pas juste une vérification théorique) + suite de tests
unitaires à chaque fois.

### Radar de découverte automatique de boutiques (AFNIC)

Demande initiale de Justok : un système qui scanne le web en continu pour
trouver de nouvelles boutiques Shopify françaises (recherche moteur +
WHOIS + "outils de scan"). Vérification de faisabilité AVANT de coder
(même démarche que pour CoinGlass/CMC sur le projet BTC) :
- **Recherche web continue gratuite : PORTE FERMÉE en 2026.** Google
  Custom Search API fermée aux nouveaux comptes + dépréciée au
  01/01/2027. Brave Search API a supprimé son tier gratuit pour les
  nouveaux comptes en février 2026 (facturation à l'usage désormais).
  Aucune alternative gratuite et pérenne trouvée pour une vraie recherche
  web par mots-clés.
- **AFNIC (registre officiel .fr) : la vraie bonne surprise.** Publie en
  libre accès, sans clé ni inscription, une liste QUOTIDIENNE des
  nouveaux domaines `.fr` enregistrés
  (`https://www.afnic.fr/wp-media/ftp/domaineTLD_Afnic/YYYYMMDD_CREA_fr.txt`,
  disponible 7 jours sur le serveur — donc un cron hebdomadaire suffit).
  Format texte simple, un domaine par ligne, vérifié en conditions
  réelles (fichier du 11/08/2026 téléchargé et parsé avec succès, 3042
  domaines ce jour-là).
- **Limite assumée et documentée** : ne couvre QUE les `.fr` fraîchement
  créés avec un nom de domaine évocateur — n'aurait pas trouvé la moitié
  des boutiques ajoutées cette même session (`kairyu.fr`, `upcfrance.shop`
  en `.shop`, `kwilytcg.com` en `.com`...). La veille manuelle de Justok
  reste complémentaire, pas remplacée.

Construit (`decouverte_boutiques.py`, workflow hebdomadaire dédié
`decouverte_boutiques.yml`, lundi 06h UTC) : télécharge 7 jours de
listes AFNIC → filtre par mots-clés sur le nom de domaine → vérifie
techniquement chaque candidat (Shopify `/products.json` ou WooCommerce
`product-sitemap.xml`) avec les MÊMES critères objectifs que la
vérification manuelle du jour (numéro NNN/MMM + mention Pokémon
explicite) → ajout AUTOMATIQUE seulement si le signal est net (seuils
stricts), sinon juste rapporté sans ajout → notification Telegram
récapitulative à chaque cycle.

Fichiers auto-gérés **séparés** des listes annotées à la main
(`boutiques_decouvertes.py`, jamais `boutiques_shopify.py`/
`boutiques_woocommerce.py`) pour ne jamais risquer d'écraser leurs
commentaires/contexte accumulés au fil des sessions. Câblé dans
`scan_boutique.py`, `scan_boutique_woocommerce.py`, `scan_precommandes.py`.

**Bug de conception trouvé et corrigé PENDANT le test** (avant tout
commit) : une boutique fraîchement enregistrée avec un catalogue encore
vide (cas réel rencontré en testant : `nemee-tcg.fr`, 1 seul produit)
était mémorisée comme "signal insuffisant" **définitivement** — ne
serait donc plus jamais revérifiée alors que son catalogue pouvait se
remplir dans les semaines suivantes. Fix : seule l'absence totale de
site (aucune plateforme détectée du tout) est mémorisée en permanence ;
un signal "insuffisant" reste re-vérifié à chaque cycle hebdomadaire.

**Testé avant commit** : classification automatique validée sur les 4 cas
déjà connus du travail manuel du jour (`playshop.fr` → singles,
`lorenzone.fr` → rejeté À RAISON malgré le nom Pokémon trompeur,
`bgeek.be` → scellé, domaine inexistant → non_boutique) — tous
correspondent exactement au jugement manuel. Cycle complet exécuté sur
les vraies données AFNIC du jour, round-trip d'écriture du fichier
auto-généré vérifié, suite de tests unitaires (22/22 OK) à chaque étape.

**Non testé en conditions réelles GitHub Actions** (le workflow n'a pas
encore tourné en prod au moment de ce commit, cron hebdomadaire lundi
06h UTC — pas de moyen de le déclencher manuellement sans être connecté à
GitHub). À vérifier au prochain lundi ou via un déclenchement manuel
(`workflow_dispatch`) par Justok si besoin de confirmer plus tôt.

## Session du 2026-08-12/13 : cote Cardmarket affichée, suivi de tendance JP, fix cartes gradées

### Cote Cardmarket affichée sur Telegram (V46)

Justok a transmis un prompt suggéré par DeepSeek : ajouter un mode
`api_cotes.mode = "cardmarket"` qui utiliserait `cardmarket_prix()` comme
SEULE source de cote. **Refusé après vérification** : `cardmarket_prix()`
dépend entièrement du blueprint Cardtrader pour trouver le
`cardmarket_id` — pas une source indépendante. Un mode exclusif
supprimerait tous les garde-fous existants (GARDE-FOU 4 écart eBay,
GARDE-FOU 5 cohérence langue) et réintroduirait exactement le type de
faux positif qu'ils empêchent (cf. Mew ex 208 JP/KR, Méga-Dracaufeu X
3€ vs 1199€, déjà documentés dans le code). Le prompt se trompait même
de nom de fichier ("pokedeals.py" au lieu de `main.py`), signe que
DeepSeek n'avait pas accès au code réel.

**Version retenue** : `prix_cm_affiche` calculé au même endroit qu'avant
(juste après les GARDE-FOU 4/5, donc uniquement quand Cardtrader est
déjà jugé fiable), mais désormais **affiché** dans le message Telegram
("🇪🇺 Cardmarket (tendance)") quel que soit `api_cotes.mode`, sans jamais
toucher à `cote` ni à la logique de décision. Testé (formatage
avec/sans le champ, non-régression du mode `plus_bas`).

### Suivi de tendance de prix long terme — 3 cartes JP (`historique_prix.py`)

Demande de Justok : savoir s'il est intéressant d'acheter une carte
précise selon son historique de prix sur la durée, pour 3 cartes JP
(Plumeline ex/Oricorio ex m2-111, Carapuce/Squirtle sv2a-170,
Psykokwak/Psyduck m2a-199).

**Vérification préalable** (avant tout code) : aucune donnée d'un an
n'existe nulle part — `data/cotes.json` est plafonné à 5 points/carte
(`HISTORIQUE_MAX`) ET purgé à chaque `PURGE_VERSION`. Le "nombre
d'achats" (volume de ventes réelles) n'est accessible gratuitement pour
AUCUNE carte — même mur que l'API eBay Marketplace Insights déjà
rencontré pour le bot BTC.

**Solution construite** : `watchlist_tendance.py` (liste explicite et
réduite, 3 cartes choisies par Justok, pas la watchlist complète) +
`historique_prix.py` (accumulateur quotidien INDÉPENDANT de `cotes.json`,
jamais plafonné ni purgé). Combine [PokemonPriceTracker](https://www.pokemonpricetracker.com)
(API tierce gratuite, `POKEMONPRICETRACKER_API_KEY`, couvre le JP/KR) et
la dernière cote locale en repli. Signal de tendance calculé seulement
au-delà de 14 points accumulés (même logique que `alerte_stock.py` :
pas de conclusion prématurée). Workflow dédié `tendance_prix.yml`, cron
quotidien 8h30 UTC. Alerte Telegram uniquement au CHANGEMENT de signal.

**3 itérations de debug en conditions réelles** (logs fournis par
Justok à chaque fois) :
1. `name`/`number` ne sont PAS des paramètres acceptés par l'API (HTTP
   400) — corrigé en combinant nom+numéro dans `search` (texte libre) +
   `set`.
2. Oricorio ex 111 renvoyait `total:1` mais `data:[]` avec le `set`
   précisé — ajout d'un repli automatique sans `set` si la 1ère
   recherche échoue. Les 3 cartes ont fini par toutes fonctionner.
3. Le repli a révélé la vraie réponse complète : `setName` réel =
   "M2: Inferno X", pas "MEGA Dream ex" que j'avais mis par erreur dans
   `watchlist_tendance.py` (confusion avec le code `m2a` de Psyduck, un
   set différent — c'est d'ailleurs exactement le nom que Justok avait
   donné dès le premier message). Corrigé pour matcher directement sans
   dépendre du repli à l'avenir.

**Conversion USD → EUR** : les prix PokemonPriceTracker sont confirmés
en USD (vérifié via la réponse réelle). Sources de change gratuites
sans clé vérifiées en direct (frankfurter.dev en priorité, repli
open.er-api.com), appliquées UNIQUEMENT à l'affichage Telegram — jamais
aux données stockées ni au calcul de tendance (un écart en % entre 2
valeurs USD reste mathématiquement valide sans conversion). Montant
converti en gras + montant d'origine entre parenthèses, toujours
transparent sur la source. Repli propre si les 2 sources de taux
échouent le même jour (affiche la devise d'origine plutôt que de
bloquer l'alerte).

**Refus explicite de connexion GitHub** : Justok a proposé de me
connecter à son compte GitHub pour lire les logs moi-même (par lassitude
de coller les logs à la main). Refusé : entrer un mot de passe reste
interdit quelle que soit l'autorisation donnée, et un token même en
lecture seule élargirait mon accès à son compte au-delà du nécessaire.
Le partage manuel de logs n'était de toute façon qu'un besoin ponctuel
de mise au point, pas permanent — le système alerte maintenant tout
seul par Telegram.

### Fix cartes gradées non filtrées dans le système boutiques TCG

Justok a reçu 4 alertes Telegram réelles un soir et a demandé si
c'était inquiétant. Analyse alerte par alerte :
- **Écart suspect entre langues** (Squirtle JP 23.19€ vs KR 11.48€,
  ratio 2.02× pour un seuil de 2.0×) : garde-fou `main.py` existant
  (V34/anti-spam, indépendant de cette session), fonctionne comme prévu,
  pas un bug.
- **2× Evoli ex 167/131 sur relictcg.com** (150€ et 220€, "-53.9%" et
  "-32.4%") : **vrai bug confirmé**. Les 2 annonces sont des cartes
  GRADÉES (PSA 8, CCC 9.5) comparées à tort à la cote d'une carte BRUTE.
  Vérifié par grep : `main.py` exclut les cartes gradées depuis
  longtemps (`EXCLUSIONS` : psa/pca/bgs/cgc/gradee/graded + négation
  "non gradée"), mais `bonne_affaire_shopify.py`/`alerte_stock.py`
  n'avaient AUCUN filtre équivalent — zéro occurrence dans tout le
  système boutiques TCG avant ce fix.
- **Méga-Lucario ex 179/132 sur lesprofesseurschinent.fr** (200€,
  -32.6%) : re-scanné après le fix, toujours présent → vraie bonne
  affaire confirmée, pas un faux positif.

**Fix** : `_est_carte_gradee()` dans `bonne_affaire_shopify.py` (même
liste de mots-clés que `main.py` + négation, PLUS "ccc" qui manquait
même dans la liste d'origine de `main.py` — découvert via la 2e alerte
réelle). Même garde-fou appliqué dans `alerte_stock.py` (import croisé,
pas de duplication), pour respecter la convention "mêmes garde-fous,
même ordre" déjà établie entre les deux modules.

**Testé** : les 2 titres réels rejetés, non-régression sur les cas
bruts existants (dont la négation "non gradée"), **non-régression
réelle en relançant un scan** sur les 2 boutiques concernées
(relictcg.com : 2→0 deal, faux positifs disparus ; lesprofesseurschinent.fr :
1 deal inchangé, confirmé légitime). 4 nouveaux tests, suite complète
36/36 OK.

### Repli TCGdex automatique quand Cardtrader n'a rien (V47)

Justok a reçu une alerte 🔥 réelle sur `cardshunter.fr` (Evoli ex 167/131,
165€, "Cote : 325,28€ (-49,3%)") et a fourni une capture de la vraie page
Cardmarket montrant une tendance à ~145-150€ — écart net, garde-fou
d'avertissement déclenché à raison.

**Diagnostic** : l'alerte vient du système boutiques TCG
(`bonne_affaire_shopify.py`), qui lit `data/cotes.json` — cote calculée
par `main.py` en bas-marché eBay (3 annonces les moins chères, méthode
V43). `cardtrader.json` montrait `"prix": null` ET `"cm_id": null` pour
cette carte : le seul garde-fou censé corriger une cote eBay isolée
(vérification croisée Cardtrader, GARDE-FOU 4/5) était donc totalement
hors service pour ce cas précis — carte trop récente, pas encore
référencée côté Cardtrader. Vérifié en direct sur eBay.fr : même les 3
annonces FR non-gradées les moins chères du moment tournent ~183€ en
moyenne, donc le 325,28€ enregistré reflète un panier différent (marché
eBay qui bouge) plutôt qu'une erreur de carte.

**Solution** : réactivation de `api_prix_carte()` (TCGdex/Cardmarket,
code V21 écrit mais jamais branché depuis l'arrivée de Cardtrader en
V22 — `_api_charger_cache()`/`_api_sauver_cache()` n'étaient même pas
appelés). Sert désormais de repli INDÉPENDANT de Cardtrader quand celui-ci
ne renvoie rien (`prix_ct is None`), uniquement en mode `plus_bas` et
hors cote manuelle. Seuil de suspicion fixé à ×3 (pas ×2 comme pour la
fusion à 3 sources Cardtrader/eBay/Cardmarket) : le biais eBay documenté
en V17 (facteur 1,8-2,5×) doit pouvoir être corrigé, un seuil à ×2
l'aurait exclu du champ d'action dans le cas même qui motive ce repli.
Testé en direct : `deduire_api_id` résout correctement `sv08.5-167`
(mapping dénominateur déjà existant), TCGdex retourne 145,46€ — cohérent
avec la capture Cardmarket de Justok. Correction confirmée par simulation
complète du bloc (325,28€ -> 145,46€).

**Persistance corrigée pour le système boutiques TCG** : `data/cotes.json`
n'enregistrait jusqu'ici QUE la cote eBay brute (dans `obtenir_cote()`,
avant toute correction Cardtrader/TCGdex) — la correction restait donc
invisible pour `bonne_affaire_shopify.py`/`alerte_stock.py`, qui lisent
ce fichier tel quel sans repasser par `main.py`. Un défaut préexistant,
qui touchait aussi les corrections Cardtrader déjà en place (jamais
persistées non plus). Corrigé : la cote FINALEMENT retenue (après
correction, quelle que soit sa source) est maintenant réenregistrée dans
l'historique quand elle diffère de la cote brute, avant la sauvegarde en
fin de `main()`. Bénéficie automatiquement aux 2 systèmes sans aucune
config par carte.

**Tests** : suite complète 36/36 OK (aucun test unitaire n'existe sur
`main.py`, cf. convention documentée dans `CLAUDE.md`) + simulation
manuelle du bloc de correction avec les vraies fonctions (`cardtrader_prix`
sans token -> `None` comme en dev local, `api_prix_carte` en appel réel).

**Couverture élargie à toute la watchlist** : Justok a demandé si le repli
pouvait couvrir toutes les cartes, pas seulement Evoli ex. Test réel sur
les 82 cartes éligibles (hors KR, hors cote manuelle) de `config.yaml` :
TCGdex trouve un prix pour **71/82 (~87%)** sans aucune intervention,
`deduire_api_id()` suffisant seul. Sur les 11 échecs, 5 corrigées en
ajoutant un `api_id:` explicite (champ déjà prévu dans `config.yaml`,
prioritaire sur la déduction automatique) après recherche manuelle sur
l'API TCGdex, vérifiées par cohérence de rareté/prix avec les notes déjà
présentes dans la watchlist (ex. `Mega Darkrai ex 116` FR annoté "~250€"
confirme le match JP `me05-116`, Special Illustration Rare à 239-312€) :
- `Mega Darkrai ex 114/081` (jp) -> `me05-116`
- `Mega Darkrai ex 118/081` (jp) -> `me05-120`
- `Mega Darkrai ex 099/081` (jp) -> `me05-101`
- `Morpeko ex 115/081` (jp) -> `me05-117`
- `Evoli Trainer Gallery` (fr) -> `swsh9.5tg-TG11`

**6 cartes restent sans repli**, aucune correspondance trouvée dans
TCGdex malgré recherche par nom et par numéro local dans toute la base
(pas de devinette risquée — mieux vaut aucune cote qu'une cote sur la
mauvaise carte) : `Pikachu ex 764 mC`, `Clefairy ex 765 mC` (numéros
locaux 764/765 absents de toute la base TCGdex), `Mega Gardevoir ex
087/063` (jp, aucun set dont le total correspond au dénominateur 063),
`Lugia V 198/172`, `Lugia V 110/098` (jp, le set international déduit
`s12`→`swsh12` ne contient pas Lugia à ces numéros), `Lugia VSTAR
GG70/GG70` (fr, aucune carte "Lugia VSTAR" dans un sous-ensemble "GG"
chez TCGdex). Si l'une de ces cartes se retrouve un jour sans Cardtrader
non plus, elle n'aura simplement aucun garde-fou — comportement identique
à avant cette session (pas de régression, juste pas d'amélioration).

### 4 cartes JP supplémentaires + set S11a/S12/MC/M1S japonais exclusifs

Justok a fourni les vrais liens Cardmarket pour 4 des 6 cartes ci-dessus,
révélant les codes de set réels (`mC`/`MC` = Start Deck 100 Battle
Collection, `m1S`/`M1S` = Mega Symphonia, `s12`/`S12` = Paradigm Trigger)
— des sets **japonais exclusifs**, jamais sortis à l'international,
absents du catalogue `/en/` de TCGdex mais présents sous `/ja/`.
`api_prix_carte()` essaie désormais `/ja/` en repli quand `/en/` renvoie
404 pour une carte JP (corrige la cause racine, pas seulement ces 4
cartes). `api_id` explicite ajouté pour `Pikachu ex 764 mC` (MC-764,
856,17€), `Clefairy ex 765 mC` (MC-765, 392,73€), `Mega Gardevoir ex
087/063` (M1S-087, pas encore de prix côté TCGdex), `Lugia V 110/098`
(S12-110, idem). `Lugia V 198/172` et `Lugia VSTAR GG70/GG70` retirées
de la watchlist sur demande explicite — introuvables même par Justok.

### Couverture Cardtrader pour les 32 dernières cartes sans garde-fou

Justok a demandé "le prix le plus juste possible" et de faire le maximum.
Analyse du **vrai cache Cardtrader de production** (`data/cardtrader.json`,
généré avec le vrai token, contrairement à l'environnement local) : sur
118 cartes, 86 ont un garde-fou proactif (Cardtrader réel OU TCGdex),
32 n'en ont aucun (30 coréennes + 2 japonaises en attente de prix
TCGdex). Bonne nouvelle trouvée en creusant : les 30 coréennes ont
toutes un équivalent FR/JP suivi, donc bénéficient au moins du garde-fou
réactif "écart suspect entre langues" (V34) — plus faible qu'une
correction proactive (il alerte APRÈS qu'un possible faux positif soit
déjà parti), mais pas un filet totalement absent.

Recherche de la cause des échecs Cardtrader (via `blueprint_id` en
cache) : 14 cartes ont un blueprint trouvé mais un marché jugé trop fin
(< `min_annonces`) ; 16 n'ont même pas de blueprint. Sur ces 16, 2 vrais
bugs de mapping trouvés dans `_ct_indices_set`/`CT_SETS`/`CT_SETS_JP`,
**affectant JP et KR de façon identique** (pas un problème propre au
coréen) :
- `CT_SETS["098"]` pointait vers "Lost Origin" au lieu de "Paradigm
  Trigger" — seule carte concernée, `Lugia V 110/098`, confirmée via les
  liens Cardmarket. Corrigé.
- `CT_SETS_JP["m2"/"m3"/"m4"]` utilisaient tous le mot-clé générique
  "mega", qui ne matche que ME01 "Mega Evolution" — les vrais noms
  anglais de ME02/ME03/ME04 (confirmés via TCGdex : Phantasmal Flames/
  Perfect Order/Chaos Rising) ne contiennent pas "mega" du tout.
  Corrigé avec les bons mots-clés. Expliquait l'échec total (JP ET KR)
  pour Meowth ex, Froakie, Piplup, Mega Charizard X, Oricorio ex.

Ajouté aussi `min_annonces_kr: 1` (vs 3 par défaut) dans `config.yaml` :
le coréen est la SEULE langue sans repli TCGdex possible (Cardmarket ne
cote pas le coréen), donc la seule où Cardtrader est le dernier rempart.
Un marché coréen d'1 annonce reste moins fiable qu'un marché FR/JP de 3,
mais mieux qu'aucune vérification — les GARDE-FOU 2 (prix aberrants
écartés) et 4 (écart ×5 vs eBay) existants limitent le risque d'une
annonce isolée erronée.

**Non vérifiable en local** (pas de `CARDTRADER_TOKEN` dans cet
environnement) — impact réel à confirmer au prochain run en prod. À
revisiter dans quelques jours : combien des 16 cartes "blueprint
introuvable" sont récupérées par les 2 corrections de mapping, et
combien des 14 "marché trop fin" par `min_annonces_kr`.

### Radar de prix bas quotidien (nouveau système) + corrections m2/m3/m4

Justok a demandé un digest quotidien Telegram (11h Paris) pour 4 cartes
suivies en priorité (Plumeline ex, Carapuce, Psykokwak, + Tiplouf ajoutée
en cours de session), toutes langues (FR/JP/KR/CN) et sites confondus
(eBay/Vinted/Cardtrader/83 boutiques TCG — Leboncoin/Cardmarket/TCGplayer
explicitement exclus, cf. `CLAUDE.md`), avec alerte immédiate dès qu'un
prix passe sous la cote.

**Décision d'architecture** : les alertes "sous la cote" pour FR/JP/KR
existaient déjà (ces cartes sont dans `config.yaml` depuis longtemps) —
rien à construire. Pour le CN (langue absente jusqu'ici), ajouté comme
entrées `config.yaml` normales avec cote **manuelle** (Cardmarket/
Cardtrader ne cotent pas le chinois) : bénéficie automatiquement des
systèmes existants sans dupliquer la logique. Le nouveau code
(`watchlist_prix_bas.py` + `radar_prix_bas.py` + `prix_bas_quotidien.yml`)
ne fait QUE le digest quotidien "prix le plus bas du jour, dispo
confirmée", en réutilisant les connecteurs eBay/Vinted/boutiques
existants sans les modifier (même esprit que `radar_precommandes.py`).

**Régression en creusant les cotes CN** : en posant une cote manuelle pour
Tiplouf, Justok a fourni des captures Cardmarket réelles montrant que la
cote calculée (eBay) pour Tiplouf/Piplup était ~20x trop basse (FR 0,72€
vs 11,82€ réel ; JP 0,45€ vs 5,70€ réel). Justok a explicitement demandé
de ne PAS se contenter d'une cote manuelle et de creuser l'automatisation
— **feedback enregistré en mémoire durable** (`feedback_dig_deeper_
automate.md`) pour les sessions futures.

**Cause racine FR (Tiplouf)** : `"Tiplouf 098"` n'avait pas de
dénominateur — la vraie référence est `098/094` (confirmé TCGdex
`me02-098`, tendance 12,04€ quasi identique à la capture 11,82€). Sans
dénominateur, ni Cardtrader (`CT_SETS["094"]` déjà mappé vers Phantasmal
Flames mais jamais consulté) ni le filtre anti-confusion eBay/boutiques
ne pouvaient fonctionner. Corrigé (`config.yaml`), cote manuelle FR
retirée.

**Cause racine JP (Piplup, "m2")** : creusé plus loin, DEUX bugs trouvés
dans `main.py` :
1. `CT_SETS_JP["m2"]` avait été mappé (session précédente le jour même) à
   tort vers `"phantasmal"` (= ME02 international) par similarité de
   code — en réalité "m2" est le set **japonais exclusif** `M2 :
   インフェルノX` ("Inferno X", confirmé via `TCGdex /ja/sets`), sans
   aucun rapport avec ME02. Corrigé vers `"inferno"`. Même erreur
   suspectée et corrigée pour m3 (`ムニキスゼロ`, aucune traduction
   anglaise fiable trouvée — mot-clé `"zero"` posé à titre provisoire,
   NON vérifié) et m4 (`ニンジャスピナー` = "Ninja Spinner", confiance
   modérée). m5 (`アビスアイ` = Abyss Eye) était déjà correct, laissé
   inchangé.
2. `deduire_api_id()` ne complétait jamais un numéro JP à 3 chiffres
   (`"m2-85"` au lieu de `"m2-085"`) — vérifié en direct : 404 sans le
   padding, 200 avec. Bug latent sur tout numéro JP < 100, seul le cas
   promo SWSH avait déjà ce padding.
   Avec les 2 fix, le repli TCGdex retrouve Piplup JP à 6,14€ (confirmé
   par la capture Cardmarket, 5,70€) — **vérifié EN DIRECT avant de
   retirer la cote manuelle**, pas seulement déduit.

**Vérification étendue aux 3 autres cartes "m2"** (sur consigne de
Justok de creuser systématiquement, pas juste le cas qui a déclenché
l'alerte) :
- Oricorio ex JP (Plumeline ex) : TCGdex retrouve 51,41€ — très au-dessus
  des ~25€ estimés initialement (source PokemonPriceTracker, moins
  fiable). Justok a repéré en parallèle une vraie annonce CN à 28€ sur
  Cardmarket, confirmant que 51,41€ est la bonne tendance (Cardmarket
  affiche 52,90€/44,64€ de façon indépendante) et que 28€ est une vraie
  bonne affaire (~45% sous tendance), pas le prix normal. Cote CN
  Plumeline corrigée de 25€ à 50€.
- Squirtle JP : TCGdex retrouve 0,80€ — un MAUVAIS match (carte commune,
  pas l'alt-art recherchée). Pas corrigé activement, mais vérifié que le
  garde-fou d'écart (×3) déjà en place aurait empêché cette valeur de
  contaminer la cote réelle (23,54€ via Cardtrader) si jamais Cardtrader
  échouait un jour pour cette carte précise — limite connue du repli
  TCGdex pour ce set spécifique, à surveiller.
- Psyduck CN (17€, posée en début de session) : confirmée indépendamment
  par TCGdex (16,79€), aucun changement nécessaire.

**Tests** : 36/36 OK après chaque modification. `radar_prix_bas.py`
vérifié en simulant tout le flux de données SANS réseau (16/16 entrées
config.yaml retrouvées, 28 `CarteWatchlist` avec variantes alias, 19
critères de recherche uniques) — la partie réseau (eBay/Vinted/83
boutiques) reste **non testable en local** faute de secrets, à confirmer
au premier run réel (demain 11h Paris).

## État du programme au 2026-08-13 (référence pour la prochaine session)

**95 boutiques actives** au total (hors radar de découverte, qui démarre
à 0 et grossira automatiquement) : 44 Shopify (dont 3 en
`BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT`) + 17 PrestaShop (inchangé) +
28 WooCommerce (dont 2 en `BOUTIQUES_WOOCOMMERCE_PRECOMMANDE_SEULEMENT`).
**3 cartes JP suivies en tendance longue durée** (système séparé, cf.
`watchlist_tendance.py`). **122 cartes dans la watchlist principale**
(`config.yaml`, +4 depuis la dernière session : versions chinoises de
Plumeline ex/Carapuce/Psykokwak/Tiplouf). **4 cartes suivies en priorité
absolue** par le nouveau radar de prix bas quotidien (`watchlist_prix_
bas.py`), FR/JP/KR/CN, digest Telegram 11h Paris.

**Inventaire des fichiers** (racine du repo, par rôle) :

| Fichier | Rôle |
|---|---|
| `main.py` | Système historique eBay/Vinted/Cardtrader/Leboncoin (documenté dans `CLAUDE.md`) |
| `config.yaml` | Watchlist partagée par `main.py` ET le système boutiques TCG |
| `connecteur_shopify.py` | Connecteur Shopify + fonctions PARTAGÉES par les 3 connecteurs (`_titre_correspond`, `_slug_correspond`, `_normaliser_texte`, `_regex_numero_sans_denominateur`, `_retirer_fractions`, `_est_xml_valide`, `detecter_langue`) |
| `connecteur_prestashop_sitemap.py` | Connecteur PrestaShop (sitemap + repli recherche HTML + fix stock DOM) |
| `connecteur_woocommerce.py` | Connecteur WooCommerce (sitemap + repli recherche HTML + repli API REST) |
| `watchlist_shopify.py` | `CarteWatchlist`, parsing `config.yaml`, matching qualificatif (symétrique + faux positifs noms de coffret) |
| `bonne_affaire_shopify.py` | Alerte 🔥 bonnes affaires (garde-fous stock/gradée/langue/qualificatif) + `_est_carte_gradee()` partagée |
| `alerte_stock.py` | Alerte 📦 retour en stock (mêmes garde-fous que ci-dessus) |
| `precommandes_watchlist.py` | Watchlist + matching du radar précommandes (mots-clés + date) |
| `alerte_precommande.py` | Mémoire + alerte 🎉 du radar précommandes |
| `radar_precommandes.py` | Scanners par plateforme du radar précommandes |
| `scan_precommandes.py` | Orchestrateur CLI du radar précommandes |
| `decouverte_boutiques.py` / `watchlist_tendance.py`... voir `boutiques_decouvertes.py` | Radar de découverte automatique de boutiques (AFNIC), listes auto-gérées |
| `historique_prix.py` / `watchlist_tendance.py` | Accumulateur + signal de tendance long terme, 3 cartes JP, conversion USD→EUR |
| `telegram_utils.py` | Échappement HTML partagé par les modules d'alerte |
| `memoire_json.py` | Chargement/sauvegarde JSON partagé par plusieurs modules |
| `boutiques_shopify.py` / `boutiques_prestashop.py` / `boutiques_woocommerce.py` | Listes de boutiques actives par plateforme (+ boutiques diagnostiquées non-intégrables, documentées) |
| `scan_boutique.py` / `scan_boutique_prestashop.py` / `scan_boutique_woocommerce.py` | Orchestrateurs de scan cartes par plateforme |
| `watchlist_prix_bas.py` / `radar_prix_bas.py` | Radar de prix bas quotidien (4 cartes × 4 langues, digest Telegram 11h) |
| `tests/` | Suite pytest (36 tests), lancée sur chaque push/PR via `tests.yml` |
| `.github/workflows/{pokedeals,scan_shopify,scan_prestashop,scan_woocommerce,decouverte_boutiques,tendance_prix,prix_bas_quotidien,tests}.yml` | 8 workflows CI au total |

**État de santé par composant** (au 2026-08-13) :
- Connecteurs (Shopify/PrestaShop/WooCommerce) : sains, garde-fous cohérents (stock → gradée → langue → qualificatif), aucune duplication de logique métier restante.
- `bonne_affaire_shopify.py` / `alerte_stock.py` : sains depuis le fix cartes gradées, garde-fous identiques et alignés dans les 2.
- Radar de précommandes : actif en prod, stable.
- Radar de découverte (AFNIC) : actif, testé en conditions réelles, Telegram fonctionnel.
- Suivi de tendance (3 cartes JP) : actif, PokemonPriceTracker fonctionnel pour les 3 cartes après 3 itérations de correction, conversion USD→EUR en place. Signal de tendance pas encore significatif (moins de 14 points accumulés) — à revisiter dans ~2 semaines.
- Cotes eBay/Cardtrader/TCGdex : repli TCGdex généralisé à toute la watchlist, sets JP exclusifs (M2/M3/M4/M5, MC, M1S, S12) désormais correctement identifiés séparément des sets internationaux ME0x -- m3 confirmé le 13/08/2026 : le set s'appelle officiellement "Nihil Zero" chez Cardtrader (annonces réelles trouvées, dont Meowth ex, la carte suivie ici), mot-clé resserré de "zero" à "nihil zero" pour plus de précision.

### Vérification du mot-clé m3 "zero" (13/08/2026, en fin de session)

Recherche web ciblée sur `cardtrader.com` : le set JP m3 (« ムニキスゼロ ») est
bien référencé chez Cardtrader sous le nom **"Nihil Zero"**
(`cardtrader.com/en/games/pokemon/expansions/nihil-zero/categories`), avec
des annonces réelles listées, dont **"Meowth ex ... Nihil Zero"** —
exactement la carte JP 114 m3 suivie dans la watchlist, celle qui
déclenchait le doute initial. `CT_SETS_JP["m3"]` resserré de `["zero"]` à
`["nihil zero"]` dans `main.py` : toujours suffisant pour matcher, mais
moins de risque de faux positif qu'un mot seul. 36/36 tests toujours OK.
Le cache `data/cardtrader.json` ne se purge pas automatiquement pour ce
genre de changement (la signature de cache ne hache pas `CT_SETS_JP`),
mais l'entrée `None` existante pour Meowth ex JP expirera naturellement
au prochain cycle de retry (`CT_CACHE_ECHEC_DUREE`, 2h) — pas besoin
d'intervention manuelle.
- Radar de prix bas quotidien : code complet et testé HORS réseau (flux de données vérifié), **premier run réel pas encore eu lieu** (cron demain 11h Paris) — couverture eBay/Vinted/boutiques à confirmer.
- Sécurité : aucune fuite de secret détectée (code + historique complet). Refus explicite d'un accès GitHub direct (voir ci-dessus).
- `CLAUDE.md` : à jour, tenu synchronisé à chaque ajout de cette session.

**Prochaine session** : partir de cette section plutôt que de relire
l'historique chronologique complet, sauf besoin de détail sur un bug
précis. Points à surveiller :
- Le premier vrai signal de tendance sur les 3 cartes JP
  (`bon_moment_achat`/`prix_eleve`), une fois `MIN_POINTS_POUR_SIGNAL`
  (14) atteint (~2 semaines).
- Le premier run réel de `prix_bas_quotidien.yml` (demain 11h Paris) :
  vérifier que le digest part bien, que les 4 familles trouvent au moins
  un résultat, et que le scan (83+ boutiques) tient dans les 35 min.
- Une routine cloud programmée (`trig_014zQxygUSVJaX2yxdA2PfB5`) vérifie
  le 14/08/2026 vers 20h20 UTC combien des 32 cartes sans garde-fou de
  cette session ont récupéré un prix Cardtrader réel suite aux
  corrections de mapping.

## Session du 14/08/2026

### Bug 1 : cotes JP anormalement basses (0,44€/0,54€/0,45€) — cause racine trouvée par remontée aux logs bruts

Trois alertes "écart suspect entre langues" reçues à 00:15 (Paris) pour
Mega Charizard X ex 110 m2, Froakie 086 m4, Piplup 085 m2 (cote JP plate
et anormalement basse, cote KR normale). Diagnostic fait en remontant aux
logs GitHub Actions bruts du run concerné puis du run précédent qui avait
calculé/mémorisé ces cotes (pas de supposition, lecture ligne par ligne).

**Cause racine** : PAS Cardtrader (qui n'avait aucune annonce pour ces 3
cartes au moment du calcul initial). La cote fausse venait du repli TCGdex
`_api_recherche_par_numero()` (utilisé quand Cardtrader ne trouve rien) :
sans dénominateur dans le nom de la carte (format JP `"110 m2"`, jamais
`"110/188 m2"`), le filtre de vérification du set (`if denom and total and
...`) ne s'exécutait jamais, et la fonction acceptait le premier candidat
TCGdex renvoyé -- tous sets confondus depuis 1999. Résultat concret : une
carte "Base Set 2" anglaise de 1999 numérotée 110 par pure coïncidence a
été confondue avec la carte JP recherchée (853,83€ de vraie valeur réduite
à 0,44€). Cette cote fausse, une fois mémorisée dans `data/cotes.json`,
servait ensuite de référence au garde-fou anti-incohérence de Cardtrader,
qui rejetait alors les VRAIES annonces Cardtrader comme "incohérentes" --
une boucle auto-entretenue.

**Correctif** : `_api_recherche_par_numero()` refuse maintenant tout match
sans dénominateur dans le nom, ou si la taille officielle du set est
inconnue de TCGdex -- plutôt que de deviner. Les 3 entrées fausses de
`data/cotes.json` ont aussi été purgées manuellement (le fix de code seul
n'aurait pas empêché leur réutilisation pendant encore jusqu'à 7 jours).
Vérifié sur un run réel après fusion : les 3 cartes récupèrent leurs
vraies cotes Cardtrader (853,83€/5,53€/4,10€), plus aucune alerte
"écart suspect" pour elles. PR #1 fusionnée.

Même classe de bug que le cas Squirtle JP déjà documenté plus haut
(0,80€ via un mauvais match TCGdex) -- cette fois avec un vrai fix
générique plutôt qu'un simple constat.

### Bug 2 : aucun filtre d'état de conservation côté boutiques TCG (Neuf/NM uniquement demandé)

Alerte 🔥 reçue pour Eevee ex 223 sv8a sur kairyu.fr, "Etat : Exc"
(Excellent, pas Near Mint) alertée à tort comme bonne affaire à -32,2%.
`etats_acceptes`/`etats_refuses` existait déjà dans `config.yaml`, mais
n'était lu QUE par `main.py` (système eBay historique) -- jamais par
`bonne_affaire_shopify.py`/`alerte_stock.py`. Le connecteur Shopify ne
lisait même pas `body_html` (là où l'état est écrit) : aucune donnée
disponible pour filtrer.

**Correctif** : nouvelle fonction `detecter_etat()` dans
`connecteur_shopify.py`, ANCRÉE sur un label suivi d'un vrai séparateur
(`"Etat :"`/`"Condition :"` + `:`/`-`) -- jamais une recherche libre dans
le texte, pour ne jamais confondre "ex" (quasi tous les titres de la
watchlist) avec l'abréviation d'"Excellent". Branchée sur les 3
connecteurs, sans requête réseau supplémentaire (texte déjà récupéré).
`bonne_affaire_shopify._etat_refuse()` (liste `MOTS_ETAT_REFUSE`) rejette
un état explicitement inférieur à Near Mint/Neuf ; aucun label trouvé =
accepté (même philosophie que `main.py`). Même garde-fou dans
`alerte_stock.py`. Vérifié sur un run réel après fusion : kairyu.fr ne
remonte plus cette carte comme deal. PR #2 fusionnée.

### Nouveau : serveur MCP (`mcp_pokedeals/`) pour Claude Code

Ajout d'un serveur MCP exposant TCGdex/CardDex/Cardmarket à Claude Code,
sur demande explicite de Justok, en 3 phases : audit complet du dépôt (sans
rien modifier) présenté et validé avant d'écrire du code, implémentation,
puis tests + doc. Détails dans `mcp_pokedeals/README.md` et la nouvelle
section dédiée de `CLAUDE.md`.

Points notables :
- TCGdex intégré via appels REST directs (pas le SDK officiel
  `tcgdex-sdk`, dont le modèle d'objets Python exact n'a pas pu être
  vérifié -- accès web direct bloqué dans l'environnement de
  développement, seule la recherche web fonctionnait).
- Cardmarket : réutilisation du guide de prix officiel déjà en place dans
  `main.py` (gratuit, sans auth) ; API Marketplace (OAuth, compte
  vendeur) explicitement NON implémentée, documentée comme telle.
- CardDex : service réel confirmé (bêta publique) mais URL de base non
  vérifiable en direct -- documentée "à vérifier", corrigeable par
  variable d'env sans toucher au code.
- Bug détecté et corrigé AVANT de committer : le SDK officiel `mcp`
  (PyPI) installe sa v2 par défaut, qui renomme
  `mcp.server.fastmcp.FastMCP` en `mcp.server.mcpserver.MCPServer` --
  découvert en installant réellement le package et en l'introspectant,
  pas supposé. Le serveur a été importé avec succès et ses 6 outils
  listés (`list_tools()`) avant de committer.
- 22 nouveaux tests (mocks HTTP, aucun appel réseau réel), 45/45 tests
  existants toujours au vert (isolation confirmée). PR #3 fusionnée.

### Guide (hors dépôt) : 5 MCP Pokémon tiers pour la machine locale de Justok

Sur demande séparée, audit + test réel (clone/install/build) de 5 MCP
externes (Cardpeer, TCGdex via Pipeworx, pokemon-tcg-mcp de grzetich,
ptcg-mcp de jlgrimes, PokeClaude de briansunter) -- config donnée en
message, PAS committée dans ce dépôt (installation sur la machine locale
de l'utilisateur, sans rapport avec le code PokéDeals). A noter pour une
session future si le sujet revient :
- Cardpeer (`cardpeer.com/mcp`) : AUCUNE preuve trouvée de son existence
  en tant que serveur MCP malgré recherche web -- site marketplace réel,
  mais l'endpoint MCP n'est confirmé nulle part. Justok a choisi de
  tenter quand même, en connaissance de cause.
- `pokemon-tcg-mcp` (grzetich) : cassé tel quel (`requirements.txt`
  installe `mcp` sans version fixée -> v2, qui a supprimé
  `mcp.server.fastmcp` -- même piège que ci-dessus). Fix vérifié : forcer
  `pip install "mcp<2"`.
- `ptcg-mcp` (jlgrimes) et PokeClaude (briansunter) : clonés/testés avec
  succès, fonctionnent tels quels.

## Session du 15/08/2026 (soir) — 2 bugs CI corrigés + audit de santé complet

Déclenché par un mail d'échec `Scan PrestaShop` (12h11, job `scan`,
`ENOENT ... .git/objects/75`), puis par un signalement de l'utilisateur en
soirée ("plusieurs scans qui n'étaient pas passés"). PR #6 fusionnée
(squash), branche `claude/cardtrader-jp-prices-bug-95mb50` repartie de
`main` avant travail (l'ancienne PR #1 de cette branche était déjà
fusionnée depuis longtemps, cf. section correspondante plus haut).

### Bug 1 : sortie Python bufferisée = logs vides en cas de timeout

`Scan PrestaShop` a enchaîné plusieurs annulations pour dépassement de son
timeout de 30 min (le scan prenait ~7 min à l'origine). En allant chercher
le log complet d'un run annulé pour identifier la boutique fautive : le
log était **totalement vide** entre le lancement du script et
l'annulation, alors que `scan_boutique_prestashop.py` affiche pourtant une
ligne de progression par boutique (`print(...)`, sans `flush=True`).
Cause : hors TTY, la sortie standard Python est bufferisée par blocs — un
process tué (timeout) avant que le buffer ne se remplisse ne laisse
**aucune trace** dans le log GitHub Actions, même si le script avait déjà
affiché de la progression en mémoire.

**Correctif** : `PYTHONUNBUFFERED: "1"` ajouté à toutes les étapes
`run: python ...` des 7 workflows (pas seulement `scan_prestashop.yml`,
par cohérence — n'importe lequel des scans peut un jour se retrouver dans
la même situation).

### Bug 2 : stash orphelin après un `git stash pop` en conflit → cascade

Root cause d'un échec dur (`Scan PrestaShop`, exit 128, "Committing is not
possible because you have unmerged files") trouvée dans le log complet :

1. Étape "Sauvegarder la mémoire de stock" : conflit sur
   `stock_boutiques_tcg_prestashop.json` pendant `git stash pop` (deux
   crons parallèles avaient poussé entre-temps). Le `cp`/`add`/`commit` de
   rattrapage réimpose la version fraîchement scannée et le push passe —
   mais `git stash pop` en conflit **ne supprime jamais l'entrée du
   stash** ("kept in case you need it again").
2. Ce stash orphelin reste dans le même dossier de travail, partagé par
   toutes les étapes du job.
3. Étape suivante, "Sauvegarder la mémoire du radar précommandes" : son
   propre `git stash pop` tente de réappliquer CE MÊME stash orphelin →
   nouveau conflit sur un fichier dont cette étape ne sait rien gérer →
   `git commit` refuse (chemin non fusionné dans l'index) → job en échec.

**Correctif** : `git stash drop || true` juste après chaque
`git stash pop || true`, dans `scan_prestashop.yml` et `scan_shopify.yml`
(les 2 seuls workflows à enchaîner 2 cycles stash/pull/pop dans le même
job — les autres n'ont qu'une seule étape de sauvegarde par job, donc pas
de risque de cascade).

### Audit de santé complet (sur demande explicite, ~90 runs des dernières
heures passés en revue)

- **Scan Shopify, PokéDeals (main.py), Tendance Prix, Prix Bas Quotidien,
  Tests** : 100% verts, rien à signaler.
- **Scan WooCommerce** : 1 échec dur, même classe d'incident transitoire
  runner GitHub (`ENOENT ... .git/objects/b1`, réapparu une 3e fois dans
  la soirée sur un 3e workflow différent — reste un incident
  d'infrastructure GitHub Actions, pas de code, auto-résolu au cycle
  suivant à chaque fois) ; 3 runs annulés, tous vérifiés = le job
  `scan_lot_a` heurtant exactement son budget de 22 min, déjà documenté et
  accepté comme flake connu (cf. section "Diagnostic du flake scan_lot_a"
  plus haut) — PAS une nouvelle régression, rien touché.
- **Découverte Boutiques** : aucun run planifié depuis sa création
  (cron hebdomadaire lundi 6h UTC, prochain 17/08) — normal, pas un bug.
- Fichiers mémoire (`data/*.json`) vérifiés non corrompus malgré les
  conflits git de la soirée (écriture atomique + logique de rattrapage
  ont tenu). 51 tests unitaires au vert sur `main` après fusion.

### Cause du timeout `Scan PrestaShop` lui-même — TOUJOURS NON IDENTIFIÉE

Tentative de reproduction en environnement de dev (même script, mêmes 17
boutiques, aucun `TELEGRAM_BOT_TOKEN` donc aucune alerte réelle envoyée) :
cycle complet terminé en **2 min 33s**, aucune boutique lente. Impossible
de reproduire le ralentissement observé sur les runners GitHub Actions
depuis cet environnement — hypothèse la plus probable : une ou plusieurs
boutiques appliquent un rate-limit/anti-bot ciblant spécifiquement les
plages d'IP connues des runners GitHub (comportement réseau différent de
celui observé ici), pas un bug de code. Le correctif `PYTHONUNBUFFERED`
est le préalable nécessaire pour enfin voir, au prochain timeout réel en
prod, quelle boutique précisément bloque — pas encore observé en
conditions réelles au moment d'écrire ceci.

### Cause du timeout `Scan PrestaShop` — RÉSOLUE (16/08/2026, ~1h du matin)

Run manuel déclenché via l'API Actions (id `31917110961`) pour observer le
correctif `PYTHONUNBUFFERED` en conditions réelles sans attendre le
prochain cron. Log complet fourni par Justok (collé directement dans la
conversation) : le correctif fonctionne parfaitement, progression
boutique par boutique visible en direct, ET le correctif du stash orphelin
fonctionne aussi ("Dropped refs/stash@{0}" / "No stash entries found" —
plus de cascade de conflit).

Chronométrage exact des 17 boutiques (étape "Lancer le scan PrestaShop") :
16 boutiques entre 3s et 2min40s chacune, SAUF `lepantheon-tcg.com` (la
dernière, 17/17) : **14min34s à elle seule** (874s sur 1525.9s de durée
totale de l'étape). Dans l'étape suivante (radar précommandes), même
scénario : 16/17 boutiques traitées en un peu plus de 3 minutes, puis
blocage total sur la 17e (`lepantheon-tcg.com` à nouveau) jusqu'au timeout
du job entier (30 min).

Confirme l'hypothèse posée plus haut : le scan complet tourne en 2min33s
depuis l'environnement de dev (IP différente), donc ce n'est pas un
problème de code (`investcollect.com`, qui utilise exactement la même
méthode `rechercher_via_recherche_html` sans sitemap, reste rapide) —
`lepantheon-tcg.com` applique très probablement un rate-limit/anti-bot
ciblant spécifiquement les plages d'IP des runners GitHub Actions (Azure).

**Correctif** : `lepantheon-tcg.com` retirée de
`BOUTIQUES_PRESTASHOP_REPLI_HTML` vers une nouvelle liste documentée
`BOUTIQUES_PRESTASHOP_REPLI_HTML_TROP_LENTE` dans `boutiques_prestashop.py`
(même convention que `BOUTIQUES_PRESTASHOP_SITEMAP_CASSE` pour
`bcd-jeux.fr`) — consommée à la fois par `scan_boutique_prestashop.py` et
`scan_precommandes.py`, donc corrige les deux étapes qui timeoutaient.
Décision facilitée par la valeur déjà marginale de cette boutique (1 seul
produit unique jamais trouvé en test, 0 deal ce cycle-là). Nombre de
boutiques par défaut corrigé dans `scan_prestashop.yml` (17 → 16).

Reste à confirmer sur 2-3 cycles de prod que le retrait suffit (pas de
nouveau timeout), et à surveiller si `investcollect.com` développe un jour
le même comportement.

### Purge de 17 cotes fantômes héritées du bug du 13/08 (16/08/2026, ~3h)

Justok signale une alerte Telegram "ÉCART SUSPECT ENTRE LANGUES" reçue à
03:16 : `Oricorio ex 111 m2` coté 0,33€ en JP contre 50€ en CN (carte
suivie personnellement : "Inferno X - Oricorio ex", JP/KR/CN-T). 0,33€ est
absurde pour cette carte (valeur réelle confirmée ~50€ via Cardmarket, cf.
session du 13/08).

Root cause : `data/cotes.json` contenait encore la valeur héritée du run
BUGUÉ du 13/08 19:58:21 UTC (le tout premier bug corrigé cette session-là,
PR #1 -- `_api_recherche_par_numero()` acceptait alors n'importe quel
candidat TCGdex pour une carte SANS dénominateur dans son nom). Le fix
empêche toute NOUVELLE cote fausse d'être créée, mais ne purge jamais
rétroactivement les valeurs déjà mémorisées -- et `VALIDITE_JOURS = 7`
dans `main.py` les gardait valides jusqu'au 20/08.

En élargissant la recherche à toutes les entrées `data/cotes.json` datées
de cette même fenêtre (19:55-20:00 UTC le 13/08) pour des cartes SANS "/"
dans leur nom (donc structurellement impossibles à produire avec le code
actuel, qui refuse tout match sans dénominateur) : **17 entrées** au total
partageaient ce défaut, dont 9 cartes "ex" à des cotes ridicules (0,15€ à
1,79€ pour des Mega Darkrai ex/Mega Dracaufeu X ex/Oricorio ex/etc. --
jamais crédible pour ce type de carte) et 8 cartes de base plus ambiguës
(Bulbizarre, Ivysaur, Grenousse...) dont la valeur PARAÎT plausible mais
reste non vérifiée par la même méthode buguée -- purgées aussi par
prudence, une devinette qui tombe juste par hasard n'est pas plus fiable
qu'une devinette qui tombe faux. Vérifié : aucune entrée équivalente
apparue APRÈS le déploiement du fix (13/08 22:35 UTC) -- confirme que le
correctif tient, c'était uniquement un reliquat de l'incident initial,
jamais réapparu depuis.

Les 17 clés supprimées de `data/cotes.json` (liste complète dans le commit
git) : au prochain scan, ces cartes retomberont sur `None` ("cote
introuvable") tant qu'aucune vraie donnée eBay/Cardtrader/Cardmarket ne
sera disponible -- plus sûr qu'un chiffre inventé, même si ça veut dire
temporairement aucune alerte "bonne affaire" possible sur ces cartes
précises.

## Audit de santé complet du code (16/08/2026, ~4h)

Demande explicite de Justok : "audit entier du code... supprimer, modifier,
améliorer ou optimiser". Analyse statique (pyflakes + vulture sur tout le
dépôt) + relecture manuelle des fichiers pas encore couverts par les
sessions précédentes (connecteur_woocommerce.py, decouverte_boutiques.py,
historique_prix.py, bonne_affaire_shopify.py en entier). Codebase globalement
saine (0 `except:` nu, 0 argument par défaut mutable, 0 TODO/FIXME oublié) --
peu de trouvailles mais 2 réelles, une petite et une plus structurelle.

**Nettoyage mineur** (commit `ad781b2`) : imports inutilisés (`json` dans
`decouverte_boutiques.py`, `unicodedata as _ud` doublon dans `main.py`),
variable `pricing` calculée puis jamais utilisée (`mcp_pokedeals/providers/
tcgdex.py`), 2 f-strings sans placeholder, défaut `FICHIER_MEMOIRE` mort
dans `alerte_precommande.py` (pointait vers un fichier qui n'existe jamais
en pratique -- `scan_precommandes.py` passe toujours un chemin explicite).

**2 bugs réels trouvés et corrigés** (mêmes commit) :
1. `_ecrire_boutiques_decouvertes()` écrivait `boutiques_decouvertes.py`
   (un MODULE PYTHON importé par 3 workflows) sans écriture atomique,
   contrairement à tout le reste du projet -- un process tué en pleine
   écriture y aurait laissé un fichier tronqué, cassant l'import des 3
   workflows au lieu de juste perdre une donnée périmée. Corrigé (fichier
   `.tmp` + remplacement).
2. `collecter()` (`main.py`) : `with ThreadPoolExecutor(...) as pool:`
   appelle `shutdown(wait=True)` à la SORTIE du bloc -- avant même
   d'atteindre la boucle `.result(timeout=60)` juste après, qui attendait
   donc déjà sans limite la fin des 3 tâches (eBay/Vinted/Leboncoin). Un
   retry Vinted avec backoff peut à lui seul dépasser 90s, largement au-delà
   du timeout apparent -- risque latent de contribuer aux mêmes dépassements
   de timeout que ceux diagnostiqués ce soir côté PrestaShop, jamais
   confirmé en prod côté `main.py` mais structurellement réel. Corrigé (pool
   géré à la main + `shutdown(wait=False, cancel_futures=True)`), vérifié
   par mesure directe : avant 5.0s bloqué malgré un timeout de 1s, après
   1.2s en respectant le timeout.

**Refactor structurel** (commit `9f98b29`) : la chaîne de garde-fous
(gradée → état → langue → qualificatif symétrique) était dupliquée à la
main dans 3 fichiers (`bonne_affaire_shopify.evaluer_deal`,
`alerte_stock.detecter_retours_en_stock`, et
`radar_prix_bas._resultat_boutique_fiable`) -- exactement la duplication
que CLAUDE.md documentait déjà comme risquée ("pièges connus"), et qui a
causé 3 bugs réels distincts par le passé (garde-fou langue puis état
oubliés dans `alerte_stock.py`, chaîne entière absente de
`radar_prix_bas.py` jusqu'au 14/08/2026). Extrait dans
`garde_fous_boutique(resultat, carte) -> (ok, raison)`
(`bonne_affaire_shopify.py`), appelée par les 3 -- rend ce genre d'oubli
structurellement impossible désormais. Ne couvre pas le garde-fou stock
(sémantique différente par appelant).

Vérifié : 52/52 tests unitaires (les 3 suites qui couvrent exactement ces
scénarios inchangées, toujours au vert) + non-régression réseau réelle
(`scan_boutique.py` sur 6 boutiques Shopify actives, `radar_prix_bas.py`
sur les 83 boutiques actives -- 0 erreur dans les deux cas).

CLAUDE.md mis à jour (commit `54db2fa`) : description de
`garde_fous_boutique()`, 2 nouveaux pièges connus (ThreadPoolExecutor +
écriture non-atomique d'un `.py` généré).

## Découpage progressif de `main.py` — premier module extrait (16/08/2026)

Suite au retour ChatGPT relayé par Justok sur la dette technique de
`main.py` (alors ~3690 lignes, un seul fichier, zéro test dédié), et
après validation explicite via `AskUserQuestion` ("Découpage progressif
et prudent, un module à la fois, avec tests et non-régression à chaque
étape — PAS de réécriture en un coup") : premier module extrait.

**Module choisi (le plus sûr)** : normalisation de texte + filtre de
pertinence des annonces, centré sur `annonce_pertinente()` — aucun état
partagé, aucun appel réseau, fonctions pures. Nouveau fichier
`filtre_annonces.py` (≈470 lignes), contient : `normaliser`,
`extraire_numero`/`extraire_numero_annonce`, `numero_nu_voulu`/
`numeros_nus_titre`, `mots_requis`/`mots_requis_stricts`,
`code_set_asiatique`, `_script_asiatique`, `preuve_francais`, et
`annonce_pertinente` elle-même, plus toutes les constantes associées
(`INDICES_CARTE`, `EXCLUSIONS`, `MARQUEURS_LANGUE`, `SETS_ASIATIQUES`,
`MARQUEURS_FRANCAIS`...).

**Exclusion délibérée** : `_nom_neutre_entre_langues()` (definie juste à
côté dans l'ancien `main.py`, lignes 453-471) est RESTÉE dans `main.py`.
Raison : elle dépend de `CT_NOMS_EN`, un dictionnaire défini bien plus
loin dans `main.py` (table de correspondance FR->EN utilisée par le
moteur de cote) — une dépendance vers l'avant qui sort du périmètre
"texte pur" de ce premier module. L'extraire aussi aurait forcé soit à
déplacer `CT_NOMS_EN` (hors scope, risque plus large), soit à créer une
dépendance circulaire entre `filtre_annonces.py` et `main.py`. Gardée en
place, elle importe simplement `normaliser`/`mots_requis` du nouveau
module (résolution Python normale, aucun problème d'ordre).

`main.py` importe maintenant depuis `filtre_annonces` uniquement les 8
noms qu'il utilise réellement plus loin dans le fichier (`normaliser`,
`SUFFIXES_LANGUE`, `SIGNAUX_ENCHERE`, `extraire_numero`,
`numero_nu_voulu`, `mots_requis`, `preuve_francais`,
`annonce_pertinente`) — vérifié précisément via `pyflakes` (0
avertissement après coup, contre 17 "imported but unused" avec un import
`*` naïf qui aurait été testé d'abord). Suppression au passage de l'import
`unicodedata` devenu inutile dans `main.py` (déplacé tout entier dans
`filtre_annonces.py`). Docstring d'en-tête de `main.py` mise à jour : la
phrase "TOUT le programme est dans ce seul fichier" (vestige d'un
historique d'upload manuel très ancien, confirmé via `git log -S`, pas
une décision architecturale à préserver) a été retirée.

**Nouveau fichier de tests** `tests/test_filtre_annonces.py` (22 cas) —
première couverture de test dédiée à une fonction de `main.py`, qui
n'avait jusqu'ici aucun test. Un cas par bug réel déjà documenté en
commentaire dans le code (V15 numéro obligatoire, V17.4 numéro nu PBL,
V26 preuve positive de français, V28 code de set japonais, V30
"giapponese", V38 séparateur tiret, V39 neutralisation "non gradée"),
plus les cas structurels (Méga vs nom de set "Méga-Évolution", alias,
confirmation de langue par script asiatique). 2 cas ont nécessité une
correction du TITRE de test après premier échec (pas un bug du code) :
un titre en katakana pur sans le nom romanisé du Pokémon ne peut jamais
matcher `mots_requis` (qui compare des mots latins normalisés), et un
titre coréen sans aucun `INDICES_CARTE` latin ("carte"/"card"/"holo"...)
est rejeté dès l'étape 2 avant même d'atteindre le test de langue — les
deux comportements sont corrects, seuls mes titres de test de départ
étaient irréalistes.

Vérifié avant commit : `python3 -m ast.parse` (syntaxe), `pyflakes
main.py filtre_annonces.py` (0 avertissement), import réel de `main.py`
+ tous les modules qui en dépendent (`radar_prix_bas.py`,
`bonne_affaire_shopify.py`, `precommandes_watchlist.py`,
`alerte_stock.py`) en subprocess isolé, suite complète `pytest tests/`
(74/74, dont les 22 nouveaux) — 0 régression.

Prochain module candidat (pas commencé) : à déterminer à la prochaine
session, en gardant le même principe (petit périmètre, zéro dépendance
vers l'avant, tests dédiés avant commit).

## Deuxième module extrait de main.py : notifications_historique.py (16/08/2026)

Suite à la mise en place de la vérification photo (cf. section suivante,
faite juste avant dans la même session), et pendant que Justok demandait
"s'il y a quelque chose à finir ou améliorer, j'aimerais bien qu'on le
fasse maintenant" : deuxième extraction du découpage progressif de
`main.py`, même principe que `filtre_annonces.py`.

**Module choisi** : la couche notifications Telegram/email du système
historique -- `envoyer_telegram_texte`, `_echapper_html`, `_texte_vente`,
`envoyer_telegram_ventes`, `_echapper_url_html`, `_ligne_verification_photo`,
`_texte_telegram`, `envoyer_telegram`, `_html_deal`, `envoyer_alertes`
(lignes 2153-2399 de l'ancien `main.py`). Choisi car entièrement autonome :
aucune dépendance vers l'avant dans `main.py` (vérifié via `grep` sur
chaque nom, comme pour la première extraction), aucun état partagé, ne
manipule que des dicts `deal`/`vente` passés en paramètre. Seule
dépendance externe : `verification_photo.verifier_photo_annonce` (déjà un
module séparé). Nouveau fichier `notifications_historique.py` (~275
lignes), avec son propre logger dédié (`pokedeals.notifications_historique`,
même convention que `verification_photo.py`) plutôt que le logger racine
`pokedeals` partagé par le reste de `main.py`.

`main.py` ne réimporte que les 4 fonctions publiques réellement utilisées
ailleurs (`envoyer_telegram_texte`, `envoyer_telegram_ventes`,
`envoyer_telegram`, `envoyer_alertes`) -- vérifié via `grep` que rien
d'autre n'était appelé après la fin du bloc (une seule mention de
`_texte_telegram` restante, dans un COMMENTAIRE, pas du code). Imports
`smtplib`/`MIMEMultipart`/`MIMEText` retirés de `main.py` (plus utilisés
sur place, déménagés avec le bloc) ; `imaplib`/`email as email_lib`
restent (utilisés ailleurs, par `lbc_relever_alertes_email` pour LIRE les
emails Leboncoin -- fonction différente de l'envoi SMTP).

**Test touché par l'extraction** : `tests/test_main_verification_photo.py`
(ajouté un peu plus tôt dans la session, testait `main._texte_telegram`/
`main.envoyer_telegram` avec des patches sur `main.verifier_photo_annonce`/
`main.requests.post`) a été supprimé et remplacé par
`tests/test_notifications_historique.py`, qui importe directement depuis
le nouveau module et patch `notifications_historique.verifier_photo_annonce`/
`notifications_historique.requests.post` -- les patches `unittest.mock`
ciblent le namespace où le code s'exécute réellement, qui a changé avec
le déménagement. Même raisonnement déjà appliqué à
`bonne_affaire_shopify.py`/`alerte_stock.py` pour `garde_fous_boutique()`.

**Résultat** : `main.py` passe sous les 3000 lignes (2999, contre ~3690
avant le début du découpage). Prochains candidats identifiés mais non
extraits (notés dans CLAUDE.md pour la prochaine session) : le connecteur
Cardtrader (le plus gros bloc restant, ~565 lignes, mais `CT_NOMS_EN` y
est défini et utilisé par `_nom_neutre_entre_langues()` resté dans
`main.py` -- nécessiterait un import retour, à traiter avec soin comme
pour `_nom_neutre_entre_langues`/`filtre_annonces.py`), le connecteur
TCGdex, le connecteur Leboncoin.

Vérifié avant commit : `pyflakes` propre sur `main.py` et
`notifications_historique.py`, import réel de `main.py` +
`bonne_affaire_shopify.py`/`alerte_stock.py`/`radar_prix_bas.py`/
`precommandes_watchlist.py`/`notifications_historique.py` en subprocess
isolé, appel direct de `envoyer_telegram_texte` (chat_id vide -> `False`
proprement, aucune exception), suite complète `pytest tests/` (95/95, le
compte total est resté identique car les tests ont été déplacés 1:1 vers
le nouveau fichier, pas dupliqués).

## Étude de faisabilité + implémentation : vérification photo des annonces (16/08/2026)

Suite au retour ChatGPT relayé par Justok ("pas d'analyse photo" cité comme
lacune), étude de faisabilité menée avant tout code (cf. réponse détaillée
donnée à l'utilisateur dans la conversation). Conclusion : viable et peu
coûteux, mais volontairement restreint à UNE seule vérification — la photo
montre-t-elle bien le bon Pokémon dans la bonne langue ? — et pas
l'authenticité ni la condition/le centrage, qu'une IA de vision généraliste
ne peut pas juger de façon fiable sur une photo de petite annonce.

**Motivation concrète** : cas déjà documenté en commentaire V37 dans
`main.py` — une annonce Vinted titrée entièrement en français pointait en
réalité vers une carte CORÉENNE sur la photo, aucun filtre texte ne
pouvant le détecter. Jusqu'ici, seule protection : un avertissement
générique envoyé quand la décote dépasse 30%.

**Validé par Justok puis étendu** : approbation initiale pour le système
eBay/Vinted (`main.py`) uniquement ; en cours d'implémentation, Justok a
demandé d'étendre aussi aux boutiques TCG (Shopify/PrestaShop/WooCommerce,
`bonne_affaire_shopify.py`), qui ont elles aussi de bonnes photos
disponibles via leurs connecteurs existants (`ResultatRecherche.image_url`,
déjà extrait par les 3 connecteurs). Leboncoin reste hors périmètre (pas
d'URL de photo exploitable via son système d'alertes email) ; les autres
systèmes indépendants (précommandes, tendance de prix, prix bas
quotidien) ne sont pas concernés.

**Implémentation** :
- Nouveau module `verification_photo.py` : `verifier_photo_annonce(image_url,
  nom_carte, langue, api_key) -> (verdict, raison)`. Appelle l'API Anthropic
  Messages directement en `requests` (pas de SDK `anthropic`, pour rester
  fidèle à la convention "requests + PyYAML seules dépendances de PROD"),
  modèle `claude-haiku-4-5-20251001` (le moins cher, suffisant pour ce
  classement grossier). Réponse attendue au format strict
  `COHERENT`/`INCOHERENT: raison`/`INCERTAIN: raison`, parsée par
  `_interpreter_reponse()` -- toute réponse hors format OU "INCERTAIN" est
  traitée comme NON CONCLUANTE (`None`), jamais comme une confirmation ni un
  rejet implicite. Ne lève jamais d'exception : secret absent, image
  inaccessible, timeout, erreur API -> `(None, raison)` systématiquement.
- `main.py` : `ebay_rechercher()`/`vinted_rechercher()` capturent maintenant
  `image_url` (absent auparavant, vérifié en lisant le code avant de coder --
  aucun champ image n'était extrait des réponses API alors que eBay Browse
  API et Vinted le fournissent). `evaluate()` transporte `image_url`/`langue`
  automatiquement (spread `{**annonce, ...}`, aucun changement nécessaire
  côté `evaluate()` lui-même). `envoyer_telegram()` prend un paramètre
  optionnel `anthropic_api_key` : si fourni ET `image_url` présent sur le
  deal, appelle la vérification juste avant l'envoi (donc uniquement sur les
  quelques deals déjà filtrés par TOUTE la chaîne de règles existante,
  jamais sur le flux brut). Résultat ajouté en ligne supplémentaire dans le
  message Telegram (`_ligne_verification_photo()`), en complément de
  l'avertissement générique décote≥30% existant (V37), jamais en
  remplacement. Secret `ANTHROPIC_API_KEY` ajouté à `secrets_env()`
  (optionnel, comme `GMAIL_APP_PASSWORD`).
- `bonne_affaire_shopify.py` : `evaluer_deal()` transporte désormais
  `image_url` (déjà présent sur `ResultatRecherche`, jamais recopié dans le
  dict `deal` jusqu'ici) et `langue` (depuis `carte.langue`) dans les deux
  branches (seuil fixe et cote normale). `_texte_bonne_affaire()` et
  `envoyer_telegram_bonnes_affaires()` reçoivent le même traitement que côté
  `main.py` (paramètre optionnel, ligne ajoutée, jamais bloquant).
  `scan_boutique.py`/`scan_boutique_prestashop.py`/`scan_boutique_woocommerce.py`
  lisent `ANTHROPIC_API_KEY` depuis l'environnement et le passent à
  `envoyer_telegram_bonnes_affaires()`.
- Workflows : `ANTHROPIC_API_KEY` ajouté (optionnel) aux étapes de SCAN
  CARTES uniquement (`pokedeals.yml`, `scan_shopify.yml`,
  `scan_prestashop.yml`, `scan_woocommerce.yml` lots A et B) -- PAS aux
  étapes de radar précommandes, qui n'utilisent pas ce mécanisme.

**Tests** : 3 nouveaux fichiers/extensions —
`tests/test_verification_photo.py` (9 cas : pas de clé -> 0 appel réseau,
pas d'image -> 0 appel réseau, les 3 verdicts bien parsés, image
inaccessible/erreur API ne plantent jamais), `tests/test_main_verification_photo.py`
(7 cas côté `main.py`, dont la vérification que `envoyer_telegram()`
n'appelle la vérification QUE si clé + image présentes, avec les bons
arguments), et extension de `tests/test_bonne_affaire_shopify.py` (5 cas
équivalents côté boutiques TCG). Tous mockent `requests.get`/`requests.post`
-- aucun appel réseau réel dans la suite de tests.

Vérifié avant commit : `pyflakes` propre sur tous les fichiers touchés,
import réel de `main.py`/`bonne_affaire_shopify.py`/`alerte_stock.py`/
`radar_prix_bas.py` en subprocess isolé, suite complète `pytest tests/`
(95/95), et un run RÉEL de `scan_boutique.py` sur 2 boutiques actives
(`dracaugames.com`, `cardlabtcg.com`) pour vérifier que la nouvelle
plomberie (`image_url`/`langue` sur les deals) ne casse rien en conditions
réelles -- 0 erreur, 3.3s. `ANTHROPIC_API_KEY` n'étant pas configuré dans
cet environnement, le nouveau code de vérification lui-même n'a été validé
qu'en tests unitaires mockés (pas encore de vérification en conditions
réelles avec un vrai appel API -- à surveiller au premier cycle de prod une
fois le secret configuré par Justok).

**Mise à jour** : Justok a configuré le secret `ANTHROPIC_API_KEY` peu
après. Vérification en conditions réelles faite en 2 temps : (1) un run
manuel de `scan_shopify.yml` (2 boutiques) a confirmé que le secret est
bien chargé par le workflow (`ANTHROPIC_API_KEY: ***` dans les logs),
mais 0 deal détecté ce coup-ci donc aucun appel réel à l'API n'a été
exercé ; (2) ajout d'un petit outil de test permanent (`verification_photo.py`,
bloc `__main__`, même convention que `alerte_stock.py`) + workflow dédié
`test_verification_photo.yml` (workflow_dispatch uniquement, lecture
seule) pour tester manuellement avec une vraie image sans attendre un
deal réel. Testé avec une vraie photo Charizard/Dracaufeu Base Set
anglais (`https://images.pokemontcg.io/base1/4.png`) : verdict `coherent`
en 1,3s, confirmant que l'appel API fonctionne bout en bout.

## Diagnostic + fix du flake scan_lot_a WooCommerce, round 2 (16/08/2026)

En vérifiant l'état général du projet (Justok : "s'il y a quelque chose à
finir ou améliorer, j'aimerais bien qu'on le fasse maintenant"), un run
`Scan WooCommerce` annulé a été repéré dans l'historique GitHub Actions
récent. Investigation demandée par Justok AVANT tout correctif (même
protocole que le diagnostic du 11/08/2026, référencé dans CLAUDE.md :
"ne pas ajuster à l'aveugle").

**Données collectées** (logs bruts de plusieurs runs récents, timestamps
ligne par ligne) :
- 4 runs annulés sur les 20 derniers (20%), tous après 17h -- 0 annulation
  le matin (10h-16h46). Le timeout de `scan_lot_a` (22 min, déjà remonté
  une fois le 11/08) a de nouveau été atteint pile (22m13s) sur un run.
  Un autre run a vu `scan_precommandes` (25 min de budget) dépasser à
  25m17s. Comme les jobs sont séquentiels (`needs:`), une annulation de
  `scan_lot_a` fait sauter `scan_lot_b` ET `scan_precommandes` derrière.
- Durée de `scan_lot_a` mesurée sur plusieurs runs du même jour : 12m00s
  (10h12) -> 17m22s (16h56) -> 18m34s (17h27) -> **22m13s, ANNULÉ** (20h05).
- Détail boutique par boutique (logs `[i/13] boutique : OK`, calcul des
  écarts entre timestamps consécutifs) :
  - `cardshunter.fr` : stable, ~4m25-4m30s à chaque run.
  - `hamacards.com` : TRÈS variable -- 6m00s dans un run, 9m57s dans un
    autre (même jour, quelques heures d'écart).
  - `mymesis.fr` (repli API REST, 13e/13e boutique du lot) : normalement
    rapide (42s-1min), mais dans le run annulé de 20h05, encore en cours
    d'exécution après 7+ minutes SANS AVOIR FINI quand le job a été tué --
    un vrai blocage, pas juste une lenteur (contrairement aux runs où il
    finit toujours, même lentement).
  - Les 10 autres boutiques du lot : rapides et stables (~4-5 min pour
    toutes ensemble).

**Diagnostic** : pas une dérive progressive de la taille des catalogues
(hypothèse initiale, jamais confirmée faute d'accès réseau direct au
sandbox pour comparer les tailles de sitemap -- proxy sandbox bloquant
les domaines de boutiques, cf. `curl $HTTPS_PROXY/__agentproxy/status`).
Le vrai signal : `cardshunter.fr` + `hamacards.com` consomment déjà
~10-14 min à eux deux (marge déjà tendue, cf. diagnostic du 11/08), ET
`mymesis.fr` peut en plus se bloquer complètement via son repli API REST
(`rechercher_via_api_rest`, `connecteur_woocommerce.py`) : cette fonction
interroge l'API une fois par nom de carte UNIQUE (~100+ noms dans la
watchlist), chacun avec un timeout de 15s, SANS AUCUNE protection contre
une série d'échecs consécutifs -- si l'API distante ralentit/rate-limite
en cours de cycle, le pire cas théorique est `100 × 15s` ≈ 25 minutes,
largement suffisant pour expliquer le blocage observé.

**Décision de Justok** : les deux corrections combinées (pas l'une ou
l'autre) :

1. **Déplacement** : `mymesis.fr` retirée de `LOT_A` et ajoutée à `LOT_B`
   (`boutiques_woocommerce.py`) -- LOT_B a une marge bien plus large
   (4-8 min mesurés pour un budget de 18 min), donc mieux placée pour
   absorber un pic ponctuel de `mymesis.fr`. Changement d'une ligne, même
   principe que le déplacement de `lepantheon-tcg.com` plus tôt dans la
   session. N'affecte PAS le radar de précommandes : `mymesis.fr` y est
   déjà scannée dans l'étape "lot B + API REST" (`scan_woocommerce.yml`),
   indépendamment de son appartenance à `LOT_A`/`LOT_B` pour le scan
   cartes.

2. **Coupe-circuit** : nouveau paramètre `SEUIL_ECHECS_CONSECUTIFS_API_REST = 3`
   sur `ConnecteurWooCommerce`. `_decouvrir_produits_api_rest()` renvoie
   désormais `(produits, ok)` au lieu de juste `produits` -- `ok=False`
   distingue un ÉCHEC (timeout/erreur réseau) d'une recherche réussie qui
   ne renvoie simplement aucun produit (ne jamais confondre les deux,
   même philosophie que les autres garde-fous du projet : ne pas
   sur-réagir à une absence de résultat légitime). `rechercher_via_api_rest()`
   compte les échecs CONSÉCUTIFS (un succès réinitialise le compteur) et,
   au-delà du seuil, arrête d'interroger l'API pour le reste du cycle sur
   cette boutique -- les noms restants reçoivent une liste vide sans appel
   réseau, avec un message imprimé pour visibilité dans les logs.
   Un autre appelant de `_decouvrir_produits_api_rest()` existait
   (`radar_precommandes.py`, `scanner_woocommerce_api_rest`) et a été mis
   à jour pour déballer le nouveau tuple (pas de coupe-circuit ajouté là :
   hors périmètre de ce fix, logique d'appel différente).

**Tests** : nouveau fichier `tests/test_connecteur_woocommerce.py` (6 cas) --
succès renvoie `ok=True`, timeout renvoie `ok=False`, le coupe-circuit
s'arrête pile au 3e échec CONSÉCUTIF, un succès au milieu d'une série
d'échecs réinitialise le compteur (jamais de faux déclenchement sur des
échecs non consécutifs), aucun impact si tout réussit, un nom déjà vu
n'est jamais interrogé deux fois. Tous mockent `_decouvrir_produits_api_rest`
directement (pas de vrai appel réseau).

Vérifié avant commit : `pyflakes` propre sur les 3 fichiers touchés
(`connecteur_woocommerce.py`, `boutiques_woocommerce.py`,
`radar_precommandes.py`), suite complète `pytest tests/` (101/101), ET
un run RÉEL (`scan_boutique_woocommerce.py mymesis.fr cardshunter.fr`)
qui a déclenché le coupe-circuit en conditions réelles dans le sandbox
(3 échecs consécutifs détectés et log imprimé, `cardshunter.fr` scanné
normalement dans la foulée) -- confirmation que le mécanisme fonctionne
de bout en bout, pas seulement en tests mockés.

## Rejet manuel définitif d'un candidat du radar de découverte (17/08/2026)

Justok a reçu l'alerte Telegram "Radar de découverte" signalant `nemee-tcg.fr`
comme candidat ambigu (verdict `"insuffisant"`, cf. `verifier_candidat()`),
vérifié le catalogue de son côté et demandé sa suppression définitive --
il ne veut pas de cette boutique sur PokéDeals.

**Problème** : le radar (`decouverte_boutiques.py`) mémorise définitivement
les verdicts `"singles"`/`"scelle"` (ajoutés) et `"non_boutique"` (aucune
plateforme détectée), mais PAS `"insuffisant"` (candidat ambigu) --
décision délibérée pour ne pas rater une boutique dont le catalogue
grossit (cas déjà documenté : `nemee-tcg.fr` avait 1 seul produit le
12/08/2026). Sans mécanisme dédié, un rejet humain explicite aurait été
silencieusement ignoré, et la boutique serait revenue dans un futur
rapport tant qu'elle reste dans la fenêtre de 7 jours des fichiers AFNIC.

**Fix** : nouveau `DOMAINES_REJETES_MANUELLEMENT` (set curé à la main,
même principe que `NOMS_SET_QUALIFICATIF_AMBIGU`/`MOTS_CARTE_GRADEE`
ailleurs dans le projet) dans `decouverte_boutiques.py`, avec
`nemee-tcg.fr` comme premier domaine. `main()` synchronise ce set dans
`memoire["domaines_verifies"]` à CHAQUE cycle (verdict
`"rejete_manuellement"`), avant de calculer `domaines_deja_vus` -- donc
même si le fichier mémoire est un jour recréé/vidé, le rejet reste
permanent tant que le domaine reste dans la liste curée. Contrairement
à `"insuffisant"`, ce verdict N'EST PAS un simple manque de signal
temporaire : c'est une décision humaine délibérée, jamais remise en
cause (même principe que la confiance à 100% sur les identifications de
cartes données par Justok).

Pour un effet immédiat (sans attendre le prochain cron hebdomadaire du
lundi), `data/decouverte_boutiques_memoire.json` a aussi été mis à jour
directement (écriture atomique, même pattern que partout ailleurs dans
le projet) avec l'entrée `nemee-tcg.fr -> {"verdict": "rejete_manuellement"}`.

Vérifié : `pyflakes` propre, simulation de la logique de filtrage en
Python direct (confirmé que `nemee-tcg.fr` est bien exclu de la liste de
candidats après synchronisation), suite complète `pytest tests/`
inchangée (101/101, ce fix ne touche pas de fonction couverte par des
tests dédiés -- `main()` de `decouverte_boutiques.py` n'est pas testé
unitairement, comme les autres orchestrateurs du projet).

## Retour sur le bilan ChatGPT : alerte de fiabilité Vinted/Leboncoin (17/08/2026)

Justok a demandé un rappel des points restants de l'avis ChatGPT relayé la
veille, puis validé (via un choix multiple) de traiter les deux éléments
encore ouverts : cette alerte de fiabilité, et la poursuite du découpage
de `main.py`. Consigne explicite : "fais en sorte que tout soit fini et
fonctionne à la perfection [...] du moment que tu peux te corriger et ne
pas créer de bug."

**Problème visé** : si Vinted ou Leboncoin change son API/son mécanisme
de cookies du jour au lendemain, `vinted_rechercher()`/`lbc_rechercher()`
avalent déjà l'exception et renvoient `[]` (comportement voulu, pour ne
jamais faire planter un cycle sur une plateforme en panne) -- mais rien
ne distinguait "0 résultat légitime pour cette carte" de "la plateforme
entière ne répond plus", donc une casse totale et durable pouvait passer
inaperçue pendant des jours.

**Choix d'implémentation** : plutôt que de changer la signature de
`vinted_rechercher()`/`lbc_rechercher()` (aurait fallu mettre à jour
`radar_prix_bas.py`, seul autre appelant de `vinted_rechercher`, et créer
un risque de régression pour un gain marginal), compteurs module-level
`_stats_fiabilite` (`{plateforme}_appels`/`{plateforme}_echecs`),
incrémentés directement dans les blocs `try`/`except` existants des deux
fonctions -- zéro changement de signature, zéro appelant à toucher.
Remis à zéro en tout début de `main()` (`_reinitialiser_stats_fiabilite()`)
: chaque cycle cron repart d'un compteur propre.

Point d'attention explicite : le blocage 403/429 de Leboncoin (déjà
documenté dans le code comme un comportement anti-bot ROUTINE, pas une
panne) est volontairement EXCLU du comptage d'échecs -- seul le bloc
`except Exception` générique (erreur réseau/timeout/format inattendu)
compte. Sans cette distinction, l'alerte se serait déclenchée en continu
puisque Leboncoin bloque fréquemment par conception.

`verifier_fiabilite_plateformes(vues)`, appelée une fois en fin de
`main()` (même emplacement que `detecter_anomalies`/
`verifier_cotes_manuelles_perimees`) : alerte si le taux d'échec dépasse
80% (`SEUIL_TAUX_ECHEC_FIABILITE`) sur au moins 5 appels
(`SEUIL_MIN_APPELS_FIABILITE`, pour ne pas conclure sur un tout petit
échantillon). Anti-spam 6h (`DELAI_ANTI_SPAM_FIABILITE`, réutilise
`anti_spam()` déjà existant) -- sans ça, `pokedeals.yml` tournant toutes
les 15 min aurait ré-envoyé la même alerte en boucle tant que le
problème persiste.

**Tests** : nouveau `tests/test_fiabilite_plateformes.py` (9 cas) --
aucune alerte sous le seuil minimum d'appels (même à 100% d'échec),
aucune alerte à taux normal, alerte correcte par plateforme et pour les
deux à la fois, anti-spam empêchant bien une répétition immédiate,
réinitialisation des compteurs, et surtout : vérification que
`vinted_rechercher()` compte bien un vrai échec (session indisponible)
et que `lbc_rechercher()` NE compte PAS un 403 comme un échec (mock de
`_get_vinted_session`/`requete_avec_retry` via `monkeypatch`).

Vérifié avant commit : `pyflakes` propre sur `main.py`, suite complète
`pytest tests/` (110/110).

## Troisième module extrait de main.py : connecteur_cardtrader.py (17/08/2026)

Suite directe de la section précédente (même session, même consigne de
Justok : "fais en sorte que tout soit fini et fonctionne à la perfection
[...] du moment que tu peux te corriger et ne pas créer de bug"). Module
le plus gros et le plus couplé identifié pour le découpage progressif de
`main.py` (~565 lignes), déjà signalé dans CLAUDE.md comme nécessitant
un import retour pour `CT_NOMS_EN`.

**Incident évité en cours de route** : première tentative d'extraction
faite avec des numéros de ligne PÉRIMÉS (calculés avant l'édit de
`_ecrire_json_atomique`, qui a décalé tout le fichier de plusieurs
lignes) -- le `sed`/slicing Python a coupé le bloc au mauvais endroit,
tronquant une partie du banner de commentaire Cardmarket qui suit. Détecté
immédiatement par une vérification de diff systématique (comparaison
ligne à ligne du bloc extrait contre l'original avant de toucher
`main.py`) plutôt que de faire confiance aveuglément au résultat. Comme
`main.py` n'était pas encore committé à ce stade, correction simple :
`git checkout -- main.py` pour repartir de zéro, puis re-extraction avec
des numéros de ligne fraîchement recalculés APRÈS l'édit préalable. Cet
incident renforce la leçon déjà tirée plus tôt dans le projet (piège
"écriture non-atomique") : ne jamais faire confiance à un numéro de ligne
sans le revérifier juste avant de s'en servir, surtout après une édition
précédente du même fichier dans la même session.

**Deux points de couplage réels, gérés explicitement (pas juste
constatés)** :
1. `CT_NOMS_EN` (table FR->EN) est utilisée par `_nom_neutre_entre_langues()`,
   restée dans `main.py` -- déjà anticipé, réimportée normalement
   (`from connecteur_cardtrader import CT_NOMS_EN`), aucun souci : ce
   dict n'est jamais réassigné après sa définition, seulement lu.
2. **Piège NON anticipé initialement, trouvé en cartographiant les
   dépendances avant d'écrire le moindre code** : `_ct_cache` (dict de
   cache blueprints/prix) EST réassigné par `_ct_charger_cache()`
   (`global _ct_cache; _ct_cache = {...}`), pas seulement muté par
   `.update()`/`.setdefault()`. Un `from connecteur_cardtrader import
   _ct_cache` dans `main.py` aurait figé la liaison sur l'objet
   dict EXISTANT AU MOMENT DE L'IMPORT -- une réassignation ultérieure
   dans `connecteur_cardtrader.py` ne serait JAMAIS vue par `main.py`,
   qui aurait continué à lire un cache figé/périmé indéfiniment après le
   premier chargement. Seul `cardmarket_prix()` (reste dans `main.py`,
   a besoin de `_ct_trouver_blueprint`/`_ct_cache` pour retrouver le
   `cardmarket_id` déjà résolu par Cardtrader) était concerné. Corrigé
   par un accès QUALIFIÉ (`import connecteur_cardtrader` puis
   `connecteur_cardtrader._ct_cache["blueprints"]...`), qui lit toujours
   l'attribut COURANT du module, jamais une copie figée. Vérifié
   explicitement par un test dédié (`test_ct_cache_reassignation_visible_via_acces_qualifie`)
   ET par une simulation manuelle (réassignation directe de
   `connecteur_cardtrader._ct_cache`, confirmation que l'accès qualifié
   voit bien le nouvel objet).

**Extraction annexe** : `_ecrire_json_atomique()` (écriture JSON atomique
générique, jusqu'ici dupliquée nulle part mais utilisée SEULEMENT par
`main.py`) déplacée dans un nouveau `json_utils.py`, car
`connecteur_cardtrader.py` en a aussi besoin (`_ct_sauver_cache()`) --
sans ce partage, `connecteur_cardtrader.py` aurait dû soit dupliquer la
fonction, soit importer depuis `main.py` (créant un import circulaire
réel : `main.py` importe `connecteur_cardtrader`, qui aurait importé
`main.py`). `main.py` continue à appeler `_ecrire_json_atomique(...)`
sous son nom historique partout (6 autres call sites inchangés) via un
alias d'import (`from json_utils import ecrire_json_atomique as
_ecrire_json_atomique`).

**Réimporté dans `main.py`** (10 noms, le plus gros nombre de tous les
modules extraits jusqu'ici -- reflète le couplage réel de ce connecteur
avec l'orchestration) : `CT_NOMS_EN`, `_ct_charger_cache`,
`_ct_sauver_cache`, `_ct_trouver_blueprint`, `_ct_incoherent_entre_langues`,
`_ct_memoriser_prix`, `_calibration_ajouter`, `_calibration_coefficient`,
`_calibration_paires`, `_ct_cfg`, `cardtrader_prix` -- plus l'import du
module entier (`import connecteur_cardtrader`) pour l'accès qualifié à
`_ct_cache`. `hashlib`/`inspect` retirés des imports de `main.py` (plus
utilisés sur place, déménagés avec `_ct_signature_code()`).

**Résultat** : `main.py` passe sous les 2530 lignes (2527, contre ~3690
avant le début du découpage -- plus de 1150 lignes déplacées vers des
modules dédiés en 3 extractions). Candidats restants : le connecteur
TCGdex, le connecteur Leboncoin.

**Tests** : nouveau `tests/test_connecteur_cardtrader.py` (15 cas) --
extraction de numéro de carte (3 formats différents, dont le piège
slug/ID déjà documenté), déduction de set par dénominateur ET par code
JP, cohérence de prix entre langues, calibration (rapports absurdes
ignorés, coefficient sous le minimum), robustesse de la signature de
cache, et le test dédié au piège de réassignation de `_ct_cache`
ci-dessus.

Vérifié avant commit : diff ligne à ligne du bloc extrait contre
l'original AVANT toute modification de `main.py` (0 différence hors le
renommage volontaire `_ecrire_json_atomique` -> `ecrire_json_atomique`),
`pyflakes` propre sur tous les fichiers touchés, import réel de tous les
modules dépendants en subprocess isolé, suite complète `pytest tests/`
(125/125), et un test fonctionnel réel en conditions de production :
chargement du VRAI fichier `data/cardtrader.json` (122 blueprints/122
prix en cache), calcul réel d'un coefficient de calibration, et appel de
`cardmarket_prix()` avec un token vide -- échec réseau (proxy sandbox)
géré proprement, `None` retourné sans exception, comme le code le
garantit explicitement pour ce cas ("échec réseau : pas bloquant").
Aucun fichier `data/*.json` modifié par ces vérifications (lecture
seule, `_ct_sauver_cache()` jamais appelée).

## Quatrième module extrait de main.py : connecteur_tcgdex.py (17/08/2026)

Suite directe (même session, même consigne de Justok de continuer "dans
l'ordre qui te parait le plus judicieux"). Extraction beaucoup plus
simple que `connecteur_cardtrader.py` : aucun couplage particulier avec
`main.py` (aucun dict réassigné, aucune dépendance vers l'avant) --
seulement 3 fonctions publiques réutilisées ailleurs
(`_api_charger_cache`, `_api_sauver_cache`, `api_prix_carte`, toutes
appelées depuis `main()`).

Leçon du module précédent appliquée cette fois : les numéros de ligne
ont été revérifiés (`grep -n "^TCGDEX_BASE = \|^VINTED_BASE = "`) juste
avant l'extraction du bloc de `main.py`, sans réutiliser un numéro
calculé plus tôt dans la conversation -- même incident que la fois
précédente évité d'entrée de jeu.

**Réimporté dans `main.py`** (3 noms seulement) : `_api_charger_cache`,
`_api_sauver_cache`, `api_prix_carte`. Aucun accès qualifié nécessaire
(pas de dict réassigné comme `_ct_cache` chez Cardtrader).

**Résultat** : `main.py` passe sous les 2320 lignes (2319, contre ~3690
avant le début du découpage -- 4 modules extraits, plus de 1350 lignes
déplacées). Candidat restant : le connecteur Leboncoin.

**Tests** : nouveau `tests/test_connecteur_tcgdex.py` (12 cas) --
déduction d'identifiant pour chaque piège déjà documenté en commentaire
(V47 : padding à 3 chiffres obligatoire, coréen toujours exclu, série
151 FR, code de set JP avec ET sans dénominateur, promos SWSH/SV,
absence totale d'indice = pas de match), lecture de prix (repli sur les
champs disponibles), et confirmation qu'une carte coréenne ne déclenche
aucun appel réseau.

Vérifié avant commit : diff ligne à ligne du bloc extrait contre
l'original AVANT toute modification de `main.py` (0 différence hors le
renommage volontaire déjà utilisé pour Cardtrader), `pyflakes` propre,
import réel de tous les modules dépendants en subprocess isolé, appel
réel de `_api_charger_cache()` (95 entrées chargées depuis le vrai
`data/api_prix.json`), suite complète `pytest tests/` (137/137).

## Cinquième et sixième modules extraits de main.py : http_utils.py, stats_fiabilite.py, connecteur_leboncoin.py (17/08/2026)

Suite directe (même session, mandat "on continue" de Justok). Ce module
était le premier du découpage à ne PAS former un bloc contigu dans
`main.py` : `lbc_rechercher`/`LBC_API`/`LBC_HEADERS` d'un côté (lignes
944-1000), `lbc_extraire_annonces_email`/`lbc_relever_alertes_email`/
`_html_vers_texte`/`_prix_depuis_texte`/`RE_LBC_LIEN`/`RE_LBC_PRIX` de
l'autre (lignes 1063-1184), séparés par le moteur de cote/historique
(`_charger_historique`, `sauvegarder_historique`, `historique()`) qui
n'a AUCUNE dépendance avec l'un ou l'autre bloc et reste dans `main.py`.
Recollés en un seul fichier `connecteur_leboncoin.py`.

**Deux dépendances auraient créé un import circulaire** si laissées
dans `main.py` (qui aurait dû importer `connecteur_leboncoin`, qui
aurait dû importer en retour depuis `main.py`) :
- `requete_avec_retry`/`user_agent`/`USER_AGENTS` : utilisées par
  `lbc_rechercher`, mais AUSSI par `ebay_rechercher`/`vinted_rechercher`/
  `vinted_description`, qui restent dans `main.py`. Extraites dans un
  nouveau module `http_utils.py` (bloc pur, sans état partagé, déjà
  repéré comme candidat naturel plus tôt dans la session) ; `main.py`
  les réimporte comme il le fait déjà pour `ecrire_json_atomique`
  (`json_utils.py`).
- `_stats_fiabilite` (dict de compteurs V50) : incrémenté à la fois par
  `vinted_rechercher()` (resté dans `main.py`) et `lbc_rechercher()`
  (migré). Extrait dans un nouveau module `stats_fiabilite.py`, minimal
  (juste le dict). Point vérifié avant d'écrire le code (même démarche
  que pour `_ct_cache` chez Cardtrader) : `_stats_fiabilite` n'est
  JAMAIS réassigné en bloc dans `main.py`, seulement muté clé par clé
  (`_stats_fiabilite[cle] = 0` dans `_reinitialiser_stats_fiabilite()`,
  `+= 1` dans les connecteurs) -- donc un simple
  `from stats_fiabilite import _stats_fiabilite` dans les deux modules
  suffit, PAS besoin d'accès qualifié comme `connecteur_cardtrader._ct_cache`.
  Vérifié explicitement par un test d'intégration (mutation via
  `main._stats_fiabilite`, lecture via `connecteur_leboncoin._stats_fiabilite`,
  même objet dict).

**Réimporté dans `main.py`** : `lbc_rechercher`, `lbc_relever_alertes_email`
(les 2 seuls noms Leboncoin utilisés ailleurs dans `main.py`, dans
`collecter()` et `main()`) ; `user_agent`, `requete_avec_retry` (pas
`USER_AGENTS`, jamais référencé directement ailleurs dans `main.py` --
repéré par `pyflakes` comme import inutile puis retiré) ; `_stats_fiabilite`.

Ancien banner de commentaire "LEBONCOIN VIA ALERTES EMAIL (V11)" (qui
expliquait le choix du repli email face au blocage DataDome) retiré de
`main.py` et absorbé dans le docstring de `connecteur_leboncoin.py` --
même traitement que les banners Cardtrader/TCGdex précédents.

Deux imports devenus inutiles dans `main.py` après le départ de
`lbc_relever_alertes_email` (seul consommateur) : `imaplib`, `email as
email_lib` -- retirés (repérés par `pyflakes`).

**Résultat** : `main.py` passe de 2319 à 2105 lignes (-214, dont le
retrait du banner de commentaire) -- 6 modules extraits au total depuis
le 16/08/2026, main.py réduit d'environ 3690 à 2105 lignes.

**Tests** : nouveaux `tests/test_connecteur_leboncoin.py` (12 cas --
blocage 403/429 jamais compté comme échec de fiabilité, vraie panne
réseau comptée, parsing de la réponse API, gestion des espaces
insécables dans un prix, extraction/dédoublonnage/rejet d'annonces
depuis un HTML d'email, `lbc_relever_alertes_email` ne fait aucun appel
IMAP si désactivé ou sans mot de passe) et `tests/test_http_utils.py` (4
cas -- retry sur 429, propagation d'erreur après épuisement des
tentatives). Un test PRÉEXISTANT (`tests/test_fiabilite_plateformes.py::
test_lbc_rechercher_403_nest_pas_compte_comme_un_echec`) a dû être
corrigé : il monkeypatchait `main.requete_avec_retry`, qui n'a plus
aucun effet sur le code réellement exécuté par `lbc_rechercher()`
(désormais dans `connecteur_leboncoin.py`, avec sa propre référence
importée) -- corrigé pour patcher `connecteur_leboncoin.requete_avec_retry`,
avec un commentaire expliquant pourquoi ce n'est plus équivalent depuis
l'extraction.

Vérifié avant commit : diff ligne à ligne des DEUX blocs extraits contre
l'original, chacun contre une extraction `sed` fraîche du fichier
`main.py` juste avant l'édition (0 différence sur les deux, en dehors
des imports/en-tête du nouveau module) ; `pyflakes` propre sur les 4
fichiers touchés (`main.py`, `connecteur_leboncoin.py`, `http_utils.py`,
`stats_fiabilite.py`) ; import réel de tous les modules en subprocess
isolé, avec vérification explicite que les objets réimportés dans
`main.py` sont bien les MÊMES objets que ceux de `connecteur_leboncoin.py`
(`is`, pas juste `==`) ; test fonctionnel réel de
`lbc_extraire_annonces_email()` sur un HTML d'exemple ; suite complète
`pytest tests/` (152/152, après correction du test préexistant).

## Septième module extrait de main.py : moteur_cote.py (17/08/2026)

Suite directe (même session, l'utilisateur a explicitement demandé de
s'attaquer au moteur de cote/évaluation SI c'est fait "minutieusement et
vérifié derrière", "le plus propre possible, bénéfique aussi bien pour le
code que pour l'utilisateur" — après que ce module ait été identifié
comme le seul candidat restant, mais jugé "trop central/risqué pour une
extraction casuelle"). Extraction la plus étendue et la plus rigoureuse du
découpage à ce jour, à la hauteur du risque :

**Portée** : `calculer_cote()` (calcul du prix de référence -- médiane
eBay nettoyée des valeurs aberrantes IQR, ou moyenne du bas de marché
selon `cfg.cote.methode`), `_localisation_incoherente()` (V18, garde-fou
langue/pays), le suivi d'ancienneté des annonces (V44 : `anciennete()`,
`jours_en_ligne()`, sert à exclure du panier bas-marché une annonce qui
traîne sans se vendre), la persistance de l'historique des cotes
(`historique()`, `sauvegarder_historique()`, purge par `PURGE_VERSION`),
`cle_cote()`/`cote_lissee()`/`enregistrer_cote()`/`obtenir_cote()` (choix
de la cote : manuelle > lissée > instantanée), `_etat_ok()` (V36, gère
les négations "non gradée"), `evaluate()` (décision DEAL/pas-DEAL, tous
les garde-fous : seuil fixe V45, prix d'appel suspect V22.8, port V40/V41,
profit minimum...) et `calculer_tendance_cote()` (flèche hausse/baisse
pour le CSV).

**Quatre blocs non contigus recollés** (contre deux pour
`connecteur_leboncoin.py`) : le suivi d'ancienneté (entre le "vues"/dédup
et le fetch eBay), `_localisation_incoherente`+`calculer_cote` (entre le
fetch eBay et les cotes Cardmarket/TCGdex), l'historique+`evaluate` (entre
le fetch Vinted et les notifications), et `calculer_tendance_cote` (entre
les stats et l'export CSV) -- chacun laissé à sa place originale sauf
extraction, avec un commentaire pointant vers `moteur_cote.py` là où un
lecteur pourrait chercher la fonction disparue (ex. dans la section CSV,
juste avant `_proteger_csv`).

**`detecter_anomalies()`/`verifier_cotes_manuelles_perimees()` restent
dans `main.py`** bien qu'elles lisent `historique()` : ce sont des
générateurs d'ALERTES Telegram couplés à `anti_spam()`/`vues` (état du
système de dédup, hors périmètre du moteur de cote), même logique que
`verifier_fiabilite_plateformes()` restée en place lors de l'extraction
de `_stats_fiabilite`.

**Deux dépendances évitant un import circulaire, déjà réglées lors de
l'extraction précédente** : `annonce_pertinente`/`normaliser`/
`SIGNAUX_ENCHERE` (déjà dans `filtre_annonces.py`) et
`ecrire_json_atomique` (déjà dans `json_utils.py`) -- aucun nouveau
module de support nécessaire cette fois, contrairement à Leboncoin
(`http_utils.py`/`stats_fiabilite.py`).

**Aucun état mutable partagé réassigné en bloc** : `_historique` et
`_anciennete` (dicts de cache) sont mutés via leurs accesseurs
`historique()`/`anciennete()`, jamais réassignés depuis l'extérieur --
`main.py` ne réimporte que des FONCTIONS, jamais ces variables
directement, donc pas de piège de liaison figée comme `_ct_cache`.

**Nettoyage des imports devenus inutiles** dans `main.py`, repéré par
`pyflakes` : `SIGNAUX_ENCHERE` (n'était utilisée que dans `evaluate()`,
migrée), `calculer_cote` et `cle_cote` (jamais appelées directement par
`main.py` -- seulement via `obtenir_cote()`/`cote_lissee()`/
`enregistrer_cote()`/`calculer_tendance_cote()`, qui restent le seul
point d'entrée public utilisé).

**Méthode d'extraction adaptée à l'ampleur du risque** : après un faux
départ (édition par index de ligne Python, deux fois en erreur d'un
cran -- confusion entre "numéro de ligne fichier" et "position dans la
liste 0-indexée", cf. leçon déjà notée pour Cardtrader), la refonte a été
reconstruite par CONCATÉNATION DE SEGMENTS `sed` (extraits par numéro de
ligne vérifié juste avant usage) plutôt que par des slices Python
calculées à la main -- élimine complètement le risque d'erreur d'indice.
Chaque segment inchangé a été extrait individuellement puis recollé avec
les blocs de remplacement (imports), la version finale relue diff par
diff contre l'ancienne pour confirmer que SEUL le contenu voulu avait
changé (renommages `_ecrire_json_atomique` -> `ecrire_json_atomique`,
suppression des redéfinitions locales de `RACINE`, et les 4 blocs
d'import). Un excès ponctuel de lignes vides aux points de jonction
(sous-produit mécanique de la concaténation) a été identifié et corrigé
à la main avant de valider le fichier final.

**Vérification différentielle (au-delà du protocole habituel)** : en plus
du diff ligne à ligne des 4 blocs extraits contre l'original, un script
de comparaison a fait tourner CÔTE À CÔTE l'ancien `main.py` (sauvegardé
avant modification, importé sous un nom distinct) et le nouveau
(`main.py` + `moteur_cote.py`) sur 1200 cas générés pour `calculer_cote()`
(annonces aléatoires, langues FR/JP, méthode médiane/bas-marché) et 2000
cas pour `evaluate()` (prix/port/cote/confiance/marge/état/plateforme/
seuil fixe aléatoires, couvrant tous les chemins de rejet documentés) :
**0 différence** de résultat entre ancien et nouveau code sur l'ensemble
des 3200 comparaisons. C'est la vérification la plus forte appliquée à
ce jour dans le découpage, proportionnée au fait que ce module n'avait
JAMAIS eu de test dédié avant aujourd'hui (contrairement aux connecteurs,
qui avaient déjà des tests de non-régression).

**Tests** : nouveau `tests/test_moteur_cote.py` (50 cas) -- un cas par
comportement documenté par un commentaire `VNN` dans le code (V15 numéro
exact, V16 langue, V17 médiane, V18 localisation, V20 diagnostic, V22.8
prix d'appel suspect, V23 méthode bas-marché, V26 clés par langue, V36
négations d'état, V39 `etats_acceptes` décoratif, V40/V41 plafond de port
basé sur la cote, V44 exclusion des annonces stagnantes, V45 seuil de
prix fixe), plus la persistance de l'historique (purge par version,
chargement/sauvegarde réels via `tmp_path`, jamais sur `data/cotes.json`)
et `obtenir_cote()` (priorité manuelle > instantanée > lissée > absente).
Isolation systématique de `_historique`/`_anciennete` du disque réel via
une fixture `autouse` (jamais de lecture/écriture sur les fichiers de
production pendant les tests).

Vérifié avant commit : diff ligne à ligne des 4 blocs extraits contre
l'original (0 différence hors renommages/redéfinitions RACINE attendus),
comparaison différentielle ancien/nouveau (3200 cas, 0 différence, cf.
ci-dessus), `pyflakes` propre sur l'ensemble du dépôt (`main.py` et tous
les modules touchés, imports inutiles retirés), import réel avec
vérification d'identité d'objet (`is`, pas `==`) entre les fonctions
réimportées dans `main.py` et celles de `moteur_cote.py`, chargement réel
des fichiers de production (`data/cotes.json` : 94 clés, `data/
anciennete_annonces.json` : 380 entrées) et appel réel de `obtenir_cote()`
sur une carte de la watchlist (repli correct sur la cote mémorisée),
suite complète `pytest tests/` (202/202). `main.py` passe de 2105 à 1663
lignes (~3690 lignes au tout début du découpage, 16/08/2026 -- sept
modules extraits, plus de 2000 lignes déplacées).

## Audit des marges de timeout des 8 workflows + revue des pièges connus (17/08/2026)

Demandé par Justok après l'extraction de `moteur_cote.py` : vérifier si des
marges de timeout sont devenues trop justes, et repasser sur les pièges
connus pour un cas non couvert. Délégué à un agent en arrière-plan pour la
collecte de données (beaucoup d'appels API GitHub), puis **vérifié
manuellement avant d'agir** — l'agent avait mal daté ses observations
(comparé des échecs anciens à un correctif récent sans vérifier l'horodatage
du commit vs celui des runs), ce qui aurait mené à une fausse alerte si pris
tel quel.

**Ce qui a été confirmé sain sans changement** : `pokedeals.yml` (15 min de
budget, 4.7-6.0 min réels, marge très large), `scan_prestashop.yml` (30 min
de budget, 13.2-15.7 min réels), `scan_woocommerce.yml` → `scan_lot_b` et
`scan_precommandes` (18/25 min de budget, 5-10 min réels),
`decouverte_boutiques.yml`/`tendance_prix.yml` (quelques secondes contre
10-20 min de budget). Les 14 pièges documentés dans `CLAUDE.md` ont tous été
revérifiés par recherche dans le code (grep ciblé) — tous intacts, aucune
régression, y compris dans les modules extraits aujourd'hui même
(`moteur_cote.py`, `connecteur_leboncoin.py`, `http_utils.py`,
`stats_fiabilite.py`, qui référencent d'ailleurs eux-mêmes certains de ces
pièges dans leurs propres commentaires).

**Fausse alerte écartée après vérification** : l'agent a signalé
`scan_lot_a` (WooCommerce) comme "le fix du 16/08 ne tient pas" en trouvant
6 annulations sur 30 runs récents (~20%). Vérification manuelle : le commit
du fix (`3ec8bb4`, déplacement de `mymesis.fr` vers `LOT_B` + coupe-circuit
API REST) a en réalité été poussé le **17/08 à 06h53:46 UTC** — PAS "le
16/08" comme son propre message de commit le disait (erreur d'horodatage
dans le commit lui-même, à noter pour éviter de la reproduire). Or les 6
annulations trouvées par l'agent datent TOUTES d'avant ce commit (la
dernière à 06h30, soit 23 minutes avant le fix). Log du run annulé de
06h30 lu en détail : `mymesis.fr` était bien encore listé en 13e boutique
de LOT_A (confirmant qu'il tournait sur l'ancien code), bloqué de 06h43:49
jusqu'à l'annulation à 06h52:46 (9+ min sans jamais finir) — exactement le
symptôme déjà diagnostiqué et censé être corrigé. Les 2 cycles complets
observés APRÈS le fix (08h26 et 09h06) sont tous les deux propres :
`scan_lot_a` en 13m26s-13m36s (contre 22 min de budget, ~38-39% de marge,
sain), `scan_lot_b` en 4m51s-5m19s, `scan_precommandes` en 9m14s (le
premier cycle) et en cours mais sans signe de lenteur pour le second. Le
fix tient bel et bien — l'agent avait juste mélangé des données d'avant et
d'après le correctif sans vérifier l'horodatage du commit. Commentaire du
job `scan_lot_a` dans `scan_woocommerce.yml` mis à jour pour documenter
cette reconfirmation (et éviter qu'un futur diagnostic reparte de zéro en
voyant les vieilles annulations dans l'historique GitHub Actions).

**Deux marges resserrées par prudence** (aucun échec réel constaté sur ces
deux workflows à ce jour, mais marge jugée insuffisante pour absorber un
ralentissement ponctuel, cf. le surcoût réseau GitHub Actions de +19 à
+38% déjà documenté ailleurs) :
- `scan_shopify.yml` : 10 runs consécutifs mesurés à 16.2-19.9 min contre
  un budget de 25 min (marge tombée à ~20%, alors que le commentaire du
  fichier datait encore d'une mesure locale à 6.3 min, très en dessous de
  la réalité de prod) → budget remonté à **30 min**.
- `prix_bas_quotidien.yml` : seulement 3 cycles depuis son activation
  (peu de recul), mais le pire des trois a consommé 30.6 min sur un
  budget de 35 min (~87%, ~12.6% de marge) → budget remonté à **40 min**.

Aucun changement de logique Python dans cette passe — uniquement 3 valeurs
`timeout-minutes` et leurs commentaires explicatifs, dans
`scan_shopify.yml`, `prix_bas_quotidien.yml` et `scan_woocommerce.yml`
(ce dernier pour documenter la reconfirmation, sans changer sa valeur).
Vérifié : les 3 fichiers YAML restent syntaxiquement valides
(`yaml.safe_load`).

## V51 : reformule l'alerte "photo INCOHÉRENTE" après un faux positif réel (17/08/2026)

Signalé par Justok : une alerte 🔥 pour Méga-Dracaufeu X ex 125/094 (eBay,
700€ + 2,78€ de port, cote 916,67€, **+305,56€ de profit net estimé**)
affichait "🚨 Vérification IA : photo INCOHÉRENTE (La carte montre
Méga-Dracaufeu Y (version bleue), pas Méga-Dracaufeu X...)" — alors que la
photo montrait bien la bonne carte (confirmé par Justok, dont
l'identification de carte fait foi par convention, cf. CLAUDE.md). Faux
positif du modèle de vision (Claude Haiku) sur une distinction visuelle
fine (variantes Méga X/Y), pas un bug de code : l'image était correctement
téléchargée et transmise, le prompt correctement formé.

**Pas de correctif déterministe possible** côté prompt/modèle (limite déjà
documentée dans `verification_photo.py` : "qu'une IA de vision généraliste
ne peut pas juger de façon fiable"). La vérification reste volontairement
NON BLOQUANTE depuis sa conception précisément pour ce genre de cas —
l'alerte 🔥 est bien partie malgré le faux "INCOHÉRENTE". Le vrai problème
trouvé : le message affichait ce verdict comme un FAIT confirmé
("INCOHÉRENTE" en majuscules, ton alarmiste), risquant de faire fuir un
vrai deal (+305€) sur un faux positif, alors que le système est censé
n'ajouter qu'un signal informatif imparfait.

**Correctif** : reformulation du message dans les deux points d'affichage
(`notifications_historique._ligne_verification_photo()` et
`bonne_affaire_shopify._ligne_verification_photo()`, copies dupliquées
identiques -- candidates à factoriser un jour, pas fait ici pour rester
scopé au bug signalé) — le verdict "incohérent" est maintenant présenté
en minuscules ("photo semble incohérente") avec une phrase explicite
"cette vérification automatique peut se tromper (ex. variantes
visuellement proches), regarde toi-même la photo avant de décider !".
Aucun changement de logique (le verdict "coherent"/"incoherent"/None et
le comportement non-bloquant sont inchangés), uniquement le TEXTE affiché
à l'utilisateur — pour recalibrer la confiance sans perdre le signal
(souvent utile, cf. cas réel documenté dans `verification_photo.py` :
annonce Vinted en français pointant vers une carte coréenne).

Tests mis à jour (`tests/test_notifications_historique.py`,
`tests/test_bonne_affaire_shopify.py`) : les 3 assertions qui vérifiaient
la présence de "INCOHÉRENTE" (majuscules) vérifient maintenant
"incohérente" + "peut se tromper". Suite complète : 202/202.

## Audit externe par deux IA concurrentes (DeepSeek + ChatGPT), 17/08/2026

Demandé par Justok : audit indépendant du projet par deux IA rivales, avec
un prompt structuré (lecture README/CLAUDE.md/SESSION_NOTES.md/tests,
priorité correction/sécurité/fiabilité/couverture de tests/architecture/
documentation). Chaque retour a été **vérifié contre le code réel avant
toute action** — les deux audits contiennent des erreurs factuelles
qu'il aurait été dangereux de suivre aveuglément.

**Faux/inexacts, écartés après vérification** :
- DeepSeek affirmait `main.py` à 389 lignes (`wc -l` confirme 1663).
- DeepSeek affirmait qu'aucun test ne couvre l'IQR/la méthode bas-marché/
  les annonces stagnantes/la localisation incohérente/la cote lissée dans
  `calculer_cote()` — faux, les 5 comportements ont chacun un test dédié
  dans `tests/test_moteur_cote.py` (noms quasi identiques à ceux que
  DeepSeek proposait d'ajouter, signe qu'il n'a probablement pas
  réellement lu ce fichier de test).
- ChatGPT affirmait que le port était "caché" sur les deals à seuil fixe
  (`prix_max_fixe`) — faux, le message Telegram affiche systématiquement
  "prix + port = total" sur toute alerte, seuil fixe inclus (vérifié dans
  `notifications_historique.py` et `moteur_cote.py`).

**Vrais, corrigés dans cette passe** :

1. **`pokedeals.yml` faisait `cp data/*.json`** (repéré par ChatGPT, le
   point le plus sérieux des deux audits). Confirmé en lisant le
   workflow : il sauvegardait/restaurait TOUS les fichiers JSON de
   `data/`, y compris ceux appartenant aux 3 autres workflows (stock
   boutiques, précommandes, découverte, tendance) qui tournent en
   parallèle sur le même dépôt. Scénario concret : un `scan_shopify.yml`
   pousse une mise à jour de `data/stock_boutiques_tcg.json` PENDANT que
   `pokedeals.yml` tourne ; `git pull --rebase` la récupère correctement,
   mais le `cp /tmp/*.json data/` qui suit l'écrasait aussitôt par la
   version périmée capturée avant le pull — pas une corruption de fichier
   (l'écriture atomique reste intacte), mais une mise à jour silencieusement
   annulée, avec un risque concret d'alerte de retour en stock dupliquée
   au cycle suivant. **Corrigé** : le backup/restore ne porte plus que sur
   les 7 JSON + 1 CSV réellement possédés par `main.py` (lui-même +
   `moteur_cote.py` + `connecteur_cardtrader.py` + `connecteur_tcgdex.py`) :
   `seen.json`, `cotes.json`, `anciennete_annonces.json`, `stats.json`,
   `cardtrader.json`, `api_prix.json`, `cardmarket_prix.json`,
   `deals.csv`. Testé manuellement en bash (simulation d'un fichier d'un
   autre workflow mis à jour "pendant" le run : reste intact après le
   nouveau code, contre écrasé avant).

2. **`requete_avec_retry` ne retentait que sur 429**, jamais sur 5xx/408
   (DeepSeek) — confirmé dans `http_utils.py`. Un 503 ponctuel d'eBay/
   Vinted/Cardtrader (fréquent sur API publiques) faisait échouer le
   cycle pour cette carte/boutique sans nouvelle tentative. Étendu aux
   codes 408 et ≥500 ; les vrais 4xx (401/403/404...) restent retournés
   immédiatement (pas de retry sur une erreur qui ne se corrige pas en
   réessayant).

3. **`verification_photo.py` téléchargeait une image sans valider
   l'URL** ni limiter sa taille (DeepSeek) — confirmé : `image_url` vient
   d'annonces tierces (eBay/Vinted/boutiques), rien n'empêchait de faire
   télécharger par le runner GitHub Actions une URL pointant vers une
   ressource interne (ex. service de métadonnées cloud à
   169.254.169.254) ni de plafonner la taille téléchargée. **Corrigé** :
   nouvelle fonction `_url_photo_autorisee()` (schéma http/https
   obligatoire + résolution DNS de l'hôte rejetée si IP privée/loopback/
   link-local/réservée/multicast), et téléchargement en streaming avec
   plafond `TAILLE_IMAGE_MAX` (10 Mo). Limite connue et documentée en
   commentaire : un DNS rebinding pourrait en théorie contourner le
   contrôle (résolution différente entre notre vérification et l'appel
   `requests.get()` réel) -- jugé disproportionné à mitiger entièrement
   ici (runner GitHub Actions éphémère, pas de secret sensible exposé
   localement au-delà de l'environnement du job).

4. **`README.md` affichait encore "au moins 30% sous la cote"** alors que
   `config.yaml` est à 10% (`marge_achat: 0.10`) — contradiction
   introduite par moi-même lors de la réécriture du README plus tôt dans
   la session (j'avais bien écrit ailleurs dans le même fichier "les
   valeurs actuelles dans config.yaml font foi", mais laissé un chiffre
   en dur juste au-dessus). Corrigé pour renvoyer vers `config.yaml`
   plutôt que dupliquer un chiffre qui se désynchronise.

5. **`echapper_url_html` (`telegram_utils.py`) n'échappait que `&`**, pas
   `<`/`>` (DeepSeek, mineur) — aligné sur `echapper_html`. Une copie
   dupliquée du même nom existait aussi dans `notifications_historique.py`
   (jamais migrée vers `telegram_utils.py` lors de la factorisation du
   11/08/2026, avec son propre commentaire justifiant explicitement de
   NE PAS échapper `<`/`>` -- rationale qui ne tenait pas à l'examen,
   ces caractères n'étant jamais valides dans une vraie URL) : alignée
   par cohérence.

6. **`detecter_bonnes_affaires()` (orchestrateur qui filtre par
   confiance et dédoublonne) n'avait aucun test dédié** (DeepSeek) —
   confirmé : seul `evaluer_deal()` (le garde-fou par garde-fou) était
   testé, pas la boucle qui l'appelle. 6 nouveaux tests ajoutés (cas
   nominal, confiance faible ignorée, carte sans numéro ignorée, critère
   orphelin ignoré, déduplication du même produit trouvé via nom+alias,
   non-déduplication de deux produits réellement différents).

**Signalés comme réels mais non prioritaires** (mentionnés à Justok,
pas d'action immédiate) :
- `LIMITE_CANDIDATS_PAR_CRITERE` (15, dans `connecteur_prestashop_sitemap.py`
  et `connecteur_woocommerce.py`) peut en théorie créer un faux négatif
  si un critère SANS numéro matche >15 URLs -- mais déjà largement
  mitigé par la convention du projet (numéro obligatoire dans la
  watchlist depuis V15, déjà documentée comme piège connu dans
  `CLAUDE.md`).
- Absence de tests d'intégration bout-en-bout pour `main()`/`collecter()`
  -- limitation déjà connue et assumée (`CLAUDE.md` le dit explicitement :
  "ce qui reste dans main.py... demeure peu testé directement").
- La cote reste basée sur des prix EBAY DEMANDÉS, pas des prix de vente
  réels -- limite structurelle déjà identifiée et discutée avec Justok
  dans une session précédente (compromis assumé, pas actionnable
  facilement : pas d'API de volume de ventes gratuite disponible).

**Vérification avant commit** : suite complète `pytest tests/`
(219/219, +15 tests nouveaux : 4 sur `requete_avec_retry`, 6 sur
`_url_photo_autorisee`/taille max, 6 sur `detecter_bonnes_affaires`,
moins les 1 test existant remplacé), `pyflakes` propre sur tout le
dépôt, `pokedeals.yml` validé par `yaml.safe_load` ET par une simulation
bash locale du scénario de collision (fichier d'un autre workflow
confirmé intact après le nouveau code, altéré par l'ancien), résolution
DNS réelle testée en direct pour `_url_photo_autorisee` (google.com
autorisé, localhost/127.0.0.1/169.254.169.254/file:// refusés).

## Boutique jamais enregistrée (gmcardsandtoys.com) + fausses alertes 📦 sur échec réseau total (18/08/2026)

Deux sujets distincts remontés/creusés le même jour.

**1. Précommande manquée, signalée par Justok.** Une précommande du
Coffret ETB 30e Anniversaire vue le 18/08/2026 sur `gmcardsandtoys.com`
(`/fr-fr/collections/chiques/PRECO`) n'a jamais alerté. Diagnostic :
la boutique n'était enregistrée **nulle part** dans PokéDeals — ni
listes manuelles, ni mémoire de découverte auto. Cause racine :
`decouverte_boutiques.py` ne couvre que les nouveaux domaines `.fr`
(listes AFNIC) ; `gmcardsandtoys.com` est en `.com`, structurellement
invisible pour ce mécanisme quelle que soit sa date de création — pas
un bug de la logique d'alerte. Corrigé (PR #11, mergée) : ajout à
`BOUTIQUES_SHOPIFY_PRECOMMANDE_SEULEMENT` (confirmé par Justok :
scellé uniquement ; le produit lui-même était déjà dans
`PRODUITS_SURVEILLES`). Plateforme déduite du motif d'URL
(`/collections/<handle>`, préfixe `/fr-fr/` typique de Shopify
Markets) — PAS vérifiée via `/products.json` (réseau sortant bloqué
vers ce domaine dans l'environnement de dev) ; à confirmer au premier
vrai cycle `scan_shopify.yml`.

**2. Audit "zéro bug" demandé par Justok, en parallèle.** En vérifiant
un signalement d'un des deux audits IA concurrents (cf. entrée du
17/08/2026) sur le thème "un échec réseau peut-il produire une fausse
alerte de retour en stock ?", confirmé un vrai bug **dans les 3
connecteurs boutiques** (`connecteur_shopify.py`,
`connecteur_prestashop_sitemap.py`, `connecteur_woocommerce.py`) :

- `recuperer_tout_le_catalogue()` (Shopify) : un échec de la toute
  PREMIÈRE page `/products.json` (réseau, timeout, JSON invalide)
  renvoyait un catalogue vide **sans lever d'exception** — indiscernable
  d'une boutique dont aucun produit ne matche la watchlist ce cycle.
- `recuperer_toutes_les_urls_produits()` (PrestaShop/WooCommerce) : même
  défaut si aucun sitemap racine n'est trouvé, ou si tous échouent à se
  charger.

Conséquence réelle tracée dans le code : `scanner_boutique_complet()`
(chacun des 3 `scan_boutique*.py`) passe ce catalogue vide tel quel à
`alerte_stock.detecter_retours_en_stock()`, qui enregistre alors
`en_stock: False` pour **chaque** carte suivie sur cette boutique (la
mémoire est mise à jour à chaque cycle, en_stock ou non). Dès que le
réseau se rétablit, si le produit est réellement en stock, la
transition `False -> True` déclenche une **fausse** alerte 📦. Pire :
ce cycle en échec n'apparaissait même pas dans `boutiques_echec` (le
mécanisme de résilience déjà prévu par `scanner_plusieurs_boutiques`,
avec son `try/except` par boutique) puisqu'aucune exception ne
remontait jamais — un vrai échec réseau se présentait dans les logs
comme "OK — 0 deal(s), 0 retour(s) en stock", impossible à distinguer
d'un cycle normal sans correspondance.

Corrigé en levant une `RuntimeError` uniquement sur l'échec TOTAL de
la première étape de récupération (page 1 Shopify ; aucune URL sitemap
du tout, avant filtre des segments exclus, pour PrestaShop/WooCommerce)
— une page suivante en échec après un catalogue partiel déjà récupéré
reste tolérée (pas fatale), et un résultat vide **après** filtre des
segments exclus (boutique fraîchement enregistrée, sitemap encore
quasi vide) reste traité comme légitime, pas comme une erreur. La
`RuntimeError` remonte jusqu'au `try/except` déjà existant de
`scanner_plusieurs_boutiques` (identique dans les 3 orchestrateurs),
qui la journalise proprement dans `boutiques_echec` et **saute** la
boutique pour ce cycle — sans jamais toucher `memoire_stock` pour elle,
donc plus de fausse transition rupture→stock.

11 nouveaux tests (`test_connecteur_shopify.py`,
`test_connecteur_woocommerce.py`, et un nouveau
`test_connecteur_prestashop_sitemap.py` — première couverture dédiée à
ce connecteur, jusqu'ici à 0 test comme documenté dans `CLAUDE.md`) :
lève bien sur échec total, ne lève PAS sur catalogue page-1 réellement
vide, ne lève PAS sur un résultat vide seulement après filtrage des
segments exclus, tolère un échec de pagination après un premier
succès (Shopify).

**Limite assumée** : non-régression "sur l'ensemble des boutiques
actives" (convention habituelle du projet pour tout changement de
connecteur partagé) non réalisable depuis cette session — le réseau
sortant de cet environnement de développement est bloqué vers la
plupart des domaines externes (constaté en tentant de vérifier
gmcardsandtoys.com ci-dessus). Le changement ne modifie AUCUN chemin de
succès (mêmes valeurs de retour qu'avant sur un scan normal) — seul le
chemin d'échec total change de comportement (lève au lieu de renvoyer
`[]`), donc le risque de régression sur un scan sain est jugé
négligeable, mais à surveiller sur les premiers vrais cycles en prod
(`boutiques_echec` devrait désormais faire apparaître les échecs réseau
qui étaient auparavant invisibles).

**Vérification avant commit** : suite complète `pytest tests/`
(230/230, +11 tests nouveaux).

## Suite de l'audit maximal (18/08/2026) : accent manqué + cote_min bloquait Tiplouf

Deux points supplémentaires trouvés en poursuivant l'audit du même jour.

**1. `_est_carte_gradee()` (`bonne_affaire_shopify.py`) ratait "Gradée"
accentué.** Simple `.lower()` sans retrait d'accent — "Gradée" (orthographe
FR naturelle sur une fiche produit) ne matchait jamais "gradee" (seule
forme dans `MOTS_CARTE_GRADEE`), contrairement à `config.yaml ->
etats_refuses` qui liste déjà les deux formes pour ce même mot côté
système eBay/Vinted historique. Corrigé en réutilisant
`_normaliser_texte()` (`connecteur_shopify.py`) au lieu du `.lower()` nu
— retire aussi les accents des négations (`NEGATIONS_GRADATION`). 4
nouveaux tests, première couverture dédiée à cette fonction.

**2. `cote_min` (15€, regles globales) bloquait silencieusement TOUTE
alerte sur Tiplouf.** En vérifiant `data/cotes.json` : cote réelle
13,89-19,3€ (FR), ~4,10€ (JP), ~4,99€ (KR) — régulièrement/toujours sous
le seuil de 15€. `evaluate()` (`moteur_cote.py`) et le garde-fou
équivalent de `bonne_affaire_shopify.py` (même clé `regles.cote_min`)
rejettent une cote insuffisante AVANT même de comparer le prix : aucun
prix, même excellent, ne pouvait donc jamais déclencher d'alerte sur
cette carte — ni côté eBay/Vinted/Leboncoin, ni côté boutiques Shopify.
Repéré en vérifiant un signalement d'un des deux audits IA concurrents
(cf. entrée du 17/08/2026), contre les vraies données de `data/cotes.json`
plutôt que sur la seule foi du signalement.

Ce n'était pas un choix technique à trancher seul : `cote_min` est une
règle métier ("ignorer les micro-deals sans intérêt"), et Tiplouf est
justement l'une des 4 cartes suivies en priorité par Justok
(`radar_prix_bas.py`) — signalé à Justok plutôt que corrigé à l'aveugle.
Débloqué via `prix_max_fixe` (même mécanisme déjà en place pour Carapuce
18€/Plumeline 15€, court-circuite `cote_min`) : seuils choisis par Justok,
14€ (FR), 4€ (JP et KR) sur les 3 entrées watchlist correspondantes.

**Vérification avant commit** : suite complète `pytest tests/`
(234/234, +4 tests nouveaux), `config.yaml` validé par `yaml.safe_load` +
`charger_watchlist_config()` (199 critères, sans erreur), `pyflakes`
propre.

## Rafraîchissement des cotes manuelles CN (18/08/2026)

Justok a fourni 4 nouvelles captures Cardmarket JP (référence des 4 cotes
manuelles chinois-traditionnel, cf. entrée du 13/08 sur ce même sujet) :

- **Plumeline ex (Oricorio m2-111)** : tendance 52,51€ -- cohérent avec les
  50€ retenus, juste `cote_date` rafraîchie.
- **Psykokwak (Psyduck m2a-199)** : tendance 16,59€ -- cohérent avec les
  17€ retenus, juste `cote_date` rafraîchie.
- **Tiplouf (Piplup m2-085)** : tendance 4,00€ contre 5,70€ le 13/08
  (-30% environ, vraie baisse de marché, pas du bruit) -- cote corrigée
  de 6€ à 4€.
- **Carapuce (Squirtle sv2a-170)** : tendance JP 25,53€, plus du double de
  la cote actuelle (12€, basée sur Cardtrader KR à l'origine). Écart
  signalé à Justok plutôt que corrigé à l'aveugle (même principe que
  `cote_min`/Tiplouf plus haut) -- décision explicite : GARDER la
  référence KR, ne pas basculer sur le JP comme les 3 autres cartes CN.
  Documenté dans le commentaire pour qu'une future session ne "corrige"
  pas cet écart apparent sans revérifier d'abord.

**Vérification avant commit** : suite complète `pytest tests/` (234/234,
inchangé -- pas de code touché, uniquement `config.yaml`), `config.yaml`
validé par `yaml.safe_load` + `charger_watchlist_config()` (199 critères).

## Cote manuelle posée pour Psykokwak FR (18/08/2026)

En répondant à une question de Justok ("as-tu besoin des cotes
françaises ?"), vérification de `data/cotes.json` pour les 4 cartes
suivies de près : 3/4 ont une cote automatique fonctionnelle (Carapuce
~89-92€, Plumeline ~43€, Tiplouf ~14-19€), mais **Psykokwak FR (226,
Héros Transcendants) n'a AUCUNE entrée du tout** -- ni eBay/Vinted ni le
repli Cardtrader/TCGdex n'ont jamais produit de cote pour cette carte,
signalé à Justok plutôt que deviné. Justok a fourni une capture Cardmarket
FR en retour : tendance 64,46€ (30j 61,11€ / 7j 63,12€ -- le "1 jour" à
110,08€ est un pic isolé récent, pas retenu comme référence). Cote
manuelle posée à 64€ (`cote_date: "2026-08-18"`, rappel automatique après
30 jours comme pour toute cote manuelle).

**Vérification avant commit** : suite complète `pytest tests/` (234/234,
inchangé), `config.yaml` validé par `yaml.safe_load` +
`charger_watchlist_config()` (199 critères).

## V53 : précommandes à confiance "forte" jamais alertées dès la 1ère détection (18/08/2026)

Justok a signalé n'avoir jamais reçu d'alerte 🎉 pour le Coffret ETB 30e
Anniversaire, alors que le radar l'a bien repéré sur `playshop.fr` et
`gamesavenue.fr` (visible dans `data/precommandes_anniversaire_shopify.json`).
Diagnostic via `git log -S` sur ces clés précises (pas une supposition) :
les deux boutiques avaient la date de sortie DÉJÀ confirmée sur la page dès
leur toute première vérification (12/08 et 14/08) -- jamais alertées,
puisque `detecter_nouvelles_precommandes()` (`alerte_precommande.py`)
rendait silencieuse la toute première détection d'un `(domaine,
nom_produit)`, **quelle que soit sa confiance**, pour éviter le bug réel du
11/08 (spam sur des annonces déjà existantes). Le même angle mort touchait
2 autres cas jamais remarqués (`hikarudistribution.com` pour l'ETB ME06
Règne Delta, `playshop.fr` pour la Collection Ultra-Premium Mentali) --
tous vérifiés avec la même méthode `git log -S` avant de conclure, aucun
n'était passé par une transition moyenne→forte qui aurait déjà dû alerter.

Le risque de faux positif du 11/08 concernait spécifiquement les matches
"moyenne" (mots-clés seuls, une vieille annonce sans rapport peut matcher
par coïncidence) -- un match "forte" dès la première détection a une
nature différente : la date de sortie EXACTE attendue est déjà confirmée
sur la page, un faux positif par coïncidence est quasiment exclu.

**Corrigé** : `premiere_fois_ambigue = premiere_fois and confiance !=
"forte"` -- seule une première détection à confiance "moyenne" reste
silencieuse (mémoire établie, comportement inchangé) ; une première
détection DIRECTEMENT à "forte" alerte immédiatement. Les 4 entrées
concernées ont été retirées de `data/precommandes_anniversaire_shopify.json`
(via `memoire_json.charger_memoire`/`sauvegarder_memoire`, pas un
`json.dump` à la main, pour préserver le format exact du fichier -- premier
essai avec `sort_keys=True` corrigé après avoir vu un diff de 70 lignes
au lieu de 4 suppressions propres) pour que le prochain cycle les
redétecte comme "nouvelles" et déclenche les vraies alertes Telegram.

7 nouveaux tests (`tests/test_alerte_precommande.py`) -- première
couverture dédiée à `detecter_nouvelles_precommandes()`, jusqu'ici à 0
test malgré sa logique à 3 états (premiere fois / déjà vu à ce niveau /
déjà confirmé mieux).

**Vérification avant commit** : suite complète `pytest tests/` (241/241,
+7 nouveaux), `pyflakes` propre, diff de la mémoire vérifié minimal (4
suppressions, aucun autre changement de formatage).

## V54 : transition hors-stock -> en-stock jamais mémorisée pour les précommandes (18/08/2026)

Justok, en réaction au fix V53 ci-dessus, a précisé sa vraie attente :
"les dates de précommande ne sont pas égales aux dates de sortie -- je
veux pouvoir précommander dès que possible pour être SÛR de pouvoir
acheter". En relisant `detecter_nouvelles_precommandes()` à la lumière de
cette précision, un second angle mort direct : `memoire[cle_mem]` ne
stockait JAMAIS `en_stock` -- seule `confiance` déterminait si on
re-alertait. Conséquence concrète : une page qui apparaît tôt (date de
sortie déjà confirmée, donc alerte immédiate grâce à V53) mais encore
HORS STOCK (annonce/placeholder avant ouverture réelle) déclenchait bien
une alerte UNE FOIS -- puis plus JAMAIS de second signal quand elle
devient réellement commandable, la confiance ne changeant pas entre les
deux états. Exactement l'inverse de ce que Justok demande : le moment qui
compte pour lui n'est pas l'apparition de la page, c'est le moment où il
peut réellement passer commande.

**Corrigé** : `en_stock` est désormais mémorisé, et une alerte se
déclenche dès que ce champ passe à `True` alors qu'il ne l'était pas avant
(`False`/indéterminé -> `True`) pour un produit **déjà connu**, quel que
soit son niveau de confiance actuel -- cette transition prime sur toutes
les autres règles de suppression, y compris `deja_confirme_mieux`. Une
toute première détection reste soumise aux règles habituelles (V53) :
cette exception ne s'applique qu'à un produit dont le stock vient de
changer, pas à une apparition inédite.

**Effet de bord assumé** : les entrées déjà en mémoire avant ce correctif
n'ont jamais eu `en_stock` enregistré -- au prochain cycle, si l'une
d'elles se trouve actuellement en stock, la transition `None -> True`
sera interprétée comme une ouverture et alertera une fois (rattrapage
naturel, pas un bug). Assumé délibérément : cohérent avec la priorité
explicite de Justok (mieux vaut une alerte de rattrapage honnête qu'un
silence), et chaque alerte reste auto-suffisante (`_texte_precommande`
indique déjà le niveau de confiance réel -- 🟡 probable vs 🟢 confirmée).

5 nouveaux tests couvrant la transition (déjà "forte"+hors stock -> en
stock alerte ; stock indéterminé -> en stock alerte ; reste hors stock ne
re-alerte pas ; reste en stock ne re-alerte pas deux fois ; une première
détection "moyenne" même en_stock=True reste silencieuse), plus mise à
jour de 4 tests existants (fixtures `memoire` complétées avec
`en_stock: True` pour isoler ce qu'ils testent réellement).

**Vérification avant commit** : suite complète `pytest tests/` (246/246,
+5 nouveaux), `pyflakes` propre.

## V55 : UPC Mentali et UPC Noctali étaient un seul produit surveillé, pas deux (18/08/2026)

Justok, en réaction au petit audit récapitulatif de la journée, a précisé :
"UPC Mentali et UPC Noctali sont deux produits distincts". Vérification
dans `precommandes_watchlist.py` : l'entrée "Collection Ultra-Premium —
30e Anniversaire Journée et Soirée (Mentali/Noctali) FR" couvrait bien les
DEUX personnages avec un seul `ProduitSurveille` (mots-clés type incluant
`mentali`/`espeon` ET `noctali`/`umbreon`).

Bug réel identifié **avant qu'il ne se manifeste** (creusé dans la mémoire
du jour même, pas une supposition) : `radar_precommandes._candidat()`
utilise `produit.nom` comme clé de mémoire (`domaine|nom_produit`, cf.
`alerte_precommande._cle_memoire`) -- avec un seul `ProduitSurveille`
couvrant les deux personnages, deux fiches produit distinctes d'une même
boutique (une pour chaque UPC) auraient partagé la MÊME clé mémoire.
`detecter_nouvelles_precommandes()` traite les candidats un par un pour
un même domaine et écrit `memoire[cle_mem]` à chaque itération : la
seconde fiche scannée aurait donc silencieusement écrasé les infos de la
première en mémoire (deux URLs, deux prix, deux statuts de stock
distincts pour un seul emplacement mémoire), perdant le suivi d'une des
deux précommandes sans jamais alerter dessus. Vérifié que ce cas ne
s'était pas encore produit (les 4 entrées existantes en mémoire, une par
boutique, ne couvraient chacune qu'un seul des deux personnages) --
trouvé avant le premier vrai dégât, pas après.

**Corrigé** : scindé en 2 `ProduitSurveille` distincts ("Collection
Ultra-Premium — Espeon (Mentali) 30e Anniversaire FR" et "... — Umbreon
(Noctali) ..."), mêmes mots-clés édition et `date_sortie`, mots-clés type
isolés par personnage. Les 4 entrées mémoire existantes (clé basée sur
l'ancien nom fusionné) retirées des 3 fichiers de mémoire précommandes
pour que le prochain cycle les re-détecte proprement sous les nouvelles
clés séparées -- toutes à confiance "moyenne" (donc silencieuses au
prochain cycle, comportement inchangé pour l'utilisateur, juste la
mémoire interne qui se réaligne).

4 nouveaux tests (`tests/test_precommandes_watchlist.py`, nouveau fichier
-- première couverture dédiée à ce module) : les deux produits ont des
noms distincts ; un titre "UPC Mentali" ne matche QUE le produit Mentali,
jamais Noctali (et inversement) ; la variante anglaise "Espeon" matche
bien le même produit que "Mentali".

**Vérification avant commit** : suite complète `pytest tests/` (250/250,
+4 nouveaux), `pyflakes` propre, diff des 2 fichiers mémoire concernés
vérifié minimal (suppressions seules, aucun autre changement).

**Preuve en direct que le fix V53 fonctionne** : en résolvant un conflit
sur `data/precommandes_anniversaire_shopify.json` (cycle de scan concurrent
pendant cette édition), `playshop.fr` avait déjà été re-détectée à
confiance "forte" à 12:10:59 UTC -- la toute première vraie alerte
immédiate en prod grâce au fix précédent. Cette entrée (nommée sous
l'ancien produit fusionné) a aussi été retirée pour le même
rattrapage V55 -- effet de bord mineur assumé : Justok reçoit une alerte
quasi-identique une seconde fois au prochain cycle, sous le nom du
produit désormais correctement scindé (Mentali seul).
