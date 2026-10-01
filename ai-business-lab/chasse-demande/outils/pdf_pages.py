#!/usr/bin/env python3
"""Génère le PDF d'un support à pages A4 fixes et vérifie qu'aucune page ne déborde.

Usage : python3 outils/pdf_pages.py supports/guide-prospection.html supports/Dig-Guide-prospection.pdf

Contrôle (ajouté le 01/10/2026 après un débordement invisible au contrôle pymupdf) :
dans chaque <section class="page">, le bas de chaque bloc de contenu doit rester au-dessus
du haut du pied de page (.pied), et la section ne doit pas dépasser sa hauteur.
Code de sortie 1 si une page déborde (le PDF n'est alors pas écrit).
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

MESURE = """() => [...document.querySelectorAll('section.page')].map((s, i) => {
  const pied = s.querySelector('.pied');
  const r = s.getBoundingClientRect();
  const limite = pied ? pied.getBoundingClientRect().top - 1 : r.bottom;
  let pire = 0, quoi = '';
  for (const el of s.querySelectorAll('*')) {
    if (pied && (el === pied || pied.contains(el))) continue;
    const b = el.getBoundingClientRect();
    if (b.height === 0) continue;
    if (b.bottom - limite > pire) { pire = b.bottom - limite; quoi = (el.innerText || el.tagName).slice(0, 60); }
  }
  return {page: i + 1, depasse_px: Math.round(pire), quoi, scroll: s.scrollHeight - s.clientHeight};
})"""


def main(html, pdf):
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page()
        pg.goto('file://' + __import__('os').path.abspath(html))
        pg.emulate_media(media='print')
        pg.wait_for_timeout(500)
        res = pg.evaluate(MESURE)
        fautes = [r for r in res if r['depasse_px'] > 0 or r['scroll'] > 1]
        for r in fautes:
            print(f"Page {r['page']} déborde de {r['depasse_px']} px (scroll {r['scroll']}) : {r['quoi']!r}")
        if fautes:
            nav.close()
            return 1
        pg.pdf(path=pdf, format='A4', print_background=True, prefer_css_page_size=True)
        nav.close()
    print(f'{len(res)} pages, aucun débordement. PDF écrit : {pdf}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
