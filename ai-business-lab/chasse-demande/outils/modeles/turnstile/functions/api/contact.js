// Cloudflare Pages Function : vérifie le jeton Turnstile avant d'accepter la demande.
// API officielle « siteverify » (doc Cloudflare mise à jour le 22/10/2026, lue le 03/11/2026) : POST secret + response
// (+ remoteip facultatif) ; le jeton n'est valable que 5 minutes et une seule fois.
// La clé secrète vient de la variable d'environnement TURNSTILE_SECRET (jamais écrite dans le code).
export async function onRequestPost({ request, env }) {
  const donnees = await request.formData();
  const jeton = donnees.get("cf-turnstile-response");
  if (!jeton) return new Response("Vérification anti-robot manquante.", { status: 400 });

  const verif = new FormData();
  verif.append("secret", env.TURNSTILE_SECRET);
  verif.append("response", jeton);
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) verif.append("remoteip", ip);

  const reponse = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body: verif,
  });
  const resultat = await reponse.json();
  if (!resultat.success) {
    return new Response("La vérification anti-robot a échoué. Merci de réessayer.", { status: 403 });
  }
  // À compléter au premier client : transmettre nom, tel, message (service d'envoi choisi avec lui),
  // puis rediriger vers une page « demande envoyée ».
  return Response.redirect(new URL("/demande-envoyee/", request.url), 303);
}
