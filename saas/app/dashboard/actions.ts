"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { EARLY_BIRD_COUPON_ID, LIMITE_CARTES_GRATUIT, getStripe } from "@/lib/stripe";

const LANGUES_VALIDES = ["fr", "jp", "en", "kr", "cn"] as const;
const STATUTS_ABONNEMENT_ACTIF = ["active", "trialing"];

async function abonnementActif(
  supabase: Awaited<ReturnType<typeof createClient>>,
  userId: string
): Promise<boolean> {
  const { data } = await supabase
    .from("subscriptions")
    .select("status")
    .eq("user_id", userId)
    .maybeSingle();
  return !!data && STATUTS_ABONNEMENT_ACTIF.includes(data.status);
}

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

  if (!(await abonnementActif(supabase, user.id))) {
    const { count } = await supabase
      .from("watchlist_items")
      .select("id", { count: "exact", head: true })
      .eq("user_id", user.id);
    if ((count ?? 0) >= LIMITE_CARTES_GRATUIT) {
      throw new Error(
        `Limite de ${LIMITE_CARTES_GRATUIT} cartes gratuites atteinte -- passe à l'abonnement pour en surveiller plus.`
      );
    }
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

export async function creerSessionCheckout() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const stripe = getStripe();
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

  // Tarif early bird (200 premiers abonnés, verrouillé à vie) : appliqué
  // automatiquement tant que le coupon Stripe a des redemptions restantes
  // (coupon.valid passe à false de lui-même une fois max_redemptions
  // atteint -- Stripe gère le comptage, pas nous). Coupon absent/erreur ->
  // tarif standard, sans jamais bloquer le checkout.
  let discounts: { coupon: string }[] | undefined;
  try {
    const coupon = await stripe.coupons.retrieve(EARLY_BIRD_COUPON_ID);
    if (coupon.valid) discounts = [{ coupon: coupon.id }];
  } catch {
    // coupon pas encore créé côté dashboard Stripe -- tarif standard
  }

  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price: process.env.STRIPE_PRICE_ID!, quantity: 1 }],
    customer_email: user.email,
    client_reference_id: user.id,
    discounts,
    success_url: `${siteUrl}/dashboard?abonnement=succes`,
    cancel_url: `${siteUrl}/dashboard?abonnement=annule`,
  });

  if (session.url) redirect(session.url);
}

export async function creerSessionPortail() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: abonnement } = await supabase
    .from("subscriptions")
    .select("stripe_customer_id")
    .eq("user_id", user.id)
    .maybeSingle();

  if (!abonnement?.stripe_customer_id) redirect("/dashboard");

  const stripe = getStripe();
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
  const session = await stripe.billingPortal.sessions.create({
    customer: abonnement.stripe_customer_id,
    return_url: `${siteUrl}/dashboard`,
  });

  redirect(session.url);
}

export async function deconnexion() {
  const supabase = await createClient();
  await supabase.auth.signOut();
  redirect("/");
}
