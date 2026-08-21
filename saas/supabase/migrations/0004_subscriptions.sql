-- Etat de l'abonnement Stripe de chaque utilisateur. Ecrite UNIQUEMENT par
-- le webhook Stripe (saas/app/api/webhooks/stripe/route.ts, cle service_role,
-- contourne RLS) -- jamais par l'utilisateur lui-meme (pas de policy insert/
-- update cote client, seulement select).

create table if not exists public.subscriptions (
  user_id uuid primary key references auth.users (id) on delete cascade,
  stripe_customer_id text not null unique,
  stripe_subscription_id text unique,
  status text not null default 'none' check (
    status in ('none', 'active', 'trialing', 'past_due', 'canceled', 'unpaid')
  ),
  price_id text,
  current_period_end timestamptz,
  updated_at timestamptz not null default now()
);

alter table public.subscriptions enable row level security;

create policy "subscriptions_select_own"
  on public.subscriptions for select
  using (auth.uid() = user_id);

-- Nombre de cartes autorisees pour un utilisateur SANS abonnement actif
-- (niveau gratuit). Verifie cote application (saas/app/dashboard/actions.ts,
-- ajouterCarte) -- pas de contrainte DB, car la limite depend du statut
-- d'abonnement, pas d'une regle purement structurelle.
