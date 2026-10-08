#!/usr/bin/env python3
"""Campagne « Le test du pouce » (08/10/2026) : visuels à la charte DIG16 (60-charte-dig16.md).

Idée : le prospect se cherche lui-même sur son téléphone (« votre métier + votre ville ») et constate seul
où il apparaît. Aucun chiffre inventé, aucun concurrent nommé, entreprises des maquettes fictives.
Détail de la campagne : 62-campagne-test-du-pouce.md.

Usage : python3 outils/marque/campagne_pouce.py
  écrit supports/campagne-pouce/ : 6 publications 1080 × 1350 (pouce-1.png … pouce-6.png),
  une story 1080 × 1920 (pouce-story.png), l'affiche A4 (affiche-pouce.pdf + .png) et une planche de contrôle.
  Avec DIG16_IDENTITE et DIG16_SORTIE (fichiers privés) : l'affiche remplie (nom, SIREN) va dans DIG16_SORTIE.
Contrôles : polices chargées, images chargées, aucun bloc hors de la marge de sécurité, QR de l'affiche décodé.
"""

import os
import sys

import cv2
import numpy as np
import segno
from PIL import Image
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import identite  # noqa: E402

RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
SORTIE = os.path.join(RACINE, "supports", "campagne-pouce")
MARQUE = "file://" + os.path.join(RACINE, "site-dig", "img", "marque") + "/"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LIEN = "https://dig16.fr/"
POLICES = ('<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
           '&family=Geist:wght@300;400;500;600&family=Geist+Mono&display=block" rel="stylesheet">')
MARGE = 64  # marge de sécurité des publications (px)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{margin:0}
body{width:%(l)dpx;height:%(h)dpx;overflow:hidden;font-family:Geist,sans-serif;color:#efe9df;
 background:#0f0e0c;background-image:radial-gradient(70%% 55%% at 88%% 6%%,rgba(200,164,110,.22),rgba(200,164,110,0) 70%%),
 radial-gradient(60%% 50%% at 0%% 100%%,rgba(200,164,110,.10),rgba(200,164,110,0) 70%%);position:relative}
body:after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.05;
 background-image:url("data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%%3E%%3Cfilter id='n'%%3E%%3CfeTurbulence baseFrequency='.85' numOctaves='3'/%%3E%%3C/filter%%3E%%3Crect width='100%%25' height='100%%25' filter='url(%%23n)'/%%3E%%3C/svg%%3E")}
