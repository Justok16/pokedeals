"""Repère les « signatures » de site fait par IA (look générique) dans une page HTML de démo.

Règles adaptées de Taste Skill (Leonxlnx/taste-skill, licence MIT, section 9 « AI Tells »), lu en entier
le 29/09/2026, et ramenées au français et à nos démos (un seul fichier HTML, photos réelles).
Usage : python3 anti_generique.py page1.html [page2.html ...]   (code de sortie 1 si un défaut bloquant)
"""

import re
import sys
import html as H

REGLES = [  # (gravité, nom, motif sur le texte visible, conseil)
    (
        "bloquant",
        "numéros de section décoratifs",
        r"(?m)^\s*0\d\s*[/·.]\s*\S",
        "nommer la section en clair (« Nos travaux »), pas « 01 / Services »",
    ),
    (
        "bloquant",
        "étapes génériques",
        r"\b(Étape|Etape|Phase|Stage|Step)\s*0?\d\b",
        "le contenu de l’étape sert de titre (« On se rencontre », « Devis »)",
    ),
    (
        "bloquant",
        "invitation à défiler",
        r"(?i)\b(scroll|défilez|faites défiler)\b",
        "supprimer : le visiteur sait faire défiler",
    ),
    (
        "bloquant",
        "verbes creux",
        r"(?i)\b(révolutionn\w*|sublim\w+ votre|seamless|next-gen|unleash|elevate)\b",
        "verbes concrets (« poser », « réparer », « isoler »)",
    ),
    (
        "bloquant",
        "noms bidon",
        r"\b(Jean Dupont|John Doe|Jane Doe|Acme|Lorem ipsum)\b",
        "vrais noms ou rien",
    ),
    (
        "attention",
        "chiffres trop ronds ou trop parfaits",
        r"\b(100\s?%|99[.,]9\d?\s?%)",
        "chiffre réel et sourcé, sinon le retirer",
    ),
    (
        "attention",
        "trop de points médians",
        r"(?:[^·\n]*·){3,}",
        "au plus un « · » par ligne",
    ),
    (
        "attention",
        "étiquette de version",
        r"\b(BETA|Bêta|v\d+\.\d+)\b",
        "pas de numéro de version sur un site vitrine",
    ),
]


def texte_visible(s):
    s = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|h\d|li|a|span|figcaption|button)>", "\n", s)
    return H.unescape(re.sub(r"<[^>]+>", " ", s))


def structure(s):
    """Défauts de mise en page repérables dans le code."""
    d = []
    # trois cartes identiques côte à côte (grille de 3 colonnes égales)
    if re.search(
        r"grid-template-columns\s*:\s*(repeat\(\s*3\s*,\s*1fr\s*\)|1fr\s+1fr\s+1fr)(?!\s*\w)",
        s,
    ):
        d.append(
            (
                "attention",
                "grille de 3 colonnes égales",
                "varier : 2 colonnes décalées, grille asymétrique",
            )
        )
    if re.search(r"(?i)cursor\s*:\s*url\(", s):
        d.append(
            ("bloquant", "curseur de souris personnalisé", "supprimer (accessibilité)")
        )
    if re.search(r"#000000\b|#000\b(?![0-9a-f])", s, re.I):
        d.append(("attention", "noir pur #000", "préférer un noir doux (charbon)"))
    if re.search(
        r"(?i)picsum\.photos|placehold\.co|placehold\.it|via\.placeholder\.com|dummyimage\.com",
        s,
    ):
        d.append(
            (
                "bloquant",
                "image de remplissage",
                "photos réelles sous licence libre uniquement",
            )
        )
    return d


code = 0
for f in sys.argv[1:]:
    s = open(f, encoding="utf-8").read()
    t = texte_visible(s)
    trouve = []
    for grav, nom, motif, conseil in REGLES:
        m = re.search(motif, t)
        if m:
            trouve.append((grav, nom, conseil, m.group(0).strip()[:60]))
    trouve += [(g, n, c, "") for g, n, c in structure(s)]
    if not trouve:
        print(f"OK  {f}")
    for g, n, c, ex in trouve:
        print(f"{g.upper():10} {f} : {n}" + (f" (« {ex} »)" if ex else "") + f" → {c}")
        if g == "bloquant":
            code = 1
sys.exit(code)
