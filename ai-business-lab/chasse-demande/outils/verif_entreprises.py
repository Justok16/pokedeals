"""Vérifie la santé administrative d'une liste d'entreprises avant de les démarcher ou de signer.

Pour chaque entreprise : SIREN (fourni ou retrouvé dans l'annuaire officiel par nom + commune),
état (active / fermée) et annonces BODACC de procédures collectives (sauvegarde, redressement,
liquidation) et de radiation.

Usage : python3 verif_entreprises.py entree.json sortie.json cookies.txt [departement]
  entree.json : liste d'objets {"n", "nom", "commune", "siren" (facultatif)}
  cookies.txt : cookie du relais Vercel (voir 33-outils.md), car l'annuaire bloque les conteneurs.
Les listes de prospects sont privées : entree/sortie restent hors du dépôt.
"""

import json
import re
import sys
import time
import unicodedata
import urllib.parse
import subprocess

RELAIS = "https://relais-dig-justok1.vercel.app/api/entreprise"
BODACC = "https://bodacc-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/annonces-commerciales/records"


def norm(s):
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def curl(url, cookies=None):
    cmd = ["curl", "-s", "-m", "40", url] + (["-b", cookies] if cookies else [])
    for essai in range(3):
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        if "Protected by Vercel Authentication" in out:
            sys.exit(
                "cookie du relais Vercel expiré : renouveler /tmp/cj.txt (33-outils.md) puis relancer"
            )
        try:
            return json.loads(out)
        except Exception:
            time.sleep(3 + 5 * essai)
    return None


def chercher(e, cookies, dep):
    """Renvoie (résultat annuaire, confiance) ; confiance = 'siren', 'commune' ou 'faible'."""
    if e.get("siren"):
        d = curl(f"{RELAIS}?q={e['siren']}&per_page=1", cookies)
        if d and d.get("results"):
            return d["results"][0], "siren"
    nom = re.sub(r"\(.*?\)", " ", e["nom"])
    q = urllib.parse.quote(nom)
    d = curl(f"{RELAIS}?q={q}&departement={dep}&per_page=10", cookies)
    res = (d or {}).get("results") or []
    com = norm(e.get("commune", "")).split(" ")[0]
    for r in res:
        communes = [norm((r.get("siege") or {}).get("libelle_commune", ""))]
        communes += [
            norm(m.get("libelle_commune", ""))
            for m in r.get("matching_etablissements") or []
        ]
        if com and any(c.startswith(com) or com in c for c in communes if c):
            return r, "commune"
    return (res[0], "faible") if res else (None, "introuvable")


def bodacc(siren):
    w = urllib.parse.quote(
        f'registre="{siren}" and (familleavis="collective" or familleavis="radiation")'
    )
    d = curl(
        f"{BODACC}?where={w}&order_by=dateparution%20desc&limit=20&select=familleavis,familleavis_lib,dateparution,jugement,tribunal"
    )
    L = []
    for r in (d or {}).get("results") or []:
        nature = ""
        try:
            j = json.loads(r.get("jugement") or "{}")
            nature = j.get("nature") or j.get("complementJugement") or ""
        except Exception:
            nature = str(r.get("jugement") or "")[:120]
        L.append(
            {
                "type": r.get("familleavis_lib"),
                "date": r.get("dateparution"),
                "nature": nature[:160],
            }
        )
    return L


def main():
    entree, sortie, cookies = sys.argv[1:4]
    dep = sys.argv[4] if len(sys.argv) > 4 else "16"
    E = json.load(open(entree))
    R = []
    for e in E:
        r, conf = chercher(e, cookies, dep)
        x = dict(e, confiance=conf)
        if r:
            x.update(
                siren=r["siren"],
                nom_officiel=r.get("nom_complet"),
                etat=r.get("etat_administratif"),
                date_fermeture=r.get("date_fermeture"),
                commune_siege=(r.get("siege") or {}).get("libelle_commune"),
            )
            x["bodacc"] = bodacc(r["siren"])
        R.append(x)
        print(
            e.get("n"),
            conf,
            x.get("siren"),
            x.get("etat"),
            len(x.get("bodacc", [])),
            flush=True,
        )
        time.sleep(0.4)
    json.dump(R, open(sortie, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
