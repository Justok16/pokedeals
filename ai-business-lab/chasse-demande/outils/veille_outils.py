#!/usr/bin/env python3
"""Veille des outils retenus et des nouveaux outils officiels (28/10/2026).

Demande de l'utilisateur du 28/10 : « garder absolument TOUS les outils à jour, fiables et légitimes […] surveiller
l'arrivée de nouveaux outils gratuits […] que TOUT soit irréprochable et mis à jour au fur et à mesure ».

Lit `connaissances/inventaire-outils.json` et, pour chaque outil :
- nouvelle version (registres npm, PyPI, proxy Go), étoiles et licence (API publique deps.dev, Google) ;
- ALERTE si la licence change (un outil libre peut devenir payant), si la dernière version a plus de 6 mois
  (projet peut-être abandonné) ou si l'outil devient introuvable.
Puis lit les catalogues officiels (`sources_officielles`) et signale chaque extension ou skill **nouveau**.
État gardé dans `veille/etat/outils.json` ; rapport ajouté à `veille/AAAA-MM-JJ.md` ; tableau régénéré dans
`connaissances/inventaire-outils.md`.

    python3 outils/veille_outils.py          # veille complète (réseau)
    python3 outils/veille_outils.py --eval   # jeu d'essai hors réseau (à rejouer après chaque modification)
"""
import argparse
import datetime
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
INVENTAIRE = os.path.join(RACINE, "connaissances", "inventaire-outils.json")
TABLEAU = os.path.join(RACINE, "connaissances", "inventaire-outils.md")
ETAT = os.path.join(RACINE, "veille", "etat", "outils.json")
VEILLE = os.path.join(RACINE, "veille")
SIX_MOIS = 183


def lire_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "veille-dig16"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.load(r)
    except Exception as e:  # noqa: BLE001 (réseau ou format : on note l'échec, la veille continue)
        return {"_erreur": str(e)[:80]}


def interroger(o):
    """Version, date, étoiles et licence d'un outil (None si l'information n'existe pas)."""
    info = {"version": None, "date": None, "etoiles": None, "licence": None}
    if o.get("depot"):
        p = lire_json("https://api.deps.dev/v3/projects/" + urllib.parse.quote("github.com/" + o["depot"], safe=""))
        info["etoiles"] = p.get("starsCount")
        info["licence"] = p.get("license") or None
    reg, pkg = o.get("registre"), o.get("paquet")
    if reg == "npm":
        n = lire_json("https://registry.npmjs.org/" + urllib.parse.quote(pkg, safe="@"))
        if "_erreur" in n:
            info["introuvable"] = True
        else:
            info["version"] = n.get("dist-tags", {}).get("latest")
            info["date"] = (n.get("time", {}).get(info["version"] or "", "") or "")[:10] or None
            info["licence"] = info["licence"] or (n.get("license") if isinstance(n.get("license"), str) else None)
    elif reg == "pypi":
        n = lire_json(f"https://pypi.org/pypi/{pkg}/json")
        if "_erreur" in n:
            info["introuvable"] = True
        else:
            info["version"] = n.get("info", {}).get("version")
            fichiers = n.get("urls") or []
            info["date"] = fichiers[0]["upload_time"][:10] if fichiers else None
    elif reg == "go":
        n = lire_json(f"https://proxy.golang.org/{pkg.lower()}/@latest")
        if "_erreur" in n:
            info["introuvable"] = True
        else:
            info["version"], info["date"] = n.get("Version"), (n.get("Time") or "")[:10] or None
    return info


