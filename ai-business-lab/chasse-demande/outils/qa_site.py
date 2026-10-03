import os,sys
from playwright.sync_api import sync_playwright
JS="""()=>{const b=document.getElementById('barre');const cs=b?getComputedStyle(b):null;const vis=!!b&&cs.display!=='none'&&!b.classList.contains('cache');
const br=b?b.getBoundingClientRect():{top:0,bottom:0};const pb=[];
const tgt=[...document.querySelectorAll('#cta-haut,#form input,#form select,#form textarea,#form button')];
if(vis){for(const t of tgt){const r=t.getBoundingClientRect();if(r.bottom>br.top&&r.top<br.bottom&&r.bottom>0&&r.top<innerHeight)pb.push(t.name||t.id||t.tagName)}}
const over=document.documentElement.scrollWidth>innerWidth+1;
const liens=[...document.querySelectorAll('a[href^="tel:"],a[href^="mailto:"]')].filter(a=>getComputedStyle(a).display!=='none'&&a.getAttribute('href').includes('[')).length;
const crochets=document.body.innerText.match(/\\[[^\\]]{2,40}\\]/g);
return {vis,pb,over,liens,crochets}}"""
bad=0;n=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for w,h in [(320,568),(360,740),(390,844),(414,896),(768,1024),(1024,768),(1440,900)]:
        pg=b.new_page(viewport={'width':w,'height':h});pg.goto('file://'+os.path.abspath(sys.argv[1]));pg.wait_for_timeout(1200)
        H=pg.evaluate('document.documentElement.scrollHeight')
        for y in list(range(0,H,150))+[H]:
            pg.evaluate(f'window.scrollTo(0,{y})');pg.wait_for_timeout(120);m=pg.evaluate(JS);n+=1
            if m['pb'] or m['over'] or m['liens'] or m['crochets'] or (w>820 and m['vis']): bad+=1;print(w,y,m) if bad<15 else None
        pg.close()
    b.close()
print('états testés',n,'problèmes',bad)
