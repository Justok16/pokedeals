# Notes de session — extension multi-plateforme PokéDeals

Dernière mise à jour : 2026-08-10, en fin de session (contexte sur le point de manquer).

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
- `scan_boutique_prestashop.py` (PrestaShop, 15 boutiques actives dans `boutiques_prestashop.py` — 16 couvertes par sitemap moins `bcd-jeux.fr` retirée, sitemap cassé côté site)
- `scan_boutique_woocommerce.py` (WooCommerce, 26 boutiques actives dans `boutiques_woocommerce.py`, scindées en 2 lots équilibrés par volume d'URLs pour le workflow)

**Workflows GitHub Actions :** `.github/workflows/{pokedeals,scan_shopify,scan_prestashop,scan_woocommerce}.yml`

## Travail de couverture interrompu, code écrit mais PAS testé de bout en bout ni intégré aux listes actives

Suite à la demande "compléter avec les cas restants les plus rentables", du
code a été ajouté (déjà commité) mais l'intégration finale n'a pas été
terminée avant que la priorité bascule sur les 3 bugs de production :

- **Repli "recherche HTML"** (`rechercher_via_recherche_html`) ajouté à
  `connecteur_prestashop_sitemap.py` et `connecteur_woocommerce.py`, pour
  les boutiques sans sitemap exploitable. Fonctionne en isolation
  (vérifié sur pokemoncarte.com, investcollect.com, kiokutcg.fr,
  nexthobby.fr) mais :
  - **`gamespirit.fr` et `lepantheon-tcg.com`** : confirmés NON couvrables
    (ni sitemap, ni JSON-LD, ni microdata schema.org) — à laisser de côté.
  - **`mymesis.fr`** : sitemap cassé (pointe vers un domaine de démo
    générique) ET sa recherche interne ne renvoie aucun résultat pour
    "dracaufeu"/"pikachu" — probablement faible valeur (boutique
    accessoires/sleeves), pas prioritaire.
  - **`nexthobby.fr`** : re-testé avec succès (200 après 45s d'attente),
    identifié comme WooCommerce, sans sitemap. Repli recherche HTML
    fonctionnel après généralisation de la détection (classes CSS trop
    fragiles, remplacées par une détection par forme d'URL/domaine).
  - **`investcollect.com`** : plus de blocage 403 constaté (contrairement à
    l'audit initial) — son HTML de recherche est parfois rendu dans un
    bloc échappé façon JSON (`href=\"https:\/\/...\"`), un cas de
    normalisation ajouté dans `_decouvrir_candidats_recherche`.
  - **PAS ENCORE FAIT** : re-test complet sur l'échantillon de 10 cartes
    pour `pokemoncarte.com`/`investcollect.com`/`kiokutcg.fr`/
    `nexthobby.fr` avec le code le plus à jour (les derniers tests datent
    d'avant certains fixes) ; intégration de ces boutiques dans
    `boutiques_prestashop.py`/`boutiques_woocommerce.py` (listes actives) ;
    aucun nouveau workflow à créer (décision déjà prise : les intégrer aux
    workflows existants, pas de 5e cron).

## Prochaines étapes suggérées (par ordre de priorité)

1. ~~Committer le fix de symétrie du filtre qualificatif~~ — fait.
2. ~~Terminer le test de non-régression du fix qualificatif sur les listes
   actives complètes des 3 plateformes~~ — fait (81/81 boutiques, 2 runs,
   0 régression, cf. sections dédiées ci-dessus). Committer le fix du faux
   positif `NOMS_SET_QUALIFICATIF_AMBIGU` (`watchlist_shopify.py`,
   `bonne_affaire_shopify.py`, `alerte_stock.py` — modifiés, pas encore
   commités à la fin de cette session).
3. Reprendre le travail de couverture interrompu : test final sur
   l'échantillon de 10 cartes pour les 4 boutiques nouvellement
   couvrables (pokemoncarte.com, investcollect.com, kiokutcg.fr,
   nexthobby.fr), puis intégration dans les listes actives existantes.
