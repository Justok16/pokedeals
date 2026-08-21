import { createClient as createSupabaseClient } from "@supabase/supabase-js";

// Client Supabase avec la cle service_role -- contourne RLS, cote SERVEUR
// uniquement (jamais exposee au navigateur). Utilise UNIQUEMENT par le
// webhook Stripe (app/api/webhooks/stripe/route.ts) pour ecrire l'etat
// d'abonnement, qu'aucun utilisateur ne doit pouvoir modifier lui-meme.
export function createAdminClient() {
  return createSupabaseClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!,
    { auth: { autoRefreshToken: false, persistSession: false } }
  );
}
