"""Simulateur DIG16 : ce que coûte un chiffre d'affaires en micro-entreprise, BIC ou BNC.

Usage : python3 outils/fiscal/simulateur.py <CA annuel HT> [--sans-acre]
        python3 outils/fiscal/simulateur.py --cfe2026 <CA HT encaissé en 2026>

Les taux viennent de connaissances/fiscal-valeurs.json (sources officielles datées).
Le script refuse de calculer si ces valeurs ont plus de 45 jours : relancer la veille fiscale.
Aucune donnée personnelle : seulement des montants.
"""

import datetime as dt
import json
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parents[2]
VALEURS = json.loads((ICI / "connaissances" / "fiscal-valeurs.json").read_text(encoding="utf-8"))
MAX_AGE = 45


def verifier_fraicheur() -> None:
    lu = dt.date.fromisoformat(VALEURS["_lu_le"])
    age = (dt.datetime.now(dt.UTC).date() - lu).days
    if age > MAX_AGE:
        sys.exit(f"ALERTE : valeurs fiscales lues il y a {age} jours (> {MAX_AGE}). Relancer la veille fiscale avant tout calcul.")


def euros(x: float) -> str:
    return f"{x:,.0f} €".replace(",", " ")


def cout(ca: float, nature: str, acre: bool) -> dict:
    t = VALEURS["cotisations_taux"][nature]["acre" if acre else "normal"]
    cotis = ca * t
    cfp = ca * VALEURS["cfp_taux"][nature]
    # Taxe CCI additionnelle à la CFE : comptée ici par prudence (cas où la CFE est due) ;
    # elle vaut 0 € l'année de création et les années d'exonération de CFE.
    tcci = 0.0 if ca <= VALEURS["tcci_taux"]["exoneration_si_ca_inferieur_ou_egal"] else ca * VALEURS["tcci_taux"][nature]
    ab = VALEURS["abattement_micro"]
    benefice = max(0.0, ca - max(ca * ab[nature], ab["minimum"]))
    return {"cotisations": cotis, "cfp": cfp, "tcci": tcci, "total": cotis + cfp + tcci, "benefice_imposable_avant_exoneration": benefice}


def simuler(ca: float, acre: bool) -> None:
    print(f"Chiffre d'affaires annuel HT : {euros(ca)} ({'avec' if acre else 'sans'} ACRE)")
    lignes = {n: cout(ca, n, acre) for n in ("BIC_services", "BNC_liberal")}
    for n, r in lignes.items():
        print(f"  {n:13s} cotisations {euros(r['cotisations']):>9s} + formation {euros(r['cfp']):>6s} + CCI {euros(r['tcci']):>5s} = {euros(r['total']):>9s}"
              f" ; bénéfice imposable {euros(r['benefice_imposable_avant_exoneration'])} (exonéré d'impôt sur le revenu en ZFRR+ pendant 59 mois)")
    ecart = lignes["BNC_liberal"]["total"] - lignes["BIC_services"]["total"]
    print(f"  Écart BNC - BIC : {euros(ecart)} par an en faveur du BIC.")
    plafond = VALEURS["franchise_tva_services"]
    if ca > plafond["majore"]:
        print(f"  ALERTE TVA : au-delà de {euros(plafond['majore'])}, la TVA est due dès le jour du dépassement.")
    elif ca > plafond["base"]:
        print(f"  ATTENTION TVA : au-delà de {euros(plafond['base'])}, TVA due à partir du 1er janvier suivant.")
    if ca > VALEURS["plafond_micro_services"]["valeur"]:
        print("  ALERTE : plafond du régime micro dépassé.")


def cfe_2026(ca_2026: float) -> None:
    debut = dt.date.fromisoformat(VALEURS["debut_activite"])
    jours = (dt.date(2026, 12, 31) - debut).days + 1
    seuil = VALEURS["cfe"]["exoneration_ca_n2_inferieur_ou_egal"]
    plafond_2026 = seuil * jours / 365
    ramene = ca_2026 * 365 / jours
    print(f"Activité en 2026 : {jours} jours. CA 2026 ramené à 12 mois : {euros(ramene)}.")
    print(f"Pour être exonéré de CFE en 2027 ET 2028 (année de référence 2026), le CA HT 2026 doit rester ≤ {euros(plafond_2026)}.")
    print("  → OK : exonération 2027 et 2028 par le seuil de 5 000 €." if ca_2026 <= plafond_2026 else "  → DÉPASSÉ : CFE minimum possible en 2027 (base réduite de moitié) et 2028, sauf exonération ZFRR+ votée (art. 1466 G).")


if __name__ == "__main__":
    verifier_fraicheur()
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "--cfe2026":
        cfe_2026(float(args[1]))
    else:
        simuler(float(args[0]), acre="--sans-acre" not in args)
