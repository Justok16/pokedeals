#!/usr/bin/env python3
"""Vidéo verticale « Le test du pouce » (09/10/2026) : Reel Instagram, Short YouTube, TikTok, statut WhatsApp.

1080 × 1920, ~17 s, voix « Algieba » (validée par l'utilisateur le 08/10), musique originale DIG16 (musique.py de la
vidéo de présentation), charte et empreinte dorée de la campagne (62-campagne-test-du-pouce.md).
Aucun chiffre, aucun nom d'entreprise réel : recherche et numéro de téléphone fictifs ; le bas de la démo
(note et avis fictifs de la maquette) est masqué : pas d'avis inventé dans une publicité.

Usage : python3 fabriquer.py   (depuis ce dossier ; voix-Algieba.wav doit exister, voir LISEZMOI.md)
Écrit test-du-pouce.mp4 et des images de contrôle dans controle/.
Les débuts de phrase sont repérés automatiquement dans la voix (pauses détectées par FFmpeg).
"""

import base64
import os
import re
import subprocess
import sys

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
CD = os.path.normpath(os.path.join(ICI, "..", ".."))
sys.path.insert(0, os.path.join(CD, "outils", "marque"))
from empreinte import empreinte_svg  # noqa: E402

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FPS = 30
DEBUT_VOIX = 0.5  # s de silence avant la voix
FIN = 2.2  # s d'écran final après la voix
VOIX = os.path.join(ICI, "voix-Algieba.wav")


def data(chemin, mime):
    with open(chemin, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def segments_voix():
    """Paroles = intervalles entre les pauses de plus de 0,22 s."""
    sortie = subprocess.run(["ffmpeg", "-i", VOIX, "-af", "silencedetect=noise=-38dB:d=0.22", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    debuts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", sortie)]
    fins = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sortie)]
    duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VOIX],
                                 capture_output=True, text=True).stdout)
    paroles, t = [], 0.0
    for d, f in zip(debuts, fins):
        if d > t + 0.05:
            paroles.append((t, d))
        t = f
    if duree > t + 0.05:
        paroles.append((t, duree))
    return paroles, duree


def page(rep, t3b):
    """rep : débuts (s, dans la vidéo) des 6 scènes ; t3b : début de « Ou votre numéro… »."""
    emp_grand = empreinte_svg(820, opacite=1.0, ident="g")
    emp_petit = empreinte_svg(150, opacite=1.0, ident="p")
    emp_fin = empreinte_svg(700, opacite=1.0, ident="f")
    signature = data(os.path.join(CD, "site-dig", "img", "marque", "signature-ivoire@2x.png"), "image/png")
    vitrine = data(os.path.join(CD, "site-dig", "img", "vitrine-paysagiste-tel.webp"), "image/webp")
    resultats = "".join(
        f'<div class="res"><i style="width:{w}%"></i><b></b><b style="width:60%"></b></div>' for w in (72, 58, 66))
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&display=block" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;background:#0f0e0c;color:#efe9df;font-family:Geist,sans-serif;position:relative;
 background-image:radial-gradient(80% 50% at 90% 0%,rgba(200,164,110,.16),rgba(200,164,110,0) 70%),
 radial-gradient(70% 40% at 0% 100%,rgba(200,164,110,.08),rgba(200,164,110,0) 70%)}}
