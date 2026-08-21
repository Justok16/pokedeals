import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import {
  ajouterCarte,
  basculerNotifEmail,
  deconnexion,
  modifierCarte,
  supprimerCarte,
} from "./actions";
import NotifPush from "./notif-push";

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

  const { data: alertes, error: erreurAlertes } = await supabase
    .from("watchlist_alerts")
    .select("id, titre, prix, url, plateforme, created_at, watchlist_items(nom_carte)")
    .order("created_at", { ascending: false })
    .limit(20);

  const { data: preferences } = await supabase
    .from("user_preferences")
    .select("notif_email")
    .eq("user_id", user.id)
    .maybeSingle();
  const notifEmailActive = preferences?.notif_email ?? true;

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

      <section className="flex flex-col gap-2 rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
        <h2 className="text-sm font-medium">Notifications</h2>
        <NotifPush />
        <form action={basculerNotifEmail} className="flex items-center gap-2">
          <input
            type="checkbox"
            id="notif_email"
            name="notif_email"
            defaultChecked={notifEmailActive}
            className="h-4 w-4"
          />
          <label htmlFor="notif_email" className="text-xs text-zinc-500">
            Recevoir mes alertes par email
          </label>
          <button
            type="submit"
            className="text-xs text-zinc-500 underline-offset-4 hover:underline"
          >
            Enregistrer
          </button>
        </form>
      </section>

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
          <details
            key={carte.id}
            className="rounded-lg border border-zinc-200 dark:border-zinc-800"
          >
            <summary className="flex cursor-pointer list-none items-center justify-between px-4 py-3">
              <div>
                <p className="text-sm font-medium">{carte.nom_carte}</p>
                <p className="text-xs text-zinc-500">
                  {LABELS_LANGUE[carte.langue] ?? carte.langue} · seuil{" "}
                  {Number(carte.prix_seuil).toFixed(2)} €
                  {carte.notes ? ` · ${carte.notes}` : ""}
                </p>
              </div>
              <span className="text-xs text-zinc-500 underline-offset-4 hover:underline">
                Modifier
              </span>
            </summary>

            <div className="border-t border-zinc-200 px-4 py-3 dark:border-zinc-800">
              <form action={modifierCarte} className="grid gap-3 sm:grid-cols-2">
                <input type="hidden" name="id" value={carte.id} />
                <input
                  type="text"
                  name="nom_carte"
                  defaultValue={carte.nom_carte}
                  required
                  className="rounded-lg border border-zinc-300 px-3 py-2 text-sm sm:col-span-2 dark:border-zinc-700 dark:bg-transparent"
                />
                <select
                  name="langue"
                  defaultValue={carte.langue}
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
                  defaultValue={carte.prix_seuil}
                  step="0.01"
                  min="0"
                  required
                  className="rounded-lg border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-transparent"
                />
                <input
                  type="text"
                  name="notes"
                  defaultValue={carte.notes ?? ""}
                  placeholder="Notes (optionnel)"
                  className="rounded-lg border border-zinc-300 px-3 py-2 text-sm sm:col-span-2 dark:border-zinc-700 dark:bg-transparent"
                />
                <div className="flex items-center justify-between sm:col-span-2">
                  <button
                    type="submit"
                    className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
                  >
                    Enregistrer
                  </button>
                  <button
                    type="submit"
                    formAction={supprimerCarte}
                    className="text-xs text-red-600 hover:underline dark:text-red-400"
                  >
                    Retirer
                  </button>
                </div>
              </form>
            </div>
          </details>
        ))}
      </section>

      <section className="flex flex-col gap-3">
        <h2 className="text-sm font-medium">Dernières bonnes affaires détectées</h2>

        {erreurAlertes && (
          <p className="text-sm text-red-600 dark:text-red-400">
            Erreur de chargement : {erreurAlertes.message}
          </p>
        )}

        {!erreurAlertes && alertes?.length === 0 && (
          <p className="text-sm text-zinc-500">
            Aucune alerte pour l&apos;instant — dès qu&apos;une carte de ta
            watchlist tombe sous ton seuil de prix, elle apparaîtra ici.
          </p>
        )}

        {alertes?.map((alerte) => (
          <a
            key={alerte.id}
            href={alerte.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between rounded-lg border border-zinc-200 px-4 py-3 transition hover:border-zinc-400 dark:border-zinc-800 dark:hover:border-zinc-600"
          >
            <div>
              <p className="text-sm font-medium">
                {alerte.watchlist_items?.[0]?.nom_carte ?? alerte.titre}
              </p>
              <p className="text-xs text-zinc-500">
                {alerte.titre}
                {alerte.plateforme ? ` · ${alerte.plateforme}` : ""}
              </p>
            </div>
            <p className="text-sm font-semibold">
              {Number(alerte.prix).toFixed(2)} €
            </p>
          </a>
        ))}
      </section>
    </main>
  );
}
