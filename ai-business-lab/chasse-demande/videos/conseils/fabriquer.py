#!/usr/bin/env python3
"""Série « Les conseils DIG16 » (18/10/2026) : vidéos verticales courtes tirées du guide
https://dig16.fr/site-internet-artisan/ (choix B de l'utilisateur : vidéos animées avec voix de synthèse, sans se filmer).

1080 × 1920, 30 i/s, voix « Algieba » (gemini-3.8-flash-tts, validée par l'utilisateur le 08/10) via /api/voix du relais,
musique originale DIG16 (../dig16-presentation/musique.py) baissée sous la voix, charte du site (polices incorporées).
Une phrase = une scène : chaque phrase est synthétisée séparément, donc le texte à l'écran suit exactement la voix.
Rien d'inventé : chaque phrase reprend le guide (sources citées dans le guide) ; aucun chiffre, aucun nom réel.

Usage : python3 fabriquer.py [numéro…]   (depuis n'importe où ; cookie du relais dans /tmp/cj.txt)
Écrit conseil-N.mp4, et des images de contrôle dans controle/ (non versionnées).
Contrôles bloquants : polices chargées, aucun texte hors de la marge de 84 px, durée 12-35 s.
"""

import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
CD = os.path.normpath(os.path.join(ICI, "..", ".."))
sys.path.insert(0, os.path.join(CD, "outils", "marque"))
from empreinte import empreinte_svg  # noqa: E402

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
RELAIS = "https://relais-dig-justok1.vercel.app/api/voix"
POLICES = os.path.join(CD, "site-dig", "moteur", "polices")
FPS = 30
DEBUT = 0.6  # silence avant la première phrase
PAUSE = 0.38  # silence entre deux phrases
FIN = 2.4  # écran final après la voix
# Pas de consigne de style : le modèle la lisait à voix haute (constaté le 18/10 par transcription).

# Chaque conseil : liste de scènes (texte dit, texte affiché avec *mots dorés*). La dernière scène est l'écran final.
SERIE = {
    1: {"titre": "Votre site est-il vraiment à vous ?", "scenes": [
        ("Votre site internet est-il vraiment à vous ?", "Votre site est-il vraiment *à vous ?*"),
        ("Tout dépend d'un détail : le nom de domaine.", "Tout dépend d'un détail : *le nom de domaine.*"),
        ("S'il est au nom de votre prestataire, vous ne pouvez pas partir sans perdre votre adresse.",
         "Au nom du prestataire ? Impossible de partir *sans perdre votre adresse.*"),
        ("Avant de signer, demandez-le par écrit : sera-t-il à mon nom ?", "Avant de signer, demandez-le *par écrit.*"),
        ("Le guide complet est sur Dig seize point F R.", None)]},
    2: {"titre": "Les 5 pages qui comptent", "scenes": [
        ("Un site d'artisan n'a pas besoin de vingt pages. Cinq suffisent.", "Pas vingt pages. *Cinq suffisent.*"),
        ("L'accueil, avec votre numéro bien visible.", "L'accueil, avec votre *numéro bien visible.*"),
        ("Une page par service, et vos réalisations en vraies photos.",
         "Vos services, et vos réalisations *en vraies photos.*"),
        ("Qui vous êtes, votre secteur, et un moyen simple de demander un devis.",
         "Qui vous êtes, et un devis *simple à demander.*"),
        ("Le guide complet est sur Dig seize point F R.", None)]},
    3: {"titre": "Les avis Google, sans tricher", "scenes": [
        ("Les avis Google, c'est souvent ce qu'un client lit avant de vous appeler.",
         "Vos avis Google, *on les lit avant d'appeler.*"),
        ("Le bon réflexe : demander un avis à chaque client satisfait, avec un lien direct.",
         "Demandez un avis à chaque *client satisfait.*"),
        ("Et répondez à chaque avis, même mitigé, poliment.", "Répondez à chaque avis, *même mitigé.*"),
        ("Un avis payé ou inventé ? Les règles de Google l'interdisent.", "Avis payé ou inventé ? *Interdit par Google.*"),
        ("Le guide complet est sur Dig seize point F R.", None)]},
    4: {"titre": "3 questions avant de signer", "scenes": [
        ("Avant de signer pour un site internet, posez au moins trois questions.", "Avant de signer, *trois questions.*"),
        ("Un : le nom de domaine sera-t-il à mon nom ?", "Le nom de domaine sera-t-il *à mon nom ?*"),
        ("Deux : combien de temps suis-je engagé ?", "Combien de temps *suis-je engagé ?*"),
        ("Trois : si j'arrête, est-ce que je récupère mon site ?", "Si j'arrête, je *récupère mon site ?*"),
        ("Les sept questions sont dans le guide, sur Dig seize point F R.", None)]},
    5: {"titre": "Une page Facebook suffit ?", "scenes": [
        ("J'ai déjà une page Facebook, ça suffit, non ?", "Une page Facebook, *ça suffit ?*"),
        ("La fiche Google est indispensable pour être trouvé sur Maps.",
         "La fiche Google : *indispensable* pour Maps."),
        ("Mais ces pages ne vous appartiennent pas : la plateforme peut changer ses règles.",
         "Mais ces pages *ne vous appartiennent pas.*"),
        ("Votre site, à votre nom, reste à vous.", "Votre site, à votre nom, *reste à vous.*"),
        ("Le guide complet est sur Dig seize point F R.", None)]},
}


