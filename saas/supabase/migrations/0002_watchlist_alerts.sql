-- Deals detectes par le scraper (scraper/connecteur_supabase.py) qui
-- matchent une carte surveillee par un utilisateur. Ecrite UNIQUEMENT par
-- le scraper (cle service_role, contourne RLS) ; lue par le SaaS via RLS
-- normal (chaque utilisateur ne voit que ses propres alertes).

create table if not exists public.watchlist_alerts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  watchlist_item_id uuid not null references public.watchlist_items (id) on delete cascade,
  titre text not null,
  prix numeric(10, 2) not null,
  url text not null,
  plateforme text,
  created_at timestamptz not null default now(),
  unique (watchlist_item_id, url)
);

create index if not exists watchlist_alerts_user_id_idx on public.watchlist_alerts (user_id);

alter table public.watchlist_alerts enable row level security;

-- Lecture seule cote utilisateur : les alertes sont ecrites exclusivement
-- par le scraper via la cle service_role (qui contourne RLS), jamais par
-- un utilisateur authentifie.
create policy "watchlist_alerts_select_own"
  on public.watchlist_alerts for select
  using (auth.uid() = user_id);
