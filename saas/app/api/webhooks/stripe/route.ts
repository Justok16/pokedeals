import { NextResponse } from "next/server";
import type Stripe from "stripe";
import { createAdminClient } from "@/lib/supabase/admin";
import { getStripe } from "@/lib/stripe";

// Route webhook Stripe -- reçoit les événements d'abonnement (paiement
// réussi, renouvellement, annulation...) et met à jour la table
// `subscriptions` en conséquence. Seul point d'écriture de cette table
// (cf. migration 0004_subscriptions.sql, RLS lecture seule côté client).

async function synchroniserDepuisAbonnement(
  admin: ReturnType<typeof createAdminClient>,
  subscription: Stripe.Subscription
) {
  const customerId =
    typeof subscription.customer === "string" ? subscription.customer : subscription.customer.id;
  const item = subscription.items.data[0];

  await admin
    .from("subscriptions")
    .update({
      stripe_subscription_id: subscription.id,
      status: subscription.status,
      price_id: item?.price.id ?? null,
      current_period_end: item?.current_period_end
        ? new Date(item.current_period_end * 1000).toISOString()
        : null,
      updated_at: new Date().toISOString(),
    })
    .eq("stripe_customer_id", customerId);
}

export async function POST(request: Request) {
  const body = await request.text();
  const signature = request.headers.get("stripe-signature");

  if (!signature) {
    return NextResponse.json({ error: "Signature manquante" }, { status: 400 });
  }

  const stripe = getStripe();

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Signature invalide";
    return NextResponse.json({ error: message }, { status: 400 });
  }

  const admin = createAdminClient();

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object as Stripe.Checkout.Session;
      const userId = session.client_reference_id;
      const customerId =
        typeof session.customer === "string" ? session.customer : session.customer?.id;
      const subscriptionId =
        typeof session.subscription === "string" ? session.subscription : session.subscription?.id;

      if (userId && customerId) {
        await admin.from("subscriptions").upsert(
          {
            user_id: userId,
            stripe_customer_id: customerId,
            stripe_subscription_id: subscriptionId ?? null,
            status: "active",
            updated_at: new Date().toISOString(),
          },
          { onConflict: "user_id" }
        );
      }
      break;
    }

    case "customer.subscription.updated":
    case "customer.subscription.deleted": {
      const subscription = event.data.object as Stripe.Subscription;
      await synchroniserDepuisAbonnement(admin, subscription);
      break;
    }

    default:
      // Evenement non geré, ignoré volontairement -- pas une erreur.
      break;
  }

  return NextResponse.json({ received: true });
}
