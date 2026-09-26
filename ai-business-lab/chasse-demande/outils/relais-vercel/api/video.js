// Résume une vidéo YouTube avec Gemini via Vercel AI Gateway.
// Authentification : jeton OIDC du déploiement (aucune clé stockée).
// Déploiement protégé (Vercel Authentication) : appel via le connecteur Vercel.
import { generateText } from 'ai';

const CONSIGNE =
  "Résume cette vidéo en français, pour quelqu'un qui cherche à gagner de l'argent " +
  "légalement avec l'IA et Claude Code. Donne : 1) l'idée principale ; 2) chaque outil, " +
  "site ou dépôt GitHub cité, avec son nom exact, s'il est gratuit ou payant, et à quoi il sert ; " +
  "3) les astuces concrètes et réutilisables ; 4) les chiffres de revenus annoncés, marqués " +
  "« affirmé par l'auteur ». N'invente rien : si un détail n'est pas clair, écris « non précisé ».";


// Seules les adresses protégées par Vercel Authentication (…-justok1.vercel.app)
// sont acceptées ; l'adresse de production publique est refusée.
function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const id = new URL(request.url).searchParams.get('id') || '';
  if (!/^[A-Za-z0-9_-]{11}$/.test(id)) {
    return Response.json({ erreur: 'identifiant vidéo invalide' }, { status: 400 });
  }
  try {
    const r = await generateText({
      model: 'google/gemini-2.5-flash',
      messages: [{
        role: 'user',
        content: [
          { type: 'file', data: new URL(`https://www.youtube.com/watch?v=${id}`), mediaType: 'video/mp4' },
          { type: 'text', text: CONSIGNE },
        ],
      }],
    });
    return Response.json({ id, resume: r.text, usage: r.usage });
  } catch (e) {
    return Response.json({ id, erreur: String(e && e.message || e).slice(0, 500) }, { status: 502 });
  }
}
