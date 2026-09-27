# Maquette premium personnalisée (privée) par prospect.
# Entrée : prospects.json (PRIVÉ, jamais dans le dépôt) ; photos : dossier DIG_PHOTOS (défaut ./photos/),
# photos : StockSnap (CC0, via l'API Openverse) nommées <métier>_<n>.jpg, et Unsplash HD (h<métier>_<n>.jpg, sources dans supports/).
# N'afficher que des faits vérifiés (RGE via l'annuaire ADEME, dates du registre) ; pas de faux avis.
import html,re,json,os,base64
PH=os.environ.get('DIG_PHOTOS','photos/')
def img(n): return 'data:image/jpeg;base64,'+base64.b64encode(open(PH+n+'.jpg','rb').read()).decode()
T={
'menuiserie':dict(acc='#b07a4a',hero='hbois_0',bande='hbois_2',g=['hbois_6','hbois_12','hbois_13','hbois_9'],sur='Menuiserie · Agencement',
  h1='Le bois, <em>travaillé</em> pour durer.',intro='Fenêtres, portes, volets, escaliers : chaque ouvrage est pensé, fabriqué et posé avec l’exigence d’un artisan.',
  s=[('Fenêtres & baies','Bois, alu ou PVC, double ou triple vitrage, pose en rénovation sans gros travaux.'),('Portes d’entrée','Isolantes, sécurisées, dessinées pour le caractère de votre maison.'),('Volets & portails','Battants, roulants ou motorisés, pilotables depuis votre téléphone.'),('Agencement sur mesure','Escaliers, placards, dressings : ajustés au centimètre.')],gl=['Le geste juste','Assemblé à l’atelier','Finitions précises','Bois sélectionné']),
'chauffage':dict(acc='#d9774b',hero='chauf_8',g=['chauf_2','chauf_14','chauf_26','chauf_0'],sur='Chauffage · Plomberie · Énergies',
  h1='La chaleur, <em>maîtrisée</em>.',intro='Pompes à chaleur, chaudières, poêles, plomberie : un confort durable et des factures qui baissent.',
  s=[('Pompes à chaleur','Étude, installation et mise en service, air/eau ou air/air.'),('Chaudières & poêles','Gaz, granulés ou bois : le bon équipement pour votre maison.'),('Salle de bain & plomberie','Rénovation complète, chauffe-eau, dépannage.'),('Entretien & dépannage','Contrat annuel et intervention rapide.')],gl=['Chaleur du bois','Salle de bain','Solaire thermique','Confort toute l’année']),
'electricite':dict(acc='#e0a458',hero='elec_18',g=['elec_1','elec_10','elec_13','elec_20'],sur='Électricité · Chauffage',
  h1='Votre maison, <em>en pleine lumière</em>.',intro='Installation, rénovation et mise aux normes, avec la rigueur qu’exige la sécurité de votre foyer.',
  s=[('Installation & rénovation','Neuf et ancien, tableaux, mises aux normes.'),('Chauffage électrique','Radiateurs à inertie, chauffe-eau, pompes à chaleur.'),('Éclairage','Intérieur et extérieur, mises en valeur LED.'),('Dépannage','Diagnostic et intervention rapide.')],gl=['Intervention soignée','Tableaux aux normes','Éclairage d’ambiance','Mise en valeur']),
'couverture':dict(acc='#c0754a',hero='toit_4',g=['toit_1','toit_12','toit_0','toit_8'],sur='Couverture · Charpente · Zinguerie',
  h1='Un toit <em>solide</em>, une maison sereine.',intro='Tuiles, ardoises, charpente, zinguerie et isolation : votre toiture confiée à des spécialistes.',
  s=[('Couverture','Réfection complète ou partielle, tuiles et ardoises.'),('Charpente','Création, traitement et renforcement.'),('Zinguerie','Gouttières, descentes, habillages.'),('Isolation & fenêtres de toit','Combles isolés, lumière naturelle.')],gl=['Tuiles posées au cordeau','Tuiles anciennes','Architecture contemporaine','Finitions précises']),
'peinture':dict(acc='#c9a45c',hero='peint_12',g=['peint_15','peint_28','peint_21','peint_23'],sur='Peinture · Façades · Isolation',
  h1='Des murs qui <em>changent</em> tout.',intro='Peinture intérieure, ravalement et isolation par l’extérieur : des finitions impeccables, un logement transformé.',
  s=[('Peinture intérieure','Murs, plafonds, boiseries, finitions soignées.'),('Ravalement de façade','Nettoyage, réparation et mise en peinture.'),('Isolation extérieure','Moins de pertes de chaleur, façade rénovée.'),('Conseil déco','Couleurs et matières choisies avec vous.')],gl=['Intérieurs lumineux','Entrées de caractère','Couleurs apaisantes','Volumes révélés']),
'restaurant':dict(acc='#c8a26b',hero='resto_11',g=['resto_25','resto_29','resto_19','resto_9'],sur='Restaurant · Chambres d’hôtes',
  h1='Une table <em>au bord de l’eau</em>.',intro='Cuisine de saison, produits frais et vins de la région, dans un cadre où l’on prend le temps.',
  s=[('La carte','Plats de saison et spécialités de la région.'),('Les vins','Une sélection de vins locaux.'),('Groupes & fêtes','Repas de famille, anniversaires, événements.'),('Chambres','Prolongez le moment : nuit sur place.')],gl=['Dans l’assiette','Produits de saison','Au fil de l’eau','Autour de la table']),
}
X={"menuiserie": ["Des ouvrages sur mesure,", "pensés pour durer.", "Chaque projet commence par une visite et des mesures précises. Nous vous conseillons sur les matériaux, l’isolation et les aides possibles, puis nous posons avec soin et laissons le chantier propre."], "chauffage": ["Le bon équipement,", "bien installé.", "Nous étudions votre logement avant de vous conseiller : puissance adaptée, consommation, aides possibles. L’installation est faite proprement, puis nous assurons l’entretien et le dépannage."], "electricite": ["La sécurité d’abord,", "le confort ensuite.", "Diagnostic, conseil, installation : nous travaillons dans le respect des normes et vous expliquons chaque étape, pour une installation fiable et durable."], "couverture": ["Votre toiture,", "entre des mains expertes.", "Diagnostic de la toiture, devis détaillé, travaux réalisés en sécurité : nous protégeons votre maison des intempéries pour longtemps."], "peinture": ["Des finitions impeccables,", "un logement transformé.", "Préparation soignée des supports, peintures de qualité, protection de votre mobilier : nous vous rendons un intérieur ou une façade comme neufs, dans les délais annoncés."], "restaurant": ["Une cuisine sincère,", "au fil des saisons.", "Des produits frais, des recettes de la région et le temps de bien faire. Au bord de l’eau, on vient pour un déjeuner, on reste pour la soirée."]}

