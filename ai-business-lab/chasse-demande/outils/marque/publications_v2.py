#!/usr/bin/env python3
"""Série 2 des publications DIG16 (19/10/2026) : carrousels 1080 × 1350 pour Instagram, Facebook, Threads et TikTok.

Pourquoi (demande de l'utilisateur du 19/10 : « pousse au maximum la campagne ») : les 19 visuels de la série 1 étaient
tous identiques (fond sombre, titre seul) et deux ne montraient pas ce que le texte annonçait (« un site sur un
téléphone » sans téléphone, « avant / après » sans avant ni après). Série 2 :
- fonds clair et sombre en alternance (charte `60-charte-dig16.md`, comme le flyer) ;
- carrousels de 4 à 5 images (couverture, idées, appel), que TikTok et Instagram font défiler ;
- vraies captures des démonstrations du site (entreprises fictives, mention sur l'image) dans un téléphone ;
- **ni téléphone ni email sur les images** (réutilisables partout, règle des posts Google, leçon du 18/10) ;
- JPEG (TikTok n'accepte que JPEG ou WebP, documentation développeurs TikTok lue le 19/10), hébergés sur
  dig16.fr/img/reseaux/pub/ pour la programmation dans Metricool.
Chaque phrase reprend un texte déjà publié (légendes validées de la série 1, guide /site-internet-artisan/, CGV) :
rien d'inventé, aucun chiffre nouveau.

Usage : python3 outils/marque/publications_v2.py [identifiant…]
Écrit site-dig/img/reseaux/pub/<id>-<n>.jpg, une planche de contrôle dans supports/publications-v2/planche.jpg et
supports/publications-v2/series.json (textes et liens des images, pour Metricool).
Contrôles bloquants : polices chargées, aucun texte hors de la marge, aucun débordement, aucun chiffre de téléphone
ni « @ » dans les textes des images, images du téléphone chargées.
"""

import base64
import json
import os
import re
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from empreinte import empreinte_svg  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
SITE = os.path.join(RACINE, "site-dig")
SORTIE = os.path.join(SITE, "img", "reseaux", "pub")
SUPPORTS = os.path.join(RACINE, "supports", "publications-v2")
POLICES = os.path.join(SITE, "moteur", "polices")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
URL = "https://dig16.fr/img/reseaux/pub/"
MARGE = 84

ESSENTIEL = "vitrine-essentiel-tel.webp"
VISITE = "vitrine-visite-tel.webp"
PRESTIGE = "vitrine-prestige-tel.webp"

APPEL = ("cta", "Et le vôtre, *on le regarde ensemble ?*",
         "Je refais votre page d'accueil gratuitement, avant que vous décidiez quoi que ce soit.")

