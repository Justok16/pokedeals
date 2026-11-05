#!/usr/bin/env python3
"""Repreneurs récents : entreprises qui viennent d'être rachetées, d'après le BODACC (04/11/2026).

Pourquoi : un artisan ou un commerçant qui reprend une affaire doit refaire tout de suite son site et sa fiche Google
(nouveau dirigeant, parfois nouveau nom). Idée retenue du texte « modèles méconnus » ; 310 000 TPE employeuses à
transmettre d'ici 2030 (livre blanc CMA France, janvier 2026). Décision de l'utilisateur du 04/11/2026 : ajouter les
reprises de moins de 6 mois aux lots d'appels du mardi et du jeudi.

Source : API publique du BODACC (bodacc-datadila.opendatasoft.com, jeu « annonces-commerciales »), famille « Ventes et
cessions », avec un précédent propriétaire (achat d'un fonds). Gratuite, sans clé.
Filtre : secteurs exclus par les consignes de DIG16 (bars, tabac, jeux, armurerie, alcool, santé et pharmacie,
professions réglementées, immobilier, assurance, crédit, CBD).

Usage : python3 repreneurs.py --sortie DOSSIER_PRIVE [--departements 16,86,17] [--mois 6]
Sorties (refusées dans le dépôt : données nominatives) : repreneurs-<date>.json et .md
Ensuite : chaque repreneur retenu est revérifié le jour même (registre, Google, site) comme tout prospect, puis passe
par outils/prospects/fiche_appel.py (champ google_statut obligatoire).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

API = "https://bodacc-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/annonces-commerciales/records"
PARIS = ZoneInfo("Europe/Paris")
EXCLUS = re.compile(
    r"\b(bar|bars|caf[ée]-bar|d[ée]bit de boissons?|licence (iv|4|iii|3)|tabac|presse-tabac|jeux|fran[çc]aise des jeux|"
    r"pmu|casino|armurerie|armes?|vins?|spiritueux|cave|alcools?|bi[èe]re|brasserie artisanale|pharmac\w*|vapot\w*|"
    r"cigarettes? [ée]lectroniques?|m[ée]dico-social|h[ée]bergement social|"
    r"parapharmacie|m[ée]dical|sant[ée]|optique|opticien|audioprothés|infirmi|kin[ée]|dentaire|v[ée]t[ée]rinaire|"
    r"immobili\w*|transactions? immobili|assurances?|courtage|cr[ée]dit|cbd|chanvre|"
    r"notari|avocat|expert-comptable|pompes fun[èe]bres|holding|location de locaux|marchand de biens|discoth[èe]que)\b",
    re.IGNORECASE,
)


def appel(params, essais=10):
    """GET sur l'API du BODACC avec reprises (la connexion est parfois coupée par le proxy du conteneur)."""
    from urllib.parse import urlencode
    url = API + "?" + urlencode(params)
    for i in range(essais):
        r = subprocess.run(["curl", "-s", "-m", "40", url], capture_output=True, text=True, check=False).stdout
        try:
            return json.loads(r)
        except ValueError:
            time.sleep(3 * (i + 1))
    raise RuntimeError("BODACC injoignable après plusieurs essais")


def champ_json(v):
    if not v or v == "None":
        return {}
    if isinstance(v, dict):
        return v
    try:
        return json.loads(v)
    except ValueError:
        return {}


def un_seul(x):
    """Le BODACC renvoie soit un objet, soit une liste d'objets."""
    return x[0] if isinstance(x, list) and x else x if isinstance(x, dict) else {}