def data(chemin, mime):
    with open(chemin, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def css_polices():
    css = open(os.path.join(POLICES, "instrumentserif-geist-geistmono.css"), encoding="utf-8").read()
    return re.sub(r"url\(/moteur/polices/([^)]+)\)",
                  lambda m: f"url({data(os.path.join(POLICES, m.group(1)), 'font/woff2')})", css)


def voix(texte, chemin):
    """Synthèse d'une phrase (mise en cache : une phrase déjà dite n'est pas redemandée)."""
    if os.path.exists(chemin):
        return
    url = RELAIS + "?" + urllib.parse.urlencode({"texte": texte, "voix": "Algieba", "modele": "gemini-3.8-flash-tts"})
    for essai in range(8):  # quota gratuit par minute : on attend et on réessaie (constaté le 18/10)
        brut_rep = subprocess.run(["curl", "-s", "-b", "/tmp/cj.txt", "--max-time", "120", url],
                                  capture_output=True, text=True).stdout
        try:
            rep = json.loads(brut_rep)
        except ValueError:
            sys.exit(f"ALERTE voix (cookie du relais ?) : {brut_rep[:200]}")
        if "audio" in rep or "429" not in json.dumps(rep):
            break
        time.sleep(70)
    if "audio" not in rep:
        sys.exit(f"ALERTE voix : {rep}")
    brut = base64.b64decode(rep["audio"])
    tmp = chemin + ".brut"
    with open(tmp, "wb") as f:
        f.write(brut)
    fmt = [] if brut[:4] == b"RIFF" else ["-f", "s16le", "-ar", "24000", "-ac", "1"]
    # retire les silences de début et de fin pour un enchaînement régulier
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *fmt, "-i", tmp, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse", "-ar", "24000", "-ac", "1", chemin],
                   check=True)
    os.remove(tmp)


def verifier_voix(fichiers, textes):
    """Transcrit chaque phrase (faster-whisper, local) et refuse si le texte entendu s'écarte du texte voulu."""
    import difflib

    from faster_whisper import WhisperModel

    m = WhisperModel("small", compute_type="int8")
    def norm(s):
        s = s.lower().replace("dig seize point f r", "dig16 fr").replace("dig16.fr", "dig16 fr")
        return re.sub(r"[^a-zàâçéèêëîïôûùüÿœ0-9 ]", " ", s).split()

    for ch, txt in zip(fichiers, textes):
        entendu = " ".join(x.text for x in m.transcribe(ch, language="fr")[0])
        ratio = difflib.SequenceMatcher(None, norm(entendu), norm(txt)).ratio()
        if ratio < 0.75 or duree(ch) > 9:
            sys.exit(f"ALERTE voix {os.path.basename(ch)} : entendu « {entendu.strip()} » ({ratio:.2f}, {duree(ch):.1f} s)")


def duree(chemin):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", chemin],
                                capture_output=True, text=True).stdout)


def insecables(t):
    """Typographie française : apostrophe courbe, espace insécable avant « : ; ? ! » (sinon le signe tombe en début de ligne)."""
    return re.sub(r" ([:;?!])", "\u00a0\\1", t.replace("'", "\u2019"))


def dores(t):
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", insecables(t))