# Chaque publication : identifiant, date, thème, étiquette, images, légende (sans l'appel final, ajouté par réseau),
# texte alternatif. Les dates reprennent les créneaux déjà programmés (lundi, mercredi, vendredi à 18 h 30).
SERIE = [
    {"id": "p01", "date": "2026-10-19T18:30:00", "theme": "sombre", "etiquette": "À voir", "metricool": 392399762,
     "titre_tiktok": "Un site DIG16, sur un téléphone",
     "images": [
         ("phones", "Voici des sites DIG16, *sur un téléphone.*", [ESSENTIEL, VISITE, PRESTIGE],
          "Démonstrations · entreprises fictives"),
         ("phone", "Vos photos d'abord, *le devis d'un geste.*", ESSENTIEL,
          "Une menuiserie : ses réalisations en photos, ses services et un bouton pour appeler."),
         ("phone", "La visite de l'atelier, *en faisant défiler.*", VISITE,
          "Le même artisan, en plus immersif : de la planche à la pose."),
         APPEL],
     "legende": "Voici à quoi ressemble un site DIG16 sur un téléphone 📱 Faites glisser.\n"
                "Une menuiserie et sa visite d'atelier (entreprises fictives) : les réalisations en photos, les services, "
                "et un bouton pour appeler d'un geste.\nImaginez le vôtre : je refais votre page d'accueil gratuitement, "
                "avant que vous décidiez.",
     "alt": "Trois sites de démonstration DIG16 affichés sur un téléphone : menuiserie, visite d'atelier, maison d'hôtes."},
    {"id": "p02", "date": "2026-10-21T18:30:00", "theme": "clair", "etiquette": "Le conseil", "metricool": 392399835,
     "titre_tiktok": "Votre numéro s'appelle-t-il d'un geste ?",
     "images": [
         ("cover", "Votre numéro *s'appelle-t-il d'un geste ?*", "Un test à faire depuis votre téléphone."),
         ("point", "1", "Ouvrez votre site *sur votre téléphone.*", "Comme le ferait un client qui vous cherche."),
         ("point", "2", "Touchez *votre numéro.*", "Le téléphone vous propose d'appeler ? C'est bon."),
         ("point", "3", "Rien ne se passe ? *C'est à corriger.*",
          "Vos clients veulent appeler en un geste, pas recopier 10 chiffres."),
         APPEL],
     "legende": "Sur votre site, votre numéro de téléphone est-il cliquable ? 📞\n"
                "Sur un téléphone, vos clients veulent appeler en un geste, pas recopier 10 chiffres.\n"
                "Testez votre site depuis votre téléphone : si rien ne se passe en touchant le numéro, c'est à corriger.",
     "alt": "Le conseil DIG16 : vérifier que son numéro s'appelle d'un geste, en 3 étapes."},
    {"id": "p03", "date": "2026-10-23T18:30:00", "theme": "sombre", "etiquette": "Comment je travaille",
     "metricool": 392400103, "titre_tiktok": "Votre site est à vous. Pas à moi.",
     "images": [
         ("cover", "Votre site est à vous. *Pas à moi.*", "Ce qui change tout : le nom de domaine."),
         ("point", "1", "Le nom de domaine, *à votre nom.*",
          "L'adresse de votre site est enregistrée à votre nom, pas à celui du prestataire."),
         ("point", "2", "Si vous partez, *vous gardez tout.*", "Votre adresse internet, vos textes, vos photos, vos fichiers."),
         ("point", "3", "Avant de signer, *demandez-le par écrit.*", "Chez n'importe quel prestataire, DIG16 compris."),
         APPEL],
     "legende": "Avec DIG16, votre site et votre nom de domaine sont à votre nom. Pas au mien. 🔑\n"
                "Si un jour vous partez, vous gardez tout : votre adresse internet, vos textes, vos photos.\n"
                "Et chez n'importe quel prestataire : demandez-le par écrit avant de signer.",
     "alt": "Votre site est à vous, pas à moi : le nom de domaine à votre nom, et vous gardez tout si vous partez."},
    {"id": "p04", "date": "2026-10-26T18:30:00", "theme": "clair", "etiquette": "Le conseil", "metricool": 399469211,
     "titre_tiktok": "Les mentions légales, obligatoires",
     "images": [
         ("cover", "Les mentions légales : *obligatoires.*", "Pour tout site professionnel en France."),
         ("liste", "Ce qu'elles indiquent", ["Votre nom", "Votre adresse", "Votre numéro d'immatriculation",
                                              "L'hébergeur du site"]),
         ("point", "", "Elles manquent sur votre site ? *Ajoutez-les.*",
          "Sur un site DIG16, elles sont comprises, comme la page sur les données personnelles."),
         APPEL],
     "legende": "Les mentions légales sont obligatoires pour tout site professionnel en France ⚖️\n"
                "Elles indiquent votre nom, votre adresse, votre numéro d'immatriculation et l'hébergeur du site.\n"
                "Elles manquent sur le vôtre ? Ajoutez-les. Sur un site DIG16, elles sont comprises.",
     "alt": "Le conseil DIG16 : les mentions légales sont obligatoires, avec ce qu'elles doivent indiquer."},
    {"id": "p05", "date": "2026-10-28T18:30:00", "theme": "sombre", "etiquette": "Le conseil", "metricool": 392400668,
     "titre_tiktok": "3 conseils pour de belles photos",
     "images": [
         ("cover", "3 conseils pour *de belles photos.*", "De chantier ou de boutique."),
         ("point", "1", "En journée, *en lumière naturelle.*", "Une photo prise de jour est plus fidèle à votre travail."),
         ("point", "2", "Le résultat fini, *de face.*", "Sans désordre autour."),
         ("point", "3", "Une photo nette *vaut mieux que dix floues.*", "Gardez seulement les meilleures."),
         APPEL],
     "legende": "3 conseils pour vos photos de chantier ou de boutique 📸\n"
                "1️⃣ Photographiez en journée, en lumière naturelle.\n2️⃣ Montrez le résultat fini, de face, sans désordre autour.\n"
                "3️⃣ Une photo nette vaut mieux que dix floues.",
     "alt": "Le conseil DIG16 : 3 conseils pour de belles photos de chantier ou de boutique."},
    {"id": "p06", "date": "2026-10-30T18:30:00", "theme": "clair", "etiquette": "Combien ça coûte", "metricool": 392400688,
     "titre_tiktok": "Combien coûte un site DIG16 ?",
     "images": [
         ("cover", "Combien coûte *un site DIG16 ?*", "Tout est écrit, noir sur blanc."),
         ("prix",),
         ("formules",),
         ("point", "", "6 mois d'engagement, *puis vous arrêtez quand vous voulez.*",
          "Le nom de domaine, à votre nom : environ 10 € par an. TVA non applicable, article 293 B du CGI."),
         APPEL],
     "legende": "Combien coûte un site avec DIG16 ? 💶\n"
                "0 € de création sur les formules mensuelles, puis dès 49 € par mois : hébergement, modifications et suivi compris.\n"
                "6 mois d'engagement, puis vous arrêtez quand vous voulez.",
     "alt": "Les prix DIG16 : 0 € de création, dès 49 € par mois, ou 690 € à l'achat."},
    {"id": "p07", "date": "2026-11-02T18:30:00", "theme": "sombre", "etiquette": "À voir", "metricool": 392400785,
     "titre_tiktok": "Avant, après : la même page d'accueil",
     "images": [
         ("avantapres", "Avant, après : *la même page d'accueil.*"),
         ("point", "1", "Une page *claire.*", "Votre métier et votre secteur, lisibles sans zoomer."),
         ("point", "2", "Vos réalisations, *en grandes photos.*", "C'est ce que vos clients viennent voir."),
         ("point", "3", "Un bouton pour *demander un devis.*", "En haut de la page, toujours à portée de pouce."),
         APPEL],
     "legende": "Avant / après : une page d'accueil d'artisan refaite par DIG16 (exemple fictif) ✨\n"
                "Plus claire, les réalisations en grand, et le devis à portée de pouce.\n"
                "Vous voulez voir la même chose pour votre entreprise ? C'est gratuit pour voir.",
     "alt": "Avant, après : une page d'accueil d'artisan démodée, puis la même refaite par DIG16 (exemple fictif)."},
    {"id": "p08", "date": "2026-11-04T18:30:00", "theme": "clair", "etiquette": "Le conseil", "metricool": 392400832,
     "titre_tiktok": "Un avis négatif ? Répondez-y.",
     "images": [
         ("cover", "Un avis négatif ? *Répondez-y.*", "Sur votre fiche Google."),
         ("point", "1", "Répondez à chaque avis, *bon ou mauvais.*", "Calmement et poliment."),
         ("point", "2", "Vos futurs clients *lisent votre réponse.*", "C'est elle qui montre votre sérieux."),
         ("point", "3", "Un vrai avis, même moyen, *inspire confiance.*", "Surtout suivi d'une réponse polie."),
         APPEL],
     "legende": "Un avis négatif sur votre fiche Google ? Répondez-y, calmement et poliment ⭐\n"
                "Vos futurs clients lisent surtout votre réponse : c'est elle qui montre votre sérieux.",
     "alt": "Le conseil DIG16 : répondre à un avis négatif, calmement et poliment."},
    {"id": "p09", "date": "2026-11-06T18:30:00", "theme": "sombre", "etiquette": "Comment je travaille",
     "metricool": 392400850, "titre_tiktok": "Après 6 mois, sans engagement",
     "images": [
         ("cover", "Après 6 mois, *sans engagement.*", "Vous restez parce que vous êtes content."),
         ("point", "1", "Vous arrêtez *par simple email.*", "À tout moment, avec effet à la fin du mois en cours."),
         ("point", "2", "Vous repartez *avec tous vos fichiers.*", "Et le nom de domaine reste à votre nom."),
         APPEL],
     "legende": "Après 6 mois, votre site DIG16 est sans engagement : vous pouvez arrêter à tout moment, par simple email.\n"
                "Et vous repartez avec tous les fichiers de votre site.",
     "alt": "Après 6 mois, sans engagement : arrêt par simple email, et vous repartez avec vos fichiers."},
    {"id": "p10", "date": "2026-11-09T18:30:00", "theme": "clair", "etiquette": "Comment je travaille",
     "metricool": 392400865, "titre_tiktok": "Votre site, sans rien gérer",
     "images": [
         ("cover", "Votre site, *sans rien gérer.*", "Comment ça se passe ?"),
         ("point", "", "Étape 1 : *20 minutes ensemble.*", "Pour vos textes et vos photos."),
         ("point", "", "Étape 2 : *je construis, vous relisez.*", "Vous suivez votre site avant qu'il soit en ligne."),
         ("point", "", "Étape 3 : *votre site est en ligne.*", "Après votre accord écrit."),
         APPEL],
     # 24/10 : plus aucun délai de création annoncé (demande de l'utilisateur) ; on met en avant la disponibilité.
     "legende": "Votre site, sans rien gérer : comment ça se passe ? 🛠️\n"
                "Étape 1 : 20 minutes ensemble pour vos textes et vos photos.\nÉtape 2 : je construis, vous relisez.\n"
                "Étape 3 : votre site est mis en ligne après votre accord.\nUne question ? Je suis joignable 7 jours sur 7.",
     "alt": "Comment ça se passe : étape 1, 20 minutes ensemble ; étape 2, je construis et vous relisez ; étape 3, en ligne après votre accord."},
    {"id": "p11", "date": "2026-11-11T18:30:00", "theme": "sombre", "etiquette": "Le conseil", "metricool": 392400879,
     "titre_tiktok": "Vos horaires, les mêmes partout ?",
     "images": [
         ("cover", "Vos horaires, *les mêmes partout ?*", "Un client devant une porte close ne revient pas toujours."),
         ("liste", "À vérifier aujourd'hui", ["Votre site", "Votre fiche Google", "Votre page Facebook",
                                               "Vos annuaires"]),
         ("point", "", "Le nom, l'adresse, le téléphone : *exactement les mêmes.*",
          "Les différences brouillent aussi les moteurs de recherche."),
         APPEL],
     "legende": "Vos horaires sont-ils les mêmes sur votre site, votre fiche Google et votre page Facebook ? 🕘\n"
                "Un client qui trouve porte close à cause d'un horaire erroné ne revient pas toujours.",
     "alt": "Le conseil DIG16 : vérifier que ses horaires sont les mêmes sur le site, la fiche Google et Facebook."},
    {"id": "p12", "date": "2026-11-13T18:30:00", "theme": "clair", "etiquette": "Comment je travaille",
     "metricool": 392400906, "titre_tiktok": "Un site suivi, chaque mois",
     "images": [
         ("cover", "Un site suivi, *chaque mois.*", "Pas abandonné après sa mise en ligne."),
         ("point", "1", "Vos changements *en 3 jours ouvrés.*", "Un horaire, une photo, un prix : un email suffit."),
         ("point", "2", "Un bilan rapide *chaque mois.*", "Pour savoir combien de personnes vous ont trouvé."),
         APPEL],
     "legende": "Avec DIG16, votre site n'est pas abandonné après sa mise en ligne 🔧\n"
                "Chaque mois : vos changements faits en 3 jours ouvrés, et un bilan rapide pour savoir combien de personnes "
                "vous ont trouvé.",
     "alt": "Un site suivi : changements en 3 jours ouvrés et bilan rapide chaque mois."},
    {"id": "p13", "date": "2026-11-16T18:30:00", "theme": "sombre", "etiquette": "Le conseil", "metricool": 392400921,
     "titre_tiktok": "Votre site s'affiche-t-il vite ?",
     "images": [
         ("phone", "Votre site s'affiche-t-il *vite sur un téléphone ?*", ESSENTIEL, "Démonstration · entreprise fictive"),
         ("point", "1", "Au-delà de quelques secondes, *beaucoup repartent.*", "Et vont voir ailleurs."),
         ("point", "2", "Visez *moins de deux secondes.*", "Texte lisible sans zoomer, photos qui ne débordent pas."),
         APPEL],
     "legende": "Combien de temps met votre site à s'afficher sur un téléphone ? 📱\n"
                "Au-delà de quelques secondes, beaucoup de visiteurs repartent. Les sites DIG16 sont construits pour être rapides.",
     "alt": "Le conseil DIG16 : un site doit s'afficher vite sur un téléphone."},
    {"id": "p14", "date": "2026-11-18T18:30:00", "theme": "clair", "etiquette": "Le conseil", "metricool": 392400938,
     "titre_tiktok": "Votre métier en 3 phrases",
     "images": [
         ("cover", "Votre métier *en 3 phrases.*", "Pour votre site, votre fiche Google, vos réseaux."),
         ("point", "1", "Ce que *vous faites.*", "Votre métier, en mots simples."),
         ("point", "2", "Où *vous intervenez.*", "Votre ville et votre secteur."),
         ("point", "3", "Ce qui *vous distingue.*", "Sur mesure, savoir-faire, délais : le vrai, pas le slogan."),
         ("citation", "« Menuisier en Charente, je fabrique et pose fenêtres et escaliers sur mesure. »", "Un exemple"),
         APPEL],
     "legende": "Une bonne description de votre entreprise tient en 3 phrases ✍️\n"
                "Ce que vous faites, où vous intervenez, et ce qui vous distingue.\n"
                "Exemple : « Menuisier en Charente, je fabrique et pose fenêtres et escaliers sur mesure. »",
     "alt": "Le conseil DIG16 : décrire son métier en 3 phrases, avec un exemple."},
    {"id": "p15", "date": "2026-11-20T18:30:00", "theme": "sombre", "etiquette": "Recommandation", "metricool": 392400957,
     "titre_tiktok": "Recommandez un artisan, un mois offert",
     "images": [
         ("cover", "Recommandez un artisan, *un mois offert.*", "Vous connaissez quelqu'un qui a besoin d'un site ?"),
         ("point", "1", "S'il devient client, *votre prochain mois est offert.*", "Conditions sur dig16.fr."),
         ("point", "2", "Et son premier mois *aussi.*", "Tout le monde y gagne."),
         APPEL],
     "legende": "Vous connaissez un artisan ou un commerçant qui a besoin d'un site ? 🤝\n"
                "Recommandez-le : s'il devient client, votre prochain mois est offert, et son premier mois aussi.",
     "alt": "Recommandez un artisan : un mois offert pour vous, et son premier mois offert aussi."},
    {"id": "p16", "date": "2026-11-25T18:30:00", "theme": "clair", "etiquette": "Le conseil", "metricool": 392400988,
     "titre_tiktok": "Un site lent ? Regardez vos photos.",
     "images": [
         ("cover", "Un site lent ? *Regardez vos photos.*", "C'est souvent là que tout se joue."),
         ("point", "1", "Une photo de plusieurs mégaoctets…", "…peut presque toujours être allégée fortement, sans perte visible."),
         ("point", "2", "Allégez-les *avant de les mettre en ligne.*", "Votre site s'ouvre plus vite sur un téléphone."),
         APPEL],
     "legende": "Un site lent, ce sont souvent des photos trop lourdes 🐢\n"
                "Une photo de plusieurs mégaoctets peut presque toujours être allégée fortement sans perte visible.",
     "alt": "Le conseil DIG16 : un site lent vient souvent de photos trop lourdes."},
    {"id": "p17", "date": "2026-11-27T18:30:00", "theme": "sombre", "etiquette": "Vos questions", "metricool": 392400998,
     "titre_tiktok": "Les questions qu'on me pose le plus",
     "images": [
         ("cover", "Les questions *qu'on me pose le plus.*", "Et les réponses, sans détour."),
         ("qr", "Je dois écrire les textes ?", "Non : je les rédige avec vous."),
         ("qr", "Je peux modifier mon site ?", "Oui : envoyez-moi un email, c'est fait en 3 jours ouvrés."),
         ("qr", "Et si j'arrête ?", "Vous gardez votre nom de domaine et vos fichiers."),
         APPEL],
     "legende": "Les questions qu'on me pose le plus 💬\n"
                "« Je dois écrire les textes ? » Non, je les rédige avec vous.\n"
                "« Je peux modifier mon site ? » Oui, envoyez-moi un email, c'est fait en 3 jours ouvrés.\n"
                "« Et si j'arrête ? » Vous gardez votre nom de domaine et vos fichiers.",
     "alt": "Les 3 questions les plus posées à DIG16, avec leurs réponses."},
    {"id": "p18", "date": "2026-12-02T18:30:00", "theme": "clair", "etiquette": "Le conseil", "metricool": 392401018,
     "titre_tiktok": "Préparez votre saison dès maintenant",
     "images": [
         ("cover", "Préparez votre saison *dès maintenant.*", "Trois choses à mettre à jour."),
         ("liste", "Sur votre site", ["Vos horaires", "Des photos récentes", "Vos offres du moment"]),
         ("point", "", "Un site à jour, *ce sont des appels en plus.*", "Et des clients qui trouvent porte ouverte."),
         APPEL],
     "legende": "Préparez votre saison maintenant 📅\n"
                "Horaires, photos récentes, offres du moment : un site à jour, ce sont des appels en plus.",
     "alt": "Le conseil DIG16 : préparer sa saison en mettant à jour horaires, photos et offres."},
    {"id": "p19", "date": "2026-12-04T18:30:00", "theme": "sombre", "etiquette": "L'offre découverte",
     "metricool": 392401054, "titre_tiktok": "Votre page d'accueil refaite gratuitement",
     "images": [
         ("phone", "Votre page d'accueil, *refaite gratuitement.*", VISITE, "Démonstration · entreprise fictive"),
         ("point", "", "Pour voir *avant de décider.*", "Aucune obligation d'achat."),
         ("prix",),
         APPEL],
     "legende": "Votre page d'accueil refaite gratuitement, pour voir avant de décider 🎁\n"
                "Aucune obligation. Écrivez-moi ou appelez.",
     "alt": "L'offre découverte DIG16 : votre page d'accueil refaite gratuitement, sans obligation."},
]


