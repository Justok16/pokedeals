// Liste toutes les vidéos publiques d'une chaîne YouTube (identifiant, titre,
// durée), depuis Vercel car YouTube bloque les conteneurs cloud de Claude Code.
// Paramètre ?chaine=@nom. Pages suivantes via l'API interne « browse » de YouTube.

function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

const UA = { 'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'fr-FR,fr;q=0.9' };

function extraire(obj, videos, suite) {
  if (Array.isArray(obj)) { obj.forEach((x) => extraire(x, videos, suite)); return; }
  if (!obj || typeof obj !== 'object') return;
  const v = obj.playlistVideoRenderer || obj.videoRenderer;
  if (v && v.videoId) {
    const titre = (v.title && (v.title.simpleText || (v.title.runs || []).map((r) => r.text).join(''))) || '';
    const duree = (v.lengthText && (v.lengthText.simpleText || (v.lengthText.runs || []).map((r) => r.text).join(''))) || v.lengthSeconds || '';
    videos.push({ id: v.videoId, titre, duree });
  }
  if (obj.continuationCommand && obj.continuationCommand.token) suite.push(obj.continuationCommand.token);
  for (const x of Object.values(obj)) extraire(x, videos, suite);
}

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  const chaine = new URL(request.url).searchParams.get('chaine') || '';
  if (!/^@[A-Za-z0-9._-]{2,60}$/.test(chaine)) return Response.json({ erreur: 'chaîne invalide' }, { status: 400 });
  const page = await (await fetch(`https://www.youtube.com/${chaine}/videos?hl=fr`, { headers: UA })).text();
  const idChaine = (page.match(/"externalId":"(UC[A-Za-z0-9_-]{22})"/) || [])[1];
  const cleApi = (page.match(/"INNERTUBE_API_KEY":"([^"]+)"/) || [])[1];
  const version = (page.match(/"INNERTUBE_CLIENT_VERSION":"([^"]+)"/) || [])[1] || '2.20260901.00.00';
  if (!idChaine) return Response.json({ erreur: 'identifiant de chaîne introuvable', debut: page.slice(0, 300) }, { status: 502 });
  const liste = 'UU' + idChaine.slice(2);
  const html = await (await fetch(`https://www.youtube.com/playlist?list=${liste}&hl=fr`, { headers: UA })).text();
  const m = html.match(/var ytInitialData = (\{.*?\});<\/script>/s);
  const videos = []; let suite = [];
  if (m) extraire(JSON.parse(m[1]), videos, suite);
  let tours = 0;
  while (suite.length && tours < 60 && cleApi) {
    const jeton = suite.shift(); tours++;
    const r = await fetch(`https://www.youtube.com/youtubei/v1/browse?key=${cleApi}&prettyPrint=false`, {
      method: 'POST', headers: { ...UA, 'Content-Type': 'application/json' },
      body: JSON.stringify({ context: { client: { clientName: 'WEB', clientVersion: version, hl: 'fr' } }, continuation: jeton }),
    });
    const j = await r.json(); const nouvelles = [];
    extraire(j, videos, nouvelles); suite = nouvelles;
  }
  const vus = new Set(); const uniques = videos.filter((v) => !vus.has(v.id) && vus.add(v.id));
  return Response.json({ chaine, idChaine, nombre: uniques.length, pages: tours + 1, videos: uniques });
}