.sc{{position:absolute;inset:0;opacity:0}}
.titre{{position:absolute;left:84px;right:84px;font:400 116px/1 'Instrument Serif';letter-spacing:-.025em;text-wrap:balance}}
.titre em{{color:#d9bb8a;font-style:italic}}
.sous{{position:absolute;left:84px;right:84px;font:300 46px/1.35 Geist;color:#cfc6b8;text-wrap:balance}}
.tel{{position:absolute;left:50%;width:600px;height:1000px;margin-left:-300px;border-radius:76px;padding:16px;
 background:linear-gradient(160deg,#3a352d,#1a1814 40%,#2a2620);box-shadow:0 60px 120px rgba(0,0,0,.6),0 0 0 2px rgba(200,164,110,.35)}}
.ecran{{position:relative;width:100%;height:100%;border-radius:62px;background:#14120f;overflow:hidden;padding:96px 30px 30px}}
.ecran:before{{content:"";position:absolute;top:26px;left:50%;margin-left:-70px;width:140px;height:38px;border-radius:19px;background:#000}}
.barre{{height:80px;border-radius:40px;background:#efe9df;color:#14110d;display:flex;align-items:center;gap:16px;padding:0 30px;font:400 32px Geist}}
.barre svg{{flex:none}}
.curseur{{display:inline-block;width:3px;height:36px;background:#14110d;margin-left:2px;vertical-align:middle}}
.res{{margin-top:28px;height:132px;border-radius:24px;background:#201d18;padding:28px}}
.res i{{display:block;height:22px;border-radius:11px;background:#4a453c}}
.res b{{display:block;height:14px;width:88%;border-radius:7px;background:#2e2b25;margin-top:20px}}
.vide{{margin-top:28px;height:132px;border-radius:24px;border:3px dashed rgba(200,164,110,.7);display:flex;align-items:center;justify-content:center}}
.numero{{margin-top:60px;border-radius:28px;background:#201d18;padding:40px 34px;text-align:center}}
.numero p{{font:400 30px Geist;color:#a8a093}}
.numero strong{{display:block;font:500 54px Geist;letter-spacing:.04em;margin-top:16px;color:#efe9df}}
.croix{{position:absolute;width:150px;height:150px;border-radius:50%;background:#7a2e22;color:#fff;font:600 92px/150px Geist;text-align:center;
 box-shadow:0 20px 50px rgba(0,0,0,.5)}}
.onde{{position:absolute;width:120px;height:120px;border-radius:50%;border:4px solid #c8a46e}}
.vitrine{{position:absolute;inset:0;background:url({vitrine}) top center/cover no-repeat}}
.signature{{position:absolute;left:84px;top:90px;height:92px}}
.lien{{position:absolute;left:84px;right:84px;bottom:220px;font:500 58px Geist;letter-spacing:-.01em}}
.lien span{{color:#c8a46e}}
.bouton{{position:absolute;left:84px;bottom:110px;font:500 36px Geist;background:#c8a46e;color:#14110d;border-radius:999px;padding:22px 44px}}
</style></head><body>
<img class="signature" src="{signature}" alt="DIG16">

<section class="sc" id="s0">
 <div id="g0" style="position:absolute;left:130px;top:470px">{emp_grand}</div>
 <h1 class="titre" style="top:250px">Prenez votre <em>téléphone.</em></h1>
</section>

<section class="sc" id="s1">
 <h1 class="titre" style="top:230px;font-size:96px">Tapez votre métier <em>et votre ville.</em></h1>
 <div class="tel" style="top:600px"><div class="ecran">
  <div class="barre"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#655e54" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><span id="frappe"></span><span class="curseur" id="cur"></span></div>
 </div></div>
</section>

<section class="sc" id="s2">
 <h1 class="titre" style="top:250px;font-size:150px">Vous êtes <em>où ?</em></h1>
 <div class="tel" style="top:600px"><div class="ecran">
  <div class="barre"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#655e54" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>menuisier cognac</div>
  {resultats}<div class="vide" id="vide">{emp_petit}</div>
 </div></div>
</section>

<section class="sc" id="s3">
 <h1 class="titre" style="top:230px;font-size:104px" id="t3a">Pas là ?</h1>
 <p class="sous" style="top:380px" id="t3b">Ou votre numéro ne s'appelle pas d'un geste ?</p>
 <div class="tel" style="top:640px"><div class="ecran">
  <div class="numero"><p>Téléphone</p><strong>05 •• •• •• ••</strong></div>
  <div class="onde" id="onde" style="left:210px;top:250px"></div>
  <div class="croix" id="croix" style="left:195px;top:430px">×</div>
 </div></div>
</section>

<section class="sc" id="s4">
 <h1 class="titre" style="top:230px;font-size:100px">Je refais <em>gratuitement</em> votre page d'accueil.</h1>
 <div class="tel" style="top:700px"><div class="ecran" style="padding:0"><div class="vitrine" id="vitrine"></div><div style="position:absolute;left:0;right:0;bottom:0;height:330px;background:linear-gradient(rgba(20,18,15,0),#14120f 55%)"></div></div></div>
</section>

<section class="sc" id="s5">
 <div id="g5" style="position:absolute;left:190px;top:520px">{emp_fin}</div>
 <h1 class="titre" style="top:250px;font-size:132px">Le test <em>du pouce.</em></h1>
 <div class="lien">dig16<span>.fr</span>/test-du-pouce</div>
 <div class="bouton">Faites le test en 30 secondes</div>
</section>

<script>
const R={rep}, T3B={t3b};
const RECH="menuisier cognac";
const cl=(x,a,b)=>Math.max(a,Math.min(b,x));
const doux=x=>{{x=cl(x,0,1);return x*x*(3-2*x)}};
function voile(id,t,a,b){{
  const e=document.getElementById(id);const o=Math.min(doux((t-a)/.3),b<1e9?doux((b-t)/.3):1);
  e.style.opacity=o;e.style.transform=`translateY(${{(1-doux((t-a)/.45))*40}}px)`;return t-a;
}}
function seek(t){{
  const f=R.concat([1e10]);
  for(let i=0;i<6;i++) voile('s'+i,t,f[i],f[i+1]);
  const u0=t-f[0]; document.getElementById('g0').style.transform=`scale(${{.92+.08*doux(u0/1.6)}})`;
  const u1=t-f[1]; const n=Math.round(cl((u1-.35)/1.6,0,1)*RECH.length);
  document.getElementById('frappe').textContent=RECH.slice(0,n);
  document.getElementById('cur').style.opacity=(Math.floor(u1*2.4)%2)?0:1;
  const u2=t-f[2]; document.getElementById('vide').style.boxShadow=`0 0 ${{40*Math.abs(Math.sin(u2*3))}}px rgba(200,164,110,.55)`;
  const u3=t-f[3];
  document.getElementById('t3b').style.opacity=doux((t-T3B)/.35);
  const ph=((u3-.8)%1.4)/1.4; const on=document.getElementById('onde');
  on.style.opacity=u3>.8?(1-ph):0; on.style.transform=`scale(${{.4+ph*1.4}})`;
  document.getElementById('croix').style.opacity=doux((u3-1.3)/.25);
  document.getElementById('croix').style.transform=`scale(${{.6+.4*doux((u3-1.3)/.25)}})`;
  const u4=t-f[4]; document.getElementById('vitrine').style.backgroundPosition=`center ${{-cl(u4/2.6,0,1)*0}}px`;
  document.getElementById('vitrine').style.transform=`scale(${{1.06-.06*doux(u4/2.6)}})`;
  const u5=t-f[5]; document.getElementById('g5').style.transform=`rotate(${{-6+6*doux(u5/1.2)}}deg) scale(${{.9+.1*doux(u5/1.2)}})`;
}}
</script></body></html>"""


def main():
    os.chdir(ICI)
    paroles, duree_voix = segments_voix()
    # 8 morceaux de parole attendus : 1 Prenez / 2 Tapez / 3 Vous êtes où / 4 Pas là / 5 Ou votre numéro /
    # 6 Je refais / 7 Le test du pouce / 8 sur Dig seize point F R
    if len(paroles) != 8:
        sys.exit(f"ALERTE : {len(paroles)} morceaux de parole au lieu de 8 : {paroles}")
    d = [DEBUT_VOIX + a for a, _ in paroles]
    scenes = [0.0, d[1] - .15, d[2] - .15, d[3] - .15, d[5] - .2, d[6] - .2]
    duree = round(DEBUT_VOIX + duree_voix + FIN, 2)
    html = page(scenes, d[4] - .1)
    env = dict(os.environ, DUREE=str(duree + .5))
    subprocess.run(["python3", os.path.join(CD, "videos", "dig16-presentation", "musique.py")], check=True, env=env)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VOIX, "-i", "musique.wav", "-filter_complex",
                    f"[0:a]aresample=44100,adelay={int(DEBUT_VOIX * 1000)}:all=1,apad,atrim=0:{duree},volume=1.3,asplit=2[vx][sc];"
                    "[1:a]volume=-13dB[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=25:release=400[md];"
                    f"[vx][md]amix=inputs=2:normalize=0,atrim=0:{duree},afade=t=out:st={duree - 1.2}:d=1.2,"
                    "alimiter=limit=0.89,aformat=sample_rates=44100:channel_layouts=stereo[out]",
                    "-map", "[out]", "-c:a", "aac", "-b:a", "192k", "son.m4a"], check=True)
    os.makedirs("controle", exist_ok=True)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                           "-i", "-", "-i", "son.m4a", "-af", "loudnorm=I=-15:TP=-1.5:LRA=9", "-c:v", "libx264",
                           "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                           "-ar", "44100", "-c:a", "aac", "-b:a", "192k", "-shortest", "test-du-pouce.mp4"], stdin=subprocess.PIPE)
    controles = {round(s + 1.2, 1) for s in scenes} | {round(duree - .3, 1)}
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(html, wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        polices = pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)")
        if not any("Instrument" in x for x in polices) or not any("Geist" in x for x in polices):
            sys.exit(f"ALERTE : polices non chargées {polices}")
        for i in range(int(FPS * duree)):
            t = i / FPS
            pg.evaluate(f"seek({t:.4f})")
            img = pg.screenshot(type="jpeg", quality=93)
            ff.stdin.write(img)
            if round(t, 1) in controles and abs(t - round(t, 1)) < 1 / FPS / 2:
                with open(f"controle/t{t:04.1f}.jpg", "wb") as f:
                    f.write(img)
        # débordements : chaque titre et sous-titre doit tenir dans 1080 px avec 84 px de marge
        fautes = pg.evaluate("""[...document.querySelectorAll('.titre,.sous,.lien,.bouton')].map(e=>{const r=e.getBoundingClientRect();
            return (r.right>1080-80||r.left<80||e.scrollWidth>e.clientWidth+1)?e.textContent:null}).filter(Boolean)""")
        nav.close()
    ff.stdin.close()
    ff.wait()
    if fautes:
        sys.exit(f"ALERTE : textes hors marge {fautes}")
    print("test-du-pouce.mp4 :", duree, "s, scènes", [round(x, 2) for x in scenes])


if __name__ == "__main__":
    main()