def data(chemin, type_mime):
    with open(chemin, "rb") as f:
        return f"data:{type_mime};base64,{base64.b64encode(f.read()).decode()}"


def css_polices():
    css = open(os.path.join(POLICES, "instrumentserif-geist-geistmono.css"), encoding="utf-8").read()
    return re.sub(r"url\(/moteur/polices/([^)]+)\)",
                  lambda m: f"url({data(os.path.join(POLICES, m.group(1)), 'font/woff2')})", css)


def insecables(t):
    """Typographie française : apostrophe courbe, espace insécable avant « : ; ? ! »."""
    return re.sub(r" ([:;?!»])", " \\1", t.replace("'", "’")).replace("« ", "« ")


def dores(t):
    """Mots dorés entre astérisques ; les mots à trait d'union ne sont jamais coupés (« demandez-le »)."""
    t = re.sub(r"(\w+(?:-\w+)+)", r'<span class="nw">\1</span>', insecables(t))
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)


def capture(nom):
    return data(os.path.join(SITE, "img", nom), "image/webp")


def telephone(nom, classe=""):
    return f'<div class="tel {classe}"><img src="{capture(nom)}" alt=""></div>'


AVANT = """<div class="tel avant"><div class="vieux">
<div class="v-bandeau">MENUISERIE EXEMPLE - Bienvenue sur notre site internet</div>
<div class="v-menu"><u>Accueil</u> | <u>Société</u> | <u>Nos produits</u> | <u>Galerie</u> | <u>Plan d'accès</u> | <u>Contact</u></div>
<div class="v-photo"></div>
<p>Bienvenue sur le site de notre entreprise. Nous sommes une entreprise familiale de menuiserie qui intervient dans
toute la région pour tous vos travaux de menuiserie intérieure et extérieure, neuf et rénovation, pour les particuliers
et les professionnels. N'hésitez pas à nous contacter pour tout renseignement complémentaire ou pour un devis.</p>
<p>Nos coordonnées sont disponibles dans la rubrique contact de ce site. Horaires : voir page contact.</p>
<div class="v-pied">Site optimisé pour un écran 1024 x 768 - Dernière mise à jour du site</div></div></div>"""


