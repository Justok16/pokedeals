#!/usr/bin/env python3
"""Fiche d'appel d'une page par prospect (demande de l'utilisateur du 21/10/2026 : « Oui » à la proposition
« avant chacun de tes appels, une fiche d'une page : qui tu vas voir, ce que fait son entreprise, l'état de son site
et de sa fiche Google, 3 questions précises »).

Ce que l'outil fait seul, le jour même (règle « revérifier en ligne le jour même », leçon du 05/10) :
- annuaire officiel (Recherche d'entreprises, via le relais Vercel et le cookie /tmp/cj.txt) : dirigeants, forme,
  date de création, salariés, adresse, état ;
- site du prospect s'il en a un : réponse, HTTPS, adapté au téléphone, année la plus récente affichée, date de
  dernière mise à jour (sitemap), outil utilisé (SoLocal, Wix, Jimdo, WordPress…).
Ce qui vient du fichier d'entrée, relevé par Claude avec ses outils (sources citées dans la fiche) :
- BODACC (procédures collectives ET changements de nom : leçon du 21/10 : un prospect repris sous un nouveau
  nom avait encore sa fiche Google sous l'ancien), fiche Google et avis (recherche Google en direct, OpenRush, sur le NOM puis sur « métier + commune »
  pour voir la carte), recherches mensuelles du métier (OpenRush, France, estimation : toujours « environ »).

Les 3 questions viennent de `57-entretiens-etude-de-marche.md` et sont choisies selon la situation du prospect.
Aucun prix : on écoute (57). Les objections ont leurs réponses dans l'antisèche (`antiseche.py`).

Usage : python3 fiche_appel.py <lot.json> <dossier de sortie PRIVÉ>
Le lot et la sortie contiennent des données de prospects : scratchpad ou Drive « Dig », JAMAIS ce dépôt.
Format du lot : {"date": "21/10/2026", "titre": "...", "prospects": [{"num", "nom", "siren", "metier", "commune",
"telephone", "site"?, "google", "bodacc", "demande", "notes"?, "pourquoi"}]}
"""

import html
import json
import os
import re
import subprocess
import sys
import urllib.parse

ICI = os.path.dirname(os.path.abspath(__file__))
POLICES = os.path.join(ICI, "..", "..", "site-dig", "moteur", "polices", "instrumentserif-geist-geistmono.css")
RELAIS = "https://relais-dig-justok1.vercel.app/api/entreprise"
COOKIE = "/tmp/cj.txt"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
AGENT = "Mozilla/5.0 (compatible; DIG16-fiche/1.0; +https://dig16.fr)"
TRANCHES = {"NN": "aucun salarié déclaré", "00": "aucun salarié", "01": "1 ou 2 salariés", "02": "3 à 5 salariés",
            "03": "6 à 9 salariés", "11": "10 à 19 salariés", "12": "20 à 49 salariés", "21": "50 à 99 salariés"}
OUTILS_SITE = [("site-solocal", "SoLocal (PagesJaunes)"), ("solocal", "SoLocal (PagesJaunes)"), ("wix", "Wix"),
               ("jimdo", "Jimdo"), ("wp-content", "WordPress"), ("squarespace", "Squarespace"),
               ("webself", "Webself"), ("e-monsite", "e-monsite"), ("sitew", "SiteW")]
PETITS = r"\b(De|Du|Des|La|Le|Les|Sur|Sous|En|Et|Aux?|D|L|Rue|Route|Chemin|Avenue|Boulevard|Place|Impasse|Allée|Lieu-Dit)\b"


def e(t):
    return html.escape(str(t), quote=False)


def joli(t):
    """« MANSLE-LES-FONTAINES » → « Mansle-les-Fontaines », « SARL » gardé en capitales."""
    t = re.sub(PETITS, lambda m: m.group(0).lower(), (t or "").title())
    t = re.sub(r"\b(Sarl|Sas|Sasu|Eurl|Sci)\b", lambda m: m.group(0).upper(), t)
    return t[:1].upper() + t[1:]


def curl(url, cookie=False, tete=False):
    cmd = ["curl", "-s", "-L", "-m", "30", "-A", AGENT]
    if cookie:
        cmd += ["-b", COOKIE]
    if tete:
        cmd += ["-o", "/dev/null", "-w", "%{http_code} %{url_effective}"]
    return subprocess.run(cmd + [url], capture_output=True, text=True).stdout


