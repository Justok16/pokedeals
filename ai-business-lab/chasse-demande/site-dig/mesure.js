// Mesure d'audience DIG16 (12/10/2026) : compteur Metricool, sans cookie et sans rien enregistrer sur l'appareil.
// Reprend à l'identique le code officiel (tracker.metricool.com/resources/be.js, lu le 12/10/2026) sans charger
// de script extérieur : seule une image de comptage est demandée à Metricool (adresse de la page, taille de la
// fenêtre, page de provenance). Identifiant public de la marque Metricool DIG16 (visible par tous, ce n'est pas un secret).
//
// Audit de la campagne du 19/10/2026 :
// - nos propres contrôles automatiques (Playwright : navigator.webdriver) ne sont plus comptés : ils gonflaient les
//   chiffres (pic de 290 pages vues le 15/10, jour de l'audit du site) ;
// - les deux gestes qui comptent sont comptés comme des pages virtuelles, visibles dans le rapport « pages » :
//   /_appel (appui sur un bouton « Appeler »), /_email (clic sur l'adresse), /_demande-envoyee (formulaire envoyé) ;
// - la provenance passée dans l'adresse (?de=ig, ?de=tt… posée par les liens courts de _redirects) reste dans
//   l'adresse comptée : on sait enfin d'où vient chaque visite, même depuis les applis qui cachent la provenance.
(function () {
  if (navigator.webdriver) return; // contrôles automatiques de DIG16 : pas des visiteurs
  var hash = "2d5eb2c5c56ba106d82441aa7d253243"; // pragma: allowlist secret
  function compter(page) {
    var a = { hash: hash };
    a.u = page ? document.location.origin + page + document.location.search : document.location.href;
    a.bw = window.innerWidth;
    a.bh = window.innerHeight;
    if (document.referrer && document.referrer !== "") a.ref = document.referrer;
    var b = [];
    for (var c in a) if (Object.prototype.hasOwnProperty.call(a, c)) b.push(encodeURIComponent(c) + "=" + encodeURIComponent(a[c]));
    new Image().src = "https://tracker.metricool.com/c3po.jpg?" + b.join("&");
  }
  compter();
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var h = a.getAttribute("href") || "";
    if (h.indexOf("tel:") === 0) compter("/_appel");
    else if (h.indexOf("mailto:") === 0) compter("/_email");
  }, true);
  var msg = document.getElementById("msg");
  if (msg && window.MutationObserver) {
    new MutationObserver(function () {
      if (/^Merci/.test(msg.textContent)) compter("/_demande-envoyee");
    }).observe(msg, { childList: true, characterData: true, subtree: true });
  }
})();
