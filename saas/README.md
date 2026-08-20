# PokéDeals — SaaS

Application web (Next.js, App Router, Tailwind CSS) permettant à chaque
utilisateur de configurer sa propre watchlist de cartes Pokémon TCG (nom,
langue, seuil de prix) et de recevoir ses alertes personnalisées, en
complément du bot `scraper/` qui tourne déjà en production.

PWA : voir `public/sw.js`, `public/manifest` (généré via `app/manifest.ts`)
et `app/register-sw.tsx`.

## Mise en route

### 1. Créer un projet Supabase

1. Créer un compte sur [supabase.com](https://supabase.com) et un nouveau projet.
2. Dans **Project Settings > API**, récupérer l'URL du projet et la clé `anon public`.
3. Copier `.env.example` vers `.env.local` et renseigner ces deux valeurs :

   ```bash
   cp .env.example .env.local
   ```

### 2. Appliquer le schéma de base de données

Le schéma vit dans `supabase/migrations/`. Depuis le dashboard Supabase
(**SQL Editor**), exécuter le contenu de `supabase/migrations/0001_watchlist_items.sql`.

(Alternative en local avec la CLI Supabase : `npx supabase link` puis
`npx supabase db push` — nécessite Docker.)

### 3. Configurer les fournisseurs OAuth (Google + GitHub)

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

### 4. Lancer en local

```bash
npm install
npm run dev
```

## Structure

- `app/page.tsx` — landing page
- `app/login/` — connexion OAuth (Google/GitHub)
- `app/auth/callback/` — échange du code OAuth contre une session
- `app/dashboard/` — watchlist protégée (liste, ajout, suppression)
- `lib/supabase/` — clients Supabase (browser, server, middleware)
- `middleware.ts` — rafraîchissement de session + protection de `/dashboard`
- `supabase/migrations/` — schéma SQL (table `watchlist_items`, policies RLS)

## Déploiement

Prévu pour [Vercel](https://vercel.com) : connecter le repo, définir le
répertoire racine du projet sur `saas/`, et renseigner les variables
d'environnement `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`
dans les réglages du projet Vercel.
