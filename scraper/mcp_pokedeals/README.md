# MCP PokéDeals

Serveur MCP (Model Context Protocol) exposant des données Pokémon TCG
(cartes, sets, prix) à une IA comme Claude Code — module **indépendant**
du reste du dépôt PokéDeals : il ne modifie et n'importe rien de `main.py`
ni des workflows GitHub Actions existants, et tourne **en local sur ta
machine**, jamais en CI.

## Architecture

```
Claude Code
    ↓
MCP PokéDeals (mcp_pokedeals/server.py, transport stdio)
    ↓
Providers
  ├── TCGdex      (cartes, sets — gratuit, sans clé)
  ├── CardDex     (prix — gratuit, clé optionnelle)
  └── Cardmarket  (guide de prix officiel — gratuit, sans clé
                   + interface Marketplace désactivée par défaut)
```

## Outils MCP disponibles

| Outil | Fonction | Source | Statut |
|---|---|---|---|
| `search_cards` | Recherche cartes (nom, numéro, set, rareté, langue) | TCGdex | ✅ Disponible gratuitement |
| `get_card` | Détails complets d'une carte | TCGdex | ✅ Disponible gratuitement |
| `search_set` | Recherche d'extension | TCGdex | ✅ Disponible gratuitement |
| `get_set_cards` | Cartes d'un set (paginé) | TCGdex | ✅ Disponible gratuitement |
| `get_card_prices` | Prix, par source, jamais mélangés | CardDex + Cardmarket | ⚠️ Voir statut par source ci-dessous |
| `analyze_card` | Synthèse informative carte + prix (PAS une prédiction) | TCGdex + prix | Dépend des outils ci-dessus |

## Statut des sources

### TCGdex — ✅ Disponible gratuitement, sans clé
API publique confirmée et **déjà utilisée en production** dans `main.py`
(racine du dépôt) depuis des mois — les noms de champs JSON utilisés ici
(`localId`, `set.cardCount.official`, `pricing.cardmarket.trend`...) sont
donc **vérifiés empiriquement**, pas devinés. Le module `providers/
tcgdex.py` fait des appels REST directs (`requests`) plutôt que d'utiliser
le SDK officiel `tcgdex-sdk` (PyPI) : le modèle d'objets exact de ce SDK
n'a pas pu être vérifié en détail pendant le développement (accès web
bloqué dans l'environnement de développement — voir plus bas). C'est un
choix de prudence, pas un rejet du SDK — libre à toi de migrer vers
`tcgdex-sdk` plus tard si tu le vérifies toi-même.

### CardDex — ⚠️ À vérifier précisément avant la première utilisation
Le service existe réellement (bêta publique, [carddex.dev](https://carddex.dev/)),
avec un jeu de données public sans clé et une clé gratuite optionnelle
pour une limite plus haute (header `X-API-Key`, clés au format
`pk_live_...`). **L'URL de base par défaut (`CARDDEX_BASE_URL` dans
`.env.example`) est une déduction, pas une valeur confirmée** — l'accès
web direct était bloqué dans l'environnement où ce module a été écrit.

**Avant la première utilisation** : va sur https://carddex.dev/, vérifie
l'URL de base réelle de l'API et le chemin exact de l'endpoint de prix, et
corrige `CARDDEX_BASE_URL` dans ton `.env` si besoin — **aucune
modification de code n'est nécessaire**, tout est piloté par variable
d'environnement. Si l'URL est incorrecte, `get_card_prices` te renverra un
message d'erreur explicite te renvoyant vers cette vérification (pas une
erreur réseau opaque).

### Cardmarket — Statut nuancé, deux intégrations séparées
- **Guide de prix officiel (`price_guide_6.json`)** : ✅ disponible
  gratuitement, sans authentification. Fichier public publié par
  Cardmarket lui-même une fois par jour — aucun scraping. C'est la **même
  technique déjà utilisée en production** dans `main.py`
  (`cardmarket_prix()`/`_cm_charger_guide_prix()`, depuis le 26/07/2026).
  Limite connue : ce guide identifie les cartes par un `idProduct`
  Cardmarket numérique, pas par nom — il faut déjà connaître cet
  identifiant (`get_card_prices(..., cardmarket_product_id=...)`).
- **API Marketplace (annonces, vente)** : ❌ **non disponible sans compte
  vendeur Cardmarket**. Nécessite une authentification OAuth 1.0 (clé +
  token + signature HMAC-SHA1 par requête), pas une simple clé API.
  Volontairement **non implémentée** — voir `providers/cardmarket.py`
  (`CardmarketMarketplaceProvider`), qui documente la situation et lève
  une erreur explicite si on tente de l'utiliser. Aucun scraping, aucun
  contournement d'authentification n'a été fait.

## ⚠️ Limite de développement à connaître

