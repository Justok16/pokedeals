"""Vidéo de lancement verticale de dig16.fr (skill brag-slim, 20/10/2026) : plan dans brag-plan.md.

1080 × 1920, 30 i/s, ~22 s, voix off « Algieba » (gemini-3.8-flash-tts, voix validée par l'utilisateur le 08/10 ;
voix off demandée le 20/10), musique DIG16 baissée sous la voix + effets dans la même tonalité.
Chaque phrase est synthétisée seule, transcrite et comparée au texte (faster-whisper) ; l'animation suit la voix.
Tout vient du site : textes de l'accueil, faux vieux site de la section avant/après, capture de démonstration
(entreprise fictive), chiffres des encarts de confiance. Polices du site incorporées.

Usage : python3 fabriquer.py [--controle]   (--controle : seulement les images fixes, sans rendu)
Écrit brag.mp4, brag.jpg (affiche = image 0) et des images de contrôle dans controle/ (non versionnées).
"""

import json
import os
import subprocess
import sys

import numpy as np
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
CD = os.path.normpath(os.path.join(ICI, "..", ".."))
sys.path.insert(0, os.path.join(CD, "videos", "conseils"))
from fabriquer import CHROME, css_polices, data, duree, empreinte_svg, marque_mal_dite, voix  # noqa: E402

FPS = 30
# Phrases dites (8) : l'écran suit chacune. « DIG16 » écrit pour être bien prononcé.
PHRASES = [
    "Vos clients vous cherchent sur leur téléphone.",
    "Ils vous trouvent ?",
    "Votre site aujourd'hui : daté, minuscule sur un téléphone.",
    "Je le refais. Le même, refait par Dig seize.",
    "Zéro euro de création.",
    "Sept jours pour être en ligne.",
    "Et cent pour cent à votre nom.",
    "Je refais votre page d'accueil gratuitement. Vous décidez ensuite. Dig seize point F R.",
]
ECARTS = [0.15, 0.55, 0.45, 0.35, 0.15, 0.15, 0.45]  # silence après chaque phrase (sauf la dernière)
DEBUT = 0.35
FIN = 2.0
SITE = os.path.join(CD, "site-dig")


