// Alerte « nouveau message » (13/11/2026, demande de l'utilisateur : « oui alerte »).
// Répond seulement par le numéro du dernier message non lu et non douteux (0 s'il n'y en a pas). Aucune donnée du
// message ne sort d'ici : ni nom, ni contact, ni texte. Lu toutes les 10 minutes environ par le contrôle GitHub
// « Alerte message DIG16 », qui ouvre une issue ; GitHub prévient alors l'utilisateur par mail.
// Un message douteux (étiquette « [À VÉRIFIER », voir contact.js) ne déclenche pas d'alerte : Claude le lit au point suivant.

function reponse(corps, statut = 200) {
  return new Response(JSON.stringify(corps), {
    status: statut,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex" },
  });
}

export async function onRequestGet({ env }) {
  if (!env || !env.DB) return reponse({ dernier: 0, erreur: "service indisponible" }, 503);
  const r = await env.DB.prepare(
    "SELECT COALESCE(MAX(id), 0) AS dernier FROM messages WHERE lu = 0 AND message NOT LIKE '[À VÉRIFIER%'",
  ).first();
  return reponse({ dernier: Number((r && r.dernier) || 0) });
}

export function onRequest() {
  return reponse({ erreur: "méthode non autorisée" }, 405);
}
