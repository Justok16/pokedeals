"""Coordonnées de l'entrepreneur pour les documents de DIG16 (préparé le 08/10/2026, jour du dépôt au guichet).

Le dépôt est public : les vraies coordonnées n'y sont jamais écrites. Elles vivent dans un fichier JSON privé
(scratchpad ou Drive « Dig ») indiqué par la variable d'environnement DIG16_IDENTITE, par exemple :
  {"nom": "Prénom NOM", "adresse": "n° rue, code postal Ville", "telephone": "06 …", "siren": "123 456 789"}
Sans cette variable, les documents gardent les champs entre crochets (version publique du dépôt).
Avec elle, les générateurs écrivent leurs fichiers remplis dans DIG16_SORTIE (dossier privé, obligatoire),
jamais dans supports/.
Utilisé par outils/documents_commerciaux.py et outils/marque/flyer.py.
"""

import json
import os

# Champ entre crochets du dépôt -> clé du fichier privé
CHAMPS = {
    "[Prénom Nom]": "nom",
    "[Adresse]": "adresse",
    "[adresse]": "adresse",
    "[téléphone]": "telephone",
    "[Téléphone]": "telephone",
    "SIREN [numéro à l’immatriculation]": "siren",
    "SIREN [à compléter]": "siren",
}


def charger():
    """Renvoie le dictionnaire privé (et exige DIG16_SORTIE), ou None pour la version publique."""
    ident = charger_identite_seule()
    if ident and not os.environ.get("DIG16_SORTIE"):
        raise SystemExit("ALERTE : DIG16_SORTIE (dossier privé) est obligatoire avec DIG16_IDENTITE")
    return ident


def charger_identite_seule():
    """Renvoie le dictionnaire privé, ou None ; sans exiger de dossier de sortie (site : outils/ouverture_site.py)."""
    chemin = os.environ.get("DIG16_IDENTITE")
    if not chemin:
        return None
    with open(chemin, encoding="utf-8") as f:
        ident = json.load(f)
    manque = [k for k in ("nom", "adresse", "telephone", "siren") if not str(ident.get(k, "")).strip()]
    if manque:
        raise SystemExit(f"ALERTE identité incomplète : {manque}")
    return ident


def remplir(texte, ident):
    """Remplace les champs entre crochets ; ne touche pas aux champs du client (devis, facture)."""
    if not ident:
        return texte
    if ident.get("immatriculation"):  # date du Kbis : « Version du [date de l’immatriculation] » des CGV
        texte = texte.replace("[date de l’immatriculation]", ident["immatriculation"])
    for champ, cle in CHAMPS.items():
        valeur = ident[cle]
        if cle == "siren":  # immatriculé au RCS : ville du greffe obligatoire sur factures et papiers (art. R123-237)
            valeur = "SIREN " + valeur + (" — " + ident["rcs"] if ident.get("rcs") else "")
        texte = texte.replace(champ, valeur)
    return texte


def sortie(defaut):
    """Dossier où écrire les fichiers : supports/ (public) ou DIG16_SORTIE (privé)."""
    return os.environ.get("DIG16_SORTIE") or defaut
