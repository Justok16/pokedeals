// Une seule adresse pour le site (18/10/2026, audit référencement) : www.dig16.fr répondait en 200 sans redirection,
// soit deux copies du même site pour Google (et la fiche Google pointait vers www). Le fichier _redirects de
// Cloudflare Pages ne sait pas rediriger un domaine entier (« Domain-level redirects : non pris en charge »,
// developers.cloudflare.com/pages/configuration/redirects, lu le 18/10/2026) : on le fait ici, en une ligne.
export async function onRequest({ request, next }) {
  const u = new URL(request.url);
  if (u.hostname === "www.dig16.fr") {
    u.hostname = "dig16.fr";
    return Response.redirect(u.toString(), 301);
  }
  return next();
}
