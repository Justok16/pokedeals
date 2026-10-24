"""Version Markdown des pages publiques de dig16.fr, pour les agents IA (24/10/2026).

Pourquoi : le test gratuit de Cloudflare (isitagentready.com, vu dans la veille du 24/10) attend qu'une page demandée
avec l'en-tête « Accept: text/markdown » réponde en Markdown (« Markdown for Agents »,
developers.cloudflare.com/fundamentals/reference/markdown-for-agents, lu le 24/10). Plutôt qu'un réglage du compte
Cloudflare, on prépare ici un fichier .md par page dans site-dig/md/ ; site-dig/functions/_middleware.js le sert
seulement aux agents qui le demandent. Les visiteurs reçoivent toujours la page HTML, sans changement.

Format (le même que celui de Cloudflare) : en-tête YAML (titre, description, image), le contenu de <main> sans scripts,
styles, formulaires ni boutons, puis les données structurées JSON-LD de la page.

Usage : python3 pages_markdown.py           → régénère les fichiers
        python3 pages_markdown.py --verifier → ALERTE si un fichier n'est plus à jour (utilisé par test_pages.py)
À relancer après chaque modification d'une page publique.
"""

import json
import os
import re
import sys
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from markdownify import markdownify

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site-dig")
# Adresse publique → page source → fichier Markdown (même liste que sitemap.xml).
PAGES = {
    "/": ("index.html", "md/index.md"),
    "/prestige": ("prestige.html", "md/prestige.md"),
    "/test-du-pouce/": ("test-du-pouce/index.html", "md/test-du-pouce.md"),
    "/le-projet/": ("le-projet/index.html", "md/le-projet.md"),
    "/site-internet-artisan/": ("site-internet-artisan/index.html", "md/site-internet-artisan.md"),
    "/mentions-legales": ("mentions-legales.html", "md/mentions-legales.md"),
}
RETIRER = ["script", "style", "noscript", "template", "form", "button", "svg", "video", "audio", "iframe", "canvas",
           "dialog", "input", "select", "textarea"]


def meta(soup, *noms):
    for nom in noms:
        t = soup.find("meta", attrs={"name": nom}) or soup.find("meta", attrs={"property": nom})
        if t and t.get("content"):
            return t["content"].strip()
    return ""


def yaml(valeur):
    return json.dumps(valeur, ensure_ascii=False)  # chaîne entre guillemets, valide en YAML


def convertir(chemin_html, adresse):
    with open(chemin_html, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    titre = (soup.title.get_text(strip=True) if soup.title else "") or meta(soup, "og:title")
    description = meta(soup, "description", "og:description")
    image = meta(soup, "og:image")
    jsonld = []
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            jsonld.append(json.loads(s.string or ""))
        except ValueError:
            pass
    zone = soup.find("main") or soup.body or soup
    for t in zone.find_all(RETIRER):
        t.decompose()
    for t in zone.find_all(attrs={"aria-hidden": "true"}):
        t.decompose()
    for t in zone.find_all(attrs={"hidden": True}):
        t.decompose()
    base = "https://dig16.fr" + adresse
    for a in zone.find_all("a", href=True):
        a["href"] = urljoin(base, a["href"])  # liens en adresse complète : l'agent n'a pas la page d'origine
    for img in zone.find_all("img", src=True):
        img["src"] = urljoin(base, img["src"])
    corps = markdownify(str(zone), heading_style="ATX", bullets="-")
    corps = re.sub(r"[ \t]+\n", "\n", corps)
    corps = re.sub(r"\n{3,}", "\n\n", corps).strip()
    lignes = ["---", f"title: {yaml(titre)}"]
    if description:
        lignes.append(f"description: {yaml(description)}")
    if image:
        lignes.append(f"image: {yaml(image)}")
    lignes += [f"url: {yaml('https://dig16.fr' + adresse)}", "---", "", corps, ""]
    for bloc in jsonld:
        lignes += ["```json", json.dumps(bloc, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lignes)


def main():
    verifier = "--verifier" in sys.argv
    erreurs = 0
    for adresse, (source, cible) in PAGES.items():
        texte = convertir(os.path.join(SITE, source), adresse)
        chemin = os.path.join(SITE, cible)
        actuel = open(chemin, encoding="utf-8").read() if os.path.exists(chemin) else None
        if verifier:
            ok = actuel == texte
            erreurs += not ok
            print(("OK    " if ok else "ALERTE"), "markdown", adresse,
                  "" if ok else "pas à jour : lancer outils/pages_markdown.py")
        elif actuel != texte:
            os.makedirs(os.path.dirname(chemin), exist_ok=True)
            with open(chemin, "w", encoding="utf-8") as f:
                f.write(texte)
            print("écrit", cible, len(texte), "caractères")
    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()
