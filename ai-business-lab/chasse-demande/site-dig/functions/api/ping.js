// Essai minimal des Cloudflare Pages Functions (09/10/2026) : vérifie que le dossier functions/ est déployé.
export function onRequestGet() {
  return new Response(JSON.stringify({ ok: true }), { headers: { "content-type": "application/json" } });
}
