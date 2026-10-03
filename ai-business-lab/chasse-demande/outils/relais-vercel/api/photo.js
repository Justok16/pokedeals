// Récupère une photo ou une page de banque d'images libres de droits, depuis Vercel,
// car ces sites bloquent les conteneurs cloud de Claude Code. Hôtes autorisés
// uniquement (liste ci-dessous). Paramètre ?url=https://…

function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

const HOTES = ['stocksnap.io', 'cdn.stocksnap.io', 'unsplash.com', 'images.unsplash.com', 'www.pexels.com', 'images.pexels.com'];

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const cible = new URL(request.url).searchParams.get('url') || '';
  let u;
  try { u = new URL(cible); } catch { return new Response('Adresse invalide', { status: 400 }); }
  if (u.protocol !== 'https:' || !HOTES.includes(u.hostname)) return new Response('Hôte non autorisé', { status: 400 });
  const r = await fetch(u, {
    headers: { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36', 'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8' },
    redirect: 'follow',
  });
  return new Response(r.body, {
    status: r.status,
    headers: { 'Content-Type': r.headers.get('content-type') || 'application/octet-stream', 'X-Adresse-Finale': r.url },
  });
}
