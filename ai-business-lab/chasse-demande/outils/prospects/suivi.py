#!/usr/bin/env python3
"""Feuille unique et privée de suivi des prospects : état et prochaine action par entreprise ; bloque les refus.

Décision de l'utilisateur du 11/11/2026 (audit lot B3 : « un seul endroit avec, par prospect, un état et une date
de relance »).

Une ligne par entreprise : date de chaque appel, résultat, prochaine action. La feuille est PRIVÉE : un fichier
JSON dans le scratchpad, copié au Drive « Dig » (jamais dans ce dépôt, qui est public). Cet outil ne contient
aucune donnée.

Résultats possibles d'un appel :
  pas_de_reponse   personne n'a décroché (ou répondeur, sans message)
  message_laisse   message laissé sur le répondeur
  rappeler         la personne demande à être rappelée (--rappel-le JJ/MM/AAAA obligatoire)
  demo_demandee    une démo est demandée (--demo-le JJ/MM/AAAA obligatoire : date promise ou du rendez-vous)
  interesse        échange utile, suite à préparer (--prochaine "…" obligatoire)
  refus_definitif  « non » : NE JAMAIS RAPPELER (définitif : aucun appel ne peut plus être ajouté)
  autre            tout le reste (--note obligatoire)

Usage (le fichier de suivi vient en premier ; s'il n'existe pas, « ajouter » le crée) :
  python3 suivi.py <suivi.json> ajouter --nom "…" [--siren 9 chiffres] [--telephone "…"] [--commune "…"] [--metier "…"]
                                        [--prochaine "…"] [--date JJ/MM/AAAA] [--ne-plus-appeler "raison"]
  python3 suivi.py <suivi.json> appel (--siren … | --telephone … | --nom "…") --date JJ/MM/AAAA --resultat <code>
                                      [--rappel-le JJ/MM/AAAA] [--demo-le JJ/MM/AAAA] [--prochaine "…"] [--note "…"]
  python3 suivi.py <suivi.json> liste [--a-faire]          tableau, les actions les plus proches en premier
  python3 suivi.py <suivi.json> exporter <dossier privé>   suivi-prospects.csv (pour une feuille Google du Drive « Dig »)
  python3 suivi.py <suivi.json> verifier-lot <lot.json>    code 2 si le lot contient un refus définitif

`--ne-plus-appeler "raison"` sert aux entreprises à ne plus appeler sans qu'un « non » ait été dit au téléphone
(entreprise fermée ou radiée, relais déjà contacté par écrit) : elles sont bloquées dans les lots comme un refus.
`fiche_appel.py` appelle `controler_lot()` : un prospect en refus définitif ou « à ne plus appeler » ne peut plus
sortir dans un lot.
Rapprochement d'une entreprise : SIREN, sinon 9 derniers chiffres du téléphone (« +33 5 45… » = « 05 45… »),
sinon nom sans accents ni forme juridique.
"""

import argparse
import csv
import datetime
import json
import os
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.abspath(os.path.join(ICI, "..", "..", "..", ".."))
NOM_FICHIER = "suivi-prospects.json"
RESULTATS = {
    "pas_de_reponse": "pas de réponse",
    "message_laisse": "message laissé",
    "rappeler": "rappeler",
    "demo_demandee": "démo demandée",
    "interesse": "intéressé",
    "refus_definitif": "REFUS DÉFINITIF : ne jamais rappeler",
    "autre": "autre",
}
REFUS = "refus_definitif"


def hors_depot(chemin):
    if os.path.realpath(chemin).startswith(os.path.realpath(DEPOT) + os.sep):
        sys.exit("Refusé : la feuille de suivi est privée (scratchpad ou Drive « Dig »), jamais dans le dépôt public.")


def date(texte):
    """« 03/11/2026 » → date ; arrêt clair sinon (jamais de date devinée)."""
    try:
        return datetime.datetime.strptime(texte.strip(), "%d/%m/%Y").date()
    except ValueError:
        sys.exit(f"Date « {texte} » invalide : format JJ/MM/AAAA.")


def cle_nom(nom):
    t = unicodedata.normalize("NFD", (nom or "").lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"\b(sarl|sas|sasu|eurl|sci|ei|eirl|snc|ets|etablissements?|entreprise|societe|ste)\b", " ", t)
    return re.sub(r"[^a-z0-9]+", "", t)


def cle_tel(tel):
    chiffres = re.sub(r"\D", "", tel or "")
    return chiffres[-9:] if len(chiffres) >= 9 else ""


