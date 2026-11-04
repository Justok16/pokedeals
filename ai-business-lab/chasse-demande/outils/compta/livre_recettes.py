#!/usr/bin/env python3
"""Livre des recettes DIG16 + contrôles + préparation du e-reporting des paiements (04/11/2026, audit global).

Pourquoi : le micro-entrepreneur doit tenir un livre des recettes encaissées, chronologique, avec le montant,
l'origine (identité du client), le mode de règlement et la référence des pièces, et en faire le total tous les
3 mois (entreprendre.service-public.gouv.fr/vosdroits/F23266, « Vérifié le 07 septembre 2026 », lu le 04/11/2026).
L'offre gratuite d'Indy (Essentiel) ne fournit pas ce livre (il est dans l'offre Autonomie, page tarifs lue le
10/10/2026) : ce script le tient sans abonnement.

À partir du 01/09/2027, une micro-entreprise doit aussi transmettre (par sa plateforme agréée, Indy pour DIG16) :
- les DONNÉES DE PAIEMENT des prestations de services, « qu'elles aient donné lieu à facture ou non, entre
  assujettis ou avec un non-assujetti » (FAQ DGFiP « J'approfondis la facturation électronique », version du
  01/09/2026, § 4.1) ;
- les DONNÉES DE TRANSACTION des opérations avec des particuliers ou l'étranger (même FAQ, § 3 ; les ventes B2B
  en France passent, elles, par la facture électronique) ;
en franchise en base : « Bimestrielle civile », dépôt « au plus tard entre le 25 et 30 du mois suivant la fin de la
période » (impots.gouv.fr, tableau des fréquences et délais de transmission, lu le 04/11/2026).
Ce script ne transmet RIEN : il prépare et contrôle les chiffres que la plateforme agréée enverra, pour pouvoir les
comparer. Les trois flux (facture électronique, e-reporting transaction, e-reporting paiement) restent séparés.

Entrée : un CSV PRIVÉ (jamais dans le dépôt), une ligne par encaissement, colonnes :
  date_encaissement (AAAA-MM-JJ), numero_facture, client, type_client (pro|particulier), pays (code ISO, FR par
  défaut), nature (service|vente), montant_eur (TTC = HT en franchise), mode (virement|prelevement|cheque|especes|cb)

Usage :
  python3 livre_recettes.py recettes.csv --sortie DOSSIER_PRIVE [--annee 2026]
Sorties (dans DOSSIER_PRIVE, refusé s'il est dans le dépôt) : livre-recettes-<annee>.csv, controle-<annee>.md
Code de sortie : 0 si aucun défaut, 1 si au moins une ALERTE.
"""

import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
VALEURS = os.path.join(ICI, "..", "..", "connaissances", "fiscal-valeurs.json")
DEBUT_E_REPORTING = date(2027, 9, 1)  # micro-entreprises (FAQ DGFiP § 3.2, version du 01/09/2026)
MODES = {"virement", "prelevement", "cheque", "especes", "cb"}
TYPES = {"pro", "particulier"}
NATURES = {"service", "vente"}
PARIS = ZoneInfo("Europe/Paris")
COLONNES = ["date_encaissement", "numero_facture", "client", "type_client", "pays", "nature", "montant_eur", "mode"]


def seuils_franchise():
    """Seuils de la franchise en base de TVA (prestations de services), depuis le fichier de valeurs datées."""
    with open(VALEURS, encoding="utf-8") as f:
        v = json.load(f)["franchise_tva_services"]
    return Decimal(str(v["base"])), Decimal(str(v["majore"])), v["source"]


