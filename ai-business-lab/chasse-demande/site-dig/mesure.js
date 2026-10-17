// Mesure d'audience DIG16 (12/10/2026) : compteur Metricool, sans cookie et sans rien enregistrer sur l'appareil.
// Reprend à l'identique le code officiel (tracker.metricool.com/resources/be.js, lu le 12/10/2026) sans charger
// de script extérieur : seule une image de comptage est demandée à Metricool (adresse de la page, taille de la
// fenêtre, page de provenance). Identifiant public de la marque Metricool DIG16 (visible par tous, ce n'est pas un secret).
(function () {
  var a = { hash: "2d5eb2c5c56ba106d82441aa7d253243" }; // pragma: allowlist secret
  a.u = document.location.href;
  a.bw = window.innerWidth;
  a.bh = window.innerHeight;
  if (document.referrer && document.referrer !== "") a.ref = document.referrer;
  var b = [];
  for (var c in a) if (Object.prototype.hasOwnProperty.call(a, c)) b.push(encodeURIComponent(c) + "=" + encodeURIComponent(a[c]));
  new Image().src = "https://tracker.metricool.com/c3po.jpg?" + b.join("&");
})();
