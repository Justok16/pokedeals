-- Watchlist personnalisee : chaque utilisateur configure les cartes qu'il
-- veut surveiller + son seuil de prix. Alimentee par le SaaS (CRUD utilisateur)
-- et lue par le scraper (scraper/) pour savoir qui alerter sur quel deal.

create table if not exists public.watchlist_items (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  nom_carte text not null,
  langue text not null default 'fr' check (langue in ('fr', 'jp', 'en', 'kr', 'cn')),
  prix_seuil numeric(10, 2) not null check (prix_seuil >= 0),
  notes text,
  created_at timestamptz not null default now()
);

create index if not exists watchlist_items_user_id_idx on public.watchlist_items (user_id);

alter table public.watchlist_items enable row level security;

-- Chaque utilisateur ne voit et ne modifie que ses propres lignes.
create policy "watchlist_items_select_own"
  on public.watchlist_items for select
  using (auth.uid() = user_id);

create policy "watchlist_items_insert_own"
  on public.watchlist_items for insert
  with check (auth.uid() = user_id);

create policy "watchlist_items_update_own"
  on public.watchlist_items for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "watchlist_items_delete_own"
  on public.watchlist_items for delete
  using (auth.uid() = user_id);