def lire(chemin):
    """Lit le CSV ; renvoie (lignes valides, liste d'alertes)."""
    lignes, alertes = [], []
    with open(chemin, newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        manque = [c for c in COLONNES if c not in (lecteur.fieldnames or []) and c != "pays"]
        if manque:
            return [], [f"colonnes absentes : {', '.join(manque)}"]
        for n, r in enumerate(lecteur, start=2):
            r = {k: (v or "").strip() for k, v in r.items()}
            r["pays"] = (r.get("pays") or "FR").upper()
            try:
                r["date"] = date.fromisoformat(r["date_encaissement"])
            except ValueError:
                alertes.append(f"ligne {n} : date invalide « {r['date_encaissement']} »")
                continue
            try:
                r["montant"] = Decimal(r["montant_eur"].replace(",", "."))
            except InvalidOperation:
                alertes.append(f"ligne {n} : montant invalide « {r['montant_eur']} »")
                continue
            if r["montant"] == 0:
                alertes.append(f"ligne {n} : montant nul")
            if r["mode"] not in MODES:
                alertes.append(f"ligne {n} : mode de règlement inconnu « {r['mode']} » (attendu : {', '.join(sorted(MODES))})")
            if r["type_client"] not in TYPES:
                alertes.append(f"ligne {n} : type de client inconnu « {r['type_client']} » (pro ou particulier)")
            if r["nature"] not in NATURES:
                alertes.append(f"ligne {n} : nature inconnue « {r['nature']} » (service ou vente)")
            if not r["numero_facture"]:
                alertes.append(f"ligne {n} : référence de la pièce (numéro de facture) manquante")
            if not r["client"]:
                alertes.append(f"ligne {n} : origine de la recette (client) manquante")
            r["ligne"] = n
            lignes.append(r)
    return sorted(lignes, key=lambda x: (x["date"], x["numero_facture"])), alertes


def trimestre(d):
    return (d.month - 1) // 3 + 1


def bimestre(d):
    """Bimestre civil (1 = janvier-février … 6 = novembre-décembre)."""
    return (d.month - 1) // 2 + 1


def echeance_bimestre(annee, b):
    """Mois du dépôt : le mois suivant la fin du bimestre ; délai « entre le 25 et 30 » de ce mois."""
    fin = 2 * b
    return (annee + 1, 1) if fin == 12 else (annee, fin + 1)


def controler(lignes, annee, seuil_base, seuil_majore):
    alertes, infos = [], []
    vues = defaultdict(list)
    for r in lignes:
        vues[r["numero_facture"]].append(r)
    for num, rs in vues.items():
        total = sum(x["montant"] for x in rs)
        if len(rs) > 1 and total <= 0:
            alertes.append(f"facture {num} : encaissements dont la somme est nulle ou négative ({total} €)")
        elif len(rs) > 1:
            infos.append(f"facture {num} : {len(rs)} encaissements (paiement partiel ou acompte), total {total} €")
    ca = sum(r["montant"] for r in lignes if r["date"].year == annee)
    if ca > seuil_majore:
        alertes.append(f"CA encaissé {annee} = {ca} € > seuil majoré {seuil_majore} € : la franchise de TVA est perdue "
                       "dès le jour du dépassement (TVA à facturer) — prévenir l'utilisateur immédiatement")
    elif ca > seuil_base:
        alertes.append(f"CA encaissé {annee} = {ca} € > seuil de base {seuil_base} € : franchise conservée cette année "
                       "si le seuil majoré n'est pas atteint, perdue l'année suivante — prévenir l'utilisateur")
    elif ca > seuil_base * Decimal("0.8"):
        infos.append(f"CA encaissé {annee} = {ca} € : plus de 80 % du seuil de franchise ({seuil_base} €)")
    return alertes, infos, ca


def e_reporting(lignes):
    """Prépare, par bimestre civil, les totaux attendus à partir du 01/09/2027 (rien n'est transmis ici)."""
    paiement = defaultdict(lambda: defaultdict(Decimal))     # (année, bimestre) -> date -> montant (services)
    transaction = defaultdict(lambda: defaultdict(Decimal))  # (année, bimestre) -> date -> montant (B2C/étranger)
    for r in lignes:
        if r["date"] < DEBUT_E_REPORTING:
            continue
        cle = (r["date"].year, bimestre(r["date"]))
        if r["nature"] == "service":
            paiement[cle][r["date"]] += r["montant"]
        if r["type_client"] == "particulier" or r["pays"] != "FR":
            transaction[cle][r["date"]] += r["montant"]
    return paiement, transaction


def dans_le_depot(chemin):
    try:
        racine = subprocess.run(["git", "-C", ICI, "rev-parse", "--show-toplevel"], capture_output=True,
                                text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return os.path.realpath(chemin).startswith(os.path.realpath(racine) + os.sep) or \
        os.path.realpath(chemin) == os.path.realpath(racine)


def ecrire(lignes, annee, sortie, alertes, infos, ca, source_seuils):
    os.makedirs(sortie, exist_ok=True)
    livre = os.path.join(sortie, f"livre-recettes-{annee}.csv")
    with open(livre, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Date d'encaissement", "Référence de la pièce", "Client (origine)", "Nature", "Mode de règlement",
                    "Montant (€)", "Total du trimestre (€)"])
        cumul = defaultdict(Decimal)
        de_l_annee = [r for r in lignes if r["date"].year == annee]
        for i, r in enumerate(de_l_annee):
            t = trimestre(r["date"])
            cumul[t] += r["montant"]
            dernier = i == len(de_l_annee) - 1 or trimestre(de_l_annee[i + 1]["date"]) != t
            w.writerow([r["date"].strftime("%d/%m/%Y"), r["numero_facture"], r["client"], r["nature"], r["mode"],
                        f"{r['montant']:.2f}", f"T{t} : {cumul[t]:.2f}" if dernier else ""])
        w.writerow(["", "", "", "", "TOTAL ANNUEL", f"{ca:.2f}", ""])
    paiement, transaction = e_reporting(lignes)
    rapport = os.path.join(sortie, f"controle-{annee}.md")
    with open(rapport, "w", encoding="utf-8") as f:
        f.write(f"# Contrôle du livre des recettes {annee} (DIG16)\n\nGénéré le {datetime.now(PARIS):%d/%m/%Y}. "
                f"Seuils de franchise : {source_seuils}.\n\n## Alertes\n")
        f.write("".join(f"- ALERTE {a}\n" for a in alertes) or "- aucune\n")
        f.write("\n## Informations\n" + ("".join(f"- {i}\n" for i in infos) or "- rien à signaler\n"))
        f.write("\n## E-reporting (préparation, à comparer avec la plateforme agréée ; obligation au 01/09/2027)\n")
        if not paiement and not transaction:
            f.write("- aucun encaissement à partir du 01/09/2027 dans ce fichier.\n")
        for (a, b) in sorted(set(paiement) | set(transaction)):
            ma, mm = echeance_bimestre(a, b)
            f.write(f"\n### {a}, bimestre {b} (mois {2*b-1:02d}-{2*b:02d}) — dépôt entre le 25 et le 30/{mm:02d}/{ma}\n")
            p = paiement.get((a, b), {})
            t = transaction.get((a, b), {})
            f.write(f"- Données de paiement (services encaissés) : {sum(p.values()):.2f} € sur {len(p)} jour(s)\n")
            f.write(f"- Données de transaction (particuliers / étranger) : {sum(t.values()):.2f} € sur {len(t)} jour(s)\n")
    return livre, rapport


def main(argv):
    if len(argv) < 2 or "--sortie" not in argv:
        print(__doc__)
        return 2
    entree = argv[1]
    sortie = argv[argv.index("--sortie") + 1]
    annee = int(argv[argv.index("--annee") + 1]) if "--annee" in argv else datetime.now(PARIS).year
    if dans_le_depot(sortie) or dans_le_depot(entree):
        print("REFUSÉ : le fichier des recettes et les sorties contiennent des données de clients ; "
              "ils doivent rester hors du dépôt (scratchpad privé ou Drive « Dig »).")
        return 2
    base, majore, source = seuils_franchise()
    lignes, alertes = lire(entree)
    a2, infos, ca = controler(lignes, annee, base, majore)
    alertes += a2
    livre, rapport = ecrire(lignes, annee, sortie, alertes, infos, ca, source)
    for a in alertes:
        print("ALERTE", a)
    print(f"{len(lignes)} encaissement(s) ; CA {annee} = {ca:.2f} € ; livre : {livre} ; rapport : {rapport}")
    return 1 if alertes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