def page(n, cfg, debuts):
    emp = empreinte_svg(760, opacite=1.0, ident="f")
    signature = data(os.path.join(CD, "site-dig", "img", "marque", "signature-ivoire@2x.png"), "image/png")
    scenes = "".join(
        f'<section class="sc" id="s{i}"><h1 class="titre">{dores(aff)}</h1></section>'
        for i, (_, aff) in enumerate(cfg["scenes"][:-1]))
    fin = len(cfg["scenes"]) - 1
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css_polices()}</style><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;background:#0f0e0c;color:#efe9df;font-family:Geist,'Geist Fallback',sans-serif;position:relative;
 background-image:radial-gradient(80% 50% at 90% 0%,rgba(200,164,110,.16),rgba(200,164,110,0) 70%),
 radial-gradient(70% 40% at 0% 100%,rgba(200,164,110,.08),rgba(200,164,110,0) 70%)}}
.signature{{position:absolute;left:84px;top:90px;height:92px}}
.serie{{position:absolute;left:84px;right:84px;top:250px;font:500 30px 'Geist Mono','Geist Mono Fallback',monospace;letter-spacing:.2em;
 text-transform:uppercase;color:#a8a093;padding-top:22px;border-top:2px solid rgba(200,164,110,.55)}}
.sc{{position:absolute;inset:0;opacity:0}}
.titre{{position:absolute;left:84px;right:84px;top:720px;font:400 120px/1.02 'Instrument Serif','Instrument Serif Fallback',serif;
 letter-spacing:-.025em;text-wrap:balance}}
.titre em{{color:#d9bb8a;font-style:italic}}
.barre{{position:absolute;left:84px;right:84px;bottom:150px;height:6px;border-radius:3px;background:rgba(239,233,223,.12)}}
.barre i{{display:block;height:100%;border-radius:3px;background:#c8a46e;width:0}}
#emp{{position:absolute;left:160px;top:640px;opacity:0}}
.fin{{position:absolute;inset:0;opacity:0}}
.fin h2{{position:absolute;left:84px;right:84px;top:360px;font:400 104px/1.02 'Instrument Serif','Instrument Serif Fallback',serif;letter-spacing:-.02em;text-wrap:balance}}
.fin h2 em{{color:#d9bb8a;font-style:italic}}
.lien{{position:absolute;left:84px;right:84px;bottom:330px;font:500 64px Geist,'Geist Fallback',sans-serif;letter-spacing:-.01em}}
.lien span{{color:#c8a46e}}
.chemin{{position:absolute;left:84px;right:84px;bottom:262px;font:400 40px Geist,'Geist Fallback',sans-serif;color:#cfc6b8}}
</style></head><body>
<img class="signature" src="{signature}" alt="DIG16">
<div class="serie" id="serie">Le conseil DIG16 · {insecables(cfg['titre'])}</div>
{scenes}
<div id="emp">{emp}</div>
<section class="fin" id="fin"><h2>Le guide complet, <em>gratuit.</em></h2>
<div class="lien">dig16<span>.fr</span></div><div class="chemin">dig16.fr/site-internet-artisan</div></section>
<div class="barre"><i id="prog"></i></div>
<script>
const D={json.dumps(debuts)}, NF={fin}, TOTAL=window.TOTAL||1;
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), doux=x=>{{x=cl(x,0,1);return x*x*(3-2*x)}};
function seek(t){{
  for(let i=0;i<NF;i++){{
    const a=D[i]-.12, b=D[i+1]-.12, e=document.getElementById('s'+i);
    const o=Math.min(doux((t-a)/.3), doux((b-t)/.25));
    e.style.opacity=o; e.style.transform=`translateY(${{(1-doux((t-a)/.5))*46}}px)`;
  }}
  const f=D[NF]-.15, of=doux((t-f)/.45);
  document.getElementById('fin').style.opacity=of;
  document.getElementById('serie').style.opacity=1-of;
  const em=document.getElementById('emp'); em.style.opacity=of*.9;
  em.style.transform=`rotate(${{-6+6*doux((t-f)/1.2)}}deg) scale(${{.9+.1*doux((t-f)/1.2)}})`;
  document.getElementById('prog').style.width=(cl(t/TOTAL,0,1)*100)+'%';
}}
</script></body></html>"""


def fabriquer(n):
    cfg = SERIE[n]
    os.makedirs(os.path.join(ICI, "voix"), exist_ok=True)
    fichiers = []
    for i, (dit, _) in enumerate(cfg["scenes"]):
        ch = os.path.join(ICI, "voix", f"c{n}-{i}.wav")
        voix(dit, ch)
        fichiers.append(ch)
    verifier_voix(fichiers, [d for d, _ in cfg["scenes"]])
    debuts, t = [], DEBUT
    for ch in fichiers:
        debuts.append(round(t, 3))
        t += duree(ch) + PAUSE
    total = round(t - PAUSE + FIN, 2)
    if not 12 <= total <= 35:
        sys.exit(f"ALERTE durée {total} s pour le conseil {n}")
    # piste voix : phrases placées à leurs débuts
    entrees, filtres = [], []
    for i, (ch, d) in enumerate(zip(fichiers, debuts)):
        entrees += ["-i", ch]
        filtres.append(f"[{i}:a]aresample=44100,adelay={int(d * 1000)}:all=1[v{i}]")
    filtres.append("".join(f"[v{i}]" for i in range(len(fichiers))) +
                   f"amix=inputs={len(fichiers)}:normalize=0,apad,atrim=0:{total}[vx]")
    voix_wav = os.path.join(ICI, f"voix-{n}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entrees, "-filter_complex", ";".join(filtres), "-map", "[vx]",
                    voix_wav], check=True)
    env = dict(os.environ, DUREE=str(total + .5))
    subprocess.run(["python3", os.path.join(CD, "videos", "dig16-presentation", "musique.py")], check=True, env=env, cwd=ICI)
    son = os.path.join(ICI, f"son-{n}.m4a")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", voix_wav, "-i", os.path.join(ICI, "musique.wav"),
                    "-filter_complex",
                    f"[0:a]volume=1.3,asplit=2[vx][sc];[1:a]volume=-13dB[mu];"
                    "[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=25:release=400[md];"
                    f"[vx][md]amix=inputs=2:normalize=0,atrim=0:{total},afade=t=out:st={total - 1.2}:d=1.2,"
                    "alimiter=limit=0.89,aformat=sample_rates=44100:channel_layouts=stereo[out]",
                    "-map", "[out]", "-c:a", "aac", "-b:a", "192k", son], check=True)
    sortie = os.path.join(ICI, f"conseil-{n}.mp4")
    ctrl = os.path.join(ICI, "controle")
    os.makedirs(ctrl, exist_ok=True)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                           "-i", "-", "-i", son, "-af", "loudnorm=I=-15:TP=-1.5:LRA=9", "-c:v", "libx264", "-preset", "slow",
                           "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-ar", "44100", "-c:a", "aac",
                           "-b:a", "192k", "-shortest", sortie], stdin=subprocess.PIPE)
    controles = {round(d + 1.0, 1) for d in debuts} | {round(total - .3, 1)}
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.add_init_script(f"window.TOTAL={total}")
        pg.set_content(page(n, cfg, debuts), wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(400)
        polices = pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)")
        if not any("Instrument" in x for x in polices) or not any("Geist" in x for x in polices):
            sys.exit(f"ALERTE : polices non chargées {polices}")
        fautes = pg.evaluate("""[...document.querySelectorAll('.titre,.fin h2,.lien,.chemin,.serie')].map(e=>{
            const r=e.getBoundingClientRect(), s=getComputedStyle(e);
            return (r.right>1080-80||r.left<80||e.scrollWidth>e.clientWidth+1||r.bottom>1920-180)?e.textContent:null}).filter(Boolean)""")
        hauteurs = pg.evaluate("[...document.querySelectorAll('.titre')].map(e=>Math.round(e.getBoundingClientRect().bottom))")
        if fautes or max(hauteurs) > 1500:
            nav.close()
            sys.exit(f"ALERTE conseil {n} : textes hors marge {fautes} / bas des titres {hauteurs}")
        for i in range(int(FPS * total)):
            t = i / FPS
            pg.evaluate(f"seek({t:.4f})")
            img = pg.screenshot(type="jpeg", quality=93)
            ff.stdin.write(img)
            if round(t, 1) in controles and abs(t - round(t, 1)) < 1 / FPS / 2:
                with open(os.path.join(ctrl, f"c{n}-t{t:04.1f}.jpg"), "wb") as f:
                    f.write(img)
        nav.close()
    ff.stdin.close()
    ff.wait()
    for x in (voix_wav, son):
        os.remove(x)
    print(f"conseil-{n}.mp4 : {total} s, scènes {debuts}")


if __name__ == "__main__":
    for n in [int(x) for x in sys.argv[1:]] or sorted(SERIE):
        fabriquer(n)
