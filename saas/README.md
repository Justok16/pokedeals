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

### 3. Notifications (push + email) — optionnel

Chaque canal est indépendant et entièrement optionnel : sans sa config, ce
canal est simplement désactivé (cf. `scraper/notifications_saas.py`), le
reste de l'app fonctionne normalement.

**Push navigateur** — aucun compte externe requis, juste une paire de clés
VAPID auto-générées :

```bash
python3 -m venv /tmp/vapidenv && /tmp/vapidenv/bin/pip install -q py-vapid
/tmp/vapidenv/bin/python -c "
from py_vapid import Vapid02
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
import base64
v = Vapid02(); v.generate_keys()
b64url = lambda b: base64.urlsafe_b64encode(b).rstrip(b'=').decode()
print('VAPID_PUBLIC_KEY=' + b64url(v.public_key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)))
print('VAPID_PRIVATE_KEY=' + b64url(v.private_key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())))
"
rm -rf /tmp/vapidenv
```

- `VAPID_PUBLIC_KEY` → variable `NEXT_PUBLIC_VAPID_PUBLIC_KEY` (`.env.local` + réglages Vercel)
- `VAPID_PRIVATE_KEY` → secret GitHub Actions `VAPID_PRIVATE_KEY`
- Ajouter aussi le secret GitHub Actions `VAPID_CLAIM_EMAIL` (une adresse email de contact, requise par le protocole Web Push — n'importe quelle adresse valide convient)

**Email** — nécessite un compte [Resend](https://resend.com) (gratuit jusqu'à un
certain volume) :

1. Créer un compte, récupérer une clé API (**API Keys**)
2. Vérifier un domaine d'envoi (**Domains**), ou utiliser le domaine de test
   `onboarding@resend.dev` fourni par Resend pour démarrer sans domaine propre
3. Ajouter les secrets GitHub Actions `RESEND_API_KEY` et `RESEND_FROM_EMAIL`
   (l'adresse d'envoi, ex: `PokéDeals <alertes@tondomaine.com>`)

### 4. Abonnement payant (Stripe) — optionnel

Sans cette config, tout le monde reste sur le niveau gratuit (`LIMITE_CARTES_GRATUIT`
cartes, cf. `lib/stripe.ts`) — le bouton "Passer à l'abonnement" échouera
tant que `STRIPE_PRICE_ID` n'est pas configuré.

1. Créer un compte sur [stripe.com](https://stripe.com)
2. **Product catalog > Add product** : créer un produit (ex. "PokéDeals Pro"),
   prix récurrent mensuel **7,99€**. Copier l'ID du prix (`price_...`) →
   secret/variable `STRIPE_PRICE_ID`.
3. **Coupons** (tarif early bird verrouillé à vie, 200 premiers abonnés) :
   créer un coupon avec :
   - ID exact : `early-bird-200` (référencé en dur dans `lib/stripe.ts`)
   - Montant : -3,00€, durée **forever** (le prix reste réduit tant que
     l'abonnement continue, pas juste le premier mois)
   - **Max redemptions : 200** — Stripe désactive le coupon tout seul une
     fois ce nombre atteint, le checkout applique alors automatiquement le
     tarif plein sans rien à faire de plus.
4. **Developers > API keys** : copier la clé secrète → `STRIPE_SECRET_KEY`
5. **Developers > Webhooks > Add endpoint** : URL `<ton-domaine>/api/webhooks/stripe`,
   événements à écouter : `checkout.session.completed`,
   `customer.subscription.updated`, `customer.subscription.deleted`. Copier
   le secret de signature (`whsec_...`) → `STRIPE_WEBHOOK_SECRET`
6. Renseigner aussi `SUPABASE_SERVICE_ROLE_KEY` (même clé que celle donnée
   au scraper, cf. section 1) — nécessaire pour que le webhook écrive
   l'état d'abonnement (RLS interdit à l'utilisateur de le faire lui-même)
7. Appliquer la migration `0004_subscriptions.sql` (relancer
   `./scripts/setup-supabase.sh`, ou manuellement dans le SQL Editor)

En mode test Stripe, utiliser la carte `4242 4242 4242 4242` (n'importe
quelle date future, n'importe quel CVC) pour simuler un paiement.

### 5. Lancer en local

```bash
npm install
npm run dev
```

## Structure

- `app/page.tsx` — landing page
- `app/login/` — connexion OAuth (Google/GitHub)
- `app/auth/callback/` — échange du code OAuth contre une session
- `app/dashboard/` — watchlist protégée (liste, ajout, modification, suppression) + dernières alertes détectées + notifications (push/email) + statut d'abonnement
- `app/api/webhooks/stripe/` — synchronise l'état d'abonnement depuis les événements Stripe
- `lib/supabase/` — clients Supabase (browser, server, middleware, admin service_role)
- `lib/stripe.ts` — client Stripe + constantes (limite gratuite, coupon early bird)
- `proxy.ts` — rafraîchissement de session + protection de `/dashboard`
- `supabase/migrations/` — schéma SQL (`watchlist_items`, `watchlist_alerts`, `push_subscriptions`, `user_preferences`, `subscriptions`, policies RLS)
- `scripts/setup-supabase.sh` — provisionne le projet Supabase et applique le schéma via l'API (à lancer en local)

## Déploiement

Prévu pour [Vercel](https://vercel.com) : connecter le repo, définir le
répertoire racine du projet sur `saas/`, et renseigner les variables
d'environnement `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` /
`NEXT_PUBLIC_VAPID_PUBLIC_KEY` / `SUPABASE_SERVICE_ROLE_KEY` /
`STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` / `STRIPE_PRICE_ID` /
`NEXT_PUBLIC_SITE_URL` dans les réglages du projet Vercel.
