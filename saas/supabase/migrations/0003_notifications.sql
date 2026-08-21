-- Abonnements push navigateur (Web Push) : un utilisateur peut avoir
-- plusieurs abonnements (plusieurs appareils/navigateurs). Ecrits par
-- l'utilisateur lui-meme (RLS normal), lus par le scraper via service_role
-- pour l'envoi (cf. scraper/notifications_saas.py).

create table if not exists public.push_subscriptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  endpoint text not null unique,
  p256dh text not null,
  auth text not null,
  created_at timestamptz not null default now()
);

create index if not exists push_subscriptions_user_id_idx on public.push_subscriptions (user_id);

alter table public.push_subscriptions enable row level security;

create policy "push_subscriptions_select_own"
  on public.push_subscriptions for select
  using (auth.uid() = user_id);

create policy "push_subscriptions_insert_own"
  on public.push_subscriptions for insert
  with check (auth.uid() = user_id);

create policy "push_subscriptions_delete_own"
  on public.push_subscriptions for delete
  using (auth.uid() = user_id);

-- Preference de notification email (activee par defaut -- l'email est deja
-- connu via l'auth OAuth, pas de saisie supplementaire requise). Une ligne
-- par utilisateur, jamais une colonne dupliquee sur chaque watchlist_items.
-- Le push n'a pas besoin d'une table equivalente : sa presence/absence dans
-- push_subscriptions suffit a savoir si l'utilisateur l'a active.
create table if not exists public.user_preferences (
  user_id uuid primary key references auth.users (id) on delete cascade,
  notif_email boolean not null default true
);

alter table public.user_preferences enable row level security;

create policy "user_preferences_select_own"
  on public.user_preferences for select
  using (auth.uid() = user_id);

create policy "user_preferences_upsert_own"
  on public.user_preferences for insert
  with check (auth.uid() = user_id);

create policy "user_preferences_update_own"
  on public.user_preferences for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
