"""Vidéo de lancement verticale de dig16.fr (skill brag-slim, 20/10/2026) : plan dans brag-plan.md.

1080 × 1920, 30 i/s, 20 s, musique DIG16 + effets dans la même tonalité, sans voix.
Tout vient du site : textes de l'accueil, faux vieux site de la section avant/après, capture de démonstration
(entreprise fictive), chiffres des encarts de confiance. Polices du site incorporées.

Usage : python3 fabriquer.py [--controle]   (--controle : seulement les images fixes, sans rendu)
Écrit brag.mp4, brag.jpg (affiche = image 0) et des images de contrôle dans controle/ (non versionnées).
"""

import os
import subprocess
import sys

import numpy as np
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
CD = os.path.normpath(os.path.join(ICI, "..", ".."))
sys.path.insert(0, os.path.join(CD, "videos", "conseils"))
from fabriquer import CHROME, css_polices, data, empreinte_svg  # noqa: E402

FPS = 30
TOTAL = 20.0
AFFICHE = 2.6  # image la plus forte (accroche complète), recopiée en image 0
SITE = os.path.join(CD, "site-dig")


def page():
    signature = data(os.path.join(SITE, "img", "marque", "signature-ivoire@2x.png"), "image/png")
    vitrine = data(os.path.join(SITE, "img", "vitrine-visite-tel.webp"), "image/webp")
    emp = empreinte_svg(620, opacite=1.0, ident="f")
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css_polices()}</style><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;background:#0f0e0c;color:#efe9df;font-family:Geist,'Geist Fallback',sans-serif;position:relative;
 background-image:radial-gradient(80% 50% at 90% 0%,rgba(200,164,110,.16),rgba(200,164,110,0) 70%),
 radial-gradient(70% 40% at 0% 100%,rgba(200,164,110,.08),rgba(200,164,110,0) 70%)}}
