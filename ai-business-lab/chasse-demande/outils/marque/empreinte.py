"""Empreinte de pouce dorée, motif de la campagne « Le test du pouce » (08/10/2026).

empreinte_svg(...) renvoie un <svg> autonome : crêtes concentriques ondulées et interrompues, à l'intérieur
de la forme d'une pulpe de pouce. Dessin déterministe (graine fixe) pour que chaque visuel soit identique.
"""

import math
import random


def _bruit(rng, n=5):
    return [(rng.uniform(.4, 1.6), rng.uniform(0, 2 * math.pi), rng.uniform(-1, 1)) for _ in range(n)]


def empreinte_svg(taille=900, couleur="#c8a46e", epaisseur=None, graine=16, cretes=30, opacite=1.0, ident="e"):
    rng = random.Random(graine)
    w, h = taille, taille * 1.22
    cx, cy = w * .5, h * .56
    pas = (w * .47) / cretes
    ep = epaisseur or pas * .34
    ondes = _bruit(rng)
    chemins = []
    for i in range(1, cretes + 1):
        r = i * pas
        ax, by = r * .86, r * 1.06
        # interruptions (bifurcations, fins de crête) : plus nombreuses vers l'extérieur
        coupes = sorted(rng.uniform(0, 2 * math.pi) for _ in range(rng.randint(1, 2 + i // 8)))
        debut = rng.uniform(0, 2 * math.pi)
        segments, a0 = [], debut
        for c in coupes:
            a1 = debut + (c - debut) % (2 * math.pi)
            if a1 - a0 > .25:
                segments.append((a0 + .05, a1 - .07))
            a0 = a1
        if debut + 2 * math.pi - a0 > .25:
            segments.append((a0 + .05, debut + 2 * math.pi - .07))
        for s0, s1 in segments:
            pts = []
            n = max(8, int((s1 - s0) * r / 6))
            for k in range(n + 1):
                t = s0 + (s1 - s0) * k / n
                d = sum(amp * math.sin(f * t * 2 + ph + i * .21 * sg) for f, ph, sg in ondes for amp in [pas * .18])
                # aplatissement du bas (pli de la phalange) et pointe vers le haut
                fy = 1 - .16 * max(0, math.sin(t)) ** 3
                x = cx + (ax + d) * math.cos(t)
                y = cy + (by + d) * math.sin(t) * fy - (pas * .45 * -math.sin(t) if math.sin(t) < 0 else 0) * (i / cretes)
                pts.append(f"{x:.1f},{y:.1f}")
            chemins.append("M" + " L".join(pts))
    forme = (f"M{w*.5:.0f},{h*.03:.0f} C{w*.93:.0f},{h*.03:.0f} {w*.99:.0f},{h*.42:.0f} {w*.96:.0f},{h*.7:.0f} "
             f"C{w*.93:.0f},{h*.93:.0f} {w*.72:.0f},{h*.99:.0f} {w*.5:.0f},{h*.99:.0f} "
             f"C{w*.28:.0f},{h*.99:.0f} {w*.07:.0f},{h*.93:.0f} {w*.04:.0f},{h*.7:.0f} "
             f"C{w*.01:.0f},{h*.42:.0f} {w*.07:.0f},{h*.03:.0f} {w*.5:.0f},{h*.03:.0f} Z")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'aria-hidden="true"><defs><clipPath id="{ident}c"><path d="{forme}"/></clipPath>'
            f'<radialGradient id="{ident}g" cx="50%" cy="54%" r="58%"><stop offset="0" stop-color="#fff"/>'
            f'<stop offset=".7" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity=".2"/>'
            f'</radialGradient><mask id="{ident}m"><rect width="100%" height="100%" fill="url(#{ident}g)"/></mask></defs>'
            f'<g clip-path="url(#{ident}c)" mask="url(#{ident}m)" fill="none" stroke="{couleur}" '
            f'stroke-width="{ep:.2f}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacite}">'
            + "".join(f'<path d="{c}"/>' for c in chemins) + "</g></svg>")


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write("<html><body style='margin:0;background:#0f0e0c'>" + empreinte_svg() + "</body></html>")
