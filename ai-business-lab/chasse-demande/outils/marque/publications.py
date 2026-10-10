#!/usr/bin/env python3
"""Calendrier complet des publications DIG16 sur 8 semaines, prêt à programmer (08/10/2026).

Réunit les textes déjà validés (50-campagne-lancement.md § 9, 61-plan-publicite.md § 3, 62-campagne-test-du-pouce.md)
et fabrique pour chacun un visuel 1080 × 1350 à la charte (60-charte-dig16.md), avec l'empreinte de la campagne.

Usage : python3 outils/marque/publications.py
  écrit supports/publications/ : un PNG par publication, calendrier.csv (lisible dans un tableur) et
  calendrier.json (programmation par Claude dans Metricool, outil createScheduledPost, le jour de l'immatriculation).
Dates : en jours après le « jour J » (premier lundi suivant la validation de l'entreprise) ; aucune date absolue.
Contrôles : textes Bluesky ≤ 300 caractères (limite indiquée par l'outil Metricool), publication Google ≤ 1 500,
textes alternatifs présents, visuels sans débordement, polices chargées. Publications qui exigent un fait réel
(premier client, bilan) : statut « manuel », jamais programmées automatiquement.
"""

import base64
import csv
import json
import os
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from empreinte import empreinte_svg  # noqa: E402

RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
SORTIE = os.path.join(RACINE, "supports", "publications")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
BRUT = ("https://raw.githubusercontent.com/Justok16/pokedeals/claude/ai-business-portfolio-strategy-96yf4g/"
        "ai-business-lab/chasse-demande/supports/")
TAGS = "\n\n#Charente #artisan #commerce #siteinternet"
RESEAUX = ["facebook", "instagram", "linkedin", "gmb", "bluesky", "threads"]
JOURS = {"lundi": 0, "mardi": 1, "mercredi": 2, "jeudi": 3, "vendredi": 4}
THEMES = {"montrer": "À voir", "aider": "Un conseil", "rassurer": "Comment je travaille", "pouce": "Le test du pouce"}

