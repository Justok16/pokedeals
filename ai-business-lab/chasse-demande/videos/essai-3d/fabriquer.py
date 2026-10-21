#!/usr/bin/env python3
"""Essai 3D (21/10/2026, accord de l'utilisateur « Oui stp ») : le conseil DIG16 n° 1 refait en 3D (Three.js),
d'après la vidéo CCUSpJkAfgU (cartes en verre dépoli, particules, caméra qui voyage entre les cartes).

Même voix et même musique que videos/conseils/conseil-1.mp4 (piste audio reprise telle quelle), mêmes textes et
mêmes instants de scène : seule l'image change, pour comparer. Rien n'est publié : essai à montrer à l'utilisateur.

Usage : python3 fabriquer.py   (Three.js 0.169.0, licence MIT, téléchargé dans ce dossier s'il manque)
Écrit essai-3d-conseil-1.mp4 et des images de contrôle dans controle/ (non versionnées).
Contrôles bloquants : polices chargées, WebGL actif, texte des cartes dans le cadre.
Écran final : la même empreinte que la version 2D (outils/marque/empreinte.py), en relief (choix de l'utilisateur, 21/10).
"""

import base64
import functools
import http.server
import json
import os
import re
import subprocess
import sys
import threading
import urllib.request

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
CD = os.path.normpath(os.path.join(ICI, "..", ".."))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
POLICES = os.path.join(CD, "site-dig", "moteur", "polices")
SOURCE = os.path.join(CD, "videos", "conseils", "conseil-1.mp4")
THREE = os.path.join(ICI, "three.module.min.js")
sys.path.insert(0, os.path.join(CD, "outils", "marque"))
from empreinte import empreinte_svg  # noqa: E402  (même empreinte que la version 2D validée)
FPS = 30
TOTAL = 19.9
# Débuts des phrases de conseil-1.mp4, mesurés le 21/10 sur la vidéo (changements de texte à 2,93 ; 6,0 ; 10,5 ; 14,0 s).
DEBUTS = [0.6, 3.05, 6.1, 10.6, 14.1]
TITRE = "Votre site est-il vraiment à vous ?"
CARTES = ["Votre site est-il vraiment *à vous ?*",
          "Tout dépend d’un détail : *le nom de domaine.*",
          "Au nom du prestataire ? Impossible de partir *sans perdre votre adresse.*",
          "Avant de signer, demandez-le *par écrit.*"]


def data(chemin, mime):
    with open(chemin, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def css_polices():
    css = open(os.path.join(POLICES, "instrumentserif-geist-geistmono.css"), encoding="utf-8").read()
    return re.sub(r"url\(/moteur/polices/([^)]+)\)",
                  lambda m: f"url({data(os.path.join(POLICES, m.group(1)), 'font/woff2')})", css)


def insecables(t):
    return re.sub(r" ([:;?!])", " \\1", t.replace("'", "’"))


def page():
    signature = data(os.path.join(CD, "site-dig", "img", "marque", "signature-ivoire@2x.png"), "image/png")
    empreinte = "data:image/svg+xml;base64," + base64.b64encode(empreinte_svg(1024, ident="f").encode()).decode()
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css_polices()}</style><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;background:#0f0e0c;color:#efe9df;font-family:Geist,'Geist Fallback',sans-serif;position:relative}}
#fond{{position:absolute;inset:0;background:radial-gradient(80% 50% at 90% 0%,rgba(200,164,110,.18),rgba(200,164,110,0) 70%),
 radial-gradient(70% 40% at 0% 100%,rgba(200,164,110,.10),rgba(200,164,110,0) 70%)}}
