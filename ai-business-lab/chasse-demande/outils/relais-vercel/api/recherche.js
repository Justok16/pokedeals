// Recherche web (Perplexity « sonar ») via Vercel AI Gateway, authentifiée par
// OIDC : retrouve le site officiel d'une entreprise à partir de son nom et de
// sa commune. Les adresses trouvées sont ensuite vérifiées une par une.
import { generateText } from 'ai';

// Seules les adresses protégées par Vercel Authentication (…-justok1.vercel.app)
// sont acceptées ; l'adresse de production publique est refusée.
function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const p = new URL(request.url).searchParams;
  const nom = (p.get('nom') || '').slice(0, 120);
  const lieu = (p.get('lieu') || '').slice(0, 120);
  const activite = (p.get('activite') || '').slice(0, 120);
  if (!nom || !lieu) return Response.json({ erreur: 'nom et lieu requis' }, { status: 400 });
  const consigne =
    `Entreprise française : « ${nom} », activité « ${activite} », située à ${lieu}. ` +
    "Quel est son site internet officiel (son propre site, pas un annuaire, pas Facebook, " +
    "pas PagesJaunes, pas une plateforme de réservation) ? Réponds uniquement en JSON : " +
    '{"site": "adresse ou null", "facebook": "adresse ou null", "autres": ["autres pages propres à l\'entreprise"], ' +
    '"certitude": "haute|moyenne|faible"}. N\'invente rien : null si tu ne trouves pas.';
  try {
    const r = await generateText({ model: 'perplexity/sonar', prompt: consigne });
    return Response.json({ nom, lieu, reponse: r.text, sources: r.sources, usage: r.usage });
  } catch (e) {
    return Response.json({ nom, erreur: String(e && e.message || e).slice(0, 500) }, { status: 502 });
  }
}