def cle_siren(siren):
    chiffres = re.sub(r"\D", "", str(siren or ""))
    return chiffres[:9] if len(chiffres) >= 9 else ""


def charger(chemin):
    if not os.path.exists(chemin):
        return {"maj": "", "entreprises": []}
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def enregistrer(feuille, chemin):
    hors_depot(chemin)
    feuille["maj"] = datetime.date.today().strftime("%d/%m/%Y")
    os.makedirs(os.path.dirname(os.path.abspath(chemin)), exist_ok=True)
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(feuille, f, ensure_ascii=False, indent=1)
    os.replace(tmp, chemin)


def trouver(feuille, nom=None, siren=None, telephone=None):
    """Entreprises de la feuille qui correspondent (SIREN, puis téléphone, puis nom)."""
    s, t, n = cle_siren(siren), cle_tel(telephone), cle_nom(nom)
    trouvees = []
    for ent in feuille["entreprises"]:
        s2 = cle_siren(ent.get("siren"))
        if s and s2 and s != s2:
            continue  # deux SIREN connus et différents : deux entreprises, même si le nom ou le téléphone se ressemblent
        if (s and s == s2) or (t and t == cle_tel(ent.get("telephone"))) or (n and n == cle_nom(ent.get("nom"))):
            trouvees.append(ent)
    return trouvees


def etat(ent):
    """État actuel : un refus définitif l'emporte toujours ; sinon le résultat du dernier appel."""
    appels = ent.get("appels", [])
    if any(a["resultat"] == REFUS for a in appels):
        return REFUS
    return appels[-1]["resultat"] if appels else "jamais_appele"


def bloque(ent):
    """Vrai si l'entreprise ne doit plus jamais sortir dans un lot d'appels."""
    return etat(ent) == REFUS or bool(ent.get("ne_plus_appeler"))


def ajouter(feuille, nom, siren="", telephone="", commune="", metier="", prochaine="", jour="", ne_plus_appeler=""):
    if not (nom or "").strip():
        sys.exit("Nom de l'entreprise obligatoire.")
    if jour:
        date(jour)
    deja = trouver(feuille, nom, siren, telephone)
    if deja:
        ent = deja[0]
        for champ, valeur in (("siren", cle_siren(siren)), ("telephone", telephone), ("commune", commune), ("metier", metier)):
            if valeur and not ent.get(champ):
                ent[champ] = valeur
    else:
        ent = {"nom": nom.strip(), "siren": cle_siren(siren), "telephone": telephone.strip(), "commune": commune.strip(),
               "metier": metier.strip(), "appels": [], "prochaine_action": "", "prochaine_date": ""}
        feuille["entreprises"].append(ent)
    if ne_plus_appeler:
        ent["ne_plus_appeler"] = ne_plus_appeler.strip()
        ent["prochaine_action"], ent["prochaine_date"] = "aucune : ne plus appeler (" + ne_plus_appeler.strip() + ")", ""
    elif prochaine and not bloque(ent):
        ent["prochaine_action"], ent["prochaine_date"] = prochaine, jour
    return ent


