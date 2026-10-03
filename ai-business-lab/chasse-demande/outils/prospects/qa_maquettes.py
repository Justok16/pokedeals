import os,glob
from playwright.sync_api import sync_playwright
JS="""async()=>{await document.fonts.ready;const f=[document.fonts.check('16px Jost'),document.fonts.check('600 16px "Cormorant Garamond"')];
const over=document.documentElement.scrollWidth>innerWidth;
const bad=[];document.querySelectorAll('h1,h2,h3,p,a,.marque,.sur,figcaption').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&(r.right>innerWidth+1||r.left<-1))bad.push(e.className||e.tagName)});
const nav=document.querySelector('nav').getBoundingClientRect().height;
const imgs=[...document.images].filter(i=>!i.complete||!i.naturalWidth).length;
return {f,over,bad:bad.slice(0,5),nav:Math.round(nav),imgs}}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for f in sorted(glob.glob('1[0-9][0-9]-*.html')):
        for w in [320,390,768,1024,1440]:
            pg=b.new_page(viewport={'width':w,'height':800});pg.goto('file://'+os.path.abspath(f));pg.wait_for_timeout(600)
            m=pg.evaluate(JS);pg.close()
            if m['over'] or m['bad'] or m['imgs'] or not all(m['f']) or m['nav']>110: print(f,w,m)
    b.close()
print('fin')
