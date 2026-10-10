// Recherche une entreprise dans l'annuaire officiel (recherche-entreprises.api.gouv.fr),
// depuis Vercel car ce service bloque les conteneurs cloud de Claude Code.
// Paramètres transmis tels quels : q, departement, code_postal, per_page, page.
// Sert à vérifier un prospect ou un client avant signature (entreprise active ?).

function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

const PERMIS = ['q', 'departement', 'code_postal', 'per_page', 'page', 'etat_administratif'];

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const entree = new URL(request.url).searchParams;
  const sortie = new URLSearchParams();
  for (const k of PERMIS) if (entree.get(k)) sortie.set(k, entree.get(k));
  if (!sortie.get('q')) return new Response(JSON.stringify({ erreur: 'paramètre q manquant' }), { status: 400 });
  const r = await fetch('https://recherche-entreprises.api.gouv.fr/search?' + sortie, {
    headers: { 'User-Agent': 'relais-dig (verification prospects)', Accept: 'application/json' },
  });
  return new Response(await r.text(), { status: r.status, headers: { 'Content-Type': 'application/json' } });
}
