"""Vérifie (et nettoie sur demande) les métadonnées cachées des images : position GPS, appareil,
date, logiciel. Idée tirée de l'outil « Metadata Remover » (annuaire nosignups.net, 28/09/2026),
refaite ici en local pour ne rien envoyer à un site tiers.

Usage :
  python3 verif_metadonnees.py <dossier>            # liste les images qui contiennent des métadonnées
  python3 verif_metadonnees.py <dossier> --nettoyer # réécrit ces images sans leurs métadonnées

À lancer sur toute photo fournie par un client avant de la mettre en ligne (une photo prise au
téléphone contient souvent la position GPS du domicile ou de l'atelier).
"""
import glob, os, sys
from PIL import Image

dossier = sys.argv[1] if len(sys.argv) > 1 else '.'
nettoyer = '--nettoyer' in sys.argv
vues, trouvees = 0, 0
for f in glob.glob(os.path.join(dossier, '**', '*'), recursive=True):
    if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        continue
    vues += 1
    im = Image.open(f)
    ex = im.getexif()
    if not len(ex) and not im.info.get('exif'):
        continue
    trouvees += 1
    gps = bool(ex.get_ifd(0x8825)) if len(ex) else False
    print(('GPS ! ' if gps else '') + f, f'({len(ex)} champs)')
    if nettoyer:
        propre = Image.frombytes(im.mode, im.size, im.tobytes())  # pixels seuls, sans métadonnées
        propre.save(f, quality=90) if f.lower().endswith(('.jpg', '.jpeg')) else propre.save(f)
print(f'{vues} images vues, {trouvees} avec métadonnées' + (' (nettoyées)' if nettoyer and trouvees else ''))
