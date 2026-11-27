#!/usr/bin/env python3
"""Lire la réponse (trop longue pour être affichée) de l'action Zapier Buffer « New Sent Item ».

Ajouté le 27/11/2026 par l'auto-analyse : la vérification « la publication est-elle partie ? » se faisait à la main
(script recopié trois fois dans la semaine). Usage :
    python3 outils/lire_buffer_envoyes.py <fichier de résultat Zapier> [nombre]
Affiche, de la plus récente à la plus ancienne : date d'envoi (heure de Paris), réseau, début du texte.
Seulement des données publiques (textes déjà publiés) ; rien n'est écrit sur le disque.
"""
import datetime
import json
import re
import sys
from zoneinfo import ZoneInfo

MOTIF = re.compile(r'"sent_at":\s*(\d+).{0,4000}?"text":\s*"((?:[^"\\]|\\.)*)"', re.S)
SERVICE = re.compile(r'"profile_service":\s*"([a-z]+)"')


def lire(chemin, nombre=5):
    brut = open(chemin, encoding="utf-8", errors="replace").read()
    reseau = SERVICE.search(brut)
    lignes = []
    for horodatage, texte in MOTIF.findall(brut)[:nombre]:
        try:
            texte = json.loads('"' + texte + '"')
        except ValueError:
            pass
        quand = datetime.datetime.fromtimestamp(int(horodatage), ZoneInfo("Europe/Paris"))
        lignes.append(f"{quand:%d/%m %H:%M} | {(reseau.group(1) if reseau else '?')} | {texte.splitlines()[0][:90] if texte else '(sans texte : story)'}")
    return lignes


def autotest():
    exemple = '{"sent_at": 1795718103, "profile_service":"facebook", "x":1, "text": "Bonjour\\nsuite"}'
    import tempfile
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
        f.write(exemple)
    res = lire(f.name)
    ok = len(res) == 1 and "facebook" in res[0] and "Bonjour" in res[0]
    print("OK" if ok else "ÉCHEC", res)
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sys.exit(autotest())
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for ligne in lire(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 5):
        print(ligne)
