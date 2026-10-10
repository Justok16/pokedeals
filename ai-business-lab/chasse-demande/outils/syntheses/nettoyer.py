# Vérifie les identifiants de vidéos cités : un identifiant inexistant est retiré (Gemini en invente parfois).
import re
import os
import glob

S = os.path.dirname(os.path.abspath(__file__))
K = "/home/user/pokedeals/ai-business-lab/chasse-demande/connaissances"
IDL = re.compile(r"[A-Za-z0-9_-]{11}")


def idlike(x):
    return bool(IDL.fullmatch(x)) and (
        re.search(r"\d|[-_]", x)
        or (re.search(r"[A-Z]", x[1:]) and re.search(r"[a-z]", x))
    )


for f in sorted(glob.glob(S + "/*__*.md")):
    if f.endswith(".propre.md"):
        continue
    ch = os.path.basename(f).split("__")[0]
    ok = {os.path.basename(g)[:-3] for g in glob.glob(f"{K}/{ch}/*.md")}
    t = open(f).read()
    bad = []

    def par(m):
        items = [
            re.sub(r"^Vid[ée]os? ?: ?", "", x.strip()) for x in m.group(1).split(",")
        ]
        if not any(idlike(x) for x in items):
            return m.group(0)
        keep = [x for x in items if x in ok]
        bad.extend(x for x in items if x not in ok)
        return f" ({', '.join(keep)})" if keep else ""

    t = re.sub(r" ?\(([^()]{1,200})\)", par, t)
    t = re.sub(
        r"(?m)^( {1,3})([*-]|\d+\.) ", lambda m: "    " + m.group(2) + " ", t
    )  # listes imbriquées : 4 espaces
    open(f[:-3] + ".propre.md", "w").write(t)
    print(os.path.basename(f), len(bad), bad[:6])