def _lum(h):
    r,g,b=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    f=lambda v:v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def _contraste(a,b):
    x,y=_lum(a),_lum(b);return (max(x,y)+0.05)/(min(x,y)+0.05)
def fonce(h,fond='#ece4d7',cible=4.8):
    """Même teinte, assombrie jusqu'à un contraste lisible sur fond clair (et avec du texte blanc)."""
    r,g,b=[int(h[i:i+2],16) for i in (1,3,5)];k=1.0
    while k>0.2:
        c='#%02x%02x%02x'%(int(r*k),int(g*k),int(b*k))
        if _contraste(c,fond)>=cible and _contraste(c,'#ffffff')>=cible: return c
        k-=0.02
    return c
CSS='''
:root{--creme:#f6f1e9;--encre:#1f1c18;--doux:#57504a;--nuit:#12100d;--acc:%s;--acct:%s}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:Jost,system-ui,sans-serif;font-weight:400;font-size:17px;background:var(--creme);color:var(--encre);line-height:1.7;overflow-x:hidden}
h1,h2,h3{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;line-height:1.08}
a{color:inherit;text-decoration:none}img{display:block;width:100%%;height:100%%;object-fit:cover}
.basbar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:flex;flex-direction:column;padding-bottom:env(safe-area-inset-bottom)}.maq{flex-basis:100%%;color:#b5ad9f;font-size:.84rem;border-top:1px solid rgba(255,255,255,.08);padding-top:14px}
nav{background:linear-gradient(180deg,rgba(18,16,13,.75),rgba(18,16,13,0));position:fixed;top:0;left:0;right:0;z-index:50;display:flex;justify-content:space-between;align-items:center;padding:1.2rem clamp(18px,4vw,56px);color:#fff;transition:.4s}
nav:not(.plein) .marque,nav:not(.plein) .liens a{text-shadow:0 1px 3px rgba(0,0,0,.55)}
nav.plein{background:rgba(246,241,233,.95);backdrop-filter:blur(10px);color:var(--encre);padding:.75rem clamp(18px,4vw,56px);box-shadow:0 1px 0 rgba(0,0,0,.06)}
.marque{font-family:"Cormorant Garamond",serif;font-weight:600;font-size:clamp(1.7rem,2.4vw,2.1rem);letter-spacing:.01em;line-height:1.05;display:block}
.marque small{display:block;font-family:Jost;font-weight:500;font-size:.82rem;letter-spacing:.2em;text-transform:uppercase;opacity:.85;margin-top:.45rem}
.liens{display:flex;gap:2rem;align-items:center;font-size:.86rem;letter-spacing:.14em;text-transform:uppercase;font-weight:500}
.cta{border:1px solid currentColor;padding:calc(.6rem + 1px) calc(1.1rem - .14em) calc(.6rem - 1px) 1.1rem;line-height:1;white-space:nowrap;display:inline-flex;align-items:center}
.heros{min-height:100svh;display:grid;grid-template-columns:minmax(380px,44%%) 1fr;background:var(--nuit);color:#f4efe6}
.heros .texte{display:flex;flex-direction:column;justify-content:center;padding:130px clamp(24px,5vw,80px) 90px;animation:monte 1.1s .15s both;position:relative}
.heros .texte::before{content:"";display:block;width:56px;height:2px;background:var(--acc);margin-bottom:1.3rem}
@keyframes monte{from{opacity:0;transform:translateY(24px)}}
.heros .fond{position:relative;overflow:hidden}.heros .fond img{position:absolute;inset:0;transform:scale(1.08);animation:zoom 16s ease-out forwards}
@keyframes zoom{to{transform:scale(1)}}
.heros .fond::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(18,16,13,.35),rgba(18,16,13,0) 30%%)}
.heros .fond .etiq{position:absolute;z-index:2;right:24px;bottom:24px;background:rgba(246,241,233,.94);color:var(--encre);padding:.7rem 1rem;font-size:.86rem;letter-spacing:.1em;text-transform:uppercase;font-weight:500}
.sur{font-size:.84rem;letter-spacing:.24em;text-transform:uppercase;font-weight:500;color:var(--acct)}
.heros .sur{color:var(--acc)}
.heros h1{font-size:clamp(2.9rem,5.4vw,5.6rem);font-weight:600;margin:.7rem 0 1.1rem;color:#fbf8f2}
.heros h1 em{font-style:italic;color:var(--acc)}
.heros p{font-size:1.12rem;max-width:520px;color:#ddd5c8;font-weight:400}
.boutons{display:flex;gap:.8rem;margin-top:2rem;flex-wrap:wrap}
.b{display:inline-flex;align-items:center;justify-content:center;line-height:1;padding:1.05rem calc(1.6rem - .14em) 1.05rem 1.6rem;font-size:.82rem;letter-spacing:.14em;text-transform:uppercase;font-weight:500}
.b.plein{background:var(--acct);color:#fff}.b.vide{border:1.5px solid rgba(255,255,255,.75);color:#fff}
.fleche{display:none}
section{padding:clamp(76px,11vw,150px) clamp(18px,6vw,96px)}
.intro{display:grid;grid-template-columns:1fr 1fr;gap:clamp(36px,6vw,96px);align-items:center}
.intro h2{font-size:clamp(2.3rem,4.5vw,3.6rem)}.intro h2 em{color:var(--acct)}
.intro p{color:#4a443c;margin-top:1.3rem;max-width:480px}
.chiffres{display:flex;gap:2.6rem;margin-top:2.2rem;flex-wrap:wrap}
.chiffres b{display:block;font-family:"Cormorant Garamond";font-size:2.5rem;font-weight:500;color:var(--acct);line-height:1}
.chiffres span{font-size:.82rem;letter-spacing:.16em;text-transform:uppercase;color:var(--doux)}
.intro .photo{aspect-ratio:4/5;overflow:hidden}
.titre{text-align:center;max-width:660px;margin:0 auto clamp(40px,6vw,72px)}
.titre .sur{color:var(--acct)}
section.services .sur,section.services .titre .sur,section.services .n{color:var(--acc)}.titre h2{font-size:clamp(2.3rem,4.5vw,3.4rem);margin-top:.6rem}
.services{background:var(--nuit);color:#efe9df}
.services .grille{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,.08)}
.services .carte{background:var(--nuit);padding:2.4rem 1.8rem}
.services .n{font-family:"Cormorant Garamond";font-size:1.05rem;color:var(--acct);letter-spacing:.2em}
.services h3{font-size:1.7rem;margin:.8rem 0 .6rem}.services p{color:#d4ccbf;font-size:1rem}
.galerie{display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:280px 280px;gap:12px}
.galerie figure{position:relative;overflow:hidden}.galerie figure:first-child{grid-row:span 2}
.galerie img{transition:transform 1.2s}.galerie figure:hover img{transform:scale(1.06)}
.galerie figure::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.7),transparent 55%%)}.galerie figcaption{position:absolute;z-index:2;left:14px;bottom:12px;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.6);font-family:"Cormorant Garamond";font-weight:600;font-size:1.35rem}
.etapes{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(24px,4vw,56px);counter-reset:e}
.etapes div{border-top:1px solid #d9cfbf;padding-top:1.4rem}
.etapes div::before{counter-increment:e;content:"0" counter(e);font-family:"Cormorant Garamond";font-size:2.6rem;color:var(--acct)}
.etapes h3{font-size:1.5rem;margin:.3rem 0 .4rem}.etapes p{color:var(--doux)}
.avis{background:#ece4d7;text-align:center}
.etoiles{color:var(--acct);letter-spacing:.3em;font-size:1.3rem}
.avis blockquote{font-family:"Cormorant Garamond";font-size:clamp(1.6rem,3vw,2.3rem);font-style:italic;max-width:760px;margin:1.2rem auto}
.avis cite{font-style:normal;font-size:.84rem;letter-spacing:.2em;text-transform:uppercase;color:var(--doux)}
.bande{position:relative;color:#fff;text-align:center;padding:clamp(96px,14vw,180px) 18px;overflow:hidden}
.bande img{position:absolute;inset:0}.bande::after{display:none}
.bande>div{position:relative;z-index:2;display:inline-block;background:rgba(18,16,13,.93);padding:clamp(28px,5vw,56px) clamp(24px,6vw,72px);max-width:680px}.bande h2{font-size:clamp(2.2rem,4.5vw,3.6rem);font-weight:600;margin:.4rem 0 .4rem}.bande h2 em{color:var(--acc)}
.bande .sur{color:#eadbc8!important}
.contact{display:grid;grid-template-columns:1fr 1fr;gap:clamp(36px,6vw,96px)}
.contact h2{font-size:clamp(2.2rem,4vw,3.2rem)}.contact p{color:var(--doux);margin-top:1rem}
.ligne{display:flex;justify-content:space-between;border-bottom:1px solid #d9cfbf;padding:.9rem 0;font-size:.95rem}.ligne span:first-child{color:var(--doux)}
form{display:grid;gap:1rem}input,textarea,select{width:100%%;font:inherit;background:transparent;border:0;border-bottom:1px solid #bfb3a0;padding:.8rem 0;color:var(--encre)}
form button{line-height:1;text-indent:.2em;margin-top:.6rem;background:var(--encre);color:#fff;border:0;padding:1.05rem;font:inherit;font-size:.86rem;letter-spacing:.2em;text-transform:uppercase;cursor:pointer}
footer{background:var(--nuit);color:#8f887b;padding:40px clamp(18px,6vw,96px) 110px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;font-size:.85rem}
footer .marque{color:#efe9df}
.appel{display:none}
.rv{opacity:0;transform:translateY(28px);transition:1s cubic-bezier(.2,.7,.2,1)}.rv.vu{opacity:1;transform:none}
@media (max-width:860px){.liens{display:none}.marque{font-size:clamp(1.85rem,7.4vw,2.3rem);max-width:none}.marque small{font-size:.82rem;margin-top:.4rem}.heros{grid-template-columns:1fr;min-height:auto}.heros .fond{order:-1;height:56svh;min-height:340px}.heros .texte{padding:44px 22px 110px}.heros .fond .etiq{right:14px;bottom:14px;font-size:.84rem}.liens a:not(.cta){display:none}.intro,.contact{grid-template-columns:1fr}.services .grille{grid-template-columns:1fr 1fr}
.galerie{grid-template-columns:1fr 1fr;grid-template-rows:230px 170px}.galerie figure:first-child{grid-column:span 2;grid-row:auto}
.etapes{grid-template-columns:1fr}.appel{display:flex;align-items:center;justify-content:center;gap:.55rem;margin:0 14px 10px;min-height:52px;background:var(--acct);color:#fff;font-size:.92rem;font-weight:500;line-height:1;letter-spacing:.16em;text-transform:uppercase;box-shadow:0 10px 30px rgba(0,0,0,.25);transform:translateY(calc(100%% + 24px));opacity:0;pointer-events:none;transition:transform .45s cubic-bezier(.2,.7,.2,1),opacity .3s}.appel.on{transform:none;opacity:1;pointer-events:auto}.appel span{margin-right:-.16em}.appel svg{flex:none}}
@media (max-width:520px){nav{padding:1rem 18px}.services .grille{grid-template-columns:1fr}}
'''
JS='''<script>const n=document.querySelector('nav');addEventListener('scroll',()=>n.classList.toggle('plein',scrollY>60));
const io=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){x.target.classList.add('vu');io.unobserve(x.target)}}),{threshold:.12});document.querySelectorAll('.rv').forEach(e=>io.observe(e));
const ap=document.querySelector('.appel'),hb=document.querySelector('.heros .boutons'),ct=document.querySelector('#contact');let vh=true,vc=false;const maj=()=>ap&&ap.classList.toggle('on',!vh&&!vc);
if(ap&&hb)new IntersectionObserver(e=>{vh=e[0].isIntersecting;maj()},{rootMargin:'0px 0px 110px 0px'}).observe(hb);if(ap&&ct)new IntersectionObserver(e=>{vc=e[0].isIntersecting;maj()},{threshold:.15}).observe(ct);</script>'''
def page(p):
    t=T[p['type']];e=html.escape;nom=e(p['nom']);num=re.sub(r'\D','',p['tel'])
    g=[img(x) for x in t['g']];h1=p.get('h1p',t['h1']);intro=e(p.get('acc',t['intro']))
    ch=''.join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a,b in p.get('preuves',[]))
    sv=''.join(f'<div class="carte rv"><div class="n">0{i+1}</div><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i,(a,b) in enumerate(t['s']))
    gal=''.join(f'<figure class="rv"><img src="{g[i]}" alt=""><figcaption>{e(t["gl"][i])}</figcaption></figure>' for i in range(3))
    resto=p['type']=='restaurant'
    cta='Réserver' if resto else 'Devis gratuit'
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>{nom}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Jost:wght@400;500&display=swap" rel="stylesheet"><style>{CSS%(t['acc'],fonce(t['acc']))}</style></head><body>
<nav><a class="marque" href="#">{nom}<small>{e(p['commune'])}</small></a><div class="liens"><a href="#savoir">{'La maison' if resto else 'Savoir-faire'}</a><a href="#services">{'La carte' if resto else 'Services'}</a><a href="#realisations">{'Galerie' if resto else 'Réalisations'}</a><a class="cta" href="#contact">{cta}</a></div></nav>
<header class="heros"><div class="texte"><div class="sur">{e(t['sur'])}</div><h1>{h1}</h1><p>{intro}</p>
<div class="boutons"><a class="b plein" href="#contact">{'Réserver une table' if resto else 'Demander un devis'}</a><a class="b vide" href="tel:{num}">{e(p['tel'])}</a></div></div><div class="fond"><img src="{img(p.get('hero',t['hero']))}" alt=""><div class="etiq">{e(p['commune'])}</div></div></header>
<section id="savoir" class="intro"><div class="rv"><div class="sur" style="color:var(--acct)">{'La maison' if resto else 'Notre savoir-faire'}</div><h2>{e(p.get('titre2',X[p['type']][0]))} <em>{e(p.get('titre2b',X[p['type']][1]))}</em></h2>
<p>{e(p.get('texte2',X[p['type']][2]))}</p><div class="chiffres">{ch}</div></div><div class="photo rv"><img src="{g[3]}" alt=""></div></section>
<section id="services" class="services"><div class="titre rv"><div class="sur">{'À découvrir' if resto else 'Ce que nous faisons'}</div><h2>{'Le plaisir de la table' if resto else 'Des prestations complètes'}</h2></div><div class="grille">{sv}</div></section>
<section id="realisations"><div class="titre rv"><div class="sur">{'En images' if resto else 'Réalisations'}</div><h2>{'Un lieu à vivre' if resto else 'L’exigence, dans chaque détail'}</h2></div><div class="galerie">{gal}</div></section>
<section style="padding-top:0"><div class="titre rv"><div class="sur">{'Venir nous voir' if resto else 'Comment ça se passe'}</div><h2>{'Simple et chaleureux' if resto else 'Trois étapes, zéro surprise'}</h2></div><div class="etapes rv">
{'<div><h3>Réservez</h3><p>Par téléphone ou en ligne, en quelques secondes.</p></div><div><h3>Installez-vous</h3><p>En salle ou en terrasse, au calme.</p></div><div><h3>Restez</h3><p>Une chambre vous attend pour prolonger la soirée.</p></div>' if resto else '<div><h3>Visite & conseil</h3><p>Nous venons voir votre projet et vous conseillons, gratuitement.</p></div><div><h3>Devis détaillé</h3><p>Un prix clair, ligne par ligne, avec les délais.</p></div><div><h3>Réalisation</h3><p>Chantier propre, finitions vérifiées ensemble.</p></div>'}</div></section>
<section class="avis"><div class="rv"><div class="etoiles">★★★★★</div><blockquote>Vos avis Google s’afficheront ici, automatiquement.</blockquote><cite>Emplacement réservé aux avis de vos clients</cite></div></section>
<div class="bande"><img src="{img(t['bande']) if 'bande' in t else g[1]}" alt=""><div class="rv"><div class="sur">{e(p['commune'])} et alentours</div><h2>{'Une envie de' if resto else 'Un projet ?'} <em>{'bonne table ?' if resto else 'Parlons-en.'}</em></h2><div class="boutons" style="justify-content:center"><a class="b plein" href="tel:{num}">{e(p['tel'])}</a></div></div></div>
<section id="contact" class="contact"><div class="rv"><div class="sur" style="color:var(--acct)">Contact</div><h2>{'Réserver' if resto else 'Demander un devis'}</h2><p>{'Nous vous confirmons votre table rapidement.' if resto else 'Réponse rapide, devis gratuit et sans engagement.'}</p>
<div style="margin-top:1.6rem"><div class="ligne"><span>Téléphone</span><a href="tel:{num}">{e(p['tel'])}</a></div><div class="ligne"><span>Secteur</span><span>{e(p['commune'])} et alentours</span></div></div></div>
<form class="rv" onsubmit="event.preventDefault()"><input placeholder="Votre nom"><input placeholder="Téléphone ou email"><textarea rows="3" placeholder="{'Date, heure, nombre de personnes' if resto else 'Votre projet en quelques mots'}"></textarea><button type="button">Envoyer</button></form></section>
<footer><div class="marque">{nom}<small>{e(p['commune'])}</small></div><div>© {nom} · Mentions légales</div><div class="maq">{e(p.get("maq","")) or f"Maquette préparée par Dig pour {nom} · non publiée · photos d’illustration libres de droits"}</div></footer>
<div class="basbar"><a class="appel" href="tel:{num}"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg><span>{'Réserver' if resto else 'Appeler'} · {e(p['tel'])}</span></a></div>{JS}</body></html>'''
P=json.load(open(os.environ.get('DIG_PROSPECTS','prospects.json')))
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from typo_fr import fix as typo_fr
SORTIE=os.environ.get('DIG_SORTIE','')
for p in P: open(os.path.join(SORTIE,p['id']+'.html') if SORTIE else p['id']+'.html','w').write(typo_fr(page(p)))
print(len(P))
