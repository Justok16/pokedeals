# Étape 0 (02/10) : doublons d'un lot de candidats contre suivi_appels.csv (téléphone 9 derniers chiffres, puis nom/enseigne normalisés)
import json
import csv
import re
import sys
import unicodedata

S = "/tmp/claude-0/-home-user-pokedeals/444b8073-9084-510a-bb75-4fe03b0350df/scratchpad"


def norm(s):
    s = (s or "").replace("\u2019", "'").replace("'", " ")
    s = (
        unicodedata.normalize("NFKD", s or "")
        .encode("ascii", "ignore")
        .decode()
        .lower()
    )
    s = re.sub(r"\b(sarl|sas|eurl|sasu|sa|snc|ei|le|la|les|l|du|de|des|d|et)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def tel9(t):
    d = re.sub(r"\D", "", t or "")
    return d[-9:] if len(d) >= 9 else ""


rows = list(csv.DictReader(open(S + "/appels/suivi_appels.csv", encoding="utf-8")))
tels = {}
noms = {}
for r in rows:
    for k, v in r.items():
        if v and ("tel" in k.lower() or "phone" in k.lower()):
            for t in re.findall(r"(?:\+33|0)[\d\s.]{8,}", v):
                t9 = tel9(t)
                if t9:
                    tels.setdefault(t9, r)
    for k in r:
        if any(x in k.lower() for x in ("nom", "enseigne", "prospect", "entreprise")):
            # nom complet, nom sans parenthèse et contenu des parenthèses (ex. « RD Bois (Renaud Dussagne) »)
            for v in [r[k], re.sub(r"\s*\([^)]*\)", "", r[k])] + re.findall(
                r"\(([^)]+)\)", r[k]
            ):
                n = norm(v)
                if len(n) >= 5:
                    noms.setdefault(n, r)
a, b = int(sys.argv[1]), int(sys.argv[2])
cands = json.load(
    open(sys.argv[5] if len(sys.argv) > 5 else S + "/verif8/cands.json")
)  # 5e argument facultatif : fichier du vivier
out = {}
dup = []
flags = {}
import collections

vv = collections.Counter(tel9(x.get("telephone", "")) for x in cands)
for i in range(a, b + 1):
    c = cands[i]
    t9 = tel9(c.get("telephone", ""))
    names = (
        [c["nom"], re.sub(r"\s*\([^)]*\)", "", c["nom"])]
        + re.findall(r"\(([^)]+)\)", c["nom"])
        + ([c["enseigne"]] if c.get("enseigne") else [])
    )
    hit = None
    nhit = None
    for n in names:
        nn = norm(n)
        if len(nn) >= 5 and nn in noms:
            nhit = noms[nn]
            break
    if nhit:
        hit = ("nom", nhit)
    elif t9 and t9 in tels:
        r = tels[t9]
        rn = norm(r.get("Entreprise", ""))
        same = any(norm(n) and (norm(n) in rn or rn in norm(n)) for n in names)
        if same:
            hit = ("tel", r)
        else:
            flags[str(i)] = (
                "téléphone du registre partagé avec n° %s (%s) : non fiable, à confirmer par un annuaire public"
                % (
                    next((r[k] for k in r if k.lower().startswith("n")), "?"),
                    r.get("Entreprise", ""),
                )
            )
    if not hit and t9 and vv[t9] > 1 and str(i) not in flags:
        flags[str(i)] = (
            "téléphone partagé dans le vivier par %d entreprises : non fiable, à confirmer par un annuaire public"
            % vv[t9]
        )
    if hit:
        r = hit[1]
        num = next((r[k] for k in r if k.lower().startswith("n")), "?")
        dup.append((i, c["nom"], c["commune"], hit[0], num))
        continue
    out[str(i)] = c["nom"]
print("doublons", len(dup))
[print(" ", d) for d in dup]
print("à sonder", len(out))
print("drapeaux", flags)
json.dump(
    flags,
    open(sys.argv[3].replace(".json", "_drapeaux.json"), "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=0,
)
json.dump(out, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