def annuaire(siren):
    out = curl(f"{RELAIS}?q={siren}&per_page=1", cookie=True)
    if "Vercel Authentication" in out:
        sys.exit("Cookie du relais expiré : renouveler /tmp/cj.txt (33-outils.md), puis relancer.")
    try:
        r = json.loads(out)["results"][0]
    except Exception:
        return None
    s = r.get("siege") or {}
    dirigeants = []
    for d in r.get("dirigeants") or []:
        if "commissaire" in (d.get("qualite") or "").lower():
            continue
        famille = re.sub(r"\s*\(.*?\)", "", d.get("nom") or "").title()
        nom = " ".join(x for x in [(d.get("prenoms") or "").split(" ")[0].title(), famille] if x)
        nom = nom or (d.get("denomination") or "").title()
        nom = joli(nom)
        qualite = (d.get("qualite") or "").lower().replace(" de sas", " de SAS").replace("directeur général", "direction générale")
        if d.get("type_dirigeant") == "personne morale":
            qualite = "société"
        if nom:
            ligne = nom + (f" ({qualite})" if qualite else "")
            if ligne not in dirigeants:
                dirigeants.append(ligne)
    return {
        "nom_officiel": r.get("nom_complet") or "",
        "creation": (r.get("date_creation") or "")[:4],
        "salaries": TRANCHES.get(r.get("tranche_effectif_salarie") or "NN", "non déclaré"),
        "annee_salaries": r.get("annee_tranche_effectif_salarie") or "",
        "adresse": " ".join(str(x) for x in [s.get("numero_voie"), s.get("indice_repetition"), s.get("type_voie"),
                            s.get("libelle_voie"), s.get("complement_adresse") if not s.get("libelle_voie") else None,
                            s.get("code_postal"), s.get("libelle_commune")] if x).replace("None", "").strip(),
        "actif": r.get("etat_administratif") == "A",
        "dirigeants": dirigeants[:3],
        "forme": (r.get("nature_juridique") or ""),
    }


def analyser_site(url):
    if not url:
        return None
    code, _, finale = curl(url, tete=True).partition(" ")
    page = curl(url) if code.startswith("2") else ""
    bas = page.lower()
    annees = [int(a) for a in re.findall(r"(?:©|&copy;|copyright)\D{0,12}((?:19|20)\d\d)", page, re.I)]
    annees += [int(a) for a in re.findall(r"\b(20[0-2]\d)\b", re.sub(r"<script.*?</script>", "", page, flags=re.S))]
    outil = next((nom for cle, nom in OUTILS_SITE if cle in bas or cle in finale), "")
    maj = ""
    p = urllib.parse.urlparse(finale or url)
    plan = curl(f"{p.scheme}://{p.netloc}/sitemap.xml") if code.startswith("2") else ""
    dates = sorted(re.findall(r"<lastmod>(\d{4}-\d\d-\d\d)", plan))
    if dates:
        a, m, j = dates[-1].split("-")
        maj = f"{j}/{m}/{a}"
    return {
        "url": url, "code": code, "finale": finale, "https": finale.startswith("https"),
        "mobile": 'name="viewport"' in bas or "name=viewport" in bas, "outil": outil,
        "annee": max([a for a in annees if a <= 2026], default=0), "maj": maj,
    }


def questions(p, a, site):
    """3 questions de 57, dans l'ordre où les poser, choisies selon la situation."""
    q = ["D'où viennent vos derniers nouveaux clients ?"]
    if site and site["outil"].startswith("SoLocal"):
        q.append(f"Votre site {site['url'].split('//')[-1].rstrip('/')} : vous le payez encore ? Combien, et jusqu'à quand ?")
    elif site:
        q.append("Votre site vous amène-t-il des demandes ? Qui le met à jour aujourd'hui ?")
    else:
        q.append("Aujourd'hui, avez-vous besoin de davantage de demandes, ou vous êtes déjà complet ?")
    if a and a["salaries"] not in ("aucun salarié", "aucun salarié déclaré", "non déclaré"):
        q.append("En dehors du chantier, qu'est-ce qui vous prend le plus de temps : les devis, les factures, "
                 "le planning, les relances ? (si « devis » : combien par mois, combien signés ?)")
    else:
        q.append(f"Si vous cherchiez un {p['metier_court']} sur votre téléphone, vous taperiez quoi ? (noter les mots exacts)")
    return q


def bloc_site(site):
    if not site:
        return "<b>aucun site à son nom</b> (recherche du jour sur son nom et sa commune)."
    if not site["code"].startswith("2"):
        return f"<b>{e(site['url'])}</b> ne répond plus (code {e(site['code'] or 'aucun')})."
    L = [f"<b>{e(site['finale'].split('//')[-1].rstrip('/'))}</b>"]
    if site["outil"]:
        L.append(f"fait avec {e(site['outil'])}")
    if site["maj"]:
        L.append(f"dernière mise à jour déclarée : {e(site['maj'])}")
    elif site["annee"]:
        L.append(f"année la plus récente affichée : {site['annee']}")
    L.append("adapté au téléphone" if site["mobile"] else "<b>pas adapté au téléphone</b>")
    if not site["https"]:
        L.append("<b>sans cadenas (pas de HTTPS)</b>")
    return " · ".join(L)


