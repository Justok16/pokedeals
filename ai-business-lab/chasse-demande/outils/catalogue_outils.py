#!/usr/bin/env python3
"""Boîte à outils DIG16 : catalogue, classé par besoin, de tout ce que l'utilisateur a envoyé (12/10/2026).

Usage : python3 outils/catalogue_outils.py
Lit les registres (46-apprentissage-continu.md, connaissances/technologybrief-sites.md) et réécrit la partie
automatique de connaissances/boite-a-outils.md (entre les deux balises), sans toucher à la partie écrite à la main.
Chaque ligne de registre est rangée dans un domaine (mots-clés) et reçoit un état :
  ✅ en place (installé, appliqué, fait)  ⏳ plus tard ou à vérifier  ⛔ écarté  · noté (simple information).
À lancer après chaque ajout au registre (le point automatique le fait via sync).
"""

import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
SOURCES = ["46-apprentissage-continu.md", "connaissances/technologybrief-sites.md"]
CIBLE = os.path.join(RACINE, "connaissances", "boite-a-outils.md")
DEBUT, FIN = "<!-- catalogue-auto:debut -->", "<!-- catalogue-auto:fin -->"

# domaine : mots-clés (minuscules) ; l'ordre compte, le premier domaine reconnu gagne
DOMAINES = [
    ("Vidéo, voix et montage", ["vidéo de présentation", "montage", "motion", "voix", "clip", "reel", "ffmpeg",
                                "sous-titr", "avatar", "doublage", "flick", "remotion", "hyperframes", "podcast"]),
    ("Images et visuels", ["image", "photo", "visuel", "nano banana", "canva", "logo", "midjourney", "illustration"]),
    ("Création de sites et design", ["site", "design", "démo", "skill", "animation", "interface", "taste", "impeccable",
                                     "police", "landing", "page d'arrivée", "html", "css"]),
    ("Référencement et visibilité", ["seo", "référencement", "fiche google", "geo", "llms.txt", "indexation",
                                     "annuaire", "avis"]),
    ("Prospection et vente", ["prospect", "démarchage", "vente", "client", "cold", "parrainage", "offre", "prix"]),
    ("Gestion, finance et administratif", ["factur", "compta", "pennylane", "indy", "gocardless", "urssaf", "impôt",
                                           "finance", "bourse", "crypto", "budget", "banque"]),
    ("Claude, agents et automatisation", ["claude", "agent", "mcp", "hook", "mod", "automatis", "connecteur",
                                          "plugin", "prompt", "jev", "gemini", "routine", "n8n"]),
]
AUTRE = "Divers"


def etat(texte):
    t = texte.lower()
    if any(m in t for m in ("déjà branché", "déjà installé", "déjà en place", "déjà le cas", "déjà disponible")):
        return "✅"
    if any(m in t for m in ("écarté", "ecarté", "refusé", "non retenu", "abandonné", "pas installé", "non installé", "non utilisé", "exclu", "rien à installer")):
        return "⛔"
    if any(m in t for m in ("installé", "appliqué", "fait", "en place", "branché", "validé", "trié")):
        return "✅"
    if any(m in t for m in ("plus tard", "à vérifier", "a verifier", "à étudier", "à faire", "noté pour", "option")):
        return "⏳"
    return "·"


def domaine(texte):
    # le type d'envoi (reel, vidéo YouTube, carrousel…) ne dit rien du sujet : on l'enlève avant de classer
    t = re.sub(r"(reel|vidéo youtube|vidéo|carrousel|publication) (instagram|facebook|tiktok|youtube|x)?", " ", texte.lower())
    for nom, mots in DOMAINES:
        if any(m in t for m in mots):
            return nom
    return AUTRE


def nettoie(cellule, n=170):
    c = re.sub(r"\*\*|`", "", cellule).strip()
    c = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", c)
    c = re.sub(r"\s+", " ", c)
    return c if len(c) <= n else c[: n - 1].rstrip() + "…"


def lignes():
    vues = set()
    for src in SOURCES:
        chemin = os.path.join(RACINE, src)
        if not os.path.exists(chemin):
            continue
        for brut in open(chemin, encoding="utf-8"):
            if not brut.startswith("| ") or brut.startswith("|---") or set(brut.strip()) <= set("|-: "):
                continue
            cel = [c.strip() for c in brut.strip().strip("|").split("|")]
            if len(cel) < 2 or cel[0] in ("#", "Sujet", "Source", "Vidéo", "Outil", "Envoi", "Appli"):
                continue
            if cel[0].isdigit():  # tableau « À faire » numéroté : action, source, état
                cel = cel[1:]
            quoi, decision = cel[0], cel[-1]
            cle = nettoie(quoi, 80).lower()
            if cle in vues or len(cle) < 4:
                continue
            vues.add(cle)
            tout = " ".join(cel)
            yield domaine(tout), etat(decision), nettoie(quoi, 110), nettoie(decision), src


def main():
    par_dom = {}
    for dom, e, quoi, dec, src in lignes():
        par_dom.setdefault(dom, []).append((e, quoi, dec, src))
    ordre = [d for d, _ in DOMAINES] + [AUTRE]
    out = [DEBUT, "", "## Catalogue complet (généré automatiquement par `outils/catalogue_outils.py`)", "",
           "Légende : ✅ en place · ⏳ plus tard ou à vérifier · ⛔ écarté (raison indiquée) · · simple information.", ""]
    total = 0
    for dom in ordre:
        rangs = par_dom.get(dom)
        if not rangs:
            continue
        rangs.sort(key=lambda r: "✅⏳·⛔".index(r[0]))
        out += [f"### {dom} ({len(rangs)})", "", "| État | Envoi / outil | Décision et usage |", "|---|---|---|"]
        out += [f"| {e} | {q.replace('|', '/')} | {d.replace('|', '/')} |" for e, q, d, _ in rangs]
        out.append("")
        total += len(rangs)
    out += [f"_{total} entrées, registres : {', '.join(SOURCES)}._", "", FIN]
    bloc = "\n".join(out)
    texte = open(CIBLE, encoding="utf-8").read() if os.path.exists(CIBLE) else ""
    if DEBUT in texte and FIN in texte:
        texte = texte.split(DEBUT)[0] + bloc + texte.split(FIN, 1)[1]
    else:
        texte = texte.rstrip() + "\n\n" + bloc + "\n"
    open(CIBLE, "w", encoding="utf-8").write(texte)
    print(f"boite-a-outils.md : {total} entrées")


if __name__ == "__main__":
    main()