canvas{{position:absolute;inset:0;width:1080px;height:1920px}}
.signature{{position:absolute;left:84px;top:90px;height:92px}}
.serie{{position:absolute;left:84px;right:84px;top:250px;font:500 30px 'Geist Mono','Geist Mono Fallback',monospace;letter-spacing:.2em;
 text-transform:uppercase;color:#a8a093;padding-top:22px;border-top:2px solid rgba(200,164,110,.55)}}
.barre{{position:absolute;left:84px;right:84px;bottom:150px;height:6px;border-radius:3px;background:rgba(239,233,223,.12)}}
.barre i{{display:block;height:100%;border-radius:3px;background:#c8a46e;width:0}}
.fin{{position:absolute;inset:0;opacity:0;pointer-events:none}}
.fin h2{{position:absolute;left:84px;right:84px;top:440px;font:400 104px/1.02 'Instrument Serif','Instrument Serif Fallback',serif;letter-spacing:-.02em}}
.fin h2 em{{color:#d9bb8a;font-style:italic}}
.lien{{position:absolute;left:84px;right:84px;bottom:330px;font:500 64px Geist,'Geist Fallback',sans-serif;letter-spacing:-.01em}}
.lien span{{color:#c8a46e}}
.chemin{{position:absolute;left:84px;right:84px;bottom:262px;font:400 40px Geist,'Geist Fallback',sans-serif;color:#cfc6b8}}
</style></head><body>
<div id="fond"></div>
<canvas id="c" width="1080" height="1920"></canvas>
<img class="signature" src="{signature}" alt="DIG16">
<div class="serie" id="serie">Le conseil DIG16 · {insecables(TITRE)}</div>
<section class="fin" id="fin"><h2>Le guide complet, <em>gratuit.</em></h2>
<div class="lien">dig16<span>.fr</span></div><div class="chemin">dig16.fr/site-internet-artisan</div></section>
<div class="barre"><i id="prog"></i></div>
<script type="module">
import * as THREE from './three.module.min.js';
const EMPREINTE="{empreinte}";
const D={json.dumps(DEBUTS)}, TOTAL={TOTAL}, CARTES={json.dumps([insecables(c) for c in CARTES], ensure_ascii=False)};
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)), doux=x=>{{x=cl(x,0,1);return x*x*(3-2*x)}};
const ren=new THREE.WebGLRenderer({{canvas:document.getElementById('c'),antialias:true,alpha:true,preserveDrawingBuffer:true}});
ren.setPixelRatio(1); ren.setSize(1080,1920,false); ren.setClearColor(0x000000,0);
const scene=new THREE.Scene();
const cam=new THREE.PerspectiveCamera(38,1080/1920,.1,400);

// Phrase : texte dessiné sur une toile (polices de la charte), flottant seul dans l'espace (cadre de verre retiré le 21/10).
function texture(texte){{
  const W=2048,H=1600,cv=document.createElement('canvas');cv.width=W;cv.height=H;
  const g=cv.getContext('2d');
  const morceaux=[];texte.split(/(\\*[^*]+\\*)/).forEach(p=>{{if(!p)return;const d=p.startsWith('*');
    (d?p.slice(1,-1):p).split(/(\\s+)/).forEach(m=>{{if(m)morceaux.push({{t:m,d}})}})}});
  const taille=232, inter=taille*1.0, marge=150, larg=W-2*marge;
  const fonte=d=>`${{d?'italic ':''}}400 ${{taille}}px 'Instrument Serif'`;
  const lignes=[[]];let x=0;
  for(const m of morceaux){{g.font=fonte(m.d);const w=g.measureText(m.t).width;
    if(/^\\s+$/.test(m.t)){{if(x>0){{lignes.at(-1).push({{...m,w}});x+=w}};continue}}
    if(x+w>larg&&x>0){{while(lignes.at(-1).length&&/^\\s+$/.test(lignes.at(-1).at(-1).t))lignes.at(-1).pop();lignes.push([]);x=0}}
    lignes.at(-1).push({{...m,w}});x+=w}}
  const h0=(H-lignes.length*inter)/2+taille*.78;
  lignes.forEach((l,i)=>{{let x=marge;for(const m of l){{g.font=fonte(m.d);g.fillStyle=m.d?'#d9bb8a':'#efe9df';
    g.fillText(m.t,x,h0+i*inter);x+=m.w}}}});
  const t=new THREE.CanvasTexture(cv);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t;
}}
const verre=new THREE.ShaderMaterial({{transparent:true,depthWrite:false,uniforms:{{op:{{value:1}}}},
  vertexShader:`varying vec2 vUv;varying vec3 vN;varying vec3 vV;void main(){{vUv=uv;vec4 p=modelViewMatrix*vec4(position,1.);
    vN=normalize(normalMatrix*normal);vV=normalize(-p.xyz);gl_Position=projectionMatrix*p;}}`,
  fragmentShader:`uniform float op;varying vec2 vUv;varying vec3 vN;varying vec3 vV;
    float rr(vec2 p,vec2 b,float r){{vec2 q=abs(p)-b+r;return length(max(q,0.))+min(max(q.x,q.y),0.)-r;}}
    void main(){{vec2 p=(vUv-.5)*vec2(1.28,1.);float d=rr(p,vec2(.62,.48),.06);if(d>0.)discard;
      float bord=smoothstep(-.012,0.,d);float fres=pow(1.-abs(dot(vN,vV)),2.);
      vec3 c=mix(vec3(.11,.10,.09),vec3(.30,.26,.20),vUv.y*.6+fres);
      float reflet=smoothstep(.0,.35,vUv.y-vUv.x*.35)*.08;
      gl_FragColor=vec4(c+reflet+vec3(.78,.64,.43)*bord*.9,(.62+.25*fres+bord*.6)*op);}}`}});
const groupes=[];
CARTES.forEach((t,i)=>{{
  const g=new THREE.Group();
  const tex=new THREE.Mesh(new THREE.PlaneGeometry(12.2,9.6),new THREE.MeshBasicMaterial({{map:texture(t),transparent:true,depthWrite:false}}));
  g.add(tex);  // sans cadre de verre (demande de l'utilisateur du 21/10 : « ça fait trop automate et répétitif »)
  g.position.set(i%2?2.4:-2.4,-i*1.4,-i*30);g.rotation.y=i%2?-.16:.16;g.rotation.x=.03;
  scene.add(g);groupes.push(g);
}});
// Particules dorées (positions calculées à partir du temps : rendu identique à chaque passage).
const N=2600,pos=new Float32Array(N*3),graine=[];
for(let i=0;i<N;i++){{const a=Math.sin(i*12.9898)*43758.5453;const r=a-Math.floor(a);const b=Math.sin(i*78.233)*12345.678;const s=b-Math.floor(b);
  const c=Math.sin(i*39.425)*24634.6345;const u=c-Math.floor(c);graine.push([r,s,u]);}}
const geoP=new THREE.BufferGeometry();geoP.setAttribute('position',new THREE.BufferAttribute(pos,3));
const point=document.createElement('canvas');point.width=point.height=64;const pg=point.getContext('2d');
const grd=pg.createRadialGradient(32,32,0,32,32,32);grd.addColorStop(0,'rgba(240,214,170,1)');grd.addColorStop(.3,'rgba(217,187,138,.55)');grd.addColorStop(1,'rgba(200,164,110,0)');
pg.fillStyle=grd;pg.fillRect(0,0,64,64);
const pts=new THREE.Points(geoP,new THREE.PointsMaterial({{size:.32,map:new THREE.CanvasTexture(point),transparent:true,depthWrite:false,
  blending:THREE.AdditiveBlending,opacity:.85}}));scene.add(pts);
// Empreinte dorée (écran final) : le dessin de la version 2D, en 3 couches décalées en profondeur (relief),
// révélée du centre vers l'extérieur avec une crête lumineuse.
const img=new Image();img.src=EMPREINTE;await img.decode();
const cvE=document.createElement('canvas');cvE.width=1024;cvE.height=1250;cvE.getContext('2d').drawImage(img,0,0,1024,1250);
const texE=new THREE.CanvasTexture(cvE);texE.anisotropy=8;
const empreinte=new THREE.Group();const couches=[];
[[0,1],[-.18,.45],[-.36,.22]].forEach(([z,a])=>{{
  const m=new THREE.ShaderMaterial({{transparent:true,depthWrite:false,
    uniforms:{{map:{{value:texE}},rev:{{value:0}},op:{{value:0}},force:{{value:a}}}},
    vertexShader:`varying vec2 vUv;void main(){{vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}}`,
    fragmentShader:`uniform sampler2D map;uniform float rev,op,force;varying vec2 vUv;
      void main(){{vec4 c=texture2D(map,vUv);float d=length((vUv-vec2(.5,.45))*vec2(1.,1.22));
        float vis=smoothstep(rev,rev-.06,d);float crete=exp(-pow((d-rev)*28.,2.))*step(.001,rev);
        vec3 col=c.rgb*(1.+crete*.7)+vec3(.85,.68,.42)*crete*c.a*.55;
        gl_FragColor=vec4(col,c.a*(vis+crete*.8)*op*force);}}`}});
  const pl=new THREE.Mesh(new THREE.PlaneGeometry(8.6,10.5),m);pl.position.z=z;empreinte.add(pl);couches.push(m);
}});
scene.add(empreinte);const lum=new THREE.PointLight(0xffe2b0,260,90);scene.add(lum);

function cible(i){{const g=groupes[i];return {{p:new THREE.Vector3(g.position.x*1.35,g.position.y+.1,g.position.z+38),
  r:new THREE.Vector3(g.position.x,g.position.y,g.position.z)}}}}
window.seek=function(t){{
  // Caméra : reste devant la carte de la phrase en cours, puis s'envole vers la suivante en arc.
  let i=0;while(i<D.length-2&&t>=D[i+1]-.55)i++;
  const fin=t>=D[4]-.55;
  const a=cible(Math.min(i,3)), b=fin?{{p:new THREE.Vector3(0,-6.5,-118),r:new THREE.Vector3(0,-6.5,-160)}}:cible(Math.min(i+1,3));
  const debutVol=(i+1<D.length?D[i+1]:TOTAL)-.55, k=doux((t-debutVol)/1.0);
  const p=a.p.clone().lerp(b.p,k), r=a.r.clone().lerp(b.r,k);
  p.y+=Math.sin(k*Math.PI)*2.2; p.x+=Math.sin(t*.35)*.35; p.y+=Math.cos(t*.3)*.2;
  cam.position.copy(p);cam.lookAt(r);
  groupes.forEach((g,j)=>{{g.rotation.y=(j%2?-.16:.16)+Math.sin(t*.4+j)*.03;
    const dz=p.z-38-g.position.z, o=cl(1-Math.abs(dz)/30,0,1)*cl((p.z-g.position.z)/6,0,1);
    g.children[0].material.opacity=o;}});
  for(let j=0;j<N;j++){{const [u,v,w]=graine[j];pos[j*3]=(u-.5)*60+Math.sin(t*.25+j)*.6;pos[j*3+1]=(v-.5)*34+Math.sin(t*.2+u*9)*.5-3;
    pos[j*3+2]=10-w*170;}}
  geoP.attributes.position.needsUpdate=true;
  const of=doux((t-(D[4]-.15))/.6);
  const kr=doux((t-(D[4]-.05))/2.2);
  empreinte.position.set(0,-9.2,-160);
  empreinte.rotation.set(.55*(1-kr)+Math.sin(t*.7)*.05, Math.sin(t*.55)*.28, 0);
  couches.forEach(m=>{{m.uniforms.op.value=of;m.uniforms.rev.value=kr*.78;}});
  lum.position.set(p.x+6,p.y+5,p.z-8);
  document.getElementById('fin').style.opacity=of;
  document.getElementById('serie').style.opacity=1-of;
  document.getElementById('prog').style.width=(cl(t/TOTAL,0,1)*100)+'%';
  ren.render(scene,cam);
}};
window.pret=true;
</script></body></html>"""


def main():
    if not os.path.exists(THREE):
        urllib.request.urlretrieve("https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.min.js", THREE)
    with open(os.path.join(ICI, "index.html"), "w", encoding="utf-8") as f:
        f.write(page())
    serveur = http.server.ThreadingHTTPServer(("127.0.0.1", 8766),
                                              functools.partial(http.server.SimpleHTTPRequestHandler, directory=ICI))
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    son = os.path.join(ICI, "son.m4a")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SOURCE, "-vn", "-c:a", "copy", son], check=True)
    sortie = os.path.join(ICI, "essai-3d-conseil-1.mp4")
    ctrl = os.path.join(ICI, "controle")
    os.makedirs(ctrl, exist_ok=True)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg",
                           "-i", "-", "-i", son, "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-movflags", "+faststart", "-c:a", "copy", "-shortest", sortie], stdin=subprocess.PIPE)
    controles = {0.0, 2.0, 3.5, 4.6, 7.0, 10.0, 12.0, 14.2, 15.0, 19.5}
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                                                               "--ignore-gpu-blocklist"])
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("http://127.0.0.1:8766/index.html", wait_until="load")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_function("window.pret===true", timeout=60000)
        polices = pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)")
        if not any("Instrument" in x for x in polices):
            sys.exit(f"ALERTE : polices non chargées {polices}")
        gl = pg.evaluate("!!document.getElementById('c').getContext('webgl2')||'déjà pris'")
        if not gl:
            sys.exit("ALERTE : WebGL indisponible")
        for i in range(int(FPS * TOTAL)):
            t = i / FPS
            pg.evaluate(f"seek({t:.4f})")
            img = pg.screenshot(type="jpeg", quality=93)
            ff.stdin.write(img)
            if any(abs(t - c) < 1 / FPS / 2 for c in controles):
                with open(os.path.join(ctrl, f"t{t:04.1f}.jpg"), "wb") as f:
                    f.write(img)
        nav.close()
    ff.stdin.close()
    ff.wait()
    serveur.shutdown()
    os.remove(son)
    print(f"{sortie} : {TOTAL} s")


if __name__ == "__main__":
    main()
