// Formulaire de contact de dig16.fr (05/11/2026, décision de l'utilisateur : « on fait ça »).
// Remplace FormSubmit (Devro LABS, États-Unis), absent du registre officiel du Data Privacy Framework le 05/11/2026 :
// chaque message est rangé dans la base Cloudflare D1 « dig16-messages » (région Europe de l'Ouest). Cloudflare est
// certifié (dataprivacyframework.gov/participant/5666, lu le 05/11/2026). Aucun autre prestataire ne reçoit le message.
// Claude relit les messages non lus à chaque point (2 fois par jour) et prévient l'utilisateur.
// Aucune adresse IP n'est enregistrée. Le champ piège « _honey » arrête les robots sans rien enregistrer.

const LIMITES = { nom: 120, entreprise: 160, commune: 120, contact: 160, site: 80, message: 3000 };
const OBLIGATOIRES = ["nom", "entreprise", "commune", "contact"];
const MAX_PAR_HEURE = 30; // garde-fou contre l'inondation de la base

function reponse(corps, statut = 200) {
  return new Response(JSON.stringify(corps), {
    status: statut,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}

export async function onRequestPost({ request, env }) {
  if (!env || !env.DB) return reponse({ success: "false", erreur: "service indisponible" }, 503);
  // Revue de sécurité du 05/11 : n'accepter que du JSON envoyé depuis dig16.fr. Un autre site ne peut pas poster ici
  // depuis le navigateur d'un visiteur (le type JSON impose une vérification préalable que cette fonction refuse).
  const type = (request.headers.get("Content-Type") || "").toLowerCase();
  if (!type.startsWith("application/json")) return reponse({ success: "false", erreur: "format invalide" }, 415);
  const origine = request.headers.get("Origin");
  if (origine && origine !== "https://dig16.fr") return reponse({ success: "false", erreur: "origine refusée" }, 403);
  const texte = await request.text();
  if (texte.length > 8000) return reponse({ success: "false", erreur: "message trop long" }, 413);
  let d;
  try {
    d = JSON.parse(texte);
  } catch {
    return reponse({ success: "false", erreur: "format invalide" }, 400);
  }
  if (!d || typeof d !== "object") return reponse({ success: "false", erreur: "format invalide" }, 400);
  // Robot : on répond « envoyé » sans rien garder.
  if (d._honey) return reponse({ success: "true" });
  const v = {};
  for (const [champ, max] of Object.entries(LIMITES)) {
    v[champ] = String(d[champ] ?? "").trim().slice(0, max);
  }
  if (OBLIGATOIRES.some((c) => !v[c])) return reponse({ success: "false", erreur: "champ manquant" }, 400);
  const recents = await env.DB.prepare(
    "SELECT COUNT(*) AS n FROM messages WHERE recu_le > datetime('now', '-1 hour')",
  ).first();
  if (recents && recents.n >= MAX_PAR_HEURE) return reponse({ success: "false", erreur: "réessayez plus tard" }, 429);
  await env.DB.prepare(
    "INSERT INTO messages (nom, entreprise, commune, contact, site, message) VALUES (?, ?, ?, ?, ?, ?)",
  )
    .bind(v.nom, v.entreprise, v.commune, v.contact, v.site, v.message)
    .run();
  return reponse({ success: "true" });
}

export function onRequest() {
  return reponse({ success: "false", erreur: "méthode non autorisée" }, 405);
}