.signature{{position:absolute;left:84px;top:90px;height:92px}}
.serif{{font-family:'Instrument Serif','Instrument Serif Fallback',serif;font-weight:400;letter-spacing:-.025em;text-wrap:balance}}
em{{color:#d9bb8a;font-style:italic}}
.bloc{{position:absolute;left:84px;right:84px;opacity:0}}
.etiq{{font:500 30px 'Geist Mono','Geist Mono Fallback',monospace;letter-spacing:.2em;text-transform:uppercase;color:#c8a46e;margin-bottom:22px}}
#h1{{top:600px}} #h1 h1{{font-size:124px;line-height:1.02}} #h1 .l2{{display:block;opacity:0}}
#t2,#t3{{top:250px}} #t2 h2,#t3 h2{{font-size:84px;line-height:1.04}}
.tel{{position:absolute;left:270px;top:600px;width:540px;height:1168px;border-radius:68px;background:#0b0a08;padding:18px;
 box-shadow:0 40px 110px rgba(0,0,0,.7),0 0 0 2px rgba(239,233,223,.14);opacity:0}}
.ecran{{position:relative;width:100%;height:100%;border-radius:56px;overflow:hidden;background:#fff}}
.ecran>*{{position:absolute;inset:0}}
.vieux{{width:1000px;transform:scale(.504);transform-origin:0 0;font-family:"Times New Roman",Times,serif;color:#000;background:#d9d9d9}}
.vieux header{{background:#003399;color:#ffff66;padding:30px 24px;font-size:44px;font-weight:bold;text-align:center;border-bottom:6px ridge #c0c0c0}}
.vieux .menu{{display:flex;gap:16px;background:#c0c0c0;padding:10px 24px;font-size:22px}}
.vieux .menu span{{color:#0000ee;text-decoration:underline}}
.vieux .corps{{display:grid;grid-template-columns:260px 1fr;gap:20px;padding:20px 24px;background:#fff;min-height:2200px}}
.vieux aside{{background:#eeeeee;border:2px inset #999;padding:14px;font-size:20px}}
.vieux .t4{{font-size:30px;color:#990000;margin-bottom:12px;font-weight:700;line-height:1.2}}
.vieux p{{font-size:22px;line-height:1.35;margin-bottom:14px}}
.vieux .boite{{border:3px double #003399;padding:14px;margin:20px 0;background:#ffffcc;font-size:22px}}
.vieux .compteur{{font-family:"Courier New",monospace;background:#000;color:#0f0;padding:6px 10px;display:inline-block;font-size:22px}}
.nouveau img{{width:100%;height:100%;object-fit:cover;object-position:top}}
.scan{{position:absolute;left:-4%;right:-4%;height:4px;background:#c8a46e;box-shadow:0 0 30px 6px rgba(200,164,110,.75)}}
.faits{{top:600px}}
.fait{{border-top:2px solid rgba(200,164,110,.5);padding:34px 0 40px;opacity:0}}
.fait b{{display:block;font:400 150px/1 'Instrument Serif','Instrument Serif Fallback',serif;color:#d9bb8a;letter-spacing:-.02em}}
.fait span{{display:block;font:400 54px/1.15 Geist,'Geist Fallback',sans-serif;color:#efe9df;margin-top:8px}}
#fin{{top:430px}} #fin h2{{font-size:108px;line-height:1.02}} #fin p{{font-size:52px;color:#cfc6b8;margin-top:34px}}
#emp{{position:absolute;left:300px;top:700px;opacity:0}}
.demo{{position:absolute;left:84px;right:84px;top:1800px;text-align:center;font:400 30px Geist,'Geist Fallback',sans-serif;color:#8a8275;opacity:0}}
.lien{{position:absolute;left:84px;right:84px;bottom:300px;font:500 76px Geist,'Geist Fallback',sans-serif;letter-spacing:-.01em;opacity:0}}
.lien span{{color:#c8a46e}}
.lieu{{position:absolute;left:84px;right:84px;bottom:232px;font:400 40px Geist,'Geist Fallback',sans-serif;color:#a8a093;opacity:0}}
</style></head><body>
<img class="signature" src="{signature}" alt="DIG16">
<div class="bloc serif" id="h1"><h1>Vos clients vous cherchent sur leur téléphone. <em class="l2">Ils vous trouvent&nbsp;?</em></h1></div>
<div class="bloc" id="t2"><div class="etiq">Avant</div><h2 class="serif">Votre site aujourd’hui&nbsp;: <em>daté, minuscule sur un téléphone.</em></h2></div>
<div class="bloc" id="t3"><div class="etiq">Après</div><h2 class="serif">Le même, <em>refait par DIG16.</em></h2></div>
<div class="tel" id="tel"><div class="ecran">
 <div class="vieux" aria-hidden="true">
  <header>Bienvenue sur le site de VOTRE ENTREPRISE</header>
  <div class="menu"><span>Accueil</span><span>Qui sommes-nous</span><span>Nos prestations</span><span>Plan d'accès</span><span>Contact</span></div>
  <div class="corps">
   <aside><p class="t4">Infos</p><p>Ouvert du lundi au vendredi.</p><p>Devis sur demande par téléphone ou par fax.</p><span class="compteur">004521</span><p>visiteurs</p></aside>
   <div><p class="t4">Notre entreprise</p><p>Bienvenue sur notre site internet ! Notre entreprise est à votre service depuis de nombreuses années pour tous vos travaux. N'hésitez pas à nous contacter pour tout renseignement complémentaire.</p><div class="boite">NOUVEAU : découvrez nos prestations dans la rubrique « Nos prestations ».</div><p>Site optimisé pour un écran de 1024 × 768.</p></div>
  </div>
 </div>
 <div class="nouveau" id="nouveau"><img src="{vitrine}" alt=""></div>
 <div class="scan" id="scan"></div>
</div></div>
<div class="demo" id="demo">Démonstration · entreprise fictive</div>
<div class="bloc faits" id="faits">
 <div class="fait" id="f0"><b>0&nbsp;€</b><span>de création</span></div>
 <div class="fait" id="f1"><b>7 jours</b><span>pour être en ligne</span></div>
 <div class="fait" id="f2"><b>100&nbsp;%</b><span>à votre nom</span></div>
</div>
<div class="bloc" id="fin"><h2 class="serif">Je refais votre page d’accueil <em>gratuitement.</em></h2><p>Vous décidez ensuite.</p></div>
<div id="emp">{emp}</div>
<div class="lien" id="lien">dig16<span>.fr</span></div>
<div class="lieu" id="lieu">Sites internet pour artisans · Charente</div>
<script>
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), doux=x=>{{x=cl(x,0,1);return x*x*(3-2*x)}};
const $=id=>document.getElementById(id);
// entrée/sortie : apparaît à a (montée de 40 px), disparaît avant b (sortie avant l'entrée suivante)
function vis(id,a,b,dy=40,fi=.45,fo=.35){{const e=$(id),o=Math.min(doux((t0-a)/fi),doux((b-t0)/fo));
 e.style.opacity=o;e.style.transform=`translateY(${{(1-doux((t0-a)/.7))*dy}}px)`;return o}}
let t0=0;
function seek(t){{
  t0=t;
  // 1. accroche (la 1re ligne est déjà là à l'image 0)
  const e1=$('h1');e1.style.opacity=Math.min(1,doux((3.55-t)/.35));e1.style.transform='none';
  e1.querySelector('.l2').style.opacity=doux((t-1.0)/.45);
  // 2. avant
  vis('t2',3.8,7.75);
  const tel=$('tel'),ot=Math.min(doux((t-3.65)/.6),doux((12.25-t)/.45));
  tel.style.opacity=ot;tel.style.transform=`translateY(${{(1-doux((t-3.65)/.9))*160 - doux((t-11.9)/.6)*60}}px)`;
  // 3. balayage puis après
  const w=doux((t-8.0)/1.7);
  $('nouveau').style.clipPath=`inset(${{(1-w)*100}}% 0 0 0)`;
  const sc=$('scan');sc.style.top=`calc(${{(1-w)*100}}% - 2px)`;sc.style.opacity=(t>7.9&&w<1)?1:Math.max(0,1-(t-9.7)/.3)*(t>7.9?1:0);
  vis('t3',8.4,12.15);
  $('demo').style.opacity=Math.min(doux((t-9.6)/.4),doux((12.1-t)/.35));
  // 4. trois encarts, l'un après l'autre
  const f=$('faits');f.style.opacity=Math.min(1,doux((16.15-t)/.35));
  for(let i=0;i<3;i++){{const e=$('f'+i),a=12.35+i*.75;e.style.opacity=doux((t-a)/.45);
   e.style.transform=`translateY(${{(1-doux((t-a)/.6))*50}}px)`}}
  // 5. fin
  vis('fin',16.35,99);
  const of=doux((t-16.9)/.6);$('lien').style.opacity=of;$('lieu').style.opacity=doux((t-17.2)/.6);
  const em=$('emp');em.style.opacity=doux((t-16.6)/.9)*.55;
  em.style.transform=`rotate(${{-6+6*doux((t-16.6)/1.6)}}deg) scale(${{.9+.1*doux((t-16.6)/1.6)}})`;
}}
</script></body></html>"""


def son():
    """Musique DIG16 (même compositeur que la présentation) + effets accordés en Do majeur 7, mixés dessous."""
    env = dict(os.environ, DUREE=str(TOTAL + .5))
    subprocess.run(["python3", os.path.join(CD, "videos", "dig16-presentation", "musique.py")], check=True, env=env, cwd=ICI)
    sr = 44100
    n = int(sr * (TOTAL + .5))
    fx = np.zeros(n)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)

    def pluck(f, debut, amp):
        tt = np.arange(int(1.8 * sr)) / sr
        w = (np.sin(2 * np.pi * f * tt) + .3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 3.4) * np.minimum(1, tt / .008)
        i = int(debut * sr)
        fx[i:i + len(w)] += amp * w[:n - i]

    rng = np.random.default_rng(16)
    # souffle doux au balayage (bruit filtré qui monte puis retombe, 8,0 → 9,8 s)
    d, a = int(1.9 * sr), int(7.95 * sr)
    bruit = np.convolve(rng.standard_normal(d), np.ones(60) / 60, mode="same")
    env_s = np.sin(np.linspace(0, np.pi, d)) ** 2
    fx[a:a + d] += .5 * bruit * env_s
    pluck(hz(76), 9.7, .16)  # Mi : arrivée du site refait
    for i, m in enumerate((72, 76, 79)):  # Do, Mi, Sol : les trois encarts
        pluck(hz(m), 12.35 + i * .75, .14)
    for m in (60, 64, 67, 71):  # accord final Do maj7, doux
        pluck(hz(m), 16.4, .07)
    fx = np.clip(fx, -1, 1)
    import wave
    with wave.open(os.path.join(ICI, "effets.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((fx * 32767).astype(np.int16).tobytes())
    sortie = os.path.join(ICI, "son.m4a")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ICI, "musique.wav"), "-i", os.path.join(ICI, "effets.wav"),
                    "-filter_complex",
                    "[0:a]volume=-6dB[mu];[1:a]volume=-11dB,aecho=0.8:0.6:120:0.25[fx];"
                    f"[mu][fx]amix=inputs=2:normalize=0,atrim=0:{TOTAL},afade=t=out:st={TOTAL - 1.6}:d=1.6,"
                    "alimiter=limit=0.89,aformat=sample_rates=44100:channel_layouts=stereo[out]",
                    "-map", "[out]", "-c:a", "aac", "-b:a", "192k", sortie], check=True)
    return sortie


def fabriquer(controle_seul=False):
    ctrl = os.path.join(ICI, "controle")
    os.makedirs(ctrl, exist_ok=True)
    instants = [0, .6, 1.6, 2.6, 3.6, 4.4, 6.0, 7.8, 8.6, 9.0, 10.5, 12.0, 12.4, 13.2, 14.6, 16.2, 16.6, 18.0, 19.9]
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(page(), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        polices = pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)")
        if not any("Instrument" in x for x in polices) or not any("Geist" in x for x in polices):
            sys.exit(f"ALERTE : polices non chargées {polices}")
        fautes = pg.evaluate("""[...document.querySelectorAll('.bloc,.lien,.lieu')].map(e=>{
            const r=e.getBoundingClientRect();
            return (r.right>1080-80||r.left<80||e.scrollWidth>e.clientWidth+1||r.bottom>1920-150)?e.id:null}).filter(Boolean)""")
        if fautes:
            nav.close()
            sys.exit(f"ALERTE : textes hors marge {fautes}")
        for t in instants:
            pg.evaluate(f"seek({t})")
            pg.screenshot(path=os.path.join(ctrl, f"t{t:04.1f}.jpg"), type="jpeg", quality=88)
        if controle_seul:
            nav.close()
            return
        pg.evaluate(f"seek({AFFICHE})")
        affiche = pg.screenshot(type="jpeg", quality=95)
        with open(os.path.join(ICI, "brag.jpg"), "wb") as f:
            f.write(affiche)
        audio = son()
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                               "-i", "-", "-i", audio, "-af", "loudnorm=I=-15:TP=-1.5:LRA=9", "-c:v", "libx264", "-preset", "slow",
                               "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-ar", "44100", "-c:a", "aac",
                               "-b:a", "192k", "-shortest", os.path.join(ICI, "brag.mp4")], stdin=subprocess.PIPE)
        for i in range(int(FPS * TOTAL)):
            if i == 0:  # l'affiche remplace l'image 0 (miniature partout, durée inchangée)
                ff.stdin.write(affiche)
                continue
            pg.evaluate(f"seek({i / FPS:.4f})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
        nav.close()
    ff.stdin.close()
    ff.wait()
    for x in ("musique.wav", "effets.wav", "son.m4a"):
        os.remove(os.path.join(ICI, x))
    print("brag.mp4 :", TOTAL, "s")


if __name__ == "__main__":
    fabriquer(controle_seul="--controle" in sys.argv)