def fiche(p, a, site, date, rang, total):
    qui = []
    if a:
        if a["dirigeants"]:
            qui.append(("Dirigeants : " if len(a["dirigeants"]) > 1 else "Dirigeant : ") + ", ".join(e(d) for d in a["dirigeants"]))
        qui.append(f"Créée en {e(a['creation'])} · {e(a['salaries'])}"
                   + (f" (donnée {e(str(a['annee_salaries']))})" if a["annee_salaries"] else ""))
        qui.append("Adresse au registre : " + e(joli(a["adresse"])))
        qui.append("Entreprise <b>active</b>" if a["actif"] else "<b>ATTENTION : fermée au registre, ne pas appeler</b>")
    else:
        qui.append("<b>Introuvable au registre par son SIREN : vérifier avant l'appel</b>")
    qui.append(e(p["bodacc"]))
    qs = "".join(f"<li>{e(x)}</li>" for x in questions(p, a, site))
    notes = f'<p class="note">{e(p["notes"])}</p>' if p.get("notes") else ""
    personnes = [d for d in (a or {}).get("dirigeants", []) if "(société)" not in d]
    demander = (f"<b>Demander :</b> {e(personnes[0].split(' (')[0])}" if personnes
                else "<b>Demander :</b> le dirigeant, ou la personne qui décide pour l'entreprise")
    return f"""<section class="page">
<div class="haut"><span>Appel {rang}/{total} · n° {e(str(p['num']))} de ta liste</span><span>Vérifiée le {e(date)} · PRIVÉ</span></div>
<h1>{e(p['nom'])}</h1>
<p class="metier">{e(p['metier'])} · {e(p['commune'])}</p>
<p class="tel">{e(p['telephone'])}</p><p class="dem">{demander}</p>
<div class="pourquoi"><b>Pourquoi l'appeler :</b> {e(p['pourquoi'])}</div>
<h2>Qui tu vas avoir</h2><ul>{''.join(f'<li>{x}</li>' for x in qui)}</ul>
<h2>Sur internet aujourd'hui</h2><ul><li>Site : {bloc_site(site)}</li><li>Google : {e(p['google'])}</li>
<li>Demande : {e(p['demande'])}</li></ul>{notes}
<h2>Tes 3 questions</h2><ol>{qs}</ol>
<div class="cadre"><b>Ouverture (20 s) :</b> « Bonjour, ici DIG16, une entreprise de Charente qui fait des sites pour
les artisans. Je fais le tour des professionnels du coin pour comprendre comment ça se passe pour eux sur internet. Je ne
vends rien aujourd'hui. Vous avez 3 minutes ? »
<br><b>Fin :</b> « Merci. D'ici quelques semaines, je peux vous rappeler pour vous montrer à quoi pourrait ressembler votre site, sans engagement ? » → noter oui / non / date.</div>
<div class="notes">Ce qu'il a dit (mots exacts) :</div>
</section>"""


CSS = """@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font-family:'Geist','Geist Fallback',Arial,sans-serif;
color:#1d1a16;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;padding:14mm 16mm 12mm;page-break-after:always;overflow:hidden;display:flex;flex-direction:column}
.page:last-child{page-break-after:auto}
.haut{display:flex;justify-content:space-between;font:11px 'Geist Mono','Geist Mono Fallback',monospace;letter-spacing:.06em;
text-transform:uppercase;color:#8a6d3b;border-bottom:1px solid #d9c9a8;padding-bottom:3mm}
h1{font:400 40px/1.05 'Instrument Serif','Instrument Serif Fallback',Georgia,serif;margin:5mm 0 1mm}
.metier{margin:0;color:#5b544a;font-size:15px}.tel{font:600 30px 'Geist Mono','Geist Mono Fallback',monospace;margin:2mm 0 0}.dem{margin:1mm 0 3mm;font-size:14px}
.pourquoi{background:#f6efe2;border-left:3px solid #b8925a;padding:3mm 4mm;font-size:14px;line-height:1.45}
h2{font:400 22px 'Instrument Serif','Instrument Serif Fallback',Georgia,serif;margin:4.5mm 0 1.5mm;color:#8a6d3b}
ul,ol{margin:0;padding-left:5mm;font-size:14px;line-height:1.5}li{margin:.7mm 0}ol li{font-size:15px;margin:1.5mm 0}
.note{font-size:13px;color:#5b544a;margin:2mm 0 0}
.cadre{margin-top:4mm;border:1px solid #d9c9a8;border-radius:3mm;padding:3mm 4mm;font-size:12.5px;line-height:1.45;color:#3a352e}
.notes{flex:1;min-height:20mm;margin-top:4mm;border:1px dashed #b8925a;border-radius:3mm;
padding:2mm 4mm;font-size:12px;color:#8a6d3b}
.couv h1{font-size:46px}.couv table{width:100%;table-layout:fixed;border-collapse:collapse;font-size:12.5px;margin-top:5mm}
.couv td,.couv th{border-bottom:1px solid #e6dcc8;padding:2.2mm 1.5mm;text-align:left;vertical-align:top}
.nw{white-space:nowrap}.couv th{font:11px 'Geist Mono','Geist Mono Fallback',monospace;text-transform:uppercase;color:#8a6d3b}
.regles{margin-top:6mm;font-size:13px;line-height:1.5;background:#f6efe2;padding:3mm 4mm;border-radius:3mm}"""