def contenu(image, theme):
    genre = image[0]
    if genre == "cover":
        return f'<div class="corps bas"><h1>{dores(image[1])}</h1><p class="sous">{insecables(image[2])}</p></div>'
    if genre == "point":
        num = f'<div class="num">{image[1]}</div>' if image[1] else '<div class="filet"></div>'
        return f'<div class="corps bas">{num}<h2>{dores(image[2])}</h2><p class="sous">{insecables(image[3])}</p></div>'
    if genre == "liste":
        items = "".join(f"<li><span>{i + 1:02d}</span>{insecables(x)}</li>" for i, x in enumerate(image[2]))
        return f'<div class="corps bas"><div class="etq2">{insecables(image[1])}</div><ul class="liste">{items}</ul></div>'
    if genre == "qr":
        return (f'<div class="corps bas"><div class="q">{insecables("« " + image[1] + " »")}</div>'
                f'<h2>{dores(image[2])}</h2></div>')
    if genre == "citation":
        return (f'<div class="corps bas"><div class="etq2">{insecables(image[2])}</div>'
                f'<blockquote>{insecables(image[1])}</blockquote></div>')
    if genre == "phone":
        return (f'<div class="haut"><h2 class="petit">{dores(image[1])}</h2></div>{telephone(image[2], "seul")}'
                f'<p class="legende">{insecables(image[3])}</p>')
    if genre == "phones":
        tels = "".join(telephone(n, f"t{i}") for i, n in enumerate(image[2]))
        return (f'<div class="haut"><h2 class="petit">{dores(image[1])}</h2></div><div class="trio">{tels}</div>'
                f'<p class="legende">{insecables(image[3])}</p>')
    if genre == "avantapres":
        return (f'<div class="haut"><h2 class="petit">{dores(image[1])}</h2></div>'
                f'<div class="duo"><figure>{AVANT}<figcaption>Avant</figcaption></figure>'
                f'<figure>{telephone(ESSENTIEL)}<figcaption class="or">Après</figcaption></figure></div>'
                f'<p class="legende">Exemple fictif</p>')
    if genre == "prix":
        return ('<div class="corps bas"><div class="gros">0 €</div><h2>de création, <em>puis dès 49 € par mois.</em></h2>'
                '<ul class="coches"><li>Hébergement compris</li><li>Modifications comprises</li><li>Suivi compris</li></ul>'
                '</div>')
    if genre == "formules":
        lignes = [("Essentiel", "49 €", "par mois"), ("Visibilité", "79 €", "par mois"),
                  ("Achat", "690 €", "une fois, puis 15 € par mois pour l'hébergement et le suivi")]
        rangs = "".join(f'<div class="formule"><b>{a}</b><span class="m">{b}</span><span>{insecables(c)}</span></div>'
                        for a, b, c in lignes)
        return (f'<div class="corps bas"><div class="etq2">Les formules</div>{rangs}'
                f'<p class="sous">0 € de création sur les formules mensuelles.</p></div>')
    if genre == "cta":
        return (f'<div class="corps bas"><h2>{dores(image[1])}</h2><p class="sous">{insecables(image[2])}</p>'
                f'<div class="site">dig16.fr</div><p class="mini">Sites internet pour artisans et commerçants de Charente'
                f' · dès 49 € par mois</p></div>')
    raise ValueError(genre)