def lire_annonce(a):
    """Transforme une annonce BODACC en fiche courte ; None si l'annonce n'est pas un rachat exploitable."""
    etab = un_seul(champ_json(a.get("listeetablissements")).get("etablissement"))
    acte = champ_json(a.get("acte"))
    vente = acte.get("vente") or {}
    activite = (etab.get("activite") or "").strip()
    origine = (etab.get("origineFonds") or "").lower()
    if not activite or not ("achat" in origine or "achat" in (vente.get("categorieVente") or "").lower()):
        return None
    adr = etab.get("adresse") or {}
    adresse = " ".join(str(adr.get(k, "")).strip() for k in ("numeroVoie", "typeVoie", "nomVoie") if adr.get(k))
    sirens = [s for s in (a.get("registre") or []) if re.fullmatch(r"\d{9}", str(s))] if isinstance(
        a.get("registre"), list) else re.findall(r"\b\d{9}\b", str(a.get("registre") or ""))
    acheteur = (a.get("commercant") or "").split(",")[0].strip()
    return {
        "date_parution": a.get("dateparution"),
        "debut_activite": acte.get("dateCommencementActivite"),
        "acheteur": acheteur,
        "siren_acheteur": sirens[0] if sirens else None,
        "activite": activite,
        "adresse": adresse,
        "code_postal": adr.get("codePostal") or a.get("cp"),
        "ville": adr.get("ville") or a.get("ville"),
        "departement": a.get("numerodepartement"),
        "prix_fonds": re.search(r"prix stipul[ée] de ([\d .,]+) ?euros", origine).group(1).strip()
        if re.search(r"prix stipul[ée] de ([\d .,]+) ?euros", origine) else None,
        "annonce": a.get("url_complete"),
        "exclu": bool(EXCLUS.search(activite)),
    }


def chercher(departements, depuis):
    fiches, vus = [], set()
    for dep in departements:
        offset = 0
        while True:
            d = appel({
                "where": f'familleavis="vente" and numerodepartement="{dep}" and listeprecedentproprietaire is not null '
                         f'and dateparution>="{depuis.isoformat()}"',
                "order_by": "dateparution desc", "limit": 100, "offset": offset})
            res = d.get("results") or []
            for a in res:
                f = lire_annonce(a)
                # Un même repreneur publie souvent plusieurs annonces : on garde la plus récente.
                cle = (f or {}).get("siren_acheteur") or ((f or {}).get("acheteur"), (f or {}).get("adresse"))
                if f and cle not in vus:
                    vus.add(cle)
                    fiches.append(f)
            offset += 100
            if len(res) < 100 or offset >= 1000:
                break
    return fiches


def dans_un_depot(chemin):
    p = os.path.realpath(chemin)
    while not os.path.exists(p):
        p = os.path.dirname(p)
    d = p if os.path.isdir(p) else os.path.dirname(p)
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return True
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent


def main(argv):
    ap = argparse.ArgumentParser(description="Repreneurs récents (BODACC), données privées.")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--departements", default="16")
    ap.add_argument("--mois", type=int, default=6)
    try:
        a = ap.parse_args(argv[1:])
    except SystemExit:
        return 2
    if dans_un_depot(a.sortie):
        print("REFUSÉ : sortie dans un dossier git ; les noms des repreneurs sont des données privées.")
        return 2
    aujourd_hui = datetime.now(PARIS).date()
    depuis = aujourd_hui - timedelta(days=31 * a.mois)
    deps = [x.strip() for x in a.departements.split(",") if x.strip()]
    fiches = chercher(deps, depuis)
    retenus = [f for f in fiches if not f["exclu"]]
    os.makedirs(a.sortie, exist_ok=True)
    base = os.path.join(a.sortie, f"repreneurs-{aujourd_hui.isoformat()}")
    with open(base + ".json", "w", encoding="utf-8") as h:
        json.dump({"genere_le": aujourd_hui.isoformat(), "depuis": depuis.isoformat(), "departements": deps,
                   "retenus": retenus, "exclus": [f for f in fiches if f["exclu"]]}, h, ensure_ascii=False, indent=1)
    with open(base + ".md", "w", encoding="utf-8") as h:
        h.write(f"# Repreneurs récents ({', '.join(deps)}) depuis le {depuis:%d/%m/%Y} — {len(retenus)} retenus, "
                f"{len(fiches) - len(retenus)} exclus (secteurs interdits)\n\nÀ revérifier le jour même avant tout appel.\n\n")
        h.writelines(f"- {f['date_parution']} · {f['activite']} · {f['code_postal']} {f['ville']} · "
                    f"{f['acheteur']} (SIREN {f['siren_acheteur']}) · {f['annonce']}\n" for f in retenus)
    print(f"{len(fiches)} rachats trouvés, {len(retenus)} retenus ; fichiers : {base}.json / .md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