.cadre{position:absolute;inset:28px;border:1.5px solid rgba(200,164,110,.35);border-radius:22px}
.z{position:absolute;left:%(m)dpx;right:%(m)dpx}
.haut{top:%(m)dpx;display:flex;justify-content:space-between;align-items:center}
.haut img{height:46px}
.etiq{font:400 22px 'Geist Mono';letter-spacing:.2em;text-transform:uppercase;color:#c8a46e}
.titre{font:400 116px/1 'Instrument Serif';letter-spacing:-.02em;color:#efe9df}
.titre em{color:#d9bb8a}
.sous{font:300 40px/1.38 Geist;color:#cfc6b8;max-width:860px}
.sous b{font-weight:500;color:#efe9df}
.bas{bottom:%(m)dpx;display:flex;justify-content:space-between;align-items:flex-end;gap:24px}
.site{font:500 34px Geist;color:#efe9df}
.site span{color:#c8a46e}
.pill{font:500 26px Geist;background:#c8a46e;color:#14110d;border-radius:999px;padding:16px 30px;white-space:nowrap}
.num{font:400 26px 'Geist Mono';color:#c8a46e;letter-spacing:.1em}
"""


def gabarit(larg, h, corps):
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8">{POLICES}<style>'
            + CSS % {"l": larg, "h": h, "m": MARGE} + "</style></head><body><div class='cadre'></div>"
            + corps + "</body></html>")


def entete(n):
    return (f'<div class="z haut"><img src="{MARQUE}signature-ivoire@2x.png" alt="DIG16">'
            f'<div class="num">{n}/6</div></div>')


PIED = ('<div class="z bas"><div class="site">dig16<span>.fr</span></div>'
        '<div class="pill">Ma page d’accueil refaite, gratuitement</div></div>')

TELEPHONE = """<div style="width:470px;height:720px;border-radius:56px;background:#181613;border:2px solid rgba(200,164,110,.45);
 padding:34px 28px;box-shadow:0 40px 80px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.06)">
 <div style="height:62px;border-radius:31px;background:#efe9df;color:#14110d;display:flex;align-items:center;gap:14px;padding:0 24px;font:400 25px Geist">
  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#655e54" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
  <span>votre métier + votre ville</span></div>
 %s
</div>"""


def resultat(largeur, actif=False):
    if actif:
        return ('<div style="margin-top:26px;height:104px;border:2.5px dashed #c8a46e;border-radius:18px;display:flex;'
                'align-items:center;justify-content:center;font:italic 400 44px \'Instrument Serif\';color:#d9bb8a">'
                'Et vous ?</div>')
    return ('<div style="margin-top:26px;height:104px;border-radius:18px;background:#22201b;padding:20px 22px">'
            f'<div style="height:16px;width:{largeur}%;border-radius:8px;background:#4a453c"></div>'
            '<div style="height:12px;width:90%;border-radius:6px;background:#302d27;margin-top:16px"></div>'
            '<div style="height:12px;width:62%;border-radius:6px;background:#302d27;margin-top:10px"></div></div>')


def publications():
    p = {}
    p["pouce-1.png"] = entete(1) + """
<div class="z" style="top:50%;transform:translateY(-52%)"><div class="etiq">Le test du pouce</div>
<div class="titre" style="margin-top:34px;font-size:136px">Prenez votre<br><em>téléphone.</em></div>
<p class="sous" style="margin-top:48px">Tapez <b>votre métier</b> et <b>votre ville</b>,<br>comme le ferait un client.<br>Regardez bien la liste.</p></div>""" + PIED
    p["pouce-2.png"] = entete(2) + """
<div class="z" style="top:190px;display:flex;gap:56px;align-items:center">
<div style="flex:1"><div class="etiq">Le test du pouce</div>
<div class="titre" style="margin-top:30px;font-size:104px">Vous êtes<br><em>où&nbsp;?</em></div>
<p class="sous" style="margin-top:40px;font-size:34px">Le client appelle souvent l’un des premiers noms qui s’affichent.</p></div>
<div style="flex:none">""" + TELEPHONE % (resultat(58) + resultat(70) + resultat(46) + resultat(0, True)) + """</div></div>""" + PIED
    p["pouce-3.png"] = entete(3) + """
<div class="z" style="top:50%;transform:translateY(-52%)"><div class="etiq">Le test du pouce · deuxième étape</div>
<div class="titre" style="margin-top:34px;font-size:118px">Vous y êtes&nbsp;?<br><em>Touchez votre nom.</em></div>
<p class="sous" style="margin-top:48px">Votre site s’ouvre-t-il bien sur un téléphone&nbsp;?<br>
Votre numéro s’appelle-t-il <b>d’un seul geste</b>&nbsp;?<br>Vos horaires sont-ils à jour&nbsp;?</p></div>""" + PIED
    vieux = """<div style="width:400px;height:560px;background:#d9d4c7;border:2px solid #8b8578;color:#1a1814;font-family:'Times New Roman',serif;padding:18px;overflow:hidden">
<div style="background:#3a5a8c;color:#fff;font:bold 22px 'Times New Roman';padding:10px;text-align:center">Bienvenue sur le site de VOTRE ENTREPRISE</div>
<div style="font-size:15px;margin-top:12px;color:#00e;text-decoration:underline">Accueil | Qui sommes-nous | Nos prestations | Contact</div>
<p style="font-size:17px;margin-top:16px;line-height:1.3">Notre entreprise est à votre service depuis de nombreuses années. N’hésitez pas à nous contacter pour tout renseignement.</p>
<p style="font-size:14px;margin-top:16px;color:#555">Site optimisé pour un écran de 1024 × 768.</p>
<p style="font-size:14px;margin-top:8px;color:#555">Dernière mise à jour : mars 2014.</p>
<p style="font-size:14px;margin-top:8px;color:#00e;text-decoration:underline">Voir notre plaquette (PDF, 12 Mo)</p></div>"""
    neuf = """<div style="width:400px;height:560px;border-radius:30px;background:#f3eee5;color:#1a1814;padding:30px 28px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.4)">
<div style="font:400 15px 'Geist Mono';letter-spacing:.16em;color:#7a5a2c;text-transform:uppercase">Menuiserie · Charente</div>
<div style="font:400 50px/1.02 'Instrument Serif';margin-top:16px">Fenêtres et escaliers <em style="color:#7a5a2c">sur mesure</em></div>
<p style="font:300 18px/1.4 Geist;color:#655e54;margin-top:16px">Fabrication à l’atelier, pose chez vous. Devis gratuit sous 48 h.</p>
<div style="margin-top:22px;background:#1a1814;color:#efe9df;border-radius:999px;padding:16px;text-align:center;font:500 20px Geist">Appeler maintenant</div>
<div style="display:flex;gap:10px;margin-top:20px"><div style="flex:1;height:120px;border-radius:14px;background:linear-gradient(135deg,#c8a46e,#7a5a2c)"></div>
<div style="flex:1;height:120px;border-radius:14px;background:linear-gradient(135deg,#655e54,#2e2a24)"></div></div>
<p style="font:400 14px Geist;color:#655e54;margin-top:12px">Ouvert aujourd’hui · 8 h – 18 h</p></div>"""
    p["pouce-4.png"] = entete(4) + """
<div class="z" style="top:170px"><div class="etiq">Sinon&nbsp;?</div>
<div class="titre" style="margin-top:22px;font-size:92px">Je refais votre page d’accueil. <em>Gratuitement.</em></div></div>
<div class="z" style="top:560px;display:flex;justify-content:space-between;align-items:center">
<div style="text-align:center">""" + vieux + """<div class="etiq" style="margin-top:18px;color:#a8a093">Avant</div></div>
<div style="font:400 64px 'Instrument Serif';color:#c8a46e">→</div>
<div style="text-align:center">""" + neuf + """<div class="etiq" style="margin-top:18px">Après · exemple fictif</div></div></div>""" + PIED
    p["pouce-5.png"] = entete(5) + """
<div class="z" style="top:50%;transform:translateY(-52%)"><div class="etiq">Une règle simple</div>
<div class="titre" style="margin-top:34px;font-size:150px"><em>15</em> entreprises.</div>
<div class="titre" style="font-size:96px;margin-top:10px">Pas une de plus.</div>
<p class="sous" style="margin-top:48px">La première année, DIG16 accompagne <b>15 entreprises au maximum</b>,
pour que chacune ait une vraie personne au bout du fil et ses changements faits <b>en 3 jours ouvrés</b>.</p></div>""" + PIED
    ligne = ('<div style="display:flex;justify-content:space-between;align-items:baseline;padding:26px 0;'
             'border-bottom:1.5px solid rgba(200,164,110,.25)"><span style="font:300 36px Geist;color:#cfc6b8">%s</span>'
             '<span style="font:400 58px \'Instrument Serif\';color:#efe9df">%s</span></div>')
    p["pouce-6.png"] = entete(6) + """
<div class="z" style="top:50%;transform:translateY(-52%)"><div class="etiq">Ce que vous obtenez</div>
<div class="titre" style="margin-top:26px;font-size:96px">Simple, clair, <em>à votre nom.</em></div>
<div style="margin-top:44px">""" + "".join(ligne % x for x in [
        ("Création du site", "0 €"), ("En ligne en", "7 jours"), ("Site et nom de domaine", "à vous"),
        ("Après 6 mois", "sans engagement"), ("À partir de", "49 € / mois")]) + """</div></div>""" + PIED
    return p


def story():
    etape = ('<div style="display:flex;gap:30px;align-items:flex-start;margin-top:56px">'
             '<div style="flex:none;width:92px;height:92px;border-radius:50%%;border:2px solid #c8a46e;display:flex;'
             'align-items:center;justify-content:center;font:400 52px \'Instrument Serif\';color:#c8a46e">%s</div>'
             '<div><div style="font:400 60px/1.05 \'Instrument Serif\'">%s</div>'
             '<div style="font:300 32px/1.4 Geist;color:#cfc6b8;margin-top:12px">%s</div></div></div>')
    return (f'<div class="z haut"><img src="{MARQUE}signature-ivoire@2x.png" alt="DIG16"></div>'
            '<div class="z" style="top:300px"><div class="etiq">Le test du pouce</div>'
            '<div class="titre" style="margin-top:30px;font-size:132px">30 secondes<br><em>pour savoir.</em></div>'
            + etape % ("1", "Tapez votre métier<br>et votre ville.", "Sur votre téléphone, comme un client.")
            + etape % ("2", "Cherchez-vous.", "Êtes-vous dans les premiers résultats&nbsp;?")
            + etape % ("3", "Touchez votre nom.", "Le site s’ouvre bien&nbsp;? Le numéro s’appelle d’un geste&nbsp;?")
            + '<p class="sous" style="margin-top:80px;font-size:40px"><b>Un « non » ?</b> Je refais votre page d’accueil '
            'gratuitement. Vous décidez ensuite.</p></div>'
            '<div class="z bas" style="flex-direction:column;align-items:flex-start;gap:30px">'
            '<div class="pill" style="font-size:32px;padding:22px 40px">Recevoir ma démo gratuite</div>'
            '<div class="site" style="font-size:44px">dig16<span>.fr</span></div></div>')


def qr_svg():
    return segno.make(LIEN, error="q").svg_inline(scale=1, border=0, dark="#14110d", omitsize=True)


AFFICHE = """<!doctype html><html lang="fr"><head><meta charset="utf-8">""" + POLICES + """<style>
@page{size:210mm 297mm;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Geist,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;color:#1a1814;
 background:radial-gradient(140mm 110mm at 175mm 20mm,rgba(200,164,110,.30),rgba(200,164,110,0) 70%),
 linear-gradient(180deg,#f8f4ec,#f3eee5 60%,#ede6d9)}
.filet{position:absolute;inset:7mm;border:.35mm solid rgba(110,80,37,.45);border-radius:4mm}
.z{position:absolute;left:18mm;right:18mm}
.etiq{font:500 12pt Geist;letter-spacing:.12em;text-transform:uppercase;color:#6e5025}
h1{font:400 64pt/0.98 'Instrument Serif';letter-spacing:-.01em;margin-top:6mm}
h1 em{color:#6e5025}
.etapes{margin-top:12mm;display:grid;gap:7mm}
.e{display:flex;gap:6mm;align-items:flex-start}
.e b{flex:none;width:13mm;height:13mm;border-radius:50%;border:.5mm solid #6e5025;display:flex;align-items:center;
 justify-content:center;font:400 22pt 'Instrument Serif';color:#6e5025}
.e div{font:400 26pt/1.1 'Instrument Serif'}
.e span{display:block;text-wrap:pretty;font:400 13pt/1.35 Geist;color:#4a443b;margin-top:1.5mm}
.offre{margin-top:13mm;background:#1a1712;color:#efe9df;border-radius:5mm;padding:9mm 10mm;display:flex;gap:9mm;align-items:center}
.offre p{font:400 25pt/1.1 'Instrument Serif'}
.offre p em{color:#d9bb8a}
.offre small{display:block;font:400 12.5pt/1.4 Geist;color:#cfc6b8;margin-top:3mm}
.qr{flex:none;width:38mm;height:38mm;background:#fff;border-radius:3mm;padding:3mm}
.qr svg{width:100%;height:100%;display:block}
.pied{bottom:14mm;display:flex;justify-content:space-between;align-items:flex-end;font:400 10pt Geist;color:#4a443b}
.pied img{height:9mm}
</style></head><body><div class="page"><div class="filet"></div>
<div class="z" id="corps" style="top:20mm"><div class="etiq">Le test du pouce · 30 secondes</div>
<h1>Prenez votre téléphone.<br><em>Vous êtes où&nbsp;?</em></h1>
<div class="etapes">
<div class="e"><b>1</b><div>Tapez votre métier et votre ville.<span>Comme le ferait un client qui cherche quelqu’un près de chez lui.</span></div></div>
<div class="e"><b>2</b><div>Cherchez-vous dans la liste.<span>Le client appelle souvent l’un des premiers noms qui s’affichent.</span></div></div>
<div class="e"><b>3</b><div>Touchez votre nom.<span>Le site s’ouvre bien&nbsp;? Le numéro s’appelle d’un geste&nbsp;? Les horaires sont à&nbsp;jour&nbsp;?</span></div></div>
</div>
<div class="offre"><div><p>Un « non »&nbsp;? Je refais votre page d’accueil, <em>gratuitement.</em></p>
<small>Vous la regardez sur votre téléphone,<br>puis vous décidez.<br>0 € de création · en ligne en 7 jours<br>site à votre nom · dès 49 € par mois</small></div>
<div class="qr">{QR}</div></div></div>
<div class="z pied" id="pied"><div>DIG16 — sites internet pour artisans et commerçants de Charente<br>
[Prénom Nom] EI · SIREN [numéro à l’immatriculation] · contact@dig16.fr</div>
<img src="SIG" alt="DIG16"></div>
</div></body></html>"""


def rendre_png(nav, html, larg, h, chemin, fautes):
    pg = nav.new_page(viewport={"width": larg, "height": h})
    tmp = os.path.join(SORTIE, "_tmp.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    pg.goto("file://" + tmp)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(700)
    r = pg.evaluate("""(()=>{const out=[];for(const z of document.querySelectorAll('.z')){const b=z.getBoundingClientRect();
      out.push([b.left,b.top,b.right,b.bottom,z.scrollWidth>z.clientWidth+1])}
      return [out,[...document.fonts].filter(f=>f.status==='loaded').length,
      [...document.images].every(i=>i.complete&&i.naturalWidth>0)]})()""")
    os.remove(tmp)
    nom = os.path.basename(chemin)
    for g, ha, d, b, deborde in r[0]:
        if g < MARGE - 1 or ha < MARGE - 1 or d > larg - MARGE + 1 or b > h - MARGE + 1 or deborde:
            fautes.append(f"{nom} : bloc hors marge ({round(g)},{round(ha)},{round(d)},{round(b)})")
    if r[1] < 3:
        fautes.append(f"{nom} : polices non chargées ({r[1]})")
    if not r[2]:
        fautes.append(f"{nom} : image non chargée")
    pg.screenshot(path=chemin)
    pg.close()


def rendre_affiche(nav, html, pdf, png, fautes):
    tmp = os.path.join(SORTIE, "_affiche.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    pg = nav.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
    pg.goto("file://" + tmp)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(700)
    r = pg.evaluate("""(()=>{const c=document.getElementById('corps').getBoundingClientRect(),
      p=document.getElementById('pied').getBoundingClientRect();return [c.bottom,p.top,p.bottom,
      [...document.images].every(i=>i.complete&&i.naturalWidth>0)]})()""")
    if r[0] > r[1] - 8:
        fautes.append(f"affiche : le corps touche le pied ({round(r[0])} > {round(r[1])})")
    if r[2] > 1123 - 30 or not r[3]:
        fautes.append("affiche : pied hors page ou image non chargée")
    pg.screenshot(path=png)
    pg.pdf(path=pdf, width="210mm", height="297mm", print_background=True)
    pg.close()
    os.remove(tmp)
    im = Image.open(png).convert("RGB")
    lu = cv2.QRCodeDetector().detectAndDecode(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))[0]
    if lu != LIEN:
        fautes.append(f"affiche : QR non décodé ({lu!r})")


def planche(noms):
    ims = [Image.open(os.path.join(SORTIE, n)).convert("RGB").resize((360, 450)) for n in noms]
    pl = Image.new("RGB", (360 * 3 + 40, 450 * 2 + 30), "#f3eee5")
    for i, im in enumerate(ims):
        pl.paste(im, (10 + (i % 3) * 370, 10 + (i // 3) * 460))
    pl.save(os.path.join(SORTIE, "planche-publications.png"))


def main():
    os.makedirs(SORTIE, exist_ok=True)
    fautes = []
    ident = identite.charger()
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pubs = publications()
        for nom, corps in pubs.items():
            rendre_png(nav, gabarit(1080, 1350, corps), 1080, 1350, os.path.join(SORTIE, nom), fautes)
            print(nom)
        rendre_png(nav, gabarit(1080, 1920, story()), 1080, 1920, os.path.join(SORTIE, "pouce-story.png"), fautes)
        print("pouce-story.png")
        html = AFFICHE.replace("{QR}", qr_svg()).replace("SIG", MARQUE + "signature-encre@2x.png")
        rendre_affiche(nav, html, os.path.join(SORTIE, "affiche-pouce.pdf"),
                       os.path.join(SORTIE, "affiche-pouce.png"), fautes)
        print("affiche-pouce.pdf")
        if ident:
            prive = identite.sortie(SORTIE)
            rendre_affiche(nav, identite.remplir(html, ident), os.path.join(prive, "affiche-pouce-remplie.pdf"),
                           os.path.join(prive, "affiche-pouce-remplie.png"), fautes)
            print("affiche remplie (privée)")
        nav.close()
    planche(list(pubs))
    for f in fautes:
        print("ALERTE", f)
    return 1 if fautes else 0


if __name__ == "__main__":
    raise SystemExit(main())