def comparer(nom, avant, apres, aujourdhui, reference=False):
    """Lignes de rapport pour un outil : ALERTE (à traiter) ou INFO (mise à jour normale).
    Ancienneté : signalée une seule fois (champ « ancien ») ; une référence stable (GSAP, Gitleaks…) n'est signalée
    qu'après 18 mois sans version, les autres après 6 mois (règle du prompt : « sauf s'il reste la référence »)."""
    lignes = []
    if apres.get("introuvable"):
        lignes.append(f"ALERTE {nom} : paquet introuvable dans son registre (retiré, renommé ou panne)")
    if avant and avant.get("licence") and apres.get("licence") and avant["licence"] != apres["licence"]:
        lignes.append(f"ALERTE {nom} : licence changée {avant['licence']} → {apres['licence']} (relire la gratuité)")
    if apres.get("date"):
        age = (aujourdhui - datetime.date.fromisoformat(apres["date"])).days
        limite = 3 * SIX_MOIS if reference else SIX_MOIS
        if age > limite:
            apres["ancien"] = True
            if not (avant or {}).get("ancien"):
                lignes.append(f"ALERTE {nom} : dernière version du {apres['date']} (plus de {limite // 30} mois, "
                              "vérifier que le projet vit encore, sinon chercher une alternative active)")
    if avant and apres.get("version") and avant.get("version") and avant["version"] != apres["version"]:
        lignes.append(f"INFO {nom} : nouvelle version {avant['version']} → {apres['version']} ({apres.get('date')})")
    return lignes


def nouveautes_catalogue(src, avant):
    """Noms d'extensions apparues dans un catalogue officiel depuis la dernière veille."""
    d = lire_json(src["url"])
    if "_erreur" in d:
        return None, [f"ALERTE catalogue {src['nom']} illisible ({d['_erreur']})"]
    noms = sorted({p.get("name") for p in d.get("plugins", []) if p.get("name")})
    connus = set(avant or [])
    lignes = [f"NOUVEAU {src['nom']} : {n} (lire à la source, vérifier gratuité et licence, puis trier selon 46)"
              for n in noms if avant is not None and n not in connus]
    return noms, lignes