def page(debuts, fin_voix):
    signature = data(os.path.join(SITE, "img", "marque", "signature-ivoire@2x.png"), "image/png")
    vitrine = data(os.path.join(SITE, "img", "vitrine-visite-tel.webp"), "image/webp")
    emp = empreinte_svg(620, opacite=1.0, ident="f")
    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css_polices()}</style><style>
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
#emp{{position:absolute;left:300px;top:1010px;opacity:0}}
.demo{{position:absolute;left:84px;right:84px;top:548px;text-align:center;font:400 30px Geist,'Geist Fallback',sans-serif;color:#8a8275;opacity:0}}
.lien{{position:absolute;left:84px;right:84px;top:800px;font:500 76px Geist,'Geist Fallback',sans-serif;letter-spacing:-.01em;opacity:0}}
.lien span{{color:#c8a46e}}
.lieu{{position:absolute;left:84px;right:84px;top:900px;font:400 40px Geist,'Geist Fallback',sans-serif;color:#a8a093;opacity:0}}
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
const D=__D__, F=__F__;  // débuts des 8 phrases de la voix ; F = fin des phrases
function seek(t){{
  t0=t;
  const B1=D[2]-.3, B2=D[3]-.35, B3=D[4]-.3, B4=D[7]-.3;
  // 1. accroche (la 1re ligne est déjà là à l'image 0 ; la 2e arrive avec la voix)
  const e1=$('h1');e1.style.opacity=Math.min(1,doux((B1-t)/.3));e1.style.transform='none';
  e1.querySelector('.l2').style.opacity=doux((t-D[1]+.1)/.4);
  // 2. avant
  vis('t2',B1+.15,B2-.05);
  const tel=$('tel'),ot=Math.min(doux((t-B1)/.6),doux((B3+.1-t)/.4));
  tel.style.opacity=ot;tel.style.transform=`translateY(${{(1-doux((t-B1)/.9))*160 - doux((t-B3+.3)/.6)*60}}px)`;
  // 3. balayage puis après
  const w=doux((t-B2-.1)/1.6);
  $('nouveau').style.clipPath=`inset(${{(1-w)*100}}% 0 0 0)`;
  const sc=$('scan');sc.style.top=`calc(${{(1-w)*100}}% - 2px)`;sc.style.opacity=(t>B2&&w<1)?1:Math.max(0,1-(t-B2-1.7)/.3)*(t>B2?1:0);
  vis('t3',B2+.3,B3);
  $('demo').style.opacity=Math.min(doux((t-B2-1.5)/.4),doux((B3-.05-t)/.3));
  // 4. trois encarts, chacun avec sa phrase
  const f=$('faits');f.style.opacity=Math.min(1,doux((B4-t)/.3));
  for(let i=0;i<3;i++){{const e=$('f'+i),a=D[4+i]-.2;e.style.opacity=doux((t-a)/.4);
   e.style.transform=`translateY(${{(1-doux((t-a)/.55))*50}}px)`}}
  // 5. fin
  vis('fin',B4+.02,999);
  const of=doux((t-B4-.6)/.5);$('lien').style.opacity=of;$('lieu').style.opacity=doux((t-B4-.9)/.5);
  const em=$('emp');em.style.opacity=doux((t-B4-.3)/.9)*.55;
  em.style.transform=`rotate(${{-6+6*doux((t-B4-.3)/1.6)}}deg) scale(${{.9+.1*doux((t-B4-.3)/1.6)}})`;
}}
</script></body></html>"""
    return html.replace("__D__", json.dumps(debuts)).replace("__F__", str(fin_voix))


def son(debuts, fichiers, total):
    """Voix off + musique DIG16 (baissée sous la voix) + effets accordés en Do majeur 7, mixés dessous."""
    env = dict(os.environ, DUREE=str(total + .5))
    subprocess.run(["python3", os.path.join(CD, "videos", "dig16-presentation", "musique.py")], check=True, env=env, cwd=ICI)
    sr = 44100
    n = int(sr * (total + .5))
    fx = np.zeros(n)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)

    def pluck(f, debut, amp):
        tt = np.arange(int(1.8 * sr)) / sr
        w = (np.sin(2 * np.pi * f * tt) + .3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 3.4) * np.minimum(1, tt / .008)
        i = int(debut * sr)
        fx[i:i + len(w)] += amp * w[:n - i]

    rng = np.random.default_rng(16)
    b2 = debuts[3] - .35  # souffle doux pendant le balayage
    d, a = int(1.8 * sr), int((b2 + .05) * sr)
    bruit = np.convolve(rng.standard_normal(d), np.ones(60) / 60, mode="same")
    fx[a:a + d] += .5 * bruit * np.sin(np.linspace(0, np.pi, d)) ** 2
    pluck(hz(76), b2 + 1.7, .16)  # Mi : arrivée du site refait
    for i, m in enumerate((72, 76, 79)):  # Do, Mi, Sol : les trois encarts
        pluck(hz(m), debuts[4 + i] - .2, .14)
    for m in (60, 64, 67, 71):  # accord final Do maj7, doux
        pluck(hz(m), debuts[7] - .1, .07)
    fx = np.clip(fx, -1, 1)
    import wave
    with wave.open(os.path.join(ICI, "effets.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((fx * 32767).astype(np.int16).tobytes())
    entrees, filtres = [], []
    for i, (ch, d0) in enumerate(zip(fichiers, debuts)):
        entrees += ["-i", ch]
        filtres.append(f"[{i}:a]aresample=44100,adelay={int(d0 * 1000)}:all=1[v{i}]")
    k = len(fichiers)
    filtres.append("".join(f"[v{i}]" for i in range(k)) + f"amix=inputs={k}:normalize=0,apad,atrim=0:{total}[vx]")
    filtres.append("[vx]volume=1.3,asplit=2[vo][sc]")
    filtres.append(f"[{k}:a]volume=-12dB[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=25:release=400[md]")
    filtres.append(f"[{k + 1}:a]volume=-15dB,aecho=0.8:0.6:120:0.25[fx]")
    filtres.append(f"[vo][md][fx]amix=inputs=3:normalize=0,atrim=0:{total},afade=t=out:st={total - 1.4}:d=1.4,"
                   "alimiter=limit=0.89,aformat=sample_rates=44100:channel_layouts=stereo[out]")
    sortie = os.path.join(ICI, "son.m4a")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entrees, "-i", os.path.join(ICI, "musique.wav"),
                    "-i", os.path.join(ICI, "effets.wav"), "-filter_complex", ";".join(filtres),
                    "-map", "[out]", "-c:a", "aac", "-b:a", "192k", sortie], check=True)
    return sortie


def verifier_voix(fichiers, textes):
    """Transcrit chaque phrase (faster-whisper) et compare au texte voulu, à l'oreille : les terminaisons muettes
    du français (« ils vous trouvent » = « il vous trouve », constaté le 20/10) ne comptent pas.
    Renvoie les fichiers où la marque est mal dite (à resynthétiser) ; vide si tout est bon."""
    import difflib
    import re

    from faster_whisper import WhisperModel

    m = WhisperModel("small", compute_type="int8")

    def oral(s):
        s = s.lower().replace("dig16", "dig seize").replace("dig 16", "dig seize")
        # même prononciation que les vidéos conseil validées le 18/10, que Whisper écrit « dix-seize »
        for a in ("dix-seize", "dixseize", "dix seize", "dixez"):
            s = s.replace(a, "dig seize")
        for a, b in (("100 %", " cent pour cent "), ("100%", " cent pour cent "), ("€", " euro "), ("100", " cent "),
                     ("0", " zéro "), ("7", " sept ")):  # Whisper écrit les nombres en chiffres
            s = s.replace(a, b)
        mots = re.sub(r"[^a-zàâçéèêëîïôûùüÿœ0-9 ]", " ", s).split()
        return [re.sub(r"(ent|es|e|s|t|x)$", "", w) if len(w) > 3 else w.rstrip("s") for w in mots]

    a_refaire = []
    for ch, txt in zip(fichiers, textes):
        entendu = " ".join(x.text for x in m.transcribe(ch, language="fr", beam_size=5)[0])
        ratio = difflib.SequenceMatcher(None, oral(entendu), oral(txt)).ratio()
        print(f"voix {os.path.basename(ch)} : « {entendu.strip()} » ({ratio:.2f})")
        if ratio < 0.75 or duree(ch) > 9:  # 23/10 : phrase mal dite (« Je l'en fais… Dx16 ») → resynthèse, pas d'arrêt
            print(f"phrase mal dite {os.path.basename(ch)} ({ratio:.2f}, {duree(ch):.1f} s) → à refaire")
            a_refaire.append(ch)
            continue
        # 22/10 : « oral » assimile « dixseize » à la marque, donc la marque est contrôlée à part, sur le texte brut
        if "dig seize" in txt.lower() and marque_mal_dite(entendu):
            print(f"marque mal dite dans {os.path.basename(ch)} : « {entendu.strip()} » → à refaire")
            a_refaire.append(ch)
    return a_refaire


def calage():
    """Synthèse (en cache dans voix/), vérification par transcription, puis débuts de chaque phrase."""
    os.makedirs(os.path.join(ICI, "voix"), exist_ok=True)
    fichiers = []
    for i, ph in enumerate(PHRASES):
        ch = os.path.join(ICI, "voix", f"l{i}.wav")
        voix(ph, ch)
        fichiers.append(ch)
    for essai in range(5):  # 22/10 : une phrase mal dite (marque ou texte) est resynthétisée (5 essais au plus)
        a_refaire = verifier_voix(fichiers, PHRASES)
        if not a_refaire:
            break
        if essai == 4:
            sys.exit(f"ALERTE voix : phrase ou marque encore mal dite après 5 essais ({[os.path.basename(c) for c in a_refaire]})")
        for ch in a_refaire:
            os.remove(ch)
            voix(PHRASES[fichiers.index(ch)], ch)
    debuts, t = [], DEBUT
    for i, ch in enumerate(fichiers):
        debuts.append(round(t, 3))
        t += duree(ch) + (ECARTS[i] if i < len(ECARTS) else 0)
    fin_voix = round(t, 3)
    total = round(fin_voix + FIN, 2)
    if not 15 <= total <= 30:
        sys.exit(f"ALERTE durée {total} s")
    return fichiers, debuts, fin_voix, total


def fabriquer(controle_seul=False):
    ctrl = os.path.join(ICI, "controle")
    os.makedirs(ctrl, exist_ok=True)
    fichiers, debuts, fin_voix, total = calage()
    print("débuts", debuts, "total", total)
    instants = sorted({0.0} | {round(d + x, 1) for d in debuts for x in (.05, .9)} | {round(total - .1, 1)})
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(page(debuts, fin_voix), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        polices = pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)")
        if not any("Instrument" in x for x in polices) or not any("Geist" in x for x in polices):
            sys.exit(f"ALERTE : polices non chargées {polices}")
        fautes = pg.evaluate("""[...document.querySelectorAll('.bloc,.lien,.lieu')].map(e=>{
            const r=e.getBoundingClientRect();
            return (r.right>1080-80||r.left<80||e.scrollWidth>e.clientWidth+1||r.bottom>1920-150)?e.id:null}).filter(Boolean)""")
        # 23/10 : zone visible d'un Reel (guide Meta : 14 % du haut et 35 % du bas peuvent être couverts par l'appli) :
        # le lien final finit avant 1 248 px, les autres textes avant 1 500 px
        fautes += pg.evaluate("""[...document.querySelectorAll('.bloc,.lien,.lieu,.demo')].map(e=>{
            const r=e.getBoundingClientRect(), lim=(e.id==='lien'||e.id==='lieu')?1248:1500;
            return (r.top<269||r.bottom>lim)?'zone cachée : '+e.id:null}).filter(Boolean)""")
        if fautes:
            nav.close()
            sys.exit(f"ALERTE : textes hors marge {fautes}")
        for t in instants:
            pg.evaluate(f"seek({t})")
            pg.screenshot(path=os.path.join(ctrl, f"t{t:04.1f}.jpg"), type="jpeg", quality=88)
        if controle_seul:
            nav.close()
            return
        pg.evaluate(f"seek({debuts[1] + .45})")  # accroche complète (2e ligne arrivée), avant le fondu de sortie
        affiche = pg.screenshot(type="jpeg", quality=95)
        with open(os.path.join(ICI, "brag.jpg"), "wb") as f:
            f.write(affiche)
        audio = son(debuts, fichiers, total)
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                               "-i", "-", "-i", audio, "-af", "loudnorm=I=-15:TP=-1.5:LRA=9", "-c:v", "libx264", "-preset", "slow",
                               "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-ar", "44100", "-c:a", "aac",
                               "-b:a", "192k", "-shortest", os.path.join(ICI, "brag.mp4")], stdin=subprocess.PIPE)
        for i in range(int(FPS * total)):
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
    print("brag.mp4 :", total, "s")


if __name__ == "__main__":
    fabriquer(controle_seul="--controle" in sys.argv)