def noter_appel(ent, jour, resultat, rappel_le="", demo_le="", prochaine="", note=""):
    if resultat not in RESULTATS:
        sys.exit(f"Résultat « {resultat} » inconnu. Choix : {', '.join(RESULTATS)}.")
    date(jour)
    if etat(ent) == REFUS:
        sys.exit(f"REFUSÉ : « {ent['nom']} » a dit non (refus définitif) : on ne rappelle jamais, aucun appel ajouté.")
    if ent.get("ne_plus_appeler") and resultat != REFUS:
        sys.exit(f"REFUSÉ : « {ent['nom']} » est à ne plus appeler ({ent['ne_plus_appeler']}) : aucun appel ajouté.")
    if resultat == "rappeler" and not rappel_le:
        sys.exit("« rappeler » : --rappel-le JJ/MM/AAAA obligatoire.")
    if resultat == "demo_demandee" and not demo_le:
        sys.exit("« demo_demandee » : --demo-le JJ/MM/AAAA obligatoire.")
    if resultat == "interesse" and not prochaine:
        sys.exit("« interesse » : --prochaine \"…\" obligatoire (la suite à préparer).")
    if resultat == "autre" and not note:
        sys.exit("« autre » : --note obligatoire.")
    for jour_cite in (rappel_le, demo_le):
        if jour_cite:
            date(jour_cite)  # toute date est contrôlée AVANT d'écrire quoi que ce soit
    appel = {"date": jour, "resultat": resultat}
    if note:
        appel["note"] = note
    ent.setdefault("appels", []).append(appel)
    ent["appels"].sort(key=lambda a: date(a["date"]))
    if ent["appels"][-1] is not appel and resultat != REFUS:
        return ent  # appel plus ancien saisi après coup : la prochaine action reste celle de l'appel le plus récent
    if resultat == REFUS:
        ent["prochaine_action"], ent["prochaine_date"] = "aucune : ne jamais rappeler", ""
    elif resultat == "rappeler":
        date(rappel_le)
        ent["prochaine_action"], ent["prochaine_date"] = prochaine or "rappeler", rappel_le
    elif resultat == "demo_demandee":
        date(demo_le)
        ent["prochaine_action"], ent["prochaine_date"] = prochaine or "démo à montrer (validée d'abord par l'utilisateur)", demo_le
    elif prochaine:
        ent["prochaine_action"], ent["prochaine_date"] = prochaine, rappel_le
        if rappel_le:
            date(rappel_le)
    elif resultat in ("pas_de_reponse", "message_laisse"):
        ent["prochaine_action"], ent["prochaine_date"] = "à rappeler au prochain créneau (sans nouveau message)", rappel_le
    else:  # « autre » sans suite précisée : ne pas laisser une ancienne action périmée
        ent["prochaine_action"], ent["prochaine_date"] = "à préciser (voir la note du dernier appel)", ""
    return ent


def lignes(feuille, a_faire=False):
    """Lignes du tableau, triées : actions datées les plus proches, puis sans date, puis refus."""
    sortie = []
    for ent in feuille["entreprises"]:
        e = etat(ent)
        if a_faire and bloque(ent):
            continue
        appels = ent.get("appels", [])
        sortie.append({
            "Entreprise": ent["nom"], "Commune": ent.get("commune", ""), "Métier": ent.get("metier", ""),
            "Téléphone": ent.get("telephone", ""), "SIREN": ent.get("siren", ""),
            "Appels (date : résultat)": " ; ".join(
                f"{a['date']} : {RESULTATS[a['resultat']]}" + (f" ({a['note']})" if a.get("note") else "") for a in appels),
            "État": ("NE PLUS APPELER : " + ent["ne_plus_appeler"]) if ent.get("ne_plus_appeler") and e != REFUS
            else RESULTATS.get(e, "jamais appelé"),
            "Prochaine action": ent.get("prochaine_action", ""), "Date": ent.get("prochaine_date", ""),
        })

    def ordre(l):
        if l["État"] == RESULTATS[REFUS] or l["État"].startswith("NE PLUS APPELER"):
            return (2, datetime.date.max)
        return (0, date(l["Date"])) if l["Date"] else (1, datetime.date.max)
    return sorted(sortie, key=ordre)


def exporter(feuille, dossier):
    hors_depot(os.path.join(dossier, "x"))
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, "suivi-prospects.csv")
    tableau = lignes(feuille)
    colonnes = ["Entreprise", "Commune", "Métier", "Téléphone", "SIREN", "Appels (date : résultat)", "État",
                "Prochaine action", "Date"]
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colonnes)
        w.writeheader()
        w.writerows(tableau)
    return chemin, len(tableau)


def refus_du_lot(lot, feuille):
    """Prospects du lot (format de fiche_appel.py) en refus définitif ou « à ne plus appeler » dans la feuille."""
    interdits = []
    for p in lot.get("prospects", []):
        for ent in trouver(feuille, p.get("nom"), p.get("siren"), p.get("telephone")):
            if bloque(ent):
                interdits.append((p.get("num", "?"), p.get("nom", "?")))
                break
    return interdits


def chercher_feuille(*dossiers):
    """Feuille de suivi : variable DIG16_SUIVI, sinon suivi-prospects.json dans les dossiers donnés ou leur parent."""
    voulu = os.environ.get("DIG16_SUIVI", "")
    if voulu and not os.path.isfile(voulu):
        sys.exit(f"ALERTE : DIG16_SUIVI désigne un fichier absent ({voulu}) : corriger la variable ou la retirer.")
    candidats = [voulu]
    for d in dossiers:
        d = os.path.abspath(d)
        candidats += [os.path.join(d, NOM_FICHIER), os.path.join(os.path.dirname(d), NOM_FICHIER),
                      os.path.join(os.path.dirname(os.path.dirname(d)), NOM_FICHIER)]
    return next((c for c in candidats if c and os.path.isfile(c)), None)


