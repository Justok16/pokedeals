#!/usr/bin/env python3
"""Campagne « Le test du pouce » (08/10/2026, version 2 « signature ») : visuels à la charte DIG16 (60-charte-dig16.md).

Idée : le prospect se cherche lui-même sur son téléphone (« votre métier et votre ville ») et constate seul
où il apparaît. Aucun chiffre inventé, aucun concurrent nommé, entreprises des maquettes fictives.
Motif unique de la campagne : l'empreinte de pouce dorée (outils/marque/empreinte.py), seul élément fort ;
tout le reste reste sobre. Détail de la campagne : 62-campagne-test-du-pouce.md.

Usage : python3 outils/marque/campagne_pouce.py
  écrit supports/campagne-pouce/ : 5 publications 1080 × 1350 (pouce-1.png … pouce-5.png),
  une story 1080 × 1920 (pouce-story.png), l'affiche A4 (affiche-pouce.pdf + .png) et une planche de contrôle.
  Avec DIG16_IDENTITE et DIG16_SORTIE (fichiers privés) : l'affiche remplie (nom, SIREN) va dans DIG16_SORTIE.
PDF de l'affiche fait à partir de l'image A4 300 ppp (lisible dans toutes les visionneuses).
Contrôles : polices et images chargées, aucun bloc de texte (.z) hors de la marge de sécurité ni débordant,
QR de l'affiche décodé.
"""

import base64
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
from empreinte import empreinte_svg  # noqa: E402

RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
SORTIE = os.path.join(RACINE, "supports", "campagne-pouce")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
LIEN = "https://dig16.fr/"
POLICES = ('<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
           '&family=Geist:wght@300;400;500;600&display=block" rel="stylesheet">')
MARGE = 72  # marge de sécurité des publications (px)
APPEL = "Recevoir ma démo gratuite"  # même libellé que le bouton du site

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{margin:0}
body{width:%(l)dpx;height:%(h)dpx;overflow:hidden;font-family:Geist,sans-serif;color:#efe9df;position:relative;
 background:#0f0e0c;background-image:radial-gradient(80%% 60%% at 92%% 0%%,rgba(200,164,110,.16),rgba(200,164,110,0) 70%%),
 radial-gradient(70%% 50%% at 0%% 100%%,rgba(200,164,110,.07),rgba(200,164,110,0) 70%%)}
