#!/usr/bin/env python3
"""Suivi de l'immatriculation de DIG16 dans l'annuaire officiel (préparé le 08/10/2026).

Usage : DIG16_IDENTITE=<json privé> python3 outils/suivi_siren.py
Interroge l'API publique recherche-entreprises.api.gouv.fr (annuaire des entreprises de l'État, sans clé)
avec le SIREN du fichier privé (jamais écrit dans ce dépôt). Affiche :
  « PAS ENCORE PUBLIÉ » tant que l'entreprise n'apparaît pas ;
  « PUBLIÉ » avec l'état administratif, la date de création, l'activité (code NAF) et la commune.
Code de sortie : 0 publié, 1 pas encore publié, 2 annuaire injoignable (le conteneur coupe parfois la
connexion : 4 essais espacés).
Quand c'est publié : lancer outils/ouverture_site.py (voir 31-creation-entreprise.md).
"""

import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "marque"))
import identite  # noqa: E402

API = "https://recherche-entreprises.api.gouv.fr/search?q="


def interroger(numero):
    for essai in range(4):
        try:
            with urllib.request.urlopen(API + numero, timeout=20) as r:
                return json.load(r)
        except OSError:
            time.sleep(2 * 2**essai)
    return None


def main():
    ident = identite.charger_identite_seule()
    if not ident:
        raise SystemExit("ALERTE : DIG16_IDENTITE manquant (fichier privé)")
    numero = "".join(ch for ch in ident["siren"] if ch.isdigit())
    rep = interroger(numero)
    if rep is None:
        print("ANNUAIRE INJOIGNABLE (réessayer au prochain point)")
        return 2
    res = [e for e in rep.get("results", []) if e.get("siren") == numero]
    if not res:
        print("PAS ENCORE PUBLIÉ dans l'annuaire officiel")
        return 1
    e = res[0]
    siege = e.get("siege") or {}
    print("PUBLIÉ :", "état", e.get("etat_administratif"), "| création", e.get("date_creation"),
          "| NAF", e.get("activite_principale"), "| commune", siege.get("libelle_commune"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