def controler_lot(lot, *dossiers, sans_suivi=False):
    """Garde-fou de fiche_appel.py : arrêt si un refus définitif est dans le lot ; arrêt aussi si la feuille est
    introuvable (leçon du 11/11 : un garde-fou qui dépend d'un fichier privé ne doit pas être muet), sauf
    `sans_suivi=True` demandé explicitement."""
    chemin = chercher_feuille(*dossiers)
    if not chemin:
        if sans_suivi:
            print("AVERTISSEMENT : feuille de suivi absente, refus définitifs NON contrôlés (--sans-suivi).")
            return None
        sys.exit("ALERTE : feuille de suivi des prospects introuvable (suivi-prospects.json). La reprendre du Drive "
                 "« Dig » (document « DIG16 – suivi-prospects.json (PRIVÉ) ») et la poser à côté du lot ou dans "
                 "DIG16_SUIVI ; à défaut seulement, relancer avec --sans-suivi après avoir relu les refus dans ETAT.md.")
    interdits = refus_du_lot(lot, charger(chemin))
    if interdits:
        sys.exit("ALERTE : refus définitif ou entreprise à ne plus appeler dans le lot, à retirer : "
                 + ", ".join(f"n° {n} {nom}" for n, nom in interdits))
    return chemin


def main():
    ap = argparse.ArgumentParser(description="Feuille unique de suivi des prospects (privée).")
    ap.add_argument("suivi")
    sp = ap.add_subparsers(dest="commande", required=True)
    a = sp.add_parser("ajouter")
    a.add_argument("--nom", required=True)
    for champ in ("siren", "telephone", "commune", "metier", "prochaine", "date", "ne-plus-appeler"):
        a.add_argument("--" + champ, default="")
    b = sp.add_parser("appel")
    for champ in ("nom", "siren", "telephone", "rappel-le", "demo-le", "prochaine", "note"):
        b.add_argument("--" + champ, default="")
    b.add_argument("--date", required=True)
    b.add_argument("--resultat", required=True, choices=list(RESULTATS))
    c = sp.add_parser("liste")
    c.add_argument("--a-faire", action="store_true")
    d = sp.add_parser("exporter")
    d.add_argument("dossier")
    v = sp.add_parser("verifier-lot")
    v.add_argument("lot")
    args = ap.parse_args()
    hors_depot(args.suivi)
    feuille = charger(args.suivi)
    if args.commande == "ajouter":
        ajouter(feuille, args.nom, args.siren, args.telephone, args.commune, args.metier, args.prochaine, args.date,
                args.ne_plus_appeler)
        enregistrer(feuille, args.suivi)
        print(f"{len(feuille['entreprises'])} entreprise(s) dans la feuille.")
    elif args.commande == "appel":
        trouvees = trouver(feuille, args.nom, args.siren, args.telephone)
        if len(trouvees) != 1:
            sys.exit(f"{len(trouvees)} entreprise(s) trouvée(s) : préciser (--siren ou --telephone), ou « ajouter » d'abord.")
        ent = noter_appel(trouvees[0], args.date, args.resultat, args.rappel_le, args.demo_le, args.prochaine, args.note)
        enregistrer(feuille, args.suivi)
        print(f"Noté : {ent['nom']} → {RESULTATS[etat(ent)]} ; prochaine action : "
              f"{ent['prochaine_action'] or '—'} {ent['prochaine_date']}".rstrip())
    elif args.commande == "liste":
        for l in lignes(feuille, args.a_faire):
            print(f"{l['Date'] or '—':<10} | {l['Entreprise']} ({l['Commune']}) | {l['État']} | {l['Prochaine action']}"
                  f" | {l['Appels (date : résultat)']}")
    elif args.commande == "exporter":
        chemin, n = exporter(feuille, args.dossier)
        print(f"{n} ligne(s) : {chemin}")
    elif args.commande == "verifier-lot":
        interdits = refus_du_lot(json.load(open(args.lot, encoding="utf-8")), feuille)
        if interdits:
            print("REFUS DÉFINITIF ou à ne plus appeler, dans le lot :", ", ".join(f"n° {n} {nom}" for n, nom in interdits))
            sys.exit(2)
        print("Lot sans refus définitif.")


if __name__ == "__main__":
    main()
