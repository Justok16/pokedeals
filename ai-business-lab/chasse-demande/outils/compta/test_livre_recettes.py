"""Tests du livre des recettes (python3 -m unittest outils/compta/test_livre_recettes.py). Données fictives."""

import csv
import os
import sys
import tempfile
import unittest
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import livre_recettes as lr

ENTETE = ["date_encaissement", "numero_facture", "client", "type_client", "pays", "nature", "montant_eur", "mode"]


def fichier(lignes, dossier):
    p = os.path.join(dossier, "recettes.csv")
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(ENTETE)
        w.writerows(lignes)
    return p


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="livre-")

    def test_lecture_et_tri(self):
        p = fichier([["2026-12-05", "F2026-002", "Client B", "pro", "FR", "service", "49", "prelevement"],
                     ["2026-11-05", "F2026-001", "Client A", "pro", "", "service", "49,00", "virement"]], self.tmp)
        lignes, alertes = lr.lire(p)
        self.assertEqual(alertes, [])
        self.assertEqual([r["numero_facture"] for r in lignes], ["F2026-001", "F2026-002"])
        self.assertEqual(lignes[0]["pays"], "FR")
        self.assertEqual(lignes[0]["montant"], Decimal("49.00"))

    def test_erreurs_de_saisie(self):
        p = fichier([["05/11/2026", "F1", "A", "pro", "FR", "service", "49", "virement"],
                     ["2026-11-06", "", "", "client", "FR", "conseil", "49", "paypal"],
                     ["2026-11-07", "F3", "C", "pro", "FR", "service", "abc", "virement"]], self.tmp)
        lignes, alertes = lr.lire(p)
        texte = " | ".join(alertes)
        for attendu in ["date invalide", "mode de règlement inconnu", "type de client inconnu", "nature inconnue",
                        "numéro de facture", "origine de la recette", "montant invalide"]:
            self.assertIn(attendu, texte)
        self.assertEqual(len(lignes), 1)

    def test_colonnes_absentes(self):
        p = os.path.join(self.tmp, "x.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("date,montant\n2026-11-01,10\n")
        _, alertes = lr.lire(p)
        self.assertTrue(alertes and "colonnes absentes" in alertes[0])

    def test_seuils_franchise(self):
        base, majore = Decimal(37500), Decimal(41250)
        def l(m):
            return [{"date": date(2026, 6, 1), "montant": Decimal(m), "numero_facture": "F1"}]
        self.assertEqual(lr.controler(l("1000"), 2026, base, majore)[0], [])
        self.assertTrue(any("80 %" in i for i in lr.controler(l("31000"), 2026, base, majore)[1]))
        self.assertIn("seuil de base", lr.controler(l("38000"), 2026, base, majore)[0][0])
        self.assertIn("seuil majoré", lr.controler(l("42000"), 2026, base, majore)[0][0])

    def test_paiement_partiel_et_acompte(self):
        lignes = [{"date": date(2026, 11, 1), "montant": Decimal(100), "numero_facture": "F9"},
                  {"date": date(2026, 12, 1), "montant": Decimal(50), "numero_facture": "F9"}]
        alertes, infos, ca = lr.controler(lignes, 2026, Decimal(37500), Decimal(41250))
        self.assertEqual(alertes, [])
        self.assertEqual(ca, Decimal(150))
        self.assertTrue(any("2 encaissements" in i for i in infos))

    def test_bimestres_et_echeances(self):
        self.assertEqual(lr.bimestre(date(2027, 9, 15)), 5)
        self.assertEqual(lr.bimestre(date(2027, 12, 31)), 6)
        self.assertEqual(lr.echeance_bimestre(2027, 5), (2027, 11))
        self.assertEqual(lr.echeance_bimestre(2027, 6), (2028, 1))

    def test_e_reporting_flux_separes(self):
        lignes = [
            {"date": date(2027, 8, 31), "montant": Decimal(49), "nature": "service", "type_client": "pro", "pays": "FR"},
            {"date": date(2027, 9, 2), "montant": Decimal(49), "nature": "service", "type_client": "pro", "pays": "FR"},
            {"date": date(2027, 9, 3), "montant": Decimal(20), "nature": "service", "type_client": "particulier", "pays": "FR"},
            {"date": date(2027, 10, 4), "montant": Decimal(30), "nature": "vente", "type_client": "pro", "pays": "BE"},
        ]
        paiement, transaction = lr.e_reporting(lignes)
        self.assertEqual(sum(paiement[(2027, 5)].values()), Decimal(69))   # services seulement, après le 01/09/2027
        self.assertEqual(sum(transaction[(2027, 5)].values()), Decimal(50))  # particulier + étranger
        self.assertNotIn((2027, 4), paiement)                                  # avant l'obligation : rien

    def test_refus_dans_le_depot(self):
        depot = os.path.dirname(os.path.abspath(__file__))
        self.assertTrue(lr.dans_le_depot(depot))
        self.assertFalse(lr.dans_le_depot(self.tmp))
        code = lr.main(["x", os.path.join(depot, "r.csv"), "--sortie", self.tmp])
        self.assertEqual(code, 2)

    def test_bout_en_bout(self):
        p = fichier([["2026-11-05", "F2026-001", "Client A", "pro", "FR", "service", "49", "prelevement"],
                     ["2026-12-05", "F2026-002", "Client A", "pro", "FR", "service", "49", "prelevement"]], self.tmp)
        sortie = os.path.join(self.tmp, "sortie")
        code = lr.main(["x", p, "--sortie", sortie, "--annee", "2026"])
        self.assertEqual(code, 0)
        with open(os.path.join(sortie, "livre-recettes-2026.csv"), encoding="utf-8") as f:
            contenu = f.read()
        self.assertIn("T4 : 98.00", contenu)
        self.assertIn("TOTAL ANNUEL,98.00", contenu)
        with open(os.path.join(sortie, "controle-2026.md"), encoding="utf-8") as f:
            self.assertIn("aucune", f.read())


if __name__ == "__main__":
    unittest.main()
