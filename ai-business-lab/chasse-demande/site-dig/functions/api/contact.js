// Formulaire de contact de dig16.fr (05/11/2026, décision de l'utilisateur : « on fait ça »).
// Remplace FormSubmit (Devro LABS, États-Unis), absent du registre officiel du Data Privacy Framework le 05/11/2026 :
// chaque message est rangé dans la base Cloudflare D1 « dig16-messages » (région Europe de l'Ouest). Cloudflare est
// certifié (dataprivacyframework.gov/participant/5666, lu le 05/11/2026). Aucun autre prestataire ne reçoit le message.
// Claude relit les messages non lus à chaque point (2 fois par jour) et prévient l'utilisateur.
// Aucune adresse IP n'est enregistrée. Depuis le 13/11 : messages douteux étiquetés, jamais rejetés (voir plus bas). Le champ piège « _honey » arrête les robots sans rien enregistrer.

const LIMITES = { nom: 120, entreprise: 160, commune: 120, contact: 160, site: 80, message: 3000 };
const OBLIGATOIRES = ["nom", "entreprise", "commune", "contact"];
const MAX_PAR_HEURE = 30; // garde-fou contre l'inondation de la base

// Protection du 13/11/2026 (« oui protection », à condition de ne perdre aucun message légitime) : rien n'est rejeté.
// Un message douteux est enregistré comme les autres, avec une étiquette « [À VÉRIFIER : …] » en tête du message.
// Claude relit tous les messages non lus à chaque point : il ne signale à l'utilisateur que les vrais, et un vrai
// message étiqueté par erreur (un artisan qui cite son site, par exemple) lui est transmis quand même.
const JETABLES = /@(?:[a-z0-9-]+\.)*(?:mailinator\.com|yopmail\.(?:com|fr)|guerrillamail\.[a-z]+|10minutemail\.[a-z]+|tempmail\.[a-z]+|temp-mail\.[a-z]+|trashmail\.[a-z]+|sharklasers\.com|getnada\.com|maildrop\.cc|dispostable\.com|my\.id)$/i;
const LIEN = /https?:\/\/|www\.[a-z0-9-]+\.[a-z]{2,}/i;

function doutes(v, duree) {
  const raisons = [];
  const lienAilleurs = ["nom", "entreprise", "commune", "contact", "message"].some((c) => LIEN.test(v[c]));
  if (lienAilleurs) raisons.push("contient un lien");
  if (JETABLES.test(v.contact)) raisons.push("adresse jetable");
  if (Number.isFinite(duree) && duree >= 0 && duree < 4) raisons.push("rempli en moins de 4 secondes");
  return raisons;
}

function reponse(corps, statut = 200) {
  return new Response(JSON.stringify(corps), {
    status: statut,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}

// Alerte immédiate du 13/11/2026 (« oui alerte ») : une notification part vers le téléphone de l'utilisateur par ntfy.sh
// (gratuit, 250 messages par jour, lu sur docs.ntfy.sh le 13/11/2026). Elle ne contient AUCUNE donnée du message
// (ni nom, ni contact, ni texte) : seulement « nouveau message » et son numéro. Le nom du canal est secret : il est
// rangé dans la table D1 « reglages » (clé « alerte_sujet »), jamais dans ce dépôt public. Si l'alerte échoue,
// le message reste enregistré et le visiteur voit « envoyé » : l'alerte ne peut pas faire perdre un message.
async function alerter(env, numero, douteux) {
  try {
    const r = await env.DB.prepare("SELECT valeur FROM reglages WHERE cle = 'alerte_sujet'").first();
    if (!r || !r.valeur) return;
    await fetch("https://ntfy.sh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: AbortSignal.timeout(4000),
      body: JSON.stringify({
        topic: r.valeur,
        title: douteux ? "DIG16 : message à vérifier" : "DIG16 : nouveau message du site",
        message: douteux
          ? `Message n° ${numero}, probablement indésirable. Claude le vérifie au prochain point.`
          : `Message n° ${numero} reçu par le formulaire de dig16.fr. Ouvrez la conversation DIG16 et écrivez « message » pour le lire.`,
        priority: douteux ? 2 : 4,
        tags: [douteux ? "grey_question" : "envelope_with_arrow"],
      }),
    });
  } catch {
    // jamais bloquant
  }
}

export async function onRequestPost({ request, env, waitUntil }) {
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
  const raisons = doutes(v, Number(d._duree));
  const etiquette = raisons.length ? `[À VÉRIFIER : ${raisons.join(", ")}] ` : "";
  const message = (etiquette + v.message).slice(0, LIMITES.message + 120);
  const resultat = await env.DB.prepare(
    "INSERT INTO messages (nom, entreprise, commune, contact, site, message) VALUES (?, ?, ?, ?, ?, ?)",
  )
    .bind(v.nom, v.entreprise, v.commune, v.contact, v.site, message)
    .run();
  const numero = (resultat && resultat.meta && resultat.meta.last_row_id) || "?";
  const envoi = alerter(env, numero, raisons.length > 0);
  if (typeof waitUntil === "function") waitUntil(envoi);
  else await envoi;
  return reponse({ success: "true" });
}

export function onRequest() {
  return reponse({ success: "false", erreur: "méthode non autorisée" }, 405);
}
