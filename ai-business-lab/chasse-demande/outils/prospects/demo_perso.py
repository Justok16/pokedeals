# Génère une maquette de page d'accueil personnalisée (privée) par prospect.
# Entrée : prospects.json (liste de {id, nom, type, commune, tel, preuves, h1?, acc?}) — fichier PRIVÉ, jamais dans le dépôt.
# Types : menuiserie, chauffage, electricite, couverture, peinture, restaurant. Style repris de site-dig/demos/menuisier.
# N'afficher que des faits vérifiés (RGE via l'annuaire ADEME, dates du registre) ; pas de faux avis.
import html,re,json,os
M=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','site-dig','demos','menuisier','index.html')).read()
CSS=M[M.index('<style>')+7:M.index('</style>')]
T={
'menuiserie':dict(c=('#9a5b2e','#6f3f1d'),v='repeating-linear-gradient(100deg,#b77a47 0 14px,#a86a39 14px 22px,#c2885a 22px 40px,#9b5f30 40px 46px)',
  h1='Menuiseries sur mesure, posées avec soin.',acc='Fenêtres, portes, volets et agencements : un seul interlocuteur du devis à la pose.',
  s=[('▢','Fenêtres & baies','Bois, alu ou PVC, double ou triple vitrage, pose en rénovation.'),('⌂',"Portes d'entrée",'Isolantes et sécurisées, dans le style de votre maison.'),('☀','Volets & portails','Battants, roulants ou motorisés.'),('▤','Agencement','Placards, dressings, escaliers sur mesure.'),('◧','Isolation','Amélioration du confort thermique de votre logement.'),('€','Aides à la rénovation','Nous vous orientons vers les aides possibles et les démarches.')],opt=['Fenêtres','Porte','Volets / portail','Agencement','Autre']),
'chauffage':dict(c=('#c2410c','#9a3412'),v='radial-gradient(circle at 30% 70%,#fb923c 0,#ea580c 25%,#7c2d12 60%,#1c1917 100%)',
  h1='Chauffage et confort, installés et entretenus près de chez vous.',acc="Pompes à chaleur, chaudières, poêles, plomberie : conseil, installation et dépannage.",
  s=[('♨','Pompes à chaleur','Air/eau, air/air : étude et installation.'),('🔥','Chaudières & poêles','Gaz, granulés, bois : installation et remplacement.'),('💧','Plomberie & sanitaire','Salle de bain, chauffe-eau, dépannage.'),('🛠','Entretien annuel','Contrat d’entretien et dépannage rapide.'),('☀','Énergies renouvelables','Solaire thermique, solutions économes.'),('€','Aides à la rénovation','Nous vous orientons vers les aides possibles et les démarches.')],opt=['Pompe à chaleur','Chaudière / poêle','Plomberie','Entretien / dépannage','Autre']),
'electricite':dict(c=('#1d4ed8','#1e3a8a'),v='linear-gradient(135deg,#0f172a 0,#1e3a8a 50%,#3b82f6 100%)',
  h1='Électricité et chauffage, en toute sécurité.',acc='Installation, rénovation, mise aux normes et dépannage pour particuliers et professionnels.',
  s=[('⚡','Installation électrique','Neuf et rénovation, tableaux, mises aux normes.'),('♨','Chauffage','Radiateurs, pompes à chaleur, chauffe-eau.'),('💡','Éclairage','Intérieur, extérieur, LED.'),('🔌','Bornes & domotique','Recharge de véhicule, pilotage à distance.'),('🛠','Dépannage','Intervention rapide sur panne.'),('€','Aides à la rénovation','Nous vous orientons vers les démarches.')],opt=['Installation','Mise aux normes','Chauffage','Dépannage','Autre']),
'couverture':dict(c=('#b45309','#78350f'),v='repeating-linear-gradient(170deg,#9a3412 0 18px,#7c2d12 18px 22px,#b45309 22px 40px,#7c2d12 40px 44px)',
  h1='Votre toiture entre de bonnes mains.',acc='Couverture tuiles et ardoises, charpente, zinguerie et isolation.',
  s=[('⌂','Couverture','Tuiles, ardoises, réfection complète ou partielle.'),('⟋','Charpente','Création et renforcement.'),('〰','Zinguerie','Gouttières, descentes, habillages.'),('▣','Fenêtres de toit','Pose et remplacement.'),('◧','Isolation','Isolation des combles et de la toiture.'),('🛠','Réparations','Fuites, tuiles cassées, après tempête.')],opt=['Couverture','Charpente','Zinguerie','Isolation','Réparation']),
'peinture':dict(c=('#0f766e','#115e59'),v='linear-gradient(120deg,#f5f5f4 0 30%,#99f6e4 30% 55%,#0f766e 55% 80%,#134e4a 80%)',
  h1='Peinture, façades et isolation : un intérieur neuf, une maison mieux isolée.',acc='Peinture intérieure, ravalement de façade et isolation thermique par l’extérieur.',
  s=[('🖌','Peinture intérieure','Murs, plafonds, boiseries, finitions soignées.'),('▦','Ravalement de façade','Nettoyage, réparation, peinture.'),('◧','Isolation extérieure','Moins de pertes de chaleur, façade rénovée.'),('▤','Revêtements','Sols et murs.'),('✦','Décoration','Conseil couleurs et matières.'),('€','Aides à la rénovation','Nous vous orientons vers les aides possibles et les démarches.')],opt=['Peinture intérieure','Façade','Isolation extérieure','Autre']),
'restaurant':dict(c=('#be123c','#881337'),v='radial-gradient(circle at 70% 30%,#fde68a 0,#f59e0b 20%,#9f1239 60%,#1c1917 100%)',
  h1='Une table au bord de l’eau.',acc='Cuisine de saison, produits frais et vins locaux.',
  s=[('🍽','La carte','Plats de saison, spécialités de la région.'),('🍷','Les vins','Une sélection de vins locaux.'),('☀','Terrasse','Profitez des beaux jours.'),('🎉','Groupes & événements','Anniversaires, repas de famille.'),('🛏','Chambres','Nuit sur place (selon disponibilités).'),('📅','Réservation','En ligne ou par téléphone.')],opt=['Réservation','Groupe / événement','Question']),
}
def page(p):
    t=T[p['type']];nom=html.escape(p['nom']);tel=p['tel'];num=re.sub(r'\D','',tel)
    css=(CSS+'.btn{white-space:nowrap}header .btn{padding:.6rem 1rem}.logo{line-height:1.2}').replace('--bois:#9a5b2e;--bois-fonce:#6f3f1d',f"--bois:{t['c'][0]};--bois-fonce:{t['c'][1]}")
    css=re.sub(r'\.visuel\{aspect-ratio:4/5;([^}]*)background:[^}]*\}',lambda m:'.visuel{aspect-ratio:4/5;'+m.group(1)+'background:'+t['v']+'}',css)
    css=css.replace('.visuel::after{','.visuel::after{display:none;')
    preuves=''.join(f'<div><b>{html.escape(a)}</b>{html.escape(b)}</div>' for a,b in p.get('preuves',[]))
    srv=''.join(f'<div class="carte"><div class="icone">{i}</div><h3>{html.escape(h)}</h3><p>{html.escape(x)}</p></div>' for i,h,x in t['s'])
    opts=''.join(f'<option>{o}</option>' for o in t['opt'])
    h1=html.escape(p.get('h1',t['h1']));acc=html.escape(p.get('acc',t['acc']))
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{nom} — maquette</title><meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"><style>{css}</style></head><body>
<div class="bandeau">Maquette préparée par Dig pour {nom} — proposition non publiée</div>
<header><div class="cadre"><a class="logo" href="#">{nom}</a><nav><a href="#services">Services</a><a href="#avis">Avis</a><a href="#contact">Contact</a></nav><a class="btn" href="#contact">{html.escape(p.get('cta','Devis gratuit'))}</a></div></header>
<main><section class="hero"><div class="cadre"><div><h1>{h1}</h1><p class="accroche">{acc}</p>
<div class="actions"><a class="btn" href="#contact">{html.escape(p.get('cta2','Demander un devis'))}</a><a class="btn clair" href="tel:{num}">{html.escape(tel)}</a></div>
<div class="preuves">{preuves}</div></div>
<div class="visuel" role="img" aria-label="Illustration"><div class="etiquette">{html.escape(p['commune'])} et alentours</div></div></div></section>
<section id="services"><div class="cadre"><div class="titre-section"><h2>Nos services</h2><p>{html.escape(p.get('sous','Particuliers et professionnels, devis gratuit.'))}</p></div><div class="grille">{srv}</div></div></section>
<section id="avis" class="avis"><div class="cadre"><div class="titre-section"><h2>Vos avis clients</h2><p>Ici s’afficheront automatiquement vos avis Google, pour rassurer chaque visiteur.</p></div></div></section>
<section id="contact"><div class="cadre contact"><div><div class="titre-section"><h2>Contact</h2><p>Réponse rapide, devis gratuit.</p></div><p><b>Téléphone :</b> {html.escape(tel)}</p><p><b>Secteur :</b> {html.escape(p['commune'])} et alentours</p></div>
<form class="carte" onsubmit="event.preventDefault()"><label>Votre nom<input></label><label>Téléphone ou email<input></label><label>Votre demande<select>{opts}</select></label><label>Message<textarea rows="3"></textarea></label><button class="btn" type="button">Envoyer</button></form></div></section></main>
<a class="btn appel-mobile" href="tel:{num}">📞 Appeler</a><footer><div class="cadre"><span>© {nom}</span><span>Maquette Dig</span></div></footer></body></html>'''
P=json.load(open('prospects.json'))
for p in P:
    open(f"{p['id']}.html",'w').write(page(p))
print(len(P))
