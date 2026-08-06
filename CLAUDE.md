# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

PokéDeals: a fully-automated arbitrage bot that scans eBay France, Vinted, and Leboncoin (via email alerts) for Pokémon TCG cards, computes a fair market price ("cote") for each watchlist card, and sends Telegram alerts when a listing is priced ≥30% net below that cote (or when stock held in `mes_achats` reaches 2x purchase price). It runs for free on a GitHub Actions cron schedule — there is no server, database, or persistent process.

Comments, log messages, config, and the README are in French (the user's language); code identifiers mix French and English. Keep new code/comments in French to match the existing style.

## Repo layout — intentionally minimal

```
main.py                          ← the entire program, single file
config.yaml                      ← the only file meant to be edited routinely (watchlist, thresholds)
requirements.txt                 ← requests + PyYAML
data/*.json, data/*.csv          ← bot's persistent memory (auto-generated, committed by CI)
.github/workflows/pokedeals.yml  ← cron scheduler + git-commit-back-to-repo step
```

There are no modules/packages — everything lives in `main.py` (~3200 lines) by design (see the file's module docstring, which also documents version history / behavioral changes as `V15`, `V16`, `V26`, ... comments inline). When making a change, add a similarly terse `VNN:` comment near the change explaining *why*, matching the existing convention — this file is the changelog.

## Commands

```bash
pip install -r requirements.txt   # only dependencies: requests, PyYAML
python main.py                    # run one full scan (reads config.yaml, writes data/*.json + .csv)
```

No test suite, linter, or build step exists in this repo. There is no `--dry-run`; running `main.py` performs live HTTP requests (eBay API, Vinted, Gmail IMAP) and can send real Telegram/email notifications, and it mutates `data/*.json`/`data/*.csv` in place. Prefer testing individual functions (e.g. `evaluate`, `calculer_cote`, `annonce_pertinente`) via a Python REPL/one-off script over invoking `main()` when iterating.

Required secrets as env vars (set as GitHub Actions secrets in production; export locally to test end-to-end): `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `TELEGRAM_BOT_TOKEN`, `CARDTRADER_TOKEN`, and optionally `GMAIL_APP_PASSWORD` (for the Leboncoin-via-email flow).

## Architecture (main.py, top to bottom)

The file is organized into clearly delimited sections (search for `# ====` banners). Rough order:

1. **HTTP/text utilities** — `user_agent()`, `requete_avec_retry()`, `normaliser()` (accent/case-insensitive text normalization).
2. **Relevance filters** — `annonce_pertinente()` is the central gate: given a listing title and a watchlist card (name, language, alias), decides whether the listing is really that card, in the right language, not graded/damaged, not a bundle/toy/sealed product. Card-number matching (`extraire_numero*`, `numero_nu_voulu`, `numeros_nus_titre`) and language proof (`preuve_francais`, `_pays_ebay`) live here — this is the most failure-prone area (false positives/negatives), see the many `VNN:` comments explaining past bugs.
3. **Config loading** — `charger_config()`, `secrets_env()`.
4. **Persistent "seen" state** — `charger_vues()`/`sauvegarder_vues()`/`deja_vue()`/`marquer()` (dedup so the same listing isn't alerted twice) and `anciennete()` (tracks how long a listing has been online).
5. **eBay** — OAuth token (`_obtenir_token`), search (`ebay_rechercher`), cote calculation from listings (`calculer_cote`).
6. **Cardtrader integration** — a secondary/cross-check price source (`cardtrader_prix` and the `_ct_*` helpers: blueprint/expansion matching, caching, cross-language sanity checks). Controlled by `config.yaml`'s `api_cotes` block with modes `observation` / `secours` / `actif` / `plus_bas` (see comments above `api_cotes:` in config.yaml for the tradeoffs).
7. **Cardmarket** — `cardmarket_prix()`, a third price source used only as a tie-breaker in `plus_bas` mode.
8. **Generic price API lookup** — `deduire_api_id`, `api_prix_carte` and its cache.
9. **Vinted** — `vinted_rechercher()`, `vinted_description()`.
10. **Leboncoin** — direct scraping (`lbc_rechercher`, currently disabled in config due to DataDome blocking) and the email-alert-based fallback (`lbc_extraire_annonces_email`, `lbc_relever_alertes_email`) which parses Gmail via IMAP.
11. **Cote (fair-price) engine** — `cle_cote`, `cote_lissee` (smoothed over recent scans), `enregistrer_cote`, `obtenir_cote` (orchestrates eBay cote + optional Cardtrader/Cardmarket blending per `api_cotes.mode`).
12. **Deal evaluation** — `evaluate()`: given a listing + cote + config, decides buy/reject and computes net profit; this is where `regles.marge_achat`, `frais_port_max`, `prix_plancher_ratio`, `cote_min`, `profit_min` etc. from config.yaml are applied.
13. **Notifications** — Telegram (`envoyer_telegram*`, HTML-escaped messages) and email (`envoyer_alertes`) senders, plus `verifier_stock()` for resale alerts on `mes_achats`.
14. **Stats/CSV/anomalies/daily recap** — `enregistrer_scan`, `exporter_csv`, `detecter_anomalies` (cote crashed/spiked), `recap_du_jour` (21:00 Paris time summary).
15. **Orchestration** — `collecter()` (runs one card through all active platforms) and `main()` (loops the whole `watchlist`, applies Cardtrader/Cardmarket blending, sends alerts, persists state). Start reading here to trace the full scan flow.

### Data flow per scan (`main()`)

For each card in `config.yaml`'s `watchlist`: `collecter()` gathers raw listings from active platforms (`plateformes:` in config) → `annonce_pertinente()` filters each listing → `obtenir_cote()` computes/blends the fair price (eBay + optionally Cardtrader/Cardmarket per `api_cotes.mode`, with cross-source and cross-language sanity checks) → `evaluate()` scores each surviving listing against `regles` thresholds → qualifying deals go to Telegram/email and get marked "seen" in `data/seen.json` only *after* a successful send. Cotes are persisted to `data/cotes.json`/history for trend detection and the next scan's smoothing.

### config.yaml is the operator interface

Almost all tunable behavior lives in `config.yaml`, not code: `regles` (margins, fees, thresholds), `etats_acceptes`/`etats_refuses` (condition keyword filters), `watchlist` (cards to track, each with `nom` including its exact collection number, `langue`, optional manual `cote` override, optional `alias`), `api_cotes` (Cardtrader blending mode), `mes_achats` (owned stock for resale alerts), `notifications`/`telegram`/`email`, `leboncoin_alertes_email`, `plateformes`. When a user asks to change bot behavior, check `config.yaml` first — code changes are usually unnecessary.

### CI/deployment (`.github/workflows/pokedeals.yml`)

Runs every 15 minutes via cron (`workflow_dispatch` also allowed) on `ubuntu-latest`, installs deps, runs `python main.py`, then commits+pushes any changes under `data/` back to the repo as the bot's persistent memory. The push step has a stash/pull-rebase/re-apply dance specifically to avoid clobbering `data/*.json`/`.csv` when two runs overlap — be careful modifying this workflow, it was hardened after real conflicts (see inline comments).

## Working conventions in this codebase

- Every non-obvious rule change carries a `VNN:` prefixed comment explaining the concrete case that motivated it (often a specific card and observed price discrepancy). Follow this pattern — it's how the file documents its own edge-case history in lieu of a changelog or test suite.
- Money/price sanity checks appear throughout ("garde-fou" = guardrail) to reject implausible cross-source or cross-language price mismatches — preserve these when touching pricing logic; they exist because of real false-positive incidents.
- `main.py` and `requirements.txt` are described in the README as files the end user should never edit — only `config.yaml` is meant for routine changes. Code changes here are for the bot's maintainer (i.e., Claude Code sessions), not the end user.