def page(pub, n, total, story=False):
    image = pub["images"][n]
    theme = pub["theme"]
    clair = theme == "clair"
    fond, texte, second, accent, ligne = (("#f3eee5", "#1a1814", "#655e54", "#7a5a2c", "rgba(26,24,20,.16)") if clair
                                          else ("#0f0e0c", "#efe9df", "#a8a093", "#c8a46e", "rgba(239,233,223,.16)"))
    signature = data(os.path.join(SITE, "img", "marque",
                                  "signature-encre-transparent@2x.png" if clair else "signature-ivoire@2x.png"), "image/png")
    deco = (f'<div class="deco">{empreinte_svg(440, couleur=accent, opacite=1.0, ident="d")}</div>'
            if image[0] == 'cover' and len(image[1].replace('*', '')) <= 33 else '')  # titre long : pas de décor
    compte = ('<span class="or">Nouveau sur le fil</span>' if story else
              f'<span class="or">Faites glisser →</span>&nbsp;&nbsp;{n + 1} / {total}' if n == 0 and total > 1
              else f'{n + 1} / {total}' if total > 1 else '')
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css_polices()}</style><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;background:{fond};color:{texte};
 font-family:Geist,'Geist Fallback',sans-serif;
 background-image:radial-gradient(70% 45% at 100% 0%,{'rgba(122,90,44,.10)' if clair else 'rgba(200,164,110,.16)'},transparent 70%),
 radial-gradient(60% 40% at 0% 100%,{'rgba(122,90,44,.06)' if clair else 'rgba(200,164,110,.08)'},transparent 70%)}}
