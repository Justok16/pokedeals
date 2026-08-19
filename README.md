# PokéDeals

Ce dépôt héberge deux projets distincts, côte à côte :

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

## `saas/` — application web SaaS (en développement)

Nouvelle application web, initialisée avec Next.js (TypeScript, Tailwind CSS,
App Router). Pas encore en production.

```bash
cd saas
npm install
npm run dev
```

## Structure du dépôt

```
.
├── .github/workflows/   # workflows CI/CD (cron du scraper + tests)
├── scraper/              # bot Python de veille de prix (production)
└── saas/                 # application web SaaS (Next.js, en développement)
```

Les deux projets sont indépendants : le scraper ne dépend pas du SaaS et
inversement. Les workflows GitHub Actions dans `.github/workflows/` exécutent
leurs commandes avec `working-directory: scraper`.
