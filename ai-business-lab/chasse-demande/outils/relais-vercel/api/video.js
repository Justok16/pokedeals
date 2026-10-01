// Résume une vidéo YouTube avec Gemini.
// 1) Si la variable d'environnement GEMINI_API_KEY existe (clé gratuite Google AI Studio,
//    saisie par l'utilisateur dans les réglages Vercel, jamais dans le dépôt) : appel direct
//    à l'API Gemini (offre gratuite : environ 20 requêtes par jour et par modèle, constaté le 26/09).
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
  const params = new URL(request.url).searchParams;
  if (params.get('liste') === '1' && process.env.GEMINI_API_KEY) {
    // Liste des modèles disponibles pour cette clé (sans la clé dans la réponse)
    const r = await fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', { headers: { 'x-goog-api-key': process.env.GEMINI_API_KEY } });
    const j = await r.json();
    return Response.json((j.models || []).map((m) => ({ nom: m.name, methodes: m.supportedGenerationMethods })));
  }
  // Lot de vidéos (01/10) : ids=a,b,c (10 au plus, documentation Gemini « video understanding » :
  // « Gemini 2.5 and later models, you can upload a maximum of 10 videos per request »). Le quota gratuit
  // se compte en requêtes : regrouper les vidéos courtes multiplie le nombre de vidéos résumées par jour.
  const lot = (params.get('ids') || '').split(',').filter((x) => /^[A-Za-z0-9_-]{11}$/.test(x)).slice(0, 10);
  const id = lot.length ? lot[0] : (params.get('id') || '');
  if (!/^[A-Za-z0-9_-]{11}$/.test(id)) {
    return Response.json({ erreur: 'identifiant vidéo invalide' }, { status: 400 });
  }
  const mode = new URL(request.url).searchParams.get('mode') || '';
  const consigne = (CONSIGNES[mode] || CONSIGNE) + (lot.length > 1
    ? ` Tu reçois ${lot.length} vidéos distinctes, chacune précédée de son identifiant. Fais un résumé SÉPARÉ pour ` +
      'chacune, dans le même ordre, en commençant chaque résumé par une ligne seule « === VIDEO <identifiant> === ». ' +
      'Ne mélange jamais le contenu de deux vidéos.' : '');
  const debug = new URL(request.url).searchParams.get('debug') === '1';
  const cle = process.env.GEMINI_API_KEY;
  // voie=passerelle : Vercel AI Gateway, UNIQUEMENT sur le crédit gratuit mensuel offert par Vercel
  // (accord de l'utilisateur du 28/09 : « sans jamais dépasser afin de ne rien payer »).
  // Garde-fou : on lit le solde avant chaque appel et on refuse sous 1 $ de marge.
  if (params.get('voie') === 'passerelle') {
    const jeton = request.headers.get('x-vercel-oidc-token') || process.env.VERCEL_OIDC_TOKEN || process.env.AI_GATEWAY_API_KEY;
    let solde = null, statut = null;
    try {
      const rc = await fetch('https://ai-gateway.vercel.sh/v1/credits', { headers: { Authorization: `Bearer ${jeton}` } });
      statut = rc.status;
      const jc = await rc.json();
      solde = parseFloat(jc.balance);
    } catch (e) { /* solde illisible : on refuse par prudence */ }
    if (!(solde >= 1)) return Response.json({ id, erreur: `passerelle refusée : solde gratuit ${solde} $ (marge 1 $)`, solde, statut, jeton: Boolean(jeton) }, { status: 402 });
    if (params.get('solde') === '1') return Response.json({ solde });
    const modele = /^google\/[a-z0-9.-]{3,60}$/.test(params.get('modele') || '') ? params.get('modele') : 'google/gemini-3.5-flash-lite';
    try {
      const r = await generateText({
        model: modele,
        providerOptions: { google: { mediaResolution: 'MEDIA_RESOLUTION_LOW' } },
        messages: [{ role: 'user', content: [
          { type: 'file', data: new URL(`https://www.youtube.com/watch?v=${id}`), mediaType: 'video/mp4' },
          { type: 'text', text: consigne },
        ] }],
      });
      if (r.text && r.text.trim()) return Response.json({ id, resume: r.text, modele, voie: 'passerelle', solde_avant: solde, usage: r.usage });
      return Response.json({ id, erreur: `${modele} passerelle réponse vide` }, { status: 502 });
    } catch (e) {
      return Response.json({ id, erreur: `${modele} passerelle ${String(e && e.message || e).slice(0, 400)}` }, { status: 502 });
    }
  }
  if (cle) {
    const url = `https://www.youtube.com/watch?v=${id}`;
    const erreurs = [];
    // Vidéos trop longues (> ~3 h en basse résolution, limite de 1 048 576 jetons) : debut=…&fin=…
    // (en secondes) ne fait lire qu'un extrait ; on résume alors la vidéo morceau par morceau (30/09).
    const debut = params.get('debut'), fin = params.get('fin');
    const extrait = /^\d{1,6}$/.test(debut || '') && /^\d{1,6}$/.test(fin || '') && +fin > +debut
      ? { start_offset: `${+debut}s`, end_offset: `${+fin}s` } : null;
    // API « interactions » (documentation Google, septembre 2026)
    const choisis = (params.get('modeles') || '').split(',').filter((m) => /^[a-z0-9.-]{3,60}$/.test(m));
    for (const modele of (choisis.length ? choisis : [process.env.GEMINI_MODEL, 'gemini-3.8-flash', 'gemini-2.5-flash'].filter(Boolean))) {
      // 1er essai (28/09) : generateContent en BASSE résolution vidéo (environ 4 fois moins de
      // jetons par image, donc bien plus rapide quand Gemini est surchargé ; suffisant pour un résumé)
      if (params.get('resolution') !== 'normale') {
        try {
          const rep = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modele}:generateContent`, {
            method: 'POST',
            headers: { 'x-goog-api-key': cle, 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: lot.length > 1
                ? [...lot.flatMap((v) => [{ text: `Vidéo ${v} :` }, { file_data: { file_uri: `https://www.youtube.com/watch?v=${v}` } }]), { text: consigne }]
                : [{ file_data: { file_uri: url }, ...(extrait ? { video_metadata: extrait } : {}) }, { text: consigne }] }],
              generationConfig: { mediaResolution: 'MEDIA_RESOLUTION_LOW' },
            }),
          });
          const j = await rep.json();
          const texte = ((j.candidates || [])[0]?.content?.parts || []).map(p => p.text || '').join('').trim();
          if (rep.ok && texte) return Response.json({ id, ...(lot.length > 1 ? { ids: lot } : {}), resume: texte, modele, voie: 'generateContent-basse' });
          if (lot.length > 1 && rep.status !== 429) { erreurs.push(`${modele} lot ${rep.status} ${JSON.stringify(j).slice(0, 200)}`); continue; } // lot : pas d'autre API
          erreurs.push(`${modele} generateContent-basse ${rep.status} ${JSON.stringify(j).slice(0, 200)}`);
          if (rep.status === 429) continue; // quota épuisé : inutile d'essayer l'autre API
          if (params.get('voie') === 'basse') return Response.json({ id, erreur: erreurs.join(' | ') }, { status: 502 }); // diagnostic
        } catch (e) { erreurs.push(`${modele} generateContent-basse ${String(e).slice(0, 120)}`); }
      }
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