em{{font-style:italic;color:{accent}}}
.nw{{white-space:nowrap}}
.entete{{position:absolute;left:{MARGE}px;right:{MARGE}px;top:70px;display:flex;align-items:center;justify-content:space-between;
 padding-bottom:26px;border-bottom:2px solid {ligne}}}
.entete img{{height:58px}}
.etq{{font:500 24px 'Geist Mono','Geist Mono Fallback',monospace;letter-spacing:.18em;text-transform:uppercase;color:{second}}}
.pied{{position:absolute;left:{MARGE}px;right:{MARGE}px;bottom:62px;display:flex;justify-content:space-between;align-items:center;
 font:500 26px Geist,'Geist Fallback',sans-serif;color:{second}}}
.pied b{{color:{texte};font-weight:600;letter-spacing:.01em}}
.pied .or{{color:{accent}}}
.deco{{position:absolute;right:-120px;top:140px;width:440px;opacity:{.35 if clair else .5};pointer-events:none}}
.deco svg{{width:100%;height:auto}}
.corps{{position:absolute;left:{MARGE}px;right:{MARGE}px}}
.bas{{bottom:210px}}
h1{{font:400 132px/0.98 'Instrument Serif','Instrument Serif Fallback',serif;letter-spacing:-.015em}}
h2{{font:400 92px/1.02 'Instrument Serif','Instrument Serif Fallback',serif;letter-spacing:-.01em}}
h2.petit{{font-size:76px}}
.sous{{margin-top:34px;font:400 36px/1.4 Geist,'Geist Fallback',sans-serif;color:{second};max-width:860px}}
.num{{font:400 200px/0.9 'Instrument Serif','Instrument Serif Fallback',serif;color:{accent};margin-bottom:30px}}
.filet{{width:120px;height:3px;background:{accent};margin-bottom:46px}}
.etq2{{font:500 26px 'Geist Mono','Geist Mono Fallback',monospace;letter-spacing:.18em;text-transform:uppercase;color:{accent};
 margin-bottom:40px}}