Ce module a été écrit dans un environnement où l'accès web direct
(récupération de pages de documentation) était bloqué — seule la
recherche web (résumés indexés) était disponible. Tout ce qui a pu être
**vérifié empiriquement** (le package `mcp` réellement installé et
introspecté, le code TCGdex déjà en prod dans `main.py`) l'a été. Ce qui
n'a **pas** pu l'être (endpoints exacts de CardDex) est clairement marqué
ci-dessus, avec un mécanisme de correction simple (variable d'env) plutôt
qu'un code qui prétend fonctionner sans l'avoir vérifié.

---

## Installation

### 1. Prérequis
- Python **3.10 ou plus** en local (vérifie avec `python --version` — le
  paquet `mcp` l'exige).
- Le dépôt PokéDeals cloné en local.

### 2. Installer les dépendances du MCP
```bash
cd pokedeals
pip install -r mcp_pokedeals/requirements.txt
```
Ces dépendances (`mcp`, `requests`, `python-dotenv`) sont **séparées** de
`requirements.txt` (racine, utilisé par les workflows GitHub Actions en
prod) — aucun impact sur PokéDeals.

### 3. Configurer les variables d'environnement
```bash
cp .env.example .env
```
Ouvre `.env` et ajuste si besoin (voir "Statut des sources" ci-dessus).
Pour un usage basique (TCGdex + guide de prix Cardmarket), **aucune
valeur à remplir** : les valeurs par défaut suffisent.

### 4. Lancer le serveur manuellement (vérification)
```bash
python -m mcp_pokedeals.server
```
Le serveur attend des messages sur son entrée standard (normal, c'est le
fonctionnement MCP en stdio) — arrête avec `Ctrl+C`. S'il démarre sans
erreur, l'installation est correcte.

### 5. Lancer les tests
```bash
pip install -r requirements-dev.txt   # ajoute pytest (si pas deja fait)
python -m pytest mcp_pokedeals/tests/ -v
```
Tous les tests utilisent des réponses HTTP simulées (mock) — **aucun
appel réseau réel**, donc aucune dépendance à la disponibilité de TCGdex/
CardDex/Cardmarket pour que les tests passent.

---

## Configuration Claude Code

### Option A — fichier déjà fourni
Un fichier `.mcp.json` existe déjà à la racine du dépôt, pointant vers
`python -m mcp_pokedeals.server`. Si ton dépôt est ouvert dans Claude
Code, il devrait être détecté automatiquement.

### Option B — commande `claude mcp add` (recommandé pour vérifier/régénérer)
Depuis la racine du dépôt :
```bash
claude mcp add --scope project --transport stdio pokedeals -- python -m mcp_pokedeals.server
```
Cela écrit (ou corrige) `.mcp.json` automatiquement.

### Vérifier que Claude voit bien les outils
```bash
claude mcp list
```
Dans une session Claude Code, tape aussi `/mcp` pour voir le statut de
connexion du serveur `pokedeals`.

### Première requête (exemple)
Une fois connecté, demande simplement à Claude, en langage naturel :
> "Cherche la carte Dracaufeu (Charizard) du set Darkness Ablaze avec le
> MCP PokéDeals"

Claude appellera l'outil `search_cards` (voire `get_card` ensuite) tout
seul.

---

## Cache et limites de requêtes

- Cartes et sets : cache **24h** (`MCP_CACHE_TTL_CARTES`/`MCP_CACHE_TTL_SETS`).
- Prix (CardDex) : cache **3h** (`MCP_CACHE_TTL_PRIX`).
- Guide de prix Cardmarket : cache **20h minimum**, forcé (le fichier
  n'est publié qu'une fois par jour par Cardmarket).
- Le cache est un simple fichier JSON local (`mcp_pokedeals/.cache/`,
  exclu de git) — aucune base de données à installer.
- Aucune requête en parallèle : chaque outil fait ses appels
  séquentiellement, un par un.

## Gestion des erreurs

Toutes les erreurs réseau/API remontent un message clair (jamais une
traceback Python) : timeout, HTTP 4xx/5xx, JSON invalide, ressource
introuvable, clé API manquante ou invalide, prix indisponible. Exemple :
```
CardDex : limite de requetes atteinte (HTTP 429), reessaie plus tard
```

## Sécurité

- Aucune clé API en dur dans le code — tout passe par variables
  d'environnement (`.env`, jamais committé, déjà dans `.gitignore`).
- `.env.example` ne contient que des valeurs publiques ou vides.
- Aucun scraping agressif : TCGdex et le guide de prix Cardmarket sont
  des sources publiques officielles ; l'API Marketplace Cardmarket
  (nécessitant un contournement d'authentification pour être utilisée
  sans compte) n'a **pas** été implémentée.
- Le cache local (`mcp_pokedeals/.cache/`) est exclu de git.

## Fichiers de ce module

```
mcp_pokedeals/
├── server.py              ← point d'entree, declare les outils MCP
├── config.py               ← lecture des variables d'environnement
├── models.py                ← Card, CardSet, PriceResult
├── cache.py                  ← cache JSON avec expiration (TTL)
├── providers/
│   ├── tcgdex.py               ← cartes, sets (API publique)
│   ├── carddex.py               ← prix (a verifier, voir statut)
│   └── cardmarket.py             ← guide de prix officiel + interface OAuth desactivee
├── services/
│   ├── cards.py                    ← search_cards, get_card, search_set, get_set_cards
│   ├── prices.py                    ← get_card_prices (sources jamais melangees)
│   └── analysis.py                   ← analyze_card (synthese, pas de prediction)
├── tests/                              ← tests unitaires, mocks HTTP, pas de reseau reel
├── requirements.txt                      ← dependances MCP uniquement
└── README.md                               ← ce fichier
```
