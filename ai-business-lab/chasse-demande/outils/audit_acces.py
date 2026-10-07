"""Audit d'accessibilité et d'ergonomie d'une page (inspiré de la grille « audit » du skill
Impeccable, pbakaus/impeccable, licence Apache-2.0 — règles reprises, aucun programme tiers lancé).

Usage : python3 audit_acces.py page.html|https://site/page [page2 …]
Contrôles (téléphone 390 px et ordinateur 1440 px) :
- cibles tactiles (liens, boutons, champs) d'au moins 44 × 44 px sur téléphone ;
- images sans attribut alt (alt="" accepté pour une image décorative) ;
- champs de formulaire sans étiquette (un simple texte indicatif ne suffit pas) ;
- titres qui sautent un niveau (h1 → h3) ou page sans h1 unique ;
- attribut lang absent ; animations sans variante « prefers-reduced-motion ».
Ajouts du 30/09/2026 (Web Interface Guidelines de Vercel, vercel.com/design/guidelines, lue le 30/09) :
- zoom bloqué (user-scalable=no ou maximum-scale=1) ; champs en police < 16 px sur téléphone (zoom iOS) ;
- « transition: all » ; images sans largeur/hauteur (décalage à l'affichage) ; meta theme-color absente ;
- bouton ou lien à icône seule sans nom accessible ; « ... » au lieu de « … » ; navigation faite
  avec onclick sur un div ou un bouton au lieu d'un vrai lien.
"""

import os
import sys
from playwright.sync_api import sync_playwright

JS = """() => {
  const pb = [];
  const w = innerWidth;
  if (!document.documentElement.lang) pb.push('lang absent sur <html>');
  const h1 = document.querySelectorAll('h1').length;
  if (h1 !== 1) pb.push(`${h1} titre(s) h1 (il en faut un seul)`);
  let prec = 0;
  document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
    const n = +h.tagName[1];
    if (prec && n > prec + 1) pb.push(`titre ${h.tagName} après h${prec} : « ${h.textContent.trim().slice(0, 40)} »`);
    prec = n;
  });
  document.querySelectorAll('img').forEach(i => { if (!i.hasAttribute('alt')) pb.push('image sans alt : ' + (i.src || '').slice(-40)); });
  document.querySelectorAll('input,textarea,select').forEach(c => {
    if (c.type === 'hidden') return;
    const lab = (c.id && document.querySelector(`label[for="${c.id}"]`)) || c.closest('label') || c.getAttribute('aria-label') || c.getAttribute('aria-labelledby');
    if (!lab) pb.push(`champ sans étiquette (${c.getAttribute('placeholder') || c.name || c.tagName})`);
  });
  if (w < 700) {
    document.querySelectorAll('a,button,input,textarea,select').forEach(e => {
      const r = e.getBoundingClientRect();
      if (!r.width || !r.height || getComputedStyle(e).visibility === 'hidden') return;
      if (r.width < 44 || r.height < 44) {
        // lien dans un paragraphe : toléré (norme WCAG 2.5.8, exception « en ligne »)
        if (e.tagName === 'A' && getComputedStyle(e).display === 'inline' && e.closest('p,li')) return;
        pb.push(`cible tactile ${Math.round(r.width)}×${Math.round(r.height)} px : « ${(e.textContent || e.getAttribute('placeholder') || e.tagName).trim().slice(0, 30)} »`);
      }
    });
  }
  const vp = (document.querySelector('meta[name=viewport]') || {}).content || '';
  if (/user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b/.test(vp)) pb.push('zoom du navigateur bloqué (viewport)');
  if (!document.querySelector('meta[name=theme-color]')) pb.push('meta theme-color absente');
  if (w < 700) document.querySelectorAll('input,textarea,select').forEach(c => {
    if (c.type !== 'hidden' && parseFloat(getComputedStyle(c).fontSize) < 16) pb.push(`champ en police < 16 px (zoom iOS) : ${c.name || c.id || c.tagName}`);
  });
  document.querySelectorAll('img').forEach(i => {
    if (!(i.getAttribute('width') && i.getAttribute('height')) && !getComputedStyle(i).aspectRatio.includes('/')) pb.push('image sans largeur/hauteur : ' + (i.src || '').slice(-40));
  });
  document.querySelectorAll('a,button').forEach(e => {
    const nom = (e.textContent || '').trim() || e.getAttribute('aria-label') || e.getAttribute('title') || [...e.querySelectorAll('img')].map(i => i.alt).join('');
    if (!nom) pb.push(`${e.tagName.toLowerCase()} sans nom accessible (icône seule ?)`);
  });
  document.querySelectorAll('div[onclick],span[onclick],button[onclick]').forEach(e => {
    if (/location|href/.test(e.getAttribute('onclick'))) pb.push("navigation par onclick au lieu d’un lien : " + e.tagName.toLowerCase());
  });
  if (/\.\.\./.test(document.body.innerText)) pb.push('« ... » au lieu de « … »');
  const css = [...document.styleSheets].map(s => { try { return [...s.cssRules].map(r => r.cssText).join(' '); } catch (e) { return ''; } }).join(' ');
  if (/animation|transition/.test(css) && !/prefers-reduced-motion/.test(css)) pb.push('animations sans variante prefers-reduced-motion');
  if (/transition:\s*all\b/.test(css)) pb.push('« transition: all » (lister les propriétés animées)');
  return [...new Set(pb)];
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    total = 0
    for f in sys.argv[1:]:
        for w in (390, 1440):
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto(
                f
                if f.startswith(("https://", "http://"))
                else "file://" + os.path.abspath(f)
            )
            pg.wait_for_timeout(800)  # page en ligne acceptée (01/10)
            pb = pg.evaluate(JS)
            pg.close()
            total += len(pb)
            for x in pb:
                print(f"{f} {w}px : {x}")
    b.close()
    print("problèmes :", total)
