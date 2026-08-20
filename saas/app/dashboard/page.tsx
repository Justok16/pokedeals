import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { ajouterCarte, deconnexion, supprimerCarte } from "./actions";

const LABELS_LANGUE: Record<string, string> = {
  fr: "Français",
  jp: "Japonais",
  en: "Anglais",
  kr: "Coréen",
  cn: "Chinois",
};

export default async function DashboardPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) redirect("/login");

  const { data: cartes, error } = await supabase
    .from("watchlist_items")
    .select("id, nom_carte, langue, prix_seuil, notes, created_at")
    .order("created_at", { ascending: false });

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-8 px-6 py-12">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Ma watchlist</h1>
          <p className="text-sm text-zinc-500">{user.email}</p>
        </div>
        <form action={deconnexion}>
          <button
            type="submit"
            className="text-sm text-zinc-500 underline-offset-4 hover:underline"
          >
            Se déconnecter
          </button>
        </form>
      </header>

      <section className="rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
        <h2 className="mb-4 text-sm font-medium">Ajouter une carte à surveiller</h2>
        <form action={ajouterCarte} className="grid gap-3 sm:grid-cols-2">
          <input
            type="text"
            name="nom_carte"
            placeholder="Nom de la carte (ex : Dracaufeu ex 199/165)"
            required
            className="rounded-lg border border-zinc-300 px-3 py-2 text-sm sm:col-span-2 dark:border-zinc-700 dark:bg-transparent"
          />
          <select
            name="langue"
            defaultValue="fr"
            className="rounded-lg border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-transparent"
          >
            {Object.entries(LABELS_LANGUE).map(([valeur, label]) => (
              <option key={valeur} value={valeur}>
                {label}
              </option>
            ))}
          </select>
          <input
            type="number"
            name="prix_seuil"
            placeholder="Prix max (€)"
            step="0.01"
            min="0"
            required
            className="rounded-lg border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-transparent"
          />
          <input
            type="text"
            name="notes"
            placeholder="Notes (optionnel)"
            className="rounded-lg border border-zinc-300 px-3 py-2 text-sm sm:col-span-2 dark:border-zinc-700 dark:bg-transparent"
          />
          <button
            type="submit"
            className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-700 sm:col-span-2 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
          >
            Ajouter
          </button>
        </form>
      </section>

      <section className="flex flex-col gap-3">
        {error && (
          <p className="text-sm text-red-600 dark:text-red-400">
            Erreur de chargement : {error.message}
          </p>
        )}

        {!error && cartes?.length === 0 && (
          <p className="text-sm text-zinc-500">
            Aucune carte surveillée pour l&apos;instant.
          </p>
        )}

        {cartes?.map((carte) => (
          <div
            key={carte.id}
            className="flex items-center justify-between rounded-lg border border-zinc-200 px-4 py-3 dark:border-zinc-800"
          >
            <div>
              <p className="text-sm font-medium">{carte.nom_carte}</p>
              <p className="text-xs text-zinc-500">
                {LABELS_LANGUE[carte.langue] ?? carte.langue} · seuil{" "}
                {Number(carte.prix_seuil).toFixed(2)} €
                {carte.notes ? ` · ${carte.notes}` : ""}
              </p>
            </div>
            <form action={supprimerCarte}>
              <input type="hidden" name="id" value={carte.id} />
              <button
                type="submit"
                className="text-xs text-red-600 hover:underline dark:text-red-400"
              >
                Retirer
              </button>
            </form>
          </div>
        ))}
      </section>
    </main>
  );
}
