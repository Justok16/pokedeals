// Renvoie le texte des sous-titres d'une vidéo YouTube (sous-titres publics, souvent automatiques).
// Sert à résumer une vidéo à partir de son texte : bien moins coûteux en quota que l'analyse de la vidéo.
// Déploiement protégé (Vercel Authentication) : appel via le connecteur Vercel.

function adresseProtegee(request) {
  return new URL(request.url).hostname.endsWith('-justok1.vercel.app');
}

function decoder(s) {
  return s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n));
}

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const params = new URL(request.url).searchParams;
  const id = params.get('id') || '';
  if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return Response.json({ erreur: 'identifiant vidéo invalide' }, { status: 400 });
  const langue = /^[a-z]{2}$/.test(params.get('langue') || '') ? params.get('langue') : 'fr';
  try {
    const rep = await fetch('https://www.youtube.com/youtubei/v1/player?prettyPrint=false', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'User-Agent': 'com.google.android.youtube/20.10.38 (Linux; U; Android 14)' },
      body: JSON.stringify({ context: { client: { clientName: 'ANDROID', clientVersion: '20.10.38', hl: langue } }, videoId: id }),
    });
    const j = await rep.json();
    const pistes = j?.captions?.playerCaptionsTracklistRenderer?.captionTracks || [];
    if (!pistes.length) return Response.json({ erreur: 'aucun sous-titre', statut: j?.playabilityStatus?.status || rep.status }, { status: 404 });
    const piste = pistes.find((p) => p.languageCode === langue && p.kind !== 'asr') || pistes.find((p) => p.languageCode === langue) || pistes[0];
    const xml = await (await fetch(piste.baseUrl.replace(/&fmt=[^&]*/, ''))).text();
    const morceaux = [...xml.matchAll(/<(?:text|p)[^>]*>([\s\S]*?)<\/(?:text|p)>/g)].map((m) => decoder(m[1].replace(/<[^>]+>/g, '')).trim()).filter(Boolean);
    return Response.json({ id, langue: piste.languageCode, automatique: piste.kind === 'asr', caracteres: morceaux.join(' ').length, texte: morceaux.join(' ') });
  } catch (e) {
    return Response.json({ erreur: String(e).slice(0, 200) }, { status: 502 });
  }
}
