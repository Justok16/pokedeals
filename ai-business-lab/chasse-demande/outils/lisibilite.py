# Mesure la lisibilité de chaque texte visible : taille >= 13 px, graisse >= 400, contraste >= 4,5 (3 si >= 24 px),
# ombre portée pour les textes posés sur photo. Usage : python3 lisibilite.py page.html [".selecteur-photo"]
import os,sys
from playwright.sync_api import sync_playwright
JS="""(PHOTO)=>{function lum(c){const m=c.match(/[\\d.]+/g).map(Number);const [r,g,b]=m.slice(0,3).map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*r+0.7152*g+0.0722*b}
function bg(e){while(e){const c=getComputedStyle(e);if(c.backgroundImage!=='none'&&!c.backgroundImage.includes('gradient'))return null;const m=c.backgroundColor.match(/[\\d.]+/g);if(m&&(m.length<4||+m[3]>0.9))return c.backgroundColor;e=e.parentElement}return 'rgb(255,255,255)'}
const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while(n=w.nextNode()){const t=n.textContent.trim();if(!t)continue;const e=n.parentElement;const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')continue;const r=e.getBoundingClientRect();if(!r.width)continue;
const fs=parseFloat(cs.fontSize),fw=parseInt(cs.fontWeight);const surPhoto=PHOTO?(!!e.closest(PHOTO)||!!e.closest('nav:not(.plein)')):false;const b=surPhoto?null:bg(e);let ct=null;
if(b){const L1=lum(cs.color),L2=lum(b);ct=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05)}
const pb=[];if(fs<13)pb.push('taille '+fs);if(fw<400)pb.push('graisse '+fw);if(ct!==null&&ct<(fs>=24?3:4.5))pb.push('contraste '+ct.toFixed(2));if(surPhoto&&cs.textShadow==='none')pb.push('sans ombre sur photo');
if(pb.length)out.push([t.slice(0,40),pb.join(', ')])}
return out}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for w,h in [(320,640),(390,844),(1440,900)]:
        pg=b.new_page(viewport={'width':w,'height':h});pg.goto('file://'+os.path.abspath(sys.argv[1]));pg.wait_for_timeout(1200)
        pg.evaluate("document.querySelectorAll('.apparait').forEach(e=>e.classList.add('vu'))");pg.wait_for_timeout(900)
        r=pg.evaluate(JS,sys.argv[2] if len(sys.argv)>2 else '');print(w,len(r));[print('  ',x) for x in r[:25]];pg.close()
    b.close()
