"""Tri des réponses d'éditeurs avec Jev (TypeSafe AI, https://docs.typesafe.ai).

Pour chaque email reçu (texte brut), une question Choice classe la réponse et
une question Noul détecte une demande d'information à traiter vite.
La clé est lue dans la variable d'environnement TYPESAFE_API_KEY (jamais dans
le dépôt). Sans clé, repli sur des règles simples par mots-clés.

Usage :
    python3 jev_trier_reponses.py fichier1.txt [fichier2.txt ...]
    echo "texte" | python3 jev_trier_reponses.py -
Sortie : une ligne JSON par email.
"""
import json
import os
import re
import sys
import urllib.request

API = os.environ.get("TYPESAFE_BASE_URL", "https://api.typesafe.ai") + "/v1/systemone"

# Questions et seuils regroupés ici pour relecture (conseil de la doc TypeSafe).
QUESTIONS = {
    "categorie": {
        "type": "choice",
        "instructions": "An app vendor answered our offer to take over their "
                        "Atlassian Connect app. What kind of reply is this?",
        "criteria": {
            "refus": "Declines the offer, not interested, or says they are migrating the app themselves",
            "interesse": "Open to discussing, asks for a call, terms, or next steps",
            "question": "Asks who we are, for details, references or clarification, without deciding",
            "accuse_reception": "Automatic acknowledgement that a support ticket was received",
            "autre": "Anything else (out of office, bounce, unrelated)",
        },
    },
    "a_traiter": {
        "type": "noul",
        "instructions": "Does this reply need a human answer from us?",
    },
}
SEUIL_CONFIANCE = 0.6  # en dessous : l'utilisateur relit


def jev(texte, cle):
    corps = json.dumps({"state": texte[:20000], "model": "jev-latest",
                        "questions": QUESTIONS}).encode()
    req = urllib.request.Request(API, data=corps, headers={
        "Authorization": f"Bearer {cle}", "Content-Type": "application/json"})
    rep = json.load(urllib.request.urlopen(req, timeout=30))["answers"]
    c = rep["categorie"]
    return {"categorie": c["choice"], "confiance": round(c["confidence"], 2),
            "a_traiter": round(rep["a_traiter"]["noul"], 2),
            "relire": c["confidence"] < SEUIL_CONFIANCE, "moteur": "jev"}


def regles(texte):
    t = texte.lower()
    if re.search(r"not interested|decline|no thanks|we (are|will be) migrat|already (migrat|working)", t):
        cat = "refus"
    elif re.search(r"just confirming|request .*received|auto-?reply|we have received", t):
        cat = "accuse_reception"
    elif re.search(r"interested|let'?s talk|call|schedule|terms|price|offer", t):
        cat = "interesse"
    elif "?" in t:
        cat = "question"
    else:
        cat = "autre"
    return {"categorie": cat, "confiance": None,
            "a_traiter": cat in ("interesse", "question"), "relire": True, "moteur": "regles"}


def main():
    cle = os.environ.get("TYPESAFE_API_KEY")
    for chemin in sys.argv[1:] or ["-"]:
        texte = sys.stdin.read() if chemin == "-" else open(chemin, encoding="utf-8").read()
        try:
            res = jev(texte, cle) if cle else regles(texte)
        except Exception as e:  # réseau, quota : repli sans bloquer la routine
            res = regles(texte) | {"erreur_jev": str(e)[:120]}
        print(json.dumps({"source": chemin} | res, ensure_ascii=False))


if __name__ == "__main__":
    main()
