"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";

const LANGUES_VALIDES = ["fr", "jp", "en", "kr", "cn"] as const;

export async function ajouterCarte(formData: FormData) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const nomCarte = String(formData.get("nom_carte") ?? "").trim();
  const langue = String(formData.get("langue") ?? "fr");
  const prixSeuilBrut = String(formData.get("prix_seuil") ?? "");
  const notes = String(formData.get("notes") ?? "").trim() || null;

  const prixSeuil = Number(prixSeuilBrut.replace(",", "."));

  if (!nomCarte) {
    throw new Error("Le nom de la carte est requis.");
  }
  if (!Number.isFinite(prixSeuil) || prixSeuil < 0) {
    throw new Error("Le seuil de prix doit être un nombre positif.");
  }
  if (!LANGUES_VALIDES.includes(langue as (typeof LANGUES_VALIDES)[number])) {
    throw new Error("Langue invalide.");
  }

  const { error } = await supabase.from("watchlist_items").insert({
    user_id: user.id,
    nom_carte: nomCarte,
    langue,
    prix_seuil: prixSeuil,
    notes,
  });

  if (error) throw new Error(error.message);

  revalidatePath("/dashboard");
}

export async function modifierCarte(formData: FormData) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const id = String(formData.get("id") ?? "");
  const nomCarte = String(formData.get("nom_carte") ?? "").trim();
  const langue = String(formData.get("langue") ?? "fr");
  const prixSeuilBrut = String(formData.get("prix_seuil") ?? "");
  const notes = String(formData.get("notes") ?? "").trim() || null;

  const prixSeuil = Number(prixSeuilBrut.replace(",", "."));

  if (!id) return;
  if (!nomCarte) {
    throw new Error("Le nom de la carte est requis.");
  }
  if (!Number.isFinite(prixSeuil) || prixSeuil < 0) {
    throw new Error("Le seuil de prix doit être un nombre positif.");
  }
  if (!LANGUES_VALIDES.includes(langue as (typeof LANGUES_VALIDES)[number])) {
    throw new Error("Langue invalide.");
  }

  // RLS s'assure déjà qu'un utilisateur ne peut modifier que ses propres
  // lignes -- le filtre user_id ici est une défense en profondeur.
  const { error } = await supabase
    .from("watchlist_items")
    .update({ nom_carte: nomCarte, langue, prix_seuil: prixSeuil, notes })
    .eq("id", id)
    .eq("user_id", user.id);

  if (error) throw new Error(error.message);

  revalidatePath("/dashboard");
}

export async function supprimerCarte(formData: FormData) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const id = String(formData.get("id") ?? "");
  if (!id) return;

  // RLS s'assure déjà qu'un utilisateur ne peut supprimer que ses propres
  // lignes -- le filtre user_id ici est une défense en profondeur, pas la
  // seule barrière.
  const { error } = await supabase
    .from("watchlist_items")
    .delete()
    .eq("id", id)
    .eq("user_id", user.id);

  if (error) throw new Error(error.message);

  revalidatePath("/dashboard");
}

type SubscriptionPushJSON = {
  endpoint: string;
  keys?: { p256dh?: string; auth?: string };
};

export async function enregistrerAbonnementPush(subscription: SubscriptionPushJSON) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const p256dh = subscription.keys?.p256dh;
  const auth = subscription.keys?.auth;
  if (!subscription.endpoint || !p256dh || !auth) {
    throw new Error("Abonnement push invalide.");
  }

  const { error } = await supabase.from("push_subscriptions").upsert(
    {
      user_id: user.id,
      endpoint: subscription.endpoint,
      p256dh,
      auth,
    },
    { onConflict: "endpoint" }
  );

  if (error) throw new Error(error.message);
}

export async function supprimerAbonnementPush(endpoint: string) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  await supabase
    .from("push_subscriptions")
    .delete()
    .eq("endpoint", endpoint)
    .eq("user_id", user.id);
}

export async function basculerNotifEmail(formData: FormData) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const active = formData.get("notif_email") === "on";

  const { error } = await supabase
    .from("user_preferences")
    .upsert({ user_id: user.id, notif_email: active }, { onConflict: "user_id" });

  if (error) throw new Error(error.message);

  revalidatePath("/dashboard");
}

export async function deconnexion() {
  const supabase = await createClient();
  await supabase.auth.signOut();
  redirect("/");
}
