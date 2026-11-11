"""Tests de suivi.py (python3 -m unittest outils/prospects/test_suivi.py). Entreprises fictives, aucun réseau."""

import json
import os
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import suivi


def feuille_test():
    f = {"maj": "", "entreprises": []}
    a = suivi.ajouter(f, "SARL Maçonnerie Test", "123456789", "05 45 00 00 01", "Ville-Test", "maçon")
    b = suivi.ajouter(f, "Garage Essai", "", "+33 5 45 00 00 02", "Bourg-Test", "garage")
    c = suivi.ajouter(f, "Boulangerie Exemple", "987654321", "", "Ville-Test", "boulangerie")
    suivi.noter_appel(a, "03/11/2026", "pas_de_reponse")
    suivi.noter_appel(a, "10/11/2026", "rappeler", rappel_le="12/11/2026")
    suivi.noter_appel(b, "03/11/2026", "refus_definitif")
    suivi.noter_appel(c, "10/11/2026", "demo_demandee", demo_le="17/11/2026")
    return f


class Suivi(unittest.TestCase):
    def test_une_ligne_par_entreprise(self):
        f = feuille_test()
        suivi.ajouter(f, "Maçonnerie Test")                       # même nom sans forme juridique
        suivi.ajouter(f, "Autre nom", telephone="0545000002")     # même téléphone, autre écriture
        suivi.ajouter(f, "Encore autre", siren="987 654 321")     # même SIREN
        self.assertEqual(len(f["entreprises"]), 3)

    def test_etat_et_prochaine_action(self):
        f = feuille_test()
        a, b, c = f["entreprises"]
        self.assertEqual((suivi.etat(a), a["prochaine_date"]), ("rappeler", "12/11/2026"))
        self.assertEqual(suivi.etat(b), "refus_definitif")
        self.assertEqual((suivi.etat(c), c["prochaine_date"]), ("demo_demandee", "17/11/2026"))
        self.assertEqual([x["date"] for x in a["appels"]], ["03/11/2026", "10/11/2026"])

    def test_refus_definitif_ne_se_rappelle_jamais(self):
        f = feuille_test()
        with self.assertRaises(SystemExit):
            suivi.noter_appel(f["entreprises"][1], "12/11/2026", "pas_de_reponse")
        self.assertEqual(len(f["entreprises"][1]["appels"]), 1)

    def test_champs_obligatoires(self):
        f = feuille_test()
        a = f["entreprises"][0]
        for resultat in ("rappeler", "demo_demandee", "interesse", "autre"):
            with self.assertRaises(SystemExit):
                suivi.noter_appel(a, "12/11/2026", resultat)
        with self.assertRaises(SystemExit):
            suivi.noter_appel(a, "2026-11-12", "pas_de_reponse")

    def test_refus_dans_un_lot(self):
        f = feuille_test()
        lot = {"prospects": [{"num": 1, "nom": "GARAGE ESSAI", "telephone": "05 45 00 00 02"},
                             {"num": 2, "nom": "Boulangerie Exemple", "siren": "987654321"},
                             {"num": 3, "nom": "Inconnu", "telephone": "05 45 00 00 99"}]}
        self.assertEqual(suivi.refus_du_lot(lot, f), [(1, "GARAGE ESSAI")])

    def test_ne_plus_appeler_bloque_aussi(self):
        f = feuille_test()
        suivi.ajouter(f, "Restaurant Fermé Test", ne_plus_appeler="entreprise fermée")
        suivi.ajouter(f, "Plombier À Venir", prochaine="à appeler", jour="12/11/2026")
        lot = {"prospects": [{"num": 4, "nom": "RESTAURANT FERME TEST"}, {"num": 5, "nom": "Plombier à venir"}]}
        self.assertEqual(suivi.refus_du_lot(lot, f), [(4, "RESTAURANT FERME TEST")])
        with self.assertRaises(SystemExit):
            suivi.noter_appel(f["entreprises"][3], "12/11/2026", "pas_de_reponse")
        self.assertEqual(f["entreprises"][4]["prochaine_date"], "12/11/2026")
        self.assertEqual(len(suivi.lignes(f, a_faire=True)), 3)

    def test_tri_et_export(self):
        f = feuille_test()
        tableau = suivi.lignes(f)
        self.assertEqual([l["Entreprise"] for l in tableau], ["SARL Maçonnerie Test", "Boulangerie Exemple", "Garage Essai"])
        self.assertEqual(len(suivi.lignes(f, a_faire=True)), 2)
        with tempfile.TemporaryDirectory() as d:
            chemin, n = suivi.exporter(f, d)
            self.assertEqual(n, 3)
            self.assertIn("REFUS DÉFINITIF", open(chemin, encoding="utf-8").read())

    def test_jamais_dans_le_depot(self):
        with self.assertRaises(SystemExit):
            suivi.enregistrer(feuille_test(), os.path.join(ICI, "suivi-prospects.json"))
        self.assertFalse(os.path.exists(os.path.join(ICI, "suivi-prospects.json")))

    def test_garde_fou_de_la_fiche_d_appels(self):
        """fiche_appel.py s'arrête avant tout appel réseau : refus dans le lot, ou feuille absente."""
        with tempfile.TemporaryDirectory() as d:
            lot = os.path.join(d, "lot.json")
            json.dump({"date": "12/11/2026", "titre": "essai", "prospects": [
                {"num": 1, "nom": "Garage Essai", "telephone": "05 45 00 00 02", "metier": "garage",
                 "commune": "Bourg-Test", "google_statut": "ouvert, fiche Google vue le 12/11"}]}, open(lot, "w"))
            env = {k: v for k, v in os.environ.items() if k != "DIG16_SUIVI"}
            r = subprocess.run([sys.executable, os.path.join(ICI, "fiche_appel.py"), lot, os.path.join(d, "sortie")],
                               capture_output=True, text=True, env=env)
            self.assertIn("feuille de suivi des prospects introuvable", r.stderr)
            suivi.enregistrer(feuille_test(), os.path.join(d, suivi.NOM_FICHIER))
            r = subprocess.run([sys.executable, os.path.join(ICI, "fiche_appel.py"), lot, os.path.join(d, "sortie")],
                               capture_output=True, text=True, env=env)
            self.assertIn("refus définitif ou entreprise à ne plus appeler dans le lot", r.stderr)
            self.assertNotEqual(r.returncode, 0)
            self.assertFalse(os.path.exists(os.path.join(d, "sortie", "fiches-appel.pdf")))


if __name__ == "__main__":
    unittest.main()