.liste{{list-style:none}}
.liste li{{display:flex;align-items:baseline;gap:34px;padding:30px 0;border-top:2px solid {ligne};
 font:400 64px/1.1 'Instrument Serif','Instrument Serif Fallback',serif}}
.liste li span{{font:500 28px 'Geist Mono','Geist Mono Fallback',monospace;color:{accent};min-width:52px}}
.q{{font:400 44px/1.3 Geist,'Geist Fallback',sans-serif;color:{second};margin-bottom:36px}}
blockquote{{font:400 italic 78px/1.12 'Instrument Serif','Instrument Serif Fallback',serif;color:{texte}}}
.haut{{position:absolute;left:{MARGE}px;right:{MARGE}px;top:200px}}
.tel{{position:absolute;width:390px;height:844px;border-radius:58px;padding:14px;background:#0b0a09;
 box-shadow:0 0 0 2px {'rgba(26,24,20,.25)' if clair else 'rgba(200,164,110,.35)'},0 40px 90px rgba(0,0,0,{.25 if clair else .6})}}
.tel img{{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:46px;display:block}}
.tel.seul{{left:355px;top:410px;width:370px;height:700px}}
.trio .tel{{top:440px;height:620px;width:300px}}
.trio .t0{{left:110px;transform:rotate(-6deg)}}
.trio .t1{{left:390px;top:415px;z-index:2}}
.trio .t2{{left:670px;transform:rotate(6deg)}}
.legende{{position:absolute;left:{MARGE}px;right:{MARGE}px;bottom:150px;text-align:center;
 font:500 24px 'Geist Mono','Geist Mono Fallback',monospace;letter-spacing:.14em;text-transform:uppercase;color:{second}}}
.duo{{position:absolute;left:{MARGE}px;right:{MARGE}px;top:400px;height:690px}}
.duo figure{{position:absolute;top:0;width:350px;height:690px}}
.duo figure:first-child{{left:40px}}.duo figure:last-child{{right:40px}}
.duo .tel{{position:relative;height:630px;width:350px}}
.duo figcaption{{position:absolute;left:0;right:0;bottom:0;text-align:center;
 font:500 24px 'Geist Mono','Geist Mono Fallback',monospace;letter-spacing:.18em;text-transform:uppercase;color:{second}}}
.duo figcaption.or{{color:{accent}}}
.vieux{{width:100%;height:100%;border-radius:46px;overflow:hidden;background:#fff;color:#222;font:11px/1.35 'Times New Roman',serif;
 padding:30px 12px 12px;filter:saturate(.7)}}
