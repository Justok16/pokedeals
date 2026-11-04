"""Tests de repreneurs.py (python3 -m unittest outils/prospects/test_repreneurs.py). Annonces fictives, aucun réseau."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repreneurs as rp


def annonce(activite, origine="siège et établissement principal acquis par achat au prix stipulé de 120000.00 euros",
            commercant="ACHETEUR TEST, VENDEUR TEST"):
    return {
        "dateparution": "2026-10-31", "commercant": commercant, "ville": "Ville-Test", "cp": "16000",
        "registre": ["123456789", "123 456 789", "987654321", "987 654 321"], "numerodepartement": "16",
        "url_complete": "https://www.bodacc.fr/pages/annonces-commerciales-detail/?q.id=id:TEST",
        "listeetablissements": json.dumps({"etablissement": {"origineFonds": origine, "activite": activite,
                                           "adresse": {"numeroVoie": "1", "typeVoie": "Rue", "nomVoie": "de l'Essai",
                                                       "codePostal": "16000", "ville": "Ville-Test"}}}),
        "acte": json.dumps({"dateCommencementActivite": "2026-10-23",
                            "vente": {"categorieVente": "Mise en activité d'une société suite à achat"}}),
    }


class Tests(unittest.TestCase):
    def test_rachat_retenu(self):
        f = rp.lire_annonce(annonce("boulangerie pâtisserie traiteur"))
        self.assertEqual(f["acheteur"], "ACHETEUR TEST")
        self.assertEqual(f["siren_acheteur"], "123456789")
        self.assertEqual(f["prix_fonds"], "120000.00")
        self.assertEqual(f["adresse"], "1 Rue de l'Essai")
        self.assertFalse(f["exclu"])

    def test_secteurs_exclus(self):
        for act in ["bar brasserie licence IV", "débit de boissons", "tabac presse", "pharmacie", "agence immobilière",
                    "vente de CBD", "cave à vins", "armurerie"]:
            self.assertTrue(rp.lire_annonce(annonce(act))["exclu"], act)
        for act in ["restaurant traditionnel", "plomberie chauffage", "coiffure mixte", "garage automobile"]:
            self.assertFalse(rp.lire_annonce(annonce(act))["exclu"], act)

    def test_pas_un_rachat(self):
        a = annonce("plomberie", origine="fonds créé")
        a["acte"] = json.dumps({"vente": {"categorieVente": "Location-gérance"}})
        self.assertIsNone(rp.lire_annonce(a))
        a2 = annonce("")
        self.assertIsNone(rp.lire_annonce(a2))

    def test_champs_absents(self):
        a = annonce("menuiserie")
        a["registre"] = "['111222333', '111 222 333']"
        self.assertEqual(rp.lire_annonce(a)["siren_acheteur"], "111222333")
        a["listeetablissements"] = "None"
        self.assertIsNone(rp.lire_annonce(a))

    def test_refus_dans_le_depot(self):
        self.assertEqual(rp.main(["x", "--sortie", os.path.dirname(os.path.abspath(__file__))]), 2)
        self.assertFalse(rp.dans_un_depot(tempfile.mkdtemp()))


if __name__ == "__main__":
    unittest.main()
