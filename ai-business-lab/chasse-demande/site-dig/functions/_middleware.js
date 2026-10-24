// Une seule adresse pour le site (18/10/2026, audit référencement) : www.dig16.fr répondait en 200 sans redirection,
// soit deux copies du même site pour Google (et la fiche Google pointait vers www). Le fichier _redirects de
// Cloudflare Pages ne sait pas rediriger un domaine entier (« Domain-level redirects : non pris en charge »,
// developers.cloudflare.com/pages/configuration/redirects, lu le 18/10/2026) : on le fait ici, en une ligne.
//
// Version Markdown pour les agents IA (24/10/2026, test isitagentready.com de Cloudflare) : un agent qui demande une
// page avec « Accept: text/markdown » reçoit le fichier préparé par outils/pages_markdown.py (site-dig/md/).
// Tout autre visiteur reçoit la page HTML comme avant. Si le fichier manque, on sert la page HTML (jamais d'erreur).
const MARKDOWN = {
  "/": "/md/index.md",
  "/index.html": "/md/index.md",
  "/prestige": "/md/prestige.md",
  "/prestige.html": "/md/prestige.md",
  "/test-du-pouce/": "/md/test-du-pouce.md",
  "/le-projet/": "/md/le-projet.md",
  "/site-internet-artisan/": "/md/site-internet-artisan.md",
  "/mentions-legales": "/md/mentions-legales.md",
  "/mentions-legales.html": "/md/mentions-legales.md",
};
const SIGNAL = "search=yes, ai-input=yes, ai-train=yes"; // même choix que robots.txt

export async function onRequest({ request, next, env }) {
  const u = new URL(request.url);
  if (u.hostname === "www.dig16.fr") {
    u.hostname = "dig16.fr";
    return Response.redirect(u.toString(), 301);
  }
  const md = MARKDOWN[u.pathname];
  if (!md) return next();
  const accept = (request.headers.get("Accept") || "").toLowerCase();
  if (request.method === "GET" && accept.includes("text/markdown") && env && env.ASSETS) {
    const fichier = await env.ASSETS.fetch(new Request(new URL(md, u.origin)));
    if (fichier.ok) {
      const texte = await fichier.text();
      return new Response(texte, {
        status: 200,
        headers: {
          "Content-Type": "text/markdown; charset=utf-8",
          "Vary": "Accept",
          "Content-Signal": SIGNAL,
          "Cache-Control": "public, max-age=0, must-revalidate",
          "X-Content-Type-Options": "nosniff",
          "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
          "Link": `<https://dig16.fr${u.pathname.replace(/(index)?\.html$/, "")}>; rel="canonical"`,
        },
      });
    }
  }
  const reponse = await next();
  const copie = new Response(reponse.body, reponse);
  copie.headers.append("Vary", "Accept");
  return copie;
}
