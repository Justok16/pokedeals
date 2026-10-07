# Transforme une démo gen2 (images en base64) en page de site : images en fichiers nommés, chargement différé.
# Usage : python3 vers_site.py demo.html dossier_sortie "Titre" "Description"
import re
import base64
import sys
import os

src, dest, titre, desc = sys.argv[1:5]
PH = os.environ.get("DIG_PHOTOS", "photos/")
NOMS = {
    "hbois_0": "atelier",
    "hbois_2": "reserve-bois",
    "hbois_6": "artisan",
    "hbois_12": "assemblage",
    "hbois_13": "finitions",
    "hbois_9": "bois-selectionne",
}
par_octets = {open(PH + k + ".jpg", "rb").read(): v for k, v in NOMS.items()}
s = open(src).read()
vus = []


def rep(m):
    b = base64.b64decode(m.group(1))
    n = par_octets[b]
    premier = not vus
    vus.append(n)
    open(os.path.join(dest, n + ".jpg"), "wb").write(b)
    return (
        'src="' + n + '.jpg"' + ("" if premier else ' loading="lazy" decoding="async"')
    )


s = re.sub(r'src="data:image/jpeg;base64,([^"]+)"', rep, s)
s = re.sub(
    r"<title>[^<]*</title>",
    "<title>" + titre + '</title><meta name="description" content="' + desc + '">',
    s,
    count=1,
)
open(os.path.join(dest, "index.html"), "w").write(s)
print(vus, len(s))
