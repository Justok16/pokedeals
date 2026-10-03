// Relais vers Jev (TypeSafe AI) via Vercel AI Gateway, authentifié par OIDC.
// Corps attendu : le même JSON que l'API TypeSafe « systemone », encodé en
// base64url dans le paramètre ?q= (le connecteur Vercel ne fait que des GET).
import { getVercelOidcToken } from '@vercel/oidc';


// Seules les adresses protégées par Vercel Authentication (…-justok1.vercel.app)
// sont acceptées ; l'adresse de production publique est refusée.
function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const q = new URL(request.url).searchParams.get('q') || '';
  let corps;
  try {
    corps = JSON.parse(Buffer.from(q, 'base64url').toString('utf8'));
  } catch {
    return Response.json({ erreur: 'paramètre q invalide' }, { status: 400 });
  }
  const jeton = await getVercelOidcToken();
  const r = await fetch('https://ai-gateway.vercel.sh/typesafe/v1/systemone', {
    method: 'POST',
    headers: { Authorization: `Bearer ${jeton}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(corps),
  });
  return new Response(await r.text(), {
    status: r.status,
    headers: { 'Content-Type': 'application/json' },
  });
}
