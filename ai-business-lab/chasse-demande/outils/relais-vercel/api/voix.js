// Voix naturelle (08/10) : synthèse vocale Gemini (modèles « tts » de l'API Gemini, clé gratuite
// GEMINI_API_KEY déjà saisie dans les réglages Vercel, jamais dans le dépôt).
// Demande de l'utilisateur : « cette voix robotique... il n'y a pas moyen d'avoir une voix suave et naturelle ? »
// Appel : /api/voix?texte=...&voix=Kore&consigne=...&modele=gemini-2.5-flash-preview-tts
// Réponse : { modele, voix, audio } où audio est du PCM 16 bits mono 24 kHz en base64.
// Même protection que les autres fonctions : seules les adresses …-justok1.vercel.app sont acceptées.

function adresseProtegee(request) {
  const hote = new URL(request.url).hostname;
  return hote.endsWith('-justok1.vercel.app');
}

const MODELES = ['gemini-2.5-flash-preview-tts', 'gemini-2.5-pro-preview-tts', 'gemini-3.1-flash-tts-preview',
  'gemini-3.8-flash-tts', 'gemini-3.8-flash-lite-tts'];

export async function GET(request) {
  if (!adresseProtegee(request)) return new Response('Accès refusé', { status: 403 });
  if (!process.env.GEMINI_API_KEY) return Response.json({ erreur: 'clé Gemini absente' }, { status: 500 });
  const p = new URL(request.url).searchParams;
  const texte = (p.get('texte') || '').slice(0, 2000);
  if (!texte) return Response.json({ erreur: 'texte vide' }, { status: 400 });
  const voix = /^[A-Za-z]{2,20}$/.test(p.get('voix') || '') ? p.get('voix') : 'Kore';
  const consigne = (p.get('consigne') || '').slice(0, 600);
  const demandes = (p.get('modeles') || p.get('modele') || MODELES[0]).split(',').filter((m) => MODELES.includes(m));
  const essais = [];
  for (const modele of demandes.length ? demandes : [MODELES[0]]) {
    const rep = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modele}:generateContent`, {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-goog-api-key': process.env.GEMINI_API_KEY },
      body: JSON.stringify({
        contents: [{ parts: [{ text: consigne ? `${consigne}\n\n${texte}` : texte }] }],
        generationConfig: {
          responseModalities: ['AUDIO'],
          speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: voix } } },
        },
      }),
    });
    const j = await rep.json().catch(() => ({}));
    const audio = j?.candidates?.[0]?.content?.parts?.find((x) => x.inlineData)?.inlineData;
    if (rep.ok && audio?.data) return Response.json({ modele, voix, mime: audio.mimeType, audio: audio.data });
    essais.push({ modele, statut: rep.status, message: (j?.error?.message || '').slice(0, 200) });
  }
  return Response.json({ erreur: 'aucun modèle n\'a répondu', essais }, { status: 502 });
}
