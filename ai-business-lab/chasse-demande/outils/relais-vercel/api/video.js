// Résume une vidéo YouTube avec Gemini.
// 1) Si la variable d'environnement GEMINI_API_KEY existe (clé gratuite Google AI Studio,
//    saisie par l'utilisateur dans les réglages Vercel, jamais dans le dépôt) : appel direct
//    à l'API Gemini (offre gratuite : 8 h de vidéo YouTube par jour).
// 2) Sinon : Vercel AI Gateway (jeton OIDC, crédit gratuit mensuel).
// Déploiement protégé (Vercel Authentication) : appel via le connecteur Vercel.
import { generateText } from 'ai';

const CONSIGNES = {};
CONSIGNES.finance =
  "Résume cette vidéo en français, comme une fiche de connaissances en finances personnelles. Donne : " +
  "1) le sujet et la thèse principale ; 2) les notions expliquées (définitions simples) ; 3) les chiffres, " +
  "taux, plafonds et règles fiscales cités, avec l'année ou la date si elle est dite (marque « à vérifier " +
  "à la source officielle » pour toute règle fiscale ou légale) ; 4) les conseils concrets et leurs limites " +
  "ou risques ; 5) les produits, applications ou entreprises cités, en signalant s'il s'agit de publicité " +
  "ou de produits de l'auteur. N'invente rien : si un détail n'est pas clair, écris « non précisé ».";
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
  const mode = new URL(request.url).searchParams.get('mode') || '';
  const consigne = CONSIGNES[mode] || CONSIGNE;
  const debug = new URL(request.url).searchParams.get('debug') === '1';
  const cle = process.env.GEMINI_API_KEY;
  if (cle) {
    const url = `https://www.youtube.com/watch?v=${id}`;
    const erreurs = [];
    // API « interactions » (documentation Google, septembre 2026)
    for (const modele of [process.env.GEMINI_MODEL, 'gemini-3.8-flash', 'gemini-2.5-flash'].filter(Boolean)) {
      try {
        const rep = await fetch('https://generativelanguage.googleapis.com/v1beta/interactions', {
          method: 'POST',
          headers: { 'x-goog-api-key': cle, 'Content-Type': 'application/json' },
          body: JSON.stringify({ model: modele, input: [{ type: 'text', text: consigne }, { type: 'video', uri: url }] }),
        });
        const j = await rep.json();
        // Le texte peut être dans output_text ou dans outputs[] (objets imbriqués) : on le cherche partout.
        const morceaux = [];
        const parcourir = (v, cle) => {
          if (typeof v === 'string') { if (cle === 'text' || cle === 'output_text') morceaux.push(v); }
          else if (Array.isArray(v)) v.forEach((x) => parcourir(x, cle));
          else if (v && typeof v === 'object') {
            if (/thought|reason|user|input/i.test(String(v.type || '') + String(v.role || ''))) return; // ni la réflexion interne ni la consigne
            for (const [k, x] of Object.entries(v)) if (!['input', 'usage', 'signature'].includes(k)) parcourir(x, k);
          }
        };
        parcourir({ output_text: j.output_text, outputs: j.outputs, output: j.output, steps: j.steps }, '');
        const texte = [...new Set(morceaux)].join('\n').trim();
        if (rep.ok && texte) return Response.json({ id, resume: texte, modele, voie: 'interactions' });
        if (debug) { const { usage, ...reste } = j; return Response.json({ id, debug: JSON.stringify(reste, (k, v) => (k === 'signature' ? '…' : v)).slice(0, 4000) }); }
        erreurs.push(`${modele} interactions ${rep.status} ${JSON.stringify(j).slice(0, 200)}`);
      } catch (e) { erreurs.push(`${modele} interactions ${String(e).slice(0, 120)}`); }
      // API classique generateContent
      try {
        const rep = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modele}:generateContent`, {
          method: 'POST',
          headers: { 'x-goog-api-key': cle, 'Content-Type': 'application/json' },
          body: JSON.stringify({ contents: [{ parts: [{ file_data: { file_uri: url } }, { text: consigne }] }] }),
        });
        const j = await rep.json();
        const texte = ((j.candidates || [])[0]?.content?.parts || []).map(p => p.text || '').join('').trim();
        if (rep.ok && texte) return Response.json({ id, resume: texte, modele, voie: 'generateContent' });
        erreurs.push(`${modele} generateContent ${rep.status} ${JSON.stringify(j).slice(0, 200)}`);
      } catch (e) { erreurs.push(`${modele} generateContent ${String(e).slice(0, 120)}`); }
    }
    return Response.json({ id, erreur: erreurs.join(' | ').slice(0, 1500) }, { status: 502 });
  }
  try {
    const r = await generateText({
      model: 'google/gemini-2.5-flash',
      messages: [{
        role: 'user',
        content: [
          { type: 'file', data: new URL(`https://www.youtube.com/watch?v=${id}`), mediaType: 'video/mp4' },
          { type: 'text', text: consigne },
        ],
      }],
    });
    return Response.json({ id, resume: r.text, usage: r.usage });
  } catch (e) {
    return Response.json({ id, erreur: String(e && e.message || e).slice(0, 500) }, { status: 502 });
  }
}