.v-bandeau{{background:#3a5f8f;color:#fff;font:bold 12px Arial,sans-serif;padding:8px 6px;text-align:center}}
.v-menu{{font:10px Arial,sans-serif;color:#1a0dab;padding:6px 2px;text-align:center}}
.v-photo{{height:160px;margin:8px 0;background:linear-gradient(135deg,#9b9286,#6f675d);opacity:.7}}
.vieux p{{margin:8px 2px;text-align:justify}}
.v-pied{{margin-top:40px;font:9px Arial,sans-serif;color:#777;text-align:center;border-top:1px solid #ccc;padding-top:6px}}
.gros{{font:400 260px/0.85 'Instrument Serif','Instrument Serif Fallback',serif;color:{accent};margin-bottom:20px}}
.coches{{list-style:none;margin-top:44px}}
.coches li{{font:400 38px/1.3 Geist,'Geist Fallback',sans-serif;padding:16px 0;border-top:2px solid {ligne}}}
.coches li::before{{content:"✓";color:{accent};margin-right:22px;font-weight:600}}
.formule{{display:grid;grid-template-columns:300px 210px 1fr;align-items:baseline;gap:20px;padding:30px 0;
 border-top:2px solid {ligne};font:400 34px/1.25 Geist,'Geist Fallback',sans-serif;color:{second}}}
.formule b{{font:400 60px 'Instrument Serif','Instrument Serif Fallback',serif;color:{texte}}}
.formule .m{{font:400 60px 'Instrument Serif','Instrument Serif Fallback',serif;color:{accent}}}
.site{{margin-top:56px;display:inline-block;padding:26px 54px;border-radius:999px;background:{'#1a1814' if clair else '#c8a46e'};
 color:{'#f3eee5' if clair else '#14110d'};font:600 52px Geist,'Geist Fallback',sans-serif;letter-spacing:.01em}}
.mini{{margin-top:30px;font:400 26px Geist,'Geist Fallback',sans-serif;color:{second}}}
{'html{height:1920px} body{margin-top:285px}' if story else ''}
</style></head><body>
{deco}
<div class="entete"><img src="{signature}" alt=""><div class="etq">{insecables(pub['etiquette'])}</div></div>
{contenu(image, theme)}
<div class="pied"><b>dig16.fr</b><span>{compte}</span></div>
</body></html>"""


CONTROLE = """() => {
  const souci = [];
  const W = 1080, H = 1350, M = 60;
  for (const el of document.querySelectorAll('h1,h2,p,li,div,span,b,blockquote,figcaption')) {
    if (!el.childElementCount && el.textContent.trim()) {
      const r = el.getBoundingClientRect();
      if (r.left < M - 1 || r.right > W - M + 1 || r.top < 40 || r.bottom > H - 40) souci.push('hors marge : ' + el.textContent.slice(0, 40));
      if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow !== 'visible') souci.push('débordement : ' + el.textContent.slice(0, 40));
    }
  }
  const corps = document.querySelector('.corps'), entete = document.querySelector('.entete');
  if (corps && corps.getBoundingClientRect().top < entete.getBoundingClientRect().bottom + 20) souci.push('texte sous l\\'en-tête');
  const dc = document.querySelector('.deco svg');
  if (dc) { const d = dc.getBoundingClientRect();
    for (const el of document.querySelectorAll('.corps h1, .corps h2, .corps p')) { const q = el.getBoundingClientRect();
      if (q.bottom > d.top && q.top < d.bottom && q.right > d.left && q.left < d.right) souci.push('décor sous le texte'); } }
  const lg = document.querySelector('.legende');
  if (lg) { const r = lg.getBoundingClientRect();
    for (const tl of document.querySelectorAll('.tel, .duo figcaption')) { const q = tl.getBoundingClientRect();
      if (q.bottom > r.top && q.top < r.bottom && q.right > r.left && q.left < r.right) souci.push('légende chevauche un téléphone'); } }
  const hb = document.querySelector('.haut');
  if (hb) for (const tl of document.querySelectorAll('.tel')) if (tl.getBoundingClientRect().top < hb.getBoundingClientRect().bottom + 10) souci.push('téléphone sous le titre');
  for (const im of document.images) if (!im.complete || !im.naturalWidth) souci.push('image non chargée');
  const t = document.body.innerText;
  if (/0[1-9]( ?\\d\\d){4}/.test(t) || t.includes('@')) souci.push('coordonnées sur l\\'image');
  return souci;
}"""


def main():
    choix = set(sys.argv[1:])
    os.makedirs(SORTIE, exist_ok=True)
    os.makedirs(SUPPORTS, exist_ok=True)
    alertes, sortie = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for pub in SERIE:
            total = len(pub["images"])
            fichiers = []
            for n in range(total):
                nom = f"{pub['id']}-{n + 1}.jpg"
                fichiers.append(URL + nom)
                if choix and pub["id"] not in choix:
                    continue
                pg.set_content(page(pub, n, total), wait_until="load")
                # Une police n'est chargée que si la page s'en sert : on demande explicitement chaque graisse utilisée.
                charge = pg.evaluate("""async () => (await Promise.all(['400 40px "Instrument Serif"',
                    'italic 400 40px "Instrument Serif"', '400 40px Geist', '500 40px Geist', '600 40px Geist',
                    '500 40px "Geist Mono"'].map(f => document.fonts.load(f)))).every(l => l.length > 0)""")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(150)
                if not charge:
                    alertes.append(f"{nom} : polices non chargées")
                for s in pg.evaluate(CONTROLE):
                    alertes.append(f"{nom} : {s}")
                png = os.path.join(SUPPORTS, "_tmp.png")
                pg.screenshot(path=png)
                Image.open(png).convert("RGB").save(os.path.join(SORTIE, nom), "JPEG", quality=90, optimize=True,
                                                    progressive=True)
            if not choix or pub["id"] in choix:
                # Story 1080 × 1920 : la couverture dans la zone sûre (285 px libres en haut et en bas), fond continu.
                pg.set_viewport_size({"width": 1080, "height": 1920})
                pg.set_content(page(pub, 0, total, story=True), wait_until="load")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(150)
                png = os.path.join(SUPPORTS, "_tmp.png")
                pg.screenshot(path=png)
                Image.open(png).convert("RGB").save(os.path.join(SORTIE, f"{pub['id']}-story.jpg"), "JPEG", quality=90,
                                                    optimize=True, progressive=True)
                pg.set_viewport_size({"width": 1080, "height": 1350})
            sortie.append({k: pub[k] for k in ("id", "date", "theme", "etiquette", "titre_tiktok", "legende", "alt",
                                               "metricool")} | {"images": fichiers})
        b.close()
    if os.path.exists(os.path.join(SUPPORTS, "_tmp.png")):
        os.remove(os.path.join(SUPPORTS, "_tmp.png"))
    with open(os.path.join(SUPPORTS, "series.json"), "w", encoding="utf-8") as f:
        json.dump(sortie, f, ensure_ascii=False, indent=1)
    # Planche de contrôle : la couverture de chaque publication, dans l'ordre du fil.
    vignettes = [Image.open(os.path.join(SORTIE, f"{pub['id']}-1.jpg")) for pub in SERIE
                 if os.path.exists(os.path.join(SORTIE, f"{pub['id']}-1.jpg"))]
    if vignettes:
        w, h = 270, 338
        planche = Image.new("RGB", (w * 5, h * ((len(vignettes) + 4) // 5)), "white")
        for i, v in enumerate(vignettes):
            planche.paste(v.resize((w, h)), ((i % 5) * w, (i // 5) * h))
        planche.save(os.path.join(SUPPORTS, "planche.jpg"), quality=85)
    for a in alertes:
        print("ALERTE", a)
    print(f"{sum(len(p['images']) for p in SERIE)} images prévues ; {len(alertes)} alerte(s).")
    sys.exit(1 if alertes else 0)


if __name__ == "__main__":
    main()
