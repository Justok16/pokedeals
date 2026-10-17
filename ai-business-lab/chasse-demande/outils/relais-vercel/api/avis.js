// Second avis gratuit par Gemini (clé gratuite GEMINI_API_KEY, réglages Vercel, jamais dans le dépôt).
// Deux usages :
// 1) relecture critique « en lecture seule » d'un document avant envoi (idée des vidéos
//    ucer2chlfM8 et _9ZGlLWr6UE : faire chercher les failles par un autre modèle) ;
// 2) lecture d'une courte vidéo ou d'un audio envoyé en base64 (reels Facebook, etc.).
// Appel : POST JSON { texte, consigne?, media_base64?, media_type?, modeles? } avec le cookie
// de partage Vercel (curl -b). Limite Vercel : corps de 4,5 Mo.
const CONSIGNE_CRITIQUE =
  "Tu es un relecteur exigeant et indépendant. Lecture seule : ne réécris pas le document. " +
  "Trouve tous les angles morts, erreurs de fait, incohérences de chiffres, promesses risquées " +
  "juridiquement (droit français), fautes d'orthographe et passages peu clairs pour un artisan " +
  "de 50 ans. Pour chaque point : citation exacte, problème, correction proposée, gravité " +
  "(haute, moyenne, basse). N'invente rien ; si tu n'es pas sûr, écris « à vérifier ». Réponds en français.";

function adresseProtegee(request) {
  return new URL(request.url).hostname.endsWith('-justok1.vercel.app');
}

export async function POST(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const cle = process.env.GEMINI_API_KEY;
  if (!cle) return Response.json({ erreur: 'clé Gemini absente' }, { status: 500 });
  let d;
  try { d = await request.json(); } catch { return Response.json({ erreur: 'JSON invalide' }, { status: 400 }); }
  const texte = String(d.texte || '').slice(0, 200000);
  const consigne = String(d.consigne || CONSIGNE_CRITIQUE).slice(0, 4000);
  const parts = [{ text: consigne }];
  if (texte) parts.push({ text: texte });
  if (d.media_base64) {
    if (!/^(video|audio|image)\/[a-z0-9.+-]{2,20}$/.test(d.media_type || '')) {
      return Response.json({ erreur: 'media_type invalide' }, { status: 400 });
    }
    parts.push({ inline_data: { mime_type: d.media_type, data: String(d.media_base64) } });
  }
  if (parts.length < 2) return Response.json({ erreur: 'rien à lire' }, { status: 400 });
  const choisis = String(d.modeles || '').split(',').filter((m) => /^[a-z0-9.-]{3,60}$/.test(m));
  const erreurs = [];
  for (const modele of (choisis.length ? choisis : ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite'])) {
    try {
      const rep = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modele}:generateContent`, {
        method: 'POST',
        headers: { 'x-goog-api-key': cle, 'Content-Type': 'application/json' },
        body: JSON.stringify({ contents: [{ parts }] }),
      });
      const j = await rep.json();
      const sortie = ((j.candidates || [])[0]?.content?.parts || []).map((p) => p.text || '').join('').trim();
      if (rep.ok && sortie) return Response.json({ avis: sortie, modele });
      erreurs.push(`${modele} ${rep.status} ${JSON.stringify(j).slice(0, 200)}`);
    } catch (e) { erreurs.push(`${modele} ${String(e).slice(0, 120)}`); }
  }
  return Response.json({ erreur: erreurs.join(' | ').slice(0, 1500) }, { status: 502 });
}
