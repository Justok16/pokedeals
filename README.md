# PokéDeals

## `scraper/` — bot de veille de prix Pokémon TCG (production)

Le bot Python historique : scanne eBay, Vinted, Leboncoin et 83+ boutiques
françaises/japonaises spécialisées (Shopify, PrestaShop, WooCommerce) pour
détecter des bonnes affaires, des retours en stock et des précommandes, avec
alertes Telegram. Tourne en production **uniquement via des cron GitHub
Actions** (voir `.github/workflows/`), sans serveur ni base de données pour
sa logique propre — son état persiste dans `scraper/data/*.json` (et de plus
en plus dans Supabase, cf. ci-dessous).

Fiabilité : eBay, Vinted et Leboncoin ont chacun leur propre **coupe-circuit**
(après 3 échecs réels consécutifs — jamais un 0 résultat légitime ni un
blocage anti-bot déjà connu comme routine — la plateforme est abandonnée
pour le reste du cycle, les autres continuent normalement). Un radar de
**découverte automatique** de nouvelles boutiques (AFNIC) et un **watchdog**
qui surveille la santé des 10 workflows de scan complètent le dispositif.

Chaque cote eBay calculée persiste aussi désormais le nombre d'annonces qui
l'ont alimentée (`nb_annonces`, dans `data/cotes.json`) — une donnée brute
posée en base pour un futur système de score de rareté/potentiel (repérer
des cartes rares en nombre dont le prix n'a pas encore décollé), pas encore
un calcul actif aujourd'hui.

Voir `scraper/CLAUDE.md` pour l'architecture détaillée et `scraper/README.md`
pour la documentation d'usage.

```bash
cd scraper
pip install -r requirements.txt
python main.py
```

## Application web SaaS

L'application web (watchlists personnalisées, notifications, abonnement
payant) vit dans un dépôt privé séparé : `justok16/pokedeals-saas`. Elle
alimente sa base Supabase à partir de ce scraper (voir
`scraper/connecteur_supabase.py`), mais son code n'est pas hébergé ici.

Ce scraper alimente le dashboard SaaS de deux façons :
- **Détection** : les cartes des watchlists personnalisées des utilisateurs
  (en plus de `config.yaml`) sont scannées comme n'importe quelle carte, et
  toute bonne affaire trouvée est écrite dans `watchlist_alerts` puis notifiée
  par push et/ou email.
- **Radar de vérification périodique** (`verifier_alertes_watchlist.py`,
  cron 30 min) : revérifie la disponibilité et le prix des bonnes affaires
  déjà enregistrées dans `watchlist_alerts`, pour que le dashboard ne reste
  pas figé sur l'état constaté au moment de la détection. Fiable pour les
  boutiques Shopify/PrestaShop/WooCommerce (mêmes techniques d'extraction que
  les connecteurs de scan) ; hors périmètre pour eBay/Vinted/Leboncoin (pas
  de vérification fiable possible sans API dédiée), pour lesquels le badge de
  disponibilité reste simplement non renseigné plutôt que faussé. L'utilisateur
  est notifié (push/email) uniquement sur deux transitions réelles — la carte
  vient d'être vendue/retirée, ou son prix a encore baissé de plus de 5% sous
  le prix d'origine — jamais à chaque cycle sur un état déjà connu.

Un projet séparé, **PokéPrécoms** (dépôt `justok16/pokeprecoms`, pas encore
développé), réutilisera le radar de précommandes génériques de ce scraper
(détection de n'importe quel produit scellé Pokémon en précommande, pas
seulement une liste connue à l'avance) via un pont Supabase dédié.

## Structure du dépôt

```
.
├── .github/workflows/   # workflows CI/CD (cron du scraper + tests)
└── scraper/              # bot Python de veille de prix (production)
```