# id, semaine, jour, thème, titre du visuel (ligne 1 | ligne 2 dorée), texte complet, statut
P = [
    ("s1-lancement", 1, "lundi", "montrer", "DIG16 est lancé.|Des sites à votre nom.",
     "DIG16 est lancé 🎉\nJe crée des sites internet pour les artisans, commerçants et indépendants de Charente : "
     "modernes, rapides, pensés d'abord pour le téléphone, et à votre nom.\nVous voulez voir ce que ça donnerait pour "
     "vous ? Je refais votre page d'accueil gratuitement, avant que vous décidiez quoi que ce soit.\n👉 dig16.fr", "auto"),
    ("s1-pouce", 1, "mardi", "pouce", "CARROUSEL",
     "Le test du pouce 👍 30 secondes, votre téléphone, votre métier et votre ville. Vous êtes où ?\nFaites le test, "
     "puis glissez jusqu'au bout. Ou faites-le en ligne, gratuitement : dig16.fr/test-du-pouce\nUn « non » ? Je refais votre page d'accueil gratuitement.", "auto"),
    ("s1-fiche-google", 1, "mercredi", "aider", "Votre fiche Google :|3 choses à vérifier.",
     "3 choses à vérifier aujourd'hui sur votre fiche Google :\n1️⃣ Vos horaires sont-ils à jour (jours fériés "
     "compris) ?\n2️⃣ Votre numéro de téléphone est-il le bon ?\n3️⃣ Avez-vous au moins quelques photos récentes de "
     "votre travail ?\nC'est gratuit, ça prend 10 minutes, et c'est souvent la première chose que vos clients voient "
     "de vous.", "auto"),
    ("s1-methode", 1, "vendredi", "rassurer", "Un site avec DIG16,|comment ça se passe ?",
     "Un site avec DIG16, comment ça se passe ?\n✅ Je refais votre page d'accueil gratuitement, pour que vous "
     "puissiez juger sur pièce.\n✅ 20 minutes ensemble pour vos textes et vos photos.\n✅ En ligne en 7 jours.\n✅ Le "
     "site et le nom de domaine sont à votre nom.\nDès 49 € par mois, 0 € de création. Les détails : dig16.fr", "auto"),
    ("s2-demo-menuisier", 2, "lundi", "montrer", "Un site d'artisan,|sur un téléphone.",
     "Voici à quoi ressemble un site DIG16 sur un téléphone 📱\nUne menuiserie (entreprise fictive) : ses réalisations "
     "en photos, ses services et un bouton pour appeler en un geste.\nImaginez le vôtre. Je refais votre page "
     "d'accueil gratuitement : dig16.fr", "auto"),
    ("s2-numero", 2, "mercredi", "aider", "Votre numéro|s'appelle d'un geste ?",
     "Sur votre site, votre numéro de téléphone est-il cliquable ?\nSur un téléphone, vos clients veulent appeler en "
     "un geste, pas recopier 10 chiffres.\nTestez votre site depuis votre téléphone : si rien ne se passe en touchant "
     "le numéro, c'est à corriger.", "auto"),
    ("s2-a-votre-nom", 2, "vendredi", "rassurer", "Votre site est à vous.|Pas à moi.",
     "Avec DIG16, votre site et votre nom de domaine sont à votre nom. Pas au mien.\nSi un jour vous partez, vous "
     "gardez tout : votre adresse internet, vos textes, vos photos.", "auto"),
    ("s3-pouce-rappel", 3, "lundi", "pouce", "Vous avez fait|le test du pouce ?",
     "Vous avez fait le test du pouce ? Tapez votre métier et votre ville sur votre téléphone… et dites-moi en "
     "commentaire ce que vous avez trouvé (sans nommer personne 🙂).\nLe test en ligne, gratuit : dig16.fr/test-du-pouce",
     "auto"),
    ("s3-photos", 3, "mercredi", "aider", "3 conseils pour|de belles photos.",
     "3 conseils pour vos photos de chantier ou de boutique :\n1️⃣ Photographiez en journée, lumière naturelle.\n2️⃣ "
     "Montrez le résultat fini, de face, sans désordre autour.\n3️⃣ Une photo nette vaut mieux que dix floues.", "auto"),
    ("s3-prix", 3, "vendredi", "rassurer", "Combien coûte|un site DIG16 ?",
     "Combien coûte un site avec DIG16 ?\n0 € de création sur les formules mensuelles, puis dès 49 € par mois : "
     "hébergement, sécurité, modifications et suivi compris.\n6 mois d'engagement, puis vous arrêtez quand vous "
     "voulez. Tout est sur dig16.fr", "auto"),
    ("s4-avant-apres", 4, "lundi", "montrer", "Avant, après :|la même page d'accueil.",
     "Avant / après : une page d'accueil d'artisan (fictive) refaite par DIG16.\nPlus claire, plus rapide, et le "
     "numéro bien en vue.\nVous voulez la même chose pour votre entreprise ? C'est gratuit pour voir : dig16.fr", "auto"),
    ("s4-avis", 4, "mercredi", "aider", "Un avis négatif ?|Répondez-y.",
     "Un avis négatif sur votre fiche Google ? Répondez-y, calmement et poliment.\nVos futurs clients lisent surtout "
     "votre réponse : c'est elle qui montre votre sérieux.", "auto"),
    ("s4-sans-engagement", 4, "vendredi", "rassurer", "Après 6 mois,|sans engagement.",
     "Après 6 mois, votre site DIG16 est sans engagement : vous pouvez arrêter à tout moment, par simple email.\nEt "
     "vous repartez avec tous les fichiers de votre site.", "auto"),
    ("s5-7-jours", 5, "lundi", "montrer", "En ligne|en 7 jours.",
     "Un site en ligne en 7 jours, comment c'est possible ?\nJour 1 : 20 minutes ensemble pour vos textes et vos "
     "photos.\nJours 2 à 6 : je construis, vous relisez.\nJour 7 : votre site est en ligne.", "auto"),
    ("s5-horaires", 5, "mercredi", "aider", "Vos horaires,|les mêmes partout ?",
     "Vos horaires sont-ils les mêmes sur votre site, votre fiche Google et votre page Facebook ?\nUn client qui trouve "
     "porte close à cause d'un horaire erroné ne revient pas toujours.", "auto"),
    ("s5-suivi", 5, "vendredi", "rassurer", "Un site suivi,|chaque mois.",
     "Avec DIG16, votre site n'est pas abandonné après sa mise en ligne.\nChaque mois : sécurité, sauvegardes, et vos "
     "changements faits en 3 jours ouvrés.", "auto"),
    ("s6-rapidite", 6, "lundi", "montrer", "Un site qui s'affiche|vite sur un téléphone.",
     "Combien de temps met votre site à s'afficher sur un téléphone ?\nAu-delà de quelques secondes, beaucoup de "
     "visiteurs repartent. Les sites DIG16 sont construits pour être rapides.", "auto"),
    ("s6-description", 6, "mercredi", "aider", "Votre métier|en 3 phrases.",
     "Une bonne description de votre entreprise tient en 3 phrases :\nce que vous faites, où vous intervenez, et ce "
     "qui vous distingue.\nExemple : « Menuisier en Charente, je fabrique et pose fenêtres et escaliers sur mesure. »",
     "auto"),
    ("s6-recommandation", 6, "vendredi", "rassurer", "Recommandez un artisan,|un mois offert.",
     "Vous connaissez un artisan ou un commerçant qui a besoin d'un site ?\nRecommandez-le : s'il devient client, votre "
     "prochain mois est offert, et son premier mois aussi.", "auto"),
    ("s7-premier-client", 7, "lundi", "montrer", "Premier site DIG16|en ligne.",
     "Premier site DIG16 en ligne 🎉 Merci à [client] pour sa confiance.\n(À publier seulement avec l'accord écrit du "
     "client ; sinon, nouvelle démo fictive.)", "manuel"),
    ("s7-site-lent", 7, "mercredi", "aider", "Un site lent ?|Regardez vos photos.",
     "Un site lent, ce sont souvent des photos trop lourdes. Une photo de plusieurs mégaoctets peut presque toujours "
     "être allégée fortement sans perte visible.", "auto"),
    ("s7-questions", 7, "vendredi", "rassurer", "Les questions|qu'on me pose le plus.",
     "Les questions qu'on me pose le plus :\n« Je dois écrire les textes ? » Non, je les rédige avec vous.\n« Je peux "
     "modifier mon site ? » Oui, envoyez-moi un email, c'est fait en 3 jours ouvrés.\n« Et si j'arrête ? » Vous "
     "gardez votre nom de domaine et vos fichiers.", "auto"),
    ("s8-bilan", 8, "lundi", "montrer", "Deux mois de DIG16.|Merci.",
     "Deux mois de DIG16 : merci à tous ceux qui ont fait confiance à une jeune entreprise de Charente.\n(Chiffres "
     "réels seulement, vérifiés avant publication.)", "manuel"),
    ("s8-saison", 8, "mercredi", "aider", "Préparez votre saison|dès maintenant.",
     "Préparez votre saison maintenant : horaires, photos récentes, offres du moment. Un site à jour, ce sont des "
     "appels en plus.", "auto"),
    ("s8-offre", 8, "vendredi", "rassurer", "Votre page d'accueil,|refaite gratuitement.",
     "Votre page d'accueil refaite gratuitement, pour voir avant de décider.\nAucune obligation. Écrivez-moi ou "
     "appelez : dig16.fr", "auto"),
]

CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{margin:0}
body{width:1080px;height:1350px;overflow:hidden;font-family:Geist,sans-serif;color:#efe9df;position:relative;background:#0f0e0c;
background-image:radial-gradient(80% 60% at 92% 0%,rgba(200,164,110,.16),rgba(200,164,110,0) 70%),radial-gradient(70% 50% at 0% 100%,rgba(200,164,110,.07),rgba(200,164,110,0) 70%)}
.deco{position:absolute;pointer-events:none}.z{position:absolute;left:72px;right:72px}
.haut{top:72px;display:flex;justify-content:space-between;align-items:center}.haut img{height:44px}
.theme{font:500 28px Geist;color:#c8a46e}
h1{font:400 118px/1 'Instrument Serif';letter-spacing:-.025em;text-wrap:balance}h1 span{display:block;color:#d9bb8a}
.bas{bottom:72px;display:flex;justify-content:space-between;align-items:center}
.site{font:500 36px Geist}.site span{color:#c8a46e}
.bouton{font:500 27px Geist;background:#c8a46e;color:#14110d;border-radius:999px;padding:18px 34px}"""
POLICES = ('<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500'
           '&display=block" rel="stylesheet">')
PLACES = {"montrer": "right:-330px;top:-220px", "aider": "right:-360px;top:-300px;transform:rotate(-28deg)",
          "rassurer": "right:-300px;bottom:-330px", "pouce": "right:-380px;top:-200px"}


def logo():
    with open(os.path.join(RACINE, "site-dig", "img", "marque", "signature-ivoire@2x.png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def visuel(theme, titre, n):
    l1, l2 = titre.split("|")
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8">{POLICES}<style>{CSS}</style></head><body>'
            f'<div class="deco" style="{PLACES[theme]}">{empreinte_svg(820, opacite=.5, ident="e" + str(n))}</div>'
            f'<div class="z haut"><img src="{logo()}" alt="DIG16"></div>'
            f'<div class="z" style="top:50%;transform:translateY(-50%)"><div class="theme">{THEMES[theme]}</div>'
            f'<h1 style="margin-top:26px">{l1}<span>{l2}</span></h1></div>'
            '<div class="z bas"><div class="site">dig16<span>.fr</span></div><div class="bouton">Recevoir ma démo gratuite'
            '</div></div></body></html>')


def bluesky(texte):
    if len(texte) <= 300:
        return texte
    premiere = texte.split("\n")[0]
    court = premiere if "dig16.fr" in premiere else premiere + "\n👉 dig16.fr"
    return court if len(court) <= 300 else court[:280].rsplit(" ", 1)[0] + "… dig16.fr"


def main():
    os.makedirs(SORTIE, exist_ok=True)
    fautes, lignes = [], []
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 1080, "height": 1350})
        for n, (ident, sem, jour, theme, titre, texte, statut) in enumerate(P):
            if titre == "CARROUSEL":
                images = [f"campagne-pouce/pouce-{k}.png" for k in range(1, 6)]
                alt = ["Le test du pouce : prenez votre téléphone et tapez votre métier et votre ville.",
                       "Un téléphone affiche des résultats de recherche ; une place vide porte la question « Et vous ? ».",
                       "Deuxième étape : touchez votre nom ; le site s'ouvre-t-il bien, le numéro s'appelle-t-il d'un geste ?",
                       "Avant, après : un site daté et le même site refait par DIG16 (exemple fictif).",
                       "Ce que vous obtenez : 0 € de création, en ligne en 7 jours, site à votre nom, dès 49 € par mois."]
            else:
                pg.set_content(visuel(theme, titre, n), wait_until="networkidle")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(300)
                r = pg.evaluate("""(()=>{const h=document.querySelector('h1').getBoundingClientRect();
                  const t=document.querySelector('.haut').getBoundingClientRect(),b=document.querySelector('.bas').getBoundingClientRect();
                  return [h.top>t.bottom+40&&h.bottom<b.top-40&&h.right<=1008,[...document.fonts].filter(f=>f.status==='loaded').length]})()""")
                if not r[0]:
                    fautes.append(f"{ident} : titre trop grand pour le visuel")
                if r[1] < 2:
                    fautes.append(f"{ident} : polices non chargées")
                pg.screenshot(path=os.path.join(SORTIE, ident + ".png"))
                images = [f"publications/{ident}.png"]
                alt = [f"{titre.replace('|', ' ')} DIG16, sites internet pour artisans et commerçants de Charente."]
            complet = texte + TAGS
            if len(complet) > 1500:
                fautes.append(f"{ident} : texte trop long pour la fiche Google")
            bs = bluesky(texte)
            if len(bs) > 300:
                fautes.append(f"{ident} : texte Bluesky trop long")
            lignes.append({"id": ident, "semaine": sem, "jour": jour, "decalage_jours": (sem - 1) * 7 + JOURS[jour],
                           "heure": "18:30", "theme": THEMES[theme], "statut": statut, "reseaux": RESEAUX,
                           "texte": complet, "texte_bluesky": bs, "images": [BRUT + i for i in images],
                           "fichiers": ["supports/" + i for i in images], "textes_alternatifs": alt})
        story = "campagne-pouce/pouce-story.png"
        for ident, sem, jour in [("s1-story-pouce", 1, "mardi"), ("s3-story-pouce", 3, "lundi")]:
            lignes.append({"id": ident, "semaine": sem, "jour": jour, "decalage_jours": (sem - 1) * 7 + JOURS[jour],
                           "heure": "12:15", "theme": "Le test du pouce (story)", "statut": "auto",
                           "reseaux": ["instagram:STORY", "facebook:STORY"], "texte": "", "texte_bluesky": "",
                           "images": [BRUT + story], "fichiers": ["supports/" + story],
                           "textes_alternatifs": ["Le test du pouce en 3 étapes : tapez votre métier et votre ville, "
                                                  "cherchez-vous, touchez votre nom."]})
        nav.close()
    lignes.sort(key=lambda x: (x["decalage_jours"], x["heure"]))
    with open(os.path.join(SORTIE, "calendrier.json"), "w", encoding="utf-8") as f:
        json.dump(lignes, f, ensure_ascii=False, indent=1)
    with open(os.path.join(SORTIE, "calendrier.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Jour J +", "Semaine", "Jour", "Heure", "Thème", "Statut", "Réseaux", "Texte", "Texte Bluesky",
                    "Images", "Textes alternatifs"])
        for x in lignes:
            w.writerow([x["decalage_jours"], x["semaine"], x["jour"], x["heure"], x["theme"], x["statut"],
                        ", ".join(x["reseaux"]), x["texte"], x["texte_bluesky"], " ".join(x["fichiers"]),
                        " | ".join(x["textes_alternatifs"])])
    noms = [x["id"] + ".png" for x in lignes if x["fichiers"][0].startswith("supports/publications/")]
    ims = [Image.open(os.path.join(SORTIE, n)).convert("RGB").resize((216, 270)) for n in noms]
    col = 6
    pl = Image.new("RGB", (col * 226 + 10, ((len(ims) + col - 1) // col) * 280 + 10), "#f3eee5")
    for i, im in enumerate(ims):
        pl.paste(im, (10 + (i % col) * 226, 10 + (i // col) * 280))
    pl.save(os.path.join(SORTIE, "planche.png"))
    print(len(lignes), "publications au calendrier,", sum(x["statut"] == "manuel" for x in lignes), "manuelles")
    for f in fautes:
        print("ALERTE", f)
    return 1 if fautes else 0


if __name__ == "__main__":
    raise SystemExit(main())
