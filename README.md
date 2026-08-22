# PokéDeals

## `scraper/` — bot de veille de prix Pokémon TCG (production)

Le bot Python historique : scanne eBay, Vinted, Leboncoin et 83+ boutiques
françaises/japonaises spécialisées pour détecter des bonnes affaires, des
retours en stock et des précommandes, avec alertes Telegram. Tourne en
production **uniquement via des cron GitHub Actions** (voir `.github/workflows/`),
sans serveur ni base de données — son état persiste dans `scraper/data/*.json`.

Voir `scraper/CLAUDE.md` pour l'architecture détaillée et `scraper/README.md`
pour la documentation d'usage.

```bash
cd scraper
pip install -r requirements.txt
python main.py
```

## Application web SaaS

L'application web (watchlists personnalisées, notifications, abonnement payant)
vit dans un dépôt privé séparé : `justok16/pokedeals-saas`. Elle alimente sa base
Supabase à partir de ce scraper (voir `scraper/connecteur_supabase.py`), mais son
code n'est pas hébergé ici.

## Structure du dépôt

```
.
├── .github/workflows/   # workflows CI/CD (cron du scraper + tests)
└── scraper/              # bot Python de veille de prix (production)
```