def couverture(lot, prospects):
    lignes = "".join(f"<tr><td>{i}</td><td>{e(str(p['num']))}</td><td><b>{e(p['nom'])}</b><br>{e(p['metier'])}, {e(p['commune'])}</td>"
                     f'<td class="nw">{e(p["telephone"])}</td><td>{e(p["pourquoi"])}</td></tr>'
                     for i, p in enumerate(prospects, 1))
    return f"""<section class="page couv"><div class="haut"><span>DIG16 · fiches d'appel</span>
<span>Vérifiées le {e(lot['date'])} · PRIVÉ</span></div><h1>{e(lot['titre'])}</h1>
<p class="metier">Dans l'ordre conseillé. Une page par entreprise, avec tes 3 questions et la place pour noter.</p>
<table><colgroup><col style="width:7%"><col style="width:7%"><col style="width:32%"><col style="width:17%"><col style="width:37%"></colgroup><tr><th>Ordre</th><th>N° liste</th><th>Entreprise</th><th>Téléphone</th><th>Pourquoi l'appeler</th></tr>{lignes}</table>
<div class="regles"><b>Rappels :</b> on écoute, on note les mots exacts, on ne propose ni prix ni offre (57).
Les 3 questions sont choisies pour chacun ; si l'échange dure, continue avec les 7 questions de la fiche 57
(dont « Qui décide d'un changement ? »). Si « non » : « Pas de souci, bonne journée », on ne rappelle pas. Après l'appel, dis-moi le résultat :
je le note dans ton suivi et je prépare la suite.</div></section>"""


def typo(t):
    for a, b in ((" :", " :"), (" ?", " ?"), (" !", " !"), (" ;", " ;"), ("« ", "« "), (" »", " »")):
        t = t.replace(a, b)
    return re.sub(r"(?<=\w)'(?=\w)", "’", t)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    lot = json.load(open(sys.argv[1], encoding="utf-8"))
    sortie = sys.argv[2]
    if os.path.abspath(sortie).startswith(os.path.abspath(os.path.join(ICI, "..", "..", "..", ".."))):
        sys.exit("Sortie dans le dépôt public refusée : utiliser le scratchpad ou le Drive « Dig ».")
    os.makedirs(sortie, exist_ok=True)
    pages, resume = [], []
    for p in lot["prospects"]:
        a = annuaire(p["siren"]) if p.get("siren") else None
        site = analyser_site(p.get("site"))
        p.setdefault("metier_court", p["metier"].split(",")[0].lower())
        pages.append(fiche(p, a, site, lot["date"], len(pages) + 1, len(lot["prospects"])))
        resume.append({"num": p["num"], "nom": p["nom"], "annuaire": a, "site": site})
        print(f"n° {p['num']} {p['nom']} : registre {'ok' if a else 'INTROUVABLE'}"
              + (f", site {site['code']} {site['outil']} maj {site['maj'] or site['annee']}" if site else ", sans site"))
    corps = typo(couverture(lot, lot["prospects"]) + "".join(pages))
    polices = open(POLICES, encoding="utf-8").read().replace("/moteur/polices/", "file://" + os.path.dirname(os.path.abspath(POLICES)) + "/")
    page = (f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><style>{polices}{CSS}</style></head><body>{corps}</body></html>")
    nom = os.path.join(sortie, "fiches-appel")
    open(nom + ".html", "w", encoding="utf-8").write(page)
    json.dump(resume, open(nom + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else pw.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + os.path.abspath(nom + ".html"))
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        if not pg.evaluate("document.fonts.check('16px Geist') && document.fonts.check('16px \\'Instrument Serif\\'')"):
            sys.exit("ALERTE : polices DIG16 non chargées.")
        trop = pg.evaluate("[...document.querySelectorAll('.page')].map((s,i)=>(s.scrollHeight>s.clientHeight+1||s.scrollWidth>s.clientWidth+1)?i+1:0).filter(Boolean)")
        pg.pdf(path=nom + ".pdf", prefer_css_page_size=True, print_background=True)
        b.close()
    if trop:
        sys.exit(f"ALERTE : page(s) {trop} trop longue(s), raccourcir les textes.")
    print("PDF :", nom + ".pdf")


if __name__ == "__main__":
    main()
