// « Le test du pouce » (09/10/2026) : analyse rapide et gratuite d'un site d'artisan, sans clé ni service tiers.
// GET /api/test-pouce?url=exemple.fr  →  JSON des constats. Lit seulement la page d'accueil publique (HTML),
// ne stocke rien, ne collecte aucune donnée personnelle. Limites : 2 Mo lus, 8 s au plus.
const AN = new Date().getFullYear();

function reponse(obj, statut = 200) {
  return new Response(JSON.stringify(obj), {
    status: statut,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

function adresseValide(brute) {
  let texte = (brute || "").trim();
  if (!texte || texte.length > 300) return null;
  if (!/^https?:\/\//i.test(texte)) texte = "https://" + texte;
  let u;
  try { u = new URL(texte); } catch { return null; }
  const hote = u.hostname.toLowerCase();
  // jamais d'adresse locale ni d'adresse IP : uniquement des noms de domaine publics
  if (!hote.includes(".") || hote === "localhost" || hote.endsWith(".local") || /^[\d.]+$/.test(hote) || hote.includes(":")) return null;
  if (u.port && !["80", "443"].includes(u.port)) return null;
  return u;
}

async function lire(rep, max) {
  const lecteur = rep.body.getReader();
  const morceaux = [];
  let total = 0;
  while (total < max) {
    const { done, value } = await lecteur.read();
    if (done) break;
    morceaux.push(value);
    total += value.length;
  }
  try { lecteur.cancel(); } catch {}
  const tout = new Uint8Array(total);
  let pos = 0;
  for (const m of morceaux) { tout.set(m.subarray(0, Math.max(0, Math.min(m.length, total - pos))), pos); pos += m.length; }
  return new TextDecoder("utf-8").decode(tout);
}

export async function onRequestGet({ request }) {
  const u = adresseValide(new URL(request.url).searchParams.get("url"));
  if (!u) return reponse({ erreur: "Adresse non valable. Exemple : monentreprise.fr" }, 400);
  const debut = Date.now();
  let rep;
  try {
    rep = await fetch(u.toString(), {
      redirect: "follow",
      headers: { "user-agent": "Mozilla/5.0 (Linux; Android 14) DIG16-TestDuPouce/1.0 (+https://dig16.fr/test-du-pouce/)" },
      signal: AbortSignal.timeout(8000),
    });
  } catch (e) {
    return reponse({ adresse: u.hostname, joignable: false, erreur: "Le site ne répond pas (ou met plus de 8 secondes)." });
  }
  const html = await lire(rep, 2_000_000);
  const duree = (Date.now() - debut) / 1000;
  const final = new URL(rep.url || u.toString());
  const bas = html.toLowerCase();
  const viewport = /<meta[^>]+name=["']?viewport["']?[^>]*width=device-width/i.test(html)
    || /<meta[^>]+content=["'][^"']*width=device-width[^"']*["'][^>]*name=["']?viewport/i.test(html);
  const tels = (bas.match(/href=["']tel:/g) || []).length;
  const annees = [...html.matchAll(/(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(\d{4})/gi)].map((m) => +m[1]).filter((a) => a > 1995 && a <= AN);
  const derniereAnnee = annees.length ? Math.max(...annees) : null;
  const titre = (html.match(/<title[^>]*>([^<]{0,140})/i) || [])[1]?.trim() || "";
  return reponse({
    adresse: final.hostname,
    joignable: rep.ok,
    statut: rep.status,
    https: final.protocol === "https:",
    adapte_telephone: viewport,
    numero_cliquable: tels > 0,
    duree_secondes: Math.round(duree * 10) / 10,
    poids_ko: Math.round(html.length / 1024),
    annee_copyright: derniereAnnee,
    titre,
  });
}
