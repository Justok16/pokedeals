// Interroge l'index public Common Crawl (archive ouverte du web), inaccessible
// depuis les conteneurs de Claude Code. Sert à lister les sous-domaines publics
// d'un domaine (ex. *.site-solocal.com). Lecture seule, domaine d'arrivée fixe.

// Seules les adresses protégées par Vercel Authentication (…-justok1.vercel.app)
// sont acceptées ; l'adresse de production publique est refusée.
function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const p = new URL(request.url).searchParams;
  const chemin = p.get('chemin') || '';
  // Soit la liste des collections, soit une requête d'index CDX.
  let cible;
  if (chemin === 'collinfo') {
    cible = 'https://index.commoncrawl.org/collinfo.json';
  } else if (chemin === 'wayback') {
    // Index public de la Wayback Machine (archive.org), même principe.
    const q = new URLSearchParams();
    for (const cle of ['url', 'output', 'fl', 'page', 'showNumPages', 'filter', 'collapse', 'limit', 'from', 'to']) {
      if (p.get(cle) !== null) q.set(cle, p.get(cle));
    }
    cible = `https://web.archive.org/cdx/search/cdx?${q}`;
  } else if (/^CC-MAIN-\d{4}-\d{2}-index$/.test(chemin)) {
    const q = new URLSearchParams();
    for (const cle of ['url', 'output', 'fl', 'page', 'showNumPages', 'filter', 'collapse']) {
      if (p.get(cle) !== null) q.set(cle, p.get(cle));
    }
    cible = `https://index.commoncrawl.org/${chemin}?${q}`;
  } else {
    return Response.json({ erreur: 'chemin invalide' }, { status: 400 });
  }
  const r = await fetch(cible, { headers: { 'User-Agent': 'relais-dig (etude de marche)' } });
  return new Response(await r.text(), {
    status: r.status,
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
