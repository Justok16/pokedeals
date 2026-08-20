# PokéDeals — SaaS

Application web (Next.js, App Router, Tailwind CSS) permettant à chaque
utilisateur de configurer sa propre watchlist de cartes Pokémon TCG (nom,
langue, seuil de prix) et de voir apparaître ici les bonnes affaires
détectées par le bot `scraper/`, qui alimente la même base Supabase (cf.
`scraper/connecteur_supabase.py`) en plus de ses alertes Telegram existantes.

PWA : voir `public/sw.js`, `public/manifest` (généré via `app/manifest.ts`)
et `app/register-sw.tsx`.

## Mise en route

### 1. Créer le projet Supabase + appliquer le schéma

**Option automatique (recommandée)** — nécessite `jq` et un accès réseau
non restreint vers `api.supabase.com` (donc en local, pas depuis un
environnement sandboxé) :

```bash
# 1. Créer un compte sur https://supabase.com
# 2. Créer un jeton sur https://supabase.com/dashboard/account/tokens
export SUPABASE_ACCESS_TOKEN=sbp_xxxxx
./scripts/setup-supabase.sh
```

Le script crée le projet, applique toutes les migrations de
`supabase/migrations/` (schéma `watchlist_items` + `watchlist_alerts`),
écrit `.env.local` avec l'URL et la clé anonyme, et affiche à la fin les
deux secrets à ajouter côté GitHub Actions pour connecter le scraper
(`SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY`).

**Option manuelle** :

1. Créer un compte sur [supabase.com](https://supabase.com) et un nouveau projet.
2. Dans **Project Settings > API**, récupérer l'URL du projet et la clé `anon public`.
3. Copier `.env.example` vers `.env.local` et renseigner ces deux valeurs.
4. Dans le dashboard Supabase (**SQL Editor**), exécuter dans l'ordre le
   contenu de chaque fichier de `supabase/migrations/` (`0001_...` puis
   `0002_...`).
5. Pour connecter le scraper : dans **Project Settings > API**, récupérer
   aussi la clé `service_role` (secrète), puis l'ajouter avec l'URL du
   projet comme secrets `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` sur le
   dépôt GitHub (**Settings > Secrets and variables > Actions**). Sans ces
   secrets, le scraper continue de fonctionner normalement (fonctionnalité
   optionnelle, cf. `scraper/connecteur_supabase.py`) — les utilisateurs ne
   verront simplement aucune alerte apparaître dans leur dashboard.

### 2. Configurer les fournisseurs OAuth (Google + GitHub)

Dans le dashboard Supabase, **Authentication > Providers** :

- **Google** : créer des identifiants OAuth 2.0 dans
  [Google Cloud Console](https://console.cloud.google.com/apis/credentials),
  avec comme URI de redirection autorisée celle indiquée par Supabase
  (`https://<projet>.supabase.co/auth/v1/callback`). Renseigner le Client ID
  et le Client Secret dans Supabase.
- **GitHub** : créer une OAuth App dans
  [GitHub Developer Settings](https://github.com/settings/developers), même
  URI de callback. Renseigner le Client ID et le Client Secret dans Supabase.

Dans **Authentication > URL Configuration**, ajouter l'URL du site (en local :
`http://localhost:3000`, en prod : l'URL Vercel) à la liste des Redirect URLs.

### 3. Lancer en local

```bash
npm install
npm run dev
```

## Structure

- `app/page.tsx` — landing page
- `app/login/` — connexion OAuth (Google/GitHub)
- `app/auth/callback/` — échange du code OAuth contre une session
- `app/dashboard/` — watchlist protégée (liste, ajout, suppression) + dernières alertes détectées
- `lib/supabase/` — clients Supabase (browser, server, middleware)
- `proxy.ts` — rafraîchissement de session + protection de `/dashboard`
- `supabase/migrations/` — schéma SQL (`watchlist_items`, `watchlist_alerts`, policies RLS)
- `scripts/setup-supabase.sh` — provisionne le projet Supabase et applique le schéma via l'API (à lancer en local)

## Déploiement

Prévu pour [Vercel](https://vercel.com) : connecter le repo, définir le
répertoire racine du projet sur `saas/`, et renseigner les variables
d'environnement `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`
dans les réglages du projet Vercel.
