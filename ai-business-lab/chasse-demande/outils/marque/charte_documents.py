"""Charte imprimée de DIG16 (08/10/2026), commune à tous les documents A4 : même rendu que dig16.fr.

Papier clair pour l'impression, couverture noir chaud et laiton, titres Instrument Serif, texte Geist,
étiquettes Geist Mono. Importé par documents_commerciaux.py, plan_complet.py, campagne_pdf.py et
appliqué aux supports écrits à la main par outils/marque/restyler_supports.py.
Les images sont appelées depuis supports/ (chemin relatif « ../site-dig/img/marque/ »).
"""

POLICES = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
    '&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=block" rel="stylesheet">'
)

MARQUE = "../site-dig/img/marque/"

# Couleurs de la charte (60-charte-dig16.md)
NUIT, IVOIRE, DOUX, OR, OR_CLAIR = "#0f0e0c", "#efe9df", "#a8a093", "#c8a46e", "#d9bb8a"
TEXTE, GRIS, TRAIT, FOND_DOUX, BRONZE = "#1a1814", "#655e54", "#e0d8cb", "#f6f2ea", "#7a5a2c"

# Base commune : à placer avant le CSS propre à chaque document.
BASE = f"""
:root{{--nuit:{NUIT};--ivoire:{IVOIRE};--doux:{DOUX};--or:{OR};--or-clair:{OR_CLAIR};
--texte:{TEXTE};--gris:{GRIS};--trait:{TRAIT};--fond-doux:{FOND_DOUX};--bronze:{BRONZE}}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:Geist,Arial,sans-serif;color:var(--texte);font-feature-settings:"ss01"}}
h1,h2,h3{{font-family:'Instrument Serif',Georgia,serif;font-weight:400;letter-spacing:-.005em;color:var(--texte)}}
h1 em,h2 em{{color:var(--bronze)}}
b,strong{{font-weight:600}}
a{{color:var(--bronze)}}
.k,.etiquette{{font-family:'Geist Mono',monospace;font-weight:400;letter-spacing:.18em;text-transform:uppercase;color:var(--bronze)}}
.couv,.cover{{position:relative}}
.signature{{display:block;height:12.5mm}}
.embleme{{display:block;width:13mm;height:13mm}}
"""

# Bandeau de couverture sombre réutilisable (documents commerciaux, plans).
COUVERTURE = f"""
.couv{{background:{NUIT};color:{IVOIRE};border-radius:3mm;padding:5.5mm 8mm 5.6mm;margin-bottom:4.5mm;
 background-image:radial-gradient(90mm 50mm at 100% 0,rgba(200,164,110,.16),rgba(200,164,110,0) 70%);
 box-shadow:inset 0 0 0 .25mm rgba(200,164,110,.35)}}
.couv .ligne-haut{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:3mm}}
.couv .k{{color:{OR};font-size:7pt;display:flex;align-items:center;gap:2.4mm}}
.couv .k::before{{content:"";width:7mm;height:.3mm;background:{OR}}}
.couv h1{{color:{IVOIRE};font-size:23pt;line-height:1;margin:1.8mm 0 1.4mm}}
.couv h1 em{{color:{OR_CLAIR}}}
.couv p{{color:{DOUX};margin:.5mm 0}}
"""


def bandeau(etiquette, titre, sous=""):
    """Couverture sombre avec la signature DIG16 et l'emblème."""
    return (
        '<div class="couv"><div class="ligne-haut">'
        f'<img class="signature" src="{MARQUE}signature-ivoire@6x.png" alt="DIG16, sites internet">'
        f'<img class="embleme" src="{MARQUE}embleme-or@6x.png" alt=""></div>'
        f'<div class="k">{etiquette}</div><h1>{titre}</h1>'
        + (f"<p>{sous}</p>" if sous else "")
        + "</div>"
    )


def attendre_polices(pg):
    """Les polices web doivent être chargées avant le PDF (leçon du 02/10 : titres en police de secours)."""
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(400)
    charge = pg.evaluate("[...new Set([...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family))]")
    manque = {"Instrument Serif", "Geist"} - set(charge)
    if manque:
        raise SystemExit(f"ALERTE polices non chargées : {manque}")
