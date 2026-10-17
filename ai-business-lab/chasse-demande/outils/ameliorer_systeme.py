"""Auto-analyse de la conversation (idée du reel Instagram DekBh2BlTi9, 16/10/2026).

Lit l'historique local de la session Claude Code (fichier .jsonl), garde les messages
de l'utilisateur depuis N jours et repère :
- les corrections récurrentes (« encore », « je t'avais demandé », « pourquoi tu »…) ;
- les demandes répétées (mêmes mots-clés revenant souvent).

Le rapport est écrit dans un dossier PRIVÉ (jamais dans le dépôt : il cite les messages).
Usage : python3 ameliorer_systeme.py <historique.jsonl> <dossier_prive> [jours=7]
"""

import collections
import datetime as dt
import json
import re
import sys

CORRECTION = re.compile(
    r"\b(toujours pas|pas ça|c'est faux|erreur|tu as oublié|tu n'as pas|pourquoi tu|"
    r"je t'avais|je t'ai déjà|déjà dit|ne marche pas|ne fonctionne pas|pas bon|mauvais|"
    r"anglais|pas centré|chevauch\w*|où est-ce que|bah alors)\b",
    re.I,
)
MOTS_VIDES = set(
    "le la les de des du un une et à a au aux en pour pas que qui je tu il me te se ce ça "
    "est sur dans mon ma mes ton ta tes sont avec par plus ne y on nous vous stp merci oui "
    "non bien si fait faire peux peut c'est j'ai tout".split()
)


def messages(fichier, depuis):
    for ligne in open(fichier, errors="ignore"):
        try:
            d = json.loads(ligne)
        except ValueError:
            continue
        if d.get("type") != "user":
            continue
        c = d.get("message", {}).get("content")
        if isinstance(c, list):
            c = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
        if not isinstance(c, str):
            continue
        c = c.strip()
        # On écarte les messages du système, les résumés automatiques et les rappels programmés.
        if not c or c.startswith("<") or "SYSTEM NOTIFICATION" in c or c.startswith("This session is being continued"):
            continue
        if c.startswith(("Rappel", "Point autonome", "Relevé du courrier", "Bilan mensuel")):
            continue
        date = d.get("timestamp", "")[:10]
        if date >= depuis:
            yield date, c


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    fichier, sortie = sys.argv[1], sys.argv[2]
    jours = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    depuis = (dt.date.today() - dt.timedelta(days=jours)).isoformat()
    msgs = list(messages(fichier, depuis))
    corrections = [(d, t) for d, t in msgs if CORRECTION.search(t) and len(t) < 600]
    mots = collections.Counter()
    for _, t in msgs:
        if "/" in t[:200] and "image" in t.lower():
            continue  # captures d'écran : seul le chemin du fichier, sans intérêt
        for m in set(re.findall(r"[a-zà-ÿ]{5,}", t.lower())):
            if m not in MOTS_VIDES:
                mots[m] += 1
    rapport = [
        f"# Auto-analyse du {dt.date.today().isoformat()} (derniers {jours} jours)",
        "",
        f"Messages de l'utilisateur : {len(msgs)} ; corrections repérées : {len(corrections)}.",
        "",
        "## Corrections (à transformer en règle ou en outil si elles se répètent)",
    ]
    rapport += [f"- {d} : {t[:300]}" for d, t in corrections] or ["- aucune"]
    rapport += ["", "## Sujets les plus fréquents (mots présents dans le plus de messages)"]
    rapport += [f"- {m} : {n}" for m, n in mots.most_common(25)]
    nom = f"{sortie}/auto-analyse-{dt.date.today().isoformat()}.md"
    with open(nom, "w") as f:
        f.write("\n".join(rapport) + "\n")
    print(nom, len(msgs), len(corrections))


if __name__ == "__main__":
    main()