body:after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.06;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%%3E%%3Cfilter id='n'%%3E%%3CfeTurbulence baseFrequency='.9' numOctaves='3'/%%3E%%3C/filter%%3E%%3Crect width='100%%25' height='100%%25' filter='url(%%23n)'/%%3E%%3C/svg%%3E")}
.deco{position:absolute;pointer-events:none}
.z{position:absolute;left:%(m)dpx;right:%(m)dpx}
.haut{top:%(m)dpx;display:flex;justify-content:space-between;align-items:center}
.haut img{height:44px}
.serie{display:flex;gap:8px}.serie i{width:34px;height:3px;border-radius:2px;background:rgba(239,233,223,.22)}
.serie i.on{background:#c8a46e}
.campagne{font:500 28px Geist;color:#c8a46e;letter-spacing:.01em}
h1{font:400 128px/.98 'Instrument Serif';letter-spacing:-.025em;color:#efe9df}
h1 .l2{display:block;color:#d9bb8a}
.texte{font:300 40px/1.4 Geist;color:#cfc6b8;max-width:820px;text-wrap:pretty}
.texte b{font-weight:500;color:#efe9df}
.bas{bottom:%(m)dpx;display:flex;justify-content:space-between;align-items:center;gap:24px}
.site{font:500 36px Geist;color:#efe9df;letter-spacing:-.01em}
.site span{color:#c8a46e}
.bouton{font:500 27px Geist;background:#c8a46e;color:#14110d;border-radius:999px;padding:18px 34px;white-space:nowrap;
 box-shadow:0 10px 30px rgba(200,164,110,.18)}
"""


def gabarit(larg, h, corps):
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8">{POLICES}<style>'
            + CSS % {"l": larg, "h": h, "m": MARGE} + "</style></head><body>" + corps + "</body></html>")


def entete(n):
    barres = "".join(f'<i class="{"on" if k == n else ""}"></i>' for k in range(1, 6))
    return (f'<div class="z haut"><img src="{image_data("signature-ivoire@2x.png")}" alt="DIG16">'
            f'<div class="serie" aria-label="{n} sur 5">{barres}</div></div>')


PIED = f'<div class="z bas"><div class="site">dig16<span>.fr</span></div><div class="bouton">{APPEL}</div></div>'


def emp(taille, style, opacite=1.0, ident="e", couleur="#c8a46e"):
    return f'<div class="deco" style="{style}">{empreinte_svg(taille, couleur=couleur, opacite=opacite, ident=ident)}</div>'


def telephone(contenu, largeur=500):
    return (f'<div style="width:{largeur}px;height:{largeur * 1.62:.0f}px;border-radius:64px;padding:14px;'
            'background:linear-gradient(160deg,#3a352d,#1a1814 40%,#2a2620);box-shadow:0 50px 100px rgba(0,0,0,.55),'
            '0 0 0 1.5px rgba(200,164,110,.35)">'
            '<div style="position:relative;width:100%;height:100%;border-radius:52px;background:#14120f;overflow:hidden;'
            'padding:78px 26px 26px">'
            '<div style="position:absolute;top:22px;left:50%;transform:translateX(-50%);width:120px;height:32px;'
            'border-radius:16px;background:#000"></div>'
            '<div style="height:66px;border-radius:33px;background:#efe9df;color:#14110d;display:flex;align-items:center;'
            'gap:14px;padding:0 26px;font:400 26px Geist">'
            '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#655e54" stroke-width="2.4">'
            '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>votre métier, votre ville</div>'
            + contenu + '<div style="position:absolute;inset:0;border-radius:52px;pointer-events:none;'
            'background:linear-gradient(125deg,rgba(255,255,255,.07),rgba(255,255,255,0) 35%)"></div></div></div>')


def ligne_resultat(larg):
    return ('<div style="margin-top:24px;height:112px;border-radius:20px;background:#201d18;padding:24px 24px">'
            f'<div style="height:18px;width:{larg}%;border-radius:9px;background:#4a453c"></div>'
            '<div style="height:12px;width:88%;border-radius:6px;background:#2e2b25;margin-top:18px"></div>'
            '<div style="height:12px;width:60%;border-radius:6px;background:#2e2b25;margin-top:10px"></div></div>')


def publications():
    p = {}
    # 1 — l'empreinte, immense, sort du cadre : la pièce maîtresse
    p["pouce-1.png"] = (emp(1180, "right:-470px;top:-230px", .95, "a")
        + '<div class="deco" style="inset:0;background:linear-gradient(20deg,#0f0e0c 34%,rgba(15,14,12,.85) 48%,rgba(15,14,12,0) 70%)"></div>'
        + entete(1) + """
<div class="z" style="bottom:230px"><div class="campagne">Le test du pouce</div>
<h1 style="margin-top:28px;font-size:150px">Prenez votre<br>téléphone.</h1>
<p class="texte" style="margin-top:40px">Tapez <b>votre métier et votre ville</b>, comme le ferait un client.
Puis regardez bien la liste.</p></div>""" + PIED)
    # 2 — la place vide marquée par l'empreinte
    vide = ('<div style="margin-top:24px;height:150px;border-radius:20px;border:2.5px dashed #c8a46e;display:flex;'
            'align-items:center;justify-content:center;gap:22px">'
            + f'<div style="width:78px">{empreinte_svg(78, ident="b", epaisseur=1.6, cretes=12)}</div>'
            '<span style="font:italic 400 50px \'Instrument Serif\';color:#d9bb8a">Et vous&nbsp;?</span></div>')
    p["pouce-2.png"] = (entete(2) + """
<div class="z" style="top:200px"><div class="campagne">Le test du pouce</div>
<h1 style="margin-top:26px">Vous êtes<br><span class="l2">où&nbsp;?</span></h1>
<p class="texte" style="margin-top:36px;max-width:430px;font-size:36px">Le client appelle souvent l’un des premiers
noms qui s’affichent.</p></div>
<div class="deco" style="right:72px;top:190px">""" + telephone(ligne_resultat(56) + ligne_resultat(70) + ligne_resultat(44) + vide, 470)
        + "</div>" + PIED)
    # 3 — le pouce touche le nom : ondes dorées
    carte = ('<div style="position:relative;margin-top:40px;margin-bottom:56px;border-radius:22px;background:#efe9df;color:#1a1814;padding:28px">'
             '<div style="font:400 40px/1.05 \'Instrument Serif\'">Votre entreprise</div>'
             '<div style="font:400 21px Geist;color:#655e54;margin-top:10px">Votre métier, votre ville</div>'
             '<div style="display:flex;gap:10px;margin-top:18px"><span style="font:500 19px Geist;background:#1a1814;'
             'color:#efe9df;border-radius:999px;padding:10px 18px">Site web</span><span style="font:500 19px Geist;'
             'border:1.5px solid #1a1814;border-radius:999px;padding:9px 18px">Appeler</span></div>'
             '<div style="position:absolute;right:-6px;bottom:-62px;width:130px;height:130px">'
             + "".join(f'<div style="position:absolute;inset:{-k * 26}px;border-radius:50%;border:2px solid rgba(122,90,44,{.55 - k * .14})"></div>'
                       for k in range(3))
             + f'<div style="position:absolute;inset:14px">{empreinte_svg(102, couleur="#7a5a2c", ident="c", epaisseur=2.2, cretes=14)}</div>'
             '</div></div>' + ligne_resultat(64) + ligne_resultat(48))
    questions = "".join(
        f'<div style="padding:24px 0;border-top:1.5px solid rgba(200,164,110,.28);font:300 34px/1.3 Geist;color:#cfc6b8">{q}</div>'
        for q in ["Le site s’ouvre bien sur un téléphone&nbsp;?", "Le numéro s’appelle d’un seul geste&nbsp;?",
                  "Les horaires sont à jour&nbsp;?"])
    p["pouce-3.png"] = (entete(3) + """
<div class="z" style="top:200px;right:600px"><div class="campagne">Deuxième étape</div>
<h1 style="margin-top:26px;font-size:112px">Touchez<br><span class="l2">votre nom.</span></h1>
<div style="margin-top:44px">""" + questions + """</div></div>
<div class="deco" style="right:72px;top:190px">""" + telephone(carte, 470) + "</div>" + PIED)
    vieux = """<div style="width:400px;height:540px;background:#d9d4c7;border:2px solid #8b8578;color:#1a1814;font-family:'Times New Roman',serif;padding:18px;overflow:hidden;filter:saturate(.8)">
<div style="background:#3a5a8c;color:#fff;font:bold 22px 'Times New Roman';padding:10px;text-align:center">Bienvenue sur le site de VOTRE ENTREPRISE</div>
<div style="font-size:15px;margin-top:12px;color:#00e;text-decoration:underline">Accueil | Qui sommes-nous | Nos prestations | Contact</div>
<p style="font-size:17px;margin-top:16px;line-height:1.3">Notre entreprise est à votre service depuis de nombreuses années. N’hésitez pas à nous contacter pour tout renseignement.</p>
<p style="font-size:14px;margin-top:16px;color:#555">Site optimisé pour un écran de 1024 × 768.</p>
<p style="font-size:14px;margin-top:8px;color:#555">Dernière mise à jour : mars 2014.</p>
<p style="font-size:14px;margin-top:8px;color:#00e;text-decoration:underline">Voir notre plaquette (PDF, 12 Mo)</p></div>"""
    neuf = """<div style="width:400px;height:540px;border-radius:30px;background:#f3eee5;color:#1a1814;padding:34px 30px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.5)">
<div style="font:500 17px Geist;color:#7a5a2c">Menuiserie en Charente</div>
<div style="font:400 54px/1 'Instrument Serif';margin-top:16px;letter-spacing:-.01em">Fenêtres et escaliers sur mesure</div>
<p style="font:300 19px/1.45 Geist;color:#655e54;margin-top:18px">Fabrication à l’atelier, pose chez vous. Devis gratuit sous 48 h.</p>
<div style="margin-top:24px;background:#1a1814;color:#efe9df;border-radius:999px;padding:17px;text-align:center;font:500 21px Geist">Appeler maintenant</div>
<div style="display:flex;gap:10px;margin-top:22px"><div style="flex:1;height:128px;border-radius:14px;background:linear-gradient(135deg,#c8a46e,#7a5a2c)"></div>
<div style="flex:1;height:128px;border-radius:14px;background:linear-gradient(135deg,#655e54,#2e2a24)"></div></div>
<p style="font:400 15px Geist;color:#655e54;margin-top:14px">Ouvert aujourd’hui de 8 h à 18 h</p></div>"""
    legende = 'style="font:400 22px Geist;color:#a8a093;margin-top:20px;text-align:center"'
    p["pouce-4.png"] = (entete(4) + """
<div class="z" style="top:180px"><div class="campagne">Un résultat qui ne vous plaît pas&nbsp;?</div>
<h1 style="margin-top:22px;font-size:96px">Je refais votre page d’accueil.<span class="l2">Gratuitement.</span></h1></div>
<div class="z" style="top:530px;display:flex;justify-content:space-between;align-items:flex-start">
<div>""" + vieux + f"<p {legende}>Aujourd’hui</p></div>"
        + '<div style="align-self:center;width:2px;height:420px;background:linear-gradient(transparent,#c8a46e,transparent)"></div>'
        + "<div>" + neuf + f"<p {legende}>Avec DIG16 (exemple fictif)</p></div></div>" + PIED)
    rang = ('<div style="display:flex;justify-content:space-between;align-items:baseline;padding:24px 0;'
            'border-top:1.5px solid rgba(200,164,110,.26)"><span style="font:300 36px Geist;color:#cfc6b8">%s</span>'
            '<span style="font:400 62px \'Instrument Serif\';color:#efe9df;letter-spacing:-.01em">%s</span></div>')
    p["pouce-5.png"] = (emp(620, "left:-260px;bottom:-200px", .22, "f") + entete(5) + """
<div class="z" style="top:180px"><div class="campagne">Ce que vous obtenez</div>
<h1 style="margin-top:24px;font-size:104px">Un site clair,<span class="l2">à votre nom.</span></h1>
<div style="margin-top:44px">""" + "".join(rang % x for x in [
        ("Création du site", "0 €"), ("En ligne", "en 7 jours"), ("Site et nom de domaine", "à vous"),
        ("Après les 6 premiers mois", "sans engagement"), ("Abonnement", "dès 49 € par mois")]) + "</div></div>" + PIED)
    return p


def story():
    etape = ('<div style="display:grid;grid-template-columns:96px 1fr;gap:30px;padding:30px 0;'
             'border-top:1.5px solid rgba(200,164,110,.26)">'
             '<div style="font:400 84px/.9 \'Instrument Serif\';color:#c8a46e">%s</div>'
             '<div><div style="font:400 58px/1.05 \'Instrument Serif\'">%s</div>'
             '<div style="font:300 31px/1.4 Geist;color:#cfc6b8;margin-top:12px">%s</div></div></div>')
    return (emp(900, "left:50%;top:-470px;transform:translateX(-50%);-webkit-mask-image:linear-gradient(180deg,rgba(0,0,0,.35) 30%,#000 55%,#000 80%,transparent 100%);mask-image:linear-gradient(180deg,rgba(0,0,0,.35) 30%,#000 55%,#000 80%,transparent 100%)", .9, "s")
            + f'<div class="z haut"><img src="{image_data("signature-ivoire@2x.png")}" alt="DIG16"></div>'
            '<div class="z" style="top:690px"><div class="campagne">Le test du pouce</div>'
            '<h1 style="margin-top:22px;font-size:110px">30 secondes<span class="l2">pour savoir.</span></h1>'
            '<div style="margin-top:38px">'
            + etape % ("1", "Tapez votre métier et votre ville.", "Sur votre téléphone, comme un client.")
            + etape % ("2", "Cherchez-vous.", "Êtes-vous parmi les premiers noms&nbsp;?")
            + etape % ("3", "Touchez votre nom.", "Le site s’ouvre bien&nbsp;? Le numéro s’appelle d’un geste&nbsp;?")
            + '</div></div>'
            f'<div class="z bas" style="flex-direction:column;align-items:flex-start;gap:26px">'
            '<p class="texte" style="font-size:36px"><b>Un « non »&nbsp;?</b> Je refais votre page d’accueil gratuitement.</p>'
            f'<div style="display:flex;justify-content:space-between;align-items:center;width:100%">'
            f'<div class="site" style="font-size:44px">dig16<span>.fr</span></div><div class="bouton">{APPEL}</div></div></div>')


def image_data(nom):
    """Image de la marque intégrée (data URI) : les pages se rendent en mémoire, sans fichier local."""
    with open(os.path.join(RACINE, "site-dig", "img", "marque", nom), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def qr_svg():
    return segno.make(LIEN, error="q").svg_inline(scale=1, border=0, dark="#14110d", omitsize=True)


AFFICHE = """<!doctype html><html lang="fr"><head><meta charset="utf-8">""" + POLICES + """<style>
@page{size:210mm 297mm;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Geist,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;color:#1a1814;
 background:radial-gradient(140mm 110mm at 180mm 10mm,rgba(200,164,110,.26),rgba(200,164,110,0) 70%),
 linear-gradient(180deg,#f8f4ec,#f3eee5 60%,#ede6d9)}
.emp{position:absolute;right:-58mm;top:-44mm;width:140mm;opacity:.26}
.emp svg{width:100%;height:auto;display:block}
.filet{position:absolute;inset:7mm;border:.35mm solid rgba(110,80,37,.45);border-radius:4mm}
.z{position:absolute;left:18mm;right:18mm}
.campagne{font:500 13pt Geist;color:#6e5025}
h1{font:400 60pt/0.96 'Instrument Serif';letter-spacing:-.015em;margin-top:5mm}
h1 span{display:block;color:#6e5025}
.etapes{margin-top:9mm}
.e{display:grid;grid-template-columns:14mm 1fr;gap:4mm;padding:4.5mm 0;border-top:.35mm solid rgba(110,80,37,.3)}
.e b{font:400 30pt/.9 'Instrument Serif';color:#6e5025}
.e div{font:400 25pt/1.1 'Instrument Serif'}
.e span{display:block;font:400 12.5pt/1.4 Geist;color:#4a443b;margin-top:1.5mm;text-wrap:pretty}
.offre{margin-top:8mm;background:#1a1712;color:#efe9df;border-radius:5mm;padding:9mm 10mm;display:flex;gap:9mm;align-items:center}
.offre p{font:400 25pt/1.08 'Instrument Serif'}
.offre p span{color:#d9bb8a}
.offre small{display:block;font:400 12pt/1.5 Geist;color:#cfc6b8;margin-top:3.5mm}
.qr{flex:none;width:38mm;height:38mm;background:#fff;border-radius:3mm;padding:3mm}
.qr svg{width:100%;height:100%;display:block}
.pied{bottom:14mm;display:flex;justify-content:space-between;align-items:flex-end;font:400 10pt/1.45 Geist;color:#4a443b}
.pied img{height:9mm}
</style></head><body><div class="page"><div class="emp">EMPREINTE</div><div class="filet"></div>
<div class="z" id="corps" style="top:22mm"><div class="campagne">Le test du pouce, en 30 secondes</div>
<h1>Prenez votre téléphone.<span>Vous êtes où&nbsp;?</span></h1>
<div class="etapes">
<div class="e"><b>1</b><div>Tapez votre métier et votre ville.<span>Comme le ferait un client qui cherche quelqu’un près de chez lui.</span></div></div>
<div class="e"><b>2</b><div>Cherchez-vous dans la liste.<span>Le client appelle souvent l’un des premiers noms qui s’affichent.</span></div></div>
<div class="e"><b>3</b><div>Touchez votre nom.<span>Le site s’ouvre bien&nbsp;? Le numéro s’appelle d’un geste&nbsp;? Les horaires sont à&nbsp;jour&nbsp;?</span></div></div>
</div>
<div class="offre"><div><p>Un « non »&nbsp;? Je refais votre page d’accueil, <span>gratuitement.</span></p>
<small>Vous la regardez sur votre téléphone,<br>puis vous décidez.<br>0 € de création, en ligne en 7 jours,<br>site à votre nom, dès 49 € par mois.</small></div>
<div class="qr">{QR}</div></div></div>
<div class="z pied" id="pied"><div>DIG16, sites internet pour artisans et commerçants de Charente<br>
[Prénom Nom] EI, SIREN [numéro à l’immatriculation], contact@dig16.fr</div>
<img src="SIG" alt="DIG16"></div>
</div></body></html>"""


def rendre_png(nav, html, larg, h, chemin, fautes):
    pg = nav.new_page(viewport={"width": larg, "height": h})
    pg.set_content(html, wait_until="networkidle")  # en mémoire : aucun fichier intermédiaire
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(800)
    r = pg.evaluate("""(()=>{const out=[];for(const z of document.querySelectorAll('.z')){const b=z.getBoundingClientRect();
      out.push([b.left,b.top,b.right,b.bottom,z.scrollWidth>z.clientWidth+1])}
      const deco=[...document.querySelectorAll('.deco')].filter(d=>!d.querySelector('svg')||d.children.length).map(d=>{
        const b=d.getBoundingClientRect();return [b.left,b.top,b.right,b.bottom,d.querySelector('div[style*="border-radius:64px"]')!==null]});
      return [out,[...document.fonts].filter(f=>f.status==='loaded').length,
      [...document.images].every(i=>i.complete&&i.naturalWidth>0),deco]})()""")
    nom = os.path.basename(chemin)
    for g, ha, d, b, deborde in r[0]:
        if g < MARGE - 1 or ha < MARGE - 1 or d > larg - MARGE + 1 or b > h - MARGE + 1 or deborde:
            fautes.append(f"{nom} : bloc hors marge ({round(g)},{round(ha)},{round(d)},{round(b)})")
    for g, ha, d, b, est_tel in r[3]:  # le téléphone doit rester entier dans la marge
        if est_tel and (g < MARGE - 1 or ha < MARGE - 1 or d > larg - MARGE + 1 or b > h - MARGE + 1):
            fautes.append(f"{nom} : téléphone hors marge")
    if r[1] < 3:
        fautes.append(f"{nom} : polices non chargées ({r[1]})")
    if not r[2]:
        fautes.append(f"{nom} : image non chargée")
    pg.screenshot(path=chemin)
    pg.close()


def chevauchements(nav, html, larg, h, nom, fautes):
    """Le texte ne doit pas toucher le téléphone ni le pied (contrôle géométrique)."""
    pg = nav.new_page(viewport={"width": larg, "height": h})
    pg.set_content(html, wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(500)
    r = pg.evaluate("""(()=>{const R=e=>{const b=e.getBoundingClientRect();return [b.left,b.top,b.right,b.bottom]};
      const zs=[...document.querySelectorAll('.z')].map(R);
      const tel=[...document.querySelectorAll('.deco')].filter(d=>d.querySelector('div[style*="border-radius:64px"]')).map(R);
      return [zs,tel]})()""")
    pg.close()
    zs, tel = r
    inter = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]  # noqa: E731
    for i, a in enumerate(zs):
        for b in zs[i + 1:]:
            if inter(a, b):
                fautes.append(f"{nom} : deux blocs de texte se chevauchent")
        for t in tel:
            if inter(a, t) and a[2] - a[0] < larg - 2 * MARGE - 2:  # entête et pied pleine largeur tolérés au-dessus/dessous
                fautes.append(f"{nom} : texte sur le téléphone")


def rendre_affiche(nav, html, pdf, png, fautes):
    # rendu en mémoire (aucun fichier intermédiaire : la version remplie contient le nom et le SIREN)
    pg = nav.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2480 / 794)
    pg.set_content(html, wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(800)
    r = pg.evaluate("""(()=>{const c=document.getElementById('corps').getBoundingClientRect(),
      p=document.getElementById('pied').getBoundingClientRect();return [c.bottom,p.top,p.bottom,
      [...document.images].every(i=>i.complete&&i.naturalWidth>0)]})()""")
    if r[0] > r[1] - 8:
        fautes.append(f"affiche : le corps touche le pied ({round(r[0])} > {round(r[1])})")
    if r[2] > 1123 - 30 or not r[3]:
        fautes.append("affiche : pied hors page ou image non chargée")
    pg.screenshot(path=png)
    pg.close()
    # PDF fait à partir de l'image A4 à 300 ppp : rendu identique dans toutes les visionneuses (les visionneuses
    # de téléphone n'affichaient que le fond du PDF vectoriel, 08/10 ; même leçon que le flyer le 28/09)
    im = Image.open(png).convert("RGB")
    if im.size != (2480, 3508):
        im = im.resize((2480, 3508), Image.LANCZOS)
    im.save(png, dpi=(300, 300))
    im.save(pdf, "PDF", resolution=300.0)
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
            html = gabarit(1080, 1350, corps)
            rendre_png(nav, html, 1080, 1350, os.path.join(SORTIE, nom), fautes)
            chevauchements(nav, html, 1080, 1350, nom, fautes)
            print(nom)
        html = gabarit(1080, 1920, story())
        rendre_png(nav, html, 1080, 1920, os.path.join(SORTIE, "pouce-story.png"), fautes)
        chevauchements(nav, html, 1080, 1920, "pouce-story.png", fautes)
        print("pouce-story.png")
        html = (AFFICHE.replace("{QR}", qr_svg()).replace("SIG", image_data("signature-encre@2x.png"))
                .replace("EMPREINTE", empreinte_svg(600, couleur="#b08a52", ident="p")))
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
