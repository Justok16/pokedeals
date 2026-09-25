"""Aiguilleur des réponses d'éditeurs — Jev (TypeSafe AI) cantonné au tri.

Rôle de Jev : UNIQUEMENT classer chaque email dans une catégorie fermée et
dire avec quelle confiance. Il ne rédige rien et ne décide d'aucun
engagement. Le code applique ensuite un aiguillage à trois voies
(motif « confidence-gated routing », https://docs.typesafe.ai/patterns/confidence-routing.md) :

  auto   : confiance élevée ET catégorie sans enjeu → action automatique
  claude : confiance moyenne → un modèle classique (Claude) relit et décide
  humain : confiance faible, OU catégorie qui engage → l'utilisateur

Accès à Jev, au choix :
  - relais Vercel (sans clé, jeton OIDC) : variable JEV_COOKIES = chemin d'un
    fichier de cookies obtenu avec l'outil get_access_to_vercel_url du
    connecteur Vercel (lien valable 23 h) ;
  - ou clé : variable d'environnement TYPESAFE_API_KEY (jamais dans le dépôt).
Sans clé ou si l'API échoue : repli sur des règles simples, toujours
aiguillées vers « claude » (jamais d'action automatique sans Jev).

Usage :
    python3 jev_trier_reponses.py fichier1.txt [...]
    echo "texte" | python3 jev_trier_reponses.py -
Sortie : une ligne JSON par email.
"""
import json
import os
import re
import sys
import urllib.request

API = os.environ.get("TYPESAFE_BASE_URL", "https://api.typesafe.ai") + "/v1/systemone"
RELAIS = "https://relais-dig-justok1.vercel.app/api/jev"

# --- Tout ce qu'un humain doit relire est ici : catégories, actions, seuils ---

CATEGORIES = {
    "accuse_reception": "Automatic acknowledgement that a support ticket or email was received; no human wrote it",
    "rejet_adresse": "Delivery failure or the request could not be created (bounce, invalid address)",
    "absence": "Out-of-office or vacation auto-reply",
    "refus": "A person declines or thanks without accepting: not interested, or they say they will do the migration themselves (even 'soon'), or keep or sell the app",
    "question": "A person asks who we are, for details or clarification, without accepting or declining",
    "interet": "A person is open to handing over the app: wants to talk, asks for terms, a call, or next steps about the takeover",
    "hors_sujet": "Unrelated to our offer (marketing, spam, other topic)",
}

# Action automatique autorisée par catégorie (None = jamais automatique).
ACTIONS_AUTO = {
    "accuse_reception": "archiver",
    "absence": "archiver et relancer après le retour",
    "rejet_adresse": "chercher une autre adresse publique",
    "hors_sujet": "archiver",
    "refus": "noter le refus, remercier, ne pas relancer",
    "question": None,   # une réponse engage l'image de l'utilisateur → Claude au minimum
    "interet": None,    # peut mener à un accord → toujours l'humain
}
TOUJOURS_HUMAIN = {"interet"}

SEUIL_AUTO = 0.85     # au-dessus : action automatique si la catégorie le permet
SEUIL_CLAUDE = 0.55   # entre les deux : relecture par Claude ; en dessous : humain

# -----------------------------------------------------------------------------

QUESTIONS = {
    "categorie": {
        "type": "choice",
        "instructions": "We offered an app vendor to take over their Atlassian "
                        "Connect app. Classify this email received in reply.",
        "criteria": CATEGORIES,
    },
}


def aiguiller(categorie, confiance):
    if categorie in TOUJOURS_HUMAIN:
        return "humain"
    if confiance is None:
        return "claude"
    if confiance >= SEUIL_AUTO and ACTIONS_AUTO.get(categorie):
        return "auto"
    if confiance >= SEUIL_CLAUDE:
        return "claude"
    return "humain"


def jev(texte, cle):
    corps = json.dumps({"state": texte[:6000], "model": "jev-latest",
                        "questions": QUESTIONS}).encode()
    if cle:
        req = urllib.request.Request(API, data=corps, headers={
            "Authorization": f"Bearer {cle}", "Content-Type": "application/json"})
        reponse = urllib.request.urlopen(req, timeout=30)
    else:
        import base64
        import http.cookiejar
        pot = http.cookiejar.MozillaCookieJar(os.environ["JEV_COOKIES"])
        pot.load(ignore_discard=True, ignore_expires=True)
        ouvreur = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(pot))
        q = base64.urlsafe_b64encode(corps).decode().rstrip("=")
        reponse = ouvreur.open(f"{RELAIS}?q={q}", timeout=60)
    c = json.load(reponse)["answers"]["categorie"]
    return c["choice"], round(c["confidence"], 2), "jev"


def regles(texte):
    t = texte.lower()
    for cat, motif in (
        ("rejet_adresse", r"delivery status notification|couldn'?t be created|address not found|may not exist"),
        ("absence", r"out of (the )?office|on vacation|on leave until"),
        ("accuse_reception", r"just confirming|request .*(received|has been received)|auto-?reply|we have received your"),
        ("refus", r"not interested|decline|no thanks|we (are|will be) (migrat|releas)|already (migrat|working on)"),
        ("interet", r"\binterested\b|let'?s talk|schedule a call|\bterms\b|happy to discuss|open to"),
    ):
        if re.search(motif, t):
            return cat, None, "regles"
    return ("question" if "?" in t else "hors_sujet"), None, "regles"


def main():
    cle = os.environ.get("TYPESAFE_API_KEY")
    jev_dispo = bool(cle or os.environ.get("JEV_COOKIES"))
    for chemin in sys.argv[1:] or ["-"]:
        texte = sys.stdin.read() if chemin == "-" else open(chemin, encoding="utf-8").read()
        erreur = None
        try:
            cat, conf, moteur = jev(texte, cle) if jev_dispo else regles(texte)
        except Exception as e:  # réseau, quota : repli sans bloquer
            cat, conf, moteur = regles(texte)
            erreur = str(e)[:120]
        voie = aiguiller(cat, conf)
        res = {"source": chemin, "categorie": cat, "confiance": conf, "moteur": moteur,
               "aiguillage": voie,
               "action": ACTIONS_AUTO.get(cat) if voie == "auto" else None}
        if erreur:
            res["erreur_jev"] = erreur
        print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
