import os,json,glob
from playwright.sync_api import sync_playwright
JS="""()=>{const el=document.querySelector('.appel');const r=el.getBoundingClientRect();
let L=1e9,R=-1e9,T=1e9,B=-1e9;const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;
while(n=w.nextNode()){const t=n.textContent;const ls=parseFloat(getComputedStyle(n.parentElement).letterSpacing)||0;for(let i=0;i<t.length;i++){if(!t[i].trim())continue;const g=document.createRange();g.setStart(n,i);g.setEnd(n,i+1);const q=g.getClientRects()[0];if(!q)continue;L=Math.min(L,q.left);R=Math.max(R,q.right-ls);T=Math.min(T,q.top);B=Math.max(B,q.bottom)}}
const s=el.querySelector('svg').getBoundingClientRect();L=Math.min(L,s.left);
// occlusion: points along bottom edge of the button must hit the button
let libre=true;for(const x of [r.left+5,(r.left+r.right)/2,r.right-5]){const h=document.elementFromPoint(x,r.bottom-2);if(!el.contains(h))libre=false}
return {g:+(L-r.left).toFixed(1),d:+(r.right-R).toFixed(1),h:+(T-r.top).toFixed(1),b:+(r.bottom-B).toFixed(1),libre}}"""
bad=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for f in sorted(glob.glob('1[0-9][0-9]-*.html')):
        for w in [320,360,375,390,414]:
            pg=b.new_page(viewport={'width':w,'height':760});pg.goto('file://'+os.path.abspath(f));pg.wait_for_timeout(700)
            m=pg.evaluate(JS);pg.close()
            ok=m['libre'] and abs(m['g']-m['d'])<1.5 and abs(m['h']-m['b'])<1.5
            if not ok: bad+=1;print(f,w,m)
    b.close()
print('problèmes:',bad)
