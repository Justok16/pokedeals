import Link from "next/link";
import { createClient } from "@/lib/supabase/server";

export default async function Home() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col items-center justify-center gap-6 px-6 py-24 text-center">
      <h1 className="text-4xl font-semibold tracking-tight">PokéDeals</h1>
      <p className="max-w-md text-lg text-zinc-600 dark:text-zinc-400">
        Configure ta watchlist de cartes Pokémon TCG et reçois une alerte dès
        qu&apos;une bonne affaire tombe en dessous de ton seuil de prix.
      </p>
      <Link
        href={user ? "/dashboard" : "/login"}
        className="rounded-full bg-zinc-900 px-6 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
      >
        {user ? "Aller à ma watchlist" : "Commencer"}
      </Link>
    </main>
  );
}
