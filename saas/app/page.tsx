import Link from "next/link";
import { createClient } from "@/lib/supabase/server";

export default async function Home() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col items-center justify-center gap-6 px-6 py-24 text-center">
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-cyan">
        Alertes de prix en direct
      </p>
      <h1 className="font-display text-4xl font-extrabold tracking-tight text-foreground">
        PokéDeals
      </h1>
      <p className="max-w-md text-lg text-muted">
        Configure ta watchlist de cartes Pokémon TCG et reçois une alerte dès
        qu&apos;une bonne affaire tombe en dessous de ton seuil de prix.
      </p>
      <Link
        href={user ? "/dashboard" : "/login"}
        className="rounded-md bg-amber px-6 py-3 text-sm font-semibold text-amber-ink transition hover:brightness-110"
      >
        {user ? "Aller à ma watchlist" : "Commencer"}
      </Link>
    </main>
  );
}
