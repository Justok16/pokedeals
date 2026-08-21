import Stripe from "stripe";

// Client Stripe, cote SERVEUR uniquement (STRIPE_SECRET_KEY n'est jamais
// prefixee NEXT_PUBLIC_, jamais exposee au navigateur). Instanciation
// PARESSEUSE (pas un `export const` evalue au chargement du module) --
// Next.js collecte la config des Route Handlers (app/api/**) au BUILD, un
// throw immediat dans le constructeur Stripe (cf. `new Stripe(undefined)`)
// casserait `next build` meme sans jamais servir la route. Meme piege que
// les clients Supabase (cf. lib/supabase/*.ts), qui sont deja des fonctions
// pour la meme raison.
export function getStripe() {
  return new Stripe(process.env.STRIPE_SECRET_KEY!);
}

// Niveau gratuit : nombre de cartes surveillables sans abonnement actif.
export const LIMITE_CARTES_GRATUIT = 10;

// Tarif early bird verrouille a vie pour les 200 premiers abonnes -- coupon
// Stripe avec max_redemptions=200 (cf. saas/README.md pour la creation).
// Applique automatiquement au checkout tant qu'il reste des redemptions.
export const EARLY_BIRD_COUPON_ID = "early-bird-200";