def texte_page(url):
    """Texte lisible d'une page de prix (scripts et balises retirés), ou None si la page ne répond pas."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            brut = r.read().decode("utf-8", errors="ignore")
    except Exception:  # noqa: BLE001 (page injoignable : signalé en INFO, la veille continue)
        return None
    brut = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", brut, flags=re.DOTALL)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", brut)))


def controler_offre(service, texte):
    """28/10 : une offre gratuite peut changer sans prévenir. ALERTE si une phrase repère a disparu de la page de prix."""
    if not texte or len(texte) < 500:
        return [f"INFO {service['nom']} : page de prix illisible aujourd'hui ({service['url']}), à relire à la main si cela dure"]
    manquent = [p for p in service["doit_contenir"] if p not in texte]
    return [f"ALERTE {service['nom']} : la page de prix ne dit plus « {m} » ({service['url']}) : relire l'offre gratuite"
            for m in manquent]


def ecrire_tableau(inv, etat):
    lignes = ["# Inventaire des outils DIG16 (tenu à jour automatiquement)", "",
              ("Fichier régénéré par `outils/veille_outils.py` à chaque veille, depuis `inventaire-outils.json` "
              "(demande de l'utilisateur du 28/10 : garder tous les outils fiables à portée et à jour). "
              "Statut : **en place** (utilisé), **installé** (prêt dans Claude), **réserve** (vérifié, à sortir au "
              "bon moment, voir `reserve-prete.md`)."), "",
              "| Domaine | Outil | Statut | Usage | Version (date) | Licence | Étoiles |", "|---|---|---|---|---|---|---|"]
    statuts = {"en_place": "en place", "installe": "installé", "reserve": "réserve"}
    for o in sorted(inv["outils"], key=lambda x: (x["domaine"], x["nom"])):
        e = etat.get("outils", {}).get(o["nom"], {})
        ver = f"{e.get('version')} ({e.get('date')})" if e.get("version") else "—"
        lignes.append(f"| {o['domaine']} | {o['nom']} | {statuts.get(o['statut'], o['statut'])} | {o['usage']} | {ver} | "
                      f"{e.get('licence') or '—'} | {e.get('etoiles') or '—'} |")
    lignes += ["", f"Dernière veille : {etat.get('date', '—')}."]
    with open(TABLEAU, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lignes) + "\n")


def veille():
    with open(INVENTAIRE, encoding="utf-8") as fh:
        inv = json.load(fh)
    try:
        with open(ETAT, encoding="utf-8") as fh:
            etat = json.load(fh)
    except (OSError, ValueError):
        etat = {}
    aujourdhui = datetime.datetime.now(datetime.timezone.utc).date()
    rapport, nouvel = [], {"date": aujourdhui.isoformat(), "outils": {}, "catalogues": {}}
    for o in inv["outils"]:
        apres = interroger(o)
        rapport += comparer(o["nom"], etat.get("outils", {}).get(o["nom"]), apres, aujourdhui, o.get("reference", False))
        nouvel["outils"][o["nom"]] = apres
    for service in inv.get("services_offres_gratuites", []):
        rapport += controler_offre(service, texte_page(service["url"]))
    for src in inv.get("sources_officielles", []):
        noms, lignes = nouveautes_catalogue(src, etat.get("catalogues", {}).get(src["nom"]))
        rapport += lignes
        nouvel["catalogues"][src["nom"]] = noms if noms is not None else etat.get("catalogues", {}).get(src["nom"])
    os.makedirs(os.path.dirname(ETAT), exist_ok=True)
    with open(ETAT, "w", encoding="utf-8") as fh:
        json.dump(nouvel, fh, ensure_ascii=False, indent=1)
    ecrire_tableau(inv, nouvel)
    texte = "\n".join(f"- {l}" for l in rapport) or "- Rien de nouveau : tous les outils suivis sont à jour."
    with open(os.path.join(VEILLE, aujourdhui.isoformat() + ".md"), "a", encoding="utf-8") as fh:
        fh.write(f"\n## Veille des outils DIG16 ({len(inv['outils'])} suivis)\n\n{texte}\n")
    print(texte)
    return 0


def evaluer():
    """Jeu d'essai hors réseau : ce qui doit déclencher une alerte, et ce qui ne doit pas."""
    j = datetime.date(2026, 10, 28)
    cas = [
        ("licence changée", comparer("X", {"licence": "MIT"}, {"licence": "BUSL-1.1", "date": "2026-10-01"}, j), "ALERTE"),
        ("projet ancien", comparer("X", None, {"date": "2025-01-01"}, j), "ALERTE"),
        ("ancien déjà signalé", comparer("X", {"ancien": True, "date": "2025-01-01"}, {"date": "2025-01-01"}, j), None),
        ("référence stable de 7 mois", comparer("X", None, {"date": "2026-03-20"}, j, reference=True), None),
        ("paquet introuvable", comparer("X", None, {"introuvable": True}, j), "ALERTE"),
        ("nouvelle version", comparer("X", {"version": "1.0"}, {"version": "1.1", "date": "2026-10-20"}, j), "INFO"),
        ("rien de neuf", comparer("X", {"version": "1.0", "licence": "MIT"},
                                  {"version": "1.0", "licence": "MIT", "date": "2026-10-20"}, j), None),
        ("premier passage sans historique", comparer("X", None, {"version": "1.0", "date": "2026-10-20"}, j), None),
        ("offre gratuite inchangée", controler_offre({"nom": "S", "url": "u", "doit_contenir": ["100 tasks"]},
                                                      "x" * 600 + " 100 tasks "), None),
        ("offre gratuite modifiée", controler_offre({"nom": "S", "url": "u", "doit_contenir": ["100 tasks"]},
                                                     "x" * 600 + " 50 tasks "), "ALERTE"),
        ("page de prix illisible", controler_offre({"nom": "S", "url": "u", "doit_contenir": ["a"]}, None), "INFO"),
    ]
    echecs = 0
    for nom, lignes, attendu in cas:
        ok = (not lignes) if attendu is None else any(l.startswith(attendu) for l in lignes)
        echecs += not ok
        print(("OK    " if ok else "ÉCHEC ") + nom + " -> " + ("; ".join(lignes) or "rien"))
    print(f"{len(cas) - echecs}/{len(cas)} cas réussis")
    return 1 if echecs else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Veille des outils DIG16")
    ap.add_argument("--eval", action="store_true", help="jeu d'essai hors réseau")
    sys.exit(evaluer() if ap.parse_args().eval else veille())
