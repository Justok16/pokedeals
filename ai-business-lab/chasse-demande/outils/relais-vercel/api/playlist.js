// Liste les vidéos d'une playlist YouTube publique (identifiants),
// lue depuis Vercel car YouTube bloque les conteneurs cloud de Claude Code.
// Les titres s'obtiennent ensuite par le flux RSS ou oEmbed de YouTube.

// Seules les adresses protégées par Vercel Authentication (…-justok1.vercel.app)
// sont acceptées ; l'adresse de production publique est refusée.
function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const liste = new URL(request.url).searchParams.get('list') || '';
  if (!/^[A-Za-z0-9_-]{10,64}$/.test(liste)) {
    return Response.json({ erreur: 'identifiant de playlist invalide' }, { status: 400 });
  }
  const r = await fetch(`https://www.youtube.com/playlist?list=${liste}&hl=fr`, {
    headers: { 'Accept-Language': 'fr-FR,fr;q=0.9', 'User-Agent': 'Mozilla/5.0' },
  });
  const html = await r.text();
  // Identifiants de vidéos dans l'ordre d'apparition (la structure de page varie).
  const vus = new Set();
  for (const m of html.matchAll(/"videoId":"([A-Za-z0-9_-]{11})"/g)) vus.add(m[1]);
  const videos = [...vus].map((id) => ({ id }));
  return Response.json({
    statut: r.status,
    taille: html.length,
    nombre: videos.length,
    videos,
    debut: videos.length ? undefined : html.slice(0, 400),
  });
}
