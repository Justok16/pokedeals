#!/usr/bin/env python3
"""Teste l'envoi du formulaire de contact AVEC la politique de sécurité (CSP) réelle du site (09/10/2026).

Usage : python3 outils/test_formulaire.py [dossier_du_site]
Ouvre index.html servi comme sur Cloudflare (en-tête CSP lu dans _headers), remplit le formulaire et l'envoie ;
la réponse de FormSubmit est simulée (aucun email ne part). Code 0 si le message de réussite s'affiche, 1 sinon.
Pourquoi : un essai sur fichier local ignore _headers ; le 09/10, la CSP « connect-src 'self' » aurait bloqué
l'envoi vers formsubmit.co le jour de l'ouverture. À lancer après outils/ouverture_site.py --ecrire.
"""

import os
import re
import sys

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(ICI, "..", "site-dig"))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


def main():
    csp = re.search(r"Content-Security-Policy: (.*)", open(os.path.join(SITE, "_headers"), encoding="utf-8").read()).group(1)
    html = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    if "disabled aria-disabled" in html:
        print("Formulaire encore fermé (site pas ouvert) : rien à tester.")
        return 0
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page()
        refus = []
        pg.on("console", lambda m: refus.append(m.text) if "Content Security Policy" in m.text else None)
        pg.route("https://dig16.fr/", lambda r: r.fulfill(status=200, body=html, headers={
            "content-type": "text/html; charset=utf-8", "content-security-policy": csp}))
        pg.route("https://formsubmit.co/**", lambda r: r.fulfill(status=200, body='{"success":"true"}', headers={
            "content-type": "application/json", "access-control-allow-origin": "*"}))
        pg.goto("https://dig16.fr/", wait_until="domcontentloaded")
        for nom, valeur in [("nom", "TEST DIG16"), ("entreprise", "Test"), ("commune", "Test"), ("contact", "0600000000")]:
            pg.fill(f"#form [name={nom}]", valeur)
        pg.click("#form button[type=submit]")
        pg.wait_for_timeout(2000)
        msg = pg.locator("#msg").text_content() or ""
        nav.close()
    ok = msg.startswith("Merci")
    print("Formulaire :", "OK" if ok else "ALERTE", "|", msg, "|", refus[0][:120] if refus else "aucun refus CSP")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
